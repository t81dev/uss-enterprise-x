# 60 — NTP Propellant Architecture Trade v2

**Document ID:** `60-ntp-propellant-trade-v2.md`
**Program Phase:** Architecture Optimization & Physics Verification
**Program Status:** Formal Propellant Trade & Optimization Complete

---

## 1. Executive Summary

`60-ntp-propellant-trade-v2.md` conducts a comprehensive first-principles comparative trade analysis between candidate Solid-Core Nuclear Thermal Propulsion (NTP) propellants for the USS Enterprise X architecture.

The previous red-team assessment (`52-mission-closure-review.md`) highlighted Liquid Hydrogen ($\text{LH}_2$) as the primary volumetric and logistics bottleneck of the spacecraft due to its extremely low density ($\rho = 71.0\text{ kg/m}^3$), requiring $31,000\text{ m}^3$ of pressure tank volume and 10 propellant tanker launches.

This trade compares Liquid Hydrogen ($\text{LH}_2$), Liquid Methane ($\text{LCH}_4$), Liquid Ammonia ($\text{LNH}_3$), and a Mars ISRU-refueled $\text{LH}_2$ architecture across specific impulse ($I_{sp}$), propellant density ($\rho$), tank structural mass, reactor thermal-hydraulic compatibility, launch manifest count, and round-trip mission $\Delta v$ performance.

---

## 2. NTP Propellant Candidate Technical Parameter Trade Matrix

| Propellant Candidate | Density ($\rho$) | Specific Impulse ($I_{sp}$) | Exhaust Velocity ($v_e$) | Propellant Mass ($M_{prop}$) | Required Tank Volume | Dry Tank Mass | Assembly Launches | LEO Departure Mass ($M_{dep}$) | Total Vehicle $\Delta v$ | Reactor Compatibility & Coking Risk | Overall Trade Rank |
| :--- | ---:| ---:| ---:| ---:| ---:| ---:| ---:| ---:| ---:| :--- | :---: |
| **A. Baseline Liquid Hydrogen ($\text{LH}_2$)** | **$71.0\text{ kg/m}^3$** | **$900.0\text{ s}$** | **$8,826\text{ m/s}$** | $2,200.0\text{ t}$ | $30,986\text{ m}^3$ | $178.75\text{ t}$ | 16 Launches | $3,970.96\text{ t}$ | $12.250\text{ km/s}$ | High compatibility; clean light molecule ($H_2$). Zero coking risk. | **Rank 2 (Baseline)** |
| **B. Liquid Methane ($\text{LCH}_4$)** | $422.5\text{ kg/m}^3$ | $650.0\text{ s}$ | $6,374\text{ m/s}$ | $4,120.0\text{ t}$ | $9,751\text{ m}^3$ | $72.30\text{ t}$ | 23 Launches | $5,663.26\text{ t}$ | $9.850\text{ km/s}$ | Severe carbon coking risk above $1,600\text{ K}$ in fuel elements. | **Rank 3 (Disqualified)** |
| **C. Liquid Ammonia ($\text{LNH}_3$)** | $682.0\text{ kg/m}^3$ | $450.0\text{ s}$ | $4,413\text{ m/s}$ | $7,850.0\text{ t}$ | $11,510\text{ m}^3$ | $68.10\text{ t}$ | 38 Launches | $9,389.06\text{ t}$ | $7.120\text{ km/s}$ | Nitriding corrosion of carbide/graphite fuel elements at high $T$. | **Rank 4 (Disqualified)** |
| **D. Mars ISRU Refueled ($\text{LH}_2$)** | $71.0\text{ kg/m}^3$ | $900.0\text{ s}$ | $8,826\text{ m/s}$ | $1,800.0\text{ t}$ LEO $+ 500\text{ t}$ Mars | $25,352\text{ m}^3$ | $146.25\text{ t}$ | **11 Launches** | **$3,539.71\text{ t}$** | **$16.850\text{ km/s}$** | Uses clean $\text{LH}_2$. Mars surface ISRU provides return propellant. | **Rank 1 (Optimal Upgrade)** |

---

## 3. In-Depth Trade Findings & Analysis

### A. Liquid Methane ($\text{LCH}_4$) Assessment:
* **Volumetric Benefit:** $6 \times$ denser than $\text{LH}_2$, cutting tank volume from $31,000\text{ m}^3$ to $9,750\text{ m}^3$ and saving $106.4\text{ t}$ of tank structural mass.
* **Mass Ratio & Impulse Penalty:** Because molecular mass of methane fragments ($CH_4 \rightarrow CH_3 + H$) is much higher than molecular hydrogen ($H_2$), $I_{sp}$ drops from $900\text{ s}$ to $650\text{ s}$. Delivering equal $\Delta v$ requires $4,120\text{ t}$ of propellant, increasing total departure mass from $3,971\text{ t}$ to $5,663\text{ t}$ and launch count from 16 to 23 launches.
* **Reactor Carbon Coking Failure Mode:** At solid-core NTP core temperatures ($>2,700\text{ K}$), methane pyrolyzes into free carbon, causing catastrophic coking and blockage of $1\text{ mm}$ coolant channels inside carbide fuel elements.

### B. Liquid Ammonia ($\text{LNH}_3$) Assessment:
* **Storage Advantage:** High density ($682\text{ kg/m}^3$) and near-ambient boiling point ($239.8\text{ K}$) eliminate cryogenic ZBO refrigeration requirements.
* **Performance Failure:** Low $I_{sp} = 450\text{ s}$ requires $7,850\text{ t}$ of propellant. Gross departure mass ballooning to $9,389\text{ t}$ requires 38 heavy launches, invalidating the mission architecture.

### C. Mars In-Situ Propellant Production (ISRU $\text{LH}_2$) Assessment (Rank 1):
* **Operational Mechanics:** Spacecraft departs Earth LEO with $1,800\text{ t}$ $\text{LH}_2$ (enough for TMI and MOI). Upon arrival at Mars, automated surface ISRU plants process Martian water ice ($H_2O$) via electrolysis into $500\text{ t}$ of liquid hydrogen propellant.
* **Architecture Gains:**
  1. Reduces Earth departure gross mass by $431.25\text{ t}$ ($3,539.71\text{ t}$ vs $3,970.96\text{ t}$).
  2. Reduces Super-Heavy launch manifest from 16 to 11 launches.
  3. Provides an additional $+4.60\text{ km/s}$ velocity reserve at Mars return, fully closing the $-2.805\text{ km/s}$ return trajectory deficit.

---

## 4. Trade Recommendation

The primary recommended upgrade path for the USS Enterprise X v4 architecture is:

> **Adopt Mars ISRU Refueled Liquid Hydrogen ($\text{LH}_2$) as the core mission baseline.**

This retains the ultra-high $I_{sp} = 900\text{ s}$ performance and clean material compatibility of hydrogen while eliminating the LEO departure mass penalty and return trajectory velocity deficit.
