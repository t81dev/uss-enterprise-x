#!/usr/bin/env python3
"""
Monte Carlo Sensitivity Analysis & Causal Failure Validation for Project Occam-7 (USS Enterprise X)
Updated for Program Phase 8.6 — Radiation Transport & Habitat Geometry Closure.

Executes 10,000 simulated mission cases under Architecture B (Precursor Autonomous ISRU Depot).
Evaluates:
- Statistical distributions for mission success P(success)
- Dynamic Radiation Environment sampling (GCR solar cycle, SPE frequency/severity, shelter response delays)
- Structured causal failure taxonomy (Root engineering failures vs Cascaded downstream predicates)
- Parameter provenance classifications (MEASURED, SPECIFIED, DERIVED, MODELED, ASSUMED, PROVISIONAL, UNKNOWN)
- 446.21 t verified depot reserve stress analysis under uncertainty
- Spearman rank correlation sensitivity analysis
- Deterministic seed reproducibility (seed=42)
- Machine-readable JSON output generation
"""

import math
import json
import random
import os
from mission_digital_twin import MissionDigitalTwin, SpacecraftState
from mars_isru import MarsISRUModel, REQUIRED_GROSS_DEPOT_WITHDRAWAL_MT, REQUIRED_NET_RETURN_LH2_MT

# Parameter Provenance Classification Metadata
PARAMETER_PROVENANCE = {
    "dry_mass_mt": {
        "parameter": "dry_mass_mt",
        "nominal_value": 1470.96,
        "classification": "SPECIFIED",
        "uncertainty_type": "Epistemic",
        "description": "Baseline unmargined dry mass subtotal (1,225.80 t) with 20% AIAA reserve margin -> 1,470.96 t dry baseline.",
        "distribution": "Gaussian",
        "parameters": {"mean": 1470.96, "std_dev": 73.548},
        "source": "68-system-reference-model-v5.md",
        "rationale": "AIAA S-120A dry mass contingency growth standard assumption (±5% sigma)."
    },
    "lh2_mass_mt": {
        "parameter": "lh2_mass_mt",
        "nominal_value": 2200.0,
        "classification": "SPECIFIED",
        "uncertainty_type": "Epistemic",
        "description": "Initial spacecraft LH2 propellant load at Earth departure.",
        "distribution": "Gaussian",
        "parameters": {"mean": 2200.0, "std_dev": 66.0},
        "source": "68-system-reference-model-v5.md",
        "rationale": "Specified tank capacity and departure loading budget (±3% sigma)."
    },
    "lnh3_mass_mt": {
        "parameter": "lnh3_mass_mt",
        "nominal_value": 300.0,
        "classification": "SPECIFIED",
        "uncertainty_type": "Epistemic",
        "description": "Initial spacecraft LNH3 propellant load at Earth departure.",
        "distribution": "Gaussian",
        "parameters": {"mean": 300.0, "std_dev": 9.0},
        "source": "68-system-reference-model-v5.md",
        "rationale": "Specified secondary propellant tank loading budget (±3% sigma)."
    },
    "nep_efficiency": {
        "parameter": "nep_efficiency",
        "nominal_value": 0.65,
        "classification": "MODELED",
        "uncertainty_type": "Aleatory/Epistemic",
        "description": "Magnetoplasmadynamic (MPD) thruster electrical-to-jet power efficiency.",
        "distribution": "Uniform",
        "parameters": {"min": 0.58, "max": 0.72},
        "source": "03-propulsion.md",
        "rationale": "Theoretical plasma acceleration thruster efficiency range based on laboratory MPD models."
    },
    "gcr_environment": {
        "parameter": "gcr_environment",
        "nominal_value": "nominal",
        "classification": "MODELED",
        "uncertainty_type": "Aleatory",
        "description": "Solar cycle phase variation modulating galactic cosmic ray background intensity.",
        "distribution": "Categorical",
        "parameters": {"solar_maximum": 0.25, "nominal": 0.50, "solar_minimum": 0.25},
        "source": "27-radiation-protection-model.md",
        "rationale": "11-year solar activity cycle variation."
    },
    "spe_scenario": {
        "parameter": "spe_scenario",
        "nominal_value": "severe",
        "classification": "MODELED",
        "uncertainty_type": "Aleatory",
        "description": "Solar particle event storm fluence/flux severity level.",
        "distribution": "Categorical",
        "parameters": {"moderate": 0.50, "severe": 0.40, "extreme_design_basis": 0.10},
        "source": "27-radiation-protection-model.md",
        "rationale": "Historical SPE frequency and magnitude distributions."
    },
    "shelter_response_time_min": {
        "parameter": "shelter_response_time_min",
        "nominal_value": 10.0,
        "classification": "ASSUMED",
        "uncertainty_type": "Aleatory",
        "description": "Crew transit time from ambient habitat deck into central SPE storm shelter core upon SPE alarm.",
        "distribution": "Uniform",
        "parameters": {"min": 0.0, "max": 60.0},
        "source": "58-crew-survivability-model-v1.md",
        "rationale": "Operational emergency response time range."
    }
}


