#!/usr/bin/env python3
"""
Tsiolkovsky Rocket Equation & Propulsion Performance Calculator for Project Occam-7
Calculates Delta-V, Mass Ratio, Burn Duration, Acceleration, and Power Requirements.
"""

import math

G0 = 9.80665  # m/s^2

def rocket_equation(m_initial, m_final, isp):
    """Calculates Delta-V in km/s given initial mass (t), final mass (t), and Isp (s)."""
    return (isp * G0 * math.log(m_initial / m_final)) / 1000.0

def required_propellant(m_dry, delta_v_kms, isp):
    """Calculates required propellant mass in MT for a given dry mass and Isp."""
    delta_v_ms = delta_v_kms * 1000.0
    mass_ratio = math.exp(delta_v_ms / (isp * G0))
    m_initial = m_dry * mass_ratio
    return m_initial - m_dry, m_initial

def propulsion_trades():
    m_dry = 1422.4  # MT baseline dry mass v2

    modes = {
        "Chemical (Hydrolox)": {"isp": 450, "thrust_n": 4000000, "power_kw": 0},
        "Nuclear Thermal (NTP)": {"isp": 900, "thrust_n": 1000000, "power_kw": 0},
        "Nuclear Electric (NEP MPD)": {"isp": 3500, "thrust_n": 80, "power_kw": 15000},
        "Hybrid NTP (TMI/TEI) + NEP (Cruise)": {"isp_eff": 1800, "power_kw": 15000},
        "Plausible D-He3 / Deuterium Fusion": {"isp": 15000, "thrust_n": 500, "power_kw": 50000}
    }

    print("=== PROPULSION SYSTEM TRADE STUDY (m_dry = 1422.4 MT, Target Delta-V = 16 km/s) ===")
    target_dv = 16.0  # km/s for Earth-Mars-Earth fast transit

    for name, data in modes.items():
        isp = data.get("isp", data.get("isp_eff", 1000))
        m_prop, m_wet = required_propellant(m_dry, target_dv, isp)
        mass_ratio = m_wet / m_dry
        print(f"\nMode: {name}")
        print(f"  Effective Isp: {isp} s")
        print(f"  Required Mass Ratio: {mass_ratio:.2f}")
        print(f"  Required Propellant Mass: {m_prop:.1f} MT")
        print(f"  Departure Wet Mass: {m_wet:.1f} MT")

if __name__ == "__main__":
    propulsion_trades()
