# 51 — System Reference Model v3 (Authoritative Baseline)

**Document ID:** `51-system-reference-model-v3.md`
**Baseline Vehicle:** USS Enterprise X (Project Occam-7)
**Program Status:** Post-Digital Twin Sequential Physics Closure Complete
**System Convergence:** **CLOSED (Digital Twin Sequential State Verified)**

---

## 1. Executive Summary & Vehicle Definition

The System Reference Model v3 represents the ultimate single-source-of-truth engineering definition for the USS Enterprise X following full sequential digital twin mission integration (`mission_digital_twin.py`).

Every numerical metric in this model is derived from coupled first-principles calculations across geometry, structural loads, nuclear power generation, thermal radiation, magnetoplasmadynamic electric propulsion, solid-core nuclear thermal impulse, life support, radiation shielding, centrifuge dynamics, and launch manifests.

---

## 2. Reconciled Master Parameter Table (v3 Canonical Baseline)

### A. General Vehicle Geometry & Mass State
| Parameter | Value | Unit | Reality Class | First-Principles Derivation / Basis | Confidence |
| :--- | ---:| :---: | :---: | :--- | :---: |
| **Overall Structural Length** | $380.0$ | $\text{m}$ | Class A | Octagonal welded 316L SS space frame spine | High |
| **Spine Truss Outer Diameter** | $6.0$ | $\text{m}$ | Class A | $4,000\text{ kN}$ maximum NTP axial thrust load | High |
| **Propellant Tank Outer Diameter** | $12.0$ | $\text{m}$ | Class A | $6.5\text{mm}$ 316L SS skin ($\sigma_\theta = 138.5\text{ MPa}$) | High |
| **Habitat Pressure Hull Size** | $8.0 \times 30.0$ | $\text{m}$ | Class A | Al-Li pressure shell ($0.8\text{ atm}$ $N_2/O_2$) | High |
| **Centrifuge Ring Radius / RPM** | $15.0 / 6.0$ | $\text{m} / \text{RPM}$ | Class B | Transverse mag-lev ring ($a_{pro}=0.81\text{g}, a_{ret}=0.43\text{g}$) | Medium |
| **Nominal Crew Complement** | $24$ | Crew | Class A | 4-shift operational rotation & science staff | High |
| **Autonomous Horizon** | $1,000$ | Days | Class A | Closed-loop ECLSS net consumable balance | High |
| **Unmargined Subtotal Dry Mass** | **1,225.80** | $\text{MT}$ | Class B | Sum of 22 itemized subsystem rows | High |
| **AIAA Reserve Growth Margin (20%)** | **245.16** | $\text{MT}$ | Class B | Mandatory $20\%$ growth contingency | High |
| **Total Vehicle Dry Mass ($M_{dry}$)** | **1,470.96** | $\text{MT}$ | Class B | Fully margined dry structural baseline | High |
| **NTP Impulse Propellant ($\text{LH}_2$)** | **2,200.00** | $\text{MT}$ | Class B | $I_{sp} = 900\text{ s}$ main impulse inventory | High |
| **NEP Cruise Propellant ($\text{LNH}_3/\text{Ar}$)**| **300.00** | $\text{MT}$ | Class B | $I_{sp} = 3,500\text{ s}$ continuous electric inventory | High |
| **Gross Departure Wet Mass ($M_{dep}$)**| **3,970.96** | $\text{MT}$ | Class B | Total LEO departure mass ($M_{dry} + M_{prop}$) | High |
| **Maximum Structural Design Limit** | $4,500.00$ | $\text{MT}$ | Class A | Spine truss load rating limit | High |

---

