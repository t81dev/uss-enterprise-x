# 17 — Integrated System Budget v1

**Document ID:** `17-system-budget-v1.md`
**Baseline Vehicle Class:** Deep-Space Exploration Vessel (Mars / Outer System Transit)
**Nominal Crew Size:** 24 crew members
**Nominal Mission Duration:** 1,000 days autonomous operations
**Primary Propulsion Baseline:** High-Power Nuclear Thermal Propulsion (NTP) + High-Power Nuclear Electric Propulsion (NEP) hybrid

---

## 1. System Mass Budget

| Subsystem | Optimistic (t) | Baseline (t) | Pessimistic (t) | Unit | Basis / Method | Confidence | Reality Class | Source / Assumption |
|---|---|---|---|---|---|---|---|---|
| Primary Structure & Spine | 120 | 180 | 250 | MT | Finite-Element Beam/Shell | High | B | Stainless Steel 304L/316L 4mm-8mm skin |
| Pressure Hull (Habitat & Labs) | 80 | 120 | 160 | MT | Cylindrical pressure vessel ($8\text{m} \times 30\text{m}$) | High | A | ISO-grid reinforced welded SS rings |
| Passive Radiation Shielding | 150 | 220 | 300 | MT | SPE storm shelter + GCR circumferential tanks | Medium | B | Water/wastewater + polyethylene ($25\text{ g/cm}^2$) |
| Nuclear Reactor & Shielding | 45 | 65 | 90 | MT | 100 MWth / 20 MWe Fast Reactor | Medium | B | Shadow shield ($B_4C$ / Tungsten / $LiH$) |
| Propulsion Engines & Thrust Structure | 30 | 50 | 75 | MT | 4x Solid-Core NTP + 4x MW-Magnetoplasmadynamic | Medium | B | Dual-mode propulsion assembly |
| Main Propellant Tanks (Dry) | 40 | 65 | 95 | MT | Insulated Cryo Hydrolox/LNH3 tanks | High | A | Aluminium-Lithium / Stainless composite |
| Thermal Management (Radiators & Loops) | 25 | 40 | 60 | MT | Heat pipe arrays ($1.2\text{ kg/m}^2$, $12,000\text{ m}^2$) | Medium | B | Liquid metal NaK / Water heat pipes |
| ECLSS Hardware & Closed-Loop Plant | 15 | 25 | 35 | MT | ISS scaling with $98\%$ water / $95\%$ $O_2$ loop | High | A | Sabatier + Bosch + electrolysis systems |
| Avionics, Computing & Sensors | 5 | 8 | 12 | MT | Redundant rad-hard optical/processing buses | High | A | Triple-modular redundant processors + LiDAR |
| Guidance, Navigation & RCS | 10 | 15 | 22 | MT | Distributed RCS thrusters + reaction wheels | High | A | Hypergolic / cold gas RCS manifolds |
| Communications & High-Gain Optics | 3 | 5 | 8 | MT | Optical laser transceivers + RF dish arrays | High | A | 100W Deep-space optical communications |
| Crew Accommodations & Facilities | 15 | 22 | 30 | MT | Quarters, galley, medical, exercise equipment | High | A | Ergonomic modular flight hardware |
| Scientific Payload & Aux Vehicles | 30 | 50 | 80 | MT | Exobiology labs, landers, surface probes | Medium | B | Multi-mission science package |
| Defensive Systems & Shielding | 8 | 15 | 25 | MT | Layered Whipple shields + ablation laser | Medium | B | Stuffed Whipple shields for MMOD |
| Consumables (Food, Water, Gases) | 40 | 60 | 85 | MT | 1,000 days for 24 crew at closed-loop rates | High | A | $2.5\text{ kg/person/day}$ net system makeup |
| Reserve / Growth Margin ($20\%$) | 100 | 170 | 250 | MT | System growth contingency | High | B | AIAA standard design margin |
| **TOTAL DRY MASS** | **716** | **1,110** | **1,637** | **MT** | Sum of dry vehicle components | **Medium** | **B** | Baseline dry vehicle |
| **MAIN PROPELLANT** | 1,800 | 2,500 | 3,500 | MT | Liquid Hydrogen / Ammonia ($I_{sp}=900\text{s}$) | High | B | $2,500\text{ t}$ LH2 for $15\text{ km/s}$ total $\Delta V$ |
| **GROSS WET MASS** | **2,516** | **3,610** | **5,137** | **MT** | Full mission departure mass | **Medium** | **B** | Fully fueled departure state |

