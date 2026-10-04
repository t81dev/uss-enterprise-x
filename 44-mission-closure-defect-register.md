# 44 — Mission Closure Defect Register

**Document ID:** `44-mission-closure-defect-register.md`
**Program Phase:** Mission-Level Physics Closure / Digital Twin Phase (Project Occam-7)
**Status:** ACTIVE AUDIT & RECONCILIATION

---

## 1. Executive Summary

This Master Defect Register documents inconsistencies, uncoupled physical parameters, unphysical trajectory assumptions, and testing discrepancies identified during the transition from static subsystem budget verification to full sequential mission digital twin modeling.

While previous phase audits (documented in `40-post-merge-defect-register.md`) resolved individual subsystem arithmetic errors (such as tank wall hoop stress and uncoupled electric power-thrust relationships), the vehicle remained evaluated through isolated, static spreadsheet calculations.

This register identifies mission-level physical disconnects that invalidate claims of system closure until resolved through continuous numerical integration across the complete mission lifecycle.

---

## 2. Master System Parameter Canonical Definitions

To eliminate baseline ambiguity across all project documentation and analytical scripts, the following canonical mass definitions are formally established:

| Parameter Category | Canonical Symbol | Value | Unit | Definition & Scope |
| :--- | :---: | ---:| :---: | :--- |
| **Unmargined Hardware Subtotal** | $M_{sub}$ | **1,225.80** | MT | Reconciled exact sum of all 22 itemized dry hardware subsystem rows. |
| **AIAA Growth Reserve Margin (20%)** | $M_{margin}$ | **245.16** | MT | Mandatory $20\%$ growth reserve contingency ($0.20 \times M_{sub}$). |
| **Total Vehicle Dry Mass** | $M_{dry}$ | **1,470.96** | MT | Fully margined dry structural baseline ($M_{sub} + M_{margin}$). |
| **NTP Impulse Propellant ($\text{LH}_2$)** | $M_{NTP}$ | **2,200.00** | MT | Main nuclear thermal rocket propellant allocation ($I_{sp} = 900\text{ s}$). |
| **NEP Cruise Propellant ($\text{LNH}_3/\text{Ar}$)** | $M_{NEP}$ | **300.00** | MT | Continuous electric propulsion propellant allocation ($I_{sp} = 3,500\text{ s}$). |
| **Total Mission Propellant Inventory** | $M_{prop}$ | **2,500.00** | MT | Sum of main propulsion inventories ($M_{NTP} + M_{NEP}$). |
| **RCS Reaction Control Allocation** | $M_{RCS}$ | **25.00** | MT | Fine attitude control / precision maneuvering (included in dry consumables/GNC hardware budget). |
| **Gross Departure Wet Mass** | $M_{dep}$ | **3,970.96** | MT | Total LEO departure mass baseline ($M_{dry} + M_{prop}$). |
| **Maximum Structural Design Limit** | $M_{max\_limit}$ | **4,500.00** | MT | Maximum allowable spine truss load rating. |

---

## 3. Mission Closure Defect Register Matrix

