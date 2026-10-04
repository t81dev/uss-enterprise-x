# 21 — Integrated System Budget v2 (Reconciled)

**Document ID:** `21-system-budget-v2.md`
**Baseline Vehicle Class:** Deep-Space Exploration Vessel (USS Enterprise X)
**Nominal Crew Complement:** 24 crew members
**Autonomous Operations Horizon:** 1,000 days
**Primary Propulsion Baseline:** Hybrid Dual-Mode NTP (High-Thrust TMI/TEI) + NEP (High-Efficiency Cruise)

---

## 1. Integrated System Mass Budget (Bottom-Up Reconciled)

This bottom-up mass budget incorporates all structural stiffening, 6.5mm pressure tank skin thickness ($\sigma_\theta = 138.5\text{ MPa}$ @ $150\text{ kPa}$ operating pressure), multi-layer shielding, expanded centrifuge dynamic bearings, and ECLSS management hardware required following the forensic audit. Every row now sums to the unmargined subtotal exactly.

| Component Subsystem | Optimistic (MT) | Baseline (MT) | Pessimistic (MT) | Unit | First-Principles Derivation / Basis | Confidence | Class |
|---|---:|---:|---:|---|---|---|---|
| **Primary Structure & Spine Truss** | 140.0 | 210.0 | 300.0 | MT | $380\text{m}$ welded 316L SS space frame ($4000\text{ kN}$ thrust load) | High | B |
| **Pressure Hull (Hab & Labs)** | 90.0 | 135.0 | 180.0 | MT | $8\text{m} \times 30\text{m}$ cylindrical pressure shell ($0.8\text{ atm}$ $N_2/O_2$) | High | A |
| **Main Propellant Tanks (Dry Hull 6.5mm)** | 115.0 | 178.75 | 240.0 | MT | $12\text{m} \times 310\text{m}$ SS 316L pressure tanks ($6.5\text{mm}$ skin, $150\text{ kPa}$) | High | A |
| **Passive Radiation Shielding (SPE/GCR)** | 160.0 | 240.0 | 320.0 | MT | Multi-layer storm shelter ($73.1\text{ t}$) + circumferential tanks ($154.6\text{ t}$) | High | B |
| **Nuclear Reactor Core & Conversion** | 20.0 | 30.0 | 45.0 | MT | 100 MWth / 20 MWe Fast Fission Core + Brayton Turbines | Medium | B |
| **Reactor Shadow Shielding** | 30.0 | 45.0 | 65.0 | MT | Tungsten / $B_4C$ / $LiH$ conical shadow shield ($380\text{m}$ offset) | High | B |
| **Propulsion Engines (4x NTP + MPD)** | 25.0 | 40.0 | 60.0 | MT | 4x Solid-Core NTP ($32\text{ t}$) + 4x MW MPD Thruster Arrays ($8\text{ t}$) | Medium | B |
| **Thrust Vector & Gimbals** | 10.0 | 15.0 | 25.0 | MT | Heavy hydraulic gimbals + thrust cone assembly | High | A |
| **Thermal Radiators (Panel Surface)** | 5.0 | 6.75 | 10.0 | MT | $2,502.8\text{ m}^2$ NaK/Water heat pipe array ($1.8\text{ kg/m}^2$) | High | B |
| **Radiator Deployment & Booms** | 12.0 | 20.0 | 30.0 | MT | Deployable mechanical booms, manifolds & coolant fluid | Medium | B |
| **ECLSS Hardware & Recycling Plant** | 20.0 | 30.0 | 45.0 | MT | Sabatier + VCD + Catalytic Oxidizer + Sludge Processor | High | A |
| **Avionics, Computing & Radar/LiDAR** | 6.0 | 10.0 | 15.0 | MT | TMR rad-hard optical computing buses + navigation sensors | High | A |
| **GNC & Reaction Control System** | 12.0 | 18.0 | 25.0 | MT | Distributed cold gas / monopropellant thrusters & wheels | High | A |
| **Deep-Space Communications Array** | 4.0 | 6.0 | 10.0 | MT | 100W Deep-space optical laser transceivers + RF dishes | High | A |
| **Crew Accommodations & Quarters** | 18.0 | 25.0 | 35.0 | MT | Modular bunks, galley, gym, medical bay & hygiene facilities | High | A |
| **Artificial Gravity Centrifuge System** | 15.0 | 22.0 | 32.0 | MT | $15\text{m}$ dia transverse ring, magnetic bearings & counter-weight | Medium | B |
| **Scientific Payload & Exobiology Labs** | 25.0 | 40.0 | 60.0 | MT | Mass spectrometers, sub-surface drill, optical telescopes | High | A |
| **Landing & Return Hardware / Landers** | 15.0 | 25.0 | 40.0 | MT | Autonomous surface landing craft / excursion module | Medium | B |
| **Docking & Robotic Servicing Arms** | 8.0 | 12.0 | 18.0 | MT | Dual RMS manipulators, APAS docking mechanisms | High | A |
| **Defensive MMOD Whipple Shielding** | 12.0 | 20.0 | 30.0 | MT | Stuffed Nextel/Kevlar Whipple bumper shields | High | B |
| **Maintenance Inventory & Cassettes** | 15.0 | 25.0 | 40.0 | MT | Spare turbopumps, computer cores, valves, printed stock | High | A |
| **1,000-Day Net Consumables** | 60.0 | 72.3 | 90.0 | MT | Net dry rations, $O_2$, $N_2$, medical, hygiene & water makeup | High | A |
| **UNMARGINED SUBTOTAL DRY MASS** | **817.0** | **1,225.80** | **1,715.0** | **MT** | Reconciled exact sum of all dry hardware rows | **High** | **B** |
| **AIAA Reserve Growth Margin (20%)** | 163.4 | 245.16 | 343.0 | MT | System growth contingency ($20\% \times \text{subtotal}$) | High | B |
| **TOTAL VEHICLE DRY MASS ($M_{dry}$)** | **980.4** | **1,470.96** | **2,058.0** | **MT** | Fully assembled dry vehicle baseline | **High** | **B** |

