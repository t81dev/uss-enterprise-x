# 45 — Mission Digital Twin Architecture & Simulation v1

**Document ID:** `45-mission-digital-twin-v1.md`
**Executable Model Source:** `engineering/calculations/mission_digital_twin.py`
**Baseline Dataset:** `engineering/calculations/mission_baseline.json`
**Program Status:** Sequential Mission Digital Twin Integration Complete

---

## 1. Executive Summary

`45-mission-digital-twin-v1.md` establishes the sequential state-space digital twin model for the USS Enterprise X (Project Occam-7). Prior program phases relied on static, uncoupled spreadsheet budgets that evaluated propulsion, thermal, power, and life-support subsystems independently.

The Digital Twin transitions the engineering model from isolated statics to **dynamic physical state propagation**. The vehicle is represented as a continuously coupled state vector integrated across time $t$. Every burn, coast, and orbital event updates vehicle mass $m(t)$, propellant inventories ($M_{LH2}, M_{LNH3}, M_{RCS}$), power generation $P(t)$, thermal loads $Q(t)$, radiator capacities $Q_{rad}(t)$, and velocity increments $\Delta v$.

---

## 2. Digital Twin State Vector Definition

The spacecraft state vector $\vec{S}(t)$ is defined as:

$$\vec{S}(t) = \begin{bmatrix} t \\ m_{gross}(t) \\ m_{LH2}(t) \\ m_{LNH3}(t) \\ m_{RCS}(t) \\ \mathbf{r}(t) \\ \mathbf{v}(t) \\ P_{reactor}(t) \\ P_{elec}(t) \\ Q_{thermal}(t) \\ Q_{radiator}(t) \\ N_{crew}(t) \\ H_{crew}(t) \\ \vec{\mathbf{H}}_{system}(t) \end{bmatrix}$$

### State Variables & Units:
* **Time ($t$):** Elapsed mission duration ($\text{days}$).
* **Gross Vehicle Mass ($m_{gross}$):** Total instantaneous vehicle mass ($1,470.96\text{ t Dry} + m_{prop}(t)$).
* **Propellant Inventories:** $m_{LH2}$ ($\text{NTP propellant}$), $m_{LNH3}$ ($\text{NEP propellant}$), $m_{RCS}$ ($\text{attitude control}$).
* **Position & Velocity ($\mathbf{r}, \mathbf{v}$):** Orbital phase and heliocentric velocity vector ($\text{km/s}$).
* **Power System:** $P_{reactor}$ ($\text{MW}_{th}$), $P_{elec}$ ($\text{MW}_e$), $P_{propulsion}$ ($\text{MW}_e$), $P_{house}$ ($\text{kW}_e$).
* **Thermal System:** $Q_{thermal}$ ($\text{MW}_{th}$ waste heat), $Q_{radiator}$ ($\text{MW}_{th}$ rejection capacity at $850\text{ K}$).
* **Crew & System Health:** $N_{crew}$ ($24\text{ crew}$), $H_{crew}$ ($\% \text{ health}$), $\vec{\mathbf{H}}_{system}$ ($\text{reactor, radiator, engine health vectors}$).

---

## 3. Propulsion State Integration Governing Equations

### A. Solid-Core Nuclear Thermal Propulsion (NTP)
During impulse maneuvers (TMI, MOI, TEI, EOI):
* **Vacuum Thrust:** $F_{NTP} = N_{eng} \times 1,000\text{ kN} = 4,000\text{ kN}$ (for 4 engines).
* **Specific Impulse:** $I_{sp} = 900.0\text{ s}$ ($v_e = I_{sp} g_0 = 8,825.985\text{ m/s}$).
* **Propellant Mass Flow Rate:**
  $$\dot{m}_{NTP} = \frac{F_{NTP}}{v_e} = \frac{4,000,000\text{ N}}{8,825.985\text{ m/s}} = \mathbf{453.2081\text{ kg/s}} = \mathbf{0.453208\text{ MT/s}}$$
* **Mass Integration:**
  $$m(t + \Delta t) = m(t) - \int_{t}^{t+\Delta t} \dot{m}_{NTP} dt$$
* **Velocity Increment:**
  $$\Delta v_{NTP} = \int_{t}^{t+\Delta t} \frac{F_{NTP}}{m(t)} dt = v_e \ln\left(\frac{m_{initial}}{m_{final}}\right)$$

### B. Magnetoplasmadynamic Nuclear Electric Propulsion (NEP)
During continuous cruise maneuvers (Outbound/Inbound transits):
* **Electrical Input:** $P_{elec} = 15.0\text{ MWe}$ (Brayton loop generation).
* **Conversion Efficiency:** $\eta = 0.65$ ($\text{MPD plasma efficiency}$).
* **Jet Power:** $P_{jet} = \eta \times P_{elec} = \mathbf{9.75\text{ MW}_{jet}}$.
* **Specific Impulse:** $I_{sp} = 3,500.0\text{ s}$ ($v_e = I_{sp} g_0 = 34,323.275\text{ m/s}$).
* **Continuous Jet Thrust:**
  $$F_{NEP} = \frac{2 P_{jet}}{v_e} = \frac{2 \times 9.75 \times 10^6}{34,323.28} = \mathbf{568.12\text{ N}}$$
* **Propellant Mass Flow Rate:**
  $$\dot{m}_{NEP} = \frac{F_{NEP}}{v_e} = \mathbf{0.016552\text{ kg/s}} = \mathbf{1.43008\text{ MT/day}}$$
