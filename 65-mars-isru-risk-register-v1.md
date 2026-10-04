# 65 — Mars ISRU Failure Modes & Risk Register v1

**Document ID:** `65-mars-isru-risk-register-v1.md`
**Calculation Engine Source:** `engineering/calculations/mars_isru.py`
**Program Phase:** Phase 8 — Mars ISRU, Propellant Logistics & Physical Mission Closure
**Program Status:** **ENGINEERINGALLY CONDITIONAL (Risk Matrix & Mitigations Defined)**

---

## 1. Executive Summary

`65-mars-isru-risk-register-v1.md` provides a comprehensive failure mode effects and criticality analysis (FMECA) for the Mars In-Situ Resource Utilization (ISRU) propellant manufacturing plant supporting USS Enterprise X.

Under **Architecture B (Precursor Autonomous Robotic ISRU Depot)**, failure modes are categorized into critical operational hazards that affect production throughput, equipment availability, power generation, thermal rejection, and propellant storage.

The primary risk mitigation strategy is **precursor verification prior to crew launch**: crew departure from Earth occurs ONLY AFTER $100\%$ of the return propellant ($2,200\text{ MT}$ $\text{LH}_2$) is manufactured, stored, and verified in the Mars depot.

---

## 2. Ranked Failure Modes & Risk Register

| Risk ID | Failure Mode & Event | Prob. | Impact | Risk Class | Remaining Production Capability | Mission Consequence | Primary Mitigation Strategy |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- | :--- |
| **RSK-01** | **Precursor ISRU Total Launch / Landing Failure** | Medium | Critical | **HIGH** | $0\%$ ($0\text{ t LH}_2$ produced) | Precursor mission lost; crew Earth departure held | Crew launch holds on Earth until precursor succeeds. Zero crew loss. |
| **RSK-02** | **SOEC Electrolyzer Cell Degradation (50%)** | High | Moderate | **MEDIUM** | $50\%$ production rate ($2.76\text{ t/day}$) | Production time extends to $1,000\text{ days}$ | Modular SOEC stack redundancy ($2\times 10\text{ MWe}$ stacks for $17.58\text{ MWe}$ load). |
| **RSK-03** | **Surface Reactor Power Degradation (25%)** | Low | High | **MEDIUM** | $75\%$ power ($18.75\text{ MWe}$) | Production time extends to $665\text{ days}$ | Precursor reactor sized at $25.0\text{ MWe}$ ($+21.2\%$ margin over $20.63\text{ MWe}$). |
| **RSK-04** | **Excavator Unit Mechanical Jam / Abrasion Failure** | High | Moderate | **LOW** | $50\%$ mining rate ($2,208\text{ kg/hr}$) | Redundant unit operates at $90\%$ duty cycle ($600\text{d}$) | Fleet of 2 autonomous excavators + 1 spare chassis and replacement arms. |
| **RSK-05** | **Radiator Dust Deposition Degradation (30%)** | High | Moderate | **LOW** | Thermal rejection drops to $39.1\text{ MW}_{th}$ | Surface power throttled by $15\%$ | Electrostatic dust removal coatings + mechanical wiper blades. |
| **RSK-06** | **Claude Liquefaction Compressor Seal Leak** | Medium | High | **MEDIUM** | Liquefaction capacity drops by $40\%$ | Production timeline extends by $200\text{ days}$ | Dual parallel helium compressor loops with auto-isolation valves. |
| **RSK-07** | **Glacial Ice Ore Grade Deficit (20% vs 50%)** | Low | Moderate | **LOW** | Excavation demand increases $2.5\times$ ($265\text{ t/day}$) | Excavators operate at $85\%$ duty cycle | Radar-surveyed landing site selection (Arcadia Planitia / Deuteronilus Mensae). |
| **RSK-08** | **Cryogenic Depot Tank Micrometeorite Penetration** | Very Low| Critical | **HIGH** | Boiloff rate increases to $1.5\%/\text{day}$ | $300\text{ t LH}_2$ lost if unmitigated | Multi-layer MMOD Whipple shielding + 4 segmented isolated tanks. |
| **RSK-09** | **Global Martian Dust Storm (90-Day Duration)** | Medium | Low | **LOW** | ISRU plant operates nominally ($100\%$) | Zero production impact | Nuclear power source is completely immune to dust storm solar attenuation. |
| **RSK-10** | **Autonomous Robotic Assembly / Deployment Jam** | Medium | High | **MEDIUM** | Plant commissioning delayed by $180\text{ days}$ | Production window shifts within 750d precursor timeline | Self-deploying winch systems; minimal robotic assembly required. |

---

## 3. Detailed Analysis of Critical Failure Modes

### RSK-01: Precursor ISRU Total Launch or EDL Landing Failure
* **Quantitative Consequence:** If the uncrewed Super-Heavy precursor cargo lander carrying the $135\text{ t}$ ISRU plant is lost during Earth launch or Mars EDL, zero propellant is produced.
* **Architecture B Safety Advantage:** Because Enterprise X and its 24-person crew do not launch from LEO until the Mars depot is verified full, the failure results only in financial and schedule loss. **Crew mortality risk = 0.0%.**

### RSK-02: SOEC Electrolyzer Cell Degradation
* **Quantitative Consequence:** High-temperature Solid Oxide Electrolyzer Cells ($800^\circ\text{C}$) suffer chromium poisoning and thermal cycling degradation. A $50\%$ loss in cell activity reduces production from $5.52\text{ t/day}$ to $2.76\text{ t/day}$.
* **Mitigation:** Sizing the precursor production window to 750 days (with a 1,000-day pre-deployment horizon) allows the plant to complete $100\%$ of return propellant manufacturing even under $50\%$ electrolyzer degradation.

### RSK-03: Surface Reactor Power Degradation
* **Quantitative Consequence:** A $25\%$ power drop in the $25.0\text{ MWe}$ precursor surface reactor reduces electrical output to $18.75\text{ MWe}$.
* **Mitigation:** The nominal required power for $2,760.80\text{ t}$ $\text{LH}_2$ over 500 days is $17.58\text{ MWe}$. An $18.75\text{ MWe}$ supply still exceeds nominal requirements by $+1.17\text{ MWe}$, ensuring zero campaign delay.

---

## 4. Risk Register Conclusion

By transitioning from onboard crewed ISRU to **Precursor Autonomous Robotic ISRU Depot (Architecture B)**, the entire risk profile is transformed: every critical ISRU failure mode is converted from a crew-fatal hazard into a manageable schedule contingency.
