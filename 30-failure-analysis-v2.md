# 30 — Quantitative Hostile Failure Analysis v2

**Document ID:** `30-failure-analysis-v2.md`
**Reopened Document:** Reopening and quantifying `19-failure-analysis-v1.md`
**Core Pipeline Framework:**
$$\text{DETECT} \longrightarrow \text{ISOLATE} \longrightarrow \text{STABILIZE} \longrightarrow \text{RECOVER} \longrightarrow \text{CONTINUE / ABORT}$$

---

## 1. Quantitative Failure Mode Matrix

| Failure Mode | Detection Time | Isolation Time | Stabilization Time | Resource Consumed | Degraded Operating State | Recovery Probability | Crew Exposure (Dose / Hazard) | Mission Impact / Decision |
|---|---:|---:|---:|---|---|---:|---|---|
| **01 — Main Reactor Core Scram / LOCA** | $<50\text{ ms}$ | $<150\text{ ms}$ | $<1.5\text{ s}$ | $20\text{ kg}$ NaK, $185\text{ kWe}$ battery power | $185\text{ kWe}$ emergency power state (house loads only) | $92.0\%$ | $<0.1\text{ mSv/hr}$ (Shielded shelter) | Abort NEP cruise; drift on free-return trajectory or execute NTP return. |
| **02 — Reactor NaK Primary Coolant Line Leak** | $<100\text{ ms}$ | $<250\text{ ms}$ | $<5.0\text{ s}$ | $150\text{ kg}$ NaK, $50\text{ kg}$ $N_2$ purge gas | $70\%$ reactor power state ($14\text{ MWe}$) | $95.0\%$ | Zero (Aft core section) | Continue mission at $70\%$ NEP thrust speed ($+14\text{ days}$ transit). |
| **03 — Primary Radiator Wing MMOD Destruction** | $<200\text{ ms}$ | $<500\text{ ms}$ | $<10.0\text{ s}$ | $24\text{ m}^2$ radiator panel area, $30\text{ kg}$ coolant | $85\%$ total thermal rejection capacity | $98.0\%$ | Zero (External vacuum) | Continue mission at $85\%$ power; swap spare heat-pipe cassette via RMS. |
| **04 — Central Spine Structural Member Buckling** | $<10\text{ ms}$ | Immediate | $<1.0\text{ s}$ | Zero (Structural load shift) | $75\%$ main engine thrust throttle limit ($3,000\text{ kN}$) | $88.0\%$ | Zero (Structural) | Continue mission at $75\%$ NTP acceleration ($+12\text{ min}$ burn duration). |
| **05 — Single NTP Main Engine Turbopump Seizure** | $<20\text{ ms}$ | $<80\text{ ms}$ | $<200\text{ ms}$ | $1,200\text{ kg}$ $\text{LH}_2$ vented | 3x NTP engine operation state ($750\text{ kN}$ total thrust) | $96.0\%$ | Zero | Extend burn duration by $+33\%$ to complete required Delta-V; continue mission. |
| **06 — Cryogenic Main $\text{LH}_2$ Tank Micro-Puncture** | $<100\text{ ms}$ | $<1.2\text{ s}$ | $<30.0\text{ s}$ | $450\text{ kg}$ $\text{LH}_2$ boil-off loss | Vacuum insulation sleeve bypass engaged | $90.0\%$ | Zero | Seal inner wall using composite patch drone; continue mission. |
| **07 — Habitat Deck 2 Explosive Decompression** | $<10\text{ ms}$ | $<1.2\text{ s}$ | $<5.0\text{ s}$ | $120\text{ kg}$ $N_2/O_2$ atmospheric buffer | Deck 2 isolated; crew concentrated in Decks 1 & 3 | $94.0\%$ | Transient pressure drop ($0.8 \rightarrow 0.5\text{ atm}$) | Repressurize deck after magnetic composite patch application; continue mission. |
| **08 — Main Electrical Bus Short-Circuit / Trip** | $<5\text{ ms}$ | $<15\text{ ms}$ | $<50\text{ ms}$ | $50\text{ kWh}$ battery buffer draw | Backup TMR Bus B active; non-critical loads shed | $99.5\%$ | Zero | Reset solid-state breakers; re-engage non-critical loads; continue. |
| **09 — Flight Control Computer Bit-Flip Cascade** | $<10\text{ ms}$ | $<20\text{ ms}$ | $<50\text{ ms}$ | Zero | TMR Rad-Hard Core B assumes authority | $99.9\%$ | Zero | Power-cycle Core A; re-flash optical ROM memory; fully nominal. |
| **10 — ECLSS Water Loop Biofilm Contamination** | $<30\text{ s}$ | $<1.0\text{ min}$ | $<5.0\text{ min}$ | $500\text{ kg}$ reserve water buffer | Emergency UV sterilizer + Catalytic bed online | $97.0\%$ | Zero (Toxic exposure prevented) | Flush loop with $120^\circ\text{C}$ superheated steam; swap filter beds; continue. |
| **11 — Navigation System Sensor Blinding / Glare** | $<50\text{ ms}$ | $<100\text{ ms}$ | $<1.0\text{ s}$ | Zero | Inertial Optical Gyro fallback state | $99.0\%$ | Zero | Autonomous recalibration against dark-sky stellar catalog; continue. |

