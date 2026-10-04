# 25 — Mission Performance & Trajectory Analysis (Reconciled v2)

**Document ID:** `25-mission-performance-v1.md`
**Baseline Mission:** Earth-Mars-Earth Fast Transit (1,000 Days)
**Primary Propulsion Baseline:** Hybrid NTP (High-Thrust Impulse) + NEP MPD (Continuous High-Efficiency Cruise)
**Reconciled Departure Mass ($M_{dep}$):** $3,970.96\text{ MT}$
**Reconciled Dry Mass ($M_{dry}$):** $1,470.96\text{ MT}$

---

## 1. Propulsion & Trajectory Coupling Physics (Reconciled)

### A. Nuclear Electric Propulsion (NEP) First-Principles Sizing (DEF-002, DEF-003)
The baseline electrical generation system supplies $15.0\text{ MWe}$ to the Magnetoplasmadynamic (MPD) electric propulsion array during cruise.

For an ideal electric thruster:
$$P_{jet} = \frac{1}{2} \dot{m} v_e^2 = \frac{1}{2} F v_e$$
$$v_e = I_{sp} g_0 = 3,500 \times 9.80665 = 34,323.28\text{ m/s}$$

Assuming MPD electrical-to-jet power conversion efficiency $\eta_{thruster} = 0.65$:
$$P_{jet} = 15.0\text{ MWe} \times 0.65 = \mathbf{9.75\text{ MW}_{jet}}$$

#### Corrected NEP Thrust ($F_{NEP}$):
$$F_{NEP} = \frac{2 P_{jet}}{v_e} = \frac{2 \times 9,750,000\text{ W}}{34,323.28\text{ m/s}} = \mathbf{568.12\text{ N}}$$

#### Mass Flow Rate ($\dot{m}$):
$$\dot{m} = \frac{F_{NEP}}{v_e} = \frac{568.12}{34,323.28} = \mathbf{0.016552\text{ kg/s}} = \mathbf{1.430\text{ MT/day}}$$

### B. Continuous Cruise Delta-V Integration
For a continuous low-thrust burn duration $t_{burn} = 180\text{ days}$ ($15.552 \times 10^6\text{ s}$) per transit leg:
$$\Delta M_{prop} = 1.4301\text{ MT/day} \times 180\text{ days} = \mathbf{257.42\text{ MT}}$$

Evaluating the initial cruise mass $M_0 = 1,770.96\text{ MT}$ ($1,470.96\text{ t}$ dry + $300.0\text{ t}$ NEP propellant) and final mass $M_f = M_0 - 257.42 = 1,513.54\text{ MT}$:
$$\Delta v_{cruise} = v_e \ln\left(\frac{M_0}{M_f}\right) = 34,323.28 \times \ln\left(\frac{1,770.96}{1,513.54}\right) = \mathbf{5,394.8\text{ m/s}} = \mathbf{5.39\text{ km/s}}$$

The reconciled $15\text{ MWe}$ NEP system yields **$5.39\text{ km/s}$ continuous cruise $\Delta v$** per leg, fully exceeding the nominal $2.55\text{ km/s}$ leg requirement ($5.10\text{ km/s}$ combined) with $2.11\times$ margin.

---

## 2. Integrated Trajectory & Delta-V Budget (Mission B Baseline)

| Mission Phase | Propulsion Mode | Specific Impulse ($I_{sp}$) | Propellant Consumed (MT) | Phase Delta-V ($\text{km/s}$) | Cumulative Delta-V ($\text{km/s}$) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **1. Trans-Mars Injection (TMI)** | 4x NTP Solid-Core | $900\text{ s}$ | $1,320.0\text{ MT}$ $\text{LH}_2$ | $3.80\text{ km/s}$ | $3.80\text{ km/s}$ |
| **2. Outbound Cruise Acceleration** | 4x MW MPD Thrusters | $3,500\text{ s}$ | $128.7\text{ MT}$ $\text{LNH}_3/\text{Ar}$ | $2.55\text{ km/s}$ | $6.35\text{ km/s}$ |
| **3. Mars Orbit Insertion / Capture** | 4x NTP Solid-Core | $900\text{ s}$ | $480.0\text{ MT}$ $\text{LH}_2$ | $2.10\text{ km/s}$ | $8.45\text{ km/s}$ |
| **4. Trans-Earth Injection (TEI)** | 4x NTP Solid-Core | $900\text{ s}$ | $400.0\text{ MT}$ $\text{LH}_2$ | $2.80\text{ km/s}$ | $11.25\text{ km/s}$ |
| **5. Inbound Cruise Acceleration** | 4x MW MPD Thrusters | $3,500\text{ s}$ | $128.7\text{ MT}$ $\text{LNH}_3/\text{Ar}$ | $2.55\text{ km/s}$ | $13.80\text{ km/s}$ |
| **6. Earth Orbit Capture & Reserve** | 4x NTP Solid-Core | $900\text{ s}$ | $42.6\text{ MT}$ $\text{LH}_2$ / RCS | $2.20\text{ km/s}$ | $16.00\text{ km/s}$ |
| **TOTAL MISSION B** | **Hybrid NTP + NEP** | **$1,800\text{ s}$ Effective** | **$2,500.0\text{ MT}$** | **$16.00\text{ km/s}$** | **$16.00\text{ km/s}$** |

---

## 3. Mission Timeline & Orbital Operations

```
[EARTH LEO DEPARTURE] --(TMI + Outbound NEP)--> [MARS ORBIT] --(TEI + Inbound NEP)--> [EARTH CAPTURE]
     Day 0                Days 0–180               Days 180–820           Days 820–1000
```

* **Outbound Transit:** $180\text{ days}$ ($0.5\text{ years}$)
* **Mars Orbital Exploration Stay:** $640\text{ days}$
* **Inbound Return Transit:** $180\text{ days}$ ($0.5\text{ years}$)
* **Total Mission Horizon:** $1,000\text{ days}$
