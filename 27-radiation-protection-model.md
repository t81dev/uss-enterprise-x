# 27 — Quantitative Radiation Protection Model

**Document ID:** `27-radiation-protection-model.md`
**Shielding Column Density Definition:**
$$\text{Column Density } (\sigma) = \rho \cdot t \quad [\text{g/cm}^2]$$
where $\rho$ is material density ($\text{g/cm}^3$) and $t$ is thickness ($\text{cm}$).

---

## 1. Radiation Threat Environments: SPE vs GCR

| Parameter | Solar Particle Events (SPE) | Galactic Cosmic Rays (GCR) |
|---|---|---|
| **Particle Physics Source** | Solar Coronal Mass Ejections (CMEs) | Extra-solar relativistic heavy ions (HZE particles) |
| **Energy Spectrum** | Low to moderate energy ($10\text{--}100\text{ MeV}$ protons) | Relativistic ultra-high energy ($0.1\text{--}10\text{ GeV/nucleon}$) |
| **Temporal Profile** | Acute transient events ($12\text{--}48\text{ hours}$) | Continuous isotropic background flux ($1,000\text{ days}$) |
| **Shielding Strategy** | Thick hydrogenous mass ($>40\text{ g/cm}^2$) localized in storm shelter | Large-scale passive mass, material atomic mass optimization, or fast transit |
| **Secondary Production** | Minimal secondary neutrons / Bremsstrahlung | High risk of secondary neutron spallation in heavy metals (e.g. Lead/Tungsten) |
| **Unshielded Dose Rate** | $1,000\text{--}5,000\text{ mSv/event}$ (Lethal without shelter) | $500\text{--}800\text{ mSv/year}$ ($1,500\text{ mSv}$ per 1,000-day mission) |
| **Target Shielded Dose** | $< 50\text{ mSv/event}$ (Negligible clinical impact) | $< 150\text{ mSv/year}$ ($420\text{ mSv}$ 1,000-day mission limit) |

---

## 2. Material Performance & Column Density Analysis

| Material | Density $\rho$ (g/cm³) | Hydrogen Mass Fraction ($f_H$) | Secondary Neutron Spallation Risk | Primary Application Zone | Required Thickness for $25\text{ g/cm}^2$ (cm) | Mass Efficiency Score |
|---|---:|---:|---|---|---:|---|
| **Water ($\text{H}_2\text{O}$)** | 1.00 | $11.2\%$ | Very Low | Storm shelter jacket & circumferential tanks | 25.0 cm | **Optimal Dual-Use** |
| **Polyethylene (HDPE)** | 0.95 | $14.4\%$ | Extremely Low | Internal liner & storm shelter inner wall | 26.3 cm | **Optimal Polymer** |
| **Liquid Hydrogen ($\text{LH}_2$)** | 0.071 | $100.0\%$ | Zero | Interplanetary main tank axial buffer | 352.1 cm | **Maximum Hydrogen Efficiency** |
| **Liquid Ammonia ($\text{LNH}_3$)** | 0.681 | $17.8\%$ | Very Low | Secondary tank buffer | 36.7 cm | High |
| **Boron Carbide ($B_4C$)** | 2.52 | $0.0\%$ | High neutron absorption ($\sigma_B$) | Reactor shadow shield thermal neutron absorber | 9.9 cm | Specialized Reactor Shielding |
| **Tungsten (W)** | 19.25 | $0.0\%$ | High secondary Bremsstrahlung | Reactor shadow shield gamma absorber | 1.3 cm | Dense Gamma Absorber |
| **316L Stainless Steel** | 8.00 | $0.0\%$ | Moderate secondary spallation | Primary pressure hull & spine truss | 3.1 cm | Low (Structural Only) |

---

## 3. Vehicle Zonal Shielding Allocation

```
+--------------------------------------------------------------------------------------------------+
| AFT REACTOR ZONE         MAIN PROPELLANT TANKS          CENTRAL HABITAT           FORWARD STORM  |
| Reactor + Shadow Shield | 2,200 MT LH2 / 300 MT LNH3  | Water Tanks (20 g/cm²)  | SHELTER CORE  |
| (Tungsten/B4C/LiH)      | (Axial Column: >200 g/cm²) | Habitats: 30 g/cm² total | (52.75 g/cm²) |
+--------------------------------------------------------------------------------------------------+
```

1. **Reactor Exclusion & Shadow Shield Zone:**
   - Fast reactor produces $100\text{ MWth}$ neutron and gamma flux.
   - Conical shadow shield ($30\text{ MT}$ Tungsten $+ 15\text{ MT}$ $B_4C/LiH$) mounted at aft reactor reduces core radiation dose at the habitat ($380\text{m}$ separation) to $<0.05\text{ mSv/hr}$ via $1/r^2$ geometric attenuation and physical absorption.
2. **Main Propellant Tank Axial Buffer:**
   - $2,200\text{ MT}$ of $\text{LH}_2$ and $300\text{ MT}$ of $\text{LNH}_3$ positioned along the $310\text{m}$ spine provide an axial column density of $>200\text{ g/cm}^2$, fully absorbing residual reactor neutrons and scatter gammas.
3. **Nominal Habitat Circumferential Zone:**
   - Outer circumferential water tanks ($20\text{ cm}$ thickness $= 20.0\text{ g/cm}^2$) + $8\text{mm}$ stainless steel pressure hull ($6.4\text{ g/cm}^2$) + internal equipment racks ($5.0\text{ g/cm}^2$) provide ambient habitat shielding of $31.4\text{ g/cm}^2$.
   - Attenuates background GCR dose from $600\text{ mSv/yr}$ down to $\sim 140\text{ mSv/yr}$.
4. **Central SPE Storm Shelter Core:**
   - Cylindrical refuge ($4.0\text{m}$ diameter $\times 10.0\text{m}$ length) buried in the innermost center of Habitat Deck 3.
   - Surrounded by a $40\text{ cm}$ double-wall water jacket ($40.0\text{ g/cm}^2$) $+ 5\text{ cm}$ HDPE liner ($4.75\text{ g/cm}^2$) $+ 1.0\text{ cm}$ stainless steel structural wall ($8.0\text{ g/cm}^2$).
   - **Total Passive Column Density:** $52.75\text{ g/cm}^2$.
   - Attenuates peak Solar Particle Event (SPE) proton flux by $>99.2\%$, reducing total event dose inside shelter to $<15\text{ mSv/event}$.

---

## 4. Degraded-Shielding & Propellant Depletion Analysis

* **Late-Mission Propellant Depletion Case:** As $\text{LH}_2$ propellant is consumed during Trans-Earth Injection (TEI), axial propellant column density drops from $200\text{ g/cm}^2$ to $15\text{ g/cm}^2$.
* **Mitigation Protocol:** The $380\text{m}$ physical separation distance alone provides $1/r^2$ flux attenuation factor of $1.4 \times 10^5$. Reactor decay power during return cruise drops to $20\text{ MWe}$, maintaining reactor dose at habitat deck below $0.10\text{ mSv/hr}$.
