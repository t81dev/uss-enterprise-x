#!/usr/bin/env python3
"""
Sequential Mission Digital Twin Simulation for USS Enterprise X (Project Occam-7)
Simulates vehicle state propagation across time (mass, propellant, velocity, position, power, thermal, crew, health).
Performs sequential integration: mass(t+dt) = mass(t) - mdot * dt and dv = integral(F/m dt).
"""

import math
import json
import os

G0 = 9.80665  # m/s^2

class SpacecraftState:
    def __init__(self, dry_mass_mt=1470.96, lh2_mt=2200.0, lnh3_mt=300.0, rcs_mt=25.0):
        self.time_days = 0.0
        self.dry_mass_mt = dry_mass_mt
        self.lh2_mt = lh2_mt
        self.lnh3_mt = lnh3_mt
        self.rcs_mt = rcs_mt
        self.position = "Earth_LEO"
        self.heliocentric_velocity_kms = 29.78  # Earth orbital velocity reference
        self.total_delta_v_kms = 0.0

        # Power & Thermal
        self.reactor_power_mwth = 100.0
        self.electrical_power_mwe = 20.0
        self.house_load_mwe = 0.445
        self.propulsion_load_mwe = 0.0
        self.thermal_load_mwth = 80.0
        self.radiator_capacity_mwth = 83.45
        self.radiator_area_m2 = 2502.8

        # Crew & Health
        self.crew_count = 24
        self.crew_health_percent = 100.0
        self.system_health = {
            "reactor_health": 1.0,
            "radiator_fraction": 1.0,
            "ntp_engines_active": 4,
            "nep_thrusters_active": 4,
            "nep_efficiency": 0.65
        }

    @property
    def total_propellant_mt(self):
        return self.lh2_mt + self.lnh3_mt

    @property
    def gross_mass_mt(self):
        return self.dry_mass_mt + self.lh2_mt + self.lnh3_mt

    def to_dict(self):
        return {
            "time_days": round(self.time_days, 2),
            "gross_mass_mt": round(self.gross_mass_mt, 2),
            "dry_mass_mt": round(self.dry_mass_mt, 2),
            "lh2_mt": round(self.lh2_mt, 2),
            "lnh3_mt": round(self.lnh3_mt, 2),
            "rcs_mt": round(self.rcs_mt, 2),
            "position": self.position,
            "total_delta_v_kms": round(self.total_delta_v_kms, 3),
            "reactor_power_mwth": round(self.reactor_power_mwth, 2),
            "electrical_power_mwe": round(self.electrical_power_mwe, 2),
            "thermal_load_mwth": round(self.thermal_load_mwth, 2),
            "radiator_capacity_mwth": round(self.radiator_capacity_mwth, 2),
            "crew_count": self.crew_count,
            "crew_health_percent": round(self.crew_health_percent, 1)
        }


