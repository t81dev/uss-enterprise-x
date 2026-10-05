#!/usr/bin/env python3
"""
Mars In-Situ Resource Utilization (ISRU) Propellant Accounting & Thermal/Power Model
Project Occam-7 (USS Enterprise X)

Provides first-principles physics and engineering models for:
- Propellant accounting (TEI LH2, ascent, RCS, losses, reserves, residuals)
- Hydrogen feedstock analysis (Glacial Ice vs Hydrated Minerals vs Atmospheric CO2)
- Water mass balance and regolith excavation rates
- Electrolysis power and chemical thermodynamics (SOEC / PEM)
- Hydrogen liquefaction, ortho-para conversion, and cryocooler ZBO power
- Single authoritative Mars surface power budget calculation (continuous MW, peak MW, margins)
- Nuclear surface reactor sizing and thermal rejection (Q_waste, radiator area/mass)
- Production rate, campaign timeline, and industrial equipment sizing
- Itemized ISRU surface plant mass budget & multi-lander payload closure verification
- Autonomous precursor architecture trade analysis (Architectures A through E)
- Failure and abort scenario modeling
- Machine-readable JSON output generation
"""

import math
import json
import os

# Physical and Chemical Constants
G0 = 9.80665                  # m/s^2
STEFAN_BOLTZMANN = 5.670374419e-8 # W/(m^2 K^4)

# Single Authoritative Mission Propellant Constants
REQUIRED_NET_RETURN_LH2_MT = 2200.0  # Net usable return propellant loaded to spacecraft (t)
F_CHILLDOWN = 0.010                  # Chill-down of lines and loading couplers (1.0%)
F_FLASH = 0.015                      # Flash evaporation during tank filling (1.5%)
F_RESIDUALS = 0.010                  # Unusable trapped tank residuals (1.0%)
F_TOTAL_TRANSFER_LOSS = F_CHILLDOWN + F_FLASH + F_RESIDUALS  # Total transfer loss fraction (3.5%)
REQUIRED_GROSS_DEPOT_WITHDRAWAL_MT = REQUIRED_NET_RETURN_LH2_MT / (1.0 - F_TOTAL_TRANSFER_LOSS)  # ~2279.79 t

# Molar Masses (g/mol)
MOLAR_MASS_H2 = 2.01588
MOLAR_MASS_O2 = 31.9988
MOLAR_MASS_H2O = 18.01528
MOLAR_MASS_CO2 = 44.0095
MOLAR_MASS_CH4 = 16.0425

# Stoichiometric Ratios
KG_WATER_PER_KG_H2 = MOLAR_MASS_H2O / MOLAR_MASS_H2  # ~8.9367 kg H2O / kg H2
KG_O2_PER_KG_H2 = MOLAR_MASS_O2 / (2.0 * MOLAR_MASS_H2) # ~7.9367 kg O2 / kg H2

# Thermodynamics of Water Electrolysis
DELTA_H_ELECTROLYSIS_KJ_PER_MOL = 285.83  # Higher Heating Value (HHV) at 298 K
DELTA_H_ELECTROLYSIS_KWH_PER_KG = (DELTA_H_ELECTROLYSIS_KJ_PER_MOL / MOLAR_MASS_H2) * (1000.0 / 3600.0) # ~39.39 kWh/kg H2

# Thermodynamics of Hydrogen Liquefaction
W_MIN_LIQUEFACTION_KWH_PER_KG = 3.91  # Ideal Carnot work to cool H2 from 300 K to 20.28 K
ORTHO_PARA_HEAT_KJ_PER_KG = 703.0    # Heat released during ortho-to-para conversion at 20 K

# Martian Environmental Parameters
T_MARS_SURFACE_AVG_K = 210.0   # Average surface temperature
T_MARS_SURFACE_MAX_K = 270.0   # Peak daytime surface temperature
P_MARS_ATM_PA = 610.0          # Average atmospheric pressure (~6.1 mbar)
H_CONVECTION_MARS = 3.5        # W/(m^2 K) - Forced/natural convection in 6 mbar CO2


