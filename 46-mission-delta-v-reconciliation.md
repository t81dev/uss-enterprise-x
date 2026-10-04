# 46 — Mission Delta-V Reconciliation & Sequential Budget v1

**Document ID:** `46-mission-delta-v-reconciliation.md`
**Digital Twin Data Source:** `engineering/calculations/mission_baseline.json`
**Program Status:** Sequential Trajectory & Delta-V Reconciliation Complete

---

## 1. Executive Summary

This document reconciles the vehicle's true physical velocity capability against trajectory requirements. Previous project documentation asserted a flat $16.00\text{ km/s}$ trajectory target for Mission B (Earth-Mars-Earth fast transit) based on uncoupled spreadsheet estimates.

By integrating the vehicle state sequentially ($m_{initial} \rightarrow m_{final}$ per phase), this reconciliation demonstrates that the $2,500.0\text{ MT}$ declared propellant inventory ($2,200\text{ t}$ $\text{LH}_2$ + $300\text{ t}$ $\text{LNH}_3/\text{Ar}$) produces **$12.250\text{ km/s}$ of total actual vehicle $\Delta v$** when propagated through real vehicle departure wet mass ($3,970.96\text{ MT}$) and dry mass ($1,470.96\text{ MT}$).

---

## 2. Reconciled Sequential Delta-V Table (Mission B Baseline)

| Phase ID | Phase Name | Propulsion System | Start Mass ($m_i$) | Propellant Burned | End Mass ($m_f$) | Vacuum Thrust | Duration | Actual Vehicle $\Delta v$ | Nominal Trajectory Req. | Margin ($\Delta v_{act} - \Delta v_{req}$) |
| :---: | :--- | :---: | ---:| ---:| ---:| ---:| ---:| ---:| ---:| ---: |
| **P1** | **Trans-Mars Injection (TMI)** | 4x Solid NTP | $3,970.96\text{ t}$ | $1,389.23\text{ t LH}_2$ | $2,581.73\text{ t}$ | $4,000\text{ kN}$ | $51.1\text{ min}$ | **$3.800\text{ km/s}$** | $3.80\text{ km/s}$ | $+0.000\text{ km/s}$ |
| **P2** | **Outbound Cruise Acceleration** | 4x MW MPD Thrusters | $2,581.73\text{ t}$ | $257.42\text{ t LNH}_3$ | $2,324.31\text{ t}$ | $568.12\text{ N}$ | $180.0\text{ days}$ | **$3.605\text{ km/s}$** | $2.55\text{ km/s}$ | **$+1.055\text{ km/s}$** |
| **P3** | **Mars Orbit Insertion (MOI)** | 4x Solid NTP | $2,324.31\text{ t}$ | $492.16\text{ t LH}_2$ | $1,832.15\text{ t}$ | $4,000\text{ kN}$ | $18.1\text{ min}$ | **$2.100\text{ km/s}$** | $2.10\text{ km/s}$ | $+0.000\text{ km/s}$ |
| **P4** | **Mars Stay & Operations** | ECLSS / House | $1,832.15\text{ t}$ | $46.27\text{ t Consum.}$ | $1,785.88\text{ t}$ | $0\text{ N}$ | $640.0\text{ days}$ | **$0.000\text{ km/s}$** | $0.00\text{ km/s}$ | $+0.000\text{ km/s}$ |
| **P5** | **Trans-Earth Injection (TEI)** | 4x Solid NTP | $1,785.88\text{ t}$ | $318.61\text{ t LH}_2$ | $1,467.27\text{ t}$ | $4,000\text{ kN}$ | $11.7\text{ min}$ | **$1.734\text{ km/s}$** | $1.80\text{ km/s}$ | **$-0.066\text{ km/s}$** |
| **P6** | **Inbound Cruise Acceleration** | 4x MW MPD Thrusters | $1,467.27\text{ t}$ | $42.58\text{ t LNH}_3$ | $1,424.69\text{ t}$ | $568.12\text{ N}$ | $29.8\text{ days}$ | **$1.011\text{ km/s}$** | $2.55\text{ km/s}$ | **$-1.539\text{ km/s}$** |
| **P7** | **Earth Orbit Capture (EOI)** | 4x Solid NTP | $1,424.69\text{ t}$ | $0.00\text{ t LH}_2$ | $1,424.69\text{ t}$ | $4,000\text{ kN}$ | $0.0\text{ min}$ | **$0.000\text{ km/s}$** | $1.20\text{ km/s}$ | **$-1.200\text{ km/s}$** |
| **TOTAL** | **Sequential Integrated Mission** | **Hybrid NTP+NEP** | **$3,970.96\text{ t}$** | **$2,500.00\text{ t}$** | **$1,424.69\text{ t}$** | — | **$849.8\text{ days}$** | **$12.250\text{ km/s}$** | **$14.00\text{ km/s}$** | **$-1.750\text{ km/s}$** |

