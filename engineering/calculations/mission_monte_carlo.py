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
        capacity_per_lander = random.gauss(150.0, 5.0)        # ±5t lander capacity variation

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
            lander_capacity_mt=capacity_per_lander
        )

        # Run Phase B (Crewed Mission)
        crewed_res = twin.run_crewed_mission()

        success = crewed_res["success_predicate_assessment"]["mission_success"]
        predicates = crewed_res["success_predicate_assessment"]["predicates"]

        if success:
            success_count += 1
        else:
            for k, v in predicates.items():
                if not v:
                    failure_reasons[k] = failure_reasons.get(k, 0) + 1

        run_record = {
            "run_id": i + 1,
            "success": success,
            "dry_mass_mt": round(dry_mass, 2),
            "lh2_mass_mt": round(lh2_mass, 2),
            "ice_concentration": round(ice_conc, 3),
            "soec_efficiency": round(soec_eff, 3),
            "liquefaction_efficiency": round(liq_eff, 3),
            "isru_power_mwe": round(isru_power_mwe, 2),
            "isru_downtime_days": round(downtime_days, 1),
            "capacity_per_lander_mt": round(capacity_per_lander, 2),
            "lh2_produced_mt": round(twin.depot.lh2_produced_mt, 1)
        }
        results.append(run_record)
        variable_history.append(run_record)

    success_rate = (success_count / num_runs) * 100.0

    # Sensitivity ranking
    success_runs = [r for r in variable_history if r["success"]]
    fail_runs = [r for r in variable_history if not r["success"]]

    sensitivities = []
    if success_runs and fail_runs:
        for param in ["isru_power_mwe", "isru_downtime_days", "soec_efficiency", "liquefaction_efficiency", "ice_concentration", "dry_mass_mt", "lh2_mass_mt", "capacity_per_lander_mt"]:
            mean_succ = sum(r[param] for r in success_runs) / len(success_runs)
            mean_fail = sum(r[param] for r in fail_runs) / len(fail_runs)
            pct_delta = abs(mean_succ - mean_fail) / mean_succ * 100.0 if mean_succ > 0 else 0.0
            sensitivities.append({
                "parameter": param,
                "impact_score_pct": round(pct_delta, 2),
                "mean_success": round(mean_succ, 2),
                "mean_fail": round(mean_fail, 2)
            })

    sensitivities.sort(key=lambda x: x["impact_score_pct"], reverse=True)

    summary = {
        "total_simulated_cases": num_runs,
        "successful_cases": success_count,
        "failed_cases": num_runs - success_count,
        "success_rate_percent": round(success_rate, 2),
        "program_status": "ENGINEERINGALLY CONDITIONAL" if success_rate >= 80.0 else "PHYSICALLY INFEASIBLE",
        "failure_reason_breakdown": failure_reasons,
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
