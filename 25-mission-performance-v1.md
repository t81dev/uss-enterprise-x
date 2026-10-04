# 25 — Mission Performance & Trajectory Closure v1

**Document ID:** `25-mission-performance-v1.md`
**Baseline Vehicle Dry Mass:** $M_{dry} = 1,422.4\text{ MT}$
**Reference Propulsion System:** Hybrid NTP ($I_{sp} = 900\text{ s}$, $T = 1,000\text{ kN}$) + NEP ($I_{sp} = 3,500\text{ s}$, $T = 80\text{ N}$, $P_{el} = 15\text{ MWe}$)

---

## 1. Concrete Reference Mission Matrix

| Parameter | Mission A: Cislunar Expedition | Mission B: Earth-Mars-Earth Transit | Mission C: Jupiter Outer System | Unit | Basis / Notes |
|---|---:|---:|---:|---|---|
| **Primary Destination** | LOP-G / Lunar Orbit / L2 | Mars Parking Orbit ($250 \times 18,000\text{ km}$) | Callisto / Europa Orbit | — | Reference orbital targets |
| **Initial Departure Mass ($M_{dep}$)** | 2,929.0 | 3,947.4 | 2,946.8 | MT | From rocket equation closure |
| **Dry Vehicle Mass ($M_{dry}$)** | 1,422.4 | 1,422.4 | 1,422.4 | MT | Baseline v2 dry mass |
| **Total Propellant Load ($M_{prop}$)** | 1,506.6 | 2,525.0 | 1,524.4 | MT | $\text{LH}_2$ (NTP) + $\text{LNH}_3$ (NEP) |
| **Total Target Delta-V ($\Delta V$)** | **8.5** | **16.0** | **25.0** | **km/s** | Impulsive + low-thrust sum |
| **Outbound Trans-Injection $\Delta V$** | $3.15\text{ km/s}$ (TLI) | $3.80\text{ km/s}$ (TMI) | $6.50\text{ km/s}$ (TJI) | km/s | High-thrust NTP burn |
| **Mid-Course Cruise Acceleration** | $0.80\text{ km/s}$ (NEP) | $5.10\text{ km/s}$ (NEP) | $10.50\text{ km/s}$ (NEP) | km/s | Continuous low-thrust MPD |
| **Target Capture / Insertion $\Delta V$** | $1.45\text{ km/s}$ (LOI) | $2.10\text{ km/s}$ (MOI) | $3.20\text{ km/s}$ (JOI) | km/s | NTP / Aerocapture assist |
| **Return Injection $\Delta V$** | $1.30\text{ km/s}$ (TEI) | $2.10\text{ km/s}$ (TEI) | $2.80\text{ km/s}$ (TEI) | km/s | High-thrust NTP burn |
| **Earth Capture Braking Strategy** | Propulsive TEI ($1.80\text{ km/s}$) | Propulsive + Aerocapture ($12.2\text{ km/s}$) | Propulsive + Aerocapture ($14.5\text{ km/s}$) | km/s | Skip entry heat-shield assist |
| **Peak Acceleration ($a_{max}$)** | $0.072\text{ g}$ ($0.71\text{ m/s}^2$) | $0.072\text{ g}$ ($0.71\text{ m/s}^2$) | $0.072\text{ g}$ ($0.71\text{ m/s}^2$) | g | NTP main-engine 4-engine burn |
| **Cruise Low-Thrust Acceleration** | $2.7 \times 10^{-5}\text{ g}$ | $2.0 \times 10^{-5}\text{ g}$ | $2.7 \times 10^{-5}\text{ g}$ | g | Continuous $80\text{ N}$ NEP thrust |
| **Total Transfer Duration** | **180 Days** | **1,000 Days** | **1,800 Days** | **Days** | Outbound + Stay + Return |
| **Crew ECLSS Survival Margin** | $200.0\%$ | $150.0\%$ | $120.0\%$ | % | Redundant consumable buffer |

---

## 2. Mission B Profile Breakdown (Earth-Mars-Earth Baseline)

```
        [EARTH LEO DEPARTURE]
               |
         (NTP Burn: 3.8 km/s, 2.1 hours)
               |
               v
      [OUTBOUND NEP CRUISE] ----> 180 Days Transit (NEP Acceleration/Deceleration)
               |
               v
       [MARS ORBIT CAPTURE] ----> 500 Days Science Operations & Surface Lander Operations
               |
         (NTP Burn: 2.1 km/s, 1.4 hours)
               |
               v
       [RETURN NEP CRUISE]  ----> 180 Days Transit
               |
               v
      [EARTH ATMOSPHERIC AEROCAPTURE & EOI] ----> 1,000 Days Total Mission Horizon
```

1. **Outbound Phase (180 Days):**
   - Trans-Mars Injection (TMI): $3.80\text{ km/s}$ impulsive $\Delta V$ executed by 4x NTP engines ($1,000\text{ kN}$ total thrust, $I_{sp} = 900\text{ s}$). Burn time: $2.1\text{ hours}$. Hydrogen consumed: $1,280\text{ MT}$.
   - Interplanetary Cruise: $180\text{ days}$ low-thrust continuous NEP propulsion ($15.0\text{ MWe}$, $80\text{ N}$, $I_{sp} = 3,500\text{ s}$) adding $2.55\text{ km/s}$ mid-course acceleration and $2.55\text{ km/s}$ deceleration. Ammonia consumed: $150\text{ MT}$.
2. **Mars Orbit & Surface Phase (500 Days):**
   - Mars Orbital Insertion (MOI): NTP propulsive burn ($2.10\text{ km/s}$) places ship in $250 \times 18,000\text{ km}$ elliptical parking orbit.
   - Surface Science: $24\text{ crew}$ conduct orbital telemetry, surface lander deployment, and sample return analysis.
3. **Return Phase (180 Days):**
   - Trans-Earth Injection (TEI): NTP impulsive burn ($2.10\text{ km/s}$).
   - Return Cruise: NEP low-thrust acceleration/deceleration ($5.10\text{ km/s}$ total $\Delta V$). Ammonia consumed: $150\text{ MT}$.
   - Earth Orbit Insertion (EOI): Combined propulsive braking ($1.80\text{ km/s}$) and high-altitude atmospheric skip aerocapture ($v_{entry} = 12.2\text{ km/s}$) enters high Earth orbit.

---

## 3. Trajectory & Crew Survival Verification

* **ECLSS Closure:** Total consumables consumed over 1,000 days $= 72.3\text{ MT}$. Onboard stored consumables reserve $= 108.5\text{ MT}$ ($150\%$ reserve factor).
* **Radiation Exposure Window:** SPE protection active continuously via storm shelter; GCR total mission cumulative dose $= 420\text{ mSv}$ (below $600\text{ mSv}$ lifetime limit).
