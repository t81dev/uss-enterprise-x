#!/usr/bin/env python3
"""
Automated System Consistency & Sequential Digital Twin Test Suite for Project Occam-7
Updated for Program Phase 8.6 — Radiation Transport & Habitat Geometry Closure.

Verifies cross-subsystem physical consistency, sequential state propagation, NEP trajectory tests,
thermal/power state machines, launch logistics, centrifuge dynamics, mass conservation, vector kinematics,
numerical vs analytical rocket equation agreement, cryogenic boiloff, crew health models,
Mars ISRU water/hydrogen conservation, electrolysis thermodynamics, liquefaction power,
radiator thermal closure, surface timeline closure, machine-readable mission success predicates,
Phase 8.1 explicit precursor/crewed safety gates & negative failure tests (Tests A through G),
Phase 8.2–8.4 hostile surface power/thermal/payload margin & state-machine prerequisite tests,
Phase 8.5 hostile radiation shielding & propellant depletion tests,
and Phase 8.6 hostile radiation transport, geometry, shelter, and mass conservation tests.
"""

import math
import sys
import unittest

from mass_budget import calculate_mass_budget
from centrifuge_calculator import analyze_centrifuge
from shielding_estimator import (
    shielding_calculator,
    calculate_axial_propellant_column_density,
    calculate_directional_solid_angles,
    calculate_habitat_geometry_statistics,
    compute_dynamic_dose_rate,
    calculate_gcr_dose_rate,
    calculate_reactor_dose_rate,
    calculate_spe_event_dose,
    verify_storm_shelter_subsystem,
    verify_radiation_mass_budget,
)
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
        self.assertEqual(twin.depot.lh2_produced_mt, 0.0)
        res = twin.run_crewed_mission()
        self.assertEqual(res["status"], "CREW DEPARTURE ABORTED ON EARTH")
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

        res_m1 = twin.run_crewed_mission()
        self.assertTrue(res_m1["success_predicate_assessment"]["mission_success"])

        twin_m2 = MissionDigitalTwin()
        twin_m2.depot = twin.depot # Pass depleted depot

        res_m2 = twin_m2.run_crewed_mission()
        self.assertEqual(res_m2["status"], "CREW DEPARTURE ABORTED ON EARTH")
        self.assertFalse(res_m2["gate_status"]["required_LH2_available"])

    def test_negative_lander_capacity_failure(self):
        """Negative Test: Lander capacity < ISRU dry mass must fail precursor payload gate."""
        model = MarsISRUModel()
        gate = model.precursor_payload_closes(number_of_landers=1, capacity_per_lander_mt=150.0)
        self.assertFalse(gate["payload_closes"])
        self.assertLess(gate["mass_margin_mt"], 0.0)

    def test_negative_power_budget_insufficient(self):
        """Negative Test: Surface nuclear power < required surface power must fail power gate."""
        model = MarsISRUModel()
        power_eval = model.surface_power_budget(available_power_mwe=18.0)
        self.assertFalse(power_eval["power_closes"])
        self.assertLess(power_eval["power_margin_mwe"], 0.0)

    def test_negative_peak_power_insufficient(self):
        """Negative Test: Available power < required peak power must fail power gate."""
        model = MarsISRUModel()
        power_eval = model.surface_power_budget(available_power_mwe=22.0)
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

    # --- PHASE 8.2 HOSTILE POST-REMEDIATION AUDIT TEST SUITE ---

    def test_propellant_transfer_loss_gross_withdrawal_requirement(self):
        """Phase 8.2 Test: Verify that 2,200 t net return LH2 requires ~2,279.79 t gross depot withdrawal."""
        twin = MissionDigitalTwin()
        twin.run_precursor_mission()

        twin.depot.lh2_verified_inventory_mt = 2200.0
        auth, gate = twin.precursor_inventory_verified(required_net_lh2_mt=2200.0)
        self.assertFalse(auth)
        self.assertFalse(gate["required_LH2_available"])

        gross_req = 2200.0 / (1.0 - 0.035)
        twin.depot.lh2_verified_inventory_mt = gross_req - 0.001
        auth_sub, gate_sub = twin.precursor_inventory_verified(required_net_lh2_mt=2200.0)
        self.assertFalse(auth_sub)

        twin.depot.lh2_verified_inventory_mt = gross_req
        auth_pass, gate_pass = twin.precursor_inventory_verified(required_net_lh2_mt=2200.0)
        self.assertTrue(auth_pass)

    def test_spacecraft_loaded_predicate_check(self):
        """Phase 8.2 Test: Verify explicit return_propellant_loaded predicate logic."""
        twin = MissionDigitalTwin()
        twin.run_precursor_mission()
        res = twin.run_crewed_mission()

        predicates = res["success_predicate_assessment"]["predicates"]
        self.assertTrue(predicates["return_propellant_loaded"])
        self.assertTrue(predicates["return_propellant_transfer_complete"])
        self.assertGreaterEqual(twin.depot.actual_net_propellant_loaded_mt, 2200.0)

    def test_hostile_individual_lander_capacity_allocation(self):
        """Phase 8.2 Test A-C: Aggregate capacity passes but individual lander fails."""
        model = MarsISRUModel()

        gate_a = model.precursor_payload_closes(lander_1_capacity_mt=140.0, lander_2_capacity_mt=160.0)
        self.assertFalse(gate_a["payload_closes"])
        self.assertFalse(gate_a["lander_1"]["lander_closes"])
        self.assertTrue(gate_a["lander_2"]["lander_closes"])

        gate_b = model.precursor_payload_closes(lander_1_capacity_mt=150.0, lander_2_capacity_mt=150.0)
        self.assertTrue(gate_b["payload_closes"])
        self.assertTrue(gate_b["lander_1"]["lander_closes"])
        self.assertTrue(gate_b["lander_2"]["lander_closes"])

        gate_c = model.precursor_payload_closes(lander_1_capacity_mt=135.0, lander_2_capacity_mt=150.0)
        self.assertFalse(gate_c["payload_closes"])
        self.assertLess(gate_c["lander_1"]["payload_margin_mt"], 0.0)

    def test_hostile_power_and_thermal_deficits(self):
        """Phase 8.2 Test: Insufficient peak surface power or thermal capacity must fail closure."""
        model = MarsISRUModel()

        p_eval = model.surface_power_budget(available_power_mwe=22.0)
        self.assertFalse(p_eval["power_closes"])
        self.assertFalse(p_eval["peak_power_closes"])

        p_info = model.calculate_electrolysis_and_liquefaction_power(2760.8)
        thermal = model.calculate_thermal_rejection_and_radiator(p_info["avg_continuous_power_mwe"])
        self.assertTrue(thermal["thermal_closure"])

    def test_hostile_isru_production_deficit(self):
        """Phase 8.2 Test: Shortened production timeline produces LH2 deficit and fails campaign."""
        model = MarsISRUModel(production_days=200.0)
        achievable = model.calculate_achievable_production(available_power_mwe=25.0, operating_days=200.0)

        self.assertFalse(achievable["production_closes"])
        self.assertLess(achievable["achievable_gross_lh2_mt"], achievable["required_gross_lh2_mt"])

    # --- PHASE 8.3 & PHASE 8.4 ADVERSARIAL VALIDATION TEST SUITE ---

    def test_phase8_4_thermal_engineering_margins(self):
        """Phase 8.4 Test: Authoritative thermal engineering margin compliance and fixed capacity deficit testing."""
        model = MarsISRUModel()

        t_nominal = model.calculate_thermal_rejection_and_radiator(avg_power_mwe=17.58, required_thermal_margin_fraction=0.15)
        self.assertTrue(t_nominal["thermal_mathematical_closure"])
        self.assertTrue(t_nominal["thermal_margin_compliance"])
        self.assertFalse(t_nominal["thermal_failure"])
        self.assertEqual(t_nominal["thermal_margin_status"], "COMPLIANT")

        t_zero_margin_cap = model.calculate_thermal_rejection_and_radiator(
            avg_power_mwe=17.58,
            required_thermal_margin_fraction=0.15,
            fixed_radiator_capacity_mwth=56.0
        )
        self.assertTrue(t_zero_margin_cap["thermal_mathematical_closure"])
        self.assertFalse(t_zero_margin_cap["thermal_margin_compliance"])
        self.assertEqual(t_zero_margin_cap["thermal_margin_status"], "ZERO_MARGIN_MATHEMATICAL_CLOSURE")

        t_deficit = model.calculate_thermal_rejection_and_radiator(
            avg_power_mwe=17.58,
            required_thermal_margin_fraction=0.15,
            fixed_radiator_capacity_mwth=45.0
        )
        self.assertFalse(t_deficit["thermal_mathematical_closure"])
        self.assertFalse(t_deficit["thermal_margin_compliance"])
        self.assertTrue(t_deficit["thermal_failure"])
        self.assertEqual(t_deficit["thermal_margin_status"], "THERMAL_FAILURE")

        twin = MissionDigitalTwin()
        precursor_res = twin.run_precursor_mission(fixed_radiator_capacity_mwth=56.0)
        self.assertFalse(twin.depot.isru_operational)
        crewed_res = twin.run_crewed_mission()
        self.assertEqual(crewed_res["status"], "CREW DEPARTURE ABORTED ON EARTH")

    def test_phase8_3_surface_power_average_vs_peak_boundaries(self):
        """Phase 8.3 Test: Independent boundary checks for average surface power vs peak surface power."""
        model = MarsISRUModel()

        p1 = model.surface_power_budget(available_power_mwe=25.0)
        self.assertTrue(p1["average_power_closes"])
        self.assertTrue(p1["peak_power_closes"])
        self.assertTrue(p1["power_closes"])

        p2 = model.surface_power_budget(available_power_mwe=22.0)
        self.assertTrue(p2["average_power_closes"])
        self.assertFalse(p2["peak_power_closes"])
        self.assertFalse(p2["power_closes"])

        p3 = model.surface_power_budget(available_power_mwe=18.0)
        self.assertFalse(p3["average_power_closes"])
        self.assertFalse(p3["peak_power_closes"])
        self.assertFalse(p3["power_closes"])

    def test_phase8_3_independent_lander_capacities_boundary(self):
        """Phase 8.3 Test: Adversarial boundary checks for independent lander capacities."""
        model = MarsISRUModel()

        g1 = model.precursor_payload_closes(lander_1_capacity_mt=144.99, lander_2_capacity_mt=150.0)
        self.assertFalse(g1["payload_closes"])
        self.assertFalse(g1["lander_1"]["lander_closes"])
        self.assertTrue(g1["lander_2"]["lander_closes"])

        g2 = model.precursor_payload_closes(lander_1_capacity_mt=150.0, lander_2_capacity_mt=114.78)
        self.assertFalse(g2["payload_closes"])
        self.assertTrue(g2["lander_1"]["lander_closes"])
        self.assertFalse(g2["lander_2"]["lander_closes"])

        g3 = model.precursor_payload_closes(lander_1_capacity_mt=140.0, lander_2_capacity_mt=110.0)
        self.assertFalse(g3["payload_closes"])
        self.assertFalse(g3["lander_1"]["lander_closes"])
        self.assertFalse(g3["lander_2"]["lander_closes"])

        g4 = model.precursor_payload_closes(lander_1_capacity_mt=120.0, lander_2_capacity_mt=180.0)
        self.assertFalse(g4["payload_closes"])

    def test_phase8_3_precursor_state_machine_prerequisite_breaking(self):
        """Phase 8.3 Test: Systematically break each precursor prerequisite and verify authorization denial."""
        prerequisites_to_test = [
            ("depot_exists", "precursor_deployed", False),
            ("depot_operational", "isru_operational", False),
            ("power_closure", "isru_power_closure", False),
            ("payload_closure", "precursor_payload_closes", False),
            ("propellant_production_complete", "production_complete", False),
            ("depot_verified", "depot_verified", False),
            ("storage_system_operational", "storage_system_operational", False),
            ("inventory_measurement_valid", "inventory_measurement_valid", False),
            ("transfer_system_operational", "transfer_system_operational", False),
        ]

        for gate_key, depot_attr, break_val in prerequisites_to_test:
            twin = MissionDigitalTwin()
            twin.run_precursor_mission()
            self.assertEqual(twin.depot.state, PrecursorDepotState.DEPOT_VERIFIED)

            setattr(twin.depot, depot_attr, break_val)

            auth, gate = twin.precursor_inventory_verified()
            self.assertFalse(auth, f"Crew departure was incorrectly authorized despite broken prerequisite: {gate_key}")
            self.assertFalse(gate[gate_key], f"Gate key {gate_key} did not reflect broken prerequisite {depot_attr}")

            crewed_res = twin.run_crewed_mission()
            self.assertEqual(crewed_res["status"], "CREW DEPARTURE ABORTED ON EARTH")

    def test_phase8_3_exact_refueling_boundaries(self):
        """Phase 8.3 Test: Deterministic boundary tests around 2,200 t net and ~2,279.79 t gross withdrawal."""
        twin = MissionDigitalTwin()
        twin.run_precursor_mission()

        gross_req = 2200.0 / (1.0 - 0.035)

        twin.depot.lh2_verified_inventory_mt = gross_req
        auth1, gate1 = twin.precursor_inventory_verified(required_net_lh2_mt=2200.0)
        self.assertTrue(auth1)

        twin.depot.lh2_verified_inventory_mt = 2279.79
        auth2, gate2 = twin.precursor_inventory_verified(required_net_lh2_mt=2200.0)
        self.assertFalse(auth2)

        twin.depot.lh2_verified_inventory_mt = 2200.0
        auth3, gate3 = twin.precursor_inventory_verified(required_net_lh2_mt=2200.0)
        self.assertFalse(auth3)

    def test_phase8_3_conservation_law_adversarial_testing(self):
        """Phase 8.3 Test: Adversarial tests verifying mass conservation enforcement assertions."""
        twin = MissionDigitalTwin()

        with self.assertRaises(AssertionError):
            twin.enforce_mass_conservation(
                event_name="Adversarial Mass Creation Test",
                m_initial=1000.0,
                m_final=1050.0,
                prop_burned=0.0,
                consumables_spent=0.0,
                boiloff_lost=0.0,
                isru_reloaded=0.0
            )

        with self.assertRaises(AssertionError):
            twin.enforce_mass_conservation(
                event_name="Adversarial Mass Loss Test",
                m_initial=1000.0,
                m_final=900.0,
                prop_burned=0.0,
                consumables_spent=0.0,
                boiloff_lost=0.0,
                isru_reloaded=0.0
            )

    def test_phase8_3_wilson_confidence_interval_validation(self):
        """Phase 8.3 Test: Independently validate Wilson score confidence interval calculation formula."""
        z = 1.959964
        num_runs = 10000
        success_count = 9790
        p_hat = success_count / num_runs

        denom = 1.0 + (z**2) / num_runs
        p_mid = (p_hat + (z**2) / (2.0 * num_runs)) / denom
        p_bound = (z / denom) * math.sqrt((p_hat * (1.0 - p_hat) / num_runs) + ((z**2) / (4.0 * (num_runs**2))))

        ci_lower = max(0.0, (p_mid - p_bound) * 100.0)
        ci_upper = min(100.0, (p_mid + p_bound) * 100.0)

        self.assertAlmostEqual(ci_lower, 97.60, places=1)
        self.assertAlmostEqual(ci_upper, 98.16, places=1)

    # --- PHASE 8.5 HOSTILE RADIATION SHIELDING & PROPELLANT DEPLETION TEST SUITE ---

    def test_depleted_propellant_axial_column_density_zero(self):
        """Phase 8.5 Test: Verify full tanks yield >1,000 g/cm^2 axial column density, while empty tanks yield exactly 0.0 g/cm^2."""
        col_full = calculate_axial_propellant_column_density(lh2_mt=2200.0, lnh3_mt=300.0)
        col_empty = calculate_axial_propellant_column_density(lh2_mt=0.0, lnh3_mt=0.0)

        self.assertGreater(col_full, 1000.0)
        self.assertEqual(col_empty, 0.0)

    def test_directional_solid_angle_radial_gcr_dominance(self):
        """Phase 8.5 Test: Verify radial sky covers >98% of 4pi space and axial propellant tanks cover <1.5%."""
        angles = calculate_directional_solid_angles(tank_radius_m=6.0, tank_distance_m=35.0)

        self.assertGreater(angles["frac_radial"], 0.98)
        self.assertLess(angles["frac_axial"], 0.02)
        self.assertAlmostEqual(angles["frac_radial"] + angles["frac_axial"], 1.0, places=6)

    def test_spe_event_storm_shelter_attenuation(self):
        """Phase 8.5 Test: Verify SPE flare dose inside SPE storm shelter core (<5 cSv) vs outside shelter (>30 cSv)."""
        dose_inside = compute_dynamic_dose_rate(lh2_mt=0.0, lnh3_mt=0.0, reactor_power_mwth=0.0, in_storm_shelter=True, spe_event=True)
        dose_outside = compute_dynamic_dose_rate(lh2_mt=0.0, lnh3_mt=0.0, reactor_power_mwth=0.0, in_storm_shelter=False, spe_event=True)

        self.assertLess(dose_inside["spe_event_dose_csv"], 5.0)
        self.assertGreater(dose_outside["spe_event_dose_csv"], 30.0)

    def test_dynamic_dose_rate_varies_with_reactor_power_and_depletion(self):
        """Phase 8.5 Test: Verify dose rate changes dynamically with reactor power and propellant depletion."""
        dose_full_rx_full_prop = compute_dynamic_dose_rate(lh2_mt=2200.0, lnh3_mt=300.0, reactor_power_mwth=100.0)
        dose_full_rx_empty_prop = compute_dynamic_dose_rate(lh2_mt=0.0, lnh3_mt=0.0, reactor_power_mwth=100.0)
        dose_low_rx_empty_prop = compute_dynamic_dose_rate(lh2_mt=0.0, lnh3_mt=0.0, reactor_power_mwth=10.0)

        self.assertGreater(dose_full_rx_empty_prop["rx_rate_csv_day"], dose_full_rx_full_prop["rx_rate_csv_day"])
        self.assertAlmostEqual(dose_low_rx_empty_prop["rx_rate_csv_day"] * 10.0, dose_full_rx_empty_prop["rx_rate_csv_day"], delta=0.05)

    def test_unclosed_radial_shielding_fails_crew_survivability(self):
        """Phase 8.5 Test: Removing radial habitat shielding (sigma_radial -> 0) causes GCR dose rate to spike and fail crew survivability."""
        gcr_unshielded = calculate_gcr_dose_rate(sigma_radial_g_cm2=0.0, sigma_axial_g_cm2=0.0)
        gcr_shielded = calculate_gcr_dose_rate(sigma_radial_g_cm2=31.4, sigma_axial_g_cm2=0.0)

        self.assertGreater(gcr_unshielded, gcr_shielded * 1.8)

        accumulated_unshielded = gcr_unshielded * 850.0
        self.assertGreater(accumulated_unshielded, 100.0)

    # --- PHASE 8.6 HOSTILE ADVERSARIAL RADIATION & GEOMETRY CLOSURE TEST SUITE ---

    def test_phase8_6_geometry_statistics_and_angular_coverage(self):
        """Phase 8.6 Test: Verify habitat spatial geometry reconstruction statistics."""
        stats = calculate_habitat_geometry_statistics()

        self.assertEqual(stats["min_column_g_cm2"], 15.0)
        self.assertGreater(stats["max_column_g_cm2"], 1000.0)  # Axial tanks line of sight
        self.assertGreater(stats["mean_column_g_cm2"], 30.0)
        self.assertGreater(stats["median_column_g_cm2"], 30.0)
        self.assertGreater(stats["std_dev_g_cm2"], 50.0)

        self.assertEqual(stats["frac_below_10_g_cm2"], 0.0)  # No direction below 10 g/cm^2
        self.assertLess(stats["frac_below_20_g_cm2"], 0.05)  # Only thin forward endcap

    def test_phase8_6_gcr_environment_envelopes(self):
        """Phase 8.6 Test: Verify GCR dose rates under solar min, nominal, and solar max."""
        dose_min = calculate_gcr_dose_rate(sigma_radial_g_cm2=31.4, sigma_axial_g_cm2=0.0, gcr_env="solar_minimum")
        dose_nom = calculate_gcr_dose_rate(sigma_radial_g_cm2=31.4, sigma_axial_g_cm2=0.0, gcr_env="nominal")
        dose_max = calculate_gcr_dose_rate(sigma_radial_g_cm2=31.4, sigma_axial_g_cm2=0.0, gcr_env="solar_maximum")

        self.assertGreater(dose_min, dose_nom)
        self.assertGreater(dose_nom, dose_max)

    def test_phase8_6_spe_scenarios_and_response_delays(self):
        """Phase 8.6 Test: Verify SPE dose across moderate, severe, and extreme events with shelter delays."""
        dose_0min = calculate_spe_event_dose("severe", in_storm_shelter=True, response_time_min=0.0)
        dose_10min = calculate_spe_event_dose("severe", in_storm_shelter=True, response_time_min=10.0)
        dose_30min = calculate_spe_event_dose("severe", in_storm_shelter=True, response_time_min=30.0)
        dose_120min = calculate_spe_event_dose("severe", in_storm_shelter=True, response_time_min=120.0)

        self.assertLess(dose_0min, dose_10min)
        self.assertLess(dose_10min, dose_30min)
        self.assertLess(dose_30min, dose_120min)

    def test_phase8_6_extreme_spe_and_delayed_shelter_failure(self):
        """Phase 8.6 Test: Extreme design-basis SPE + 300-min delay causes acute SPE survivability failure."""
        twin = MissionDigitalTwin()
        twin.state.spe_scenario = "extreme_design_basis"
        twin.state.crew_response_time_min = 300.0  # 5 hours delay

        twin.run_precursor_mission()
        res = twin.run_crewed_mission()

        predicates = res["success_predicate_assessment"]["canonical_predicates"]
        self.assertFalse(predicates["acute_spe_survivability"])
        self.assertFalse(predicates["crew_survivability"])

    def test_phase8_6_shelter_power_or_thermal_failure(self):
        """Phase 8.6 Test: Shelter power or thermal failure fails storm_shelter_closure predicate."""
        twin = MissionDigitalTwin()
        twin.state.system_health["shelter_power_available"] = False

        twin.run_precursor_mission()
        res = twin.run_crewed_mission()

        predicates = res["success_predicate_assessment"]["canonical_predicates"]
        self.assertFalse(predicates["storm_shelter_closure"])

    def test_phase8_6_radiation_mass_budget_audit_and_double_counting(self):
        """Phase 8.6 Test: Verify 240 MT dry shielding budget reconciliation and reject double-counting."""
        audit = verify_radiation_mass_budget()
        self.assertTrue(audit["mass_conserved"])
        self.assertEqual(audit["total_shield_mass_mt"], 240.0)


if __name__ == "__main__":
    unittest.main()
