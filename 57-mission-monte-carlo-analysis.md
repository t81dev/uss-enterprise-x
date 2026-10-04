# 57 — Mission Monte Carlo Sensitivity & Risk Analysis

**Document ID:** `57-mission-monte-carlo-analysis.md`
**Calculation Engine:** `engineering/calculations/mission_monte_carlo.py`
**Dataset Source:** `engineering/calculations/mission_monte_carlo.json`
**Program Status:** Statistical Monte Carlo Sensitivity Analysis Complete

---

## 1. Executive Summary

`57-mission-monte-carlo-analysis.md` documents the statistical sensitivity analysis conducted on the USS Enterprise X (Project Occam-7) mission architecture.

To evaluate the robustness of the spacecraft baseline against physical uncertainties, manufacturing tolerances, thermal degradation, and trajectory variations, a **1,000-case Monte Carlo simulation** was executed. Key engineering parameters were stochastically sampled from normal (Gaussian) and uniform probability distributions reflecting AIAA technical growth standards.

---

## 2. Monte Carlo Simulation Statistical Summary

| Statistical Metric | Baseline Value | Mean ($\mu$) | Std. Dev. ($\sigma$) | Min (99.9%) | Max (99.9%) | Unit |
| :--- | ---:| ---:| ---:| ---:| ---:| :---: |
| **Total Simulated Mission Cases** | $1,000$ | $1,000$ | — | — | — | Runs |
| **Mission Success Rate** | **100.0%** | **100.0%** | $0.0\%$ | $100.0\%$ | $100.0\%$ | $\%$ |
| **Vehicle Total Delta-V ($\Delta v$)** | $12.250$ | **12.248** | $0.312$ | $11.185$ | $13.210$ | $\text{km/s}$ |
| **Vehicle Dry Mass ($M_{dry}$)** | $1,470.96$ | $1,471.20$ | $73.12$ | $1,241.05$ | $1,698.40$ | $\text{MT}$ |
| **NTP $\text{LH}_2$ Propellant** | $2,200.00$ | $2,201.10$ | $65.80$ | $1,995.10$ | $2,408.20$ | $\text{MT}$ |
| **NEP $\text{LNH}_3$ Propellant** | $300.00$ | $300.12$ | $8.95$ | $272.10$ | $328.50$ | $\text{MT}$ |
| **Final Gross Return Mass** | $1,424.69$ | $1,425.12$ | $71.80$ | $1,201.10$ | $1,648.20$ | $\text{MT}$ |

---

## 3. Parameter Uncertainty Distributions

The 1,000-run simulation varied the following 9 system parameters simultaneously:

1. **Vehicle Dry Mass ($M_{dry}$):** Gaussian distribution $\mathcal{N}(\mu=1470.96\text{ t}, \sigma=73.55\text{ t})$ ($\pm 5\%$ std dev).
2. **NTP $\text{LH}_2$ Propellant Mass ($M_{LH2}$):** Gaussian distribution $\mathcal{N}(\mu=2200.0\text{ t}, \sigma=66.0\text{ t})$ ($\pm 3\%$ std dev).
3. **NEP $\text{LNH}_3$ Propellant Mass ($M_{LNH3}$):** Gaussian distribution $\mathcal{N}(\mu=300.0\text{ t}, \sigma=9.0\text{ t})$ ($\pm 3\%$ std dev).
4. **NTP Engine Specific Impulse ($I_{sp}$):** Gaussian distribution $\mathcal{N}(\mu=900.0\text{ s}, \sigma=18.0\text{ s})$ ($\pm 2\%$ std dev).
5. **NTP Vacuum Thrust ($F_{NTP}$):** Gaussian distribution $\mathcal{N}(\mu=4000.0\text{ kN}, \sigma=120.0\text{ kN})$ ($\pm 3\%$ std dev).
6. **NEP Electrical Input Power ($P_{elec}$):** Gaussian distribution $\mathcal{N}(\mu=15.0\text{ MWe}, \sigma=0.75\text{ MWe})$ ($\pm 5\%$ std dev).
7. **NEP MPD Thruster Efficiency ($\eta$):** Uniform distribution $\mathcal{U}(\text{min}=0.58, \text{max}=0.72)$ ($0.65 \pm 0.07$).
8. **Radiator Heat Rejection Capacity ($Q_{rad}$):** Gaussian distribution $\mathcal{N}(\mu=133.35\text{ MW}_{th}, \sigma=6.67\text{ MW}_{th})$ ($\pm 5\%$ std dev).
9. **Crew Consumable Depletion Rate:** Gaussian distribution $\mathcal{N}(\mu=0.0723\text{ t/d}, \sigma=0.0036\text{ t/d})$ ($\pm 5\%$ std dev).

---

## 4. Parameter Sensitivity Ranking Matrix

Sensitivity ranking was computed by measuring the normalized impact of each input variable's standard deviation on total vehicle velocity capability ($\Delta v$):

| Rank | System Parameter | Relative Sensitivity Score | Physical Mechanics & Sensitivity Impact |
| :---: | :--- | :---: | :--- |
| **1** | **NTP Specific Impulse ($I_{sp}$)** | **100.0% (Primary Driver)** | A $1\%$ shift in $I_{sp}$ ($\pm 9.0\text{ s}$) produces a $\pm 0.136\text{ km/s}$ change in total vehicle $\Delta v$. |
| **2** | **Vehicle Dry Mass ($M_{dry}$)** | **88.4% (Critical Mass)** | A $5\%$ growth in dry mass ($+73.5\text{ t}$) reduces total vehicle $\Delta v$ by $0.215\text{ km/s}$. |
| **3** | **NTP $\text{LH}_2$ Inventory ($M_{LH2}$)** | **72.1% (Propellant Capacity)** | A $3\%$ loss in $\text{LH}_2$ allocation ($-66.0\text{ t}$) reduces available impulse $\Delta v$ by $0.182\text{ km/s}$. |
| **4** | **NEP MPD Thruster Efficiency ($\eta$)** | **42.5% (Electric Jet Power)** | Efficiency drops below $\eta = 0.60$ decrease NEP cruise $\Delta v$ by $0.110\text{ km/s}$. |
| **5** | **NEP Electrical Power ($P_{elec}$)** | **38.2% (Brayton Loop)** | Power loss reduces low-thrust acceleration, extending transit duration. |
| **6** | **Radiator Capacity ($Q_{rad}$)** | **15.4% (Thermal Margin)** | Radiator degradation reduces reactor output margin, constraining NEP cruise. |

---

## 5. Risk Assessment & Engineering Takeaway

1. **High Mission Robustness:** Under nominal parameter uncertainties ($\pm 3\% - 5\%$ std dev), vehicle capability remains within $12.248 \pm 0.312\text{ km/s}$.
2. **Key Design Gatekeeper:** NTP Specific Impulse ($I_{sp} \ge 900\text{ s}$) and Dry Mass Containment ($M_{dry} \le 1,470.96\text{ t}$) are confirmed as the dominant gatekeepers of mission velocity capability.
