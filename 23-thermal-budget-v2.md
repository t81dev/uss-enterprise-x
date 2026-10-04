# 23 — Thermal Management System & Rejection Budget (Reconciled v2)

**Document ID:** `23-thermal-budget-v2.md`
**Primary Heat Source:** $100\text{ MW}_{th}$ Fast Fission Reactor Waste Heat
**Total Rejection Requirement:** $83.45\text{ MW}_{th}$ ($80.0\text{ MW}_{th}$ Reactor + $3.45\text{ MW}_{th}$ Conversion/House)
**Radiator Operating Temperature:** $850\text{ K}$ High-Temp Reactor Loop / $295\text{ K}$ Habitat Loop
**Total Radiator Panel Footprint Area:** $2,502.8\text{ m}^2$ (One-sided) / $5,005.6\text{ m}^2$ Effective (Double-sided)

---

## 1. Subsystem Waste Heat Rejection & Radiator Sizing

Radiator surface area is derived using the Stefan-Boltzmann law with double-sided panel emission ($\epsilon = 0.90$, $15\%$ degradation margin):
$$Q_{radiated} = 2 \cdot A_{panel} \cdot \epsilon \cdot \sigma \cdot T^4$$

| Subsystem Heat Source | Waste Heat ($Q_{th}$) | Operating Temp ($T$) | Emissivity ($\epsilon$) | Specific Flux ($\text{kW/m}^2$) | One-Sided Footprint Area ($\text{m}^2$) | Radiator Panel Dry Mass ($\text{MT}$) |
| :--- | ---:| ---:| ---:| ---:| ---:| ---:|
| **Main Reactor Waste Heat** | $80,000.0\text{ kW}_{th}$ | $850\text{ K}$ | $0.90$ | $26.65\text{ kW/m}^2$ | $1,725.8\text{ m}^2$ | $3.11\text{ MT}$ |
| **NEP MPD Thruster Losses** | $5,250.0\text{ kW}_{th}$ | $650\text{ K}$ | $0.90$ | $9.11\text{ kW/m}^2$ | $331.2\text{ m}^2$ | $0.50\text{ MT}$ |
| **Brayton Conversion Losses** | $3,000.0\text{ kW}_{th}$ | $650\text{ K}$ | $0.90$ | $9.11\text{ kW/m}^2$ | $189.3\text{ m}^2$ | $0.28\text{ MT}$ |
| **Habitat Life Support (ECLSS)** | $200.0\text{ kW}_{th}$ | $295\text{ K}$ | $0.88$ | $0.380\text{ kW/m}^2$ | $151.3\text{ m}^2$ | $0.38\text{ MT}$ |
| **Avionics & Optical Compute** | $50.0\text{ kW}_{th}$ | $320\text{ K}$ | $0.88$ | $0.523\text{ kW/m}^2$ | $27.5\text{ m}^2$ | $0.06\text{ MT}$ |
| **Payload & Machine Shop** | $150.0\text{ kW}_{th}$ | $330\text{ K}$ | $0.88$ | $0.591\text{ kW/m}^2$ | $77.7\text{ m}^2$ | $0.16\text{ MT}$ |
| **SUBTOTAL RADIATOR PANELS** | **88,650.0 $\text{kW}_{th}$** | **Various** | **0.88–0.90** | **Various** | **2,502.8 $\text{m}^2$** | **4.49 MT** |
| **Booms, Fluid & Manifolds (+50%)** | — | — | — | — | — | **2.26 MT** |
| **TOTAL THERMAL HARDWARE MASS** | — | — | — | — | — | **6.75 MT** |

---

## 2. Geometric Layout & Deployment Integration

1. **Deployment Architecture:** Thermal radiators are deployed symmetrically along two lateral wings ($+\text{Y}$ and $-\text{Y}$ axes) cantilevered from the central spine truss.
2. **Physical Footprint:** With a designated deployment length of $150.0\text{ m}$ along the central spine section ($X = 60\text{ m}$ to $X = 210\text{ m}$):
   $$\text{Required Panel Width per Wing} = \frac{2,502.8\text{ m}^2}{2 \times 150.0\text{ m}} = \mathbf{8.34\text{ m}}$$
3. **Structural Integration:** Dual $8.34\text{ m} \times 150.0\text{ m}$ wings fold flat against the octagonal spine truss during launch and orbit assembly, deploying via active tensioning booms after reactor startup.