def classify_run_failures(twin, canonical_predicates):
    """Structured Causal Failure Taxonomy Algorithm."""
    root_failures = []

    if not canonical_predicates.get("precursor_payload_closure", True):
        root_failures.append("lander_payload_capacity_deficit")

    if not canonical_predicates.get("surface_average_power_closure", True):
        root_failures.append("surface_average_power_deficit")
    if not canonical_predicates.get("surface_peak_power_closure", True):
        root_failures.append("surface_peak_power_deficit")

    if not canonical_predicates.get("surface_thermal_closure", True):
        root_failures.append("surface_thermal_capacity_deficit")
    elif not canonical_predicates.get("surface_thermal_margin_compliance", True):
        root_failures.append("surface_thermal_margin_deficit")

    if not canonical_predicates.get("isru_production_complete", True):
        upstream_failures = [
            "lander_payload_capacity_deficit",
            "surface_average_power_deficit",
            "surface_peak_power_deficit",
            "surface_thermal_capacity_deficit",
            "surface_thermal_margin_deficit"
        ]
        if not any(f in root_failures for f in upstream_failures):
            root_failures.append("isru_propellant_production_deficit")

    if not canonical_predicates.get("depot_verified", True):
        upstream_failures = [
            "lander_payload_capacity_deficit",
            "surface_average_power_deficit",
            "surface_peak_power_deficit",
            "surface_thermal_capacity_deficit",
            "surface_thermal_margin_deficit",
            "isru_propellant_production_deficit"
        ]
        if not any(f in root_failures for f in upstream_failures):
            root_failures.append("depot_verification_or_transfer_system_failure")

    if not canonical_predicates.get("propellant_reserve_sufficient", True):
        root_failures.append("spacecraft_propellant_reserve_exhaustion")

    if not canonical_predicates.get("vehicle_power_margin", True) or not canonical_predicates.get("vehicle_thermal_margin", True):
        root_failures.append("vehicle_power_or_thermal_margin_deficit")

    if not canonical_predicates.get("radiation_survivability", True) or not canonical_predicates.get("crew_survivability", True):
        root_failures.append("radiation_cumulative_dose_exceeded")

    if not canonical_predicates.get("acute_spe_survivability", True):
        root_failures.append("acute_spe_dose_exceeded")

    if not canonical_predicates.get("storm_shelter_closure", True):
        root_failures.append("storm_shelter_subsystem_failure")

    cascaded_predicates = [k for k, v in canonical_predicates.items() if not v]

    return root_failures, cascaded_predicates


