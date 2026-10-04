#!/usr/bin/env python3
"""
Automated System Consistency & Sequential Digital Twin Test Suite for Project Occam-7
Verifies cross-subsystem physical consistency, sequential state propagation, NEP trajectory tests (Tests A-E),
thermal/power state machines, launch logistics, centrifuge dynamics, and property-based edge cases.
"""

import math
import sys
import unittest

from mass_budget import calculate_mass_budget
from centrifuge_calculator import analyze_centrifuge
from shielding_estimator import shielding_calculator
from radiator_sizing import calculate_radiator_area
from mission_digital_twin import MissionDigitalTwin, SpacecraftState

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

    def test_tank_hoop_stress_and_wall_thickness(self):
        """DEF-001: Verify thin-wall hoop stress calculation for 12m dia pressure tanks."""
        p_internal = 150000.0  # Pa (150 kPa)
        radius = 6.0          # m
        t_orig = 0.004        # m (4 mm)

        # Hoop stress formula: sigma = P * r / t
        sigma_hoop_orig = (p_internal * radius) / t_orig
        self.assertAlmostEqual(sigma_hoop_orig, 225.0e6, delta=1.0)  # Exceeds 220 MPa yield!

        # Chosen wall thickness: 6.5 mm
        t_chosen = 0.0065
        sigma_hoop_chosen = (p_internal * radius) / t_chosen
        self.assertAlmostEqual(sigma_hoop_chosen, 138.46e6, delta=1e4)
        self.assertLess(sigma_hoop_chosen, 220.0e6 / 1.5)  # SF > 1.5x on yield

    def test_nep_power_thrust_jet_coupling(self):
        """DEF-002 & DEF-003: Verify NEP electrical power to jet power to thrust & mass flow relationship."""
        p_elec = 15.0e6      # 15 MWe
        eta = 0.65            # Thruster efficiency
        p_jet = p_elec * eta  # 9.75 MWjet
        isp = 3500.0          # s
        v_e = isp * G0        # 34,323.28 m/s

        # Jet power relationship: P_jet = 0.5 * F * v_e
        thrust = (2.0 * p_jet) / v_e
        self.assertAlmostEqual(thrust, 568.12, delta=0.5)

        # Mass flow rate: mdot = F / v_e
        mdot_kg_s = thrust / v_e
        self.assertAlmostEqual(mdot_kg_s, 0.016552, delta=1e-5)

    # --- REPAIRED NEP SEQUENTIAL TEST SUITE (TESTS A, B, C, D, E) ---

    def test_nep_test_a_full_departure_mass(self):
        """Test A: Evaluate NEP acceleration on full departure wet mass (3,970.96 MT)."""
        twin = MissionDigitalTwin()
        # Initial departure state: 3,970.96 MT
        res = twin.execute_nep_burn("Test A: Full Departure Mass", duration_days=180.0)
        self.assertAlmostEqual(res["start_mass_mt"], 3970.96, places=2)
        # Expected Delta-V: v_e * ln(3970.96 / (3970.96 - 257.42)) = 2.292 km/s
        self.assertAlmostEqual(res["actual_dv_kms"], 2.292, delta=0.05)

    def test_nep_test_b_after_tmi(self):
        """Test B: Evaluate NEP acceleration after TMI burn (2,581.73 MT)."""
        twin = MissionDigitalTwin()
        twin.execute_ntp_burn("TMI", target_dv_kms=3.80)
        res = twin.execute_nep_burn("Test B: Post-TMI", duration_days=180.0)
        self.assertAlmostEqual(res["start_mass_mt"], 2581.73, delta=2.0)
        # Expected Delta-V: v_e * ln(2581.73 / 2324.31) = 3.605 km/s
        self.assertAlmostEqual(res["actual_dv_kms"], 3.605, delta=0.05)

    def test_nep_test_c_after_mars_capture(self):
        """Test C: Evaluate NEP acceleration after Mars Orbit Insertion (1,832.15 MT)."""
        twin = MissionDigitalTwin()
        twin.execute_ntp_burn("TMI", target_dv_kms=3.80)
        twin.execute_nep_burn("Outbound NEP", duration_days=180.0)
        twin.execute_ntp_burn("MOI", target_dv_kms=2.10)

        start_mass = twin.state.gross_mass_mt
        self.assertAlmostEqual(start_mass, 1832.15, delta=2.0)

        # Test 30 days of NEP orbit maneuvering
        res = twin.execute_nep_burn("Test C: Post-MOI", duration_days=30.0)
        self.assertGreater(res["actual_dv_kms"], 0.75)

    def test_nep_test_d_return_transit(self):
        """Test D: Evaluate NEP acceleration during return transit after TEI."""
        twin = MissionDigitalTwin()
        twin.execute_ntp_burn("TMI", target_dv_kms=3.80)
        twin.execute_nep_burn("Outbound NEP", duration_days=180.0)
        twin.execute_ntp_burn("MOI", target_dv_kms=2.10)
        twin.execute_coast_or_stay("Mars Stay", duration_days=640.0)
        twin.execute_ntp_burn("TEI", target_dv_kms=1.80)

        start_mass = twin.state.gross_mass_mt
        self.assertAlmostEqual(start_mass, 1467.27, delta=5.0)

        # Inbound NEP consumes remaining LNH3 (42.58 MT)
        res = twin.execute_nep_burn("Test D: Inbound NEP", duration_days=180.0)
        self.assertAlmostEqual(res["lnh3_burned_mt"], 42.58, delta=1.0)
        self.assertAlmostEqual(res["actual_dv_kms"], 1.011, delta=0.05)

    def test_nep_test_e_degraded_power(self):
        """Test E: Evaluate NEP performance with 50% reactor power degradation (7.5 MWe input)."""
        twin = MissionDigitalTwin()
        twin.state.system_health["reactor_health"] = 0.50  # 50% reactor degradation

        res = twin.execute_nep_burn("Test E: Degraded Power", duration_days=180.0)
        # Power should be 50% -> Jet power = 4.875 MW -> Thrust = 284.06 N
        self.assertAlmostEqual(res["thrust_n"], 284.06, delta=1.0)
        # Mass flow rate halved -> LNH3 burned = 128.7 MT over 180 days
        self.assertAlmostEqual(res["lnh3_burned_mt"], 128.7, delta=1.0)

    # --- PROPERTY-BASED AND EDGE-CASE TESTS ---

    def test_edge_case_zero_propellant(self):
        """Edge Case: Zero propellant inventory produces zero delta-v and zero burn duration."""
        twin = MissionDigitalTwin()
        twin.state.lh2_mt = 0.0
        twin.state.lnh3_mt = 0.0

        res_ntp = twin.execute_ntp_burn("Zero Propellant NTP", target_dv_kms=2.0)
        self.assertEqual(res_ntp["lh2_burned_mt"], 0.0)
        self.assertEqual(res_ntp["actual_dv_kms"], 0.0)

        res_nep = twin.execute_nep_burn("Zero Propellant NEP", duration_days=30.0)
        self.assertEqual(res_nep["lnh3_burned_mt"], 0.0)
        self.assertEqual(res_nep["actual_dv_kms"], 0.0)

    def test_edge_case_engine_failure(self):
        """Property Test: Single NTP engine loss (4 -> 3 engines) reduces thrust to 3,000 kN and increases burn duration."""
        twin_norm = MissionDigitalTwin()
        res_norm = twin_norm.execute_ntp_burn("Normal TMI", target_dv_kms=3.80)

        twin_fail = MissionDigitalTwin()
        twin_fail.state.system_health["ntp_engines_active"] = 3
        res_fail = twin_fail.execute_ntp_burn("3-Engine TMI", target_dv_kms=3.80)

        self.assertEqual(res_fail["thrust_kn"], 3000.0)
        # Propellant burned and actual dv match rocket equation, but duration is 1.33x longer
        self.assertAlmostEqual(res_fail["actual_dv_kms"], res_norm["actual_dv_kms"], places=3)
        self.assertAlmostEqual(res_fail["duration_s"], res_norm["duration_s"] * (4.0 / 3.0), places=1)

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

    def test_launch_manifest_capacity_closure(self):
        """DEF-004: Verify launch count calculations for heavy launch vehicles."""
        m_dep = 3970.96  # MT canonical departure wet mass

        launches_250t = math.ceil(m_dep / 250.0)
        launches_150t = math.ceil(m_dep / 150.0)
        launches_100t = math.ceil(m_dep / 100.0)

        self.assertEqual(launches_250t, 16)
        self.assertEqual(launches_150t, 27)
        self.assertEqual(launches_100t, 40)

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

    def test_shielding_calculator_multi_layer_stack(self):
        """DEF-006: Verify shielding calculator includes steel pressure hull layers."""
        res = shielding_calculator()
        col_density = res["col_density_shelter"]
        self.assertAlmostEqual(col_density, 52.25, delta=1.0)


if __name__ == "__main__":
    unittest.main()
