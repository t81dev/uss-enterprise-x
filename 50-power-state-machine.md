# 50 — Power State Machine & Distribution Architecture v1

**Document ID:** `50-power-state-machine.md`
**Digital Twin Verification:** `engineering/calculations/mission_digital_twin.py`
**Program Status:** Integrated Power State Machine & Load Allocation

---

## 1. Executive Summary

`50-power-state-machine.md` defines the operational power states and distribution architecture for the USS Enterprise X. A power architecture that is closed only at steady-state cruise is insufficient for a complex deep-space vehicle.

The spacecraft utilizes a $100\text{ MW}_{th}$ fast-fission nuclear reactor coupled to a supercritical $\text{CO}_2$ ($s\text{CO}_2$) closed Brayton cycle conversion system delivering $20.0\text{ MWe}$ gross electrical generation ($20.0\%$ net thermodynamic efficiency). This document models electrical power allocation across 8 discrete operational states.

---

## 2. Power System Architecture Diagram

```
+-----------------------------------------------------------------------------------+
|                           100 MWth FAST FISSION REACTOR                           |
+-----------------------------------------------------------------------------------+
                                         |
                       [ Supercritical CO2 Brayton Loops (4x 5 MWe) ]
                                         |
                                Gross 20.0 MWe Generation
                                         |
         +-------------------------------+-------------------------------+
         |                               |                               |
  [ NEP Propulsion Bus ]       [ House Power Bus ]            [ Emergency / Reserve Bus ]
  Allocation: 15.0 MWe         Allocation: 0.445 MWe           Reserve: +4.555 MWe
  (MPD Thruster Arrays)        (ECLSS, Centrifuge, Avionics)   (Battery Charging, Science)
```

---

## 3. Power State Allocation Matrix

| Power State ID | Operational Mode | Gross Generation | NEP Propulsion Bus | House & ECLSS Load | Centrifuge MagLev Load | Science & Sensor Load | Net Reserve Margin | State Status |
| :---: | :--- | ---:| ---:| ---:| ---:| ---:| ---:| :---: |
| **ST-01** | **Nominal LEO Standby** | $2.00\text{ MWe}$ | $0.00\text{ MWe}$ | $0.300\text{ MWe}$ | $0.045\text{ MWe}$ | $0.050\text{ MWe}$ | **$+1.605\text{ MWe}$** | **STABLE** |
| **ST-02** | **NTP Impulse Support** | $20.00\text{ MWe}$ | $0.50\text{ MWe}$ | $0.350\text{ MWe}$ | $0.045\text{ MWe}$ | $0.050\text{ MWe}$ | **$+19.055\text{ MWe}$** | **STABLE** |
| **ST-03** | **NEP Cruise Maximum** | $20.00\text{ MWe}$ | $15.00\text{ MWe}$ | $0.350\text{ MWe}$ | $0.045\text{ MWe}$ | $0.050\text{ MWe}$ | **$+4.555\text{ MWe}$** | **STABLE** |
| **ST-04** | **Mars Orbital Science Max** | $5.00\text{ MWe}$ | $0.00\text{ MWe}$ | $0.400\text{ MWe}$ | $0.045\text{ MWe}$ | $0.250\text{ MWe}$ | **$+4.305\text{ MWe}$** | **STABLE** |
| **ST-05** | **Reactor Degraded (50%)** | $10.00\text{ MWe}$ | $7.50\text{ MWe}$ | $0.350\text{ MWe}$ | $0.045\text{ MWe}$ | $0.050\text{ MWe}$ | **$+2.055\text{ MWe}$** | **DEGRADED** |
| **ST-06** | **Radiator Loss (25%)** | $18.00\text{ MWe}$ | $13.50\text{ MWe}$ | $0.350\text{ MWe}$ | $0.045\text{ MWe}$ | $0.050\text{ MWe}$ | **$+4.055\text{ MWe}$** | **THROTTLED** |
| **ST-07** | **Emergency Life Support** | $1.00\text{ MWe}$ | $0.00\text{ MWe}$ | $0.200\text{ MWe}$ | $0.000\text{ MWe}$ | $0.000\text{ MWe}$ | **$+0.800\text{ MWe}$** | **CRITICAL** |
| **ST-08** | **Full Battery Backup** | $0.00\text{ MWe}$ | $0.00\text{ MWe}$ | $0.150\text{ MWe}$ | $0.000\text{ MWe}$ | $0.000\text{ MWe}$ | **$+0.000\text{ MWe}$** | **BATTERY (72h)** |

---

## 4. Itemized House Power Demand Breakdown

The continuous $445\text{ kW}_e$ ($0.445\text{ MWe}$) house power baseline is derived from first-principles component allocations:

* **Closed-Loop ECLSS System ($210\text{ kW}_e$):** Sabatier reactor, Vapor Compression Distillation (VCD) water recovery, Bosch carbon reactor, oxygen generation assembly ($180\text{ kW}_e$ nominal + $30\text{ kW}_e$ peak pumps).
* **Centrifuge Magnetic Bearings & Motor Drive ($45\text{ kW}_e$):** Active magnetic levitation position feedback ($25\text{ kW}_e$) + vacuum spin upkeep motor ($20\text{ kW}_e$).
* **Avionics, Optical Computing & Sensor Array ($65\text{ kW}_e$):** Triple modular redundant rad-hard optical processors ($25\text{ kW}_e$), LiDAR/optical nav ($20\text{ kW}_e$), deep-space laser communications ($20\text{ kW}_e$).
* **Thermal Control & Fluid Pumping ($85\text{ kW}_e$):** Primary $NaK$ liquid metal pumps ($50\text{ kW}_e$), secondary water loop pumps ($20\text{ kW}_e$), cryogenic $\text{LH}_2$ zero-boil-off cryocoolers ($15\text{ kW}_e$).
* **Crew Accommodations, Galley & Medical ($40\text{ kW}_e$):** Lighting, food preparation, diagnostic medical imaging, gym equipment.
* **TOTAL NOMINAL HOUSE LOAD:** **$445\text{ kW}_e$ ($0.445\text{ MWe}$)**.

---

## 5. State Transition & Interlock Rules

1. **Rule P1 (Propulsion Priority Interlock):** NEP propulsion load ($15.0\text{ MWe}$) is instantly shed if house load bus voltage drops below $95\%$ nominal, prioritizing ECLSS life support.
2. **Rule P2 (NTP Thermal Load shedding):** During NTP firing, NEP arrays are isolated and turbopump pre-cooling power ($0.50\text{ MWe}$) is energized from the primary generator bus.
3. **Rule P3 (Battery Buffer Reserve):** Li-S energy storage batteries ($500\text{ kWh}$) provide seamless 72-hour survival power ($0.150\text{ MWe}$) for ECLSS during reactor startup or transient shutdown.
