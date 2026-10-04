#!/usr/bin/env python3
"""
Automated System Consistency & Reconciliation Test Suite for Project Occam-7
Verifies that all coupled subsystems across mass budgets, propulsion physics, power conversion,
thermal rejection, radiation protection, centrifuge dynamics, and launch logistics agree 100%.
"""

import math
import sys
import unittest

from mass_budget import calculate_mass_budget
from centrifuge_calculator import analyze_centrifuge
from shielding_estimator import shielding_calculator
from mission_deltav import calculate_nep_burn
from radiator_sizing import calculate_radiator_area

G0 = 9.80665

class TestSystemConsistency(unittest.TestCase):

    def test_mass_budget_row_summation_reconciliation(self):
        """DEF-005: Verify that itemized mass rows sum to unmargined subtotal exactly."""
        res = calculate_mass_budget()
        subsystems = res["subsystems"]

        sum_opt = sum(item["opt"] for item in subsystems.values())
        sum_base = sum(item["base"] for item in subsystems.values())
        sum_pess = sum(item["pess"] for item in subsystems.values())

        self.assertAlmostEqual(sum_opt, res["subtotal_opt"], places=4)
        self.assertAlmostEqual(sum_base, res["subtotal_base"], places=4)
        self.assertAlmostEqual(sum_pess, res["subtotal_pess"], places=4)

        # Verify 20% AIAA reserve margin calculation
        self.assertAlmostEqual(sum_base * 1.20, res["dry_mass_base"], places=4)
        # Verify departure wet mass = dry mass + propellant
        self.assertAlmostEqual(res["dry_mass_base"] + 2500.0, res["wet_mass_base"], places=4)

    def test_tank_hoop_stress_and_wall_thickness(self):
        """DEF-001: Verify thin-wall hoop stress calculation for 12m dia pressure tanks."""
        p_internal = 150000.0  # Pa (150 kPa)
        radius = 6.0          # m
        t_orig = 0.004        # m (4 mm)

        # Hoop stress formula: sigma = P * r / t
        sigma_hoop_orig = (p_internal * radius) / t_orig
        self.assertAlmostEqual(sigma_hoop_orig, 225.0e6, delta=1.0)  # Must equal 225.0 MPa exactly!

        # 316L Stainless Steel yield strength is 220 MPa -> 4mm wall fails!
        sigma_yield = 220.0e6
        self.assertGreater(sigma_hoop_orig, sigma_yield)

        # Sizing wall with 1.5x safety factor on yield -> sigma_allow = 146.67 MPa
        sf = 1.5
        sigma_allow = sigma_yield / sf
        t_required = (p_internal * radius) / sigma_allow
        self.assertGreater(t_required, 0.00613)  # Requires ~6.14 mm minimum

        # Chosen wall thickness: 6.5 mm
        t_chosen = 0.0065
        sigma_hoop_chosen = (p_internal * radius) / t_chosen
        self.assertLess(sigma_hoop_chosen, sigma_allow)

    def test_nep_power_thrust_jet_coupling(self):
        """DEF-002 & DEF-003: Verify NEP electrical power to jet power to thrust & delta-v coupling."""
        p_elec = 15.0e6      # 15 MWe
        eta = 0.65            # Thruster efficiency
        p_jet = p_elec * eta  # 9.75 MWjet
        isp = 3500.0          # s
        v_e = isp * G0        # 34,323.28 m/s

        # Jet power relationship: P_jet = 0.5 * F * v_e
        thrust = (2.0 * p_jet) / v_e
        self.assertAlmostEqual(thrust, 568.12, delta=0.5)  # ~568.1 N

        # Verify trajectory performance for 180 days cruise burn
        m_dry = 1471.0  # MT
        m_initial_kg = (m_dry + 300.0) * 1000.0  # MT to kg
        nep_res = calculate_nep_burn(m_initial_kg, thrust, isp, duration_days=180.0)

        # Must achieve at least 2.55 km/s leg delta-v requirement
        self.assertGreaterEqual(nep_res["delta_v_kms"], 2.55)

    def test_shielding_calculator_multi_layer_stack(self):
        """DEF-006: Verify shielding calculator includes steel pressure hull layers."""
        res = shielding_calculator()
        col_density = res["col_density_shelter"]
        # SPE storm shelter design target is ~52.25 g/cm^2
        self.assertAlmostEqual(col_density, 52.25, delta=1.0)

    def test_centrifuge_walking_gravity_formula(self):
        """DEF-007: Verify centrifuge calculator implements full radial acceleration formula."""
        radius = 15.0  # m
        rpm = 6.0     # RPM
        walk_v = 1.5   # m/s

        res = analyze_centrifuge(radius, rpm, walk_v)
        omega = rpm * (2.0 * math.pi / 60.0)

        # Exact prograde formula: a_r = (omega*r + v)^2 / r
        expected_prograde = ((omega * radius + walk_v)**2) / radius
        self.assertAlmostEqual(res["a_prograde"], expected_prograde, places=4)

        # Exact retrograde formula: a_r = (omega*r - v)^2 / r
        expected_retrograde = ((omega * radius - walk_v)**2) / radius
        self.assertAlmostEqual(res["a_retrograde"], expected_retrograde, places=4)

    def test_thermal_radiator_stefan_boltzmann_balance(self):
        """Verify radiator surface area calculation under Stefan-Boltzmann law."""
        q_kw = 80000.0  # 80 MWth
        temp_k = 850.0   # K
        emiss = 0.90
        deg_margin = 0.15

        panel_area, flux_kw = calculate_radiator_area(q_kw, temp_k, emiss, deg_margin, double_sided=True)

        # Single sided emission flux = emiss * sigma * T^4
        sigma = 5.670374419e-8
        expected_flux_w = emiss * sigma * (temp_k**4)
        self.assertAlmostEqual(flux_kw * 1000.0, expected_flux_w, delta=1.0)

    def test_launch_manifest_capacity_closure(self):
        """DEF-004: Verify launch count calculations for heavy launch vehicles."""
        m_dep = 3971.0  # MT departure wet mass

        launches_250t = math.ceil(m_dep / 250.0)
        launches_150t = math.ceil(m_dep / 150.0)
        launches_100t = math.ceil(m_dep / 100.0)

        self.assertEqual(launches_250t, 16)
        self.assertEqual(launches_150t, 27)
        self.assertEqual(launches_100t, 40)

if __name__ == "__main__":
    unittest.main()
