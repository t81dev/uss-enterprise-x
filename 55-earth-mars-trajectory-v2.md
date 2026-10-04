# 55 — Earth-Mars Trajectory & Two-Body Mechanics v2

**Document ID:** `55-earth-mars-trajectory-v2.md`
**Calculation Engine:** `engineering/calculations/earth_mars_transfer.py`
**Data Source:** `engineering/calculations/earth_mars_transfer.json`
**Program Status:** Two-Body Patched-Conic & Low-Thrust Trajectory Analysis Complete

---

## 1. Executive Summary

`55-earth-mars-trajectory-v2.md` evaluates the orbital mechanics of the USS Enterprise X for round-trip Earth-Mars missions using patched-conic two-body mechanics and low-thrust vector acceleration.

While previous documentation asserted that $12.250\text{ km/s}$ total vehicle $\Delta v$ closes an 850-day Earth-Mars round trip, this analysis demonstrates that:
1. **Outbound 180-day Transit Closes:** Combined NTP TMI ($3.800\text{ km/s}$) + Outbound NEP ($3.605\text{ km/s}$) + NTP MOI ($2.100\text{ km/s}$) closes outbound transit mechanics.
2. **Inbound 180-day Fast Transit Requires Propulsive Aerocapture Or Extended Conjunction:** Pure propulsive Earth capture ($1.200\text{ km/s}$ EOI) creates a $-2.805\text{ km/s}$ trajectory deficit on a 180-day fast return timeline.
3. **640-Day Mars Stay Is Driven By Synodic Geometry:** The 640-day stay aligns with the Earth-Mars synodic period ($779.9\text{ days}$) for return window alignment.

---

## 2. Patched-Conic Analytical Results Table

| Mission Leg / Phase | Trajectory Parameter | Baseline Value | Units | First-Principles Derivation / Formula |
| :--- | :--- | ---:| :---: | :--- |
| **Hohmann Minimum Energy** | Transfer Semi-Major Axis ($a_{trans}$) | $1.262$ | $\text{AU}$ | $a = (r_E + r_M) / 2 = (1.000 + 1.524) / 2$ |
| | One-Way Hohmann Transit Time | $258.9$ | $\text{days}$ | $T = \pi \sqrt{a_{trans}^3 / \mu_\odot}$ |
| | Departure $v_\infty$ (Hohmann) | $2.949$ | $\text{km/s}$ | $v_{\infty,dep} = \sqrt{\mu_\odot (2/r_E - 1/a)} - v_E$ |
| | Impulsive TMI from LEO ($400\text{ km}$) | $3.568$ | $\text{km/s}$ | $\Delta v_{TMI} = \sqrt{v_{esc}^2 + v_\infty^2} - v_{LEO}$ |
| | Arrival $v_\infty$ (Hohmann) | $2.649$ | $\text{km/s}$ | $v_{\infty,arr} = v_M - \sqrt{\mu_\odot (2/r_M - 1/a)}$ |
| | Impulsive MOI to LMO ($500\text{ km}$) | $2.036$ | $\text{km/s}$ | $\Delta v_{MOI} = \sqrt{v_{esc,M}^2 + v_\infty^2} - v_{LMO}$ |
| **180-Day Fast Transfer** | Outbound $v_{\infty,dep}$ (Fast 180d) | $3.850$ | $\text{km/s}$ | Hyperbolic departure excess velocity |
| | Outbound $v_{\infty,arr}$ (Fast 180d) | $4.120$ | $\text{km/s}$ | Hyperbolic arrival excess velocity |
| | Required Outbound Impulsive $\Delta v$ | $6.480$ | $\text{km/s}$ | $3.80\text{ km/s TMI} + 2.68\text{ km/s MOI}$ |
| | Hybrid Outbound Actual $\Delta v$ | $9.505$ | $\text{km/s}$ | $3.80\text{ TMI} + 3.605\text{ NEP} + 2.10\text{ MOI}$ |

---

## 3. Low-Thrust NEP Acceleration Dynamics

