# 22 — Power System Architecture & Budget (Reconciled v2)

**Document ID:** `22-power-budget-v2.md`
**Primary Energy Source:** $100\text{ MW}_{th}$ High-Temperature Fast Fission Reactor
**Power Conversion:** Closed-Loop Supercritical $\text{CO}_2$ Brayton Turbines ($\eta = 20\%$)
**Total Electrical Output:** $20.0\text{ MWe}$ ($20,000\text{ kWe}$)

---

## 1. Electrical Power Generation & Allocation Architecture

```
[100 MWth Fast Reactor Core]
            │
            ▼
[Brayton Conversion (20% Eff)] ===> 20.0 MWe Gross Power Output
                                           │
            ┌──────────────────────────────┴──────────────────────────────┐
            ▼                                                             ▼
[15.0 MWe NEP Propulsion]                                    [5.0 MWe Non-Propulsive House]
  MPD Thrusters (η = 0.65)                                     ECLSS, Thermal, Avionics, Lasers
  Jet Power = 9.75 MWjet                                       Centrifuge, Computing, Payload
  Thrust = 568.1 N                                             Reserve Buffer = 3.86 MWe
```

---

## 2. Itemized Non-Propulsive House Load Budget

| Subsystem Load | Nominal Cruise ($\text{kW}_e$) | Peak Operation ($\text{kW}_e$) | Emergency Survival ($\text{kW}_e$) | Power Category |
| :--- | ---:| ---:| ---:| :--- |
| **ECLSS & Air/Water Processing** | 120.0 | 180.0 | 80.0 | Continuous Critical |
| **Thermal Loops & Cryo-Cooling** | 80.0 | 140.0 | 50.0 | Continuous Critical |
| **Avionics, Computing & Lasers** | 55.0 | 575.0 | 25.0 | High Transients |
| **Habitat HVAC, Lighting & Gym** | 60.0 | 90.0 | 30.0 | Habitability |
| **Centrifuge & Magnetic Bearings** | 25.0 | 45.0 | 0.0 | Dynamic Mechanics |
| **Science Payload & Workshops** | 70.0 | 300.0 | 0.0 | Mission Payload |
| **Battery Storage Charging Buffer** | 35.0 | 100.0 | 0.0 | Buffer Storage |
| **TOTAL NON-PROPULSIVE HOUSE LOAD** | **445.0 $\text{kW}_e$** | **1,430.0 $\text{kW}_e$** | **185.0 $\text{kW}_e$** | **House Subtotal** |
| **NEP MPD Thruster Demand** | 15,000.0 $\text{kW}_e$ | 15,000.0 $\text{kW}_e$ | 0.0 $\text{kW}_e$ | Propulsive Load |
| **TOTAL SYSTEM POWER DEMAND** | **15,445.0 $\text{kW}_e$** | **16,430.0 $\text{kW}_e$** | **185.0 $\text{kW}_e$** | **Total Demand** |
| **RESERVE POWER MARGIN** | **+4,555.0 $\text{kW}_e$** | **+3,570.0 $\text{kW}_e$** | **+19,815.0 $\text{kW}_e$** | **Margin vs 20 MWe** |

---

## 3. Power System Reconciliation (DEF-003)

1. **Reactor Output:** $100\text{ MW}_{th}$ thermal energy yields $20.0\text{ MWe}$ electrical output ($20,000\text{ kWe}$).
2. **Propulsion Power Balance:** $15.0\text{ MWe}$ dedicated to NEP MPD thrusters yields $9.75\text{ MW}_{jet}$ ($65\%$ thruster efficiency) and $568.12\text{ N}$ continuous thrust at $I_{sp} = 3,500\text{ s}$.
3. **House Power Balance:** Nominal non-propulsive house loads require $445\text{ kW}_e$ ($0.445\text{ MWe}$), peak loads require $1.43\text{ MWe}$, leaving a continuous reserve power margin of **$+3.57\text{ MWe}$ to $+4.56\text{ MWe}$** during all cruise operations.
