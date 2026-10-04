# 62 — Mars ISRU Engineering Closure Analysis v1

**Document ID:** `62-mars-isru-closure-v1.md`
**Calculation Engine Source:** `engineering/calculations/mars_isru.py`
**Program Phase:** Phase 8.1 — Mars ISRU, Propellant Logistics & Physical Mission Closure (Remediated)
**Program Status:** **ENGINEERINGALLY CONDITIONAL (Status Assignment: B — MARS ISRU CONDITIONALLY CLOSED)**

---

## 1. Executive Summary & Core Conclusion

`62-mars-isru-closure-v1.md` delivers the canonical engineering closure evaluation for manufacturing return-mission propellant on Mars for USS Enterprise X (Project Occam-7).

Following full first-principles chemical, thermodynamic, power, thermal, structural, multi-lander payload, and timeline integration:

### Primary Decision Gate Outcome:
> **STATUS B — MARS ISRU CONDITIONALLY CLOSED (`ENGINEERINGALLY CONDITIONAL`)**

The physics, mass conservation, stoichiometry, and thermodynamic energy balances **close quantitatively**. However, physical mission closure strictly mandates transitioning from onboard crewed ISRU (Architecture A) to a **Precursor Autonomous Robotic ISRU Depot (Architecture B - 2x 150t Landers)** pre-deployed 1–2 synodic cycles before crew departure from Earth.

---

## 2. Reconciled Return Propellant Mass Accounting

To execute the return trajectory (Trans-Earth Injection $\Delta v = 1.80\text{ km/s}$ + Earth Orbit Capture $\Delta v = 3.85\text{ km/s}$ or Hohmann reserve), USS Enterprise X requires $2,200.00\text{ MT}$ of net usable Liquid Hydrogen ($\text{LH}_2$).

Accounting for all physical process losses, storage boiloff, flash evaporation during transfer, unusable tank ullage, and mandatory AIAA contingency reserves:

| Propellant Accounting Parameter | Mass Value | Unit | Basis / First-Principles Derivation |
| :--- | ---:| :---: | :--- |
| **Net Usable TEI $\text{LH}_2$ Requirement** | $2,200.00$ | $\text{MT}$ | Nominal NTP main impulse inventory for Earth return |
| **Mars Surface-to-Orbit Ascent Propellant** | $45.00$ | $\text{MT}$ | MAV RCS & impulse reserve |
| **Trajectory Correction Maneuvers (TCM)** | $25.00$ | $\text{MT}$ | Deep-space midcourse corrections ($\Delta v = 30\text{ m/s}$) |
| **Emergency Abort Reserve** | $50.00$ | $\text{MT}$ | Fast-return contingency reserve |
| **Net Usable Propellant Subtotal** | **2,320.00** | $\text{MT}$ | Unmargined required inventory |
| **Chemical Production Losses ($2.0\%$)** | $46.40$ | $\text{MT}$ | Catalytic purge, filter backwash, deoxo venting |
| **Surface ZBO Storage Boiloff ($1.5\%$)** | $34.80$ | $\text{MT}$ | Passive MLI ingress during 500-day storage |
| **Line Transfer & Chilldown Losses ($1.0\%$)** | $23.20$ | $\text{MT}$ | Line chilldown and quick-disconnect purge |
| **Flash Evaporation / Tank Filling ($1.5\%$)** | $34.80$ | $\text{MT}$ | Tank wall initial thermal equilibrium flash loss |
| **Unusable Trapped Residuals ($1.0\%$)** | $23.20$ | $\text{MT}$ | Sump trapped liquid & tank wall wetting |
| **Unusable Bottom Tank Ullage ($1.0\%$)** | $23.20$ | $\text{MT}$ | NPSH pump margin & ullage gas fraction |
| **Plant Startup & Purge Cycles ($1.0\%$)** | $23.20$ | $\text{MT}$ | Commissioning cycling and filter purges |
| **AIAA Contingency Reserve ($10.0\%$)** | $232.00$ | $\text{MT}$ | Mandatory growth and operational reserve |
| **Gross $\text{LH}_2$ Manufacturing Demand** | **2,760.80** | $\text{MT}$ | Total required hydrogen production on Mars surface |
| **Gross Byproduct $\text{O}_2$ Yield** | **21,911.59** | $\text{MT}$ | Stoichiometric oxygen byproduct ($8.9367\text{ kg H}_2\text{O} / \text{kg H}_2$) |

---

## 3. Martian Feedstock Evaluation & Mass Balances

Three candidate Martian hydrogen feedstocks were evaluated using first-principles chemical process models:

### A. Glacial Water Ice (Mantle / Surface Ice Sheet @ 50% Mass Fraction) — PREFERRED
* **Stoichiometry:** $1\text{ kg H}_2 = 8.9367\text{ kg H}_2\text{O}$
* **Extraction & Purification Yield:** $\eta_{extract} = 0.95$, $\eta_{purify} = 0.98$ ($\text{net } \eta = 93.1\%$)
* **Pure Water Requirement:** $24,672.39\text{ MT } \text{H}_2\text{O}$
* **Raw Extracted Water:** $26,500.96\text{ MT } \text{H}_2\text{O}$
* **Total Regolith/Ice Excavated:** **$53,001.92\text{ MT}$** ($19.20\text{ kg regolith/ice per kg LH}_2$)