The $15\text{ MWe}$ NEP system generates $F = 568.12\text{ N}$ of continuous thrust. Applying this thrust to the vehicle mass state yields:

### Acceleration Profile:
* **Departure Mass ($3,970.96\text{ t}$):** $a = 0.143\text{ mm/s}^2 = 14.58\text{ }\mu g$. Time to accumulate $1\text{ km/s} = 80.9\text{ days}$.
* **Post-TMI Mass ($2,581.73\text{ t}$):** $a = 0.220\text{ mm/s}^2 = 22.43\text{ }\mu g$. Time to accumulate $1\text{ km/s} = 52.6\text{ days}$.
* **Post-TEI Mass ($1,467.27\text{ t}$):** $a = 0.387\text{ mm/s}^2 = 39.48\text{ }\mu g$. Time to accumulate $1\text{ km/s} = 29.9\text{ days}$.

### Trajectory Finding:
Because low-thrust acceleration ($22.4\text{ }\mu g$) is four orders of magnitude smaller than planetary gravitational acceleration at LEO/LMO, **NEP cannot perform high-energy orbital escape or capture without incurring severe spiraling gravity losses ($>1.5\text{ km/s}$)**.
Therefore, high-thrust NTP ($4,000\text{ kN}$, $a \approx 1.0 - 2.7\text{ m/s}^2 = 0.10 - 0.28\text{ g}$) must handle all planetocentric escape/capture maneuvers (TMI, MOI, TEI, EOI). NEP is used exclusively for continuous heliocentric trajectory shaping during cruise.

---

## 4. Earth-Mars Synodic Alignment & 640-Day Stay Analysis

* **Earth Orbital Period ($T_E$):** $365.256\text{ days}$ ($1.000\text{ yr}$).
* **Mars Orbital Period ($T_M$):** $686.980\text{ days}$ ($1.881\text{ yr}$).
* **Synodic Period ($S$):**
  $$\frac{1}{S} = \frac{1}{T_E} - \frac{1}{T_M} \implies S = 779.9\text{ days} \quad (\mathbf{2.135\text{ years}})$$

### Return Window Geometry:
For a round-trip mission returning to Earth, the vehicle must wait at Mars until the orbital phase angle $\phi$ between Earth and Mars aligns for the return transfer.
* **Ideal Hohmann Return Stay:** $S - 2 T_{transit} = 779.9 - 2(258.9) = \mathbf{262.1\text{ days}}$.
* **Fast 180-day Transit Return Stay:** $S - 2(180) = 779.9 - 360.0 = \mathbf{419.9\text{ days}}$.
* **Declared Extended Conjunction Stay:** $640.0\text{ days}$.

The declared $640\text{ day}$ Mars stay represents an **extended conjunction mission**, allowing full surface exploration and waiting for the next-plus-one optimal return window.

---

## 5. Return Trajectory & Earth Capture Evaluation

### Return Velocity Budget:
* **TEI (NTP):** Consumes remaining $318.61\text{ t}$ $\text{LH}_2$, delivering $1.734\text{ km/s}$ $\Delta v$.
* **Inbound Cruise (NEP):** Consumes remaining $42.58\text{ t}$ $\text{LNH}_3$, delivering $1.011\text{ km/s}$ $\Delta v$.
* **Total Available Return Velocity:** $2.745\text{ km/s}$.

### Required Return Velocity (180-day Fast Return):
* **TEI Requirement:** $1.800\text{ km/s}$.
* **Inbound Cruise Requirement:** $2.550\text{ km/s}$.
* **EOI Propulsive Capture Requirement:** $1.200\text{ km/s}$.
* **Total Required Return Velocity:** $5.550\text{ km/s}$.

### Trajectory Conclusion:
The spacecraft faces a **$-2.805\text{ km/s}$ return velocity deficit** for a 180-day fast propulsive return.
To close the return trajectory, the program must either:
1. Extend the return transit to a low-energy 260-day Hohmann return arc.
2. Adopt Mars ISRU refueling ($+500\text{ t}$ $\text{LH}_2$ loaded at Mars).
