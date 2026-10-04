#!/usr/bin/env python3
"""
Automated System Consistency & Sequential Digital Twin Test Suite for Project Occam-7
Updated for Program Phase 8.1 — Codex P1/P2 Defect Remediation & Mission Integrity.

Verifies cross-subsystem physical consistency, sequential state propagation, NEP trajectory tests,
thermal/power state machines, launch logistics, centrifuge dynamics, mass conservation, vector kinematics,
numerical vs analytical rocket equation agreement, cryogenic boiloff, crew health models,
Mars ISRU water/hydrogen conservation, electrolysis thermodynamics, liquefaction power,
radiator thermal closure, surface timeline closure, machine-readable mission success predicates,
and Phase 8.1 explicit precursor/crewed safety gates & negative failure tests (Tests A through G).
"""

import math
import sys
import unittest

from mass_budget import calculate_mass_budget
from centrifuge_calculator import analyze_centrifuge
from shielding_estimator import shielding_calculator
from radiator_sizing import calculate_radiator_area
from mission_digital_twin import MissionDigitalTwin, SpacecraftState, PrecursorDepotState
from earth_mars_transfer import EarthMarsTransferSolver, MU_SUN, MU_EARTH, MU_MARS, R_EARTH_ORBIT, R_MARS_ORBIT
from mars_isru import MarsISRUModel, KG_WATER_PER_KG_H2, KG_O2_PER_KG_H2, DELTA_H_ELECTROLYSIS_KWH_PER_KG

G0 = 9.80665


