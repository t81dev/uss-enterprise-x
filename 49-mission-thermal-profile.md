# 49 — Mission Thermal Profile & Heat Rejection v1

**Document ID:** `49-mission-thermal-profile.md`
**Digital Twin Verification:** `engineering/calculations/mission_digital_twin.py`
**Program Status:** Dynamic Mission Thermal Profile & Radiator Rejection Analysis

---

## 1. Executive Summary

`49-mission-thermal-profile.md` tracks heat generation and thermal rejection across the entire 1,000-day mission. Thermal rejection in deep space is governed strictly by the Stefan-Boltzmann radiation law ($Q = \epsilon \sigma A T^4$).

This audit verifies that total waste heat generation never exceeds the $133.35\text{ MW}_{th}$ maximum heat rejection capacity of the baseline high-temperature $850\text{ K}$ liquid metal ($NaK$) heat-pipe radiator array ($2,502.8\text{ m}^2$ footprint footprint, double-sided emission), even during high-power propulsion conditioning or partial radiator damage events.

---

## 2. Thermal Balance Governing Physics

### A. Stefan-Boltzmann Radiation Formula
Radiator heat rejection $Q_{rad}$ is given by:
$$Q_{rad} = 2 \cdot A_{footprint} \cdot \epsilon \cdot \sigma \cdot T_{rad}^4 \cdot (1 - M_{deg})$$

Where:
* $A_{footprint} = 2,502.8\text{ m}^2$ (one-sided panel footprint area).
* Factor $2$: Double-sided radiative emission into deep space.
* $\epsilon = 0.90$ (high-emissivity carbon-carbon composite surface coating).
* $\sigma = 5.670374419 \times 10^{-8}\text{ W/(m}^2\text{K}^4\text{)}$ (Stefan-Boltzmann constant).
* $T_{rad} = 850.0\text{ K}$ (primary liquid-metal heat pipe manifold temperature).
* $M_{deg} = 0.15$ ($15\%$ lifecycle thermal degradation margin).

#### Maximum Nominal Rejection Capacity ($Q_{max}$):
$$Q_{max} = 2 \times 2,502.8 \times 0.90 \times 5.67037 \times 10^{-8} \times (850)^4 \times (1 - 0.15)$$
$$Q_{max} = 2 \times 2,502.8 \times 0.90 \times 29.60 \times (0.85) = \mathbf{113.35\text{ MW}_{th}} \quad (\text{Degraded Margin Nominal})$$
$$\text{Undegraded Nominal Capacity } (M_{deg}=0) = \mathbf{133.35\text{ MW}_{th}}$$

---

## 3. Mission Phase Thermal Load Profile

| Mission Phase | Operational State | Reactor Core Output | Thermal Conversion Efficiency | Electrical Power Gen. | Propulsion Load / Loss | House / Avionics Heat | Total Thermal Waste Heat | Radiator Heat Capacity | Thermal Margin ($Q_{cap} - Q_{waste}$) |
| :--- | :--- | ---:| :---: | ---:| ---:| ---:| ---:| ---:| ---: |
| **0. LEO Assembly** | Standby / Low Power | $10.0\text{ MW}_{th}$ | $20.0\%$ | $2.0\text{ MWe}$ | $0.00\text{ MW}$ | $0.445\text{ MW}$ | **$8.00\text{ MW}_{th}$** | $133.35\text{ MW}_{th}$ | **$+125.35\text{ MW}_{th}$** |
| **1. NTP TMI Burn** | Impulsive High-Thrust | $100.0\text{ MW}_{th}$ | $20.0\%$ | $20.0\text{ MWe}$ | $0.50\text{ MW}$ | $0.445\text{ MW}$ | **$80.50\text{ MW}_{th}$** | $133.35\text{ MW}_{th}$ | **$+52.85\text{ MW}_{th}$** |
| **2. Outbound NEP Cruise** | Continuous $15\text{MWe}$ | $100.0\text{ MW}_{th}$ | $20.0\%$ | $20.0\text{ MWe}$ | $5.25\text{ MW}$ | $0.445\text{ MW}$ | **$85.25\text{ MW}_{th}$** | $133.35\text{ MW}_{th}$ | **$+48.10\text{ MW}_{th}$** |
| **3. NTP MOI Burn** | Impulsive High-Thrust | $100.0\text{ MW}_{th}$ | $20.0\%$ | $20.0\text{ MWe}$ | $0.50\text{ MW}$ | $0.445\text{ MW}$ | **$80.50\text{ MW}_{th}$** | $133.35\text{ MW}_{th}$ | **$+52.85\text{ MW}_{th}$** |
| **4. Mars Orbit Stay** | Orbital Operations | $10.0\text{ MW}_{th}$ | $20.0\%$ | $2.0\text{ MWe}$ | $0.00\text{ MW}$ | $0.600\text{ MW}$ | **$8.00\text{ MW}_{th}$** | $133.35\text{ MW}_{th}$ | **$+125.35\text{ MW}_{th}$** |
| **5. NTP TEI Burn** | Impulsive High-Thrust | $100.0\text{ MW}_{th}$ | $20.0\%$ | $20.0\text{ MWe}$ | $0.50\text{ MW}$ | $0.445\text{ MW}$ | **$80.50\text{ MW}_{th}$** | $133.35\text{ MW}_{th}$ | **$+52.85\text{ MW}_{th}$** |
| **6. Inbound NEP Cruise** | Continuous $15\text{MWe}$ | $100.0\text{ MW}_{th}$ | $20.0\%$ | $20.0\text{ MWe}$ | $5.25\text{ MW}$ | $0.445\text{ MW}$ | **$85.25\text{ MW}_{th}$** | $133.35\text{ MW}_{th}$ | **$+48.10\text{ MW}_{th}$** |

---

## 4. Off-Nominal Thermal Stress Testing

```
[ CONTINUOUS NEP CRUISE WASTE HEAT: 85.25 MWth ]
                       |
  =======================================================
  Radiator Condition                Rejection Capacity    Thermal Margin
  -------------------------------------------------------
  Nominal (100% Area @ 850K)         133.35 MWth           +48.10 MWth (CLOSED)
  Degraded (15% Margin)              113.35 MWth           +28.10 MWth (CLOSED)
  Failure: 25% Radiator Loss          100.01 MWth           +14.76 MWth (CLOSED)
  Failure: 40% Radiator Loss           80.01 MWth           -5.24 MWth  (THROTTLED)
  =======================================================
```

### Critical Off-Nominal Cases:
1. **Case T1: $25\%$ Radiator Area MMOD Loss:**
   * Remaining Area: $1,877.1\text{ m}^2$.
   * Rejection Capacity ($Q_{cap}$): $100.01\text{ MW}_{th}$.
   * NEP Cruise Waste Heat: $85.25\text{ MW}_{th}$.
   * **Result:** Thermal balance closes with $+14.76\text{ MW}_{th}$ positive headroom.

2. **Case T2: $40\%$ Radiator Area Loss (Severe Impact):**
   * Remaining Area: $1,501.7\text{ m}^2$.
   * Rejection Capacity ($Q_{cap}$): $80.01\text{ MW}_{th}$.
   * **Automated Action:** Ship Operating System (sOS) automatically throttles reactor output to $93.8\text{ MW}_{th}$ ($18.76\text{ MWe}$ generation, $14.07\text{ MWe}$ NEP input), maintaining steady-state thermal equilibrium without crew intervention.