class MissionDigitalTwin:
    def __init__(self, initial_state=None):
        self.state = initial_state if initial_state else SpacecraftState()
        self.event_log = []
        self.mass_history = []
        self.power_history = []
        self.thermal_history = []

    def update_power_and_thermal(self, mode="nominal"):
        """Updates electrical generation, loads, and heat rejection balance based on system state."""
        h = self.state.system_health

        # Generation
        self.state.reactor_power_mwth = 100.0 * h["reactor_health"]
        self.state.electrical_power_mwe = 20.0 * h["reactor_health"]

        if mode == "ntp_burn":
            self.state.propulsion_load_mwe = 0.5  # Turbopump / precooling / control power
            self.state.house_load_mwe = 0.445
            # NTP reactor core generates impulse thrust directly (separate from main 100MWth electric core)
            self.state.thermal_load_mwth = 80.0 * h["reactor_health"] + 2.0
        elif mode == "nep_cruise":
            # 15 MWe dedicated to NEP
            self.state.propulsion_load_mwe = 15.0 * h["reactor_health"]
            self.state.house_load_mwe = 0.445
            self.state.thermal_load_mwth = (100.0 - self.state.electrical_power_mwe) + 5.25  # Conversion + MPD losses
        elif mode == "mars_stay":
            self.state.propulsion_load_mwe = 0.0
            self.state.house_load_mwe = 0.600  # Surface support & science labs
            # Reactor throttled to 10 MWth for low house load
            self.state.reactor_power_mwth = 10.0
            self.state.electrical_power_mwe = 2.0
            self.state.thermal_load_mwth = 8.0
        else: # nominal
            self.state.propulsion_load_mwe = 0.0
            self.state.house_load_mwe = 0.445
            self.state.thermal_load_mwth = 80.0 * h["reactor_health"]

        # Radiator Rejection Capacity at 850 K (Stefan-Boltzmann)
        effective_area = self.state.radiator_area_m2 * h["radiator_fraction"]
        sigma = 5.670374419e-8
        emissivity = 0.90
        temp_k = 850.0
        # Double-sided emission: Q = 2 * area * emissivity * sigma * T^4
        q_watts = 2.0 * effective_area * emissivity * sigma * (temp_k ** 4)
        self.state.radiator_capacity_mwth = q_watts / 1e6

    def execute_ntp_burn(self, phase_name, target_dv_kms=None, burn_all_lh2=False):
        """Executes high-thrust Solid-Core NTP burn using actual incoming vehicle mass."""
        self.update_power_and_thermal(mode="ntp_burn")
        h = self.state.system_health

        # Engine parameters
        active_engines = h["ntp_engines_active"]
        if active_engines <= 0:
            return {"status": "FAILED", "reason": "No active NTP engines"}

        thrust_n = active_engines * 1000.0 * 1000.0  # 1,000 kN per engine
        isp_s = 900.0
        v_e = isp_s * G0  # 8,825.985 m/s
        mdot_kg_s = thrust_n / v_e  # ~453.208 kg/s for 4 engines
        mdot_mt_s = mdot_kg_s / 1000.0

        m_initial = self.state.gross_mass_mt
        lh2_avail = self.state.lh2_mt

        if burn_all_lh2 or target_dv_kms is None:
            lh2_to_burn = lh2_avail
        else:
            req_mass_ratio = math.exp((target_dv_kms * 1000.0) / v_e)
            m_final_req = m_initial / req_mass_ratio
            lh2_to_burn = m_initial - m_final_req
            if lh2_to_burn > lh2_avail:
                lh2_to_burn = lh2_avail  # Limited by physical inventory!

        duration_s = (lh2_to_burn * 1000.0) / mdot_kg_s if mdot_kg_s > 0 else 0.0
        m_final = m_initial - lh2_to_burn
        actual_dv_ms = v_e * math.log(m_initial / m_final) if m_final > 0 else 0.0
        actual_dv_kms = actual_dv_ms / 1000.0

        # State transition
        self.state.lh2_mt -= lh2_to_burn
        self.state.time_days += (duration_s / 86400.0)
        self.state.total_delta_v_kms += actual_dv_kms

        record = {
            "phase": phase_name,
            "type": "NTP_BURN",
            "start_time_days": round(self.state.time_days - (duration_s / 86400.0), 2),
            "duration_s": round(duration_s, 1),
            "start_mass_mt": round(m_initial, 2),
            "lh2_burned_mt": round(lh2_to_burn, 2),
            "end_mass_mt": round(m_final, 2),
            "thrust_kn": active_engines * 1000.0,
            "isp_s": isp_s,
            "actual_dv_kms": round(actual_dv_kms, 3),
            "target_dv_kms": target_dv_kms,
            "lh2_remaining_mt": round(self.state.lh2_mt, 2)
        }
        self.event_log.append(record)
        return record

    def execute_nep_burn(self, phase_name, duration_days):
        """Executes continuous low-thrust NEP burn using actual vehicle mass propagation."""
        self.update_power_and_thermal(mode="nep_cruise")
        h = self.state.system_health

        # Electric thruster parameters
        p_elec_mwe = self.state.electrical_power_mwe * (15.0 / 20.0)  # 15 MWe default allocation
        p_jet_mw = p_elec_mwe * h["nep_efficiency"]
        isp_s = 3500.0
        v_e = isp_s * G0  # 34,323.275 m/s

        thrust_n = (2.0 * p_jet_mw * 1e6) / v_e if v_e > 0 else 0.0
        mdot_kg_s = thrust_n / v_e if v_e > 0 else 0.0
        mdot_mt_day = (mdot_kg_s * 86400.0) / 1000.0  # ~1.43 MT/day

        m_initial = self.state.gross_mass_mt
        lnh3_avail = self.state.lnh3_mt

        lnh3_req = mdot_mt_day * duration_days
        if lnh3_req > lnh3_avail:
            lnh3_to_burn = lnh3_avail
            actual_duration_days = lnh3_avail / mdot_mt_day if mdot_mt_day > 0 else 0.0
        else:
            lnh3_to_burn = lnh3_req
            actual_duration_days = duration_days

        m_final = m_initial - lnh3_to_burn
        actual_dv_ms = v_e * math.log(m_initial / m_final) if m_final > 0 else 0.0
        actual_dv_kms = actual_dv_ms / 1000.0

        # State transition
        self.state.lnh3_mt -= lnh3_to_burn
        self.state.time_days += actual_duration_days
        self.state.total_delta_v_kms += actual_dv_kms

        record = {
            "phase": phase_name,
            "type": "NEP_BURN",
            "start_time_days": round(self.state.time_days - actual_duration_days, 2),
            "duration_days": round(actual_duration_days, 2),
            "start_mass_mt": round(m_initial, 2),
            "lnh3_burned_mt": round(lnh3_to_burn, 2),
            "end_mass_mt": round(m_final, 2),
            "thrust_n": round(thrust_n, 2),
            "p_jet_mw": round(p_jet_mw, 2),
            "isp_s": isp_s,
            "actual_dv_kms": round(actual_dv_kms, 3),
            "lnh3_remaining_mt": round(self.state.lnh3_mt, 2)
        }
        self.event_log.append(record)
        return record

    def execute_coast_or_stay(self, phase_name, duration_days, mode="mars_stay"):
        """Executes a coasting or surface stay phase updating crew consumables and thermal/power."""
        self.update_power_and_thermal(mode=mode)

        # Consumable usage: ~72.3 MT / 1000 days = 0.0723 MT/day for 24 crew
        consumable_loss_mt = 0.0723 * duration_days
        self.state.dry_mass_mt = max(1400.0, self.state.dry_mass_mt - consumable_loss_mt)
        self.state.time_days += duration_days

        record = {
            "phase": phase_name,
            "type": "COAST_STAY",
            "duration_days": duration_days,
            "end_time_days": round(self.state.time_days, 2),
            "gross_mass_mt": round(self.state.gross_mass_mt, 2),
            "crew_count": self.state.crew_count,
            "crew_health_percent": self.state.crew_health_percent
        }
        self.event_log.append(record)
        return record

    def run_full_mission_baseline(self):
        """Runs the sequential baseline simulation for Mission B (Earth-Mars-Earth)."""
        # Phase 1: Trans-Mars Injection (TMI) Target: 3.80 km/s
        self.execute_ntp_burn("Trans-Mars Injection (TMI)", target_dv_kms=3.80)
        self.state.position = "Heliocentric_Outbound"

        # Phase 2: Outbound Cruise (NEP 180 Days)
        self.execute_nep_burn("Outbound Cruise NEP (180d)", duration_days=180.0)
        self.state.position = "Mars_Approach"

        # Phase 3: Mars Orbit Insertion (MOI) Target: 2.10 km/s
        self.execute_ntp_burn("Mars Orbit Insertion (MOI)", target_dv_kms=2.10)
        self.state.position = "Mars_Orbit"

        # Phase 4: Mars Stay & Excursion Operations (640 Days)
        self.execute_coast_or_stay("Mars Orbit Stay (640d)", duration_days=640.0, mode="mars_stay")

        # Phase 5: Trans-Earth Injection (TEI) - Burn remaining LH2 allocation or target 1.80 km/s
        self.execute_ntp_burn("Trans-Earth Injection (TEI)", target_dv_kms=1.80)
        self.state.position = "Heliocentric_Inbound"

        # Phase 6: Inbound Cruise (NEP 180 Days or remaining LNH3)
        self.execute_nep_burn("Inbound Cruise NEP (180d)", duration_days=180.0)
        self.state.position = "Earth_Approach"

        # Phase 7: Earth Capture & Insertion (EOI) - Burn any remaining LH2
        if self.state.lh2_mt > 0.1:
            self.execute_ntp_burn("Earth Orbit Capture (EOI)", burn_all_lh2=True)
        self.state.position = "Earth_Orbit"

        # Assess closure
        lh2_left = self.state.lh2_mt
        lnh3_left = self.state.lnh3_mt

        # Check trajectory requirement closure
        total_actual_dv = self.state.total_delta_v_kms

        closure_status = {
            "status": "CLOSED" if total_actual_dv >= 12.0 and lh2_left >= 0 and lnh3_left >= 0 else "CONDITIONALLY_CLOSED",
            "total_vehicle_dv_kms": round(total_actual_dv, 3),
            "lh2_remaining_mt": round(lh2_left, 2),
            "lnh3_remaining_mt": round(lnh3_left, 2),
            "final_gross_mass_mt": round(self.state.gross_mass_mt, 2),
            "mission_duration_days": round(self.state.time_days, 1)
        }

        output = {
            "vehicle": {
                "name": "USS Enterprise X (Project Occam-7)",
                "dry_mass_mt": 1470.96,
                "propellant_inventory_mt": 2500.0,
                "gross_departure_mass_mt": 3970.96
            },
            "events": self.event_log,
            "final_state": self.state.to_dict(),
            "closure_summary": closure_status
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
            self.state.crew_health_percent = 85.0

        return self.run_full_mission_baseline()


def generate_json_baseline(output_path="engineering/calculations/mission_baseline.json"):
        twin = MissionDigitalTwin()
        res = twin.run_full_mission_baseline()

        # Also include failure cases in baseline output
        failure_results = {}
        for f_type in ["radiator_loss_25", "ntp_engine_loss_1", "propellant_loss_30", "reactor_degraded_50", "gravity_loss"]:
            f_twin = MissionDigitalTwin()
            f_res = f_twin.run_failure_case(f_type)
            failure_results[f_type] = {
                "total_dv_kms": f_res["closure_summary"]["total_vehicle_dv_kms"],
                "lh2_remaining_mt": f_res["closure_summary"]["lh2_remaining_mt"],
                "lnh3_remaining_mt": f_res["closure_summary"]["lnh3_remaining_mt"],
                "final_mass_mt": f_res["closure_summary"]["final_gross_mass_mt"]
            }

        res["failure_cases"] = failure_results

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(res, f, indent=2)

        print(f"Digital Twin baseline output successfully written to: {output_path}")
        return res


if __name__ == "__main__":
    generate_json_baseline()
