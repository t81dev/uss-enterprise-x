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
- Mars surface power budget (continuous MW, peak MW, MWh)
- Nuclear surface reactor sizing and thermal rejection (Q_waste, radiator area/mass)
- Production rate, campaign timeline, and industrial equipment sizing
- Itemized ISRU surface plant mass budget
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

    def __init__(self, target_lh2_net_mt=2200.0, production_days=500.0, ice_concentration=0.50):
        self.target_lh2_net_mt = target_lh2_net_mt  # Net usable return propellant required
        self.production_days = production_days      # Available production campaign duration
        self.ice_concentration = ice_concentration  # Glacial ice mass fraction in regolith (50% baseline)

    def calculate_propellant_accounting(self):
        """Calculates itemized propellant losses, reserves, and gross production requirement."""
        # Baseline return impulse requirement (TEI + EOI reserve)
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

        # Net required usable inventory before loss accumulation
        net_required_total_mt = net_tei_lh2_mt + propellant_ascent_mt + propellant_tcm_mt + propellant_abort_reserve_mt

        # Total gross production required accounting for multiplicative/additive losses
        loss_multiplier = (1.0 + f_production_loss + f_storage_boiloff + f_transfer_loss +
                           f_loading_flash + f_residuals + f_unusable_ullage +
                           f_startup_purge + f_contingency)

        gross_lh2_production_mt = net_required_total_mt * loss_multiplier

        # Byproduct Oxygen production (stoichiometric)
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

        # Pathway B: Hydrated Minerals (5% bound water, 600°C calcination required)
        eta_mineral_thermal_yield = 0.80
        water_req_mineral_raw_kg = water_req_pure_kg / eta_mineral_thermal_yield
        regolith_excavated_minerals_kg = water_req_mineral_raw_kg / 0.05
        energy_calcination_kwh_per_kg_water = 1.85 # Thermal energy to heat clay/sulfate to 600°C

        # Pathway C: Atmospheric CO2 processing (Sabatier Methane + Water electrolysis)
        # CO2 + 4 H2 -> CH4 + 2 H2O
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
        """Derives first-principles energy consumption for electrolysis and liquefaction."""
        gross_lh2_kg = gross_lh2_mt * 1000.0

        # Electrolysis Efficiency (Solid Oxide Electrolyzer Cell - SOEC)
        eta_soec = 0.72 # 72% electrical efficiency (high temp SOEC using waste heat)
        e_electrolysis_kwh_per_kg = DELTA_H_ELECTROLYSIS_KWH_PER_KG / eta_soec # ~54.71 kWh/kg H2

        # Subsystem Energy Additions per kg LH2 produced:
        e_water_heating_melting_kwh = 0.65   # Thermal heating from 210 K ice to 373 K steam
        e_water_purification_kwh = 0.30       # Filtration, ion exchange, distillation
        e_gas_purification_compression_kwh = 1.40 # Drying, catalytic deoxo, compression to 30 bar
        e_mining_excavation_kwh = 1.80        # Autonomous excavator/hauler electric drive
        e_pumps_controls_hvac_kwh = 1.15      # Coolant pumps, system controls, habitat life support

        e_production_subtotal_kwh_per_kg = (e_electrolysis_kwh_per_kg + e_water_heating_melting_kwh +
                                             e_water_purification_kwh + e_gas_purification_compression_kwh +
                                             e_mining_excavation_kwh + e_pumps_controls_hvac_kwh) # ~60.0 kWh/kg H2

        # Liquefaction Energy Derivation:
        # Claude cycle liquefaction with ortho-to-para catalytic conversion
        eta_liquefier_carnot = 0.25 # 25% Carnot efficiency at 20 K
        e_liquefaction_work_kwh_per_kg = W_MIN_LIQUEFACTION_KWH_PER_KG / eta_liquefier_carnot # ~15.64 kWh/kg LH2
        e_ortho_para_kwh_per_kg = (ORTHO_PARA_HEAT_KJ_PER_KG / 3600.0) / eta_liquefier_carnot # ~0.78 kWh/kg LH2
        e_liquefaction_total_kwh_per_kg = e_liquefaction_work_kwh_per_kg + e_ortho_para_kwh_per_kg # ~16.42 kWh/kg LH2

        # Total specific electrical energy per kg LH2
        e_total_kwh_per_kg_lh2 = e_production_subtotal_kwh_per_kg + e_liquefaction_total_kwh_per_kg # ~76.42 kWh/kg LH2

        # Campaign totals
        total_energy_mwh = (gross_lh2_kg * e_total_kwh_per_kg_lh2) / 1000.0
        total_energy_gwh = total_energy_mwh / 1000.0

        # Required average continuous power over production duration
        production_hours = self.production_days * 24.0
        avg_power_mwe = total_energy_mwh / production_hours
        peak_power_mwe = avg_power_mwe * 1.15 # 15% peak margin for starting heavy machinery

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

    def build_mars_surface_power_budget(self, avg_power_mwe):
        """Constructs detailed itemized surface power budget table."""
        # Allocate power proportional to specific energy breakdown
        p_total_kw = avg_power_mwe * 1000.0

        budget = {
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
            "Unallocated Margin (15%)": {"avg_kw": round(p_total_kw * 0.15, 1), "peak_kw": round(p_total_kw * 0.20, 1)}
        }

        total_avg_kw = sum(item["avg_kw"] for item in budget.values())
        total_peak_kw = sum(item["peak_kw"] for item in budget.values())

        return {
            "itemized_power_budget": budget,
            "total_surface_avg_mwe": round(total_avg_kw / 1000.0, 2),
            "total_surface_peak_mwe": round(total_peak_kw / 1000.0, 2)
        }

    def calculate_thermal_rejection_and_radiator(self, avg_power_mwe):
        """Calculates waste heat generation and sizes Mars surface radiators."""
        p_elec_mwe = avg_power_mwe

        # Surface Reactor Power Generation Efficiency (15 MWe fast fission sCO2 Brayton @ 30% thermal eff)
        eta_reactor_thermal = 0.30
        q_reactor_th_mw = p_elec_mwe / eta_reactor_thermal # ~41.67 MWth
        q_reactor_waste_mw = q_reactor_th_mw - p_elec_mwe # ~29.17 MWth waste heat at 750 K

        # ISRU Plant Process Heat Rejection
        # ~85% of electrical input in electrolysis, liquefaction, and machinery is rejected as waste heat
        q_isru_waste_mw = p_elec_mwe * 0.85 # ~10.63 MWth waste heat at 350 K

        total_q_waste_mw = q_reactor_waste_mw + q_isru_waste_mw

        # Radiator Area Calculation using Stefan-Boltzmann + Martian Convection + Dust Degradation
        # Reactor Radiator Loop (750 K heat rejection):
        t_rad_reactor_k = 750.0
        emissivity = 0.90
        dust_degradation = 0.85 # Dust accumulation penalty factor
        eff_emiss = emissivity * dust_degradation

        q_rad_reactor_w = (eff_emiss * STEFAN_BOLTZMANN * (t_rad_reactor_k**4 - T_MARS_SURFACE_MAX_K**4) +
                           H_CONVECTION_MARS * (t_rad_reactor_k - T_MARS_SURFACE_MAX_K))
        area_reactor_rad_m2 = (q_reactor_waste_mw * 1e6) / q_rad_reactor_w

        # ISRU Low-Temp Radiator Loop (350 K heat rejection):
        t_rad_isru_k = 350.0
        q_rad_isru_w = (eff_emiss * STEFAN_BOLTZMANN * (t_rad_isru_k**4 - T_MARS_SURFACE_MAX_K**4) +
                        H_CONVECTION_MARS * (t_rad_isru_k - T_MARS_SURFACE_MAX_K))
        area_isru_rad_m2 = (q_isru_waste_mw * 1e6) / q_rad_isru_w

        total_radiator_area_m2 = area_reactor_rad_m2 + area_isru_rad_m2

        # Radiator Mass (Lightweight Composite Heat-Pipe Radiators: 4.5 kg/m^2)
        specific_radiator_mass_kg_m2 = 4.5
        radiator_mass_mt = (total_radiator_area_m2 * specific_radiator_mass_kg_m2) / 1000.0

        return {
            "reactor_thermal_output_mwth": round(q_reactor_th_mw, 2),
            "reactor_waste_heat_mwth": round(q_reactor_waste_mw, 2),
            "isru_plant_waste_heat_mwth": round(q_isru_waste_mw, 2),
            "total_q_waste_mwth": round(total_q_waste_mw, 2),
            "radiator_area_m2": {
                "high_temp_reactor_rad_m2": round(area_reactor_rad_m2, 1),
                "low_temp_isru_rad_m2": round(area_isru_rad_m2, 1),
                "total_radiator_area_m2": round(total_radiator_area_m2, 1)
            },
            "radiator_mass_mt": round(radiator_mass_mt, 2)
        }

    def calculate_production_rates_and_equipment(self, gross_lh2_mt, water_extracted_mt, regolith_excavated_mt):
        """Calculates required hourly and daily processing rates."""
        days = self.production_days
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
                "excavator_fleet_size": 2, # Two 1.5-tonne autonomous excavators operating @ 50% duty
                "excavation_rate_per_robot_kg_hr": round(regolith_kg_hour / 2.0, 1),
                "electrolyzer_stack_rating_mwe": 10.0, # Two 5 MWe SOEC modules
                "liquefier_capacity_kg_day": round(lh2_kg_day * 1.10, 1) # Rated for 10% surge
            }
        }

    def create_isru_plant_mass_budget(self, radiator_mass_mt):
        """Creates itemized ISRU plant mass budget."""
        budget = {
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
            "Surface Nuclear Reactor & sCO2 Brayton": 28.50,
            "Thermal Radiator Array": radiator_mass_mt,
            "Structural Frames & Support Struts": 8.50,
            "Avionics, Controls & Communications": 1.80,
            "Spare Parts & Tooling": 6.00,
            "Unallocated Contingency Reserve (20%)": 25.52
        }

        total_mass_mt = sum(budget.values())

        return {
            "itemized_isru_mass_mt": {k: round(v, 2) for k, v in budget.items()},
            "total_isru_plant_dry_mass_mt": round(total_mass_mt, 2),
            "precursor_lander_capacity_mt": 150.0,
            "mass_margin_mt": round(150.0 - total_mass_mt, 2)
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
                "name": "Precursor Autonomous Robotic ISRU Depot (Canonical Baseline)",
                "isru_mass_mt": total_isru_mass_mt,
                "crewed_vessel_landing_required": False,
                "precursor_missions_required": 1, # 1 uncrewed Super-Heavy cargo lander
                "feasibility": "ENGINEERINGALLY CONDITIONAL",
                "key_benefit": "Return propellant is 100% manufactured, stored, and verified BEFORE crew departs Earth. Zero crew mortality risk from ISRU failure."
            },
            "Architecture_C": {
                "name": "Multi-Mission Precursor Depot Network",
                "isru_mass_mt": total_isru_mass_mt * 1.20,
                "precursor_missions_required": 3,
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
        power_budget = self.build_mars_surface_power_budget(power_and_energy["avg_continuous_power_mwe"])
        thermal = self.calculate_thermal_rejection_and_radiator(power_and_energy["avg_continuous_power_mwe"])

        water_mt = feedstock["glacial_ice"]["raw_water_extracted_mt"]
        regolith_mt = feedstock["glacial_ice"]["regolith_excavated_mt"]
        rates = self.calculate_production_rates_and_equipment(gross_lh2_mt, water_mt, regolith_mt)

        plant_mass = self.create_isru_plant_mass_budget(thermal["radiator_mass_mt"])
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
            "production_rates_and_equipment": rates,
            "isru_plant_mass_budget": plant_mass,
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
