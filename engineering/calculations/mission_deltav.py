#!/usr/bin/env python3
"""
Mission Delta-V, Mass Departure & Trajectory Duration Calculator for Project Occam-7
Calculates Delta-V budgets, propellant consumption, continuous electric propulsion integration, and burn profiles.
"""

import math

G0 = 9.80665

def calculate_mission_masses(m_dry, isp, delta_v_kms):
    dv_ms = delta_v_kms * 1000.0
    mass_ratio = math.exp(dv_ms / (isp * G0))
    m_departure = m_dry * mass_ratio
    m_propellant = m_departure - m_dry
    return m_departure, m_propellant, mass_ratio

def calculate_nep_burn(m_initial_kg, thrust_n, isp_s, duration_days):
    """Calculates low-thrust continuous NEP burn trajectory delta-v and propellant consumption."""
    v_e = isp_s * G0
    mdot_kg_s = thrust_n / v_e
    t_burn_s = duration_days * 86400.0
    m_prop_kg = mdot_kg_s * t_burn_s
    m_final_kg = m_initial_kg - m_prop_kg
    delta_v_ms = v_e * math.log(m_initial_kg / m_final_kg)
    p_jet_watts = 0.5 * thrust_n * v_e
    return {
        "m_prop_mt": m_prop_kg / 1000.0,
        "m_final_mt": m_final_kg / 1000.0,
        "delta_v_kms": delta_v_ms / 1000.0,
        "p_jet_mw": p_jet_watts / 1e6,
        "mdot_kg_s": mdot_kg_s
    }

def mission_profile_model():
    m_dry = 1471.0  # MT v2 reconciled dry mass (incl. 20% margin and 6.5mm tanks)

    print("=== USS ENTERPRISE X - MISSION TRAJECTORY & DELTA-V CLOSURE V2 (RECONCILED) ===")
    print(f"Reconciled Vehicle Dry Mass: {m_dry:.1f} MT\n")

    # NEP Trajectory Check for 15 MWe input (65% thruster efficiency => 9.75 MW jet power => 568.1 N thrust)
    nep_eval = calculate_nep_burn(
        m_initial_kg=(m_dry + 300.0) * 1000.0,
        thrust_n=568.12,
        isp_s=3500.0,
        duration_days=180.0
    )
    print("--- 15 MWe NEP CRUISE TRAJECTORY VERIFICATION (180 Days) ---")
    print(f"  Electrical Input Power:  15.0 MWe")
    print(f"  Jet Power (65% efficiency): {nep_eval['p_jet_mw']:.2f} MW")
    print(f"  NEP Thrust @ 3,500s Isp: {568.12:.1f} N")
    print(f"  Propellant Mass Flow:    {nep_eval['mdot_kg_s']:.4f} kg/s ({nep_eval['mdot_kg_s']*86400/1000:.2f} MT/day)")
    print(f"  Propellant Consumed (180d): {nep_eval['m_prop_mt']:.1f} MT")
    print(f"  Delivered NEP Delta-V:   {nep_eval['delta_v_kms']:.2f} km/s (Exceeds 2.55 km/s leg requirement!)\n")

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
