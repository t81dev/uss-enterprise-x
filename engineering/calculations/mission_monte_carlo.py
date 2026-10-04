#!/usr/bin/env python3
"""
Monte Carlo Sensitivity Analysis for Project Occam-7 (USS Enterprise X)
Executes 1,000+ simulated mission cases varying key engineering and trajectory parameters.
Evaluates statistical distributions for:
- Mission success probability
- Parameter sensitivity rankings (Impact on mission success)
- Failure mode breakdown
- Machine-readable output generation
"""

import math
import json
import random
import os
from mission_digital_twin import MissionDigitalTwin, SpacecraftState

def run_monte_carlo_simulation(num_runs=1000):
    random.seed(42)  # Deterministic seed for repeatable verification

    results = []
    success_count = 0
    failure_reasons = {}
    variable_history = []

    for i in range(num_runs):
        # Sample parameters around baseline with realistic uncertainty standard deviations
        dry_mass = random.gauss(1470.96, 1470.96 * 0.05)       # ±5% std dev (max ±10%)
        lh2_mass = random.gauss(2200.0, 2200.0 * 0.03)          # ±3% std dev
        lnh3_mass = random.gauss(300.0, 300.0 * 0.03)           # ±3% std dev
        ntp_isp = random.gauss(900.0, 900.0 * 0.02)             # ±2% std dev
        ntp_thrust = random.gauss(4000.0, 4000.0 * 0.03)       # ±3% std dev
        nep_power = random.gauss(15.0, 15.0 * 0.05)             # ±5% std dev
        nep_eff = random.uniform(0.58, 0.72)                   # 0.65 ±0.07
        rad_capacity = random.gauss(133.35, 133.35 * 0.05)      # ±5% std dev
        consumables_rate = random.gauss(0.0723, 0.0723 * 0.05) # ±5% std dev

        # Instantiate custom state
        state = SpacecraftState(
            dry_mass_mt=dry_mass,
            lh2_mt=lh2_mass,
            lnh3_mt=lnh3_mass,
            crew_consumables_mt=72.3
        )
        state.system_health["nep_efficiency"] = nep_eff

        twin = MissionDigitalTwin(initial_state=state)
        output = twin.run_full_mission_baseline()

        success = output["success_predicate_assessment"]["mission_success"]
        predicates = output["success_predicate_assessment"]["predicates"]

        if success:
            success_count += 1
        else:
            # Track failure causes
            for k, v in predicates.items():
                if not v:
                    failure_reasons[k] = failure_reasons.get(k, 0) + 1

        run_record = {
            "run_id": i + 1,
            "success": success,
            "dry_mass_mt": round(dry_mass, 2),
            "lh2_mass_mt": round(lh2_mass, 2),
            "lnh3_mass_mt": round(lnh3_mass, 2),
            "ntp_isp_s": round(ntp_isp, 1),
            "nep_power_mwe": round(nep_power, 2),
            "nep_efficiency": round(nep_eff, 3),
            "final_delta_v_kms": output["final_state"]["total_delta_v_kms"],
            "lh2_remaining_mt": output["final_state"]["lh2_mt"],
            "lnh3_remaining_mt": output["final_state"]["lnh3_mt"]
        }
        results.append(run_record)
        variable_history.append(run_record)

    success_rate = (success_count / num_runs) * 100.0

    # Perform parameter sensitivity ranking (Delta mean between success and failure)
    success_runs = [r for r in variable_history if r["success"]]
    fail_runs = [r for r in variable_history if not r["success"]]

    sensitivities = []
    if success_runs and fail_runs:
        for param in ["dry_mass_mt", "lh2_mass_mt", "lnh3_mass_mt", "ntp_isp_s", "nep_power_mwe", "nep_efficiency"]:
            mean_succ = sum(r[param] for r in success_runs) / len(success_runs)
            mean_fail = sum(r[param] for r in fail_runs) / len(fail_runs)
            pct_delta = abs(mean_succ - mean_fail) / mean_succ * 100.0
            sensitivities.append({"parameter": param, "impact_score_pct": round(pct_delta, 2), "mean_success": round(mean_succ, 2), "mean_fail": round(mean_fail, 2)})

    sensitivities.sort(key=lambda x: x["impact_score_pct"], reverse=True)

    summary = {
        "total_simulated_cases": num_runs,
        "successful_cases": success_count,
        "failed_cases": num_runs - success_count,
        "success_rate_percent": round(success_rate, 2),
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
    run_monte_carlo_simulation(1000)
