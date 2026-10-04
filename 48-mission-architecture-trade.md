# 48 — Mission Architecture Trade Study v1

**Document ID:** `48-mission-architecture-trade.md`
**Digital Twin Basis:** `engineering/calculations/mission_baseline.json`
**Program Status:** Mission Architecture Options & Trade Matrix

---

## 1. Executive Summary

`48-mission-architecture-trade.md` evaluates five distinct vehicle and mission architectural configurations for Project Occam-7. When evaluated against full sequential digital twin state integration, the baseline "Full Expeditionary" architecture ($3,970.96\text{ t}$ departure wet mass, $24\text{ crew}$, $1,000\text{ days}$) closed with zero propulsive margin for fast all-propulsive transits.

To establish programmatic robustness, five architecture options are traded across vehicle mass, power generation, thermal rejection, propellant inventory, launch logistics count, total mission cost, crew risk, and trajectory performance.

---

## 2. Vehicle Architecture Trade Matrix

| Architectural Parameter | Option A: Full Expeditionary (Baseline) | Option B: Pathfinder Enterprise | Option C: Cargo / Infrastructure Uncrewed | Option D: High-Power Enterprise | Option E: Low-Thrust / Long-Mission |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Primary Mission Objective** | 24-crew 1000d Mars surface science | 8-crew 500d Mars orbital/landing demo | Pre-positioned $1,500\text{t}$ surface/propellant cargo | 24-crew fast 120d Earth-Mars transit | 24-crew economical 1200d conjunction |
| **Nominal Crew Complement** | **24 Crew** | **8 Crew** | **Uncrewed (0)** | **24 Crew** | **24 Crew** |
| **Unmargined Dry Mass** | $1,225.80\text{ MT}$ | $520.00\text{ MT}$ | $680.00\text{ MT}$ | $1,650.00\text{ MT}$ | $1,225.80\text{ MT}$ |
| **AIAA Growth Reserve (20%)** | $245.16\text{ MT}$ | $104.00\text{ MT}$ | $136.00\text{ MT}$ | $330.00\text{ MT}$ | $245.16\text{ MT}$ |
| **Total Vehicle Dry Mass ($M_{dry}$)** | **1,470.96 MT** | **624.00 MT** | **816.00 MT** | **1,980.00 MT** | **1,470.96 MT** |
| **NTP $\text{LH}_2$ Propellant** | $2,200.00\text{ MT}$ | $800.00\text{ MT}$ | $1,200.00\text{ MT}$ | $3,500.00\text{ MT}$ | $1,600.00\text{ MT}$ |
| **NEP $\text{LNH}_3$ Propellant** | $300.00\text{ MT}$ | $100.00\text{ MT}$ | $200.00\text{ MT}$ | $500.00\text{ MT}$ | $400.00\text{ MT}$ |
| **Gross Departure Wet Mass ($M_{dep}$)** | **3,970.96 MT** | **1,524.00 MT** | **2,216.00 MT** | **5,980.00 MT** | **3,470.96 MT** |
| **Reactor Power Output** | $100\text{ MW}_{th} / 20\text{ MW}_e$ | $40\text{ MW}_{th} / 8\text{ MW}_e$ | $50\text{ MW}_{th} / 10\text{ MW}_e$ | $250\text{ MW}_{th} / 50\text{ MW}_e$ | $100\text{ MW}_{th} / 20\text{ MW}_e$ |
| **NEP Thrust Output** | $568.12\text{ N}$ | $227.25\text{ N}$ | $284.06\text{ N}$ | $1,893.73\text{ N}$ | $568.12\text{ N}$ |
| **Total Vehicle $\Delta v$ Capability** | **12.25 km/s** | **13.82 km/s** | **14.20 km/s** | **16.85 km/s** | **12.80 km/s** |
| **250t Heavy Launches Required** | **16 Launches** | **7 Launches** | **9 Launches** | **24 Launches** | **14 Launches** |
| **Estimated Campaign Cost** | **$992.7M** | **$381.0M** | **$554.0M** | **$1,495.0M** | **$867.7M** |
| **Mission Closure Status** | **CONDITIONALLY CLOSED** | **CLOSED** | **CLOSED** | **CLOSED** | **CLOSED** |

---

## 3. Comparative Architectural Analysis

### Option A: Full Expeditionary Enterprise (Baseline Baseline)
* **Strengths:** Maximum scientific yield, 24-crew capacity, full centrifuge gravity and storm shelter protection.
* **Weaknesses:** High launch count (16 launches), zero propulsive margin for all-propulsive $16.0\text{ km/s}$ fast transits without aerocapture.

### Option B: Pathfinder Enterprise (Risk-Reduction Precursor)
* **Strengths:** $60\%$ mass reduction ($1,524\text{ t}$ wet departure mass), fits in 7 heavy launches ($381\text{M}$ cost). Achieves $13.82\text{ km/s}$ vehicle $\Delta v$ with $800\text{ t}$ $\text{LH}_2$, providing robust propulsive closure.
* **Weaknesses:** Reduced crew complement (8 crew), smaller laboratory footprint.

### Option C: Cargo / Infrastructure Pre-Positioning Vehicle
* **Strengths:** Uncrewed logistics vessel delivering $1,400\text{ t}$ of surface supplies, landing craft, and return propellant to Mars orbit ahead of crew arrival.
* **Weaknesses:** Requires two launch cycles (Cargo vehicle departs 26 months prior to crew).

### Option D: High-Power Enterprise ($250\text{ MW}_{th} / 50\text{ MWe}$)
* **Strengths:** Delivers $1,894\text{ N}$ NEP thrust and $16.85\text{ km/s}$ total vehicle $\Delta v$, enabling true $120\text{-day}$ fast transit without atmospheric entry.
* **Weaknesses:** Heavy reactor and radiator mass ($1,980\text{ t}$ dry mass, $5,980\text{ t}$ departure wet mass), requiring 24 heavy launches.

### Option E: Low-Thrust / Extended-Transit Conjunction
* **Strengths:** Reuses baseline hardware while extending transit times to 210 days outbound/inbound ($1,200\text{-day}$ total mission horizon). Delivers $12.80\text{ km/s}$ $\Delta v$ on $3,470.96\text{ t}$ departure mass.
* **Weaknesses:** Increases crew space radiation exposure and consumable mass requirements.

---

## 4. Architectural Synthesis & Roadmap Recommendation

To balance technical feasibility, mission safety, and program cost, the program adopts a **Two-Phase Architecture Strategy**:

```
[ PHASE I: PATHFINDER (Option B) ]  ---> [ PHASE II: EXPEDITIONARY (Option A + Option C Cargo) ]
  - 8 Crew / 500 Days                      - Uncrewed Cargo Lander Pre-positioned (Option C)
  - 1,524 MT Wet Mass                      - Full 24 Crew / 1,000 Days (Option A)
  - 7 Launches / $381M                     - Aerocapture / In-Situ Propellant Refueling
```

1. **Pathfinder First Flight (Option B):** Demonstrates nuclear thermal and nuclear electric propulsion integration, centrifuge operations, and ECLSS closure with an 8-person crew in cislunar/Mars orbit.
2. **Cargo Pre-Positioning (Option C):** Uncrewed cargo vessel pre-positions surface habitat and surface return propellant in Mars orbit.
3. **Full Expeditionary Mission (Option A):** 24 crew depart for full 1,000-day expedition using Option C pre-positioned infrastructure to achieve $100\%$ mission success margin.
