# 56 — Mission Event Timeline v1 (Model-Generated State Sequence)

**Document ID:** `56-mission-event-timeline-v1.md`
**Simulation Source:** `engineering/calculations/mission_digital_twin.py`
**Dataset:** `engineering/calculations/mission_baseline.json`
**Program Status:** Model-Generated Full Mission State Sequence Verified

---

## 1. Executive Summary

`56-mission-event-timeline-v1.md` documents the canonical sequential state vector of the USS Enterprise X across its 850-day baseline Earth-Mars-Earth round-trip mission.

Unlike manual spreadsheet estimates, every numerical parameter in this timeline is generated dynamically by the mission digital twin (`mission_digital_twin.py`), enforcing exact mass conservation, rocket equation integration, power-thermal state coupling, active ZBO cryogenic boiloff tracking, and crew health/radiation accumulation.

---

## 2. Complete Model-Generated Mission Event State Matrix

| Event ID | Event / Mission Phase Description | Mission Day ($t$) | Position / SOI | Gross Mass ($m$) | $\text{LH}_2$ Propellant | $\text{LNH}_3$ Propellant | Event $\Delta v$ | Cum. $\Delta v$ | Electrical Power | Thermal Waste | Radiator Capacity | Crew Health | Rad. Dose |
| :---: | :--- | :---: | :---: | ---:| ---:| ---:| ---:| ---:| ---:| ---:| ---:| ---:| ---: |
| **E01** | LEO Orbital Assembly Complete | $0.00\text{ d}$ | Earth LEO ($400\text{km}$) | $3,970.96\text{ t}$ | $2,200.00\text{ t}$ | $300.00\text{ t}$ | $0.000\text{ km/s}$ | $0.000$ | $20.00\text{ MWe}$ | $80.00\text{ MW}_{th}$ | $133.35\text{ MW}_{th}$ | $100.0\%$ | $0.00\text{ cSv}$ |
| **E02** | Trans-Mars Injection (TMI NTP) | $0.04\text{ d}$ | Earth Escape Hyperbola | $2,581.73\text{ t}$ | $810.77\text{ t}$ | $300.00\text{ t}$ | $3.800\text{ km/s}$ | $3.800$ | $20.00\text{ MWe}$ | $82.00\text{ MW}_{th}$ | $133.35\text{ MW}_{th}$ | $100.0\%$ | $0.00\text{ cSv}$ |
| **E03** | Outbound NEP Cruise Midpoint | $90.04\text{ d}$ | Heliocentric Transfer | $2,443.02\text{ t}$ | $803.57\text{ t}$ | $171.29\text{ t}$ | $1.802\text{ km/s}$ | $5.602$ | $20.00\text{ MWe}$ | $85.25\text{ MW}_{th}$ | $133.35\text{ MW}_{th}$ | $100.0\%$ | $6.30\text{ cSv}$ |
| **E04** | Outbound NEP Cruise Complete | $180.04\text{ d}$ | Mars Approach | $2,309.71\text{ t}$ | $796.37\text{ t}$ | $42.58\text{ t}$ | $1.803\text{ km/s}$ | $7.405$ | $20.00\text{ MWe}$ | $85.25\text{ MW}_{th}$ | $133.35\text{ MW}_{th}$ | $100.0\%$ | $12.60\text{ cSv}$ |
| **E05** | Mars Orbit Insertion (MOI NTP) | $180.05\text{ d}$ | Mars Orbit ($500\text{km}$) | $1,820.62\text{ t}$ | $307.28\text{ t}$ | $42.58\text{ t}$ | $2.100\text{ km/s}$ | $9.505$ | $20.00\text{ MWe}$ | $82.00\text{ MW}_{th}$ | $133.35\text{ MW}_{th}$ | $100.0\%$ | $12.60\text{ cSv}$ |
| **E06** | Mars Stay & Operations Midpoint | $500.05\text{ d}$ | Mars Orbit / Excursion | $1,787.82\text{ t}$ | $297.45\text{ t}$ | $42.58\text{ t}$ | $0.000\text{ km/s}$ | $9.505$ | $2.00\text{ MWe}$ | $8.00\text{ MW}_{th}$ | $133.35\text{ MW}_{th}$ | $100.0\%$ | $22.20\text{ cSv}$ |
| **E07** | Mars Stay Complete | $820.05\text{ d}$ | Mars Orbit Exit | $1,755.02\text{ t}$ | $287.62\text{ t}$ | $42.58\text{ t}$ | $0.000\text{ km/s}$ | $9.505$ | $2.00\text{ MWe}$ | $8.00\text{ MW}_{th}$ | $133.35\text{ MW}_{th}$ | $100.0\%$ | $31.80\text{ cSv}$ |
| **E08** | Trans-Earth Injection (TEI NTP) | $820.06\text{ d}$ | Mars Escape Hyperbola | $1,467.40\text{ t}$ | $0.00\text{ t}$ | $42.58\text{ t}$ | $1.511\text{ km/s}$ | $11.016$ | $20.00\text{ MWe}$ | $82.00\text{ MW}_{th}$ | $133.35\text{ MW}_{th}$ | $100.0\%$ | $31.80\text{ cSv}$ |
| **E09** | Inbound NEP Cruise Complete | $849.83\text{ d}$ | Earth Approach | $1,424.82\text{ t}$ | $0.00\text{ t}$ | $0.00\text{ t}$ | $1.000\text{ km/s}$ | $12.016$ | $20.00\text{ MWe}$ | $85.25\text{ MW}_{th}$ | $133.35\text{ MW}_{th}$ | $100.0\%$ | $33.88\text{ cSv}$ |
| **E10** | Earth Arrival & Capture | $849.83\text{ d}$ | Earth Orbit ($400\text{km}$) | $1,424.82\text{ t}$ | $0.00\text{ t}$ | $0.00\text{ t}$ | $0.000\text{ km/s}$ | $12.016$ | $20.00\text{ MWe}$ | $80.00\text{ MW}_{th}$ | $133.35\text{ MW}_{th}$ | $100.0\%$ | $33.88\text{ cSv}$ |

