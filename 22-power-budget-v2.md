# 22 — Integrated Power Budget v2

**Document ID:** `22-power-budget-v2.md`
**Primary Generation Source:** $100\text{ MWth} / 20\text{ MWe}$ High-Temperature Fast Fission Reactor
**Conversion Cycle:** Closed-Loop Supercritical $CO_2$ ($sCO_2$) / Helium-Xenon Brayton Cycle ($\eta = 20.0\%$)
**Energy Storage Buffer:** $1,200\text{ kWh}$ Lithium-Sulfur / Solid-State Battery Bank + Regenerative Fuel Cells

---

## 1. Power Classification Architecture

Power flows are strictly categorized into three coupled domains:
1. **Thermal Power ($Q_{th}$):** Raw nuclear heat output from the reactor core ($100\text{ MWth}$) or NTP thermal core.
2. **Electrical Power ($P_{el}$):** Net output from Brayton turbogenerators ($20.0\text{ MWe}$) distributed across ship buses.
3. **Propulsive Power ($P_{prop}$):** Power directed into kinetic acceleration (NTP hydrogen heating or NEP MPD plasma acceleration).

---

## 2. Detailed Subsystem Electrical Power Budget

| Subsystem Load | Nominal Power (kWe) | Peak Power (kWe) | Duty Cycle (%) | Redundancy Level | Thermal Waste ($Q_{th}$ kWe) | Primary Power Function | Class |
|---|---:|---:|---:|---|---:|---|---|
| **ECLSS Air Scrubbing & $O_2$ Generation** | 70.0 | 100.0 | $100\%$ | $N+2$ Dual-Loop | 56.0 | Sabatier reactor, electrolysis, $CO_2$ scrubbers | A |
| **ECLSS Water Distillation & Sludge Processor**| 50.0 | 80.0 | $80\%$ | $N+1$ Redundant | 40.0 | Vapor compression distillation, catalytic oxidizer | A |
| **Thermal Control Coolant Pumps** | 80.0 | 140.0 | $100\%$ | $N+2$ Multi-pump | 64.0 | NaK / Water circulation pumps, radiator actuators | A |
| **Avionics & Rad-Hard High-Performance Compute**| 40.0 | 75.0 | $100\%$ | TMR ($N+2$) | 36.0 | Optical bus, AI flight control, navigation sensor fusion | A |
| **Deep-Space Laser & RF Communications** | 15.0 | 50.0 | $50\%$ | $N+1$ Dual-Gimbal | 12.0 | 100W optical laser transceivers, dish gimbals | A |
| **Habitat Environmental, Lighting & HVAC** | 60.0 | 90.0 | $100\%$ | $N+1$ Ring Bus | 54.0 | LED illumination, deck climate control, air circulation | A |
| **Centrifuge Magnetic Drive & Bearings** | 25.0 | 45.0 | $100\%$ | Dual Motor | 15.0 | Continuous ring rotation & dynamic counter-torque | B |
| **Scientific Payload & Instrumentation** | 50.0 | 200.0 | $40\%$ | Isolated Bus | 42.0 | Mass spectrometers, LiDAR, sub-surface radar | A |
| **Automated Machine Shop & Manufacturing** | 20.0 | 100.0 | $20\%$ | Standard | 18.0 | Metal 3D printing, CNC milling, robotic arm assembly | A |
| **Active Debris Radar & Laser Ablation** | 5.0 | 500.0 | Intermittent | Dual Array | 4.0 | Optical radar tracking & pulse ablation laser | B |
| **Battery Storage Buffer Charging** | 35.0 | 100.0 | $60\%$ | 4x Quadrant | 5.0 | $1,200\text{ kWh}$ solid-state buffer trickle charge | A |
| **Medical Operations & Diagnostic Bay** | 10.0 | 35.0 | Intermittent | Emergency Bus | 8.0 | Imaging, surgical bay, intensive care monitors | A |
| **NEP MPD Thruster Array (Cruise Mode)** | 15,000.0 | 15,000.0 | $80\%$ | 4x Modular | 3,000.0 | MW Magnetoplasmadynamic electric propulsion | B |
| **SUBTOTAL HOUSEHOLD LOADS (Non-Propulsive)** | **450.0** | **1,515.0** | **—** | **High** | **354.0** | **Base ship operations requirement** | **A/B** |
| **TOTAL WITH NEP ELECTRIC PROPULSION** | **15,450.0** | **16,515.0** | **—** | **Integrated** | **3,354.0** | **Maximum electrical demand state** | **B** |

