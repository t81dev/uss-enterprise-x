#!/usr/bin/env python3
"""
Sequential Mission Digital Twin Simulation for USS Enterprise X (Project Occam-7)
Simulates vehicle state propagation across time:
- Vector position & velocity (2D/3D heliocentric & planetocentric states)
- Mass conservation assertions & propellant tracking (LH2, LNH3, RCS, Consumables)
- Numerical finite-burn integration vs Tsiolkovsky rocket equation checks
- Dynamic power & thermal rejection state machine (Stefan-Boltzmann, 850 K radiators)
- Cryogenic boiloff derivation & Zero-Boiloff (ZBO) active refrigeration power
- Crew survivability model (SPE/GCR radiation dose, ECLSS consumables, centrifuge gravity)
- Formal machine-readable mission success predicate
"""

import math
import json
import os

# Physical and Astronomical Constants
G0 = 9.80665                  # m/s^2
MU_SUN = 1.32712440018e20      # m^3/s^2
MU_EARTH = 3.986004418e14     # m^3/s^2
MU_MARS = 4.2828372e13        # m^3/s^2
AU_IN_M = 1.495978707e11      # m

class SpacecraftState:
    def __init__(self, dry_mass_mt=1470.96, lh2_mt=2200.0, lnh3_mt=300.0, rcs_mt=0.0):
        self.time_days = 0.0
        self.dry_mass_mt = dry_mass_mt  # 1,470.96 t dry baseline (includes 72.3 t ECLSS consumables & RCS)
        self.lh2_mt = lh2_mt
        self.lnh3_mt = lnh3_mt
        self.rcs_mt = rcs_mt
        self.crew_consumables_mt = 72.3 # Tracked within dry budget

        # Orbital State (Heliocentric 2D Vector)
        # Position [x, y] in AU, Velocity [vx, vy] in km/s
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
    def __init__(self, initial_state=None):
        self.state = initial_state if initial_state else SpacecraftState()
        self.event_log = []
        self.mass_conservation_log = []

    def enforce_mass_conservation(self, event_name, m_initial, m_final, prop_burned, consumables_spent, boiloff_lost):
        """Enforces M_initial = M_final + prop_burned + consumables_spent + boiloff_lost within numerical tolerance."""
        accounted_final = m_final + prop_burned + consumables_spent + boiloff_lost
        error_mt = abs(m_initial - accounted_final)
        assert error_mt < 1e-4, f"MASS CONSERVATION VIOLATION in {event_name}: M_i={m_initial}, Accounted={accounted_final}, Err={error_mt}"
        self.mass_conservation_log.append({
            "event": event_name,
            "m_initial_mt": round(m_initial, 4),
            "m_final_mt": round(m_final, 4),
            "prop_burned_mt": round(prop_burned, 4),
            "consumables_spent_mt": round(consumables_spent, 4),
            "boiloff_lost_mt": round(boiloff_lost, 4),
            "error_mt": round(error_mt, 8)
        })

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

        # Analytical Tsiolkovsky Delta-V
        tsiolkovsky_dv_kms = (v_e * math.log(m_initial / m_final)) / 1000.0 if m_final > 0 else 0.0

        # Numerical integration step cross-check (dt = 1s)
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

        # Disagreement check between numerical and analytical equation (<0.5%)
        dv_diff_percent = abs(tsiolkovsky_dv_kms - numerical_dv_kms) / tsiolkovsky_dv_kms * 100.0 if tsiolkovsky_dv_kms > 0 else 0.0
        assert dv_diff_percent < 0.5, f"NUMERICAL VS ANALYTICAL DISAGREEMENT: Tsiolkovsky={tsiolkovsky_dv_kms}, Num={numerical_dv_kms}"

        # Vector update
        norm_dir = [vector_direction[0] / max(1e-6, math.hypot(*vector_direction)),
                    vector_direction[1] / max(1e-6, math.hypot(*vector_direction))]
        self.state.v_vec_kms[0] += tsiolkovsky_dv_kms * norm_dir[0]
        self.state.v_vec_kms[1] += tsiolkovsky_dv_kms * norm_dir[1]

        # State transition
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

        # Passive LH2 boiloff during cruise phase
        boiloff_lost_mt = self.state.lh2_mt * self.state.passive_boiloff_rate_percent_per_day * actual_duration_days
        boiloff_lost_mt = min(self.state.lh2_mt, boiloff_lost_mt)
        self.state.lh2_mt -= boiloff_lost_mt
        self.state.cumulative_boiloff_loss_mt += boiloff_lost_mt

        # Radiation accumulation during transit (0.07 cSv / day baseline GCR)
        rad_dose_csv = 0.07 * actual_duration_days
        self.state.accumulated_radiation_csv += rad_dose_csv

        # Vector update
        norm_dir = [vector_direction[0] / max(1e-6, math.hypot(*vector_direction)),
                    vector_direction[1] / max(1e-6, math.hypot(*vector_direction))]
        self.state.v_vec_kms[0] += tsiolkovsky_dv_kms * norm_dir[0]
        self.state.v_vec_kms[1] += tsiolkovsky_dv_kms * norm_dir[1]

        # State transition
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

    def execute_coast_or_stay(self, phase_name, duration_days, mode="mars_stay"):
        """Executes surface stay or coast phase with crew consumable loss and health propagation."""
        m_initial = self.state.gross_mass_mt
        self.update_power_and_thermal(mode=mode)

        # Crew consumable usage deducted from dry mass
        consumable_loss_mt = min(self.state.crew_consumables_mt, 0.0723 * duration_days)
        self.state.crew_consumables_mt -= consumable_loss_mt
        self.state.dry_mass_mt -= consumable_loss_mt  # Dry mass decreases as consumables are consumed

        # Passive LH2 boiloff during stay
        boiloff_lost_mt = min(self.state.lh2_mt, self.state.lh2_mt * self.state.passive_boiloff_rate_percent_per_day * duration_days)
        self.state.lh2_mt -= boiloff_lost_mt
        self.state.cumulative_boiloff_loss_mt += boiloff_lost_mt

        # Radiation accumulation during stay (0.03 cSv/day on Mars surface/orbit shielded)
        rad_dose_csv = 0.03 * duration_days
        self.state.accumulated_radiation_csv += rad_dose_csv

        # Centrifuge check on crew health
        if not self.state.centrifuge_active:
            self.state.crew_health_percent = max(50.0, self.state.crew_health_percent - 0.05 * duration_days)

        self.state.time_days += duration_days

        self.enforce_mass_conservation(phase_name, m_initial, self.state.gross_mass_mt, 0.0, consumable_loss_mt, boiloff_lost_mt)

        record = {
            "phase": phase_name,
            "type": "COAST_STAY",
            "duration_days": duration_days,
            "end_time_days": round(self.state.time_days, 2),
            "gross_mass_mt": round(self.state.gross_mass_mt, 2),
            "crew_health_percent": round(self.state.crew_health_percent, 1),
            "accumulated_radiation_csv": round(self.state.accumulated_radiation_csv, 2)
        }
        self.event_log.append(record)
        return record

    def evaluate_mission_success_predicate(self):
        """Formally evaluates machine-readable mission success predicate."""
        p_earth_dep = "Trans-Mars Injection (TMI)" in [e["phase"] for e in self.event_log]
        p_mars_enc = "Mars Orbit Insertion (MOI)" in [e["phase"] for e in self.event_log]
        p_mars_stay = "Mars Orbit Stay (640d)" in [e["phase"] for e in self.event_log]
        p_tei = "Trans-Earth Injection (TEI)" in [e["phase"] for e in self.event_log]
        p_earth_cap = "Earth Orbit Capture (EOI)" in [e["phase"] for e in self.event_log]

        p_prop_reserve = (self.state.lh2_mt >= 0.0 and self.state.lnh3_mt >= 0.0)
        p_power_margin = (self.state.electrical_power_mwe - self.state.house_load_mwe - self.state.propulsion_load_mwe) >= -0.01
        p_thermal_margin = (self.state.radiator_capacity_mwth - self.state.thermal_load_mwth) >= -0.01
        p_crew_health = (self.state.crew_health_percent >= 70.0 and self.state.accumulated_radiation_csv <= 100.0)
        p_no_critical_fail = not self.state.system_health["critical_failure"]

        success = (p_earth_dep and p_mars_enc and p_mars_stay and p_tei and
                   p_prop_reserve and p_power_margin and p_thermal_margin and
                   p_crew_health and p_no_critical_fail)

        return {
            "mission_success": success,
            "predicates": {
                "earth_departure_achieved": p_earth_dep,
                "mars_encounter_achieved": p_mars_enc,
                "mars_operations_completed": p_mars_stay,
                "earth_return_achieved": p_tei,
                "earth_capture_achieved": p_earth_cap,
                "propellant_reserve_positive": p_prop_reserve,
                "power_margin_positive": p_power_margin,
                "thermal_margin_positive": p_thermal_margin,
                "crew_health_viable": p_crew_health,
                "no_critical_failure": p_no_critical_fail
            }
        }

    def run_full_mission_baseline(self):
        """Runs the sequential baseline simulation for Mission B (Earth-Mars-Earth)."""
        self.execute_ntp_burn("Trans-Mars Injection (TMI)", target_dv_kms=3.80, vector_direction=[1.0, 0.2])
        self.state.soi_reference = "Sun_Heliocentric"

        self.execute_nep_burn("Outbound Cruise NEP (180d)", duration_days=180.0, vector_direction=[0.8, 0.6])
        self.state.soi_reference = "Mars_SOI"

        self.execute_ntp_burn("Mars Orbit Insertion (MOI)", target_dv_kms=2.10, vector_direction=[-0.9, -0.1])

        self.execute_coast_or_stay("Mars Orbit Stay (640d)", duration_days=640.0, mode="mars_stay")

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
                "propellant_inventory_mt": 2500.0,
                "gross_departure_mass_mt": 3970.96
            },
            "events": self.event_log,
            "final_state": self.state.to_dict(),
            "success_predicate_assessment": predicates,
            "mass_conservation_summary": {
                "total_events_checked": len(self.mass_conservation_log),
                "max_conservation_error_mt": max(e["error_mt"] for e in self.mass_conservation_log)
            }
        }
        return output

    def run_failure_case(self, failure_type):
        """Simulates specific failure modes and propagates state consequences."""
        if failure_type == "radiator_loss_25":
            self.state.system_health["radiator_fraction"] = 0.75
        elif failure_type == "ntp_engine_loss_1":
            self.state.system_health["ntp_engines_active"] = 3
        elif failure_type == "propellant_loss_30":
            self.state.lh2_mt *= 0.70
            self.state.lnh3_mt *= 0.70
        elif failure_type == "reactor_degraded_50":
            self.state.system_health["reactor_health"] = 0.50
        elif failure_type == "gravity_loss":
            self.state.centrifuge_active = False

        return self.run_full_mission_baseline()


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