### B. Propulsion & Sequential Trajectory Performance
| Parameter | Value | Unit | Reality Class | First-Principles Derivation / Basis | Confidence |
| :--- | ---:| :---: | :---: | :--- | :---: |
| **Primary Impulse Engine Type** | 4x Solid-Core NTP | — | Class B | Solid-core nuclear thermal rocket | High |
| **NTP Vacuum Thrust ($F_{NTP}$)** | $4,000.0$ | $\text{kN}$ | Class B | $1,000\text{ kN}$ per engine $\times 4$ engines | High |
| **NTP Specific Impulse ($I_{sp}$)** | $900.0$ | $\text{s}$ | Class B | $v_e = 8,825.985\text{ m/s}$ | High |
| **NTP Propellant Flow Rate ($\dot{m}$)**| $453.2081$ | $\text{kg/s}$ | Class B | $\dot{m} = F / v_e = 0.4532\text{ MT/s}$ | High |
| **Cruise Engine Type** | 4x MW MPD Thrusters | — | Class B | Magnetoplasmadynamic electric thruster array | Medium |
| **NEP Electrical Generation** | $15.0$ | $\text{MWe}$ | Class B | Dedicated Brayton loop generation | High |
| **NEP Thruster Efficiency ($\eta$)** | $0.65$ | — | Class B | MPD plasma conversion efficiency | Medium |
| **NEP Jet Power ($P_{jet}$)** | $9.75$ | $\text{MW}_{jet}$ | Class B | $P_{jet} = 0.65 \times 15.0\text{ MWe}$ | High |
| **NEP Jet Thrust ($F_{NEP}$)** | **568.12** | $\text{N}$ | Class B | $F = 2 P_{jet} / v_e$ ($142.0\text{ N}$ per thruster) | High |
| **NEP Specific Impulse ($I_{sp}$)** | $3,500.0$ | $\text{s}$ | Class B | $v_e = 34,323.275\text{ m/s}$ | High |
| **NEP Mass Flow Rate ($\dot{m}$)** | $0.016552$ | $\text{kg/s}$ | Class B | $1.43008\text{ MT/day}$ continuous burn | High |
| **Sequential Outbound NEP $\Delta v$** | **3.605** | $\text{km/s}$ | Class B | $v_e \ln(2581.73 / 2324.31)$ digital twin | High |
| **Total Vehicle $\Delta v$ Capability** | **12.250** | $\text{km/s}$ | Class B | Full sequential digital twin integration | High |

---

### C. Power & Thermal Management
| Parameter | Value | Unit | Reality Class | First-Principles Derivation / Basis | Confidence |
| :--- | ---:| :---: | :---: | :--- | :---: |
| **Reactor Thermal Output** | $100.0$ | $\text{MW}_{th}$ | Class B | High-temperature fast fission core | High |
| **Supercritical $\text{CO}_2$ Efficiency**| $20.0\%$ | — | Class B | $s\text{CO}_2$ closed Brayton cycle | High |
| **Gross Electrical Generation** | $20.0$ | $\text{MWe}$ | Class B | $20,000\text{ kWe}$ total electric output | High |
| **Propulsion Power Demand** | $15.0$ | $\text{MWe}$ | Class B | Dedicated NEP MPD thruster bus | High |
| **Nominal House Load Demand** | $0.445$ | $\text{MWe}$ | Class A | ECLSS, mag-lev, avionics, sensors | High |
| **Continuous Net Power Reserve** | **+4.555** | $\text{MWe}$ | Class B | Emergency battery charging & science | High |
| **Maximum Thermal Waste Heat** | $85.25$ | $\text{MW}_{th}$ | Class B | $80\text{ MW}_{th}$ reactor + $5.25\text{ MW}_{th}$ losses | High |
| **High-Temp Radiator Temp** | $850.0$ | $\text{K}$ | Class B | $NaK$ liquid metal heat-pipe manifold | High |
| **One-Sided Radiator Footprint** | $2,502.8$ | $\text{m}^2$ | Class B | Carbon-composite panel footprint | High |
| **Nominal Rejection Capacity** | **133.35** | $\text{MW}_{th}$ | Class B | Stefan-Boltzmann double-sided emission | High |
| **Degraded Capacity (15% Margin)**| **113.35** | $\text{MW}_{th}$ | Class B | Life-end thermal degradation rating | High |

---

### D. Radiation, Structure & Launch Manifest
| Parameter | Value | Unit | Reality Class | First-Principles Derivation / Basis | Confidence |
| :--- | ---:| :---: | :---: | :--- | :---: |
| **SPE Storm Shelter Column Density** | **52.25** | $\text{g/cm}^2$ | Class B | SS / Water / HDPE / SS multi-layer stack | High |
| **Storm Shelter Hardware Mass** | $73.1$ | $\text{MT}$ | Class B | $4\text{m} \times 10\text{m}$ inner storm cylinder | High |
| **Ambient GCR Column Density** | $20.0$ | $\text{g/cm}^2$ | Class B | Circumferential water buffer tanks | High |
| **Primary Assembly Node** | Low Earth Orbit | — | Class A | $400\text{ km}$ inclination $28.5^\circ$ | High |
| **Baseline Launch Vehicle Class** | $250$ | MT/Launch | Class B | Super-heavy reusable launch vehicle | Medium |
| **Hardware Module Launches** | 6 | Launches | Class B | $\lceil 1,470.96 / 250 \rceil = 6\text{ launches}$ | High |
| **Propellant Tanker Launches** | 10 | Launches | Class B | $\lceil 2,500.00 / 250 \rceil = 10\text{ launches}$ | High |
| **Total Assembly Launch Count** | **16** | Launches | Class B | $\lceil 3,970.96 / 250 \rceil = 16\text{ launches}$ | High |
| **Total Campaign Cost** | **$992.7** | Million | Class B | $\$250/\text{kg}$ delivered LEO payload | Medium |
