# 20 — Quantitative Forensic Audit v1

**Document ID:** `20-quantitative-forensics.md`
**Purpose:** Rigorous numerical audit and physical verification of all quantitative claims across v1 baseline documents
**Scope:** `17-system-budget-v1.md`, `18-hull-architecture-trade.md`, `19-failure-analysis-v1.md`, `03-propulsion.md`, `04-power-and-thermal.md`, `05-hull-structure.md`, `06-habitation.md`, `11-mission-profile.md`, `12-economics.md`, `16-architecture-audit.md`

---

## 1. Forensics Methodology

Every numerical claim in the Project Occam-7 v1 baseline was evaluated against first-principles physics and dimensional analysis using eight core questions:
1. What physical equation supports it?
2. What inputs are required?
3. What assumptions are hidden?
4. What unit system is being used?
5. Is the result dimensionally correct?
6. Is the result consistent with neighboring subsystems?
7. Does the result close the total vehicle budget?
8. What is the confidence level and what makes the number wrong by $2\times$, $5\times$, or $10\times$?

---

## 2. Quantitative Forensic Audit Table

| Parameter | Current Value | Unit | Source | Equation / Basis | Confidence | Problem / Audit Finding |
|---|---:|---|---|---|---|---|
| **Radiator Surface Area v1** | 12,000 / 11,160 | $\text{m}^2$ | `17-system-budget-v1` §4 | $q = \epsilon \sigma T^4$ | Low | **Thermodynamic Error / Double Counting:** Claims $11,160\text{ m}^2$ panel area for $83.4\text{ MWth}$ waste heat at $850\text{ K}$. At $850\text{ K}$, flux is $26.6\text{ kW/m}^2$. Double-sided emission gives $53.2\text{ kW/m}^2$. Required total one-sided panel area for $83.4\text{ MWth}$ is actually $\sim 1,727\text{ m}^2$ (with $15\%$ margin $\approx 2,500\text{ m}^2$). $11,160\text{ m}^2$ overstates radiator area by $>4.4\times$, adding unnecessary structural dry mass. |
| **Reactor Thermal to Electric Conversion** | 20 / 100 | $\text{MWe} / \text{MWth}$ | `17-system-budget-v1` §1,4 | $\eta = P_{el} / Q_{th} = 0.20$ | High | **Missing Heat Accounting:** $100\text{ MWth}$ core at $20\%$ Brayton efficiency generates $20\text{ MWe}$ electrical and $80\text{ MWth}$ waste heat. However, `17-system-budget-v1` Table 4 lists $80\text{ MWth}$ reactor heat + $3.0\text{ MWth}$ conversion loss, summing to $83.39\text{ MWth}$. The $3\text{ MW}$ NEP conversion loss was calculated on $15\text{ MWe}$ input, but total reactor waste heat is strictly $80\text{ MWth}$. |
| **NEP Power Demand vs Available Power** | 15,000 | $\text{kWe}$ | `17-system-budget-v1` §2 | Subsystem sum | Medium | **Power Budget Contradiction:** NEP demand ($15.0\text{ MWe}$) + Peak non-propulsive household load ($1.335\text{ MWe}$) = $16.335\text{ MWe}$. Available power from 20 MWe generator leaves only $3.665\text{ MWe}$ margin. While mathematically closed under peak, transient active defense ($2.0\text{ MWe}$) + manufacturing ($0.2\text{ MWe}$) exceeds 20 MWe total core capacity during NEP thrusting. |
| **Main Propellant Tank Volume vs Mass** | 35,000 | $\text{m}^3$ | `17-system-budget-v1` §5 | $V = m / \rho$ | Medium | **Density / Volume Inconsistency:** Liquid Hydrogen ($\text{LH}_2$) density is $\sim 71\text{ kg/m}^3$. A $35,000\text{ m}^3$ tank holds $2,485\text{ MT}$ of $\text{LH}_2$. `17-system-budget-v1` specifies $2,500\text{ MT}$ propellant. The volume is correct for $\text{LH}_2$, but tank dry mass of $65\text{ MT}$ ($12\text{m} \text{ dia} \times 310\text{m} \text{ length}$) is severely underestimated for a $380\text{m}$ pressure skin ($<1.8\text{ mm}$ wall thickness), violating buckling limits. |
| **Primary Structure & Spine Dry Mass** | 180 | MT | `17-system-budget-v1` §1 | Beam bending / shell model | Low | **Optimistic Mass Assumption:** A $380\text{m}$ stainless steel truss spine subjected to 4,000 kN thrust, tank hydrostatic loads, and radiator cantilever moments requires $>210\text{ MT}$ to meet structural yield and buckling safety margins ($>1.5\times$). |
| **Centrifuge Artificial Gravity Parameters** | 12m dia / 10 RPM | $\text{m} / \text{RPM}$ | `18-hull-architecture-trade` §5 | $a = \omega^2 r$ | High | **Physiological / Motion Error:** Radius $r = 6.0\text{ m}$, $\omega = 1.047\text{ rad/s}$. $a = (1.047)^2 \times 6 = 6.58\text{ m/s}^2 = 0.67\text{ g}$. Tangential speed $v = 6.28\text{ m/s}$. Walking prograde at $1.5\text{ m/s}$ increases $v$ to $7.78\text{ m/s}$, producing $a = 10.08\text{ m/s}^2 = 1.03\text{ g}$ ($+54\%$ surge). Walking retrograde drops $a$ to $3.81\text{ m/s}^2 = 0.39\text{ g}$ ($-42\%$). Coriolis cross-coupling ($a_{cor} = 3.14\text{ m/s}^2$) causes severe motion sickness. $6\text{m}$ radius is too small for $10\text{ RPM}$ human habitability. |
| **Radiation Shielding Thickness & Mass** | 220 MT / 25 $g/cm^2$ | MT / $\text{g/cm}^2$ | `17-system-budget-v1` §1, `18` §5 | Column density $\rho t$ | Medium | **Missing Heavy Ion (GCR) Protection:** $25\text{ g/cm}^2$ water provides adequate protection against Solar Particle Events (SPE, $<100\text{ MeV}$ protons), reducing SPE dose to safe levels. However, Galactic Cosmic Rays (GCR, $>1\text{ GeV/nucleon}$ HZE ions) require $>100\text{ g/cm}^2$ or active magnetic deflection for 1,000-day missions. Ambient GCR dose remains $\sim 450\text{ mSv/yr}$, exceeding NASA career limits ($600\text{ mSv}$). |
| **NTP Engine Thrust & Mass** | 4x Solid Core | MT | `17-system-budget-v1` §1 | $T = \dot{m} I_{sp} g_0$ | Low | **Uncalculated Engine Feed Infrastructure:** 4x NTP engines ($50\text{ MT}$ total) do not account for turbopumping hardware, liquid hydrogen feed lines running $300\text{m}$ along the spine, boil-off zero-loss cryocoolers ($+15\text{ MT}$), or thrust vector control gimbals ($+8\text{ MT}$). |
| **ECLSS Mass & Resupply Rates** | 25 MT / 72.3 MT | MT | `17-system-budget-v1` §1,6 | ISS scaling + Sabatier | High | **Missing Solid Waste / Salt Disposal Mass:** $98\%$ water recovery assumes urine distillation, but solids/salt residue ($0.15\text{ kg/person/day} = 3.6\text{ kg/day}$) produces $3,600\text{ kg}$ of hazardous toxic sludge over 1,000 days. No mass or storage volume allocated in v1. |
| **"Sub-Billion Dollar Vehicle" Claim** | < $1.0B | USD | `12-economics.md` §3 | Rule-of-thumb projection | Unrated | **Unsupported Economic Assertion:** Unsubstantiated by manufacturing bill-of-materials, tooling, launch mass cadence, or flight qualification costs. Rebuilt in `32-manufacturing-system-v1.md`. |

