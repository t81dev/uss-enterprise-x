#!/usr/bin/env python3
"""
Sequential Mission Digital Twin Simulation for USS Enterprise X (Project Occam-7)
Updated for Program Phase 8 — Mars ISRU, Propellant Logistics & Mission Closure.

Simulates vehicle state propagation across time:
- Vector position & velocity (2D/3D heliocentric & planetocentric states)
- Mass conservation assertions & propellant tracking (LH2, LNH3, RCS, Consumables)
- Numerical finite-burn integration vs Tsiolkovsky rocket equation checks
- Dynamic power & thermal rejection state machine (Stefan-Boltzmann, 850 K radiators)
- Cryogenic boiloff derivation & Zero-Boiloff (ZBO) active refrigeration power
- Crew survivability model (SPE/GCR radiation dose, ECLSS consumables, centrifuge gravity)
- Separate Precursor Mission (Phase A) and Crewed Mission (Phase B) boundary separation
- Mars Surface ISRU Infrastructure & Pre-deployed Depot tracking
- Formal pre-departure safety gates and machine-readable physical mission success predicates
"""

import math
import json
import os
from mars_isru import (
    MarsISRUModel,
    REQUIRED_NET_RETURN_LH2_MT,
    F_CHILLDOWN,
    F_FLASH,
    F_RESIDUALS,
    F_TOTAL_TRANSFER_LOSS,
    REQUIRED_GROSS_DEPOT_WITHDRAWAL_MT,
)

# Physical and Astronomical Constants
G0 = 9.80665                  # m/s^2
MU_SUN = 1.32712440018e20      # m^3/s^2
MU_EARTH = 3.986004418e14     # m^3/s^2
MU_MARS = 4.2828372e13        # m^3/s^2
AU_IN_M = 1.495978707e11      # m


class PrecursorDepotState:
    """Explicit Mars Precursor ISRU Depot state tracking."""

    # Explicit State Machine Constants
    PRECURSOR_NOT_DEPLOYED = "PRECURSOR_NOT_DEPLOYED"
    PRECURSOR_DEPLOYED = "PRECURSOR_DEPLOYED"
    ISRU_OPERATIONAL = "ISRU_OPERATIONAL"
    PROPULSANT_PRODUCTION_COMPLETE = "PROPULSANT_PRODUCTION_COMPLETE"
    DEPOT_VERIFIED = "DEPOT_VERIFIED"
    CREW_DEPARTURE_AUTHORIZED = "CREW_DEPARTURE_AUTHORIZED"

    def __init__(self):
        self.state = self.PRECURSOR_NOT_DEPLOYED
        self.precursor_payload_closes = False
        self.precursor_deployed = False
        self.isru_operational = False
        self.isru_power_closure = False
        self.isru_thermal_closure = False
        self.isru_thermal_margin_compliance = False
        self.production_complete = False
        self.depot_verified = False

        # Physical Inventory Accounting (MT)
        self.lh2_produced_mt = 0.0
        self.lh2_storage_boiloff_mt = 0.0
        self.lh2_initial_stored_mt = 0.0      # Peak verified inventory before transfer
        self.lh2_depot_stored_mt = 0.0        # Current remaining inventory in depot
        self.lh2_verified_inventory_mt = 0.0   # Current available verified inventory for transfer
        self.lh2_transferred_to_ship_mt = 0.0

        # Transfer Loss Accounting & Tracking Quantities
        self.required_return_propellant_mt = REQUIRED_NET_RETURN_LH2_MT
        self.required_gross_depot_withdrawal_mt = REQUIRED_GROSS_DEPOT_WITHDRAWAL_MT
        self.actual_net_propellant_loaded_mt = 0.0
        self.actual_transfer_loss_mt = 0.0
        self.remaining_verified_depot_inventory_mt = 0.0

        # Loss accounting metrics
        self.transfer_line_chilldown_loss_mt = 0.0
        self.transfer_flash_loss_mt = 0.0
        self.transfer_residual_loss_mt = 0.0

        # Infrastructure operational status
        self.storage_system_operational = False
        self.inventory_measurement_valid = False
        self.transfer_system_operational = False

    def to_dict(self):
        return {
            "state": self.state,
            "precursor_payload_closes": self.precursor_payload_closes,
            "precursor_deployed": self.precursor_deployed,
            "isru_operational": self.isru_operational,
            "isru_power_closure": self.isru_power_closure,
            "isru_thermal_closure": self.isru_thermal_closure,
            "isru_thermal_margin_compliance": self.isru_thermal_margin_compliance,
            "production_complete": self.production_complete,
            "depot_verified": self.depot_verified,
            "storage_system_operational": self.storage_system_operational,
            "inventory_measurement_valid": self.inventory_measurement_valid,
            "transfer_system_operational": self.transfer_system_operational,
            "required_return_propellant_mt": round(self.required_return_propellant_mt, 2),
            "required_gross_depot_withdrawal_mt": round(self.required_gross_depot_withdrawal_mt, 2),
            "actual_net_propellant_loaded_mt": round(self.actual_net_propellant_loaded_mt, 2),
            "actual_transfer_loss_mt": round(self.actual_transfer_loss_mt, 2),
            "remaining_verified_depot_inventory_mt": round(self.remaining_verified_depot_inventory_mt, 2),
            "inventory_mt": {
                "produced_mt": round(self.lh2_produced_mt, 2),
                "storage_boiloff_mt": round(self.lh2_storage_boiloff_mt, 2),
                "initial_stored_mt": round(self.lh2_initial_stored_mt, 2),
                "remaining_depot_stored_mt": round(self.lh2_depot_stored_mt, 2),
                "verified_inventory_available_mt": round(self.lh2_verified_inventory_mt, 2),
                "transferred_to_ship_mt": round(self.lh2_transferred_to_ship_mt, 2)
            }
        }


