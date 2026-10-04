#!/usr/bin/env python3
"""
Mass Budget Calculator for USS Enterprise X (Project Occam-7)
Calculates bottom-up vehicle dry mass, wet mass, consumables, and margin with 100% row summation reconciliation.
"""

def calculate_mass_budget():
    # Primary Subsystems (Metric Tons - MT) Baseline
    # Updated tank dry mass from 110 MT to 178.75 MT (6.5mm SS 316L pressure vessel sizing for 150 kPa hoop stress)
    subsystems = {
        "Primary Structure & Spine Truss": {"opt": 140.0, "base": 210.0, "pess": 300.0, "cat": "Structure"},
        "Pressure Hull (Habitat Decks & Labs)": {"opt": 90.0, "base": 135.0, "pess": 180.0, "cat": "Structure"},
        "Main Propellant Tanks (Dry Hull 6.5mm)": {"opt": 115.0, "base": 178.75, "pess": 240.0, "cat": "Tanks"},
        "Passive Radiation Shielding (SPE Shelter + GCR)": {"opt": 160.0, "base": 240.0, "pess": 320.0, "cat": "Shielding"},
        "Nuclear Reactor Core & Electrical Conversion": {"opt": 20.0, "base": 30.0, "pess": 45.0, "cat": "Power"},
        "Reactor Shadow Shielding": {"opt": 30.0, "base": 45.0, "pess": 65.0, "cat": "Power"},
        "Propulsion Engines (4x NTP + MPD Arrays)": {"opt": 25.0, "base": 40.0, "pess": 60.0, "cat": "Propulsion"},
        "Thrust Vector & Gimbals": {"opt": 10.0, "base": 15.0, "pess": 25.0, "cat": "Propulsion"},
        "Thermal Radiators (Panel Surface)": {"opt": 5.0, "base": 6.75, "pess": 10.0, "cat": "Thermal"},
        "Radiator Deployment & Booms": {"opt": 12.0, "base": 20.0, "pess": 30.0, "cat": "Thermal"},
        "ECLSS Hardware & Closed-Loop Recycling": {"opt": 20.0, "base": 30.0, "pess": 45.0, "cat": "Habitation"},
        "Avionics, Computing & Optical Bus": {"opt": 6.0, "base": 10.0, "pess": 15.0, "cat": "Avionics"},
        "GNC, Reaction Control System & Wheels": {"opt": 12.0, "base": 18.0, "pess": 25.0, "cat": "Avionics"},
        "Communications & Deep-Space Lasers": {"opt": 4.0, "base": 6.0, "pess": 10.0, "cat": "Comms"},
        "Crew Accommodations, Quarters & Medical": {"opt": 18.0, "base": 25.0, "pess": 35.0, "cat": "Habitation"},
        "Centrifuge System & Magnetic Bearings": {"opt": 15.0, "base": 22.0, "pess": 32.0, "cat": "Habitation"},
        "Scientific Payload, Probes & Exobiology Labs": {"opt": 25.0, "base": 40.0, "pess": 60.0, "cat": "Payload"},
        "Landing & Return Hardware / Landers": {"opt": 15.0, "base": 25.0, "pess": 40.0, "cat": "Payload"},
        "Docking, Berthing & Servicing Hardware": {"opt": 8.0, "base": 12.0, "pess": 18.0, "cat": "Structure"},
        "Defensive MMOD Whipple Shielding": {"opt": 12.0, "base": 20.0, "pess": 30.0, "cat": "Defense"},
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
    # Baseline Mission B (Earth-Mars-Earth): 2,200 MT LH2 for NTP + 300 MT LNH3/Argon for NEP
    propellant_base = 2500.0
    propellant_opt = 1800.0
    propellant_pess = 3500.0

    wet_mass_opt = dry_mass_opt + propellant_opt
    wet_mass_base = dry_mass_base + propellant_base
    wet_mass_pess = dry_mass_pess + propellant_pess

    print("=== USS ENTERPRISE X - MASS BUDGET V2 SUMMARY (RECONCILED) ===")
    print(f"Subtotal Dry (Unmargined): Opt={subtotal_opt:.2f} t | Base={subtotal_base:.2f} t | Pess={subtotal_pess:.2f} t")
    print(f"Reserve Growth Margin (20%): Opt={margin_opt:.2f} t | Base={margin_base:.2f} t | Pess={margin_pess:.2f} t")
    print(f"TOTAL DRY MASS:            Opt={dry_mass_opt:.2f} t | Base={dry_mass_base:.2f} t | Pess={dry_mass_pess:.2f} t")
    print(f"Main Propellant Mass:      Opt={propellant_opt:.2f} t | Base={propellant_base:.2f} t | Pess={propellant_pess:.2f} t")
    print(f"GROSS DEPARTURE WET MASS:  Opt={wet_mass_opt:.2f} t | Base={wet_mass_base:.2f} t | Pess={wet_mass_pess:.2f} t")

    return {
        "subsystems": subsystems,
        "subtotal_opt": subtotal_opt,
        "subtotal_base": subtotal_base,
        "subtotal_pess": subtotal_pess,
        "dry_mass_base": dry_mass_base,
        "wet_mass_base": wet_mass_base
    }

if __name__ == "__main__":
    calculate_mass_budget()
