#!/usr/bin/env python3
"""
Power Budget & Energy Closure Calculator for USS Enterprise X (Project Occam-7)
Calculates electrical, thermal, and propulsive loads across Nominal, High-Load, and Emergency cases.
"""

def power_budget_model():
    # Power loads in kWe (electrical)
    subsystem_loads = {
        "ECLSS & Closed-Loop Air/Water Plant": {"nom": 120, "peak": 180, "emerg": 80},
        "Thermal Control Pumps & Heat Transport": {"nom": 80, "peak": 140, "emerg": 50},
        "Avionics, Optical Bus & Rad-Hard Compute": {"nom": 40, "peak": 75, "emerg": 20},
        "Communications & High-Gain Optical Lasers": {"nom": 15, "peak": 50, "emerg": 5},
        "Habitat HVAC, Lighting & Accommodations": {"nom": 60, "peak": 90, "emerg": 30},
        "Centrifuge Drive & Momentum Compensation": {"nom": 25, "peak": 45, "emerg": 0},
        "Scientific Payload & Sensor Arrays": {"nom": 50, "peak": 200, "emerg": 0},
        "Automated Machine Shop & Manufacturing": {"nom": 20, "peak": 100, "emerg": 0},
        "Active Laser Ablation / Debris Radar": {"nom": 5, "peak": 500, "emerg": 0},
        "Battery Charging & Storage Buffer": {"nom": 35, "peak": 100, "emerg": 0}
    }

    nom_house = sum(item["nom"] for item in subsystem_loads.values())
    peak_house = sum(item["peak"] for item in subsystem_loads.values())
    emerg_house = sum(item["emerg"] for item in subsystem_loads.values())

    # Electric Propulsion Demand (NEP mode)
    nep_propulsion_kwe = 15000.0  # 15 MWe for Magnetoplasmadynamic (MPD) thrust

    # Main Nuclear Reactor Generation Capacity
    reactor_thermal_kwth = 100000.0  # 100 MWth core
    brayton_efficiency = 0.20        # 20% electrical conversion efficiency
    reactor_electric_kwe = reactor_thermal_kwth * brayton_efficiency  # 20,000 kWe (20 MWe)

    print("=== USS ENTERPRISE X - POWER BUDGET V2 ===")
    print(f"Reactor Thermal Capacity:  {reactor_thermal_kwth / 1000.0:.1f} MWth")
    print(f"Reactor Electric Output:   {reactor_electric_kwe / 1000.0:.1f} MWe ({brayton_efficiency*100:.0f}% Brayton efficiency)")
    print(f"\nHouse Loads (Non-Propulsive):")
    print(f"  Nominal Cruise Load:    {nom_house:.1f} kWe ({nom_house / 1000.0:.2f} MWe)")
    print(f"  Peak Operating Load:    {peak_house:.1f} kWe ({peak_house / 1000.0:.2f} MWe)")
    print(f"  Emergency Survival Load: {emerg_house:.1f} kWe ({emerg_house / 1000.0:.2f} MWe)")

    print(f"\nFull Cruise State (House + NEP Electric Thrust):")
    print(f"  Total Electric Load:    {(nom_house + nep_propulsion_kwe) / 1000.0:.2f} MWe")
    print(f"  Available Margin:       {(reactor_electric_kwe - nom_house - nep_propulsion_kwe) / 1000.0:.2f} MWe")

if __name__ == "__main__":
    power_budget_model()