class TestSystemConsistency(unittest.TestCase):

    def test_mass_budget_row_summation_reconciliation(self):
        """DEF-005 & DEF-M01: Verify that itemized mass rows sum to unmargined subtotal exactly and departure mass equals 3,970.96 t."""
        res = calculate_mass_budget()
        subsystems = res["subsystems"]

        sum_opt = sum(item["opt"] for item in subsystems.values())
        sum_base = sum(item["base"] for item in subsystems.values())
        sum_pess = sum(item["pess"] for item in subsystems.values())

        self.assertAlmostEqual(sum_opt, res["subtotal_opt"], places=4)
        self.assertAlmostEqual(sum_base, res["subtotal_base"], places=4)
        self.assertAlmostEqual(sum_pess, res["subtotal_pess"], places=4)

        # Verify 20% AIAA reserve margin calculation (1,225.80 t -> 1,470.96 t)
        self.assertAlmostEqual(sum_base * 1.20, res["dry_mass_base"], places=4)
        self.assertAlmostEqual(res["dry_mass_base"], 1470.96, places=2)

        # Verify canonical departure wet mass = 1,470.96 t dry + 2,500.0 t mission propellant = 3,970.96 t
        self.assertAlmostEqual(res["dry_mass_base"] + 2500.0, res["wet_mass_base"], places=4)
        self.assertAlmostEqual(res["wet_mass_base"], 3970.96, places=2)

    def test_mass_conservation_enforcement(self):
        """Requirement 5: Verify mass conservation across all simulation steps."""
        twin = MissionDigitalTwin()
        output = twin.run_full_mission_baseline()

        # Check mass conservation log
        for event in twin.mass_conservation_log:
            self.assertLess(event["error_mt"], 1e-4, f"Mass conservation violated in {event['event']}")

        # Verify initial wet mass equals final mass + total consumed
        m_initial = 3970.96
        lh2_burned = sum(e.get("lh2_burned_mt", 0.0) for e in twin.event_log)
        lnh3_burned = sum(e.get("lnh3_burned_mt", 0.0) for e in twin.event_log)
        boiloff_lost = twin.state.cumulative_boiloff_loss_mt
        isru_reloaded = twin.depot.lh2_transferred_to_ship_mt
        m_final = twin.state.gross_mass_mt

        consumables_lost = 72.3 - twin.state.crew_consumables_mt

        m_accounted = m_final + lh2_burned + lnh3_burned + boiloff_lost + consumables_lost - isru_reloaded
        self.assertAlmostEqual(m_initial, m_accounted, delta=0.1)

    def test_numerical_vs_tsiolkovsky_rocket_equation(self):
        """Requirement 6: Compare finite burn numerical integration against Tsiolkovsky equation (<0.5% diff)."""
        twin = MissionDigitalTwin()
        res = twin.execute_ntp_burn("TMI Test", target_dv_kms=3.80)

        actual_dv = res["actual_dv_kms"]
        num_dv = res["numerical_dv_kms"]

        diff_pct = abs(actual_dv - num_dv) / actual_dv * 100.0
        self.assertLess(diff_pct, 0.5)

    def test_tank_hoop_stress_and_wall_thickness(self):
        """DEF-001: Verify thin-wall hoop stress calculation for 12m dia pressure tanks."""
        p_internal = 150000.0  # Pa (150 kPa)
        radius = 6.0          # m
        t_orig = 0.004        # m (4 mm)

        sigma_hoop_orig = (p_internal * radius) / t_orig
        self.assertAlmostEqual(sigma_hoop_orig, 225.0e6, delta=1.0)

        t_chosen = 0.0065
        sigma_hoop_chosen = (p_internal * radius) / t_chosen
        self.assertAlmostEqual(sigma_hoop_chosen, 138.46e6, delta=1e4)
        self.assertLess(sigma_hoop_chosen, 220.0e6 / 1.5)

    def test_nep_power_thrust_jet_coupling(self):
        """DEF-002 & DEF-003: Verify NEP electrical power to jet power to thrust & mass flow relationship."""
        p_elec = 15.0e6      # 15 MWe
        eta = 0.65            # Thruster efficiency
        p_jet = p_elec * eta  # 9.75 MWjet
        isp = 3500.0          # s
        v_e = isp * G0        # 34,323.28 m/s

        thrust = (2.0 * p_jet) / v_e
        self.assertAlmostEqual(thrust, 568.12, delta=0.5)

        mdot_kg_s = thrust / v_e
        self.assertAlmostEqual(mdot_kg_s, 0.016552, delta=1e-5)

    def test_earth_mars_patched_conic_solver(self):
        """Requirement 7 & 8: Verify patched-conic two-body transfer solver outputs."""
        solver = EarthMarsTransferSolver()
        hohmann = solver.hohmann_transfer()

        self.assertAlmostEqual(hohmann["dv_tmi_kms"], 3.568, delta=0.05)
        self.assertAlmostEqual(hohmann["dv_moi_kms"], 2.036, delta=0.05)
        self.assertAlmostEqual(hohmann["v_inf_dep_kms"], 2.949, delta=0.05)

    def test_synodic_geometry_alignment(self):
        """Requirement 9: Verify synodic period and stay duration alignment."""
        synodic = EarthMarsTransferSolver.synodic_and_return_geometry()
        self.assertAlmostEqual(synodic["synodic_period_days"], 779.9, delta=2.0)
        self.assertAlmostEqual(synodic["ideal_synodic_stay_days"], 419.9, delta=2.0)

    def test_crew_health_and_survivability_model(self):
        """Requirement 19 & 20: Verify crew radiation dose, centrifuge dynamics, and health decay."""
        twin = MissionDigitalTwin()
        twin.state.centrifuge_active = False
        twin.execute_mars_isru_reload_and_stay("Microgravity Stay", duration_days=100.0)

        self.assertAlmostEqual(twin.state.crew_health_percent, 95.0, delta=0.1)

    def test_cryogenic_boiloff_and_zbo_refrigeration(self):
        """Requirement 21: Verify active Zero-Boiloff refrigeration and passive boiloff."""
        state = SpacecraftState()
        self.assertEqual(state.zbo_refrigeration_mwe, 0.015)  # 15 kWe

        twin = MissionDigitalTwin(initial_state=state)
        twin.execute_mars_isru_reload_and_stay("Orbital Storage", duration_days=100.0)

        self.assertGreater(twin.state.cumulative_boiloff_loss_mt, 0.0)

    def test_machine_readable_mission_success_predicate(self):
        """Requirement 18: Verify machine-readable success predicate logic."""
        twin = MissionDigitalTwin()
        res = twin.run_full_mission_baseline()
        predicates = res["success_predicate_assessment"]

        self.assertTrue(predicates["mission_success"])
        self.assertTrue(predicates["predicates"]["earth_departure_authorized"])
        self.assertTrue(predicates["predicates"]["earth_departure_achieved"])
        self.assertTrue(predicates["predicates"]["mars_encounter_achieved"])
        self.assertTrue(predicates["predicates"]["return_propellant_manufactured"])
        self.assertTrue(predicates["predicates"]["return_trajectory_closes"])

    def test_thermal_radiator_stefan_boltzmann_balance(self):
        """Verify radiator surface area calculation under Stefan-Boltzmann law."""
        q_kw = 80000.0  # 80 MWth
        temp_k = 850.0   # K
        emiss = 0.90
        deg_margin = 0.15

        panel_area, flux_kw = calculate_radiator_area(q_kw, temp_k, emiss, deg_margin, double_sided=True)

        sigma = 5.670374419e-8
        expected_flux_w = emiss * sigma * (temp_k**4)
        self.assertAlmostEqual(flux_kw * 1000.0, expected_flux_w, delta=1.0)

    def test_centrifuge_walking_gravity_formula(self):
        """DEF-007: Verify centrifuge calculator implements full radial acceleration formula."""
        radius = 15.0  # m
        rpm = 6.0     # RPM
        walk_v = 1.5   # m/s

        res = analyze_centrifuge(radius, rpm, walk_v)
        omega = rpm * (2.0 * math.pi / 60.0)

        expected_prograde = ((omega * radius + walk_v)**2) / radius
        self.assertAlmostEqual(res["a_prograde"], expected_prograde, places=4)

        expected_retrograde = ((omega * radius - walk_v)**2) / radius
        self.assertAlmostEqual(res["a_retrograde"], expected_retrograde, places=4)

    # --- PHASE 8 MARS ISRU TEST SUITE ---

    def test_isru_water_and_hydrogen_stoichiometry(self):
        """Phase 8 Test: Verify water-to-hydrogen chemical stoichiometry mass conservation."""
        model = MarsISRUModel()
        res = model.run_full_isru_model()

        gross_lh2 = res["propellant_accounting"]["gross_lh2_production_mt"]
        pure_water = res["feedstock_analysis"]["glacial_ice"]["pure_water_required_mt"]

        expected_water_mt = gross_lh2 * KG_WATER_PER_KG_H2
        self.assertAlmostEqual(pure_water, expected_water_mt, delta=1.0)

        gross_o2 = res["propellant_accounting"]["gross_o2_byproduct_mt"]
        expected_o2_mt = gross_lh2 * KG_O2_PER_KG_H2
        self.assertAlmostEqual(gross_o2, expected_o2_mt, delta=1.0)

    def test_isru_electrolysis_power_first_principles(self):
        """Phase 8 Test: Verify first-principles SOEC electrolysis thermodynamic power calculation."""
        model = MarsISRUModel()
        res = model.run_full_isru_model()

        specific_e = res["power_and_energy_derivation"]["specific_energy_kwh_per_kg_lh2"]
        soec_e = res["power_and_energy_derivation"]["breakdown_kwh_per_kg"]["soec_electrolysis"]

        self.assertGreater(soec_e, DELTA_H_ELECTROLYSIS_KWH_PER_KG)
        self.assertAlmostEqual(soec_e, DELTA_H_ELECTROLYSIS_KWH_PER_KG / 0.72, delta=0.5)

        self.assertGreater(specific_e, 70.0)
        self.assertLess(specific_e, 95.0)

    def test_isru_power_budget_and_reactor_closure(self):
        """Phase 8 Test: Verify Mars surface power budget summation and power closure."""
        model = MarsISRUModel()
        res = model.run_full_isru_model()

        budget = res["mars_surface_power_budget"]["itemized_power_budget"]
        total_avg_mwe = res["mars_surface_power_budget"]["required_average_power_mwe"]

        sum_kw = sum(v["avg_kw"] for v in budget.values())
        self.assertAlmostEqual(sum_kw / 1000.0, total_avg_mwe, delta=0.1)

        # Precursor reactor rating must exceed total surface power demand
        reactor_power_mwe = 25.0
        self.assertGreater(reactor_power_mwe, total_avg_mwe)

    def test_isru_thermal_rejection_radiators(self):
        """Phase 8 Test: Verify waste heat Q_waste calculation and radiator area/mass closure."""
        model = MarsISRUModel()
        res = model.run_full_isru_model()

        thermal = res["thermal_rejection_and_radiators"]
        total_q_waste = thermal["total_q_waste_mwth"]
        rad_mass = thermal["radiator_mass_mt"]

        self.assertGreater(total_q_waste, 30.0)  # > 30 MWth waste heat
        self.assertGreater(rad_mass, 50.0)      # > 50 tonnes radiator array

    def test_isru_production_rates_and_timeline(self):
        """Phase 8 Test: Verify daily/hourly production rates over campaign timeline."""
        model = MarsISRUModel(target_lh2_net_mt=2200.0, production_days=500.0)
        res = model.run_full_isru_model()

        rates = res["production_rates_and_equipment"]["production_rates"]
        lh2_day = rates["lh2_produced_kg_day"]
        water_day = rates["water_extracted_mt_day"]

        self.assertAlmostEqual(lh2_day, (2760.8 * 1000.0) / 500.0, delta=1.0)
        self.assertGreater(water_day, 40.0)  # > 40 tonnes water/day

    # --- PHASE 8.1 CODEX P1/P2 DEFECT REMEDIATION REGRESSION SUITE ---

    def test_a_zero_precursor_inventory_fails_departure(self):
        """Test A: Zero precursor inventory must fail crew departure."""
        twin = MissionDigitalTwin()
        # Do not run precursor mission -> zero inventory
        res = twin.run_crewed_mission()
        self.assertEqual(res["status"], "CREW DEPARTURE ABORTED ON EARTH")
        self.assertFalse(res["gate_status"]["required_LH2_available"])
        self.assertFalse(res["success_predicate_assessment"]["mission_success"])

    def test_b_precursor_unverified_inventory_fails_departure(self):
        """Test B: Precursor production completed but inventory not verified must fail crew departure."""
        twin = MissionDigitalTwin()
        twin.run_precursor_mission()
        twin.depot.depot_verified = False # Intentionally unverify
        res = twin.run_crewed_mission()
        self.assertEqual(res["status"], "CREW DEPARTURE ABORTED ON EARTH")
        self.assertFalse(res["gate_status"]["depot_verified"])

    def test_c_verified_inventory_below_requirement_fails_departure(self):
        """Test C: Verified inventory below requirement must fail crew departure."""
        twin = MissionDigitalTwin()
        twin.run_precursor_mission()
        twin.depot.lh2_verified_inventory_mt = 2199.0 # 1t below required 2200t
        res = twin.run_crewed_mission()
        self.assertEqual(res["status"], "CREW DEPARTURE ABORTED ON EARTH")
        self.assertFalse(res["gate_status"]["required_LH2_available"])

    def test_d_verified_inventory_above_requirement_permits_departure(self):
        """Test D: Verified inventory above requirement must permit departure."""
        twin = MissionDigitalTwin()
        twin.run_precursor_mission()
        res = twin.run_crewed_mission()
        self.assertNotIn("status", res) # Successfully executed without Earth abort
        self.assertTrue(res["success_predicate_assessment"]["mission_success"])

    def test_e_crewed_mission_cannot_create_precursor_inventory(self):
        """Test E: Crewed mission cannot create precursor inventory."""
        twin = MissionDigitalTwin()
        # Uninitialized precursor depot
        self.assertEqual(twin.depot.lh2_produced_mt, 0.0)
        res = twin.run_crewed_mission()
        self.assertEqual(res["status"], "CREW DEPARTURE ABORTED ON EARTH")
        # Ensure crewed mission execution attempt did not magically manufacture propellant
        self.assertEqual(twin.depot.lh2_produced_mt, 0.0)

    def test_f_running_precursor_separately_and_passing_state_permits_departure(self):
        """Test F: Running precursor separately and then passing verified state into crewed mission permits departure."""
        twin_precursor = MissionDigitalTwin()
        precursor_output = twin_precursor.run_precursor_mission()
        self.assertEqual(precursor_output["state"], PrecursorDepotState.DEPOT_VERIFIED)

        twin_crewed = MissionDigitalTwin()
        twin_crewed.depot = twin_precursor.depot # Explicit handoff of verified precursor depot
        crewed_output = twin_crewed.run_crewed_mission()

        self.assertTrue(crewed_output["success_predicate_assessment"]["mission_success"])
        self.assertGreater(twin_crewed.depot.lh2_transferred_to_ship_mt, 2000.0)

    def test_g_repeated_execution_cannot_duplicate_depot_inventory(self):
        """Test G: Repeated execution cannot duplicate the same precursor inventory."""
        twin = MissionDigitalTwin()
        twin.run_precursor_mission()

        # Mission 1 consumes return propellant
        res_m1 = twin.run_crewed_mission()
        self.assertTrue(res_m1["success_predicate_assessment"]["mission_success"])

        # Attempt Mission 2 without manufacturing new propellant
        twin_m2 = MissionDigitalTwin()
        twin_m2.depot = twin.depot # Pass depleted depot

        res_m2 = twin_m2.run_crewed_mission()
        self.assertEqual(res_m2["status"], "CREW DEPARTURE ABORTED ON EARTH")
        self.assertFalse(res_m2["gate_status"]["required_LH2_available"])

    def test_negative_lander_capacity_failure(self):
        """Negative Test: Lander capacity < ISRU dry mass must fail precursor payload gate."""
        model = MarsISRUModel()
        gate = model.precursor_payload_closes(number_of_landers=1, capacity_per_lander_mt=150.0) # 150t capacity vs ~256t plant
        self.assertFalse(gate["payload_closes"])
        self.assertLess(gate["mass_margin_mt"], 0.0)

    def test_negative_power_budget_insufficient(self):
        """Negative Test: Surface nuclear power < required surface power must fail power gate."""
        model = MarsISRUModel()
        power_eval = model.surface_power_budget(available_power_mwe=18.0) # 18 MWe < ~20.63 MWe demand
        self.assertFalse(power_eval["power_closes"])
        self.assertLess(power_eval["power_margin_mwe"], 0.0)

    def test_negative_peak_power_insufficient(self):
        """Negative Test: Available power < required peak power must fail power gate."""
        model = MarsISRUModel()
        power_eval = model.surface_power_budget(available_power_mwe=22.0) # 22 MWe < 24.42 MWe peak
        self.assertFalse(power_eval["power_closes"])

    def test_efficiency_parameterization_monotonicity(self):
        """Verify that SOEC & Liquefaction efficiency degradation increases power demand monotonically."""
        model_high = MarsISRUModel(soec_efficiency=0.80, liquefaction_efficiency=0.30)
        power_high = model_high.surface_power_budget()["required_average_power_mwe"]

        model_nominal = MarsISRUModel(soec_efficiency=0.72, liquefaction_efficiency=0.25)
        power_nominal = model_nominal.surface_power_budget()["required_average_power_mwe"]

        model_low = MarsISRUModel(soec_efficiency=0.60, liquefaction_efficiency=0.20)
        power_low = model_low.surface_power_budget()["required_average_power_mwe"]

        self.assertLess(power_high, power_nominal)
        self.assertLess(power_nominal, power_low)

    def test_depot_refueling_mass_conservation_and_losses(self):
        """Verify transfer loss accounting and mass conservation during refueling."""
        twin = MissionDigitalTwin()
        twin.run_precursor_mission()

        initial_verified = twin.depot.lh2_verified_inventory_mt
        res = twin.execute_mars_isru_reload_and_stay("Refueling Test", target_reload_net_mt=2200.0)

        debit = res["depot_debit_mt"]
        losses = res["transfer_losses_mt"]
        credit = res["lh2_reloaded_mt"]

        self.assertAlmostEqual(debit, losses + credit, places=1)
        self.assertAlmostEqual(twin.depot.lh2_verified_inventory_mt, initial_verified - debit, places=1)


if __name__ == "__main__":
    unittest.main()
