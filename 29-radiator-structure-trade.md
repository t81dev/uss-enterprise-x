# 29 — Quantitative Radiator-Structure Trade Study

**Document ID:** `29-radiator-structure-trade.md`
**Primary Structural Driver:** Thermal radiator survivability under launch, main NTP engine acceleration ($0.10\text{ g} - 0.29\text{ g}$), orbital assembly, MMOD hypervelocity impact, and $830\text{ K}$ thermal expansion gradients.

---

## 1. Quantitative Comparison of Radiator Architectural Concepts

| Concept Candidate | Specific Mass (kg/m²) | Operational Complexity | MMOD Vulnerability | Acceleration Tolerance | Thermal Expansion Compliance | Mechanical Risk Level | Class | Selection Evaluation |
|---|---:|---|---|---|---|---|---|---|
| **1 — Fixed Hull Surface Radiators** | 2.5 kg/m² | Very Low | Moderate | High ($>5.0\text{ g}$) | Low (Buckling risk) | Low | Class A | **Inadequate Surface Area:** Hull area is insufficient for $83.4\text{ MWth}$ rejection ($2,878\text{ m}^2$). |
| **2 — Deployable Composite Panels (Selected Baseline)** | 1.8 kg/m² | Moderate | Low (Segmented isolation) | Moderate ($1.0\text{ g}$) | High (Flexible loops) | Medium | Class B | **OPTIMAL WINNER:** Folds into standard launch fairings; deploys along spine with dual guy-wire support. |
| **3 — Rigid Heat-Pipe Wing Arrays** | 2.2 kg/m² | Low | Moderate | High ($2.0\text{ g}$) | Medium | Low | Class B | **Heavy:** Rigid structural spars add $12\text{ MT}$ dead mass compared to deployable panels. |
| **4 — Liquid-Droplet Radiators (LDR)** | 0.4 kg/m² | Extreme | High (Droplet loss/drift) | Extremely Low ($<0.001\text{ g}$) | High | High | Class C | **Rejected:** Fluid droplets drift away during main-engine acceleration burns or RCS firings. |
| **5 — Rotating Radiator Structures** | 3.2 kg/m² | Extreme | High (Seal failure) | Low ($0.05\text{ g}$) | Low | High | Class C | **Rejected:** Heavy dynamic rotating seals fail rapidly under $850\text{ K}$ NaK fluid conditions. |
| **6 — Sacrificial / Redundant Cassette Arrays** | 1.9 kg/m² | Low | Very Low (N+2 redundancy) | Moderate ($1.0\text{ g}$) | High | Low | Class B | **Selected Sub-Feature:** Individual $2\text{m} \times 4\text{m}$ panels can be isolated pyrotechnically when struck by MMOD. |

---

## 2. Radiator Load Case Survival Analysis

```
       +-------------------------------------------------------------------------+
       |                           MAIN ENGINE BURN LOAD                         |
       |  Axial Thrust Acceleration: 0.10 g --> Radiator Wing Deflection: <12 cm |
       |  Guy-wire Tension: 18.5 kN        --> Stress Margin: > 4.5x             |
       +-------------------------------------------------------------------------+
                                            |
                                            v
       +-------------------------------------------------------------------------+
       |                           MMOD IMPACT EVENT                             |
       |  Impactor: 1 cm @ 12 km/s         --> Auto-Isolate Panel Cassette       |
       |  Isolation Time: < 200 ms         --> Core Thermal Rejection Loss: 0.28%|
       +-------------------------------------------------------------------------+
```

### A — Launch & Fairing Packaging Phase
* **Constraint:** Radiators must fit within $12.0\text{ m}$ diameter launch vehicle fairings.
* **Mechanism:** 360 individual $2.0\text{m} \times 4.0\text{m}$ panels fold accordion-style into 8 compact radiator cassettes ($4.0\text{m} \times 4.0\text{m} \times 6.0\text{m}$ each) for orbital launch.

### B — Orbital Deployment & Assembly
* **Mechanism:** Automated electric winches extend carbon-composite deployment booms laterally from spine nodes at $X = 70\text{m}$ and $X = 320\text{m}$.
* **Deployment Lock:** Pyrotechnic locking pins engage dual triangular high-modulus Kevlar guy-wires, providing stiffness against transverse vibration.

### C — Main Engine Burns & Acceleration ($0.10\text{ g} - 0.29\text{ g}$)
* **Thrust Loading:** NTP engine acceleration ($4,000\text{ kN}$) acts along the $+\text{X}$ axis.
* **Wing Deflection:** $110\text{m}$ radiator wing cantilever deflection under $0.29\text{ g}$ maximum dry acceleration is limited to $11.8\text{ cm}$ at the wingtip by the guy-wire tension network ($18.5\text{ kN}$ cable tension), preventing structural flutter or resonance with engine turbopump frequencies ($120\text{ Hz}$).

### D — Thermal Expansion Gradient ($\Delta T = 830\text{ K}$)
* **Mechanism:** Flexible titanium braided bellows at the manifold-to-boom interface absorb $0.85\text{m}$ axial expansion of the hot NaK fluid loop without transferring thermal shear loads to deployable composite radiator panels.

### E — Micrometeoroid & Orbital Debris (MMOD) Hypervelocity Impact
* **Impact Scenario:** $1\text{ cm}$ aluminum sphere at $12.0\text{ km/s}$ strikes Radiator Cassette No. 14.
* **Containment Protocol:** High-speed pressure drop sensors trigger micro-pyrotechnic shutoff valves in $<200\text{ ms}$, isolating the compromised 8-panel cassette loop ($24\text{ m}^2$, $0.28\%$ of total area).
* **System Degradation:** Remaining 352 panels easily absorb the diverted thermal load using the $15.0\%$ baseline design margin without requiring reactor throttling.
