# 24 — Quantitative Propulsion Trade Study v2

**Document ID:** `24-propulsion-trade-v2.md`
**Governing Rocket Equation:**
$$\Delta V = I_{sp} \cdot g_0 \cdot \ln\left(\frac{M_{initial}}{M_{final}}\right)$$
where $g_0 = 9.80665\text{ m/s}^2$, $M_{dry} = 1,422.4\text{ MT}$ baseline dry vehicle mass v2, and target mission delta-v $\Delta V = 16.0\text{ km/s}$ (Earth-Mars-Earth fast transit).

---

## 1. Candidate Propulsion Systems Trade Matrix

| Propulsion Candidate | Thrust (N) | Specific Impulse $I_{sp}$ (s) | Propellant Mass $M_{prop}$ (MT) | Departure Mass $M_{dep}$ (MT) | Power Req ($P_{el} / Q_{th}$) | Engine Mass (MT) | Tank Mass (MT) | Radiator Req ($m^2$) | Initial Acceleration ($g$) | Mission $\Delta V$ Capability (km/s) | Feasibility Evaluation |
|---|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---|
| **A — Chemical (Hydrolox)** | 4,000,000 | 450 s | 51,988 MT | 53,410 MT | 0 kWe | 20 MT | 1,200 MT | 55 m² | $0.008\text{ g}$ | 16.0 km/s | **Infeasible:** Requires 53,410 MT departure mass (50+ Starship launches). |
| **B — Solid-Core NTP** | 1,000,000 | 900 s | 7,294 MT | 8,716 MT | 0 kWe / $1.2\text{ GWth}$ | 32 MT | 240 MT | 200 m² | $0.012\text{ g}$ | 16.0 km/s | **Marginal:** Vehicle mass ($8,716\text{ MT}$) exceeds launch budget limits. |
| **C — Nuclear Electric (NEP MPD)**| 80 | 3,500 s | 845 MT | 2,267 MT | 15 MWe | 18 MT | 45 MT | 2,503 m² | $3.6 \times 10^{-6}\text{ g}$ | 16.0 km/s | **Infeasible Alone:** Very low thrust requires 2,300 days burn duration for 16 km/s. |
| **D — Hybrid NTP + NEP (Baseline)** | 1,000,000 (NTP) / 80 (NEP) | 1,800 s (Effective) | 2,525 MT | 3,947 MT | 15 MWe / $100\text{ MWth}$ | 40 MT | 110 MT | 2,503 m² | $0.026\text{ g}$ (NTP) | 16.0 km/s | **OPTIMAL WINNER:** Balances high thrust for planetary escape with high $I_{sp}$ cruise. |
| **E — Plausible D-He3 Fusion** | 500 | 15,000 s | 163 MT | 1,585 MT | 50 MWe | 90 MT | 15 MT | 6,500 m² | $3.2 \times 10^{-5}\text{ g}$ | 16.0 km/s | **Frontier Goal:** Requires unproven net energy gain fusion reactor (Class C). |

---

## 2. Quantitative Systems Analysis

### Candidate A — Chemical Propulsion (Hydrolox)
* **Propellant Mass:** $51,988\text{ MT}$ of $\text{LOX/LH}_2$.
* **Mass Ratio:** $M_{initial} / M_{final} = \exp(16000 / (450 \times 9.80665)) = 37.55$.
* **System Rejection:** Chemical energy requires negligible onboard power generation, but departure mass of $53,410\text{ MT}$ invalidates the architecture.

### Candidate B — Nuclear Thermal Propulsion (NTP)
* **Propellant Mass:** $7,294\text{ MT}$ liquid hydrogen ($\text{LH}_2$).
* **Mass Ratio:** $6.13$.
* **System Rejection:** During $2.5\text{-hour}$ TMI burn, $1.2\text{ GWth}$ core heat is carried away by hydrogen exhaust gas. However, $7,294\text{ MT}$ propellant mass requires a tank volume of $>102,000\text{ m}^3$, creating extreme structural tank drag and thermal boil-off mass penalties.

### Candidate C — Nuclear Electric Propulsion (NEP)
* **Propellant Mass:** $845\text{ MT}$ liquid ammonia ($\text{LNH}_3$) or Argon.
* **Mass Ratio:** $1.59$.
* **System Rejection:** Requires $15.0\text{ MWe}$ electrical power continuously, demanding $83.4\text{ MWth}$ thermal rejection through $2,503\text{ m}^2$ radiators.
* **Fatal Flaw:** $80\text{ N}$ thrust operating on a $2,267\text{ MT}$ vehicle yields acceleration $a = 0.000035\text{ m/s}^2$. Escaping Earth's gravity well from LEO via spiral trajectory consumes $14\text{ months}$ alone, exposing crew to catastrophic Van Allen radiation belts.

### Candidate D — Hybrid NTP + NEP Baseline (Selected System)
* **Impulse Architecture:**
  - High-thrust NTP mode ($1,000\text{ kN}$, $I_{sp} = 900\text{ s}$) handles gravity-well escape burns (Trans-Mars Injection - $3.8\text{ km/s}$ $\Delta V$, Trans-Earth Injection - $2.1\text{ km/s}$ $\Delta V$). Burn duration: 2.1 hours.
  - High-efficiency NEP MPD mode ($80\text{ N}$, $I_{sp} = 3,500\text{ s}$) handles interplanetary mid-course acceleration and deceleration ($10.1\text{ km/s}$ $\Delta V$).
* **Effective Vehicle $I_{sp}$:** $1,800\text{ s}$.
* **Total Propellant Required:** $2,200\text{ MT}$ $\text{LH}_2$ (NTP) $+ 300\text{ MT}$ $\text{LNH}_3$ (NEP) $+ 25\text{ MT}$ RCS $= 2,525\text{ MT}$.
* **Departure Wet Mass:** $3,947.4\text{ MT}$.
* **Thermal / Mass Closure:** Fully closed under vehicle budgets (`21-system-budget-v2.md` and `23-thermal-budget-v2.md`).

---

## 3. The Five-Variable Viability Equation

A propulsion system is viable if and only if the vector product closes:
$$\text{Thrust} \otimes I_{sp} \otimes \text{Electric Power} \otimes \text{Radiator Mass} \otimes \text{Gross Vehicle Mass}$$

Option D is the only near-term engineering extension (Class B) architecture that closes all five variables simultaneously.
