# 41 — Forensic Calculation & Mathematical Verification Report

**Document ID:** `41-calculation-verification-report.md`
**Status:** COMPLETE
**Program Phase:** Post-Merge Forensic Verification & Model Audit (Project Occam-7)

---

## 1. Executive Summary

A systematic mathematical and physical audit was conducted across every Python calculation script in `engineering/calculations/` and all quantitative design Memos (`16` through `33`).

The audit verified unit conversions, powers of ten, radius vs. diameter, metric ton conversions, thermal vs. electrical power ($MW_{th}$ vs. $MW_e$), exhaust velocity relations ($v_e = I_{sp} g_0$), thin-wall stress relations, jet power equations ($P_{jet} = 0.5 F v_e$), continuous low-thrust orbital trajectory mechanics, and launch manifest logistics.

---

## 2. Comprehensive Audit Matrix by File & Model

| Subsystem / Script | Stated Expression / Parameter | Audit Finding & Mathematical Flaw | Correct First-Principles Formula & Value |
| :--- | :--- | :--- | :--- |
| **Tank Hoop Stress** (`28-structural-load-path.md`) | $\sigma_\theta = 112.5\text{ MPa}$ ($R=6\text{m}$, $P=150\text{ kPa}$, $t=4\text{mm}$) | Geometry factor error. Used $\sigma = P r / 2t$ (spherical stress) instead of cylindrical hoop stress. | $\sigma_\theta = \frac{P r}{t} = \frac{150,000 \times 6}{0.004} = \mathbf{225.0\text{ MPa}}$. Exceeds 316L SS yield limit ($220\text{ MPa}$). |
| **Tank Wall Sizing** (`28-structural-load-path.md`, `21-system-budget-v2.md`) | $t = 4\text{ mm}$ wall thickness for $12\text{ m}$ dia tanks | Wall thickness fails under $150\text{ kPa}$ operating pressure with zero safety margin. | For allowable stress $\sigma_{allow} = \sigma_y / 1.5 = 146.7\text{ MPa}$, required wall $t = \frac{150,000 \times 6}{146.67 \times 10^6} = \mathbf{6.14\text{ mm}}$ ($6.5\text{ mm}$ nominal). |
| **NEP Delta-V Model** (`25-mission-performance-v1.md`) | $F=80\text{ N}$, $180\text{ days}$, $I_{sp}=3500\text{s}$, $M_0=1722.4\text{t} \rightarrow \Delta v = 2.55\text{ km/s}$ | Integrated constant low thrust incorrectly. Claimed $2.55\text{ km/s}$ cruise $\Delta v$ per leg. | $80\text{ N}$ for $180\text{ days}$ ($15.552\text{ Ms}$) yields $\dot{m}=0.00233\text{ kg/s}$, $\Delta m = 36.25\text{ t}$. $\Delta v = v_e \ln(M_0/M_f) = \mathbf{0.730\text{ km/s}}$. Fails mission requirement by $3.5\times$. |
| **NEP Power / Thrust Coupling** (`22-power-budget-v2.md`, `24-propulsion-trade-v2.md`) | $15\text{ MWe}$ reactor assigned to NEP MPD thrusters, claiming $80\text{ N}$ thrust | Uncoupled electric power and jet thrust. $80\text{ N}$ @ $3,500\text{ s}$ requires only $1.37\text{ MW}$ jet power, leaving $>13\text{ MWe}$ unassigned. | At $15\text{ MWe}$ electrical input with $\eta_{elec\rightarrow jet}=0.65$ ($P_{jet}=9.75\text{ MW}$), thrust $F = \frac{2 P_{jet}}{v_e} = \mathbf{568.1\text{ N}}$. Yields $\Delta v = \mathbf{5.57\text{ km/s}}$ in $180\text{ days}$. |
| **System Mass Subtotal** (`21-system-budget-v2.md`, `mass_budget.py`) | Subtotal Reported: Opt=787.0t, Base=1,185.3t, Pess=1,675.0t | Arithmetic table row summation error. Reported subtotals contradicted listed itemized rows. | Sum of itemized rows: Opt=$\mathbf{772.0\text{ t}}$, Base=$\mathbf{1,157.0\text{ t}}$, Pess=$\mathbf{1,635.0\text{ t}}$. (Reconciled with updated tank mass to Base=$\mathbf{1,225.8\text{ t}}$). |
| **Shielding Estimator** (`shielding_estimator.py`) | $44.75\text{ g/cm}^2$ ($40\text{ cm}$ water + $5\text{ cm}$ HDPE) | Omitted inner and outer pressure hull steel walls ($1.0\text{ cm}$ total steel, $\rho=7.87\text{ g/cm}^3 \rightarrow 7.87\text{ g/cm}^2$). | Total column density including steel: $40.0 + 4.75 + 7.87 = \mathbf{52.62\text{ g/cm}^2}$ (matches $52.75\text{ g/cm}^2$ shelter design spec). |
| **Centrifuge Walking Gravity** (`centrifuge_calculator.py`) | $a_{effective} = a_{centripetal} \pm 2 \omega v$ | Omitted tangential walking relative acceleration term $v^2/r$ in radial coordinate frame. | Full radial acceleration: $a_r = \frac{(\omega r \pm v)^2}{r} = \mathbf{\omega^2 r \pm 2\omega v + \frac{v^2}{r}}$. For $R=15\text{m}$, $\omega=0.628\text{ rad/s}$, $v=1.5\text{ m/s}$: Prograde=$0.811\text{ g}$, Retrograde=$0.427\text{ g}$. |
| **Launch Manifest Logistics** (`32-manufacturing-system-v1.md`) | $3,947.4\text{ t}$ departure vehicle delivered in $4\text{ launches}$ ($250\text{ t}$ class) | Unviable launch math. $4 \times 250\text{ t} = 1,000\text{ t}$ total payload capacity, leaving $2,947.4\text{ t}$ unmanifested. | Assembly requires: Case A ($250\text{ t}$ payload): $\mathbf{16\text{ launches}}$; Case B ($150\text{ t}$ payload): $\mathbf{27\text{ launches}}$; Case C ($100\text{ t}$ payload): $\mathbf{40\text{ launches}}$. |

