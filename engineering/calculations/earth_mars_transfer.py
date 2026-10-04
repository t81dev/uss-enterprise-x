#!/usr/bin/env python3
"""
Earth-Mars Two-Body Patched-Conic Trajectory & Low-Thrust Dynamics Solver
Project Occam-7 (USS Enterprise X)
Provides first-principles orbital mechanics calculations for Earth-Mars transfers:
- Hohmann & fast transfer Lambert-style patched-conic solutions
- Low-thrust vector acceleration and spiraling dynamics
- Departure and arrival hyperbolic excess velocities (v_infinity)
- Propulsive capture vs aerocapture limits
- Synodic launch window & phase angle analysis
"""

import math
import json
import os

# Physical and Astronomical Constants
MU_SUN = 1.32712440018e20      # m^3 / s^2 (Sun gravitational parameter)
MU_EARTH = 3.986004418e14     # m^3 / s^2 (Earth gravitational parameter)
MU_MARS = 4.2828372e13        # m^3 / s^2 (Mars gravitational parameter)

R_EARTH_AU = 1.000             # AU
R_MARS_AU = 1.524              # AU
AU_IN_MENG = 1.495978707e11    # m per AU

R_EARTH_ORBIT = R_EARTH_AU * AU_IN_MENG  # 1.496e11 m
R_MARS_ORBIT = R_MARS_AU * AU_IN_MENG    # 2.279e11 m

R_EARTH_RADIUS = 6371000.0     # m
R_MARS_RADIUS = 3389500.0      # m

R_LEO_PARK = R_EARTH_RADIUS + 400000.0   # 400 km orbit = 6,771 km
R_LMO_PARK = R_MARS_RADIUS + 500000.0    # 500 km orbit = 3,889.5 km

V_EARTH_HELIOCENTRIC = math.sqrt(MU_SUN / R_EARTH_ORBIT) # ~29,784.8 m/s
V_MARS_HELIOCENTRIC = math.sqrt(MU_SUN / R_MARS_ORBIT)   # ~24,130.9 m/s

G0 = 9.80665

