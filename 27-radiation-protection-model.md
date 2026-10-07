# 27 — Quantitative Radiation Protection Model & Hostile Engineering Shielding Audit

**Document ID:** `27-radiation-protection-model.md`
**Digital Twin Source:** `engineering/calculations/shielding_estimator.py` & `engineering/calculations/mission_digital_twin.py`
**Program Phase:** Post-Phase 8.6 Hostile Engineering Radiation & Geometry Closure Audit
**Program Status:** **CONDITIONALLY CLOSED UNDER OPTION F HYBRID DYNAMIC ARCHITECTURE**

---

## 1. Executive Finding & Concise Determination

> **EXECUTIVE DETERMINATION: RADIATION PROTECTION IS CONDITIONALLY CLOSED UNDER THE OPTION F HYBRID DYNAMIC ARCHITECTURE.**

A hostile engineering audit of Project Occam-7's radiation protection model revealed that treating the spacecraft's $2,500\text{ MT}$ propellant inventory as equivalent to a validated radiation shield was physically indefensible for two primary reasons:

1. **Directional Solid Angle Fallacy ($\Omega_{axial}$ vs $\Omega_{radial}$):** Propellant tanks arranged linearly along the $380\text{m}$ spine truss subtend an axial solid angle of $\Omega_{axial} \approx 0.090\text{ sr}$ ($\approx 0.72\%$ of the $4\pi$ sky). The remaining $99.28\%$ of space ($\Omega_{radial} \approx 12.48\text{ sr}$) is exposed to isotropic Galactic Cosmic Rays (GCR) and omnidirectional Solar Particle Events (SPE). Main propellant mass provides almost **zero protection** against $99\%$ of background space radiation.
2. **Propellant Depletion Void:** Propellant mass decreases dramatically throughout the mission (dropping to $0\text{ t}$ during Mars stay prior to ISRU reload and after final Earth capture). A spacecraft cannot claim radiation credit for propellant that has already been burned.

**Resolution:** The architecture is validated by establishing strict separation between directional reactor shadow shielding (handled via $45\text{ MT}$ Tungsten/$B_4C/LiH$ shadow shield $+ 380\text{m}$ distance $+ 1/R^2$ geometric attenuation) and circumferential/radial habitat shielding ($240\text{ MT}$ fixed passive dry mass allocation in `mass_budget.py`, comprising $184.6\text{ MT}$ circumferential water/polyethylene habitat buffer $+ 55.4\text{ MT}$ central SPE storm shelter core).

---

## 2. Inventory of Current Radiation & Shielding Assumptions

Every radiation assumption in the repository is explicitly classified below according to strict physical reality standards:

| Assumption Description | Scope & Application | Reality Classification | Forensic Status & Remediation |
| :--- | :--- | :---: | :--- |
| **Fast Reactor Shadow Shield ($45\text{ MT}$)** | Line-of-sight attenuation for aft reactor core ($100\text{ MWth}$) | **VERIFIED** | Physics-derived. $30\text{ t}$ Tungsten $+ 15\text{ t}$ $B_4C/LiH$ reduces core flux by factor $1.43 \times 10^{-4}$. |
| **Inverse-Square Geometric Attenuation ($380\text{m}$)** | Reactor-to-habitat separation distance | **VERIFIED** | First-principles geometric $1/R^2$ attenuation factor $= 6.925 \times 10^{-6}$. |
| **Central SPE Storm Shelter Core ($52.25\text{ g/cm}^2$)** | $4\text{m} \times 10\text{m}$ inner cylinder refuge for solar flare events | **VERIFIED** | Multi-layer SS/Water/HDPE/SS stack attenuates SPE proton flux by $>98.5\%$. Verified life support ($1.5\text{ kWe}$, $3.9\text{ kWth}$, $48\text{h}$ ECLSS). |
| **Circumferential Habitat Water Buffer ($20.0\text{ g/cm}^2$)** | Radial $360^\circ$ GCR protection ($184.6\text{ MT}$ fluid mass) | **VERIFIED** | Formally accounted for within $240\text{ MT}$ passive shielding dry mass budget. |
| **Spatial Habitat Geometry Statistics** | $8\text{m} \times 30\text{m}$ pressurized cylinder shielding distribution | **VERIFIED** | Calculated min ($15.0\text{ g/cm}^2$), max ($2222.5\text{ g/cm}^2$), mean ($89.7\text{ g/cm}^2$), median ($35.7\text{ g/cm}^2$), std dev ($220.1\text{ g/cm}^2$). |
| **Main Tank Axial Propellant Shielding ($>200\text{ g/cm}^2$)** | Dual-use shadow shield along axial spine | **MODELED / ASSUMED** | Valid for axial line-of-sight when tanks full, but depletes to $0\text{ g/cm}^2$ when empty. |
| **Constant Daily Radiation Dose Rate ($0.07\text{ cSv/d}$)** | Legacy digital twin static scalar dose rate assumption | **REJECTED / DEFICIENT** | Replaced by dynamic time-dependent physics calculation in `mission_digital_twin.py`. |
| **Active ZBO Cryogenic Refrigeration ($15\text{ kWe}$)** | Zero-boiloff active cooling for hydrogen mass retention | **FRONTIER** | Requires long-duration space-qualified reverse Brayton cryocoolers. |
| **Active Electromagnetic / Plasma Shielding** | Charged particle deflectors | **SCIENCE FICTION** | Retained strictly as speculative research annex; excluded from baseline. |

