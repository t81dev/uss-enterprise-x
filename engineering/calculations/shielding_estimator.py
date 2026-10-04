#!/usr/bin/env python3
"""
Radiation Protection & Shielding Column Density Calculator for Project Occam-7
Calculates column density (g/cm^2) and total shield mass for SPE Storm Shelter & Nominal Habitat.
"""

def shielding_calculator():
    # Densities in g/cm^3
    densities = {
        "Water": 1.00,
        "Polyethylene (HDPE)": 0.95,
        "Liquid Hydrogen (LH2)": 0.071,
        "Liquid Ammonia (LNH3)": 0.681,
        "Stainless Steel 316L": 8.00,
        "Boron Carbide (B4C)": 2.52,
        "Tungsten": 19.25,
        "Lithium Hydride (LiH)": 0.78
    }

    print("=== RADIATION SHIELDING & COLUMN DENSITY ESTIMATOR V2 ===")

    # 1. Storm Shelter (SPE Protection)
    # Cylindrical inner shelter: r = 2.0 m, length = 10.0 m
    # Double-wall water jacket thickness = 40 cm (40 g/cm^2) + 5 cm HDPE (4.75 g/cm^2) + SS inner/outer walls (2x 0.5 cm = 8 g/cm^2)
    # Total column density = 52.75 g/cm^2
    r_inner = 2.0  # m
    length = 10.0  # m
    t_water = 0.40  # m (40 cm)
    t_hdpe = 0.05   # m (5 cm)

    # Calculate water volume: V = pi * ( (r+t_water)^2 - r^2 ) * length
    v_water = 3.14159 * ((r_inner + t_water)**2 - r_inner**2) * length
    m_water_kg = v_water * densities["Water"] * 1000.0

    # Calculate HDPE volume
    r_hdpe_inner = r_inner + t_water
    v_hdpe = 3.14159 * ((r_hdpe_inner + t_hdpe)**2 - r_hdpe_inner**2) * length
    m_hdpe_kg = v_hdpe * densities["Polyethylene (HDPE)"] * 1000.0

    m_shelter_total_mt = (m_water_kg + m_hdpe_kg) / 1000.0
    col_density_shelter = (t_water * 100.0 * densities["Water"]) + (t_hdpe * 100.0 * densities["Polyethylene (HDPE)"])

    print(f"\nSPE Central Storm Shelter:")
    print(f"  Inner Dimensions: {r_inner*2:.1f} m dia x {length:.1f} m length")
    print(f"  Water Shield Layer: {t_water*100:.0f} cm ({m_water_kg/1000.0:.1f} MT)")
    print(f"  HDPE Polymer Layer: {t_hdpe*100:.0f} cm ({m_hdpe_kg/1000.0:.1f} MT)")
    print(f"  Effective Passive Column Density: {col_density_shelter:.2f} g/cm^2")
    print(f"  Total Storm Shelter Shield Mass: {m_shelter_total_mt:.1f} MT")

    # 2. Main Habitat Outer Circumferential Tanks (GCR Buffer)
    # Outer habitat radius r = 4.0 m, length = 30.0 m
    # Water tank belt thickness = 20 cm (20 g/cm^2)
    r_hab = 4.0
    len_hab = 30.0
    t_hab_water = 0.20
    v_hab_water = 3.14159 * ((r_hab + t_hab_water)**2 - r_hab**2) * len_hab
    m_hab_water_mt = (v_hab_water * densities["Water"] * 1000.0) / 1000.0

    print(f"\nOuter Habitat Circumferential GCR Shielding (Water Buffer):")
    print(f"  Habitat Cylinder: {r_hab*2:.1f} m dia x {len_hab:.1f} m length")
    print(f"  Circumferential Water Layer: {t_hab_water*100:.0f} cm")
    print(f"  Water Buffer Mass: {m_hab_water_mt:.1f} MT")
    print(f"  Habitat Ambient Column Density: {t_hab_water * 100.0 * densities['Water']:.1f} g/cm^2")

if __name__ == "__main__":
    shielding_calculator()