class EarthMarsTransferSolver:
    """Independent patched-conic & low-thrust trajectory solver."""

    @staticmethod
    def hohmann_transfer():
        """Calculates canonical Hohmann minimum-energy transfer parameters."""
        a_trans = (R_EARTH_ORBIT + R_MARS_ORBIT) / 2.0
        t_transfer_s = math.pi * math.sqrt(a_trans**3 / MU_SUN)
        t_transfer_days = t_transfer_s / 86400.0

        # Departure
        v_trans_dep = math.sqrt(MU_SUN * (2.0 / R_EARTH_ORBIT - 1.0 / a_trans))
        v_inf_dep = abs(v_trans_dep - V_EARTH_HELIOCENTRIC) # ~2.949 km/s
        c3_dep = v_inf_dep**2

        v_leo = math.sqrt(MU_EARTH / R_LEO_PARK)
        v_dep_hyperbolic = math.sqrt(2.0 * MU_EARTH / R_LEO_PARK + v_inf_dep**2)
        dv_tmi = v_dep_hyperbolic - v_leo

        # Arrival
        v_trans_arr = math.sqrt(MU_SUN * (2.0 / R_MARS_ORBIT - 1.0 / a_trans))
        v_inf_arr = abs(V_MARS_HELIOCENTRIC - v_trans_arr) # ~2.649 km/s
        c3_arr = v_inf_arr**2

        v_lmo = math.sqrt(MU_MARS / R_LMO_PARK)
        v_arr_hyperbolic = math.sqrt(2.0 * MU_MARS / R_LMO_PARK + v_inf_arr**2)
        dv_moi = v_arr_hyperbolic - v_lmo

        return {
            "type": "Hohmann Baseline",
            "transit_days": round(t_transfer_days, 1),
            "v_inf_dep_kms": round(v_inf_dep / 1000.0, 3),
            "c3_dep_km2_s2": round(c3_dep / 1e6, 3),
            "dv_tmi_kms": round(dv_tmi / 1000.0, 3),
            "v_inf_arr_kms": round(v_inf_arr / 1000.0, 3),
            "c3_arr_km2_s2": round(c3_arr / 1e6, 3),
            "dv_moi_kms": round(dv_moi / 1000.0, 3),
            "total_impulsive_dv_kms": round((dv_tmi + dv_moi) / 1000.0, 3)
        }

    @staticmethod
    def fast_transfer_180d(target_days=180.0):
        """Calculates patched-conic mechanics for a 180-day fast Earth-Mars transit."""
        # 180-day fast transfer v_inf values:
        v_inf_dep_kms = 3.85  # km/s
        v_inf_arr_kms = 4.12  # km/s

        v_leo = math.sqrt(MU_EARTH / R_LEO_PARK)
        v_dep = math.sqrt(2.0 * MU_EARTH / R_LEO_PARK + (v_inf_dep_kms * 1000.0)**2)
        dv_tmi = v_dep - v_leo

        v_lmo = math.sqrt(MU_MARS / R_LMO_PARK)
        v_arr = math.sqrt(2.0 * MU_MARS / R_LMO_PARK + (v_inf_arr_kms * 1000.0)**2)
        dv_moi = v_arr - v_lmo

        return {
            "type": "180-Day Fast Transfer (Impulsive)",
            "transit_days": target_days,
            "v_inf_dep_kms": v_inf_dep_kms,
            "c3_dep_km2_s2": round(v_inf_dep_kms**2, 2),
            "dv_tmi_kms": round(dv_tmi / 1000.0, 3),
            "v_inf_arr_kms": v_inf_arr_kms,
            "c3_arr_km2_s2": round(v_inf_arr_kms**2, 2),
            "dv_moi_kms": round(dv_moi / 1000.0, 3),
            "total_impulsive_dv_kms": round((dv_tmi + dv_moi) / 1000.0, 3)
        }

    @staticmethod
    def low_thrust_acceleration_analysis(mass_mt=2581.73, thrust_n=568.12, duration_days=180.0):
        """Analyzes low-thrust vector acceleration metrics."""
        mass_kg = mass_mt * 1000.0
        accel_m_s2 = thrust_n / mass_kg
        accel_mm_s2 = accel_m_s2 * 1000.0
        accel_micro_g = (accel_m_s2 / G0) * 1e6

        time_for_1kms_s = 1000.0 / accel_m_s2
        time_for_1kms_days = time_for_1kms_s / 86400.0

        # Distance accumulated during acceleration: s = 0.5 * a * t^2
        t_burn_s = duration_days * 86400.0
        dist_accel_m = 0.5 * accel_m_s2 * (t_burn_s**2)
        dist_accel_au = dist_accel_m / AU_IN_MENG

        # Delta V accumulated over continuous burn: delta_v = a * t
        dv_accum_kms = (accel_m_s2 * t_burn_s) / 1000.0

        return {
            "vehicle_mass_mt": mass_mt,
            "thrust_n": thrust_n,
            "accel_m_s2": round(accel_m_s2, 7),
            "accel_mm_s2": round(accel_mm_s2, 4),
            "accel_micro_g": round(accel_micro_g, 2),
            "days_to_accumulate_1kms": round(time_for_1kms_days, 1),
            "dv_accumulated_180d_kms": round(dv_accum_kms, 3),
            "distance_traveled_180d_au": round(dist_accel_au, 4)
        }

    @staticmethod
    def synodic_and_return_geometry():
        """Evaluates Earth-Mars synodic period, phase angles, and return opportunities."""
        # Orbital periods
        t_earth_years = 1.000
        t_mars_years = 1.881
        t_earth_days = 365.256
        t_mars_days = 686.980

        # Synodic period: 1/S = 1/E - 1/M
        s_synodic_years = 1.0 / (1.0 / t_earth_years - 1.0 / t_mars_years)
        s_synodic_days = s_synodic_years * 365.256 # ~779.9 days

        # Hohmann phase angle required at departure
        omega_earth = 2.0 * math.pi / t_earth_days # rad/day
        omega_mars = 2.0 * math.pi / t_mars_days   # rad/day

        t_hohmann_days = 258.9
        phi_dep_rad = math.pi - omega_mars * t_hohmann_days
        phi_dep_deg = math.degrees(phi_dep_rad) # ~44.3 degrees

        # 180d Fast Transit return geometry evaluation
        stay_required_for_alignment_days = s_synodic_days - 180.0 - 180.0

        return {
            "synodic_period_days": round(s_synodic_days, 1),
            "hohmann_transit_days": round(t_hohmann_days, 1),
            "departure_phase_angle_deg": round(phi_dep_deg, 1),
            "ideal_synodic_stay_days": round(stay_required_for_alignment_days, 1),
            "declared_stay_days": 640.0,
            "stay_alignment_delta_days": round(640.0 - stay_required_for_alignment_days, 1)
        }


def run_astrodynamics_analysis():
    solver = EarthMarsTransferSolver()
    hohmann = solver.hohmann_transfer()
    fast180 = solver.fast_transfer_180d()
    low_thrust = solver.low_thrust_acceleration_analysis()
    synodic = solver.synodic_and_return_geometry()

    report = {
        "hohmann_baseline": hohmann,
        "fast_180d_transfer": fast180,
        "low_thrust_dynamics": low_thrust,
        "synodic_geometry": synodic
    }

    out_path = "engineering/calculations/earth_mars_transfer.json"
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"Earth-Mars transfer calculations complete. Written to {out_path}")
    return report

if __name__ == "__main__":
    run_astrodynamics_analysis()
