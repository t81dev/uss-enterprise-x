# 23 — Integrated Thermal Budget v2

**Document ID:** `23-thermal-budget-v2.md`
**Primary Thermodynamics Governing Equation:** Stefan-Boltzmann Radiative Rejection
$$P_{rad} = 2 \cdot A_{panel} \cdot \epsilon \cdot \sigma \cdot T^4$$
where $\sigma = 5.670374419 \times 10^{-8}\text{ W/(m}^2\text{K}^4)$, emissivity $\epsilon = 0.88 - 0.90$, $T$ is temperature in Kelvin, and double-sided radiation factor $= 2$.

---

## 1. Waste Heat Inventory & Radiator Sizing

| Subsystem Waste Source | Waste Heat $Q_{th}$ (kWth) | Operating Temp $T$ (K) | Emissivity $\epsilon$ | Radiated Flux (kW/m² single side) | Required Footprint Area $A_{panel}$ (m²) | Dry Radiator Mass (MT) | Cooling Loop Fluid Mechanism |
|---|---:|---:|---:|---:|---:|---:|---|
| **Main Nuclear Core Waste Heat** | 80,000.0 | 850 K | 0.90 | 26.64 | 1,726.7 | 3.11 | Liquid NaK ($783\text{ K} - 873\text{ K}$) Heat Pipes |
| **NEP Power Conversion Losses** | 3,000.0 | 650 K | 0.90 | 9.11 | 189.4 | 0.28 | Carbon-composite / Potassium Heat Pipes |
| **Avionics & Compute Bus** | 50.0 | 320 K | 0.88 | 0.52 | 54.9 | 0.12 | Deionized Water Heat Pipes |
| **Habitat Life Support & HVAC** | 200.0 | 295 K | 0.88 | 0.38 | 304.3 | 0.76 | Dual-loop Ammonia / Water heat exchangers |
| **ECLSS Recycling Loop** | 120.0 | 310 K | 0.88 | 0.46 | 149.7 | 0.33 | Water / Glycol loop |
| **Scientific Workshop & Payload** | 80.0 | 330 K | 0.88 | 0.59 | 77.7 | 0.16 | Local Heat Pipes |
| **SUBTOTAL UNMARGINED** | **83,450.0** | **—** | **—** | **—** | **2,502.8** | **4.76** | **Integrated Rejection Loops** |
| **System Margin (+15% Degradation/MMOD)**| — | — | — | — | 375.4 | 1.90 | Micrometeoroid degradation allocation |
| **TOTAL THERMAL MANAGEMENT SYSTEM** | **83,450.0** | **—** | **0.90 avg** | **—** | **2,878.2 m²** | **26.66 MT** | **Dry Panels (6.66t) + Booms/Fluid (20.0t)** |

---

## 2. Radiator Panel Geometry & Deployment Mechanics

```
====================================== CENTRAL SPINE (380m) ======================================
                      |                                              |
     [HABITAT & ECLSS RADIATORS]                     [MAIN REACTOR HIGH-TEMP RADIATORS]
     (295K-330K, 666 m² footprint)                   (850K NaK, 1,727 m² footprint)
     2x Wings (40m length x 8.3m width)             2x Wings (110m length x 7.85m width)
                      |                                              |
==================================================================================================
```

* **Individual Panel Sizing:** Standardized $2.0\text{m} \times 4.0\text{m}$ deployable composite heat-pipe cassettes. Total panel count: 360 panels.
* **Deployable Boom Layout:** Radiators deploy laterally in two planar wings along non-thrust axes to minimize solar flux trapping and thrust plume impingement.
* **High-Temperature Reactor Array:** $110\text{m}$ length along aft spine $\times 7.85\text{m}$ width per wing ($1,727\text{ m}^2$).
* **Low-Temperature Habitat Array:** $40\text{m}$ length along forward spine $\times 8.33\text{m}$ width per wing ($666\text{ m}^2$).
* **Total Spine Footprint Occupied:** $150\text{m}$ along the $380\text{m}$ central spine, fitting comfortably within vehicle axial length without overlapping propellant tanks or habitat windows.

---

## 3. Coolant Inventory & Transport Architecture

1. **Primary High-Temp Loop:** Sodium-Potassium eutectic ($\text{NaK-78}$, freezing point $-12.6^\circ\text{C}$, boiling point $785^\circ\text{C}$). Total fluid inventory: $8.5\text{ MT}$.
2. **Intermediate Transport Loop:** Heat pipes with sintered powder wicks and potassium working fluid transfer heat from reactor Brayton heat exchangers to deployable wing manifolds.
3. **Low-Temp Loop:** Anhydrous ammonia ($\text{NH}_3$) external loop isolated from pressurized habitat spaces via intermediate water/glycol heat exchangers ($4.5\text{ MT}$ fluid inventory).
4. **Emergency Thermal Storage Capacity:** Phase-Change Material (PCM) paraffin / lithium fluoride thermal storage sinks ($15\text{ GJ}$ capacity) capable of absorbing $30\text{ minutes}$ of unrejected core heat during sudden radiator manifold isolation events.

---

## 4. Radiator Integration & Geometric Verification

* **Geometric Fit Confirmation:** The required $2,878.2\text{ m}^2$ panel footprint requires $150\text{m}$ of linear axial length along the $380\text{m}$ spine truss.
* **Conclusion:** The quantitative radiator architecture fits cleanly on the modular central spine without requiring hull modifications or extra boom extensions.
