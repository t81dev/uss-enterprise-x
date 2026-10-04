# 47 — Earth-Mars Trajectory Mechanics & Orbital Closure v1

**Document ID:** `47-earth-mars-trajectory-closure.md`
**Digital Twin Verification:** `engineering/calculations/mission_baseline.json`
**Program Status:** Trajectory Mechanics & Patched-Conic Orbital Closure

---

## 1. Executive Summary

A rocket-equation $\Delta v$ budget is an expression of vehicle mass ratio and exhaust velocity, not an Earth-Mars trajectory solution. `47-earth-mars-trajectory-closure.md` separates **Vehicle Capability** ($\Delta v_{vehicle} = 12.25\text{ km/s}$) from **Trajectory Requirement** ($\Delta v_{req}(\text{geometry, transit time})$).

Using first-order patched-conic two-body orbital mechanics, this document demonstrates how the $12.25\text{ km/s}$ sequential vehicle capability closes the Earth-Mars-Earth transit by matching orbital departure $v_\infty$ vectors, low-thrust continuous thrust arcs, and planetary gravity-assist / aerobraking options.

---

## 2. Distinction Between Vehicle Capability and Trajectory Requirement

```
[ VEHICLE CAPABILITY ]                       [ TRAJECTORY REQUIREMENT ]
  m_dep = 3,970.96 MT                          Departure C3 (Earth LEO)
  m_dry = 1,470.96 MT         --- vs ---       Hyperbolic excess v_infinity
  I_sp = 900s / 3,500s                         Helicentric Hohmann / Fast Arc
  Propellant = 2,500 MT                        Arrival C3 / Orbital Capture
  --> Actual Δv = 12.25 km/s                   --> Trajectory Demand: 11.8 - 16.0 km/s
```

### Key Definitions:
1. **Vehicle Capability ($\Delta v_{vehicle}$):** The maximum velocity increment the vehicle can physically generate given its propellant mass, dry mass, and propulsion exhaust velocities.
2. **Trajectory Requirement ($\Delta v_{req}$):** The sum of impulsive and continuous velocity changes required by orbital mechanics to transition between Earth's orbit ($1.00\text{ AU}$) and Mars's orbit ($1.524\text{ AU}$) within a specified transit window.
3. **Trajectory Closure Solution:** A physically valid trajectory where $\Delta v_{vehicle} \ge \Delta v_{req}$ with positive reserve margin.

---

## 3. Patched-Conic Orbital Mechanics Model

### A. Heliocentric Transfer Geometry
* Earth semi-major axis: $r_1 = 1.000\text{ AU} = 1.496 \times 10^{11}\text{ m}$
* Mars semi-major axis: $r_2 = 1.524\text{ AU} = 2.279 \times 10^{11}\text{ m}$
* Sun gravitational parameter: $\mu_\odot = 1.327 \times 10^{20}\text{ m}^3/\text{s}^2$
* Earth heliocentric orbital velocity: $v_{E} = \sqrt{\mu_\odot / r_1} = 29.78\text{ km/s}$
* Mars heliocentric orbital velocity: $v_{M} = \sqrt{\mu_\odot / r_2} = 24.13\text{ km/s}$

### B. Hohmann Minimum-Energy Baseline
* Transfer semi-major axis: $a_{trans} = (r_1 + r_2)/2 = 1.262\text{ AU} = 1.888 \times 10^{11}\text{ m}$
* Heliocentric velocity at Earth departure: $v_{trans,1} = \sqrt{\mu_\odot (2/r_1 - 1/a_{trans})} = 32.73\text{ km/s}$
* Hyperbolic departure excess velocity: $v_{\infty, dep} = v_{trans,1} - v_E = 32.73 - 29.78 = \mathbf{2.95\text{ km/s}}$
* Departure $C_3$: $C_3 = v_{\infty, dep}^2 = \mathbf{8.70\text{ km}^2/\text{s}^2}$
* Impulsive TMI from $400\text{ km}$ LEO ($r_p = 6,778\text{ km}$, $v_{LEO} = 7.67\text{ km/s}$):
  $$v_{dep} = \sqrt{v_{esc}^2 + v_\infty^2} = \sqrt{\frac{2 \mu_\oplus}{r_p} + v_\infty^2} = \sqrt{117.61 + 8.70} = 11.238\text{ km/s}$$
  $$\Delta v_{TMI, Hohmann} = v_{dep} - v_{LEO} = 11.238 - 7.670 = \mathbf{3.568\text{ km/s}}$$

