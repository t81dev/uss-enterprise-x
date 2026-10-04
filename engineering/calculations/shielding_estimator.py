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

    print("=== RADIATION SHIELDING & COLUMN DENSITY ESTIMATOR V2 (RECONCILED) ===")

    # 1. Storm Shelter (SPE Protection)
    # Inner shelter: r = 2.0 m, length = 10.0 m
    # Multi-layer shielding stack:
    # - Inner Pressure Hull SS 316L: t = 0.5 cm (4.00 g/cm^2)
    # - Water Jacket: t = 30 cm (30.00 g/cm^2)
    # - HDPE Polymer Layer: t = 15 cm (14.25 g/cm^2)
    # - Outer Pressure Hull SS 316L: t = 0.5 cm (4.00 g/cm^2)
    # Total nominal areal density = 4.00 + 30.00 + 14.25 + 4.00 = 52.25 g/cm^2 (matches ~52.75 g/cm^2 spec)

    r_inner = 2.0  # m
    length = 10.0  # m
    t_ss_inner = 0.005  # m (0.5 cm)
    t_water = 0.30      # m (30 cm)
    t_hdpe = 0.15       # m (15 cm)
    t_ss_outer = 0.005  # m (0.5 cm)

    # Calculate material volumes and masses
    # Layer 1: Inner SS Hull
    r1 = r_inner
    r2 = r1 + t_ss_inner
    v_ss_inner = 3.14159 * (r2**2 - r1**2) * length
    m_ss_inner_kg = v_ss_inner * densities["Stainless Steel 316L"] * 1000.0

    # Layer 2: Water Jacket
    r3 = r2 + t_water
    v_water = 3.14159 * (r3**2 - r2**2) * length
    m_water_kg = v_water * densities["Water"] * 1000.0

    # Layer 3: HDPE Polymer
    r4 = r3 + t_hdpe
    v_hdpe = 3.14159 * (r4**2 - r3**2) * length
    m_hdpe_kg = v_hdpe * densities["Polyethylene (HDPE)"] * 1000.0

    # Layer 4: Outer SS Hull
    r5 = r4 + t_ss_outer
    v_ss_outer = 3.14159 * (r5**2 - r4**2) * length
    m_ss_outer_kg = v_ss_outer * densities["Stainless Steel 316L"] * 1000.0

    m_shelter_total_mt = (m_ss_inner_kg + m_water_kg + m_hdpe_kg + m_ss_outer_kg) / 1000.0

    col_ss_inner = t_ss_inner * 100.0 * densities["Stainless Steel 316L"]
    col_water = t_water * 100.0 * densities["Water"]
    col_hdpe = t_hdpe * 100.0 * densities["Polyethylene (HDPE)"]
    col_ss_outer = t_ss_outer * 100.0 * densities["Stainless Steel 316L"]

    col_density_shelter = col_ss_inner + col_water + col_hdpe + col_ss_outer

    print(f"\nSPE Central Storm Shelter (Multi-Layer Stack):")
    print(f"  Inner Dimensions: {r_inner*2:.1f} m dia x {length:.1f} m length")
    print(f"  Layer 1 Inner SS Hull: {t_ss_inner*100:.1f} cm ({col_ss_inner:.2f} g/cm^2, {m_ss_inner_kg/1000.0:.2f} MT)")
    print(f"  Layer 2 Water Jacket: {t_water*100:.0f} cm ({col_water:.2f} g/cm^2, {m_water_kg/1000.0:.2f} MT)")
    print(f"  Layer 3 HDPE Layer:   {t_hdpe*100:.0f} cm ({col_hdpe:.2f} g/cm^2, {m_hdpe_kg/1000.0:.2f} MT)")
    print(f"  Layer 4 Outer SS Hull: {t_ss_outer*100:.1f} cm ({col_ss_outer:.2f} g/cm^2, {m_ss_outer_kg/1000.0:.2f} MT)")
    print(f"  Total SPE Column Density: {col_density_shelter:.2f} g/cm^2")
    print(f"  Total Storm Shelter Hardware/Fluid Mass: {m_shelter_total_mt:.1f} MT")

    # 2. Outer Habitat Circumferential GCR Shielding
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

    return {
        "col_density_shelter": col_density_shelter,
        "m_shelter_total_mt": m_shelter_total_mt
    }

if __name__ == "__main__":
    shielding_calculator()