def run_monte_carlo_simulation(num_runs=10000, correlated_degradation=False):
    random.seed(42)

    results = []
    success_count = 0
    root_failure_counts = {}
    cascaded_predicate_counts = {}
    simultaneous_root_failure_runs = 0
    simultaneous_root_distribution = {}

    remaining_reserves_mt = []

    for i in range(num_runs):
        dry_mass = random.gauss(1470.96, 1470.96 * 0.05)
        lh2_mass = random.gauss(2200.0, 2200.0 * 0.03)
        lnh3_mass = random.gauss(300.0, 300.0 * 0.03)
        nep_eff = random.uniform(0.58, 0.72)

        # Radiation parameter sampling
        gcr_rand = random.random()
        if gcr_rand < 0.25:
            gcr_env = "solar_maximum"
        elif gcr_rand < 0.75:
            gcr_env = "nominal"
        else:
            gcr_env = "solar_minimum"

        spe_rand = random.random()
        if spe_rand < 0.50:
            spe_scen = "moderate"
        elif spe_rand < 0.90:
            spe_scen = "severe"
        else:
            spe_scen = "extreme_design_basis"

        response_time = random.uniform(0.0, 45.0)  # min

        if correlated_degradation:
            env_factor = random.uniform(0.85, 1.0)
            ice_conc = random.uniform(0.35, 0.65)
            soec_eff = random.uniform(0.60, 0.80) * env_factor
            liq_eff = random.uniform(0.20, 0.30) * env_factor
            isru_power_mwe = random.gauss(25.0, 1.2) * env_factor
        else:
            ice_conc = random.uniform(0.35, 0.65)
            soec_eff = random.uniform(0.60, 0.80)
            liq_eff = random.uniform(0.20, 0.30)
            isru_power_mwe = random.gauss(25.0, 1.2)

        isru_avail = random.uniform(0.80, 1.00)
        downtime_days = random.uniform(0.0, 90.0)
        num_landers = 2
        lander_1_capacity = random.gauss(150.0, 5.0)
        lander_2_capacity = random.gauss(150.0, 5.0)

        state = SpacecraftState(
            dry_mass_mt=dry_mass,
            lh2_mt=lh2_mass,
            lnh3_mt=lnh3_mass
        )
        state.system_health["nep_efficiency"] = nep_eff
        state.gcr_environment = gcr_env
        state.spe_scenario = spe_scen
        state.crew_response_time_min = response_time

        nominal_window_days = 750.0
        effective_days = (nominal_window_days - downtime_days) * isru_avail

        isru_model = MarsISRUModel(
            target_lh2_net_mt=2200.0,
            production_days=effective_days,
            ice_concentration=ice_conc,
            soec_efficiency=soec_eff,
            liquefaction_efficiency=liq_eff
        )

        twin = MissionDigitalTwin(initial_state=state, isru_model=isru_model)

        precursor_res = twin.run_precursor_mission(
            duration_days=effective_days,
            available_power_mwe=isru_power_mwe,
            number_of_landers=num_landers,
            lander_1_capacity_mt=lander_1_capacity,
            lander_2_capacity_mt=lander_2_capacity
        )

        crewed_res = twin.run_crewed_mission()

        success = crewed_res["success_predicate_assessment"]["mission_success"]
        canonical_predicates = crewed_res["success_predicate_assessment"].get("canonical_predicates", crewed_res["success_predicate_assessment"]["predicates"])

        depot_reserve_mt = twin.depot.remaining_verified_depot_inventory_mt
        remaining_reserves_mt.append(depot_reserve_mt)

        if success:
            success_count += 1
        else:
            roots, cascaded = classify_run_failures(twin, canonical_predicates)

            for r in roots:
                root_failure_counts[r] = root_failure_counts.get(r, 0) + 1

            for c in cascaded:
                cascaded_predicate_counts[c] = cascaded_predicate_counts.get(c, 0) + 1

            num_roots = len(roots)
            if num_roots > 1:
                simultaneous_root_failure_runs += 1
                key = f"{num_roots}_simultaneous_roots"
                simultaneous_root_distribution[key] = simultaneous_root_distribution.get(key, 0) + 1

        run_record = {
            "run_id": i + 1,
            "success": 1 if success else 0,
            "dry_mass_mt": round(dry_mass, 2),
            "lh2_mass_mt": round(lh2_mass, 2),
            "lnh3_mass_mt": round(lnh3_mass, 2),
            "nep_efficiency": round(nep_eff, 3),
            "gcr_environment": gcr_env,
            "spe_scenario": spe_scen,
            "crew_response_time_min": round(response_time, 1),
            "accumulated_radiation_csv": round(twin.state.accumulated_radiation_csv, 2),
            "depot_reserve_mt": round(depot_reserve_mt, 2)
        }
        results.append(run_record)

    success_rate = (success_count / num_runs) * 100.0

    z = 1.959964
    p_hat = success_count / num_runs
    denom = 1.0 + (z**2) / num_runs
    p_mid = (p_hat + (z**2) / (2.0 * num_runs)) / denom
    p_bound = (z / denom) * math.sqrt((p_hat * (1.0 - p_hat) / num_runs) + ((z**2) / (4.0 * (num_runs**2))))
    ci_lower_pct = max(0.0, (p_mid - p_bound) * 100.0)
    ci_upper_pct = min(100.0, (p_mid + p_bound) * 100.0)

    def spearman_correlation(x_vals, y_vals):
        n = len(x_vals)
        if n == 0:
            return 0.0

        def get_ranks(vals):
            sorted_indices = sorted(range(n), key=lambda idx: vals[idx])
            ranks = [0.0] * n
            i = 0
            while i < n:
                j = i
                while j < n - 1 and vals[sorted_indices[j]] == vals[sorted_indices[j + 1]]:
                    j += 1
                avg_rank = (i + j) / 2.0 + 1.0
                for k in range(i, j + 1):
                    ranks[sorted_indices[k]] = avg_rank
                i = j + 1
            return ranks

        rx = get_ranks(x_vals)
        ry = get_ranks(y_vals)

        mean_rx = sum(rx) / n
        mean_ry = sum(ry) / n

        num = sum((rx[k] - mean_rx) * (ry[k] - mean_ry) for k in range(n))
        den = math.sqrt(sum((rx[k] - mean_rx)**2 for k in range(n)) * sum((ry[k] - mean_ry)**2 for k in range(n)))
        return num / den if den > 0 else 0.0

    y_success = [r["success"] for r in results]
    sensitivities = []
    monitored_params = [
        "dry_mass_mt",
        "lh2_mass_mt",
        "lnh3_mass_mt",
        "nep_efficiency",
        "crew_response_time_min"
    ]

    for param in monitored_params:
        x_vals = [r[param] for r in results]
        rho = spearman_correlation(x_vals, y_success)
        sensitivities.append({
            "parameter": param,
            "spearman_rank_correlation": round(rho, 4),
            "correlation_magnitude": round(abs(rho), 4),
            "provenance_classification": PARAMETER_PROVENANCE.get(param, {}).get("classification", "UNKNOWN")
        })

    sensitivities.sort(key=lambda item: item["correlation_magnitude"], reverse=True)

    sorted_reserves = sorted(remaining_reserves_mt)
    p05_idx = int(0.05 * num_runs)
    p50_idx = int(0.50 * num_runs)
    p95_idx = int(0.95 * num_runs)

    reserve_stats = {
        "nominal_baseline_reserve_mt": 446.21,
        "mean_reserve_mt": round(sum(remaining_reserves_mt) / num_runs, 2),
        "min_reserve_mt": round(sorted_reserves[0], 2),
        "max_reserve_mt": round(sorted_reserves[-1], 2),
        "percentile_5th_mt": round(sorted_reserves[p05_idx], 2),
        "median_50th_mt": round(sorted_reserves[p50_idx], 2),
        "percentile_95th_mt": round(sorted_reserves[p95_idx], 2),
        "deficit_runs_count": sum(1 for r in remaining_reserves_mt if r < 0.0)
    }

    summary = {
        "random_seed": 42,
        "total_simulated_cases": num_runs,
        "correlated_degradation_mode": correlated_degradation,
        "successful_cases": success_count,
        "failed_cases": num_runs - success_count,
        "estimated_success_probability_percent": round(success_rate, 2),
        "confidence_interval_95_percent": {
            "lower_bound_percent": round(ci_lower_pct, 2),
            "upper_bound_percent": round(ci_upper_pct, 2),
            "method": "Wilson Score Interval"
        },
        "program_status": "ENGINEERINGALLY CONDITIONAL" if success_rate >= 80.0 else "PHYSICALLY INFEASIBLE",
        "causal_failure_taxonomy": {
            "root_failure_counts": root_failure_counts,
            "simultaneous_independent_root_failure_runs": simultaneous_root_failure_runs,
            "simultaneous_root_distribution": simultaneous_root_distribution,
            "cascaded_predicate_counts": cascaded_predicate_counts
        },
        "parameter_provenance_audit": PARAMETER_PROVENANCE,
        "verified_depot_reserve_stress_analysis": reserve_stats,
        "parameter_sensitivity_ranking": sensitivities
    }

    return summary


