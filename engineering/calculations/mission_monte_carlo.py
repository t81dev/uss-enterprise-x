#!/usr/bin/env python3
"""
Monte Carlo Sensitivity Analysis for Project Occam-7 (USS Enterprise X)
Updated for Program Phase 8.1 — Codex Defect Remediation & Mission Integrity.

Executes 10,000 simulated mission cases under Architecture B (Precursor Autonomous ISRU Depot).
Evaluates statistical distributions for:
- Mission success probability P(success)
- ISRU production success probability
- Parameter sensitivity rankings (Impact on mission success)
- Failure mode breakdown
- Machine-readable output generation
"""

import math
import json
import random
import os
from mission_digital_twin import MissionDigitalTwin, SpacecraftState
from mars_isru import MarsISRUModel


def run_monte_carlo_simulation(num_runs=10000):
    random.seed(42)  # Deterministic seed for repeatable verification

    results = []
    success_count = 0
    primary_failure_reasons = {}
    failure_reasons = {}
    variable_history = []

    for i in range(num_runs):
        # Sample Spacecraft Parameters
        dry_mass = random.gauss(1470.96, 1470.96 * 0.05)       # ±5% std dev
        lh2_mass = random.gauss(2200.0, 2200.0 * 0.03)          # ±3% std dev
        lnh3_mass = random.gauss(300.0, 300.0 * 0.03)           # ±3% std dev
        nep_eff = random.uniform(0.58, 0.72)                   # 0.65 ±0.07

        # Sample Mars Precursor ISRU Parameters
        ice_conc = random.uniform(0.35, 0.65)                  # 35% to 65% ice in regolith
        soec_eff = random.uniform(0.60, 0.80)                  # 60% to 80% SOEC efficiency
        liq_eff = random.uniform(0.20, 0.30)                   # 20% to 30% Carnot liquefaction efficiency
        isru_power_mwe = random.gauss(25.0, 1.2)               # 25.0 MWe precursor nuclear reactor (std dev 1.2 MW)
        isru_avail = random.uniform(0.80, 1.00)                # 80% to 100% equipment availability
        downtime_days = random.uniform(0.0, 90.0)             # 0 to 90 days maintenance downtime
        num_landers = 2                                        # Multi-lander precursor architecture
        lander_1_capacity = random.gauss(150.0, 5.0)           # Independent Lander 1 capacity variation
        lander_2_capacity = random.gauss(150.0, 5.0)           # Independent Lander 2 capacity variation

        # Instantiate custom state
        state = SpacecraftState(
            dry_mass_mt=dry_mass,
            lh2_mt=lh2_mass,
            lnh3_mt=lnh3_mass
        )
        state.system_health["nep_efficiency"] = nep_eff

        # Evaluate Precursor ISRU capability (750-day window available before crew Earth departure)
        nominal_window_days = 750.0
        effective_days = (nominal_window_days - downtime_days) * isru_avail

        # Parameterize model with sampled efficiencies
        isru_model = MarsISRUModel(
            target_lh2_net_mt=2200.0,
            production_days=effective_days,
            ice_concentration=ice_conc,
            soec_efficiency=soec_eff,
            liquefaction_efficiency=liq_eff
        )

        twin = MissionDigitalTwin(initial_state=state, isru_model=isru_model)

        # Run Phase A (Precursor)
        precursor_res = twin.run_precursor_mission(
            duration_days=effective_days,
            available_power_mwe=isru_power_mwe,
            number_of_landers=num_landers,
            lander_1_capacity_mt=lander_1_capacity,
            lander_2_capacity_mt=lander_2_capacity
        )

        # Run Phase B (Crewed Mission)
        crewed_res = twin.run_crewed_mission()

        success = crewed_res["success_predicate_assessment"]["mission_success"]
        predicates = crewed_res["success_predicate_assessment"]["predicates"]

        if success:
            success_count += 1
        else:
            primary_found = False
            for k, v in predicates.items():
                if not v:
                    # Count overlapping
                    failure_reasons[k] = failure_reasons.get(k, 0) + 1
                    # Count primary
                    if not primary_found:
                        primary_failure_reasons[k] = primary_failure_reasons.get(k, 0) + 1
                        primary_found = True

        run_record = {
            "run_id": i + 1,
            "success": 1 if success else 0,
            "dry_mass_mt": round(dry_mass, 2),
            "lh2_mass_mt": round(lh2_mass, 2),
            "lnh3_mass_mt": round(lnh3_mass, 2),
            "nep_efficiency": round(nep_eff, 3),
            "ice_concentration": round(ice_conc, 3),
            "soec_efficiency": round(soec_eff, 3),
            "liquefaction_efficiency": round(liq_eff, 3),
            "isru_power_mwe": round(isru_power_mwe, 2),
            "isru_downtime_days": round(downtime_days, 1),
            "lander_1_capacity_mt": round(lander_1_capacity, 2),
            "lander_2_capacity_mt": round(lander_2_capacity, 2),
            "lh2_produced_mt": round(twin.depot.lh2_produced_mt, 1)
        }
        results.append(run_record)
        variable_history.append(run_record)

    success_rate = (success_count / num_runs) * 100.0

    # 95% Wilson Score Confidence Interval
    z = 1.959964  # 95% confidence z-score
    p_hat = success_count / num_runs
    denom = 1.0 + (z**2) / num_runs
    p_mid = (p_hat + (z**2) / (2.0 * num_runs)) / denom
    p_bound = (z / denom) * math.sqrt((p_hat * (1.0 - p_hat) / num_runs) + ((z**2) / (4.0 * (num_runs**2))))
    ci_lower_pct = max(0.0, (p_mid - p_bound) * 100.0)
    ci_upper_pct = min(100.0, (p_mid + p_bound) * 100.0)

    # Spearman Rank Correlation Sensitivity Analysis
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

    y_success = [r["success"] for r in variable_history]
    sensitivities = []
    monitored_params = [
        "isru_power_mwe",
        "isru_downtime_days",
        "soec_efficiency",
        "liquefaction_efficiency",
        "ice_concentration",
        "dry_mass_mt",
        "lh2_mass_mt",
        "lnh3_mass_mt",
        "nep_efficiency",
        "lander_1_capacity_mt",
        "lander_2_capacity_mt"
    ]

    for param in monitored_params:
        x_vals = [r[param] for r in variable_history]
        rho = spearman_correlation(x_vals, y_success)
        sensitivities.append({
            "parameter": param,
            "spearman_rank_correlation": round(rho, 4),
            "correlation_magnitude": round(abs(rho), 4)
        })

    sensitivities.sort(key=lambda item: item["correlation_magnitude"], reverse=True)

    summary = {
        "random_seed": 42,
        "total_simulated_cases": num_runs,
        "successful_cases": success_count,
        "failed_cases": num_runs - success_count,
        "estimated_success_probability_percent": round(success_rate, 2),
        "confidence_interval_95_percent": {
            "lower_bound_percent": round(ci_lower_pct, 2),
            "upper_bound_percent": round(ci_upper_pct, 2),
            "method": "Wilson Score Interval"
        },
        "program_status": "ENGINEERINGALLY CONDITIONAL" if success_rate >= 80.0 else "PHYSICALLY INFEASIBLE",
        "primary_failure_reason_counts": primary_failure_reasons,
        "overlapping_predicate_failure_counts": failure_reasons,
        "parameter_sensitivity_ranking": sensitivities
    }

    out_path = "engineering/calculations/mission_monte_carlo.json"
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"Monte Carlo simulation of {num_runs} cases completed.")
    print(f"Success rate: {success_rate:.2f}%")
    print(f"Report written to {out_path}")
    return summary


if __name__ == "__main__":
    run_monte_carlo_simulation(10000)