---

## 2. Quantified 5-Stage Pipeline Case Studies

```
[ANOMALY] --> DETECT (<50ms) --> ISOLATE (<250ms) --> STABILIZE (<5s) --> RECOVER (1-48h) --> CONTINUE
```

### Deep-Dive: Mode 01 — Reactor LOCA / Core Scram Event
1. **DETECT ($<50\text{ ms}$):** Triple-redundant acoustic flowmeters and pressure differential sensors detect $15\text{ kPa/s}$ drop in primary NaK loop.
2. **ISOLATE ($<150\text{ ms}$):** Fast-acting pyrotechnic isolation valves wall off damaged Loop 1 manifold segment.
3. **STABILIZE ($<1.5\text{ s}$):** Pneumatic actuators insert $B_4C$ control rods into reactor core ($<1.5\text{ s}$ core SCRAM). Emergency decay heat Brayton loop engages automatically. $1,200\text{ kWh}$ solid-state battery assumes $185\text{ kWe}$ household survival load.
4. **RECOVER ($24\text{--}48\text{ hours}$):** Service drones deploy spare heat-pipe cassette from unpressurized cargo bay; automated welding head splices new NaK manifold. Core re-criticality executed under autonomous Ship OS supervision.
5. **CONTINUE / ABORT:** If $>75\%$ cooling capacity restored, continue mission in low-thrust NEP mode; otherwise execute $2.1\text{ km/s}$ NTP abort burn to Earth parking orbit.

### Deep-Dive: Mode 07 — Habitat Deck 2 Decompression
1. **DETECT ($<10\text{ ms}$):** Ultrasonic acoustic puncture transducers detect hull penetration ($dP/dt = 8.5\text{ kPa/s}$).
2. **ISOLATE ($<1.2\text{ s}$):** Solenoid pressure bulkheads seal Deck 2 from adjacent decks. Deck 2 pressure drops to $0.4\text{ atm}$ before sealing completes.
3. **STABILIZE ($<5.0\text{ s}$):** Emergency gas injection valves inject $80\text{ kg}$ $N_2/O_2$ into adjacent Decks 1 & 3 to maintain $0.80\text{ atm}$ equilibrium. Crew dons emergency pressure suits.
4. **RECOVER ($1\text{--}4\text{ hours}$):** Internal autonomous crawler locates $2.5\text{ cm}$ hole, applies magnetic elastomer composite patch, and cures patch with ultraviolet laser. Deck repressurized and helium leak-tested.
5. **CONTINUE / ABORT:** Mission nominal; full deck access restored.