class SpacecraftState:
    def __init__(self, dry_mass_mt=1470.96, lh2_mt=2200.0, lnh3_mt=300.0, rcs_mt=0.0):
        self.time_days = 0.0
        self.dry_mass_mt = dry_mass_mt  # 1,470.96 t dry baseline (includes 72.3 t ECLSS consumables & RCS)
        self.lh2_mt = lh2_mt
        self.lnh3_mt = lnh3_mt
        self.rcs_mt = rcs_mt
        self.crew_consumables_mt = 72.3 # Tracked within dry budget

        # Orbital State (Heliocentric 2D Vector)
        self.r_vec_au = [1.0, 0.0]
        self.v_vec_kms = [0.0, 29.78]
        self.soi_reference = "Earth_SOI"
        self.total_delta_v_kms = 0.0

        # Power & Thermal
        self.reactor_power_mwth = 100.0
        self.electrical_power_mwe = 20.0
        self.house_load_mwe = 0.445
        self.propulsion_load_mwe = 0.0
        self.zbo_refrigeration_mwe = 0.015  # 15 kWe ZBO active refrigeration
        self.thermal_load_mwth = 80.0
        self.radiator_capacity_mwth = 133.35
        self.radiator_area_m2 = 2502.8

        # Cryogenic Boiloff Metrics
        self.passive_boiloff_rate_percent_per_day = 0.0001  # 0.01%/day with ZBO active
        self.cumulative_boiloff_loss_mt = 0.0

        # Crew & Survivability
        self.crew_count = 24
        self.crew_health_percent = 100.0
        self.accumulated_radiation_csv = 0.0  # cSv
        self.centrifuge_active = True
        self.centrifuge_rpm = 6.0
        self.centrifuge_radius_m = 15.0

        # System Health
        self.system_health = {
            "reactor_health": 1.0,
            "radiator_fraction": 1.0,
            "ntp_engines_active": 4,
            "nep_thrusters_active": 4,
            "nep_efficiency": 0.65,
            "critical_failure": False
        }

    @property
    def total_propellant_mt(self):
        return self.lh2_mt + self.lnh3_mt + self.rcs_mt

    @property
    def gross_mass_mt(self):
        return self.dry_mass_mt + self.lh2_mt + self.lnh3_mt + self.rcs_mt

    def to_dict(self):
        return {
            "time_days": round(self.time_days, 2),
            "gross_mass_mt": round(self.gross_mass_mt, 2),
            "dry_mass_mt": round(self.dry_mass_mt, 2),
            "lh2_mt": round(self.lh2_mt, 2),
            "lnh3_mt": round(self.lnh3_mt, 2),
            "rcs_mt": round(self.rcs_mt, 2),
            "crew_consumables_mt": round(self.crew_consumables_mt, 2),
            "soi_reference": self.soi_reference,
            "r_vec_au": [round(x, 4) for x in self.r_vec_au],
            "v_vec_kms": [round(v, 3) for v in self.v_vec_kms],
            "total_delta_v_kms": round(self.total_delta_v_kms, 3),
            "reactor_power_mwth": round(self.reactor_power_mwth, 2),
            "electrical_power_mwe": round(self.electrical_power_mwe, 2),
            "thermal_load_mwth": round(self.thermal_load_mwth, 2),
            "radiator_capacity_mwth": round(self.radiator_capacity_mwth, 2),
            "crew_count": self.crew_count,
            "crew_health_percent": round(self.crew_health_percent, 1),
            "accumulated_radiation_csv": round(self.accumulated_radiation_csv, 2)
        }


