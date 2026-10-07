#!/usr/bin/env python3
"""
Radiation Protection & Dynamic Shielding Column Density Calculator for Project Occam-7
Hostile Engineering Audit Version: Incorporates directional solid angle geometry,
propellant depletion tracking, GCR isotropic background, SPE storm shelter attenuation,
secondary neutron spallation in steel, and reactor inverse-square scatter flux.
"""

import math

# Material Densities in g/cm^3
DENSITIES = {
    "Water": 1.00,
    "Polyethylene (HDPE)": 0.95,
    "Liquid Hydrogen (LH2)": 0.071,
    "Liquid Ammonia (LNH3)": 0.681,
    "Stainless Steel 316L": 8.00,
    "Boron Carbide (B4C)": 2.52,
    "Tungsten": 19.25,
    "Lithium Hydride (LiH)": 0.78
}

def calculate_directional_solid_angles(tank_radius_m=6.0, tank_distance_m=35.0):
    """
    Calculates solid angle subtended by main propellant tanks looking aft from habitat center.
    Omega_axial = 2 * pi * (1 - cos(theta_axial))
    Omega_radial = 4 * pi - Omega_axial
    """
    theta_axial_rad = math.atan(tank_radius_m / tank_distance_m)
    omega_axial_sr = 2.0 * math.pi * (1.0 - math.cos(theta_axial_rad))
    omega_radial_sr = 4.0 * math.pi - omega_axial_sr

    frac_axial = omega_axial_sr / (4.0 * math.pi)
    frac_radial = omega_radial_sr / (4.0 * math.pi)

    return {
        "theta_axial_deg": math.degrees(theta_axial_rad),
        "omega_axial_sr": omega_axial_sr,
        "omega_radial_sr": omega_radial_sr,
        "frac_axial": frac_axial,
        "frac_radial": frac_radial
    }


def calculate_axial_propellant_column_density(lh2_mt, lnh3_mt, tank_diameter_m=12.0, tank_length_m=280.0):
    """
    Calculates axial column density (g/cm^2) through propellant tanks based on current propellant inventory.
    """
    # Max capacity reference: 2,200 t LH2 + 300 t LNH3 -> ~280m total effective liquid path length
    if lh2_mt <= 0 and lnh3_mt <= 0:
        return 0.0

    # Effective path length scales with liquid volume fill fraction
    # LH2 density = 0.071 g/cm^3 (0.071 t/m^3), LNH3 density = 0.681 g/cm^3 (0.681 t/m^3)
    v_lh2_m3 = lh2_mt / DENSITIES["Liquid Hydrogen (LH2)"]
    v_lnh3_m3 = lnh3_mt / DENSITIES["Liquid Ammonia (LNH3)"]

    cross_section_m2 = math.pi * ((tank_diameter_m / 2.0) ** 2)

    # Effective liquid column length along axial line of sight
    path_lh2_cm = (v_lh2_m3 / cross_section_m2) * 100.0 if cross_section_m2 > 0 else 0.0
    path_lnh3_cm = (v_lnh3_m3 / cross_section_m2) * 100.0 if cross_section_m2 > 0 else 0.0

    col_lh2_g_cm2 = path_lh2_cm * DENSITIES["Liquid Hydrogen (LH2)"]
    col_lnh3_g_cm2 = path_lnh3_cm * DENSITIES["Liquid Ammonia (LNH3)"]

    return col_lh2_g_cm2 + col_lnh3_g_cm2


