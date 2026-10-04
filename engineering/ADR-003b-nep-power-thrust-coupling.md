# ADR-003b: Nuclear Electric Propulsion Power-Thrust Coupling

**Document ID:** `ADR-003b.md`
**Supercedes:** `ADR-003a` / `25-mission-performance-v1.md` (v1)
**Status:** APPROVED
**Date:** Post-Merge Forensic Reconciliation Phase

---

## 1. Context & Problem Statement

The previous v1 baseline stated an NEP thrust of $80\text{ N}$ operating at $I_{sp} = 3,500\text{ s}$ while allocating $15.0\text{ MWe}$ of electrical power from a $100\text{ MW}_{th}$ fast fission reactor.

A quantitative audit identified two critical physical errors:
1. **Uncoupled Jet Power:** An $80\text{ N}$ thrust at $I_{sp} = 3,500\text{ s}$ ($v_e = 34,323\text{ m/s}$) requires only $P_{jet} = 0.5 F v_e = 1.373\text{ MW}_{jet}$, leaving $>13\text{ MWe}$ of electrical power unassigned.
2. **Trajectory Breakdown:** $80\text{ N}$ continuous thrust operating on a $1,722.4\text{ t}$ vehicle for $180\text{ days}$ produces only $\Delta v = 0.73\text{ km/s}$, failing the required $2.55\text{ km/s}$ leg cruise $\Delta v$ by $3.5\times$.

---

## 2. Decision

Reconcile NEP thrust to match full $15.0\text{ MWe}$ propulsion power input at $\eta_{thruster} = 0.65$ MPD efficiency:

* **Electrical Power to Propulsion ($P_{elec}$):** $15.0\text{ MWe}$ ($15,000\text{ kWe}$)
* **Jet Power Output ($P_{jet}$):** $9.75\text{ MW}_{jet}$
* **Exhaust Velocity ($v_e$):** $34,323.28\text{ m/s}$ ($I_{sp} = 3,500\text{ s}$)
* **Reconciled NEP Thrust ($F_{NEP}$):** $\mathbf{568.12\text{ N}}$ ($142.0\text{ N}$ per MPD array)
* **Propellant Mass Flow Rate ($\dot{m}$):** $0.01655\text{ kg/s}$ ($1.430\text{ MT/day}$)
* **180-Day Cruise Delta-V:** $\mathbf{5.39\text{ km/s}}$ (exceeds $2.55\text{ km/s}$ requirement with $2.11\times$ margin)

---

## 3. Downstream Consequences

1. **Mission Trajectory Closure:** Continuous cruise acceleration achieves $5.39\text{ km/s}$ per leg, closing the $16.0\text{ km/s}$ Earth-Mars-Earth fast transit trajectory.
2. **Thermal Waste Heat Rejection:** $5.25\text{ MW}_{th}$ of thruster conversion waste heat is added to the central thermal loop, requiring $331.2\text{ m}^2$ of dedicated high-temp radiator panels.

---

## 4. Revisit Trigger

Demonstration of higher thruster conversion efficiency ($\eta > 0.75$) or higher specific impulse ($I_{sp} > 5,000\text{ s}$) during laboratory MPD testing.
