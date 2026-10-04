#!/usr/bin/env python3
"""
Mass Budget Calculator for USS Enterprise X (Project Occam-7)
Calculates bottom-up vehicle dry mass, wet mass, consumables, and margin.
"""

def calculate_mass_budget():
    # Primary Subsystems (Metric Tons - MT) Baseline
    subsystems = {
        "Primary Structure & Spine": {"opt": 140.0, "base": 210.0, "pess": 300.0, "cat": "Structure"},
        "Pressure Hull (Habitat Decks & Labs)": {"opt": 90.0, "base": 135.0, "pess": 180.0, "cat": "Structure"},
        "Passive Radiation Shielding (SPE Shelter + GCR)": {"opt": 160.0, "base": 240.0, "pess": 320.0, "cat": "Shielding"},
        "Nuclear Reactor & Reactor Shadow Shield": {"opt": 50.0, "base": 75.0, "pess": 110.0, "cat": "Power"},
        "Propulsion Engines & Thrust Frame": {"opt": 35.0, "base": 55.0, "pess": 85.0, "cat": "Propulsion"},
        "Main Propellant Tanks (Dry Hull & Insulation)": {"opt": 70.0, "base": 110.0, "pess": 160.0, "cat": "Tanks"},
        "Thermal Management (Radiators, Loops, Deployables)": {"opt": 35.0, "base": 55.0, "pess": 80.0, "cat": "Thermal"},
        "ECLSS Hardware & Closed-Loop Recycling": {"opt": 20.0, "base": 30.0, "pess": 45.0, "cat": "Habitation"},
        "Avionics, Computing & Optical Bus": {"opt": 6.0, "base": 10.0, "pess": 15.0, "cat": "Avionics"},
        "GNC, Reaction Control System & Wheels": {"opt": 12.0, "base": 18.0, "pess": 25.0, "cat": "Avionics"},
        "Communications & Deep-Space Lasers": {"opt": 4.0, "base": 6.0, "pess": 10.0, "cat": "Comms"},
        "Crew Accommodations, Quarters & Medical": {"opt": 18.0, "base": 25.0, "pess": 35.0, "cat": "Habitation"},
        "Centrifuge Mechanism & Dynamic Bearings": {"opt": 15.0, "base": 22.0, "pess": 32.0, "cat": "Habitation"},
        "Scientific Payload, Probes & Landers": {"opt": 40.0, "base": 65.0, "pess": 100.0, "cat": "Payload"},
        "Defensive Systems & MMOD Whipple Shielding": {"opt": 12.0, "base": 20.0, "pess": 30.0, "cat": "Defense"},
        "Docking, Berthing & Servicing Hardware": {"opt": 8.0, "base": 12.0, "pess": 18.0, "cat": "Structure"},
        "Maintenance Inventory & Spare Cassettes": {"opt": 15.0, "base": 25.0, "pess": 40.0, "cat": "Operations"},
        "1,000-Day Net Consumables (24 Crew + ECLSS Makeup)": {"opt": 60.0, "base": 72.3, "pess": 90.0, "cat": "Consumables"}
    }

    subtotal_opt = sum(item["opt"] for item in subsystems.values())
    subtotal_base = sum(item["base"] for item in subsystems.values())
    subtotal_pess = sum(item["pess"] for item in subsystems.values())

    margin_rate = 0.20  # 20% AIAA reserve margin
    margin_opt = subtotal_opt * margin_rate
    margin_base = subtotal_base * margin_rate
    margin_pess = subtotal_pess * margin_rate

    dry_mass_opt = subtotal_opt + margin_opt
    dry_mass_base = subtotal_base + margin_base
    dry_mass_pess = subtotal_pess + margin_pess

    # Propellant Mass Options (MT)
    # Baseline Mission B (Earth-Mars-Earth): 2,200 MT LH2 for NTP + 300 MT LNH3/Ar for NEP
    propellant_base = 2500.0
    propellant_opt = 1800.0
    propellant_pess = 3500.0

    wet_mass_opt = dry_mass_opt + propellant_opt
    wet_mass_base = dry_mass_base + propellant_base
    wet_mass_pess = dry_mass_pess + propellant_pess

    print("=== USS ENTERPRISE X - MASS BUDGET V2 SUMMARY ===")
    print(f"Subtotal Dry (Unmargined): Opt={subtotal_opt:.1f} t | Base={subtotal_base:.1f} t | Pess={subtotal_pess:.1f} t")
    print(f"Reserve Growth Margin (20%): Opt={margin_opt:.1f} t | Base={margin_base:.1f} t | Pess={margin_pess:.1f} t")
    print(f"TOTAL DRY MASS:            Opt={dry_mass_opt:.1f} t | Base={dry_mass_base:.1f} t | Pess={dry_mass_pess:.1f} t")
    print(f"Main Propellant Mass:      Opt={propellant_opt:.1f} t | Base={propellant_base:.1f} t | Pess={propellant_pess:.1f} t")
    print(f"GROSS DEPARTURE WET MASS:  Opt={wet_mass_opt:.1f} t | Base={wet_mass_base:.1f} t | Pess={wet_mass_pess:.1f} t")

    return {
        "subtotal_base": subtotal_base,
        "dry_mass_base": dry_mass_base,
        "wet_mass_base": wet_mass_base
    }

if __name__ == "__main__":
    calculate_mass_budget()