* **Velocity Increment:**
  $$\Delta v_{NEP} = v_e \ln\left(\frac{m(t)}{m(t) - \dot{m}_{NEP} \Delta t}\right)$$

---

## 4. Sequential Mission B Simulation Baseline Results

Executing `mission_digital_twin.py` propagates the $3,970.96\text{ MT}$ gross departure vehicle sequentially through Mission B:

| Sequential Mission Phase | Propulsion Mode | Initial Mass (MT) | Propellant Burned (MT) | Final Mass (MT) | Duration | Actual Phase $\Delta v$ | Cum. $\Delta v$ ($\text{km/s}$) | Remaining Propellant Inventory |
| :--- | :---: | ---:| ---:| ---:| ---:| ---:| ---:| :--- |
| **0. Departure LEO Baseline** | — | $3,970.96$ | $0.00$ | $3,970.96$ | $0.0\text{ d}$ | $0.000\text{ km/s}$ | $0.000$ | $2,200.0\text{t LH}_2$ / $300.0\text{t LNH}_3$ |
| **1. Trans-Mars Injection (TMI)** | NTP ($4000\text{kN}$) | $3,970.96$ | $1,389.23\text{ LH}_2$ | $2,581.73$ | $51.1\text{ min}$ | $3.800\text{ km/s}$ | $3.800$ | $810.77\text{t LH}_2$ / $300.0\text{t LNH}_3$ |
| **2. Outbound Cruise Acceleration** | NEP ($568\text{N}$) | $2,581.73$ | $257.42\text{ LNH}_3$ | $2,324.31$ | $180.0\text{ days}$ | $3.605\text{ km/s}$ | $7.405$ | $810.77\text{t LH}_2$ / $42.58\text{t LNH}_3$ |
| **3. Mars Orbit Insertion (MOI)** | NTP ($4000\text{kN}$) | $2,324.31$ | $492.16\text{ LH}_2$ | $1,832.15$ | $18.1\text{ min}$ | $2.100\text{ km/s}$ | $9.505$ | $318.61\text{t LH}_2$ / $42.58\text{t LNH}_3$ |
| **4. Mars Orbit Stay & Operations** | House/ECLSS | $1,832.15$ | $46.27\text{ Consum.}$ | $1,785.88$ | $640.0\text{ days}$ | $0.000\text{ km/s}$ | $9.505$ | $318.61\text{t LH}_2$ / $42.58\text{t LNH}_3$ |
| **5. Trans-Earth Injection (TEI)** | NTP ($4000\text{kN}$) | $1,785.88$ | $318.61\text{ LH}_2$ | $1,467.27$ | $11.7\text{ min}$ | $1.734\text{ km/s}$ | $11.239$ | $0.00\text{t LH}_2$ / $42.58\text{t LNH}_3$ |
| **6. Inbound Cruise Acceleration** | NEP ($568\text{N}$) | $1,467.27$ | $42.58\text{ LNH}_3$ | $1,424.69$ | $29.8\text{ days}$ | $1.011\text{ km/s}$ | $12.250$ | $0.00\text{t LH}_2$ / $0.00\text{t LNH}_3$ |
| **TOTAL MISSION B DIGITAL TWIN** | **Hybrid NTP+NEP** | **3,970.96** | **2,500.00** | **1,424.69** | **849.8 days** | **12.250 km/s** | **12.250** | **100% Depleted Inventory** |

---

## 5. Physical Insights & Trajectory Findings

1. **Sequential Vehicle Mass Propagation (DEF-M02 Resolved):** Outbound NEP cruise occurs at an average vehicle mass of $\approx 2,453\text{ MT}$ (due to $810.77\text{ t}$ remaining NTP $\text{LH}_2$ onboard), generating $3.605\text{ km/s}$ of continuous $\Delta v$ over 180 days rather than the static reduced-mass assumption.
2. **Propellant Exhaustion & Actual Vehicle Capability (DEF-M03 Resolved):** The finite $2,200\text{ t}$ $\text{LH}_2$ inventory is fully expended after TMI ($1,389.23\text{ t}$), MOI ($492.16\text{ t}$), and TEI ($318.61\text{ t}$). The TEI burn produces $1.734\text{ km/s}$ $\Delta v$.
3. **Total Integrated Vehicle Velocity:** The baseline vessel delivers **$12.25\text{ km/s}$ total actual vehicle $\Delta v$** from its $2,500\text{ t}$ propellant inventory.
4. **Trajectory Gap:** While $12.25\text{ km/s}$ is sufficient for a 850-day opposition-class Earth-Mars return trajectory, fast 1,000-day high-energy transits demanding $>16.0\text{ km/s}$ require trajectory optimization or propellant augmentation.

---

## 6. Machine-Readable Digital Twin Interface (`mission_baseline.json`)

The Digital Twin outputs a validated JSON schema containing full event trace arrays, final vehicle state vectors, closure statuses, and failure case matrices.

```json
{
  "vehicle": {
    "name": "USS Enterprise X (Project Occam-7)",
    "dry_mass_mt": 1470.96,
    "propellant_inventory_mt": 2500.0,
    "gross_departure_mass_mt": 3970.96
  },
  "events": [ ... ],
  "final_state": {
    "time_days": 849.83,
    "gross_mass_mt": 1424.69,
    "total_delta_v_kms": 12.25,
    "reactor_power_mwth": 100.0,
    "radiator_capacity_mwth": 133.35
  },
  "closure_summary": {
    "status": "CLOSED",
    "total_vehicle_dv_kms": 12.25
  }
}
```
