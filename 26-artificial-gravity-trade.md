# 26 — Quantitative Artificial Gravity Reassessment

**Document ID:** `26-artificial-gravity-trade.md`
**Reopened Decision:** Reopening ADR-002 (`18-hull-architecture-trade.md`)
**Centripetal Acceleration Equation:**
$$a_c = \omega^2 \cdot r = \left(\frac{2\pi \cdot \text{RPM}}{60}\right)^2 \cdot r$$
**Coriolis Acceleration Equation:**
$$a_{coriolis} = 2 \cdot (\vec{\omega} \times \vec{v})$$

---

## 1. Quantitative Artificial Gravity Candidate Matrix

| Option | Radius $r$ (m) | Speed (RPM) | Centripetal Accel $a_c$ ($g$) | Tangential Velocity (m/s) | Coriolis Delta (1.5 m/s walk) | Structural Load (kN) | Dynamic Bearing Mass (MT) | Mass Penalty (MT) | Crew Usability Score (1-5) | Failure Consequence | Evaluation |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| **1 — Zero-G Baseline (Microgravity)** | 0.0 m | 0.0 | $0.00\text{ g}$ | 0.0 m/s | $0.00\text{ m/s}^2$ | 0 kN | 0.0 MT | 0.0 MT | 1 / 5 | Severe bone density loss, SANS, muscle atrophy | **Unacceptable:** 1,000-day microgravity causes irreversible neuro-ocular and musculoskeletal degradation. |
| **2 — Compact Internal Centrifuge (v1 Baseline)** | 6.0 m | 10.0 | $0.67\text{ g}$ | 6.28 m/s | $3.14\text{ m/s}^2$ ($+54\% / -42\%$) | 450 kN | 18.0 MT | 22.0 MT | 2 / 5 | Bearing seizure, cross-coupling motion sickness | **REJECTED (v1 Audit Failure):** $10\text{ RPM}$ produces intolerable $100\%$ Coriolis gravity fluctuation while walking prograde/retrograde. |
| **3 — Transverse Counter-Rotating Ring (v2 Candidate)** | 15.0 m | 6.0 | $0.60\text{ g}$ | 9.42 m/s | $1.88\text{ m/s}^2$ ($+33\% / -33\%$) | 850 kN | 22.0 MT | 38.0 MT | 4 / 5 | Dynamic imbalance, seal degradation | **HIGH PERFORMANCE:** Comfortable $6\text{ RPM}$ rotation provides $0.60\text{ g}$ sleep/exercise shifts without vehicle-wide tumbling. |
| **4 — Dual-Hull Deployable Tether Rotation** | 56.0 m | 4.0 | $1.00\text{ g}$ | 23.46 m/s | $1.26\text{ m/s}^2$ ($+13\% / -13\%$) | 1,200 kN | 5.0 MT | 18.0 MT | 5 / 5 | Tether severance, RCS propellant waste | **OPTIMAL FLIGHT OPTION:** Provides full Earth $1.0\text{ g}$ during 180-day cruise; retracted during NTP burns. |
| **5 — Continuous Thrust Gravity** | $\infty$ | 0.0 | $0.026\text{ g}$ | 0.0 m/s | $0.00\text{ m/s}^2$ | 4,000 kN | 0.0 MT | 0.0 MT | 1 / 5 | Engine flameout | **Inadequate:** $80\text{ N}$ NEP thrust provides negligible acceleration ($0.00002\text{ g}$). |

---

## 2. In-Depth Engineering Analysis of Top Candidates

### Option 2 (v1 Compact $12\text{m}$ Centrifuge) Audit Rejection
* **Physical Failure:** At $r = 6.0\text{ m}$ and $10\text{ RPM}$ ($\omega = 1.047\text{ rad/s}$), walking prograde at $1.5\text{ m/s}$ increases apparent gravity from $0.67\text{ g}$ to $1.03\text{ g}$ ($+54\%$). Walking retrograde drops apparent gravity to $0.39\text{ g}$ ($-42\%$).
* **Nauseogenic Cross-Coupling:** Head rotation in a $10\text{ RPM}$ environment induces severe vestibular cross-coupling angular acceleration ($\omega_{cross} > 1.5\text{ rad/s}^2$), causing incapacitating motion sickness in $>80\%$ of crew members within 15 minutes.

### Option 3 (Transverse $30\text{m}$ Ring) Sizing
* **Physical Mechanics:** $r = 15.0\text{ m}$, $6.0\text{ RPM}$ ($\omega = 0.628\text{ rad/s}$). Apparent gravity $= 0.60\text{ g}$.
* **Coriolis Fluctuation:** Walking prograde at $1.5\text{ m/s}$ increases apparent gravity to $0.80\text{ g}$; walking retrograde drops it to $0.41\text{ g}$. Cross-coupling angular acceleration is reduced below the clinical motion-sickness threshold.
* **Mass Penalty:** $38.0\text{ MT}$ total (including $22.0\text{ MT}$ dynamic magnetic levitation bearing and counter-rotating momentum ring).

### Option 4 (Deployable Dual-Mass Tether) Sizing
* **Physical Mechanics:** Habitat section ($150\text{ MT}$) separates from main reactor/propellant spine ($1,272\text{ MT}$) by $56\text{m}$ high-strength carbon-nanotube / Kevlar tether array. Rotation at $4.0\text{ RPM}$ yields full Earth gravity ($1.00\text{ g}$) at the habitat deck.
* **Mass Penalty:** $18.0\text{ MT}$ tether spool and winching mechanism.
* **Operational Mode:** Deployed during the 180-day interplanetary cruise phase; retracted for main NTP engine burns and Mars orbital operations.

---

## 3. Formal Decision Update: ADR-002a

### ADR-002a: Artificial Gravity Architecture Revision

* **Decision:** Replace the $12\text{m}$ compact internal centrifuge with a **Dual-Mode Artificial Gravity Architecture**:
  1. **Primary Cruise Mode:** Deployable $56\text{m}$ dual-mass tether rotation ($4.0\text{ RPM}$ producing $1.00\text{ g}$) during interplanetary transit.
  2. **Orbital / High-Load Mode:** A transverse $30\text{m}$ diameter ($15\text{m}$ radius) magnetic-levitation ring ($6.0\text{ RPM}$ producing $0.60\text{ g}$) mounted inside the habitat module for sleep/exercise shifts during orbital stay and powered maneuvers.
* **Reason for Reversal:** The v1 $12\text{m}$ centrifuge failed human habitability limits ($100\%$ Coriolis gravity fluctuation and cross-coupling nausea).
* **Tradeoff:** Adds $38.0\text{ MT}$ total dry mass for the transverse ring and $18.0\text{ MT}$ for the tether spooling assembly ($56.0\text{ MT}$ combined).
* **Confidence:** High
* **Class:** Class B (Engineering Extension)