### B. Hydrated Minerals (Smectite / Polyhydrated Sulfates @ 5% Bound Water) — INFEASIBLE
* **Thermal Calcination Requirement:** Heating clay to $600^\circ\text{C}$ requires $1.85\text{ kWh/kg H}_2\text{O}$
* **Regolith Excavated:** **$616,809.84\text{ MT}$** ($223.42\text{ kg regolith per kg LH}_2$)
* **Thermal Energy Consumption:** $57,054.91\text{ MWh}$ thermal energy
* **Verdict:** **INFEASIBLE** (Requires $11.6 \times$ more excavation and excessive thermal power).

### C. Atmospheric $\text{CO}_2$ Processing (Sabatier Methane + Water) — COMPLEMENTARY
* **Reaction:** $\text{CO}_2 + 4\text{H}_2 \rightarrow \text{CH}_4 + 2\text{H}_2\text{O}$
* **$\text{CO}_2$ Processed:** $15,068.04\text{ MT}$
* **$\text{CH}_4$ Yield:** $5,492.66\text{ MT}$
* **Verdict:** **COMPLEMENTARY** for surface-to-orbit ascent rockets ($\text{CH}_4/\text{LOX}$), but does NOT supply pure $\text{LH}_2$ for NTP without water extraction.

---

## 4. First-Principles Energy & Power Derivation

The electrical energy required for hydrogen production and liquefaction is derived directly from chemical thermodynamics:

### A. Water Electrolysis (Solid Oxide Electrolyzer Cell — SOEC @ 72% Efficiency):
$$\Delta H^0_{HHV} = 285.83\text{ kJ/mol} = 39.39\text{ kWh/kg H}_2$$
$$E_{SOEC} = \frac{39.39\text{ kWh/kg}}{0.72} = \mathbf{54.71\text{ kWh/kg H}_2}$$

### B. Auxiliary Process Energy Requirements (per kg $\text{LH}_2$):
* Thermal Ice Heating/Melting ($210\text{ K} \rightarrow 373\text{ K}$): $0.65\text{ kWh/kg}$
* Water Purification & Distillation: $0.30\text{ kWh/kg}$
* Gas Drying & Compression ($30\text{ bar}$): $1.40\text{ kWh/kg}$
* Mining & Excavation Machinery: $1.80\text{ kWh/kg}$
* Pumps, HVAC & Controls: $1.15\text{ kWh/kg}$

### C. Hydrogen Liquefaction & Ortho-Para Conversion:
* Carnot Minimum Work ($300\text{ K} \rightarrow 20.28\text{ K}$): $W_{min} = 3.91\text{ kWh/kg}$
* Claude-Cycle Real Efficiency ($25.0\%$ Carnot): $15.64\text{ kWh/kg}$
* Ortho-to-Para Conversion Heat Removal ($703\text{ kJ/kg}$ @ $25\%$ Carnot): $0.78\text{ kWh/kg}$
* Total Liquefaction Energy: $\mathbf{16.42\text{ kWh/kg LH}_2}$

### D. Total Specific Electrical Demand:
$$E_{total} = 54.71 + 0.65 + 0.30 + 1.40 + 1.80 + 16.42 + 1.15 = \mathbf{76.42\text{ kWh/kg LH}_2}$$

### E. Campaign Power Demand (500-Day Campaign):
* Total Campaign Electrical Energy: **$210,990.64\text{ MWh}$** ($210.991\text{ GWh}$)
* Process Continuous Electrical Power: **$17.58\text{ MWe}$**
* Total Gross Surface Power Demand (incl. Aux, ZBO, Habitat, Margin): **$20.63\text{ MWe}$ Average / $24.42\text{ MWe}$ Peak**

---

## 5. Industrial Equipment Processing Rates & Multi-Lander Delivery Architecture

To manufacture $2,760.80\text{ MT}$ of $\text{LH}_2$ over a 500-day surface campaign:

* **Daily $\text{LH}_2$ Production Rate:** $5,521.60\text{ kg LH}_2/\text{day}$ ($230.07\text{ kg/hour}$)
* **Daily Water Extraction Rate:** $53.00\text{ MT water/day}$ ($2,208.40\text{ kg/hour}$)
* **Daily Regolith Excavation Rate:** $106.00\text{ MT regolith/day}$ ($4,416.80\text{ kg/hour}$)
* **Mining Fleet Sizing:** 2x $2.5\text{-tonne}$ autonomous excavators operating at $50\%$ duty cycle ($2,208\text{ kg/hour}$ per robot).

### Resolved Precursor Delivery Architecture (2x Heavy Cargo Landers @ 150t capacity = 300t total):
* **Total Plant Dry Mass:** $256.29\text{ MT}$ (includes $108.17\text{ MT}$ radiators)
* **Lander 1 Payload:** Power Plant ($28.50\text{ t}$) + Radiators ($108.17\text{ t}$) + Controls ($8.33\text{ t}$) = **$145.00\text{ MT}$** (Margin: $+5.00\text{ MT}$)
* **Lander 2 Payload:** Mining, Processing, Liquefaction, Storage Depot & Spares = **$111.29\text{ MT}$** (Margin: $+38.71\text{ MT}$)
* **Total Precursor Delivery Margin:** **$+43.71\text{ MT}$** (Hard Deployability Gate: `PASSED`)
