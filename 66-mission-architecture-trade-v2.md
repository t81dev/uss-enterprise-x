# 66 — Mission Architecture Trade Analysis v2

**Document ID:** `66-mission-architecture-trade-v2.md`
**Calculation Engine Source:** `engineering/calculations/mars_isru.py`
**Program Phase:** Phase 8.1 — Mars ISRU, Propellant Logistics & Physical Mission Closure (Remediated)
**Program Status:** **ENGINEERINGALLY CONDITIONAL (Architecture B Selected as Baseline)**

---

## 1. Executive Summary

`66-mission-architecture-trade-v2.md` evaluates five candidate mission architectures for Project Occam-7 (USS Enterprise X) to resolve the return propellant closure dependency identified in Phase 7.

Previous program phases assumed that USS Enterprise X would carry its own Mars In-Situ Resource Utilization (ISRU) manufacturing plant on board and produce return propellant after crew arrival on Mars (**Architecture A**). First-principles analysis in Phase 8 proves Architecture A is **PHYSICALLY INFEASIBLE and ARCHITECTURALLY INVALID**.

This document conducts a quantitative trade study across Architectures A through E and establishes **Architecture B (Precursor Autonomous Robotic ISRU Depot - 2x 150t Cargo Landers)** as the canonical program baseline.

---

## 2. Evaluation of Candidate Mission Architectures

### Architecture A: Crewed Enterprise Carries Onboard ISRU (Legacy Concept)
* **Description:** USS Enterprise X carries a $135\text{ t}$ ISRU surface plant on board, lands on Mars, deploys power/mining, and manufactures $2,200\text{ t}$ of return $\text{LH}_2$ during the 640-day crew stay.
* **Fatal Engineering Flaws:**
  1. USS Enterprise X is a $380\text{-meter}$ nuclear space-truss ship designed strictly for orbital transfer; landing and ascending from Mars is physically impossible.
  2. Forcing crew to wait 500 days on Mars surface for unproven ISRU creates an unacceptable single-point-failure crew mortality risk ($P_{mortality} > 65\%$).
* **Verdict:** **PHYSICALLY INFEASIBLE / ARCHITECTURE INVALID.**

---

### Architecture B: Precursor Autonomous Robotic ISRU Depot (CANONICAL BASELINE - 2x LANDERS)
* **Description:** Uncrewed Super-Heavy cargo landers (2x 150t payload capacity) pre-deploy a $256.29\text{ t}$ ISRU plant and $25\text{ MWe}$ nuclear power source to Mars **1 to 2 synodic cycles (26 to 52 months) before crew departure from Earth**. The autonomous plant manufactures, liquefies, stores, and verifies $2,760.80\text{ t}$ of $\text{LH}_2$ in a verified surface/orbital depot.
* **Key Engineering Advantages:**
  1. Crew departure from Earth occurs **ONLY AFTER $100\%$ of return propellant is manufactured and verified in the Mars depot** via machine-readable pre-departure safety gate (`precursor_inventory_verified()`).
  2. Eliminates crew mortality risk from ISRU failure ($P_{mortality\_isru} = 0.0\%$).
  3. Extends available production window from 500 days to 750+ days, easily accommodating maintenance downtime.
  4. Multi-lander delivery architecture (2x 150t landers) provides $+43.71\text{ MT}$ payload margin over the $256.29\text{ MT}$ dry plant mass.
* **Verdict:** **ENGINEERINGALLY CONDITIONAL (RECOMMENDED BASELINE).**

---

### Architecture C: Multi-Mission Precursor ISRU Depot Network
* **Description:** Deploys four independent ISRU precursor landers to separate locations (e.g. Arcadia Planitia & Deuteronilus Mensae) to build redundant propellant depots.
* **Tradeoffs:** Provides $200\%$ production capacity and zero single-point hardware failure, but increases precursor program cost by $+85\%$.
* **Verdict:** **FEASIBLE BUT HIGH COST.**