---

## 2. Electrical Power Budget

| Load Category | Continuous (kW) | Peak (kW) | Transient (kW) | Startup / Standby (kW) | Emergency (kW) | Basis / Description | Reality Class |
|---|---|---|---|---|---|---|---|
| ECLSS & Life Support | 120 | 180 | 250 | 60 | 80 | Air scrubbing, water distillation, oxygen generation | A |
| Thermal Control Loops & Pumps | 80 | 140 | 200 | 30 | 50 | Fluid circulation pumps, radiator deployment actuators | A |
| Avionics, Sensors & Computing | 40 | 75 | 100 | 25 | 20 | Rad-hard flight computers, LiDAR, radar, optical buses | A |
| Communications & Transceivers | 15 | 50 | 80 | 5 | 5 | Optical laser communications to Earth/Mars | A |
| Habitat Environment, Lighting, HVAC | 60 | 90 | 120 | 20 | 30 | Crew quarters, galley, environmental heating | A |
| Scientific Instrumentation | 50 | 200 | 400 | 10 | 0 | Mass spectrometers, subsurface radar, optical scopes | A |
| Electric Propulsion Subsystem | 0 | 15,000 | 20,000 | 0 | 0 | MW-Magnetoplasmadynamic NEP mode (cruise phase) | B |
| Active Defense & Laser Ablation | 5 | 500 | 2,000 | 5 | 0 | Optical sensor / laser ablation of orbital debris | B |
| Machine Shop & Automated Maintenance | 20 | 100 | 200 | 0 | 0 | Metal 3D printing, CNC mills, robotic arms | A |
| **TOTAL HOUSEHOLD LOAD (Non-Propulsive)** | **390** | **1,335** | **3,350** | **155** | **185** | Baseline vehicle operating requirement | **A/B** |
| **TOTAL WITH NEP PROPULSION** | **390** | **16,335** | **23,350** | **155** | **185** | Maximum electric power demand state | **B** |

---

## 3. Energy Budget by Mission Phase

| Mission Phase | Duration | Avg Power (kW) | Total Energy (GJ) | Primary Power Source | Energy Storage / Buffer | Reality Class |
|---|---|---|---|---|---|---|
| Launch & LEO Assembly | 30 Days | 500 | 1,300 | Solar / Fuel Cells / APU | Li-ion battery banks ($500\text{ kWh}$) | A |
| Trans-Mars Injection (NTP Acceleration) | 2 Hours | 2,000 | 14.4 | NTP Reactor Thermal/Electric | Regenerative fuel cells | B |
| Interplanetary Cruise (NEP Mode) | 180 Days | 15,000 | 233,280,000 | Main Nuclear Reactor ($20\text{ MWe}$) | Reactor thermal loop | B |
| Orbital Capture & Science Operations | 500 Days | 800 | 34,560,000 | Main Reactor (Low power mode) | Battery buffer | B |
| Trans-Earth Injection (NTP Acceleration) | 2 Hours | 2,000 | 14.4 | NTP Reactor Thermal/Electric | Regenerative fuel cells | B |
| Return Cruise & Aerocapture / EOI | 180 Days | 15,000 | 233,280,000 | Main Nuclear Reactor | Battery buffer | B |
| **TOTAL MISSION ENERGY EXPENDITURE** | **1,000 Days** | **—** | **$\sim 5.01 \times 10^8\text{ GJ}$** | **Primary Nuclear Core** | **Multi-layer redundancy** | **B** |

