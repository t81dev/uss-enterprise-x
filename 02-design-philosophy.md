# 02 — Design Philosophy

## First-principles method

For every major feature, ask:

1. What mission requirement creates it?
2. What physical law constrains it?
3. What mass, power, thermal, volume, and maintenance cost does it impose?
4. Can another subsystem perform the same function more simply?
5. What happens when it fails?
6. Can it be manufactured repeatedly rather than crafted once?

## Simplification rule

> The best part is no part — but only after proving that removing the part does not merely move the complexity somewhere more dangerous.

The repository therefore distinguishes between **component elimination** and **complexity displacement**.

## Geometry

The ship should converge on a geometry that naturally follows from:

- axial thrust loads;
- pressure containment;
- radiation shielding;
- tankage;
- thermal radiators;
- maintenance access;
- rotating habitation where justified;
- propulsion field geometry if a future system requires it.

A cylindrical or lifting-body primary hull is therefore a **starting hypothesis**, not a sacred answer.
