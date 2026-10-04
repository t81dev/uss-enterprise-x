# ADR-001b: Propellant Tank Structural Wall Thickness Sizing

**Document ID:** `ADR-001b.md`
**Supercedes:** `ADR-001a` / `28-structural-load-path.md` (v1)
**Status:** APPROVED
**Date:** Post-Merge Forensic Reconciliation Phase

---

## 1. Context & Problem Statement

The previous v1 baseline specified $12.0\text{ m}$ diameter main propellant tanks ($R = 6.0\text{ m}$) constructed with a $4.0\text{ mm}$ 316L Stainless Steel / Al-Li wall thickness under an internal ullage pressure $P_{ullage} = 150\text{ kPa}$. The v1 documentation reported a hoop stress of $112.5\text{ MPa}$.

A quantitative audit identified that $112.5\text{ MPa}$ was calculated using an incorrect geometry factor ($\sigma = P r / 2t$, valid for spherical shells). For a cylindrical shell, the thin-wall hoop relation is:
$$\sigma_\theta = \frac{P \cdot r}{t} = \frac{150,000 \times 6.0}{0.004} = \mathbf{225.0\text{ MPa}}$$

Because the yield strength of 316L Stainless Steel is $\sigma_y = 220\text{ MPa}$, the $4.0\text{ mm}$ wall thickness operates at $102.3\%$ of yield strength under normal operating pressure, creating a negative structural margin.

---

## 2. Decision

Select $t_{tank} = \mathbf{6.5\text{ mm}}$ 316L Stainless Steel for the primary $12.0\text{ m}$ diameter propellant tanks.

* **Operating Pressure ($P_{op}$):** $150\text{ kPa}$
* **Operating Hoop Stress ($\sigma_\theta$):** $138.46\text{ MPa}$
* **Allowable Design Stress ($\sigma_{allow} = \sigma_y / 1.5$):** $146.67\text{ MPa}$
* **Yield Safety Factor ($SF_{yield}$):** $1.59\times$ ($+58.9\%$ yield margin)
* **Proof Pressure ($1.25\times P_{op} = 187.5\text{ kPa}$):** $173.08\text{ MPa}$ ($SF_{proof} = 1.27\times$)

---

## 3. Downstream Consequences

1. **Tank Dry Mass Increase:** Tank wall volume across $310\text{ m}$ total length increases from $110.0\text{ MT}$ to $\mathbf{178.75\text{ MT}}$ ($+68.75\text{ MT}$ unmargined).
2. **System Mass Budget Propagation:** Unmargined vehicle dry mass increases from $1,157.0\text{ MT}$ to $1,225.80\text{ MT}$. Fully margined vehicle dry mass increases from $1,422.4\text{ MT}$ to $\mathbf{1,470.96\text{ MT}}$.
3. **Gross Departure Wet Mass:** Increases from $3,947.4\text{ MT}$ to $\mathbf{3,970.96\text{ MT}}$.

---

## 4. Revisit Trigger

Transition to carbon-composite linerless cryogenic tanks ($\rho = 1.55\text{ g/cm}^3$, $\sigma_y = 1,800\text{ MPa}$) during Phase 2 prototype qualification, which would reduce tank wall mass to $< 45\text{ MT}$.