---

## 2. Propellant & Wet Departure Mass

| Propellant Category | Optimistic (MT) | Baseline (MT) | Pessimistic (MT) | Primary Allocation & Function |
|---|---:|---:|---:|---|
| **Liquid Hydrogen ($\text{LH}_2$)** | 1,600.0 | 2,200.0 | 3,100.0 | Main NTP Impulse propellant ($I_{sp} = 900\text{ s}$) |
| **Liquid Ammonia ($\text{LNH}_3$) / Argon** | 200.0 | 300.0 | 400.0 | NEP MPD Cruise propellant ($I_{sp} = 3,500\text{ s}$) |
| **RCS Hydrazine / Cold Gas** | 15.0 | 25.0 | 35.0 | Attitude control & fine precision maneuvering |
| **TOTAL PROPELLANT MASS ($M_{prop}$)** | **1,815.0** | **2,525.0** | **3,535.0** | Total mission propellant load |
| **NOMINAL MISSION DEPARTURE MASS ($M_{dep}$)** | **2,795.4** | **3,995.96** | **5,593.0** | Reconciled departure mass ($M_{dry} + M_{prop}$) |
| **MAXIMUM GROSS DESIGN LIMIT** | **3,000.0** | **4,500.0** | **6,000.0** | Structural limit for main spine space frame |

---

## 3. Mass Distribution & Physical Balance

1. **Mass Dominance:** Propellant accounts for $63.2\%$ of the $3,995.96\text{ MT}$ departure wet mass. Dry mass ($1,470.96\text{ MT}$) represents $36.8\%$ of the departure vehicle.
2. **Structural Integrity:** Primary structure ($210\text{ MT}$) and propellant tanks ($178.75\text{ MT}$) form $31.7\%$ of unmargined dry mass, ensuring a structural safety factor of $1.59$ on tank hoop stress under $150\text{ kPa}$ operating pressure and $\ge 9.95$ axial safety factor under $4,000\text{ kN}$ NTP acceleration ($0.10\text{ g}$ wet, $0.27\text{ g}$ dry).
3. **Shielding Fraction:** Passive radiation shielding ($240\text{ MT}$) and reactor shadow shielding ($45\text{ MT}$) sum to $285\text{ MT}$ ($23.2\%$ of unmargined dry mass), providing multi-layer SPE storm shelter ($52.25\text{ g/cm}^2$) and reactor isolation.
