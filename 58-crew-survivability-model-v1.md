# 58 — Crew Survivability, Radiation & Centrifuge Dynamic Model v1

**Document ID:** `58-crew-survivability-model-v1.md`
**Digital Twin Source:** `engineering/calculations/mission_digital_twin.py`
**Program Status:** Quantitative Crew Health, Dynamic Radiation & Life-Support Verification Complete

---

## 1. Executive Summary

`58-crew-survivability-model-v1.md` details the quantitative crew survivability, environmental control, dynamic directional radiation protection, and artificial gravity model for the 24-person crew of the USS Enterprise X across its 850-day mission.

Rather than assuming crew health remains a static $100\%$ or assuming static scalar radiation dose rates, this model tracks crew health as a dynamic state variable dependent on time-dependent propellant tank depletion, $4\pi$ directional solid angles, Solar Particle Event (SPE) radiation storms, Galactic Cosmic Ray (GCR) background doses, reactor scatter flux, ECLSS consumable balances, habitat atmospheric pressure, thermal comfort, centrifuge microgravity decay, and centrifuge hardware reliability.

---

## 2. Dynamic Crew Health State Variable Definition

Crew Health $H_{crew}(t)$ is integrated as:

$$H_{crew}(t) = 100.0\% - \int_{0}^{t} \left( \dot{D}_{rad}(\tau) \cdot k_{rad} + \dot{L}_{ECLSS}(\tau) \cdot k_{ECLSS} + \dot{S}_{grav}(\tau) \cdot k_{grav} \right) d\tau$$

Where:
* $\dot{D}_{rad}$: Accumulated equivalent radiation dose rate ($\text{cSv/day}$), computed dynamically via `compute_dynamic_dose_rate()`.
* $\dot{L}_{ECLSS}$: ECLSS atmospheric / consumable deficiency factor.
* $\dot{S}_{grav}$: Physiological deconditioning rate due to zero-gravity / centrifuge failure ($0.05\%/\text{day}$ without artificial gravity).

---

## 3. Directional Radiation Protection & Dynamic Depletion Model

### A. Deep-Space Radiation Environment Baseline:
* **Unshielded GCR Background Rate:** $\approx 1.8\text{ mSv/day}$ ($0.18\text{ cSv/day}$ nominal; $0.24$ solar min; $0.14$ solar max).
* **Unshielded SPE Solar Flare Peak Rate:** Up to $10 - 50\text{ Sv/event}$ ($1,000 - 5,000\text{ cSv/event}$ free-space).

### B. Directional Solid Angle Weighting & Shielding Mass:
* **Radial/Circumferential Habitat Shielding:** $20.0\text{ g/cm}^2$ water buffer tanks $+ 6.4\text{ g/cm}^2$ 316L SS pressure hull $+ 5.0\text{ g/cm}^2$ internal racks ($31.4\text{ g/cm}^2$ total ambient). Covers $99.28\%$ of $4\pi$ sky ($\Omega_{radial} = 12.48\text{ sr}$).
* **Central SPE Storm Shelter Stack:** $52.25\text{ g/cm}^2$ column density ($4\text{m} \times 10\text{m}$ inner cylinder constructed of Steel + Water + High-Density Polyethylene + Steel). Attenuates SPE protons by $>98.5\%$ ($0.015$ factor). Verified life support ($125.7\text{ m}^3$ volume, $5.24\text{ m}^3/\text{crew}$, $1.5\text{ kWe}$ power, $3.9\text{ kWth}$ thermal load, $48\text{h}$ certified stay).
* **Axial Propellant Tank Buffer:** Subtends $\Omega_{axial} = 0.090\text{ sr}$ ($0.72\%$ of $4\pi$ sky). Provides dynamic axial reactor secondary attenuation when propellant is present ($\sigma_{axial} = 1,988\text{ g/cm}^2 \to 0\text{ g/cm}^2$).

### C. Mission Accumulated Crew Dose Results (Digital Twin Reconciled):
* **Trans-Mars Injection (TMI Burn):** $0.00\text{ cSv}$ (acute duration).
* **Outbound Transit NEP (180 days @ $0.041\text{ cSv/d}$ + 1 SPE Flare):** $54.75\text{ cSv}$.
* **Mars Orbit Insertion (MOI Burn):** $0.00\text{ cSv}$ (acute duration).
* **Mars Orbit / Surface Stay (640 days @ $0.028\text{ cSv/d}$ + 1 SPE Flare in Shelter):** $17.92\text{ cSv}$.
* **Trans-Earth Injection (TEI Burn):** $0.00\text{ cSv}$ (acute duration).
* **Inbound Transit NEP (29.8 days @ $0.039\text{ cSv/d}$):** $2.85\text{ cSv}$.
* **Earth Capture EOI Burn:** $0.01\text{ cSv}$ (acute duration).
* **Total Baseline Mission Accumulated Dose:** **$75.53\text{ cSv}$ ($0.755\text{ Sv}$)**.
* **NASA Career Limit Standard ($1,000\text{ mSv} = 100\text{ cSv}$):** Safety Margin = $+24.47\text{ cSv}$ ($24.47\%$) below career radiation safety ceiling.

---

## 4. Artificial Gravity & Transverse Centrifuge Dynamics

To eliminate long-term microgravity bone mineral density loss and neuro-vestibular degradation, the vessel incorporates a **$15.0\text{ m}$ radius transverse mag-lev centrifuge ring**.

### Centrifuge Dynamics Parameters:
* **Centrifuge Radius ($r$):** $15.0\text{ m}$.
* **Nominal Rotation Speed ($\omega$):** $6.0\text{ RPM} = 0.6283\text{ rad/s}$.
* **Centripetal Artificial Acceleration ($a_c$):**
  $$a_c = \omega^2 r = (0.6283)^2 \times 15.0 = \mathbf{5.922\text{ m/s}^2} = \mathbf{0.604\text{ g}}$$

### Walking Coriolis Acceleration & Radial Gradients:
When crew members walk inside the centrifuge ring at speed $v_{walk} = 1.5\text{ m/s}$:
* **Prograde Walking Acceleration:**
  $$a_{pro} = \frac{(\omega r + v_{walk})^2}{r} = \frac{(9.425 + 1.5)^2}{15.0} = \mathbf{7.957\text{ m/s}^2} = \mathbf{0.811\text{ g}}$$
* **Retrograde Walking Acceleration:**
  $$a_{ret} = \frac{(\omega r - v_{walk})^2}{r} = \frac{(9.425 - 1.5)^2}{15.0} = \mathbf{4.187\text{ m/s}^2} = \mathbf{0.427\text{ g}}$$
* **Comfort Limit Evaluation:** $a_{pro} / a_{ret}$ ratio ($1.9 \times$) is well within human neuro-vestibular adaptation limits for 6.0 RPM centrifuges.

---

## 5. Centrifuge Failure Mode & Crew Health Impact

If a centrifuge mechanical/mag-lev failure disables rotation for 30 days during cruise:
1. Artificial gravity drops from $0.60\text{ g}$ to $0.00\text{ g}$.
2. Microgravity health decay occurs at $0.05\%/\text{day}$.
3. After 30 days of microgravity, crew health drops from $100.0\%$ to **$98.5\%$**.
4. Mission success predicate remains satisfied ($H_{crew} \ge 70.0\%$), but exercise protocols must double to mitigate bone density loss.