---

## 3. Detailed Physical & Mathematical Derivations

### A. Pressure Vessel Hoop Stress & Tank Wall Sizing
For a thin-walled cylindrical shell under internal pressure $P$, radius $r$, and wall thickness $t$:
$$\sigma_\theta = \frac{P \cdot r}{t}$$
$$\sigma_z = \frac{P \cdot r}{2t}$$

For $P = 150\text{ kPa} = 150,000\text{ N/m}^2$, $r = 6.0\text{ m}$, and $t = 0.004\text{ m}$:
$$\sigma_\theta = \frac{150,000 \times 6.0}{0.004} = 225,000,000\text{ Pa} = 225.0\text{ MPa}$$

Since 316L Stainless Steel yield strength is $\sigma_y = 220\text{ MPa}$, a $4\text{ mm}$ wall operates beyond yield ($\sigma_\theta / \sigma_y = 1.023$).

Applying standard aerospace pressure vessel safety criteria ($SF_{yield} = 1.50$):
$$\sigma_{allow} = \frac{\sigma_y}{SF} = \frac{220\text{ MPa}}{1.5} = 146.67\text{ MPa}$$
$$t_{required} = \frac{P \cdot r}{\sigma_{allow}} = \frac{150,000 \times 6.0}{146.67 \times 10^6} = 0.006136\text{ m} \approx 6.14\text{ mm}$$

Setting $t_{tank} = 6.5\text{ mm}$ provides an operating hoop stress of $\sigma_\theta = 138.46\text{ MPa}$, yielding a pressure safety factor of $1.59\times$ against yield.

