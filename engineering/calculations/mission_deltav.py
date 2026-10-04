#!/usr/bin/env python3
"""
Mission Delta-V, Mass Departure & Trajectory Duration Calculator for Project Occam-7
Calculates Delta-V budgets, propellant consumption, burn profiles, and transit times for Missions A, B, and C.
"""

import math

G0 = 9.80665

def calculate_mission_masses(m_dry, isp, delta_v_kms):
    dv_ms = delta_v_kms * 1000.0
    mass_ratio = math.exp(dv_ms / (isp * G0))
    m_departure = m_dry * mass_ratio
    m_propellant = m_departure - m_dry
    return m_departure, m_propellant, mass_ratio

def mission_profile_model():
    m_dry = 1422.4  # MT v2 baseline dry mass

    missions = [
        {
            "name": "Mission A: Cislunar Expedition & Gateway Operations",
            "delta_v": 8.5,  # km/s
            "duration_days": 180,
            "propulsion_mode": "Hybrid NTP (Isp=900s) + NEP (Isp=3500s)",
            "effective_isp": 1200
        },
        {
            "name": "Mission B: Earth-Mars-Earth Fast Transit Expedition",
            "delta_v": 16.0,  # km/s
            "duration_days": 1000,
            "propulsion_mode": "Hybrid NTP (Isp=900s) + NEP (Isp=3500s)",
            "effective_isp": 1800
        },
        {
            "name": "Mission C: Jupiter System / Outer Solar System Exploration",
            "delta_v": 25.0,  # km/s
            "duration_days": 1800,
            "propulsion_mode": "High-Efficiency NEP (Isp=3500s) / Advanced Fusion (Isp=10000s)",
            "effective_isp": 3500
        }
    ]

    print("=== USS ENTERPRISE X - MISSION TRAJECTORY & DELTA-V CLOSURE V1 ===")
    print(f"Baseline Vehicle Dry Mass: {m_dry:.1f} MT\n")

    for m in missions:
        m_dep, m_prop, mr = calculate_mission_masses(m_dry, m["effective_isp"], m["delta_v"])
        print(f"--- {m['name']} ---")
        print(f"  Target Total Delta-V: {m['delta_v']:.1f} km/s")
        print(f"  Propulsion Strategy: {m['propulsion_mode']} (Effective Isp = {m['effective_isp']} s)")
        print(f"  Required Mass Ratio: {mr:.2f}")
        print(f"  Propellant Required: {m_prop:.1f} MT")
        print(f"  Departure Mass:      {m_dep:.1f} MT")
        print(f"  Mission Duration:    {m['duration_days']} days\n")

if __name__ == "__main__":
    mission_profile_model()