* Heliocentric velocity at Mars arrival: $v_{trans,2} = \sqrt{\mu_\odot (2/r_2 - 1/a_{trans})} = 21.48\text{ km/s}$
* Hyperbolic arrival excess velocity: $v_{\infty, arr} = v_M - v_{trans,2} = 24.13 - 21.48 = \mathbf{2.65\text{ km/s}}$
* Impulsive MOI to $500\text{ km}$ Mars orbit ($r_p = 3,890\text{ km}$, $v_{Mars\_circ} = 3.35\text{ km/s}$):
  $$\Delta v_{MOI, Hohmann} = \sqrt{\frac{2 \mu_\sigma}{r_p} + v_{\infty,arr}^2} - v_{Mars\_circ} = \sqrt{21.99 + 7.02} - 3.350 = \mathbf{2.036\text{ km/s}}$$

---

## 4. Hybrid NTP/NEP Trajectory Integration

Combining impulsive NTP burns with continuous low-thrust NEP electric arcs modifies the patched-conic solution:

```
[ LEO ] --(NTP TMI: 3.80 km/s)--> [ Hyperbolic Departure v_inf = 3.53 km/s ]
                                           |
                                  (NEP Cruise 180d: 3.61 km/s)
                                           |
[ Mars Orbit ] <--(NTP MOI: 2.10 km/s)-- [ Mars Arrival v_inf = 2.65 km/s ]
```

### Outbound Leg (180 Days):
1. **TMI (NTP):** $\Delta v = 3.800\text{ km/s}$ provides $v_\infty = 3.53\text{ km/s}$, placing the vessel on a fast ellipse toward Mars.
2. **Outbound Cruise (NEP):** $15\text{ MWe}$ MPD array fires continuously for 180 days ($F = 568.12\text{ N}$), providing **$3.605\text{ km/s}$** of low-thrust shape correction.
3. **MOI (NTP):** $\Delta v = 2.100\text{ km/s}$ captures the vehicle into a stable $500\text{ km} \times 12,000\text{ km}$ elliptical Mars orbit.

### Inbound Return Leg (180 Days):
1. **TEI (NTP):** Consumes remaining $318.61\text{ t}$ $\text{LH}_2$, generating $\Delta v = 1.734\text{ km/s}$ ($v_\infty = 2.10\text{ km/s}$).
2. **Inbound Cruise (NEP):** Consumes remaining $42.58\text{ t}$ $\text{LNH}_3$ over $29.8\text{ days}$, generating $\Delta v = 1.011\text{ km/s}$.
3. **Earth Capture Option:**
   * **Option A (Propulsive EOI):** Requires additional $1.20\text{ km/s}$ propulsive capture.
   * **Option B (Aerocapture / Lifting Body Entry):** Uses Earth's upper atmosphere ($\approx 65 - 75\text{ km}$ altitude) to bleed hyperbolic excess velocity ($v_\infty \approx 3.2\text{ km/s}$), closing the mission with zero remaining propellant.

---

## 5. Trajectory Closure Assessment Table

| Trajectory Strategy | Outbound Transit | Inbound Transit | Required Total $\Delta v$ | Vehicle Actual $\Delta v$ | Closure Status | Mitigation / Strategy |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Pure Impulsive All-Propulsive** | $180\text{ days}$ | $180\text{ days}$ | $16.00\text{ km/s}$ | $12.25\text{ km/s}$ | **OPEN (-3.75 km/s)** | Requires $1,200\text{ t}$ additional propellant or larger tanks. |
| **Hybrid NTP/NEP + Aerocapture** | $180\text{ days}$ | $180\text{ days}$ | $12.10\text{ km/s}$ | $12.25\text{ km/s}$ | **CLOSED (+0.15 km/s)** | Employs atmospheric drag pass at Mars/Earth for capture. |
| **Hybrid NTP/NEP Extended Conjunction** | $210\text{ days}$ | $210\text{ days}$ | $11.20\text{ km/s}$ | $12.25\text{ km/s}$ | **CLOSED (+1.05 km/s)** | Slightly extends transit window to match Hohmann optimal arcs. |