def calculate_gcr_dose_rate(sigma_radial_g_cm2=31.4, sigma_axial_g_cm2=0.0, soi_reference="Earth_SOI"):
    """
    Calculates dynamic GCR background dose rate (cSv/day) weighted by $4\\pi$ directional solid angles.
    Unshielded deep space GCR flux ~ 0.18 cSv/day (1.8 mSv/day).
    Martian surface provides 2pi planet shadow (50% reduction) + 16 g/cm^2 CO2 atmosphere attenuation.
    """
    unshielded_gcr_csv_day = 0.18

    # Surface / planet shadow modification
    if soi_reference == "Mars_Surface":
        # Planet blocks 50% of sky, atmosphere adds ~16 g/cm^2 CO2
        unshielded_gcr_csv_day *= 0.50
        sigma_radial_g_cm2 += 16.0

    # Exponential + secondary neutron relaxation attenuation model
    # Low-Z materials attenuation length lambda ~ 45 g/cm^2, secondary production factor ~ 0.15
    f_att_radial = math.exp(-sigma_radial_g_cm2 / 45.0) + 0.05 * math.exp(-sigma_radial_g_cm2 / 120.0)

    # Axial path includes structural hull + propellant column
    sigma_axial_total = 12.0 + sigma_axial_g_cm2  # 12 g/cm^2 steel bulkheads/structure
    f_att_axial = math.exp(-sigma_axial_total / 45.0) + 0.05 * math.exp(-sigma_axial_total / 120.0)

    angles = calculate_directional_solid_angles()
    gcr_dose_csv_day = unshielded_gcr_csv_day * (angles["frac_radial"] * f_att_radial + angles["frac_axial"] * f_att_axial)

    return gcr_dose_csv_day


def calculate_reactor_dose_rate(reactor_power_mwth, sigma_axial_prop_g_cm2=0.0, distance_m=380.0):
    """
    Calculates reactor gamma and neutron dose rate (cSv/day) at habitat deck (380m separation).
    Conical shadow shield (45 MT Tungsten + B4C/LiH) provides 1.43e-4 attenuation factor.
    Axial propellant tanks provide additional exponential attenuation when present.
    """
    if reactor_power_mwth <= 0.0:
        return 0.00001  # Negligible core decay heat radiation

    # Base unshielded reactor dose at 1m = 1.2e5 Sv/hr per MWth
    # At 380m, inverse-square 1/R^2 factor = 1 / (380^2) = 6.925e-6
    unshielded_dose_sv_hr = (reactor_power_mwth * 120.0) * (1.0 / (distance_m ** 2))

    # Shadow shield attenuation factor (45 MT Tungsten / B4C / LiH)
    f_shadow_shield = 1.43e-4

    # Propellant tank axial attenuation: hydrogen relaxation length lambda ~ 30 g/cm^2
    f_prop_attenuation = math.exp(-sigma_axial_prop_g_cm2 / 30.0)

    shielded_dose_sv_hr = unshielded_dose_sv_hr * f_shadow_shield * f_prop_attenuation
    shielded_dose_csv_day = (shielded_dose_sv_hr * 100.0) * 24.0  # Convert Sv/hr to cSv/day

    return shielded_dose_csv_day


def compute_dynamic_dose_rate(lh2_mt, lnh3_mt, reactor_power_mwth, soi_reference="Earth_SOI", in_storm_shelter=False, spe_event=False):
    """
    Computes total dynamic daily radiation dose rate (cSv/day) for current spacecraft state.
    """
    sigma_radial = 52.25 if in_storm_shelter else 31.4  # g/cm^2
    sigma_axial_prop = calculate_axial_propellant_column_density(lh2_mt, lnh3_mt)

    gcr_rate_csv_day = calculate_gcr_dose_rate(sigma_radial_g_cm2=sigma_radial, sigma_axial_g_cm2=sigma_axial_prop, soi_reference=soi_reference)
    rx_rate_csv_day = calculate_reactor_dose_rate(reactor_power_mwth=reactor_power_mwth, sigma_axial_prop_g_cm2=sigma_axial_prop)

    spe_dose_csv = 0.0
    if spe_event:
        # SPE event dose: 250 cSv unshielded. Inside storm shelter (52.25 g/cm^2), attenuated by 98.5% -> 3.75 cSv
        # Outside shelter (31.4 g/cm^2), attenuated by 85% -> 37.5 cSv
        att_factor = 0.015 if in_storm_shelter else 0.15
        spe_dose_csv = 250.0 * att_factor

    total_daily_dose_csv = gcr_rate_csv_day + rx_rate_csv_day

    return {
        "sigma_radial_g_cm2": sigma_radial,
        "sigma_axial_prop_g_cm2": sigma_axial_prop,
        "gcr_rate_csv_day": gcr_rate_csv_day,
        "rx_rate_csv_day": rx_rate_csv_day,
        "spe_event_dose_csv": spe_dose_csv,
        "total_daily_dose_csv": total_daily_dose_csv
    }