---

## 3. Critical Failure & Contradiction Summary

1. **Thermodynamic Radiator Sizing Error:** The v1 budget specified $11,160\text{ m}^2$ of radiators, confusing double-sided radiating surface with one-sided panel footprint area and neglecting the $T^4$ radiance at $850\text{ K}$. Correcting this reduces radiator dry footprint to $\sim 2,500\text{ m}^2$ and dry radiator mass from $40\text{ MT}$ to $\sim 6.66\text{ MT}$ (plus $20.0\text{ MT}$ deployment/coolant hardware = $26.66\text{ MT}$ total thermal system mass).
2. **Centrifuge Motion Sickness Limit:** The $12\text{m}$ diameter ($6\text{m}$ radius) centrifuge operating at $10\text{ RPM}$ violates human habitability limits due to a $100\%$ Coriolis gravity fluctuation between prograde and retrograde walking. The radius must be expanded to $\ge 15\text{m}$ or replaced with end-mass tether rotation.
3. **Propellant Tank Buckling & Cryogenic Plumbing:** The $310\text{m}$ long propellant tank skin ($65\text{ MT}$) was modeled purely as a tension pressure vessel without considering compressive thrust loads ($4,000\text{ kN}$) from the aft NTP engines, leading to severe structural buckling risk unless stiffened with internal ring frames ($+45\text{ MT}$).
4. **GCR vs SPE Radiation Protection:** v1 treated SPE and GCR radiation as a single shielding problem. SPE requires localized thick hydrogenous shielding ($>45\text{ g/cm}^2$) during solar flares, while GCR requires broad circumferential mass or fast transit profiles.