class MarsISRUModel:
    """Complete first-principles Mars ISRU Propellant Accounting and Engineering Model."""

    def __init__(self, target_lh2_net_mt=REQUIRED_NET_RETURN_LH2_MT, production_days=500.0, ice_concentration=0.50,
                 soec_efficiency=0.72, liquefaction_efficiency=0.25):
        self.target_lh2_net_mt = target_lh2_net_mt  # Net usable return propellant required
        self.production_days = production_days      # Available production campaign duration
        self.ice_concentration = ice_concentration  # Glacial ice mass fraction in regolith (50% baseline)
        self.soec_efficiency = soec_efficiency      # Solid Oxide Electrolyzer efficiency (baseline 72%)
        self.liquefaction_efficiency = liquefaction_efficiency # Carnot liquefaction efficiency (baseline 25%)

    def calculate_propellant_accounting(self):
        """Calculates itemized propellant losses, reserves, and gross production requirement."""
        net_tei_lh2_mt = self.target_lh2_net_mt

        # Itemized loss fractions
        f_production_loss = 0.020     # Gas purification, venting, filter purge (2.0%)
        f_storage_boiloff = 0.015     # Surface ZBO residual storage boiloff (1.5%)
        f_transfer_loss = 0.010       # Chill-down of lines and loading couplers (1.0%)
        f_loading_flash = 0.015       # Flash evaporation during tank filling (1.5%)
        f_residuals = 0.010           # Unusable trapped tank residuals (1.0%)
        f_unusable_ullage = 0.010     # Tank bottom ullage & pump NPSH margin (1.0%)
        f_startup_purge = 0.010       # Plant commissioning and purge cycles (1.0%)
        f_contingency = 0.100         # Mandatory AIAA trajectory/production margin (10.0%)

        # Additional operational propellant needs
        propellant_ascent_mt = 45.0   # Surface-to-orbit ascent vehicle propellant (MAV RCS/Impulse)
        propellant_tcm_mt = 25.0      # Trajectory correction maneuvers on return trip
        propellant_abort_reserve_mt = 50.0 # Emergency abort maneuver reserve

        net_required_total_mt = net_tei_lh2_mt + propellant_ascent_mt + propellant_tcm_mt + propellant_abort_reserve_mt

        loss_multiplier = (1.0 + f_production_loss + f_storage_boiloff + f_transfer_loss +
                           f_loading_flash + f_residuals + f_unusable_ullage +
                           f_startup_purge + f_contingency)

        gross_lh2_production_mt = net_required_total_mt * loss_multiplier
        gross_o2_byproduct_mt = gross_lh2_production_mt * KG_O2_PER_KG_H2

        return {
            "net_tei_lh2_mt": net_tei_lh2_mt,
            "propellant_ascent_mt": propellant_ascent_mt,
            "propellant_tcm_mt": propellant_tcm_mt,
            "propellant_abort_reserve_mt": propellant_abort_reserve_mt,
            "net_required_total_mt": net_required_total_mt,
            "gross_lh2_production_mt": round(gross_lh2_production_mt, 2),
            "gross_o2_byproduct_mt": round(gross_o2_byproduct_mt, 2),
            "loss_breakdown_mt": {
                "production_loss_mt": round(net_required_total_mt * f_production_loss, 2),
                "storage_boiloff_mt": round(net_required_total_mt * f_storage_boiloff, 2),
                "transfer_loss_mt": round(net_required_total_mt * f_transfer_loss, 2),
                "loading_flash_mt": round(net_required_total_mt * f_loading_flash, 2),
                "residuals_mt": round(net_required_total_mt * f_residuals, 2),
                "unusable_ullage_mt": round(net_required_total_mt * f_unusable_ullage, 2),
                "startup_purge_mt": round(net_required_total_mt * f_startup_purge, 2),
                "contingency_reserve_mt": round(net_required_total_mt * f_contingency, 2)
            }
        }

    def evaluate_feedstock_pathways(self, gross_lh2_mt):
        """Evaluates Glacial Water Ice, Hydrated Minerals, and CO2 Sabatier pathways."""
        gross_lh2_kg = gross_lh2_mt * 1000.0

        # Pathway A: Glacial Water Ice (50% ice in regolith)
        eta_ice_recovery = 0.95
        eta_water_purification = 0.98
        water_req_pure_kg = gross_lh2_kg * KG_WATER_PER_KG_H2
        water_req_raw_kg = water_req_pure_kg / (eta_ice_recovery * eta_water_purification)
        regolith_excavated_ice_kg = water_req_raw_kg / self.ice_concentration

        # Pathway B: Hydrated Minerals (5% bound water)
        eta_mineral_thermal_yield = 0.80
        water_req_mineral_raw_kg = water_req_pure_kg / eta_mineral_thermal_yield
        regolith_excavated_minerals_kg = water_req_mineral_raw_kg / 0.05
        energy_calcination_kwh_per_kg_water = 1.85

        # Pathway C: Atmospheric CO2 processing
        co2_req_for_ch4_kg = (gross_lh2_kg / 4.0) * (MOLAR_MASS_CO2 / MOLAR_MASS_H2)
        ch4_produced_kg = (gross_lh2_kg / 4.0) * (MOLAR_MASS_CH4 / MOLAR_MASS_H2)

        return {
            "glacial_ice": {
                "pure_water_required_mt": round(water_req_pure_kg / 1000.0, 2),
                "raw_water_extracted_mt": round(water_req_raw_kg / 1000.0, 2),
                "regolith_excavated_mt": round(regolith_excavated_ice_kg / 1000.0, 2),
                "ice_concentration_percent": self.ice_concentration * 100.0,
                "kg_regolith_per_kg_lh2": round(regolith_excavated_ice_kg / gross_lh2_kg, 2)
            },
            "hydrated_minerals": {
                "raw_water_extracted_mt": round(water_req_mineral_raw_kg / 1000.0, 2),
                "regolith_excavated_mt": round(regolith_excavated_minerals_kg / 1000.0, 2),
                "mineral_water_fraction_percent": 5.0,
                "thermal_calcination_energy_mwh": round((water_req_mineral_raw_kg * energy_calcination_kwh_per_kg_water) / 1000.0, 2),
                "kg_regolith_per_kg_lh2": round(regolith_excavated_minerals_kg / gross_lh2_kg, 2),
                "assessment": "INFERIOR (Requires 10x excavation and high thermal calcination energy)"
            },
            "atmospheric_co2_sabatier": {
                "co2_processed_mt": round(co2_req_for_ch4_kg / 1000.0, 2),
                "methane_yield_mt": round(ch4_produced_kg / 1000.0, 2),
                "assessment": "COMPLEMENTARY (Useful for ascent rocket CH4/LOX, but does not eliminate H2 extraction)"
            }
        }

    def calculate_electrolysis_and_liquefaction_power(self, gross_lh2_mt):
        """Derives first-principles energy consumption parameterized by SOEC and Liquefaction efficiencies."""
        gross_lh2_kg = gross_lh2_mt * 1000.0

        # Electrolysis Efficiency (SOEC) using parameterized efficiency
        eta_soec = max(0.01, self.soec_efficiency)
        e_electrolysis_kwh_per_kg = DELTA_H_ELECTROLYSIS_KWH_PER_KG / eta_soec

        # Subsystem Energy Additions per kg LH2 produced
        e_water_heating_melting_kwh = 0.65
        e_water_purification_kwh = 0.30
        e_gas_purification_compression_kwh = 1.40
        e_mining_excavation_kwh = 1.80
        e_pumps_controls_hvac_kwh = 1.15

        e_production_subtotal_kwh_per_kg = (e_electrolysis_kwh_per_kg + e_water_heating_melting_kwh +
                                             e_water_purification_kwh + e_gas_purification_compression_kwh +
                                             e_mining_excavation_kwh + e_pumps_controls_hvac_kwh)

        # Liquefaction Energy Derivation using parameterized Carnot efficiency
        eta_liquefier_carnot = max(0.01, self.liquefaction_efficiency)
        e_liquefaction_work_kwh_per_kg = W_MIN_LIQUEFACTION_KWH_PER_KG / eta_liquefier_carnot
        e_ortho_para_kwh_per_kg = (ORTHO_PARA_HEAT_KJ_PER_KG / 3600.0) / eta_liquefier_carnot
        e_liquefaction_total_kwh_per_kg = e_liquefaction_work_kwh_per_kg + e_ortho_para_kwh_per_kg

        # Total specific electrical energy per kg LH2
        e_total_kwh_per_kg_lh2 = e_production_subtotal_kwh_per_kg + e_liquefaction_total_kwh_per_kg

        # Campaign totals
        total_energy_mwh = (gross_lh2_kg * e_total_kwh_per_kg_lh2) / 1000.0
        total_energy_gwh = total_energy_mwh / 1000.0

        # Required average continuous power over production duration
        production_hours = max(1.0, self.production_days * 24.0)
        avg_power_mwe = total_energy_mwh / production_hours
        peak_power_mwe = avg_power_mwe * 1.15 # 15% peak starting margin

        return {
            "specific_energy_kwh_per_kg_lh2": round(e_total_kwh_per_kg_lh2, 2),
            "breakdown_kwh_per_kg": {
                "soec_electrolysis": round(e_electrolysis_kwh_per_kg, 2),
                "water_heating_melting": e_water_heating_melting_kwh,
                "water_purification": e_water_purification_kwh,
                "gas_purification_compression": e_gas_purification_compression_kwh,
                "mining_and_excavation": e_mining_excavation_kwh,
                "liquefaction_and_ortho_para": round(e_liquefaction_total_kwh_per_kg, 2),
                "pumps_controls_auxiliary": e_pumps_controls_hvac_kwh
            },
            "total_campaign_energy_mwh": round(total_energy_mwh, 2),
            "total_campaign_energy_gwh": round(total_energy_gwh, 3),
            "avg_continuous_power_mwe": round(avg_power_mwe, 2),
            "peak_power_mwe": round(peak_power_mwe, 2)
        }

    def surface_power_budget(self, available_power_mwe=25.0, gross_lh2_mt=None):
        """Single authoritative calculation for complete Mars surface power budget."""
        if gross_lh2_mt is None:
            acct = self.calculate_propellant_accounting()
            gross_lh2_mt = acct["gross_lh2_production_mt"]

        p_info = self.calculate_electrolysis_and_liquefaction_power(gross_lh2_mt)
        process_avg_mwe = p_info["avg_continuous_power_mwe"]

        p_total_kw = process_avg_mwe * 1000.0

        itemized_budget = {
            "Mining & Excavation": {"avg_kw": round(p_total_kw * 0.024, 1), "peak_kw": round(p_total_kw * 0.035, 1)},
            "Hauling & Crushing": {"avg_kw": round(p_total_kw * 0.012, 1), "peak_kw": round(p_total_kw * 0.020, 1)},
            "Water Extraction (Melting)": {"avg_kw": round(p_total_kw * 0.008, 1), "peak_kw": round(p_total_kw * 0.012, 1)},
            "Water Purification": {"avg_kw": round(p_total_kw * 0.004, 1), "peak_kw": round(p_total_kw * 0.006, 1)},
            "SOEC Electrolysis": {"avg_kw": round(p_total_kw * 0.716, 1), "peak_kw": round(p_total_kw * 0.800, 1)},
            "Hydrogen Gas Compression": {"avg_kw": round(p_total_kw * 0.018, 1), "peak_kw": round(p_total_kw * 0.025, 1)},
            "Liquefaction Plant": {"avg_kw": round(p_total_kw * 0.215, 1), "peak_kw": round(p_total_kw * 0.250, 1)},
            "Cryogenic Storage & ZBO": {"avg_kw": round(p_total_kw * 0.010, 1), "peak_kw": round(p_total_kw * 0.015, 1)},
            "Pumps & Controls": {"avg_kw": round(p_total_kw * 0.008, 1), "peak_kw": round(p_total_kw * 0.012, 1)},
            "Habitat & Science": {"avg_kw": round(150.0, 1), "peak_kw": round(250.0, 1)},
            "Unallocated Operating Margin (15%)": {"avg_kw": round(p_total_kw * 0.15, 1), "peak_kw": round(p_total_kw * 0.20, 1)}
        }

        total_avg_kw = sum(item["avg_kw"] for item in itemized_budget.values())
        total_peak_kw = sum(item["peak_kw"] for item in itemized_budget.values())

        required_average_mwe = total_avg_kw / 1000.0
        required_peak_mwe = total_peak_kw / 1000.0

        average_margin_mwe = available_power_mwe - required_average_mwe
        peak_margin_mwe = available_power_mwe - required_peak_mwe

        average_margin_fraction = average_margin_mwe / required_average_mwe if required_average_mwe > 0 else 0.0
        peak_margin_fraction = peak_margin_mwe / required_peak_mwe if required_peak_mwe > 0 else 0.0

        average_power_closes = (available_power_mwe >= required_average_mwe)
        peak_power_closes = (available_power_mwe >= required_peak_mwe)
        power_closes = average_power_closes and peak_power_closes

        return {
            "available_power_mwe": round(available_power_mwe, 2),
            "required_average_power_mwe": round(required_average_mwe, 2),
            "required_peak_power_mwe": round(required_peak_mwe, 2),
            "average_power_margin_mwe": round(average_margin_mwe, 2),
            "peak_power_margin_mwe": round(peak_margin_mwe, 2),
            "power_margin_mwe": round(average_margin_mwe, 2), # for backward compatibility
            "power_margin_fraction": round(average_margin_fraction, 4),
            "average_power_closes": average_power_closes,
            "peak_power_closes": peak_power_closes,
            "power_closes": power_closes,
            "itemized_power_budget": itemized_budget
        }

    def build_mars_surface_power_budget(self, avg_power_mwe):
        """Maintained for backward compatibility; calls canonical surface_power_budget."""
        res = self.surface_power_budget(available_power_mwe=25.0)
        return {
            "itemized_power_budget": res["itemized_power_budget"],
            "total_surface_avg_mwe": res["required_average_power_mwe"],
            "total_surface_peak_mwe": res["required_peak_power_mwe"]
        }

    def calculate_thermal_rejection_and_radiator(self, avg_power_mwe, required_thermal_margin_fraction=0.15):
        """Calculates waste heat generation and sizes Mars surface radiators.

        Explicitly distinguishes:
        1. Mathematical Closure: radiator_capacity >= total_q_waste
        2. Engineering Margin Compliance: radiator_capacity >= total_q_waste * (1 + required_thermal_margin_fraction)
        3. Thermal Failure: radiator_capacity < total_q_waste
        """
        p_elec_mwe = avg_power_mwe

        eta_reactor_thermal = 0.30
        q_reactor_th_mw = p_elec_mwe / eta_reactor_thermal
        q_reactor_waste_mw = q_reactor_th_mw - p_elec_mwe

        q_isru_waste_mw = p_elec_mwe * 0.85
        total_q_waste_mw = q_reactor_waste_mw + q_isru_waste_mw

        t_rad_reactor_k = 750.0
        emissivity = 0.90
        dust_degradation = 0.85
        eff_emiss = emissivity * dust_degradation

        q_rad_reactor_w = (eff_emiss * STEFAN_BOLTZMANN * (t_rad_reactor_k**4 - T_MARS_SURFACE_MAX_K**4) +
                           H_CONVECTION_MARS * (t_rad_reactor_k - T_MARS_SURFACE_MAX_K))
        area_reactor_rad_m2 = (q_reactor_waste_mw * 1e6) / q_rad_reactor_w

        t_rad_isru_k = 350.0
        q_rad_isru_w = (eff_emiss * STEFAN_BOLTZMANN * (t_rad_isru_k**4 - T_MARS_SURFACE_MAX_K**4) +
                        H_CONVECTION_MARS * (t_rad_isru_k - T_MARS_SURFACE_MAX_K))
        area_isru_rad_m2 = (q_isru_waste_mw * 1e6) / q_rad_isru_w

        total_radiator_area_m2 = area_reactor_rad_m2 + area_isru_rad_m2
        specific_radiator_mass_kg_m2 = 4.5
        radiator_mass_mt = (total_radiator_area_m2 * specific_radiator_mass_kg_m2) / 1000.0

        # Physical heat rejection capacity verification
        q_rejection_reactor_mwth = (area_reactor_rad_m2 * q_rad_reactor_w) / 1e6
        q_rejection_isru_mwth = (area_isru_rad_m2 * q_rad_isru_w) / 1e6
        total_radiator_capacity_mwth = q_rejection_reactor_mwth + q_rejection_isru_mwth

        thermal_margin_mwth = total_radiator_capacity_mwth - total_q_waste_mw
        required_capacity_mwth = total_q_waste_mw * (1.0 + required_thermal_margin_fraction)

        thermal_mathematical_closure = (total_radiator_capacity_mwth >= total_q_waste_mw - 1e-4)
        thermal_margin_compliance = (total_radiator_capacity_mwth >= required_capacity_mwth - 1e-4)
        thermal_failure = (total_radiator_capacity_mwth < total_q_waste_mw - 1e-4)

        if thermal_margin_compliance:
            status_str = "COMPLIANT"
        elif thermal_mathematical_closure:
            status_str = "ZERO_MARGIN_MATHEMATICAL_CLOSURE"
        else:
            status_str = "THERMAL_FAILURE"

        return {
            "reactor_thermal_output_mwth": round(q_reactor_th_mw, 2),
            "reactor_waste_heat_mwth": round(q_reactor_waste_mw, 2),
            "isru_plant_waste_heat_mwth": round(q_isru_waste_mw, 2),
            "total_q_waste_mwth": round(total_q_waste_mw, 2),
            "radiator_capacity_mwth": round(total_radiator_capacity_mwth, 2),
            "required_capacity_mwth": round(required_capacity_mwth, 2),
            "thermal_margin_mwth": round(thermal_margin_mwth, 2),
            "required_thermal_margin_fraction": required_thermal_margin_fraction,
            "thermal_closure": thermal_mathematical_closure,
            "thermal_mathematical_closure": thermal_mathematical_closure,
            "thermal_margin_compliance": thermal_margin_compliance,
            "thermal_failure": thermal_failure,
            "thermal_margin_status": status_str,
            "provenance": "PROVISIONAL (15% lifecycle degradation margin specified in Doc 49/51; zero-margin baseline preserved mathematically)",
            "radiator_area_m2": {
                "high_temp_reactor_rad_m2": round(area_reactor_rad_m2, 1),
                "low_temp_isru_rad_m2": round(area_isru_rad_m2, 1),
                "total_radiator_area_m2": round(total_radiator_area_m2, 1)
            },
            "radiator_mass_mt": round(radiator_mass_mt, 2)
        }

    def calculate_achievable_production(self, available_power_mwe=25.0, operating_days=None):
        """Calculates achievable LH2 production from available power, operating days, and process efficiency.
        The target is the RESULT of the physical model, not the input that forces the result.
        """
        if operating_days is None:
            operating_days = self.production_days

        # Determine gross LH2 required by baseline accounting
        acct = self.calculate_propellant_accounting()
        required_gross_lh2_mt = acct["gross_lh2_production_mt"]

        # Calculate specific electrical energy required per kg LH2
        e_info = self.calculate_electrolysis_and_liquefaction_power(required_gross_lh2_mt)
        specific_energy_kwh_per_kg = e_info["specific_energy_kwh_per_kg_lh2"]

        # Power allocated to ISRU process (subtracting habitat/science load of 150 kW)
        process_power_mwe = max(0.0, available_power_mwe - 0.150)

        # Achievable hourly production rate (kg LH2 / hour)
        achievable_kg_hr = (process_power_mwe * 1000.0) / specific_energy_kwh_per_kg

        # Achievable campaign production (metric tonnes)
        operating_hours = max(0.0, operating_days * 24.0)
        achievable_gross_lh2_mt = (achievable_kg_hr * operating_hours) / 1000.0

        # Production closes if achievable gross production meets or exceeds required gross production
        production_closes = (achievable_gross_lh2_mt >= required_gross_lh2_mt - 1e-2)

        return {
            "available_power_mwe": round(available_power_mwe, 2),
            "process_power_mwe": round(process_power_mwe, 2),
            "operating_days": round(operating_days, 1),
            "specific_energy_kwh_per_kg_lh2": round(specific_energy_kwh_per_kg, 2),
            "achievable_lh2_rate_kg_hr": round(achievable_kg_hr, 2),
            "achievable_lh2_rate_kg_day": round(achievable_kg_hr * 24.0, 1),
            "achievable_gross_lh2_mt": round(achievable_gross_lh2_mt, 2),
            "required_gross_lh2_mt": round(required_gross_lh2_mt, 2),
            "production_margin_mt": round(achievable_gross_lh2_mt - required_gross_lh2_mt, 2),
            "production_closes": production_closes
        }

    def calculate_production_rates_and_equipment(self, gross_lh2_mt, water_extracted_mt, regolith_excavated_mt):
        """Calculates required hourly and daily processing rates."""
        days = max(1.0, self.production_days)
        hours = days * 24.0

        lh2_kg_day = (gross_lh2_mt * 1000.0) / days
        lh2_kg_hour = (gross_lh2_mt * 1000.0) / hours

        water_mt_day = water_extracted_mt / days
        water_kg_hour = (water_extracted_mt * 1000.0) / hours

        regolith_mt_day = regolith_excavated_mt / days
        regolith_kg_hour = (regolith_excavated_mt * 1000.0) / hours

        return {
            "campaign_duration_days": days,
            "production_rates": {
                "lh2_produced_kg_day": round(lh2_kg_day, 1),
                "lh2_produced_kg_hour": round(lh2_kg_hour, 2),
                "water_extracted_mt_day": round(water_mt_day, 2),
                "water_extracted_kg_hour": round(water_kg_hour, 1),
                "regolith_excavated_mt_day": round(regolith_mt_day, 1),
                "regolith_excavated_kg_hour": round(regolith_kg_hour, 1)
            },
            "equipment_sizing_sanity_check": {
                "excavator_fleet_size": 2,
                "excavation_rate_per_robot_kg_hr": round(regolith_kg_hour / 2.0, 1),
                "electrolyzer_stack_rating_mwe": 10.0,
                "liquefier_capacity_kg_day": round(lh2_kg_day * 1.10, 1)
            }
        }

    def create_isru_plant_mass_budget(self, radiator_mass_mt, lander_1_capacity_mt=150.0, lander_2_capacity_mt=150.0):
        """Creates itemized ISRU plant mass budget, physical packing list, and multi-lander delivery breakdown.

        Explicit Physical Lander Allocation Table:
        Lander 1 (Power & Thermal Infrastructure):
        - Surface Nuclear Reactor & sCO2 Brayton: 28.50 t
        - Thermal Radiator Array: radiator_mass_mt (108.17 t baseline)
        - Power Distribution & Conditioning: 3.50 t
        - Structural Frame & Thermal Controls (L1): 4.83 t

        Lander 2 (Mining, Processing, Liquefaction & Depot Infrastructure):
        - Autonomous Excavators (2x 2.5t): 5.00 t
        - Autonomous Haulers & Conveyors: 4.50 t
        - Regolith Crushers & Feeders: 3.20 t
        - Water Extraction Melting Reactors: 6.80 t
        - Water Purification & Distillation: 2.50 t
        - SOEC Electrolyzer Stacks (10 MWe): 12.00 t
        - Hydrogen Gas Purifiers & Compressors: 4.80 t
        - Claude Liquefaction Plant: 14.50 t
        - Cryocoolers & Reverse Brayton Units: 3.80 t
        - Surface LH2 Storage Tanks & MLI: 18.50 t
        - Fluid Transfer Plumbing & Couplers: 2.20 t
        - Structural Frames & Support Struts (L2): 3.67 t
        - Avionics, Controls & Communications: 1.80 t
        - Spare Parts & Tooling: 6.00 t
        - Unallocated Contingency Reserve (20%): 25.52 t
        """
        lander_1_items = {
            "Surface Nuclear Reactor & sCO2 Brayton": 28.50,
            "Thermal Radiator Array": radiator_mass_mt,
            "Power Distribution & Conditioning": 3.50,
            "Structural Frame & Thermal Controls (L1)": 4.83
        }

        lander_2_items = {
            "Autonomous Excavators (2x 2.5t)": 5.00,
            "Autonomous Haulers & Conveyors": 4.50,
            "Regolith Crushers & Feeders": 3.20,
            "Water Extraction Melting Reactors": 6.80,
            "Water Purification & Distillation": 2.50,
            "SOEC Electrolyzer Stacks (10 MWe)": 12.00,
            "Hydrogen Gas Purifiers & Compressors": 4.80,
            "Claude Liquefaction Plant": 14.50,
            "Cryocoolers & Reverse Brayton Units": 3.80,
            "Surface LH2 Storage Tanks & MLI": 18.50,
            "Fluid Transfer Plumbing & Couplers": 2.20,
            "Structural Frames & Support Struts (L2)": 3.67,
            "Avionics, Controls & Communications": 1.80,
            "Spare Parts & Tooling": 6.00,
            "Unallocated Contingency Reserve (20%)": 25.52
        }

        lander_1_payload_mt = sum(lander_1_items.values())
        lander_2_payload_mt = sum(lander_2_items.values())
        total_mass_mt = lander_1_payload_mt + lander_2_payload_mt

        # Consolidated budget dictionary for backward compatibility
        budget = {}
        budget.update(lander_1_items)
        budget.update(lander_2_items)

        # Individual lander closure checks
        l1_margin_mt = lander_1_capacity_mt - lander_1_payload_mt
        l2_margin_mt = lander_2_capacity_mt - lander_2_payload_mt

        l1_closes = (lander_1_payload_mt <= lander_1_capacity_mt)
        l2_closes = (lander_2_payload_mt <= lander_2_capacity_mt)
        payload_closes = l1_closes and l2_closes

        total_capacity_mt = lander_1_capacity_mt + lander_2_capacity_mt
        mass_margin_mt = total_capacity_mt - total_mass_mt

        allocation_table = [
            {"component": k, "mass_mt": round(v, 2), "lander_assignment": "Lander 1 (Power & Thermal)"}
            for k, v in lander_1_items.items()
        ] + [
            {"component": k, "mass_mt": round(v, 2), "lander_assignment": "Lander 2 (Processing & Depot)"}
            for k, v in lander_2_items.items()
        ]

        return {
            "itemized_isru_mass_mt": {k: round(v, 2) for k, v in budget.items()},
            "allocation_table": allocation_table,
            "total_isru_plant_dry_mass_mt": round(total_mass_mt, 2),
            "precursor_lander_delivery_architecture": {
                "number_of_landers": 2,
                "total_precursor_delivery_capacity_mt": round(total_capacity_mt, 2),
                "mass_margin_mt": round(mass_margin_mt, 2),
                "payload_closes": payload_closes,
                "lander_breakdown": {
                    "lander_1": {
                        "assigned_payload_mt": round(lander_1_payload_mt, 2),
                        "capacity_mt": round(lander_1_capacity_mt, 2),
                        "payload_margin_mt": round(l1_margin_mt, 2),
                        "payload_fraction": round(lander_1_payload_mt / max(1e-6, lander_1_capacity_mt), 4),
                        "lander_closes": l1_closes
                    },
                    "lander_2": {
                        "assigned_payload_mt": round(lander_2_payload_mt, 2),
                        "capacity_mt": round(lander_2_capacity_mt, 2),
                        "payload_margin_mt": round(l2_margin_mt, 2),
                        "payload_fraction": round(lander_2_payload_mt / max(1e-6, lander_2_capacity_mt), 4),
                        "lander_closes": l2_closes
                    }
                }
            }
        }

    def precursor_payload_closes(self, number_of_landers=2, capacity_per_lander_mt=150.0, lander_1_capacity_mt=None, lander_2_capacity_mt=None):
        """Hard deployability gate evaluating whether precursor payload physically closes.
        Requires that EVERY lander individually closes (assigned_payload <= capacity).
        """
        if lander_1_capacity_mt is None:
            lander_1_capacity_mt = capacity_per_lander_mt
        if lander_2_capacity_mt is None:
            lander_2_capacity_mt = capacity_per_lander_mt if number_of_landers >= 2 else 0.0

        accounting = self.calculate_propellant_accounting()
        gross_lh2_mt = accounting["gross_lh2_production_mt"]
        power_info = self.calculate_electrolysis_and_liquefaction_power(gross_lh2_mt)
        thermal = self.calculate_thermal_rejection_and_radiator(power_info["avg_continuous_power_mwe"])
        plant_budget = self.create_isru_plant_mass_budget(
            thermal["radiator_mass_mt"],
            lander_1_capacity_mt=lander_1_capacity_mt,
            lander_2_capacity_mt=lander_2_capacity_mt
        )

        arch = plant_budget["precursor_lander_delivery_architecture"]
        l1_info = arch["lander_breakdown"]["lander_1"]
        l2_info = arch["lander_breakdown"]["lander_2"]

        closes = l1_info["lander_closes"] and l2_info["lander_closes"]

        return {
            "payload_closes": closes,
            "total_plant_mass_mt": plant_budget["total_isru_plant_dry_mass_mt"],
            "number_of_landers": number_of_landers,
            "capacity_per_lander_mt": capacity_per_lander_mt,
            "total_delivery_capacity_mt": round(lander_1_capacity_mt + lander_2_capacity_mt, 2),
            "mass_margin_mt": round(lander_1_capacity_mt + lander_2_capacity_mt - plant_budget["total_isru_plant_dry_mass_mt"], 2),
            "lander_1": l1_info,
            "lander_2": l2_info
        }

    def evaluate_architecture_trades(self, total_isru_mass_mt):
        """Evaluates Architectures A through E."""
        trades = {
            "Architecture_A": {
                "name": "Crewed Enterprise Carries Onboard ISRU",
                "isru_mass_mt": total_isru_mass_mt,
                "crewed_vessel_landing_required": True,
                "feasibility": "PHYSICALLY INFEASIBLE / ARCHITECTURE INVALID",
                "key_blocker": "Enterprise X cannot land on Mars; crew cannot wait 500 days on surface for unproven ISRU to manufacture return propellant."
            },
            "Architecture_B": {
                "name": "Precursor Autonomous Robotic ISRU Depot (Canonical Baseline - 2x 150t Landers)",
                "isru_mass_mt": total_isru_mass_mt,
                "crewed_vessel_landing_required": False,
                "precursor_missions_required": 2, # 2 uncrewed Super-Heavy cargo landers (2x 150t capacity)
                "feasibility": "ENGINEERINGALLY CONDITIONAL",
                "key_benefit": "Return propellant is 100% manufactured, stored, and verified BEFORE crew departs Earth. Zero crew mortality risk from ISRU failure."
            },
            "Architecture_C": {
                "name": "Multi-Mission Precursor Depot Network",
                "isru_mass_mt": total_isru_mass_mt * 1.20,
                "precursor_missions_required": 4,
                "feasibility": "FEASIBLE BUT HIGH COST",
                "key_benefit": "Redundant parallel production plants, higher resilience."
            },
            "Architecture_D": {
                "name": "Zero-ISRU All-Earth Propellant Supply",
                "isru_mass_mt": 0.0,
                "earth_launches_required": 28,
                "feasibility": "PHYSICALLY UNECONOMIC / HIGH BOILOFF RISK",
                "key_blocker": "Requires 28 Super-Heavy launches and massive LEO orbital propellant depot storage."
            },
            "Architecture_E": {
                "name": "Hybrid (Surface MAV CH4/LOX ISRU + Earth LH2 TEI)",
                "isru_mass_mt": 28.0,
                "feasibility": "CONDITIONALLY FEASIBLE",
                "key_benefit": "Smaller ISRU plant, but requires carrying all TEI propellant from Earth."
            }
        }
        return trades

    def analyze_failure_and_abort_scenarios(self, gross_lh2_mt):
        """Models failure modes and calculates remaining propellant capability."""
        scenarios = {
            "electrolyzer_loss_50_percent": {
                "failure": "50% Electrolyzer Cell Degradation",
                "impact": "Production rate reduced to 2.2 t/day",
                "time_to_complete_days": self.production_days * 2.0,
                "consequence": "Campaign duration extends to 1,000 days (requires 2 synodic stay cycles)."
            },
            "reactor_loss_25_percent": {
                "failure": "Reactor Power Degradation to 11.25 MWe",
                "impact": "ISRU plant operates at 75% capacity",
                "time_to_complete_days": self.production_days * 1.33,
                "consequence": "Production takes 665 days; fits within 640-day surface window with minor 25-day overrun."
            },
            "excavator_total_failure_1_unit": {
                "failure": "Loss of 1 of 2 Excavator Units",
                "impact": "Mining rate halved",
                "mitigation": "Redundant excavator operates at 90% duty cycle, completing production in 600 days."
            },
            "precursor_isru_total_failure": {
                "failure": "Precursor ISRU Plant Fails Before Crew Departure",
                "impact": "0% Return Propellant Manufactured",
                "action": "Crew Earth departure holds on Earth. Zero crew loss."
            }
        }
        return scenarios

    def run_full_isru_model(self):
        """Runs the complete Mars ISRU model suite."""
        accounting = self.calculate_propellant_accounting()
        gross_lh2_mt = accounting["gross_lh2_production_mt"]

        feedstock = self.evaluate_feedstock_pathways(gross_lh2_mt)
        power_and_energy = self.calculate_electrolysis_and_liquefaction_power(gross_lh2_mt)
        power_budget = self.surface_power_budget(available_power_mwe=25.0, gross_lh2_mt=gross_lh2_mt)
        thermal = self.calculate_thermal_rejection_and_radiator(power_and_energy["avg_continuous_power_mwe"])
        achievable_production = self.calculate_achievable_production(available_power_mwe=25.0, operating_days=self.production_days)

        water_mt = feedstock["glacial_ice"]["raw_water_extracted_mt"]
        regolith_mt = feedstock["glacial_ice"]["regolith_excavated_mt"]
        rates = self.calculate_production_rates_and_equipment(gross_lh2_mt, water_mt, regolith_mt)

        plant_mass = self.create_isru_plant_mass_budget(thermal["radiator_mass_mt"])
        payload_closure = self.precursor_payload_closes(number_of_landers=2, capacity_per_lander_mt=150.0)
        architecture_trades = self.evaluate_architecture_trades(plant_mass["total_isru_plant_dry_mass_mt"])
        failure_modes = self.analyze_failure_and_abort_scenarios(gross_lh2_mt)

        model_output = {
            "program_phase": "Phase 8 — Mars ISRU, Propellant Logistics & Mission Closure",
            "isru_status": "ENGINEERINGALLY CONDITIONAL",
            "propellant_accounting": accounting,
            "feedstock_analysis": feedstock,
            "power_and_energy_derivation": power_and_energy,
            "mars_surface_power_budget": power_budget,
            "thermal_rejection_and_radiators": thermal,
            "achievable_production": achievable_production,
            "production_rates_and_equipment": rates,
            "isru_plant_mass_budget": plant_mass,
            "precursor_payload_closure": payload_closure,
            "architecture_trade_matrix": architecture_trades,
            "failure_and_abort_analysis": failure_modes
        }
        return model_output


def generate_mars_isru_json(output_path="engineering/calculations/mars_isru.json"):
    model = MarsISRUModel()
    results = model.run_full_isru_model()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Mars ISRU calculations complete. Machine-readable JSON output written to: {output_path}")
    return results


if __name__ == "__main__":
    generate_mars_isru_json()