def shielding_calculator():
    """
    Prints baseline shielding hardware & column density estimates.
    """
    print("=== RADIATION SHIELDING & COLUMN DENSITY ESTIMATOR V3 (HOSTILE AUDIT RECONCILED) ===")

    r_inner = 2.0  # m
    length = 10.0  # m
    t_ss_inner = 0.005  # m
    t_water = 0.30      # m
    t_hdpe = 0.15       # m
    t_ss_outer = 0.005  # m

    # Calculate material volumes and masses
    v_ss_inner = 3.14159 * ((r_inner + t_ss_inner)**2 - r_inner**2) * length
    m_ss_inner_kg = v_ss_inner * DENSITIES["Stainless Steel 316L"] * 1000.0

    r2 = r_inner + t_ss_inner
    v_water = 3.14159 * ((r2 + t_water)**2 - r2**2) * length
    m_water_kg = v_water * DENSITIES["Water"] * 1000.0

    r3 = r2 + t_water
    v_hdpe = 3.14159 * ((r3 + t_hdpe)**2 - r3**2) * length
    m_hdpe_kg = v_hdpe * DENSITIES["Polyethylene (HDPE)"] * 1000.0

    r4 = r3 + t_hdpe
    v_ss_outer = 3.14159 * ((r4 + t_ss_outer)**2 - r4**2) * length
    m_ss_outer_kg = v_ss_outer * DENSITIES["Stainless Steel 316L"] * 1000.0

    m_shelter_total_mt = (m_ss_inner_kg + m_water_kg + m_hdpe_kg + m_ss_outer_kg) / 1000.0

    col_ss_inner = t_ss_inner * 100.0 * DENSITIES["Stainless Steel 316L"]
    col_water = t_water * 100.0 * DENSITIES["Water"]
    col_hdpe = t_hdpe * 100.0 * DENSITIES["Polyethylene (HDPE)"]
    col_ss_outer = t_ss_outer * 100.0 * DENSITIES["Stainless Steel 316L"]

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
    m_hab_water_mt = (v_hab_water * DENSITIES["Water"] * 1000.0) / 1000.0

    print(f"\nOuter Habitat Circumferential GCR Shielding (Water Buffer):")
    print(f"  Habitat Cylinder: {r_hab*2:.1f} m dia x {len_hab:.1f} m length")
    print(f"  Circumferential Water Layer: {t_hab_water*100:.0f} cm")
    print(f"  Water Buffer Mass: {m_hab_water_mt:.1f} MT")
    print(f"  Habitat Ambient Column Density: {t_hab_water * 100.0 * DENSITIES['Water']:.1f} g/cm^2")

    # 3. Solid Angle Demonstration
    angles = calculate_directional_solid_angles()
    print(f"\nDirectional Solid Angle Analysis:")
    print(f"  Axial Propellant Tank Subtended Angle: {angles['theta_axial_deg']:.2f} deg")
    print(f"  Axial Solid Angle: {angles['omega_axial_sr']:.3f} sr ({angles['frac_axial']*100:.2f}% of 4pi sky)")
    print(f"  Radial/Circumferential Solid Angle: {angles['omega_radial_sr']:.3f} sr ({angles['frac_radial']*100:.2f}% of 4pi sky)")

    return {
        "col_density_shelter": col_density_shelter,
        "m_shelter_total_mt": m_shelter_total_mt,
        "m_hab_water_mt": m_hab_water_mt,
        "angles": angles
    }

if __name__ == "__main__":
    shielding_calculator()
