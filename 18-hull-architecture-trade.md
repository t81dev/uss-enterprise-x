# 18 — Hull Architecture Trade Study

**Document ID:** `18-hull-architecture-trade.md`
**Purpose:** Quantitative evaluation and selection of primary hull geometry for Project Occam-7
**Evaluated Configurations:** Option A (Integrated Monocoque Cylinder), Option B (Central Spine with Separated Habitat & Propulsion Modules), Option C (Enterprise-Inspired Distributed Architecture)

---

## 1. Executive Summary

This trade study evaluates three competing structural configurations for the Project Occam-7 baseline vehicle against strict mass, thermal, structural, radiation, manufacturing, and operational constraints. The goal is to determine whether the familiar Enterprise silhouette (saucer, pylons, nacelles) survives first-principles engineering scrutiny, or if a different architecture naturally emerges from the physical constraints.

**Selected Architecture:** **Option B (Modular Central Spine with Separated Habitat & Propulsion Modules)**
Option B achieves the highest overall system performance score, resolving the core structural, thermal, and nuclear radiation shielding contradictions that disqualify Option A and Option C.

---

## 2. Architectural Candidates

### Candidate A: Integrated Cylindrical Monocoque
* **Description:** Single continuous large-diameter ($12\text{m}$ diameter) stainless-steel cylindrical shell containing habitat, propellant tankage, and reactor sections in one unified monocoque pressure hull.
* **Inspiration:** Extended SpaceX Starship / Skylab monolith architecture.

### Candidate B: Modular Central Spine (Long-Axis Architecture)
* **Description:** A linear structural truss spine ($380\text{m}$ length) with high-radiation nuclear propulsion and thermal radiators mounted at the aft end, massive liquid propellant tanks in the center acting as a shadow shield, and a pressurized habitat cylinder with an optional rotating ring centrifuge at the forward end.
* **Inspiration:** NASA Mars Transfer Vehicle / Discovery One architectural principles.

### Candidate C: Enterprise-Inspired Distributed Architecture
* **Description:** A classic 3-component geometry: forward disk/saucer primary hull containing habitat and bridge, narrow connecting pylons/neck, and twin outboard propulsion nacelles housing nuclear/fusion reactors and engines.
* **Inspiration:** Original TOS / Refit USS Enterprise silhouette.

---

## 3. Evaluation Matrix

Scoring scale: 1 (Unacceptable / High Risk) to 5 (Optimal / Outstanding). Weights sum to 100%.

| Evaluation Criteria | Weight | Option A (Cylinder) | Option B (Spine Axis) | Option C (Enterprise Form) | Selection Drivers & Notes |
|---|---|---|---|---|---|
| **Structural Mass Efficiency** | $15\%$ | **5** (0.75) | **4** (0.60) | **1** (0.15) | Pylons in Option C suffer severe cantilever bending loads during thrust. |
| **Radiation Protection Efficiency** | $15\%$ | **2** (0.30) | **5** (0.75) | **2** (0.30) | Option B uses distance ($1/r^2$) + propellant tanks as massive shadow shield. |
| **Thermal Radiator Integration** | $15\%$ | **2** (0.30) | **5** (0.75) | **1** (0.15) | Option B provides $380\text{m}$ spine for $11,000+\text{ m}^2$ unimpeded radiator area. |
| **Artificial Gravity Compatibility** | $10\%$ | **2** (0.20) | **4** (0.40) | **2** (0.20) | Option B allows low-mass transverse centrifuge or tether rotation. |
| **MMOD & Shielding Safety** | $10\%$ | **3** (0.30) | **4** (0.40) | **1** (0.10) | Option C exposes large frontal saucer area to debris vector. |
| **Manufacturing & Modular Assembly**| $15\%$ | **4** (0.60) | **5** (0.75) | **2** (0.30) | Option B uses standardized modular cassettes launched in standard fairings. |
| **Maintainability & Access** | $10\%$ | **2** (0.20) | **4** (0.40) | **2** (0.20) | Option B isolates dirty reactor maintenance from crew quarters. |
| **Crew Survivability & Abort Modes** | $10\%$ | **3** (0.30) | **5** (0.50) | **2** (0.20) | Option B habitat can detach as emergency life pod from main spine. |
| **WEIGHTED TOTAL SCORE** | **100%** | **2.95 / 5.0** | **4.55 / 5.0** | **1.60 / 5.0** | **WINNER: OPTION B** |

---

## 4. Hostile Analysis of Candidate C (Enterprise Form)

Why the classic Enterprise geometry collapses under first-principles physics:

1. **Catastrophic Pylon Bending Moments:** Cantilevering twin multi-hundred-ton propulsion nacelles on narrow structural pylons creates extreme bending moments ($>10^8\text{ N}\cdot\text{m}$) during main engine acceleration and RCS maneuvers. Reinforcing the pylons requires thousands of metric tons of dead structural mass.
2. **Radiation Exposure Overhead:** Mounting reactors in outboard nacelles exposes the central saucer habitat to line-of-sight scatter radiation unless heavy $360^\circ$ spherical shields ($>200\text{ MT}$) are installed around each nacelle, destroying the vehicle mass budget.
3. **Radiator Area Deficit:** Outboard nacelles lack the surface area required for $80+\text{ MWth}$ thermal rejection. Mounting large radiator panels on nacelles causes plume impingement and structural flutter.
4. **Hydrostatic Pressure Loss:** The wide disk saucer hull requires massive internal web frames to contain $1.0\text{ atm}$ internal pressure without ballooning, whereas cylindrical pressure vessels in Option A and B achieve optimal hoop stress distribution with minimal skin thickness.

---

## 5. Formal Architecture Decision Records (ADRs)

### ADR-001: Primary Vehicle Structural Configuration

* **Decision:** Adopt Option B (Modular Central Spine / Long-Axis Architecture) as the baseline hull geometry for Project Occam-7.
* **Alternatives Considered:** Integrated Monocoque Cylinder (Option A), Enterprise-Inspired Distributed Saucer/Pylon Geometry (Option C).
* **Reason:** Option B maximizes reactor-to-habitat distance ($380\text{m}$ separation), reducing reactor shadow shield mass by $>120\text{ MT}$ via $1/r^2$ attenuation and using $2,500\text{ MT}$ of liquid propellant as an intermediate radiation shield. It provides an ideal linear spine for mounting $11,160\text{ m}^2$ of thermal radiators without structural interference.
* **Tradeoff:** Option B requires orbital docking assembly of 4–6 modular spine segments compared to the single launch potential of Option A.
* **Confidence:** High
* **Reality Classification:** Class B (Engineering Extension)
* **Revisit Trigger:** Demonstration of compact room-temperature fusion power with zero neutron emissions or ultra-high-density electromagnetic force fields that eliminate thermal radiator and physical shielding requirements.

---

### ADR-002: Artificial Gravity Strategy

* **Decision:** Implement a dual-mode artificial gravity baseline: linear thrust gravity during NTP/NEP burns, supplemented by a compact internal counter-rotating transverse centrifuge ($12\text{m}$ diameter at $10\text{ RPM}$ yielding $\sim 0.68\text{ g}$) in the forward habitat for sleep/exercise shifts during cruise.
* **Alternatives Considered:** Full-vehicle tumbling tether rotation, zero-g microgravity baseline with exercise countermeasures, continuous 1-g FTL acceleration.
* **Reason:** Full-vehicle tumbling creates severe RCS propellant consumption and complex antenna/solar tracking, while microgravity causes irreversible neuro-ocular and musculoskeletal degradation on 1,000-day missions. An internal counter-rotating centrifuge eliminates net angular momentum while protecting critical crew physiology.
* **Tradeoff:** Adds $\sim 18\text{ MT}$ of mechanical bearing, slip-ring, and drive mechanism mass to the habitat section.
* **Confidence:** Medium
* **Reality Classification:** Class B (Engineering Extension)
* **Revisit Trigger:** Human clinical trials proving pharmaceutical or genetic countermeasures fully prevent microgravity bone loss and SANS (Spaceflight-Associated Neuro-ocular Syndrome).

---

### ADR-003: Radiation Shielding Strategy

* **Decision:** Implement a multi-layered passive/active hybrid strategy using water/wastewater circumferential tanks ($25\text{ g/cm}^2$) around crew quarters, a central storm shelter ($>45\text{ g/cm}^2$), and liquid hydrogen main propellant tanks positioned along the primary axis between the nuclear reactor and the habitat.
* **Alternatives Considered:** Dedicated tungsten/lead solid shielding, active high-voltage electrostatic shielding, room-temperature superconducting magnetic shields.
* **Reason:** Dedicated solid shielding adds dead mass. Positioning consumable water, food, and propellant in the line of sight provides dual-use radiation protection without mass penalties.
* **Tradeoff:** Shielding effectiveness degrades as liquid hydrogen propellant is consumed during the mission, requiring crew to move into the central water-shielded storm shelter during late-mission solar flare events.
* **Confidence:** High
* **Reality Classification:** Class A/B
* **Revisit Trigger:** Development of lightweight ($<5\text{ kg/m}^2$) high-field ($>5\text{ Tesla}$) superconducting magnetic coils for active charged particle deflection.