def run_full_monte_carlo_suite(num_runs=10000, output_path="engineering/calculations/mission_monte_carlo.json"):
    print(f"Executing Monte Carlo analysis suite ({num_runs} runs)...")
    independent_summary = run_monte_carlo_simulation(num_runs=num_runs, correlated_degradation=False)
    correlated_summary = run_monte_carlo_simulation(num_runs=num_runs, correlated_degradation=True)

    combined_output = dict(independent_summary)
    combined_output["independent_uncertainty_analysis"] = {
        "total_simulated_cases": independent_summary["total_simulated_cases"],
        "success_rate_percent": independent_summary["estimated_success_probability_percent"],
        "confidence_interval_95_percent": independent_summary["confidence_interval_95_percent"],
        "root_failure_counts": independent_summary["causal_failure_taxonomy"]["root_failure_counts"],
        "reserve_stats": independent_summary["verified_depot_reserve_stress_analysis"]
    }
    combined_output["correlated_degradation_scenario_analysis"] = {
        "total_simulated_cases": correlated_summary["total_simulated_cases"],
        "success_rate_percent": correlated_summary["estimated_success_probability_percent"],
        "confidence_interval_95_percent": correlated_summary["confidence_interval_95_percent"],
        "root_failure_counts": correlated_summary["causal_failure_taxonomy"]["root_failure_counts"],
        "reserve_stats": correlated_summary["verified_depot_reserve_stress_analysis"],
        "description": "Modeled environmental common-cause degradation event affecting SOEC, liquefaction, and reactor power output simultaneously."
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(combined_output, f, indent=2)

    print(f"Independent Monte Carlo success rate: {independent_summary['estimated_success_probability_percent']:.2f}%")
    print(f"Correlated degradation scenario success rate: {correlated_summary['estimated_success_probability_percent']:.2f}%")
    print(f"Report written to {output_path}")
    return combined_output


if __name__ == "__main__":
    run_full_monte_carlo_suite(10000)