---

## 4. Thermal & Radiator Budget

| Subsystem Waste Heat | Continuous Heat (kWth) | Peak Heat (kWth) | Operating Temp (K) | Rejection Mechanism | Required Radiator Area ($m^2$) | Specific Mass ($kg/m^2$) | Reality Class |
|---|---|---|---|---|---|---|---|
| Main Nuclear Reactor Waste Heat | 80,000 | 100,000 | 850 K | Liquid Metal NaK Heat Pipes | 8,200 | 1.5 | B |
| Electric Engine Power Conversion Loss | 3,000 | 5,000 | 600 K | Carbon-composite heat pipes | 1,800 | 1.2 | B |
| Avionics & Computing | 40 | 75 | 320 K | Water heat pipes | 110 | 2.0 | A |
| Habitat Environmental Waste Heat | 180 | 270 | 295 K | Water / Ammonia loops | 550 | 2.2 | A |
| ECLSS Loop Heat Rejection | 120 | 180 | 310 K | Ammonia radiator panels | 380 | 2.0 | A |
| Scientific & Maintenance Equipment | 50 | 200 | 330 K | Local coolant loops | 120 | 2.0 | A |
| **TOTAL SYSTEM THERMAL REJECTION** | **83,390** | **105,725** | **—** | **Segmented Radiator Array** | **$\sim 11,160\text{ m}^2$** | **Avg 1.5** | **B** |

* **Stefan-Boltzmann Rejection Density:** At $850\text{ K}$ average reactor radiator temperature and emissivity $\epsilon = 0.90$, radiation flux $q = \epsilon \sigma T^4 = 0.90 \times (5.67 \times 10^{-8}) \times (850)^4 \approx 26.6\text{ kW/m}^2$.
* **Radiator Mass:** $11,160\text{ m}^2 \times 1.5\text{ kg/m}^2 \approx 16.7\text{ MT}$ (dry radiator structure) $+ 23.3\text{ MT}$ manifolds, fluid, deployable booms $\approx 40\text{ MT}$ total thermal system mass.

---

## 5. Volume Budget

| Compartment / Tankage | Pressurized Vol ($m^3$) | Unpressurized Vol ($m^3$) | Dimensions ($m$) | Primary Contents | Structural Shell | Reality Class |
|---|---|---|---|---|---|---|
| Habitat Deck 1 (Command & Avionics) | 350 | 0 | $8.0\text{m dia} \times 7.0\text{m length}$ | Flight deck, AI processing, communications | SS 316L Iso-grid | A |
| Habitat Deck 2 (Crew Quarters & Hygiene) | 450 | 0 | $8.0\text{m dia} \times 9.0\text{m length}$ | 24 Private berths, showers, quiet rooms | SS 316L Iso-grid | A |
| Habitat Deck 3 (ECLSS, Galley, Medical) | 500 | 0 | $8.0\text{m dia} \times 10.0\text{m length}$ | Life support plant, dining, infirmary, gym | SS 316L Iso-grid | A |
| Science Labs & Workshop Deck | 400 | 0 | $8.0\text{m dia} \times 8.0\text{m length}$ | Sample analysis, 3D printers, airlocks | SS 316L Iso-grid | A |
| Central Storm Shelter & Shielded Core | 150 | 0 | $4.0\text{m dia} \times 12.0\text{m length}$ | SPE radiation refuge, emergency command | Double-wall water tank | B |
| Main Propellant Tankage (LH2) | 0 | 35,000 | $12.0\text{m dia} \times 310\text{m length}$ | Cryogenic liquid hydrogen | Al-Li / SS Composite | B |
| Unpressurized Cargo & Lander Bay | 0 | 1,200 | $10.0\text{m dia} \times 15.0\text{m length}$ | Surface landers, probes, spare parts | Open truss framework | A |
| Reactor & Engineering Section | 0 | 800 | $6.0\text{m dia} \times 28.0\text{m length}$ | Fission core, power turbine, shadow shield | Stainless steel truss | B |
| **TOTAL VEHICLE VOLUME** | **1,850** | **37,000** | **Overall Length: $\sim 380\text{m}$** | **Integrated Spacecraft** | **Monocoque / Truss** | **B** |