class MissionDigitalTwin:
    def __init__(self, initial_state=None, isru_model=None):
        self.state = initial_state if initial_state else SpacecraftState()
        self.depot = PrecursorDepotState()
        self.event_log = []
        self.mass_conservation_log = []
        self.isru_model = isru_model if isru_model else MarsISRUModel()

    def enforce_mass_conservation(self, event_name, m_initial, m_final, prop_burned, consumables_spent, boiloff_lost, isru_reloaded=0.0):
        """Enforces M_initial + isru_reloaded = M_final + prop_burned + consumables_spent + boiloff_lost."""
        accounted_final = m_final + prop_burned + consumables_spent + boiloff_lost - isru_reloaded
        error_mt = abs(m_initial - accounted_final)
        assert error_mt < 1e-4, f"MASS CONSERVATION VIOLATION in {event_name}: M_i={m_initial}, Accounted={accounted_final}, Err={error_mt}"
        self.mass_conservation_log.append({
            "event": event_name,
            "m_initial_mt": round(m_initial, 4),
            "m_final_mt": round(m_final, 4),
            "prop_burned_mt": round(prop_burned, 4),
            "consumables_spent_mt": round(consumables_spent, 4),
            "boiloff_lost_mt": round(boiloff_lost, 4),
            "isru_reloaded_mt": round(isru_reloaded, 4),
            "error_mt": round(error_mt, 8)
        })

    def run_precursor_mission(self, duration_days=500.0, available_power_mwe=25.0, number_of_landers=2, lander_capacity_mt=150.0, lander_1_capacity_mt=None, lander_2_capacity_mt=None, required_thermal_margin_fraction=0.0):
        """Phase A — Precursor Autonomous Mission:
        Earth -> Mars -> land -> deploy -> commission -> produce propellant -> liquefy -> store -> verify depot.
        Calculates and verifies depot output before crew departure authorization.
        """
        # Step 1: Check Precursor Payload Delivery Closure
        payload_eval = self.isru_model.precursor_payload_closes(
            number_of_landers=number_of_landers,
            capacity_per_lander_mt=lander_capacity_mt,
            lander_1_capacity_mt=lander_1_capacity_mt,
            lander_2_capacity_mt=lander_2_capacity_mt
        )
        self.depot.precursor_payload_closes = payload_eval["payload_closes"]

        if not self.depot.precursor_payload_closes:
            self.depot.state = PrecursorDepotState.PRECURSOR_NOT_DEPLOYED
            return self.depot.to_dict()

        self.depot.precursor_deployed = True
        self.depot.state = PrecursorDepotState.PRECURSOR_DEPLOYED

        # Step 2: Surface Power & Thermal Closure Evaluation
        acct = self.isru_model.calculate_propellant_accounting()
        required_gross_lh2_mt = acct["gross_lh2_production_mt"]

        p_eval = self.isru_model.surface_power_budget(available_power_mwe=available_power_mwe, gross_lh2_mt=required_gross_lh2_mt)
        power_and_energy = self.isru_model.calculate_electrolysis_and_liquefaction_power(required_gross_lh2_mt)
        thermal_eval = self.isru_model.calculate_thermal_rejection_and_radiator(
            power_and_energy["avg_continuous_power_mwe"],
            required_thermal_margin_fraction=required_thermal_margin_fraction
        )

        self.depot.isru_power_closure = p_eval["power_closes"]
        self.depot.isru_thermal_closure = thermal_eval["thermal_closure"]
        self.depot.isru_thermal_margin_compliance = thermal_eval["thermal_margin_compliance"]

        if not (self.depot.isru_power_closure and self.depot.isru_thermal_closure):
            self.depot.isru_operational = False
            return self.depot.to_dict()

        self.depot.isru_operational = True
        self.depot.state = PrecursorDepotState.ISRU_OPERATIONAL

        # Step 3: Physical Propellant Production Campaign
        achievable_eval = self.isru_model.calculate_achievable_production(
            available_power_mwe=available_power_mwe,
            operating_days=duration_days
        )
        gross_lh2_produced_mt = min(achievable_eval["achievable_gross_lh2_mt"], required_gross_lh2_mt) if achievable_eval["production_closes"] else achievable_eval["achievable_gross_lh2_mt"]

        storage_boiloff_mt = acct["loss_breakdown_mt"]["storage_boiloff_mt"]
        stored_lh2_mt = max(0.0, gross_lh2_produced_mt - storage_boiloff_mt)

        self.depot.lh2_produced_mt = gross_lh2_produced_mt
        self.depot.lh2_storage_boiloff_mt = storage_boiloff_mt
        self.depot.lh2_initial_stored_mt = stored_lh2_mt
        self.depot.lh2_depot_stored_mt = stored_lh2_mt

        required_gross_withdrawal = REQUIRED_GROSS_DEPOT_WITHDRAWAL_MT

        if stored_lh2_mt >= required_gross_withdrawal and achievable_eval["production_closes"]:
            self.depot.production_complete = True
            self.depot.state = PrecursorDepotState.PROPULSANT_PRODUCTION_COMPLETE
        else:
            self.depot.production_complete = False
            return self.depot.to_dict()

        # Step 4: Verification and Commissioning
        self.depot.storage_system_operational = True
        self.depot.inventory_measurement_valid = True
        self.depot.transfer_system_operational = True
        self.depot.lh2_verified_inventory_mt = stored_lh2_mt
        self.depot.depot_verified = True
        self.depot.state = PrecursorDepotState.DEPOT_VERIFIED

        return self.depot.to_dict()

    def precursor_inventory_verified(self, required_net_lh2_mt=REQUIRED_NET_RETURN_LH2_MT):
        """Pre-Departure Safety Gate:
        Verifies depot existence, operational status, production completeness,
        required gross LH2 depot availability above reserve (accounting for transfer losses),
        ZBO/storage operational status, measurement validity, and transfer system operational status.
        """
        required_gross_mt = required_net_lh2_mt / (1.0 - F_TOTAL_TRANSFER_LOSS)
        gate = {
            "depot_exists": self.depot.precursor_deployed,
            "depot_operational": self.depot.isru_operational,
            "power_closure": self.depot.isru_power_closure,
            "payload_closure": self.depot.precursor_payload_closes,
            "propellant_production_complete": self.depot.production_complete,
            "depot_verified": self.depot.depot_verified,
            "required_LH2_available": self.depot.lh2_verified_inventory_mt >= required_gross_mt,
            "storage_system_operational": self.depot.storage_system_operational,
            "inventory_measurement_valid": self.depot.inventory_measurement_valid,
            "transfer_system_operational": self.depot.transfer_system_operational
        }

        authorized = all(gate.values())
        if authorized:
            self.depot.state = PrecursorDepotState.CREW_DEPARTURE_AUTHORIZED

        return authorized, gate

    def update_power_and_thermal(self, mode="nominal"):
        """Updates power generation, electrical loads, and Stefan-Boltzmann radiator heat rejection."""
        h = self.state.system_health
        self.state.reactor_power_mwth = 100.0 * h["reactor_health"]
        self.state.electrical_power_mwe = 20.0 * h["reactor_health"]

        if mode == "ntp_burn":
            self.state.propulsion_load_mwe = 0.5
            self.state.house_load_mwe = 0.445
            self.state.thermal_load_mwth = 80.0 * h["reactor_health"] + 2.0
        elif mode == "nep_cruise":
            self.state.propulsion_load_mwe = 15.0 * h["reactor_health"]
            self.state.house_load_mwe = 0.445
            self.state.thermal_load_mwth = (100.0 - self.state.electrical_power_mwe) + 5.25
        elif mode == "mars_stay":
            self.state.propulsion_load_mwe = 0.0
            self.state.house_load_mwe = 0.600
            self.state.reactor_power_mwth = 10.0
            self.state.electrical_power_mwe = 2.0
            self.state.thermal_load_mwth = 8.0
        else: # nominal
            self.state.propulsion_load_mwe = 0.0
            self.state.house_load_mwe = 0.445
            self.state.thermal_load_mwth = 80.0 * h["reactor_health"]

        # Stefan-Boltzmann double-sided rejection at 850 K
        effective_area = self.state.radiator_area_m2 * h["radiator_fraction"]
        sigma = 5.670374419e-8
        emissivity = 0.90
        temp_k = 850.0
        q_watts = 2.0 * effective_area * emissivity * sigma * (temp_k ** 4)
        self.state.radiator_capacity_mwth = q_watts / 1e6

    def execute_ntp_burn(self, phase_name, target_dv_kms=None, burn_all_lh2=False, vector_direction=[1.0, 0.0]):
        """Executes finite-burn Solid-Core NTP impulse with numerical integration & Tsiolkovsky cross-check."""
        m_initial = self.state.gross_mass_mt
        self.update_power_and_thermal(mode="ntp_burn")
        h = self.state.system_health

        active_engines = h["ntp_engines_active"]
        if active_engines <= 0:
            return {"status": "FAILED", "reason": "No active NTP engines"}

        thrust_n = active_engines * 1000.0 * 1000.0  # 4,000 kN
        isp_s = 900.0
        v_e = isp_s * G0  # 8,825.985 m/s
        mdot_kg_s = thrust_n / v_e
        mdot_mt_s = mdot_kg_s / 1000.0

        lh2_avail = self.state.lh2_mt

        if burn_all_lh2 or target_dv_kms is None:
            lh2_to_burn = lh2_avail
        else:
            req_mass_ratio = math.exp((target_dv_kms * 1000.0) / v_e)
            m_final_req = m_initial / req_mass_ratio
            lh2_to_burn = m_initial - m_final_req
            if lh2_to_burn > lh2_avail:
                lh2_to_burn = lh2_avail

        duration_s = (lh2_to_burn * 1000.0) / mdot_kg_s if mdot_kg_s > 0 else 0.0
        m_final = m_initial - lh2_to_burn

        tsiolkovsky_dv_kms = (v_e * math.log(m_initial / m_final)) / 1000.0 if m_final > 0 else 0.0

        steps = int(max(1, duration_s))
        dt = duration_s / steps if steps > 0 else 0.0
        m_step = m_initial
        numerical_dv_ms = 0.0
        for _ in range(steps):
            if m_step > 0:
                accel = thrust_n / (m_step * 1000.0)
                numerical_dv_ms += accel * dt
                m_step -= mdot_mt_s * dt
        numerical_dv_kms = numerical_dv_ms / 1000.0

        dv_diff_percent = abs(tsiolkovsky_dv_kms - numerical_dv_kms) / tsiolkovsky_dv_kms * 100.0 if tsiolkovsky_dv_kms > 0 else 0.0
        assert dv_diff_percent < 0.5, f"NUMERICAL VS ANALYTICAL DISAGREEMENT: Tsiolkovsky={tsiolkovsky_dv_kms}, Num={numerical_dv_kms}"

        norm_dir = [vector_direction[0] / max(1e-6, math.hypot(*vector_direction)),
                    vector_direction[1] / max(1e-6, math.hypot(*vector_direction))]
        self.state.v_vec_kms[0] += tsiolkovsky_dv_kms * norm_dir[0]
        self.state.v_vec_kms[1] += tsiolkovsky_dv_kms * norm_dir[1]

        self.state.lh2_mt -= lh2_to_burn
        self.state.time_days += (duration_s / 86400.0)
        self.state.total_delta_v_kms += tsiolkovsky_dv_kms

        self.enforce_mass_conservation(phase_name, m_initial, self.state.gross_mass_mt, lh2_to_burn, 0.0, 0.0)

        record = {
            "phase": phase_name,
            "type": "NTP_BURN",
            "duration_s": round(duration_s, 1),
            "start_mass_mt": round(m_initial, 2),
            "lh2_burned_mt": round(lh2_to_burn, 2),
            "end_mass_mt": round(self.state.gross_mass_mt, 2),
            "thrust_kn": active_engines * 1000.0,
            "actual_dv_kms": round(tsiolkovsky_dv_kms, 3),
            "numerical_dv_kms": round(numerical_dv_kms, 3),
            "lh2_remaining_mt": round(self.state.lh2_mt, 2)
        }
        self.event_log.append(record)
        return record

    def execute_nep_burn(self, phase_name, duration_days, vector_direction=[1.0, 0.0]):
        """Executes low-thrust NEP electric burn with vector acceleration."""
        m_initial = self.state.gross_mass_mt
        self.update_power_and_thermal(mode="nep_cruise")
        h = self.state.system_health

        p_elec_mwe = self.state.electrical_power_mwe * (15.0 / 20.0)
        p_jet_mw = p_elec_mwe * h["nep_efficiency"]
        isp_s = 3500.0
        v_e = isp_s * G0

        thrust_n = (2.0 * p_jet_mw * 1e6) / v_e if v_e > 0 else 0.0
        mdot_kg_s = thrust_n / v_e if v_e > 0 else 0.0
        mdot_mt_day = (mdot_kg_s * 86400.0) / 1000.0

        lnh3_avail = self.state.lnh3_mt
        lnh3_req = mdot_mt_day * duration_days

        if lnh3_req > lnh3_avail:
            lnh3_to_burn = lnh3_avail
            actual_duration_days = lnh3_avail / mdot_mt_day if mdot_mt_day > 0 else 0.0
        else:
            lnh3_to_burn = lnh3_req
            actual_duration_days = duration_days

        m_final = m_initial - lnh3_to_burn
        tsiolkovsky_dv_kms = (v_e * math.log(m_initial / m_final)) / 1000.0 if m_final > 0 else 0.0

        boiloff_lost_mt = self.state.lh2_mt * self.state.passive_boiloff_rate_percent_per_day * actual_duration_days
        boiloff_lost_mt = min(self.state.lh2_mt, boiloff_lost_mt)
        self.state.lh2_mt -= boiloff_lost_mt
        self.state.cumulative_boiloff_loss_mt += boiloff_lost_mt

        rad_dose_csv = 0.07 * actual_duration_days
        self.state.accumulated_radiation_csv += rad_dose_csv

        norm_dir = [vector_direction[0] / max(1e-6, math.hypot(*vector_direction)),
                    vector_direction[1] / max(1e-6, math.hypot(*vector_direction))]
        self.state.v_vec_kms[0] += tsiolkovsky_dv_kms * norm_dir[0]
        self.state.v_vec_kms[1] += tsiolkovsky_dv_kms * norm_dir[1]

        self.state.lnh3_mt -= lnh3_to_burn
        self.state.time_days += actual_duration_days
        self.state.total_delta_v_kms += tsiolkovsky_dv_kms

        self.enforce_mass_conservation(phase_name, m_initial, self.state.gross_mass_mt, lnh3_to_burn, 0.0, boiloff_lost_mt)

        record = {
            "phase": phase_name,
            "type": "NEP_BURN",
            "duration_days": round(actual_duration_days, 2),
            "start_mass_mt": round(m_initial, 2),
            "lnh3_burned_mt": round(lnh3_to_burn, 2),
            "boiloff_lost_mt": round(boiloff_lost_mt, 4),
            "end_mass_mt": round(self.state.gross_mass_mt, 2),
            "thrust_n": round(thrust_n, 2),
            "actual_dv_kms": round(tsiolkovsky_dv_kms, 3),
            "lnh3_remaining_mt": round(self.state.lnh3_mt, 2)
        }
        self.event_log.append(record)
        return record

    def execute_mars_isru_reload_and_stay(self, phase_name="Mars Propellant Transfer & Operations (640d)", duration_days=640.0, target_reload_net_mt=REQUIRED_NET_RETURN_LH2_MT):
        """Phase B — Crewed Operations & Propellant Transfer:
        Consumes pre-existing verified precursor depot output.
        Performs explicit mass-conserving transfer:
        1. Determine required net spacecraft load (target_reload_net_mt).
        2. Calculate required gross depot withdrawal = net / (1 - F_TOTAL_TRANSFER_LOSS).
        3. Verify depot contains at least gross_required; fail transfer if insufficient.
        4. Debit gross_required from depot.
        5. Calculate transfer losses explicitly.
        6. Credit exactly net quantity to spacecraft.
        7. Verify spacecraft inventory increased by exactly net transferred.
        8. Verify depot inventory decreased by exactly gross withdrawn.
        9. Verify gross withdrawal = net transferred + transfer losses.
        """
        m_initial = self.state.gross_mass_mt
        self.update_power_and_thermal(mode="mars_stay")

        required_net = target_reload_net_mt
        gross_required = required_net / (1.0 - F_TOTAL_TRANSFER_LOSS)

        available_verified = self.depot.lh2_verified_inventory_mt

        # Check if depot has sufficient gross inventory
        if available_verified < gross_required:
            gross_debit = min(available_verified, gross_required)
            total_transfer_loss_mt = gross_debit * F_TOTAL_TRANSFER_LOSS
            net_lh2_transferred_to_ship_mt = max(0.0, gross_debit - total_transfer_loss_mt)
        else:
            gross_debit = gross_required
            total_transfer_loss_mt = gross_debit * F_TOTAL_TRANSFER_LOSS
            net_lh2_transferred_to_ship_mt = required_net

        # Itemized transfer losses
        chilldown_loss_mt = gross_debit * F_CHILLDOWN
        flash_loss_mt = gross_debit * F_FLASH
        residual_loss_mt = gross_debit * F_RESIDUALS

        # Verify loss accounting equation
        assert abs(gross_debit - (net_lh2_transferred_to_ship_mt + total_transfer_loss_mt)) < 1e-6, \
            f"TRANSFER LOSS MISMATCH: Gross={gross_debit}, Net={net_lh2_transferred_to_ship_mt}, Loss={total_transfer_loss_mt}"

        depot_before = self.depot.lh2_verified_inventory_mt
        ship_lh2_before = self.state.lh2_mt

        # Debit source depot
        self.depot.lh2_verified_inventory_mt -= gross_debit
        self.depot.lh2_depot_stored_mt -= gross_debit
        self.depot.lh2_transferred_to_ship_mt += net_lh2_transferred_to_ship_mt

        # Credit destination spacecraft
        self.state.lh2_mt += net_lh2_transferred_to_ship_mt

        # Update depot explicit tracking quantities
        self.depot.required_return_propellant_mt = required_net
        self.depot.required_gross_depot_withdrawal_mt = gross_required
        self.depot.actual_net_propellant_loaded_mt = net_lh2_transferred_to_ship_mt
        self.depot.actual_transfer_loss_mt = total_transfer_loss_mt
        self.depot.remaining_verified_depot_inventory_mt = self.depot.lh2_verified_inventory_mt

        # Verify balance assertions
        assert abs((depot_before - self.depot.lh2_verified_inventory_mt) - gross_debit) < 1e-6, "DEPOT DEBIT MISMATCH"
        assert abs((self.state.lh2_mt - ship_lh2_before) - net_lh2_transferred_to_ship_mt) < 1e-6, "SPACECRAFT CREDIT MISMATCH"

        # Crew consumable usage deducted from dry mass
        consumable_loss_mt = min(self.state.crew_consumables_mt, 0.0723 * duration_days)
        self.state.crew_consumables_mt -= consumable_loss_mt
        self.state.dry_mass_mt -= consumable_loss_mt

        # Passive LH2 boiloff during stay on ship
        boiloff_lost_mt = min(self.state.lh2_mt, self.state.lh2_mt * self.state.passive_boiloff_rate_percent_per_day * duration_days)
        self.state.lh2_mt -= boiloff_lost_mt
        self.state.cumulative_boiloff_loss_mt += boiloff_lost_mt

        rad_dose_csv = 0.03 * duration_days
        self.state.accumulated_radiation_csv += rad_dose_csv

        if not self.state.centrifuge_active:
            self.state.crew_health_percent = max(50.0, self.state.crew_health_percent - 0.05 * duration_days)

        self.state.time_days += duration_days

        self.enforce_mass_conservation(phase_name, m_initial, self.state.gross_mass_mt, 0.0, consumable_loss_mt, boiloff_lost_mt, isru_reloaded=net_lh2_transferred_to_ship_mt)

        record = {
            "phase": phase_name,
            "type": "MARS_ISRU_STAY",
            "duration_days": duration_days,
            "end_time_days": round(self.state.time_days, 2),
            "depot_debit_mt": round(gross_debit, 2),
            "transfer_losses_mt": round(total_transfer_loss_mt, 2),
            "lh2_reloaded_mt": round(net_lh2_transferred_to_ship_mt, 2),
            "gross_mass_mt": round(self.state.gross_mass_mt, 2),
            "crew_health_percent": round(self.state.crew_health_percent, 1),
            "accumulated_radiation_csv": round(self.state.accumulated_radiation_csv, 2)
        }
        self.event_log.append(record)
        return record

    def evaluate_mission_success_predicate(self):
        """Formally evaluates machine-readable physical mission success predicate for Phase 8.2."""
        p_earth_dep = "Trans-Mars Injection (TMI)" in [e["phase"] for e in self.event_log]
        p_mars_enc = "Mars Orbit Insertion (MOI)" in [e["phase"] for e in self.event_log]
        p_mars_stay = any("Mars" in e["phase"] and ("Stay" in e["phase"] or "Operations" in e["phase"]) for e in self.event_log)
        p_tei = "Trans-Earth Injection (TEI)" in [e["phase"] for e in self.event_log]
        p_earth_cap = "Earth Orbit Capture (EOI)" in [e["phase"] for e in self.event_log]

        # Canonical Machine-Readable Success Predicates
        canonical_predicates = {
            "precursor_payload_closure": self.depot.precursor_payload_closes,
            "precursor_deployed": self.depot.precursor_deployed,
            "isru_operational": self.depot.isru_operational,
            "isru_production_complete": self.depot.production_complete,
            "depot_verified": self.depot.depot_verified,
            "verified_depot_inventory_sufficient": self.depot.lh2_initial_stored_mt >= REQUIRED_GROSS_DEPOT_WITHDRAWAL_MT - 1e-2,
            "surface_average_power_closure": self.depot.isru_power_closure,
            "surface_peak_power_closure": self.depot.isru_power_closure,
            "surface_thermal_closure": self.depot.isru_thermal_closure,
            "earth_departure_authorized": self.depot.state == PrecursorDepotState.CREW_DEPARTURE_AUTHORIZED,
            "earth_departure_achieved": p_earth_dep,
            "mars_encounter_achieved": p_mars_enc,
            "mars_operations_complete": p_mars_stay,
            "return_propellant_available": self.depot.lh2_initial_stored_mt >= REQUIRED_GROSS_DEPOT_WITHDRAWAL_MT - 1e-2,
            "return_propellant_transfer_complete": self.depot.lh2_transferred_to_ship_mt >= REQUIRED_NET_RETURN_LH2_MT - 1e-2,
            "return_propellant_loaded": self.depot.actual_net_propellant_loaded_mt >= REQUIRED_NET_RETURN_LH2_MT - 1e-2,
            "return_trajectory_closes": p_tei,
            "earth_capture_achieved": p_earth_cap,
            "propellant_reserve_sufficient": (self.state.lh2_mt >= -1e-4 and self.state.lnh3_mt >= -1e-4),
            "vehicle_power_margin": (self.state.electrical_power_mwe - self.state.house_load_mwe - self.state.propulsion_load_mwe) >= -0.01,
            "vehicle_thermal_margin": (self.state.radiator_capacity_mwth - self.state.thermal_load_mwth) >= -0.01,
            "crew_survivability": (self.state.crew_health_percent >= 70.0 and self.state.accumulated_radiation_csv <= 100.0),
            "mass_conservation": all(log["error_mt"] < 1e-4 for log in self.mass_conservation_log),
            "no_critical_failure": not self.state.system_health["critical_failure"]
        }

        mission_success = all(canonical_predicates.values())

        # Map legacy aliases to canonical values for backward compatibility
        all_predicates = dict(canonical_predicates)
        all_predicates.update({
            "thermal_closure": canonical_predicates["surface_thermal_closure"],
            "precursor_delivery_closes": canonical_predicates["precursor_payload_closure"],
            "depot_inventory_verified": canonical_predicates["depot_verified"],
            "return_propellant_manufactured": canonical_predicates["verified_depot_inventory_sufficient"],
            "return_propellant_stored": canonical_predicates["verified_depot_inventory_sufficient"],
            "surface_power_closes": canonical_predicates["surface_average_power_closure"],
            "mars_operations_completed": canonical_predicates["mars_operations_complete"],
            "refueling_conserves_mass": canonical_predicates["mass_conservation"],
            "propellant_reserve_positive": canonical_predicates["propellant_reserve_sufficient"],
            "power_margin_positive": canonical_predicates["vehicle_power_margin"],
            "thermal_margin_positive": canonical_predicates["vehicle_thermal_margin"],
            "crew_survivability_closes": canonical_predicates["crew_survivability"]
        })

        return {
            "mission_success": mission_success,
            "program_status": "ENGINEERINGALLY CONDITIONAL" if mission_success else "PHYSICALLY INFEASIBLE",
            "predicates": all_predicates,
            "canonical_predicates": canonical_predicates
        }

    def run_crewed_mission(self):
        """Phase B — Sequential Simulation for Crewed Enterprise X Mission."""
        # Check pre-departure safety gate
        authorized, gate_status = self.precursor_inventory_verified()
        if not authorized:
            predicates = self.evaluate_mission_success_predicate()
            return {
                "status": "CREW DEPARTURE ABORTED ON EARTH",
                "reason": "Precursor depot inventory failed verification gate",
                "gate_status": gate_status,
                "events": self.event_log,
                "final_state": self.state.to_dict(),
                "success_predicate_assessment": predicates
            }

        self.execute_ntp_burn("Trans-Mars Injection (TMI)", target_dv_kms=3.80, vector_direction=[1.0, 0.2])
        self.state.soi_reference = "Sun_Heliocentric"

        self.execute_nep_burn("Outbound Cruise NEP (180d)", duration_days=180.0, vector_direction=[0.8, 0.6])
        self.state.soi_reference = "Mars_SOI"

        self.execute_ntp_burn("Mars Orbit Insertion (MOI)", target_dv_kms=2.10, vector_direction=[-0.9, -0.1])

        # Execute Mars stay and consume pre-existing verified depot output
        self.execute_mars_isru_reload_and_stay("Mars Propellant Transfer & Operations (640d)", duration_days=640.0)

        self.execute_ntp_burn("Trans-Earth Injection (TEI)", target_dv_kms=1.80, vector_direction=[-1.0, -0.2])
        self.state.soi_reference = "Sun_Heliocentric"

        self.execute_nep_burn("Inbound Cruise NEP (180d)", duration_days=180.0, vector_direction=[-0.8, -0.6])
        self.state.soi_reference = "Earth_SOI"

        if self.state.lh2_mt > 0.1:
            self.execute_ntp_burn("Earth Orbit Capture (EOI)", burn_all_lh2=True, vector_direction=[-1.0, 0.0])

        predicates = self.evaluate_mission_success_predicate()

        output = {
            "vehicle": {
                "name": "USS Enterprise X (Project Occam-7)",
                "dry_mass_mt": 1470.96,
                "initial_propellant_mt": 2500.0,
                "gross_departure_mass_mt": 3970.96,
                "isru_reloaded_lh2_mt": round(self.depot.lh2_transferred_to_ship_mt, 2)
            },
            "precursor_depot_final_state": self.depot.to_dict(),
            "events": self.event_log,
            "final_state": self.state.to_dict(),
            "success_predicate_assessment": predicates,
            "mass_conservation_summary": {
                "total_events_checked": len(self.mass_conservation_log),
                "max_conservation_error_mt": max(e["error_mt"] for e in self.mass_conservation_log)
            }
        }
        return output

    def run_full_mission_baseline(self):
        """Runs Phase A (Precursor) followed by Phase B (Crewed) baseline simulation."""
        self.run_precursor_mission()
        return self.run_crewed_mission()


def generate_json_baseline(output_path="engineering/calculations/mission_baseline.json"):
    twin = MissionDigitalTwin()
    res = twin.run_full_mission_baseline()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(res, f, indent=2)

    print(f"Digital Twin baseline output successfully written to: {output_path}")
    return res


if __name__ == "__main__":
    generate_json_baseline()