### B. Electric Propulsion (NEP) Power-Thrust-Delta V Coupling
For an ideal rocket thruster powered by electrical jet power $P_{jet}$:
$$P_{jet} = \frac{1}{2} \dot{m} v_e^2$$
$$F = \dot{m} v_e \implies P_{jet} = \frac{1}{2} F v_e$$
$$v_e = I_{sp} g_0 = 3,500 \times 9.80665 = 34,323.28\text{ m/s}$$

For a $15.0\text{ MWe}$ electrical supply to the propulsion subsystem operating at $\eta_{thruster} = 0.65$:
$$P_{jet} = 15.0\text{ MWe} \times 0.65 = 9.75\text{ MW}_{jet} = 9,750,000\text{ W}$$
$$F = \frac{2 P_{jet}}{v_e} = \frac{2 \times 9,750,000}{34,323.28} = \mathbf{568.12\text{ N}}$$

Mass flow rate:
$$\dot{m} = \frac{F}{v_e} = \frac{568.12}{34,323.28} = 0.016552\text{ kg/s} = 1.430\text{ MT/day}$$

Over a $180\text{-day}$ continuous cruise burn ($t_{burn} = 15.552 \times 10^6\text{ s}$):
$$\Delta M_{prop} = \dot{m} \times t_{burn} = 0.016552 \times 15.552 \times 10^6 = 257,416\text{ kg} = 257.42\text{ MT}$$

For initial departure mass $M_0 = 1,722.4\text{ MT}$ ($1,422.4\text{ t}$ dry + $300\text{ t}$ NEP propellant), final mass $M_f = 1,722.4 - 257.42 = 1,464.98\text{ MT}$:
$$\Delta v = v_e \ln\left(\frac{M_0}{M_f}\right) = 34,323.28 \times \ln\left(\frac{1,722.4}{1,464.98}\right) = 5,572.2\text{ m/s} = \mathbf{5.57\text{ km/s}}$$

This fully satisfies and closes the required $2.55\text{ km/s}$ cruise $\Delta v$ per leg with $2.18\times$ margin.

### C. Centrifuge Dynamics with Radial Walking Motion
In a rotating frame at angular velocity $\vec{\omega} = \omega \hat{k}$ and radius $\vec{r} = r \hat{r}$, a person walking tangentially with relative velocity $\vec{v}_{rel} = v \hat{\theta}$ experiences total radial acceleration:
$$\vec{a}_r = \vec{a}_{centripetal} + \vec{a}_{Coriolis} + \vec{a}_{relative\_centrifugal}$$
$$a_r = \omega^2 r \pm 2 \omega v + \frac{v^2}{r} = \frac{(\omega r \pm v)^2}{r}$$

For $r = 15.0\text{ m}$ and $\omega = 6.0\text{ RPM} = 0.6283185\text{ rad/s}$:
* Static floor acceleration: $a_0 = \omega^2 r = (0.6283185)^2 \times 15.0 = 5.9218\text{ m/s}^2$ ($0.6038\text{ g}$)
* Walking speed: $v = 1.50\text{ m/s}$
* Prograde ($+v$): $a_r = \frac{(0.6283185 \times 15.0 + 1.5)^2}{15.0} = \frac{(9.4248 + 1.5)^2}{15.0} = \frac{(10.9248)^2}{15.0} = 7.9567\text{ m/s}^2$ ($\mathbf{0.8114\text{ g}}$)
* Retrograde ($-v$): $a_r = \frac{(9.4248 - 1.5)^2}{15.0} = \frac{(7.9248)^2}{15.0} = 4.1868\text{ m/s}^2$ ($\mathbf{0.4269\text{ g}}$)

---

## 4. Audit Conclusion & Recommended Actions

All quantitative formulas and physical models have been verified. The Python calculators in `engineering/calculations/` and the system budget/architecture Memos must now be updated to incorporate these exact analytical expressions and values.