---

## 6. Crew Resource & Consumables Budget

| Resource Category | Daily Rate per Crew | 24-Crew Daily Total | 1,000-Day Raw Requirement | Recovery / Loop Closure % | 1,000-Day Net Consumable Mass | Reality Class |
|---|---|---|---|---|---|---|
| Oxygen ($O_2$) | $0.84\text{ kg}$ | $20.16\text{ kg}$ | $20,160\text{ kg}$ | $95.0\%$ (Sabatier + Electrolysis) | $1,008\text{ kg}$ | A |
| Potable Water ($H_2O$) | $2.50\text{ kg}$ | $60.00\text{ kg}$ | $60,000\text{ kg}$ | $98.0\%$ (Vapor Compression Distillation)| $1,200\text{ kg}$ | A |
| Hygiene & Wash Water | $25.00\text{ kg}$ | $600.00\text{ kg}$ | $600,000\text{ kg}$ | $98.5\%$ (Filtration + RO) | $9,000\text{ kg}$ | A |
| Dry Food Ration | $0.62\text{ kg}$ | $14.88\text{ kg}$ | $14,880\text{ kg}$ | $0.0\%$ (Stored dehydrated rations) | $14,880\text{ kg}$ | A |
| Nitrogen Buffer Gas ($N_2$) | $0.05\text{ kg}$ | $1.20\text{ kg}$ | $1,200\text{ kg}$ | $99.0\%$ (Hull leakage makeup) | $120\text{ kg}$ | A |
| Medical, Hygiene, Clothing Consumables | $0.50\text{ kg}$ | $12.00\text{ kg}$ | $12,000\text{ kg}$ | $0.0\%$ (Single-use / disposable) | $12,000\text{ kg}$ | A |
| ECLSS Replacement Parts & Filter Beds | — | — | — | — | $10,000\text{ kg}$ | A |
| System Consumables Reserve ($50\%$) | — | — | — | — | $24,104\text{ kg}$ | B |
| **TOTAL NET CONSUMABLES MASS** | **—** | **—** | **—** | **—** | **$\sim 72,312\text{ kg}$ (72.3 MT)** | **A/B** |

---

## 7. Budget Synthesis & Feasibility Gate

1. **Mass Dominance:** Liquid hydrogen propellant ($2,500\text{ MT}$) accounts for $69.2\%$ of total vehicle gross wet mass ($3,610\text{ MT}$). Vehicle dry mass ($1,110\text{ MT}$) is dominated by structure ($180\text{ MT}$), radiation shielding ($220\text{ MT}$), and dry propellant tanks ($65\text{ MT}$).
2. **Thermal Feasibility:** The $100\text{ MWth}$ reactor core operating at $20\%$ electric conversion efficiency generates $80\text{ MWth}$ of continuous waste heat, requiring $\sim 8,200\text{ m}^2$ of high-temperature radiators operating at $850\text{ K}$. This radiator area is physically achievable using deployable liquid-metal heat pipe panels running along the $380\text{m}$ central spine.
3. **Power Feasibility:** Non-propulsive electrical demand ($390\text{ kWe}$ baseline, $1.33\text{ MWe}$ peak) is easily satisfied by a fraction of the $20\text{ MWe}$ output from the main nuclear generator, leaving ample margin for continuous electric propulsion thrust during cruise.
4. **Habitation Feasibility:** $1,850\text{ m}^3$ of pressurized volume provides $77\text{ m}^3$ per crew member, exceeding NASA long-duration health guidelines ($50\text{ m}^3/\text{person}$).