---

## 3. Physical Geometry & Spatial Topology Reconstruction

```
+---------------------------------------------------------------------------------------------------------+
| AFT REACTOR CORE   SHADOW SHIELD   380m SPINE TRUSS & RADIATORS   PROPELLANT TANKS   HABITAT DECK CORE  |
| 100 MWth Fast Core | 45 MT W/B4C | 2,502 m² Radiator Arrays     | 12m Dia Tanks     | 8m Dia x 30m Cylinder|
| z = -380m          | z = -375m   | z = -350m to -50m            | z = -50m to -10m  | z = 0m to +30m       |
+---------------------------------------------------------------------------------------------------------+
                     \__________________ Axial Angle: 9.73° (0.090 sr / 0.72% Sky) ___________________/
                     \__________________ Radial Sky: 350.27° (12.48 sr / 99.28% Sky) _________________/
```

### Spatial Topology Parameters:
* **Spine Axis Length:** $380.0\text{ m}$ total separation between aft reactor core and forward habitat deck.
* **Main Propellant Tank Geometry:** $12.0\text{ m}$ outer diameter, $280\text{ m}$ total effective tank stack length.
* **Habitat Hull Geometry:** $8.0\text{ m}$ outer diameter, $30.0\text{ m}$ pressurized cylinder length.
* **Solid Angle Subtended by Tanks ($\Omega_{axial}$):**
  $$\theta_{axial} = \arctan\left(\frac{6.0\text{ m}}{35.0\text{ m}}\right) = 9.73^\circ = 0.170\text{ rad}$$
  $$\Omega_{axial} = 2\pi (1 - \cos 9.73^\circ) \approx 0.090\text{ sr} \quad (0.72\%\text{ of } 4\pi\text{ sky})$$
* **Radial/Circumferential Sky ($\Omega_{radial}$):**
  $$\Omega_{radial} = 4\pi - \Omega_{axial} = 12.476\text{ sr} \quad (99.28\%\text{ of } 4\pi\text{ sky})$$

---

## 4. Time-Dependent Mission-Phase Shielding & Depletion Table

The table below evaluates shielding thickness, reactor power, and daily dose rates across all 9 canonical mission phases:

| Phase | Phase Name | $\text{LH}_2$ Mass ($\text{MT}$) | $\text{LNH}_3$ Mass ($\text{MT}$) | Axial Column ($\text{g/cm}^2$) | Radial Column ($\text{g/cm}^2$) | Reactor Output | Daily Dose Rate ($\text{cSv/day}$) | Vulnerability & Protection Mode |
| :---: | :--- | ---:| ---:| ---:| ---:| :---: | ---:| :--- |
| **1** | **Earth Departure** | $2,200.0$ | $300.0$ | $1,988.0$ | $31.4$ | $100\text{ MW}_{th}$ | $0.038$ | Maximum propellant buffer; full reactor shadow. |
| **2** | **Outbound Cruise NEP** | $810.8$ | $42.6$ | $742.1$ | $31.4$ | $15\text{ MW}_{e}$ | $0.041$ | LNH3 depleting; GCR dominated by radial $31.4\text{ g/cm}^2$. |
| **3** | **Mars Arrival / MOI** | $307.1$ | $42.6$ | $278.4$ | $31.4$ | $100\text{ MW}_{th}$ | $0.045$ | LH2 burned during MOI; axial shield decreasing. |
| **4** | **Mars Surface Stay** | $0.0$ | $42.6$ | $0.0$ | $47.4$ | $2\text{ MW}_{e}$ | $0.028$ | Surface $2\pi$ planet shadow $+ 16\text{ g/cm}^2$ $CO_2$ atmosphere. |
| **5** | **Mars ISRU Reload** | $2,200.0$ | $42.6$ | $1,988.0$ | $47.4$ | $2\text{ MW}_{e}$ | $0.027$ | Refueling complete; return propellant verified. |
| **6** | **Trans-Earth Injection** | $1,643.0$ | $42.6$ | $1,485.0$ | $31.4$ | $100\text{ MW}_{th}$ | $0.039$ | LH2 consumed for TEI burn; reactor throttled post-burn. |
| **7** | **Inbound Cruise NEP** | $1,638.1$ | $0.0$ | $1,480.0$ | $31.4$ | $15\text{ MW}_{e}$ | $0.039$ | LNH3 fully exhausted; NEP electric cruise complete. |
| **8** | **Earth Capture EOI** | $0.0$ | $0.0$ | $0.0$ | $31.4$ | $100\text{ MW}_{th}$ | $0.062$ | All propellant burned; reactor shielded by shadow shield $+ 1/R^2$. |
| **9** | **Post-Mission Depletion**| $0.0$ | $0.0$ | $0.0$ | $31.4$ | $0\text{ MW}_{th}$ | $0.038$ | Reactor shut down; ambient background GCR baseline. |

---

## 5. Separation of Radiation Threat Environments

1. **Galactic Cosmic Rays (GCR):** Relativistic $0.1\text{--}10\text{ GeV/nucleon}$ HZE nuclei. Isotropic ($4\pi$). Attenuation governed strictly by radial habitat shielding ($31.4\text{ g/cm}^2$ SS/Water/HDPE). Hydrogen-rich water/polyethylene suppresses secondary neutron spallation.
2. **Solar Particle Events (SPE):** Solar coronal mass ejection protons ($10\text{--}100\text{ MeV}$). Directionally variable/omnidirectional. Attenuated by $>98.5\%$ inside central $52.25\text{ g/cm}^2$ SPE Storm Shelter core during flare arrival ($12\text{--}48\text{ hrs}$).
3. **Secondary Neutron Spallation:** Produced when heavy GCR ions strike high-Z metals (316L SS pressure hull). Mitigated by inner low-Z hydrogenous liners (water jacket $+ 15\text{ cm}$ HDPE polymer).
4. **Reactor Primary & Scatter Radiation:** Fast neutrons $+ \gamma$-flux from $100\text{ MWth}$ fast fission reactor. Highly directional from aft end. Attenuated by $45\text{ MT}$ Tungsten/$B_4C/LiH$ shadow shield, $380\text{m}$ $1/R^2$ geometric separation, and axial propellant when present.

---

## 6. Program Status & Verification

Under the remediated Option F Hybrid Architecture:
* **Total Accumulated Mission Dose:** **$75.53\text{ cSv}$** ($0.755\text{ Sv}$), fully inclusive of background GCR, reactor operation, and two SPE flare events inside the storm shelter core.
* **NASA Career Radiation Safety Limit:** **$100.0\text{ cSv}$** ($1.0\text{ Sv}$).
* **Safety Margin:** **$+24.47\text{ cSv}$** ($24.47\%\text{ margin}$) below career ceiling.
* **Test Verification:** All 52 automated consistency and hostile adversarial unit tests pass (`python3 engineering/calculations/test_system_consistency.py`).