| Defect ID | Severity | Affected Subsystems / Files | Defect Description | Physical / Quantitative Root Cause | Corrective Action / Resolution | Status |
| :--- | :---: | :--- | :--- | :--- | :--- | :---: |
| **DEF-M01** | **P1** | `21-system-budget-v2.md`, `25-mission-performance-v1.md`, `42-system-reference-model-v2.md`, `mass_budget.py` | Departure mass disagreement between $3,970.96\text{ MT}$ and $3,995.96\text{ MT}$. | In `21-system-budget-v2.md` and `25-mission-performance-v1.md`, an extra $25\text{ t}$ RCS allocation was added on top of $2,500\text{ t}$ mission propellant ($2200\text{t} + 300\text{t} + 25\text{t} = 2,525\text{t}$), double-counting RCS consumables already accounted for in GNC/consumables dry budgets. `42-system-reference-model-v2.md` used $3,970.96\text{ MT}$. | Canonical baseline updated to $M_{dep} = 3,970.96\text{ MT}$ ($1,470.96\text{ t Dry} + 2,500.0\text{ t Propellant}$). Reconciled Table 2 in `21-system-budget-v2.md` and `25-mission-performance-v1.md`. | **RESOLVED** |
| **DEF-M02** | **P0** | `engineering/calculations/mission_deltav.py`, `engineering/calculations/test_system_consistency.py` | NEP trajectory verification evaluated continuous electric burn against artificial reduced mass ($M_{dry} + 300\text{ t} = 1,771\text{ t}$) instead of actual sequential vehicle mass state. | NEP burn calculation assumed the vehicle was lightweight ($1,771\text{ t}$) during outbound cruise, ignoring the $2,200\text{ t}$ of NTP $\text{LH}_2$ propellant still onboard prior to Mars Orbit Insertion (MOI). | Rebuild trajectory integration in `mission_digital_twin.py` using sequential vehicle mass state ($M_{t}$ drops dynamically as propellant burns). Update test suite to evaluate NEP at actual sequential mass points (Departure, Post-TMI, Post-MOI, Inbound). | **RESOLVED** |
| **DEF-M03** | **P1** | `25-mission-performance-v1.md`, `mission_deltav.py` | Fixed target $\Delta v$ values ($3.8\text{ km/s}$ TMI, $2.1\text{ km/s}$ MOI, $1.8\text{ km/s}$ TEI, $1.2\text{ km/s}$ EOI) assigned to NTP phases without verifying actual burn duration and propellant mass flow integration. | Target $\Delta v$ values were treated as unvarying constants rather than outputs of rocket equation integration ($\Delta v = \int F(t)/m(t) dt$) acting on finite $2,200\text{ t}$ $\text{LH}_2$ inventory. | Recompute NTP burn profiles sequentially using $\dot{m} = F / (I_{sp} g_0) = 453.208\text{ kg/s}$. Derive actual $\Delta v$ generated per burn and track remaining $\text{LH}_2$ inventory across all 4 NTP phases. | **RESOLVED** |
| **DEF-M04** | **P1** | `22-power-budget-v2.md`, `23-thermal-budget-v2.md`, `49-mission-thermal-profile.md` | Thermal and electrical power loads evaluated only at steady-state cruise, neglecting transient thermal spikes during NTP high-power engine operation and multi-megawatt propulsion conditioning. | During NTP engine operation ($4,000\text{ kN}$ total thrust), reactor/turbopump thermal dynamics and house electrical loads differ significantly from $15\text{ MWe}$ NEP cruise mode. | Implement a dynamic power-thermal state machine (`50-power-state-machine.md` and `49-mission-thermal-profile.md`) tracking power generation, distribution, and thermal rejection across all operational modes. | **RESOLVED** |
| **DEF-M05** | **P2** | `engineering/calculations/test_system_consistency.py` | Automated test suite verified static mathematical identities but lacked sequential state transition tests, edge-case checks, and property-based validation for propulsion degradation or failures. | Unit tests passed on hardcoded equation checks without testing whether the spacecraft could execute a continuous sequence from Earth departure to Earth return. | Expand `test_system_consistency.py` to include sequential mission trajectory tests (Tests A–E), property-based bounds (zero propellant, engine failure, degraded reactor/radiator), and dynamic state transitions. | **RESOLVED** |

---

## 4. Verification & Defect Resolution Audit Standard

All defects listed in this register must be systematically corrected in both documentation and underlying executable calculation models:
1. Canonical mass definitions ($M_{dry} = 1,470.96\text{ t}$, $M_{prop} = 2,500.00\text{ t}$, $M_{dep} = 3,970.96\text{ t}$) applied everywhere without exception.
2. Sequential state propagation implemented in `engineering/calculations/mission_digital_twin.py`.
3. Mission digital twin JSON output generated and validated (`engineering/calculations/mission_baseline.json`).
4. Unit tests in `test_system_consistency.py` passing cleanly for all expanded test cases.
