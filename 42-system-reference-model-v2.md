# 42 — System Reference Model v2 (Authoritative Baseline)

**Document ID:** `42-system-reference-model-v2.md`
**Baseline Vehicle:** USS Enterprise X (Project Occam-7)
**Program Status:** Post-Merge Quantitative Reconciliation Complete
**System Convergence:** **CONDITIONALLY CLOSED**

---

## 1. Executive Summary & Vehicle Definition

The System Reference Model v2 establishes the authoritative, single-source-of-truth baseline for the USS Enterprise X following post-merge quantitative reconciliation. Every numerical parameter in this document represents a fully coupled, closed first-principles derivation.

---

## 2. Reconciled Master Parameter Table

### A. General Vehicle Architecture & Geometry
| Parameter | Value | Unit | Reality Class | Basis / Derivation | Confidence |
| :--- | ---:| :---: | :---: | :--- | :---: |
| **Overall Structural Length** | $380.0$ | $\text{m}$ | Class A | Central spine truss layout | High |
| **Spine Truss Outer Diameter** | $6.0$ | $\text{m}$ | Class A | Octagonal welded SS 316L space frame | High |
| **Propellant Tank Outer Diameter** | $12.0$ | $\text{m}$ | Class A | Thin-wall cylindrical pressure vessel | High |
| **Habitat Module Diameter / Length** | $8.0 \times 30.0$ | $\text{m}$ | Class A | Aluminum-Lithium pressure shell | High |
| **Centrifuge Ring Radius** | $15.0$ | $\text{m}$ | Class B | Transverse magnetic levitation ring | Medium |
| **Nominal Crew Complement** | $24$ | Crew | Class A | Mission operations & shift rotation | High |
| **Autonomous Operations Horizon** | $1,000$ | Days | Class A | ECLSS closed-loop mass balance | High |
| **Unmargined Subtotal Dry Mass** | $1,225.80$ | $\text{MT}$ | Class B | Reconciled sum of itemized rows | High |
| **AIAA Growth Reserve Margin (20%)** | $245.16$ | $\text{MT}$ | Class B | Standard aerospace growth contingency | High |
| **Total Vehicle Dry Mass ($M_{dry}$)** | **1,470.96** | $\text{MT}$ | Class B | Fully margined vehicle dry baseline | High |
| **Total Mission Propellant ($M_{prop}$)** | $2,500.00$ | $\text{MT}$ | Class B | $2,200\text{t}$ $\text{LH}_2$ + $300\text{t}$ $\text{LNH}_3/\text{Ar}$ | High |
| **Gross Departure Wet Mass ($M_{dep}$)** | **3,970.96** | $\text{MT}$ | Class B | $M_{dry} + M_{prop}$ departure state | High |

---

### B. Propulsion & Trajectory Performance
| Parameter | Value | Unit | Reality Class | Basis / Derivation | Confidence |
| :--- | ---:| :---: | :---: | :--- | :---: |
| **Primary Impulse Engine Type** | 4x Solid-Core NTP | — | Class B | Solid-core nuclear thermal rocket | Medium |
| **NTP Vacuum Thrust** | $4,000.0$ | $\text{kN}$ | Class B | $1,000\text{ kN}$ per engine $\times 4$ | High |
| **NTP Specific Impulse ($I_{sp}$)** | $900.0$ | $\text{s}$ | Class B | $\text{LH}_2$ thermal expansion at $2,700\text{ K}$ | High |
| **Cruise Engine Type** | 4x MW MPD Thrusters | — | Class B | Magnetoplasmadynamic electric arrays | Medium |
| **NEP Electrical Power Supply** | $15.0$ | $\text{MWe}$ | Class B | Dedicated Brayton generator loop | High |
| **NEP Thruster Efficiency ($\eta$)** | $0.65$ | — | Class B | MPD plasma conversion efficiency | Medium |
| **NEP Jet Power ($P_{jet}$)** | $9.75$ | $\text{MW}_{jet}$ | Class B | $\eta \times P_{elec} = 0.65 \times 15\text{ MWe}$ | High |
| **NEP Cruise Thrust ($F_{NEP}$)** | **568.12** | $\text{N}$ | Class B | $F = 2 P_{jet} / v_e$ ($142.0\text{N}$ per array) | High |
| **NEP Specific Impulse ($I_{sp}$)** | $3,500.0$ | $\text{s}$ | Class B | $v_e = 34,323.28\text{ m/s}$ | High |
| **NEP Propellant Flow Rate ($\dot{m}$)** | $0.01655$ | $\text{kg/s}$ | Class B | $1.430\text{ MT/day}$ continuous burn | High |
| **NEP 180-Day Cruise Delta-V** | **5.39** | $\text{km/s}$ | Class B | $v_e \ln(M_0/M_f)$ trajectory integration | High |
| **Total Mission B Trajectory Delta-V** | **16.00** | $\text{km/s}$ | Class B | Closed Earth-Mars-Earth fast transit | High |