---

## 3. Subsystem Performance & Rocket Equation Physics

### A. NTP High-Thrust Impulse Integration
* **Total Thrust ($F_{NTP}$):** $4,000\text{ kN}$ ($4\times 1,000\text{ kN}$ solid-core nuclear thermal engines).
* **Specific Impulse ($I_{sp}$):** $900\text{ s}$ ($v_e = 8,825.985\text{ m/s}$).
* **Mass Flow Rate ($\dot{m}_{NTP}$):** $453.2081\text{ kg/s}$ ($0.453208\text{ MT/s}$).
* **Total $\text{LH}_2$ Inventory:** $2,200.00\text{ MT}$ finite physical allocation.

Burn breakdown:
1. **TMI:** Consumes $1,389.23\text{ t}$ $\text{LH}_2$ to accelerate $3,970.96\text{ t}$ vehicle by $3.80\text{ km/s}$. Remaining $\text{LH}_2 = 810.77\text{ t}$.
2. **MOI:** Consumes $492.16\text{ t}$ $\text{LH}_2$ to capture $2,324.31\text{ t}$ vehicle into Mars orbit with $2.10\text{ km/s}$ $\Delta v$. Remaining $\text{LH}_2 = 318.61\text{ t}$.
3. **TEI:** Consumes all remaining $318.61\text{ t}$ $\text{LH}_2$ to escape Mars orbit, generating $1.734\text{ km/s}$ $\Delta v$ on $1,785.88\text{ t}$ vehicle mass.

### B. NEP Electric Cruise Integration
* **Electrical Power Input:** $15.0\text{ MWe}$ dedicated Brayton generation.
* **Jet Power ($P_{jet}$):** $9.75\text{ MW}_{jet}$ ($\eta = 0.65$).
* **Specific Impulse ($I_{sp}$):** $3,500\text{ s}$ ($v_e = 34,323.275\text{ m/s}$).
* **Jet Thrust ($F_{NEP}$):** $568.12\text{ N}$.
* **Mass Flow Rate ($\dot{m}_{NEP}$):** $0.016552\text{ kg/s}$ ($1.43008\text{ MT/day}$).
* **Total $\text{LNH}_3/\text{Ar}$ Inventory:** $300.00\text{ MT}$ finite physical allocation.

Burn breakdown:
1. **Outbound NEP (180 Days):** Consumes $257.42\text{ t}$ $\text{LNH}_3$ from $2,581.73\text{ t}$ post-TMI wet mass, generating **$3.605\text{ km/s}$** continuous $\Delta v$. Remaining $\text{LNH}_3 = 42.58\text{ t}$.
2. **Inbound NEP (29.8 Days):** Consumes remaining $42.58\text{ t}$ $\text{LNH}_3$ from $1,467.27\text{ t}$ post-TEI mass, generating **$1.011\text{ km/s}$** continuous $\Delta v$.

---

## 4. Reconciliation Findings & Trajectory Trade-off

1. **Outbound Performance Surplus:** Outbound NEP cruise produces $+1.055\text{ km/s}$ more $\Delta v$ than previously budgeted ($3.605\text{ km/s}$ vs $2.55\text{ km/s}$) because the vehicle drops from $2,581.73\text{ t}$ to $2,324.31\text{ t}$.
2. **Inbound Performance Deficit:** Because $257.42\text{ t}$ of $\text{LNH}_3$ is spent outbound, only $42.58\text{ t}$ remains for return transit, limiting inbound NEP cruise to $29.8\text{ days}$ and $1.011\text{ km/s}$ $\Delta v$.
3. **Total Vehicle Capability:** The baseline spacecraft delivers **$12.250\text{ km/s}$ net vehicle $\Delta v$**.
4. **Trajectory Requirement Match:** A $12.25\text{ km/s}$ vehicle budget closes a nominal 850-to-1,000 day opposition Earth-Mars mission when utilizing atmospheric aerobraking / drag capture at Mars/Earth or when optimizing Earth-Mars transfer geometry (patched conic solution detailed in `47-earth-mars-trajectory-closure.md`).