---

### Architecture D: Zero-ISRU All-Earth Propellant Supply
* **Description:** Eliminates Mars ISRU entirely. Enterprise X carries all return propellant ($2,200\text{ t}$ $\text{LH}_2$) from LEO.
* **Tradeoffs:**
  1. Gross LEO departure wet mass explodes to **$6,850.00\text{ MT}$**.
  2. Requires **28 Super-Heavy launches** within a tight 4.5-month assembly window.
  3. LEO orbital cryogenic boiloff over 135 days destroys propellant margins ($>250\text{ t}$ boiloff loss).
* **Verdict:** **PHYSICALLY UNECONOMIC / HIGH BOILOFF RISK.**

---

### Architecture E: Hybrid Architecture (Surface MAV $\text{CH}_4/\text{LOX}$ ISRU + Earth $\text{LH}_2$ TEI)
* **Description:** Small $28\text{ t}$ ISRU plant produces $\text{CH}_4/\text{LOX}$ for surface ascent lander; main NTP return $\text{LH}_2$ is carried from Earth.
* **Tradeoffs:** Reduces surface ISRU plant mass, but requires 21 Super-Heavy Earth launches and high LEO departure mass ($5,100\text{ t}$).
* **Verdict:** **CONDITIONALLY FEASIBLE (SUBOPTIMAL).**

---

## 3. Quantitative Architectural Trade Matrix

| Trade Metric | Architecture A (Onboard ISRU) | Architecture B (Precursor Depot Baseline) | Architecture C (Multi-Depot) | Architecture D (Zero ISRU All-Earth) | Architecture E (Hybrid MAV ISRU) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Vessel Mars Landing Required?** | YES (Impossible) | NO (Orbital) | NO (Orbital) | NO (Orbital) | NO (Orbital) |
| **Precursor Cargo Landers Required** | 0 | **2 Landers (2x 150t)**| 4 Cargo Landers | 0 | 1 Cargo Lander |
| **Earth LEO Super-Heavy Launches** | 16 | **11 Launches** | 13 Launches | 28 Launches | 21 Launches |
| **Gross LEO Departure Mass ($M_{dep}$)** | $3,970.96\text{ t}$ | **$3,970.96\text{ t}$** | $3,970.96\text{ t}$ | $6,850.00\text{ t}$ | $5,100.00\text{ t}$ |
| **Mars Surface Power Required** | $20.63\text{ MWe}$ | **$20.63\text{ MWe}$** | $2\times 15.0\text{ MWe}$ | $0.0\text{ MWe}$ | $2.5\text{ MWe}$ |
| **ISRU Plant Mass ($M_{isru}$)** | $256.29\text{ t}$ | **$256.29\text{ t}$** | $307.55\text{ t}$ | $0.0\text{ t}$ | $28.0\text{ t}$ |
| **ISRU Failure Crew Mortality Risk** | **$65.4\%$ (Fatal)** | **$0.0\%$ (Safe)** | $0.0\%$ (Safe) | $0.0\%$ (Safe) | $0.0\%$ (Safe) |
| **Monte Carlo Success Rate $P(success)$**| $34.57\%$ | **$99.61\%$** | $99.85\%$ | $42.10\%$ | $78.30\%$ |
| **Program Cost Index (Norm. Arch B)** | $1.25\times$ | **$1.00\times$** | $1.45\times$ | $2.10\times$ | $1.60\times$ |
| **FINAL PROGRAM STATUS** | **INVALID** | **SELECTED BASELINE**| **BACKUP** | **REJECTED** | **REJECTED** |

---

## 4. Architectural Decision Conclusion

Project Occam-7 formally adopts **Architecture B (Precursor Autonomous Robotic ISRU Depot)** as the authoritative program baseline.

All subsequent engineering documentation, system reference models, and mission event timelines reflect Architecture B with 2x 150t precursor landers and mandatory pre-departure safety gates.
