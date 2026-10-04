# 24 — Propulsion System Architecture Trade (Reconciled v2)

**Document ID:** `24-propulsion-trade-v2.md`
**Baseline Architecture:** Hybrid Dual-Mode NTP (High-Thrust) + NEP MPD (High-Efficiency Cruise)
**Primary Power Source:** 100 MWth / 20 MWe Fast Fission Reactor
**Reconciled NEP Thrust ($F_{NEP}$):** $568.12\text{ N}$ @ $15.0\text{ MWe}$ electrical input ($9.75\text{ MW}_{jet}$)

---

## 1. Hybrid Propulsion Architecture Coupling

```
[100 MWth Reactor] ===(Brayton 20%)===> [20 MWe Total Electric]
                                                │
                 ┌──────────────────────────────┴──────────────────────────────┐
                 ▼                                                             ▼
    [15 MWe NEP MPD Propulsion]                                   [5 MWe House / Payload]
      Efficiency: η = 0.65                                          ECLSS, Avionics, Lasers
      Jet Power:  9.75 MWjet                                        Thermal, Centrifuge
      Thrust:     568.1 N
      Exhaust:    ve = 34,323 m/s (3,500s Isp)
```

---

## 2. Quantitative Propulsion Mode Comparison

| Parameter | NTP Solid-Core Engine Array | NEP MPD Thruster Array | Reconciled Hybrid Baseline |
| :--- | :--- | :--- | :--- |
| **Engine Count & Type** | 4x Composite Solid-Core NTP | 4x Multi-Megawatt MPD Arrays | 4x NTP + 4x MPD Arrays |
| **Primary Propellant** | Liquid Hydrogen ($\text{LH}_2$) | Liquid Ammonia ($\text{LNH}_3$) / Argon | $\text{LH}_2$ ($2,200\text{ t}$) + $\text{LNH}_3$ ($300\text{ t}$) |
| **Specific Impulse ($I_{sp}$)** | $900\text{ s}$ ($v_e = 8,826\text{ m/s}$) | $3,500\text{ s}$ ($v_e = 34,323\text{ m/s}$) | **$1,800\text{ s}$ Effective Mission $I_{sp}$** |
| **Total Thrust ($F$)** | $4,000\text{ kN}$ ($1,000\text{ kN}$ per engine) | $568.1\text{ N}$ ($142.0\text{ N}$ per array) | $4,000\text{ kN}$ Impulse / $568.1\text{ N}$ Cruise |
| **Input Power Demand** | $100\text{ kW}$ (Pumps & Turbines) | $15.0\text{ MWe}$ ($9.75\text{ MW}_{jet}$) | $15.0\text{ MWe}$ NEP / $5.0\text{ MWe}$ House |
| **Propellant Mass Flow ($\dot{m}$)** | $453.2\text{ kg/s}$ ($1,631.5\text{ MT/hr}$) | $0.01655\text{ kg/s}$ ($1.430\text{ MT/day}$) | Dual-mode operational profile |
| **Primary Mission Function** | Impulsive TMI, MOI, TEI, EOC | Continuous low-thrust acceleration | Complete $16.0\text{ km/s}$ trajectory closure |

---

## 3. Thruster Efficiency & Jet Power Derivation

1. **Jet Power Equation:**
   $$P_{jet} = \eta_{thruster} \cdot P_{elec} = 0.65 \times 15.0\text{ MWe} = 9.75\text{ MW}_{jet}$$
2. **Thrust Derivation:**
   $$F_{NEP} = \frac{2 P_{jet}}{I_{sp} g_0} = \frac{2 \times 9,750,000}{3,500 \times 9.80665} = \mathbf{568.12\text{ N}}$$
3. **Propellant Consumption:**
   $$\dot{m}_{NEP} = \frac{568.12}{34,323.28} = 0.016552\text{ kg/s} = 1.430\text{ MT/day}$$
4. **180-Day Cruise Propellant Mass:**
   $$\Delta M_{cruise} = 1.4301\text{ MT/day} \times 180\text{ days} = 257.42\text{ MT}$$
