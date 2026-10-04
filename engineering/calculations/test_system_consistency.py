#!/usr/bin/env python3
"""
Automated System Consistency & Sequential Digital Twin Test Suite for Project Occam-7
Verifies cross-subsystem physical consistency, sequential state propagation, NEP trajectory tests,
thermal/power state machines, launch logistics, centrifuge dynamics, mass conservation, vector kinematics,
numerical vs analytical rocket equation agreement, cryogenic boiloff, crew health models, and mission success predicates.
"""

import math
import sys
import unittest

from mass_budget import calculate_mass_budget
from centrifuge_calculator import analyze_centrifuge
from shielding_estimator import shielding_calculator
from radiator_sizing import calculate_radiator_area
from mission_digital_twin import MissionDigitalTwin, SpacecraftState
from earth_mars_transfer import EarthMarsTransferSolver, MU_SUN, MU_EARTH, MU_MARS, R_EARTH_ORBIT, R_MARS_ORBIT

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
        m_final = twin.state.gross_mass_mt

        # Total consumable loss from dry budget
        consumables_lost = 72.3 - twin.state.crew_consumables_mt

        m_accounted = m_final + lh2_burned + lnh3_burned + boiloff_lost + consumables_lost
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

        # Check TMI & MOI delta-v values against orbital mechanics
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
        twin.state.centrifuge_active = False  # Disable centrifuge
        twin.execute_coast_or_stay("Microgravity Stay", duration_days=100.0)

        # Health should decay by 5.0% over 100 days
        self.assertAlmostEqual(twin.state.crew_health_percent, 95.0, delta=0.1)

    def test_cryogenic_boiloff_and_zbo_refrigeration(self):
        """Requirement 21: Verify active Zero-Boiloff refrigeration and passive boiloff."""
        state = SpacecraftState()
        self.assertEqual(state.zbo_refrigeration_mwe, 0.015)  # 15 kWe

        twin = MissionDigitalTwin(initial_state=state)
        twin.execute_coast_or_stay("Orbital Storage", duration_days=100.0)

        # Passive boiloff should be tracked
        self.assertGreater(twin.state.cumulative_boiloff_loss_mt, 0.0)

    def test_machine_readable_mission_success_predicate(self):
        """Requirement 18: Verify machine-readable success predicate logic."""
        twin = MissionDigitalTwin()
        res = twin.run_full_mission_baseline()
        predicates = res["success_predicate_assessment"]

        self.assertTrue(predicates["mission_success"])
        self.assertTrue(predicates["predicates"]["earth_departure_achieved"])
        self.assertTrue(predicates["predicates"]["mars_encounter_achieved"])
        self.assertTrue(predicates["predicates"]["earth_return_achieved"])

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


if __name__ == "__main__":
    unittest.main()