---

## 3. Power Operating Cases & Load Management

```
                               +-----------------------------------+
                               |   Main Fast Reactor Core 100 MWth |
                               +-----------------------------------+
                                                 |
                                     [Brayton Conversion 20%]
                                                 |
                                                 v
                               +-----------------------------------+
                               |  Main Electrical Bus 20,000 kWe   |
                               +-----------------------------------+
                                    /            |            \
                                   /             |             \
            +-----------------------+   +------------------+   +----------------------+
            | NEP Propulsion 15 MWe |   | House Load 0.45M |   | Storage Buffer 4.55M |
            +-----------------------+   +------------------+   +----------------------+
```

### Case A: Nominal Interplanetary Cruise Case (NEP Active)
* **Thermal Core Generation:** $100.0\text{ MWth}$
* **Electrical Output:** $20,000\text{ kWe}$ ($20.0\text{ MWe}$)
* **NEP Propulsion Demand:** $15,000\text{ kWe}$ ($15.0\text{ MWe}$)
* **Household Electrical Demand:** $450\text{ kWe}$ ($0.45\text{ MWe}$)
* **Battery Charging / Spinning Reserve:** $4,550\text{ kWe}$ ($4.55\text{ MWe}$)
* **Operating State:** Fully stable. Power generation exceeds demand by $4.55\text{ MWe}$ ($22.7\%$ reserve margin).

### Case B: High-Load Science & Manufacturing Case (Proximity Ops / Station-Keeping)
* **Thermal Core Generation:** $25.0\text{ MWth}$ (Low-power core state)
* **Electrical Output:** $5,000\text{ kWe}$ ($5.0\text{ MWe}$)
* **NEP Propulsion Demand:** $0\text{ kWe}$ (NTP engines offline, MPD offline)
* **Peak Household Load:** $1,515\text{ kWe}$ ($1.515\text{ MWe}$)
* **Active Debris Laser Pulse Load:** $500\text{ kWe}$ ($0.50\text{ MWe}$)
* **Battery Charging:** $100\text{ kWe}$
* **Operating State:** Ample electrical margin ($2.885\text{ MWe}$ unallocated reserve). Low thermal stress on radiators.

### Case C: Emergency Survival Case (Reactor Offline / Battery Fallback)
* **Primary Source:** $1,200\text{ kWh}$ Solid-State Battery Bank + Regenerative Fuel Cells ($185\text{ kWe}$ continuous discharge rate)
* **Essential Life Support (ECLSS):** $80\text{ kWe}$
* **Thermal Pumps (Low Flow):** $50\text{ kWe}$
* **Avionics & Minimal Compute:** $20\text{ kWe}$
* **Emergency Habitat HVAC & Lighting:** $30\text{ kWe}$
* **Communications (Omni-laser beacon):** $5\text{ kWe}$
* **Total Emergency Load:** $185\text{ kWe}$ ($0.185\text{ MWe}$)
* **Emergency Survival Horizon:** $6.5\text{ hours}$ on pure battery storage; extended to $>90\text{ days}$ on auxiliary fuel cells utilizing $10\text{ MT}$ stored $\text{LH}_2 / O_2$ reserves.

---

## 4. Thermodynamic & Energy Closure Verification

1. **Conversion Loss Balance:** At full power ($100\text{ MWth}$ thermal input), $20.0\text{ MWe}$ is extracted as electricity and $80.0\text{ MWth}$ is rejected continuously through the primary $850\text{ K}$ NaK heat-pipe radiators ($2,502.8\text{ m}^2$).
2. **Secondary Waste Rejection:** Electrical loads convert $100\%$ of consumed electricity into waste heat. Household loads ($450\text{ kWe}$) reject heat at $295\text{ K} - 330\text{ K}$ through low-temperature water/ammonia radiators ($736.6\text{ m}^2$). NEP losses ($3.0\text{ MWth}$) radiate at $650\text{ K}$ ($189.4\text{ m}^2$).
3. **Total Vehicle Rejection Equilibrium:** Total thermal power rejected ($80.0\text{ MWth} + 3.0\text{ MWth} + 0.45\text{ MWth} = 83.45\text{ MWth}$) exactly balances reactor thermal generation plus electric dissipation, satisfying the First Law of Thermodynamics.