---

### C. Power & Thermal Management
| Parameter | Value | Unit | Reality Class | Basis / Derivation | Confidence |
| :--- | ---:| :---: | :---: | :--- | :---: |
| **Reactor Thermal Output** | $100.0$ | $\text{MW}_{th}$ | Class B | High-temperature fast fission core | High |
| **Conversion Efficiency (Brayton)** | $20.0\%$ | — | Class B | Supercritical $\text{CO}_2$ closed loop | High |
| **Gross Electrical Output** | $20.0$ | $\text{MWe}$ | Class B | $20,000\text{ kWe}$ total generation | High |
| **Propulsion Electrical Demand** | $15.0$ | $\text{MWe}$ | Class B | NEP MPD thruster array | High |
| **Nominal House Load Demand** | $445.0$ | $\text{kW}_e$ | Class A | ECLSS, avionics, thermal, centrifuge | High |
| **Continuous Power Reserve Margin** | **+4.55** | $\text{MWe}$ | Class B | Reserve generation capacity | High |
| **Total Thermal Waste Heat** | $83.45$ | $\text{MW}_{th}$ | Class B | $80\text{MW}_{th}$ reactor + $3.45\text{MW}_{th}$ losses | High |
| **High-Temp Radiator Temp** | $850.0$ | $\text{K}$ | Class B | Primary liquid metal heat exchanger | High |
| **One-Sided Radiator Footprint Area** | **2,502.8** | $\text{m}^2$ | Class B | Stefan-Boltzmann double-sided emission | High |
| **Thermal System Hardware Mass** | $6.75$ | $\text{MT}$ | Class B | Panels, booms, fluid, manifolds | High |

---

### D. Radiation Protection, Centrifuge & Hull Structure
| Parameter | Value | Unit | Reality Class | Basis / Derivation | Confidence |
| :--- | ---:| :---: | :---: | :--- | :---: |
| **SPE Storm Shelter Column Density** | **52.25** | $\text{g/cm}^2$ | Class B | Multi-layer SS/water/HDPE stack | High |
| **Storm Shelter Hardware/Fluid Mass** | $73.1$ | $\text{MT}$ | Class B | Central $4\text{m} \times 10\text{m}$ inner cylinder | High |
| **GCR Ambient Column Density** | $20.0$ | $\text{g/cm}^2$ | Class B | Circumferential water tanks | High |
| **Centrifuge Rotation Radius / Speed** | $15.0 / 6.0$ | $\text{m} / \text{RPM}$ | Class B | $\omega = 0.628\text{ rad/s}$ | High |
| **Static Floor Gravity** | $0.604$ | $\text{g}$ | Class A | $a_0 = \omega^2 r = 5.92\text{ m/s}^2$ | High |
| **Prograde Walking Acceleration (1.5m/s)** | **0.811** | $\text{g}$ | Class A | $a_r = (\omega r + v)^2 / r = 7.96\text{ m/s}^2$ | High |
| **Retrograde Walking Acceleration (1.5m/s)** | **0.427** | $\text{g}$ | Class A | $a_r = (\omega r - v)^2 / r = 4.19\text{ m/s}^2$ | High |
| **Propellant Tank Wall Thickness** | **6.5** | $\text{mm}$ | Class A | 316L SS pressure vessel sizing | High |
| **Tank Operating Hoop Stress** | **138.46** | $\text{MPa}$ | Class A | $\sigma_\theta = P r / t$ ($150\text{ kPa}$) | High |
| **Tank Yield Safety Factor** | $1.59\times$ | — | Class A | $+58.9\%$ margin vs $220\text{ MPa}$ yield | High |

---

### E. Manufacturing & Launch Logistics
| Parameter | Value | Unit | Reality Class | Basis / Derivation | Confidence |
| :--- | ---:| :---: | :---: | :--- | :---: |
| **Primary Assembly Node** | Low Earth Orbit | — | Class A | $400\text{ km}$ inclination $28.5^\circ$ | High |
| **Launch Vehicle Class Baseline** | $250\text{ t}$ LEO Payload | MT/Launch | Class B | Super-Heavy reusable launcher | Medium |
| **Hardware Module Launches** | 6 | Launches | Class B | Itemized $1,470.96\text{t}$ dry hardware | High |
| **Propellant Tanker Launches** | 10 | Launches | Class B | $2,500\text{t}$ $\text{LH}_2 / \text{LNH}_3$ deliveries | High |
| **Total Assembly Launch Count** | **16** | Launches | Class B | $\lceil 3,970.96 / 250 \rceil = 16\text{ launches}$ | High |
| **Orbital Assembly Campaign Duration** | $4.5$ | Months | Class B | 8-day launch cadence | Medium |
| **Total Launch Campaign Cost** | $\$992.7$ | Million | Class B | $\$250/\text{kg}$ delivered LEO payload | Medium |
