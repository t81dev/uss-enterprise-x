# 28 — Quantitative Structural Load Path Analysis (Reconciled v2)

**Document ID:** `28-structural-load-path.md`
**Primary Structural Axis:** Longitudinal X-axis ($380\text{ m}$ spine length)
**Maximum Compressive Design Load:** $4,000\text{ kN}$ (4x NTP full thrust burn state)
**Primary Load Bearing Structure:** Octagonal 316L Stainless Steel / Carbon-Composite Open Space Frame Truss

---

## 1. Longitudinal Load Path Architecture

```
[AFT NTP ENGINES] ---> (Thrust Cone) ---> [REACTOR MODULE TRUSS] ---> [MAIN TANK SPINE] ---> [FORWARD HABITAT]
  4,000 kN Thrust        Compression            210 MT Mass             178.75 MT Tank Shell    135 MT Pressure Shell
```

The load-bearing structure is an octagonal spatial truss ($6.0\text{ m}$ outer diameter, $12.0\text{ m}$ at tank ring attachment nodes) running continuously from the aft engine thrust cone to the forward docking node.

### A — Main Thrust Axis Loads
* **NTP Engine Thrust:** $1,000\text{ kN}$ per engine $\times 4 = 4,000\text{ kN}$ total thrust vector directed along the $+\text{X}$ axis.
* **Axial Stress Distribution:** Under maximum wet departure mass ($3,970.96\text{ MT}$), initial axial acceleration is $a = 0.001007\text{ m/s}^2$ ($0.103\text{ g}$). Maximum compressive force along the aft spine section reaches $3,580\text{ kN}$.
* **Safety Factor:** Structural cross-sectional area ($0.18\text{ m}^2$ effective SS 316L member area) yields axial compressive stress $\sigma_c = 22.1\text{ MPa}$, compared to $316\text{L}$ yield strength $\sigma_y = 220\text{ MPa}$ ($\text{Safety Factor} = 9.95$).

### B — Propellant Tank Hydrostatic & Hoop Stress Analysis (Reconciled)
* **Geometry:** Main propellant tanks ($12.0\text{ m}$ outer diameter, $R = 6.0\text{ m}$) store $2,200\text{ MT}$ $\text{LH}_2$ $+ 300\text{ MT}$ $\text{LNH}_3$.
* **Internal Ullage Pressure:** $P_{ullage} = 150\text{ kPa}$ ($150,000\text{ N/m}^2$).
* **Thin-Wall Hoop Stress Correction (DEF-001):** The thin-wall cylindrical hoop relation is:
  $$\sigma_\theta = \frac{P \cdot r}{t}$$
  For $r = 6.0\text{ m}$ and the previous baseline wall thickness $t = 4.0\text{ mm}$ ($0.004\text{ m}$):
  $$\sigma_\theta = \frac{150,000 \times 6.0}{0.004} = \mathbf{225.0\text{ MPa}}$$
  Since $316\text{L}$ Stainless Steel yield strength is $\sigma_y = 220\text{ MPa}$, the $4\text{ mm}$ skin operates beyond yield ($\sigma_\theta / \sigma_y = 1.023$), violating structural yield limits.
* **Revised Wall Sizing Criteria:** Applying an aerospace yield safety factor $SF_{yield} = 1.50$ yields allowable operating stress:
  $$\sigma_{allow} = \frac{\sigma_y}{1.50} = \frac{220\text{ MPa}}{1.50} = 146.67\text{ MPa}$$
  $$t_{min} = \frac{P \cdot r}{\sigma_{allow}} = \frac{150,000 \times 6.0}{146.67 \times 10^6} = 0.006136\text{ m} = 6.14\text{ mm}$$
  Selected baseline wall thickness is set to $t_{tank} = \mathbf{6.5\text{ mm}}$ ($0.0065\text{ m}$).
* **Reconciled Stress & Margins:**
  * Operating Hoop Stress: $\sigma_\theta = \frac{150,000 \times 6.0}{0.0065} = \mathbf{138.46\text{ MPa}}$ ($\text{Margin vs Yield} = +58.9\%$, $SF_{operating} = 1.59$).
  * Longitudinal Stress: $\sigma_z = \frac{P \cdot r}{2t} = \mathbf{69.23\text{ MPa}}$.
  * Proof Pressure ($1.25\times P_{op} = 187.5\text{ kPa}$): $\sigma_{proof} = 173.08\text{ MPa}$ ($SF_{proof} = 1.27$).
  * Burst Pressure ($2.0\times P_{op} = 300\text{ kPa}$): $\sigma_{burst} = 276.92\text{ MPa}$ (handled by ultimate tensile strength $\sigma_u = 485\text{ MPa}$).
