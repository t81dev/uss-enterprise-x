#!/usr/bin/env python3
"""
Stefan-Boltzmann Radiator Area, Mass, and Thermal Rejection Calculator for Project Occam-7.
Calculates required surface area, panel counts, fluid mass, and physical footprint.
"""

SIGMA = 5.670374419e-8  # W / (m^2 K^4)

def calculate_radiator_area(q_th_kw, temp_k, emissivity=0.90, degradation_margin=0.15, double_sided=True):
    """
    Calculates required radiator surface area (m^2) for given heat rejection (kWth) and operating temperature (K).
    """
    q_watts = q_th_kw * 1000.0 * (1.0 + degradation_margin)
    flux_per_m2 = emissivity * SIGMA * (temp_k ** 4)  # W/m^2 single side

    total_emitting_area = q_watts / flux_per_m2
    if double_sided:
        one_sided_panel_area = total_emitting_area / 2.0
    else:
        one_sided_panel_area = total_emitting_area

    return one_sided_panel_area, flux_per_m2 / 1000.0  # Area in m^2, Flux in kW/m^2

def thermal_closure_model():
    print("=== THERMAL CLOSURE & RADIATOR SIZING CALCULATOR V2 ===")

    # Subsystem Waste Heat Sources
    # 100 MWth Reactor at 20% electric efficiency => 20 MWe electrical, 80 MWth waste heat at 850 K
    sources = [
        {"name": "Main Reactor Core Waste Heat", "q_kw": 80000.0, "temp_k": 850.0, "emiss": 0.90, "spec_mass_kg_m2": 1.8},
        {"name": "NEP Power Conversion Loss (Brayton/MPD)", "q_kw": 3000.0, "temp_k": 650.0, "emiss": 0.90, "spec_mass_kg_m2": 1.5},
        {"name": "Avionics & High-Performance Compute", "q_kw": 50.0, "temp_k": 320.0, "emiss": 0.88, "spec_mass_kg_m2": 2.2},
        {"name": "Habitat HVAC & Crew Life Support", "q_kw": 200.0, "temp_k": 295.0, "emiss": 0.88, "spec_mass_kg_m2": 2.5},
        {"name": "ECLSS Processing & Water Loop", "q_kw": 120.0, "temp_k": 310.0, "emiss": 0.88, "spec_mass_kg_m2": 2.2},
        {"name": "Scientific Instrumentation & Workshop", "q_kw": 80.0, "temp_k": 330.0, "emiss": 0.88, "spec_mass_kg_m2": 2.0}
    ]

    total_one_sided_area = 0.0
    total_radiator_mass_kg = 0.0

    for s in sources:
        panel_area, flux_kw_m2 = calculate_radiator_area(s["q_kw"], s["temp_k"], s["emiss"])
        panel_mass = panel_area * s["spec_mass_kg_m2"]
        total_one_sided_area += panel_area
        total_radiator_mass_kg += panel_mass

        print(f"\nSubsystem: {s['name']}")
        print(f"  Waste Heat: {s['q_kw']:.1f} kWth | Temp: {s['temp_k']} K")
        print(f"  Radiated Flux: {flux_kw_m2:.2f} kW/m^2 (single side)")
        print(f"  Required One-Sided Panel Area (incl 15% margin): {panel_area:.1f} m^2")
        print(f"  Radiator Dry Mass: {panel_mass / 1000.0:.2f} MT")

    # Manifolds, structural deployable booms, and NaK coolant inventory add ~40% mass
    total_thermal_system_mass_mt = (total_radiator_mass_kg * 1.40) / 1000.0

    print("\n--- THERMAL TOTALS ---")
    print(f"Total One-Sided Radiator Footprint Area: {total_one_sided_area:.1f} m^2")
    print(f"Total Effective Radiating Surface Area (Double-Sided): {total_one_sided_area * 2.0:.1f} m^2")
    print(f"Total Thermal Management System Mass (with booms & fluid): {total_thermal_system_mass_mt:.2f} MT")

    # Check physical geometric fit on 380m central spine
    # If panels are deployed symmetrically on 2 side wings along 150m length of spine:
    wing_length = 150.0  # m
    required_width = total_one_sided_area / (2 * wing_length)
    print(f"Geometric Fit Check on 150m Spine Segment:")
    print(f"  2x Deployable Wings (150m length each): Width required per wing = {required_width:.2f} m")

if __name__ == "__main__":
    thermal_closure_model()