---

## 3. Key Dynamic Event Insights

1. **Mass Transition & Propellant Expenditure:**
   * Departure Mass: $3,970.96\text{ MT}$.
   * Propellant Expended: $2,165.95\text{ t}$ $\text{LH}_2$ + $300.00\text{ t}$ $\text{LNH}_3 = 2,465.95\text{ t}$.
   * Cryogenic Boiloff Loss: $34.05\text{ t}$ $\text{LH}_2$ over 850 days ($1.5\%$ of total $\text{LH}_2$ allocation).
   * Consumables Expended: $46.27\text{ t}$ ECLSS crew support over 640 days at Mars.
   * Final Mass at Earth Return: $1,424.82\text{ MT}$.

2. **Radiation Accumulation:**
   * Total Accumulated Crew Dose: **$33.88\text{ cSv}$** ($12.60\text{ cSv}$ outbound + $19.20\text{ cSv}$ Mars stay + $2.08\text{ cSv}$ inbound).
   * Lifetime Safety Margin: Below the $100\text{ cSv}$ NASA career limit by $66.12\text{ cSv}$.

3. **Power-Thermal Mode Switching:**
   * **NTP Burn Modes (E02, E05, E08):** Reactor provides main thrust; turbopump power demand = $0.5\text{ MWe}$. Thermal load = $82.0\text{ MW}_{th}$.
   * **NEP Cruise Modes (E03, E04, E09):** Dedicated $15.0\text{ MWe}$ MPD array bus active. Thermal waste heat = $85.25\text{ MW}_{th}$. Radiator capacity margin = $+48.10\text{ MW}_{th}$.
   * **Mars Stay Mode (E06, E07):** Reactor throttled down to $10.0\text{ MW}_{th}$ generating $2.0\text{ MWe}$ house load. Thermal waste heat drops to $8.0\text{ MW}_{th}$.