* **Propellant Tank Dry Mass Impact:** Increasing tank skin thickness from $4.0\text{ mm}$ to $6.5\text{ mm}$ across the $310\text{ m}$ combined tank assembly increases unmargined tank dry mass from $110.0\text{ MT}$ to $\mathbf{178.75\text{ MT}}$ ($+68.75\text{ MT}$).

### C — Bending Moments & Transverse Loads
* **Source:** Asymmetric RCS pulse firing, centrifuge rotation imbalance, and radiator boom gravity gradient torques.
* **Peak Bending Moment:** $M_x = 4.2 \times 10^6\text{ N}\cdot\text{m}$ at the central spine midpoint ($X = 190\text{ m}$) during a maximum rate RCS rotation maneuver ($\alpha = 0.05\text{ rad/s}^2$).
* **Structural Resistance:** Octagonal spatial truss ($6\text{ m}$ depth) provides section modulus $Z = 0.28\text{ m}^3$, limiting maximum bending stress to $\sigma_b = 15.0\text{ MPa}$.

### D — Thermal Expansion & Dynamic Isolation
* **Temperature Gradient:** Aft reactor section operates at $850\text{ K}$, central propellant tanks at $20\text{ K}$ ($\text{LH}_2$), and forward habitat at $295\text{ K}$.
* **Thermal Expansion Delta:** $\Delta T = 830\text{ K}$ across reactor/tank interface ($X = 60\text{ m}$ to $X = 100\text{ m}$). Unconstrained thermal expansion would induce $\Delta L = 0.85\text{ m}$ structural elongation.
* **Expansion Joint Mechanism:** Titanium-bellows sliding flex-joints and active hydraulic tensioning struts isolate thermal strain from primary thrust members, preventing thermal buckling.

---

## 2. Load Paths for Auxiliary Subsystems

1. **Radiator Cantilever Loads:**
   - Deployable $150\text{ m}$ radiator wings ($26.66\text{ MT}$) cantilever laterally ($+\text{Y} / -\text{Y}$ axes). Root bending moment during $0.10\text{ g}$ acceleration $= 19.6\text{ kN}\cdot\text{m}$, carried by dual triangular guy-wires anchored to spine nodes.
2. **Centrifuge Dynamic Bearing Loads:**
   - $30\text{ m}$ transverse artificial gravity ring ($38.0\text{ MT}$) rotates at $6.0\text{ RPM}$.
   - Radial centripetal load $= 850\text{ kN}$, transferred to primary spine truss through 4 quadrant magnetic-levitation ring bearings with active vibration dampers.
3. **Docking & Lander Impact Loads:**
   - Orbital docking of $50\text{ MT}$ lander craft at $v_{rel} = 0.15\text{ m/s}$ creates $120\text{ kN}$ transient shock load absorbed by hydraulic attenuation dampers in the forward APAS docking ring.

---

## 3. Partial Structural Failure Behavior (Graceful Degradation)

> **What actually carries the ship?**
> The continuous octagonal space-frame truss spine carries $100\%$ of thrust, bending, and payload loads.

> **What happens when that structure partially fails?**
* **Scenario: Buckling / Fracture of 2 Primary Spine Truss Members (MMOD Impact at X = 150m)**
  - **Redundancy Factor:** Octagonal truss is 4-fold hyperstatic (statically indeterminate). Loss of 2 diagonal members redistributes compressive stress to 6 adjacent parallel members.
  - **Stress Redistribution:** Local stress on adjacent members increases by $+33\%$ ($\sigma_c$ rises from $22.1\text{ MPa}$ to $29.4\text{ MPa}$), remaining well below yield strength ($220\text{ MPa}$).
  - **Automated Control Action:** Flight OS limits main engine throttle to $75\%$ ($3,000\text{ kN}$ thrust) until robotic welding drones splice reinforcement sleeves over damaged members.
