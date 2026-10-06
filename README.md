# USS Enterprise X — Project Occam-7

**A first-principles, adversarially validated engineering model of a reusable deep-space exploration system.**

> **Core thesis:**  
> Do not design the Enterprise from its silhouette inward. Design the mission from physics, constraints, dependencies, failure modes, manufacturing, and human survivability outward — then discover what an Enterprise-shaped vehicle must become.

Project Occam-7 is a speculative engineering program that asks a deliberately difficult question:

> **What would remain of the USS Enterprise if its mission, physics, mass, power, thermal, propulsion, logistics, manufacturing, autonomy, and crew-survival requirements were allowed to veto the fiction?**

The answer is not assumed in advance.

The architecture is progressively constructed, quantified, attacked, corrected, and re-evaluated.

---

## What This Project Actually Is

This repository is not a conventional spacecraft design study and it is not an attempt to make Star Trek technology appear real.

It is an **engineering reasoning experiment**.

The Enterprise is used as a demanding systems-level test case for a broader methodology:

```text
        CONCEPT
           │
           ▼
     FIRST PRINCIPLES
           │
           ▼
        MODEL
           │
           ▼
   SYSTEM INTEGRATION
           │
           ▼
    DIGITAL TWIN
           │
           ▼
  ADVERSARIAL TESTING
           │
      ┌────┴────┐
      │         │
     PASS      FAIL
      │         │
      │    REMEDIATION
      │         │
      └────┬────┘
           ▼
      DECISION GATE
           │
           ▼
      NEXT PHASE
```

The goal is not to prove that a starship can be built.

The goal is to determine **which parts of the idea survive when every hidden dependency is made explicit.**

---

# The Governing Rule

> **No mass, energy, propellant, infrastructure, time, or mission state may appear without a physically defensible source.**

Every important claim should therefore have:

1. A defined source.
2. A governing physical relationship.
3. Explicit assumptions.
4. A state transition or dependency relationship where applicable.
5. A failure condition.
6. A confidence or reality classification.
7. A test capable of breaking it.

A calculation that produces a number is not automatically evidence that the number is physically achievable.

A model can demonstrate **consistency with its assumptions**.

It cannot, by itself, demonstrate that those assumptions are true.

---

# The Project's Real Architecture

Project Occam-7 has evolved into a coupled system rather than a collection of subsystem studies.

```text
                         PROJECT OCCAM-7
                               │
             ┌─────────────────┴─────────────────┐
             │                                   │
        VEHICLE SYSTEM                       MISSION SYSTEM
             │                                   │
     ┌───────┼────────┐                 ┌────────┼────────┐
     │       │        │                 │        │        │
 Structure Propulsion Power         Trajectory  ISRU    Crew
     │       │        │                 │        │        │
     └───────┴────────┘                 └────────┴────────┘
             │                                   │
             └─────────────────┬─────────────────┘
                               │
                         DIGITAL TWIN
                               │
                    ┌──────────┴──────────┐
                    │                     │
               STATE MACHINE        SUCCESS PREDICATE
                    │                     │
                    └──────────┬──────────┘
                               │
                       ADVERSARIAL TESTS
                               │
                         MONTE CARLO
                               │
                       DECISION GATES
```

The important object is therefore not merely the spacecraft.

It is the **dependency graph connecting spacecraft, infrastructure, mission events, physical resources, and human survival.**

---

# Three Levels of Closure

Project Occam-7 deliberately distinguishes three different meanings of "closed."

## 1. Mathematical Closure

The equations balance.

Examples:

- mass conservation;
- energy accounting;
- propellant transfer accounting;
- radiator capacity;
- lander payload capacity;
- power demand;
- trajectory mechanics.

Mathematical closure answers:

> **Does the model balance?**

---

## 2. Engineering Closure

The system balances **with explicit engineering margin**.

A mathematically valid system with zero reserve is not automatically an acceptable engineering design.

Phase 8.4 therefore promoted thermal engineering margin to an authoritative mission prerequisite.

For example:

```text
Thermal load
     │
     ▼
Required capacity
     │
     ├── mathematical closure
     │
     └── required engineering margin
              │
              ▼
        mission prerequisite
```

Engineering closure answers:

> **Does the model still work when the required margin is enforced?**

---

## 3. Mission Closure

Every prerequisite in the dependency chain closes.

```text
Precursor deployment
        ↓
Power closure
        ↓
Peak-power closure
        ↓
Thermal closure
        ↓
Thermal-margin closure
        ↓
ISRU production
        ↓
Depot verification
        ↓
Crew departure authorization
        ↓
Mars operations
        ↓
Propellant transfer
        ↓
Return trajectory
        ↓
Earth capture
        ↓
Crew survivability
        ↓
MISSION SUCCESS
```

Mission closure answers:

> **Can the entire system execute the mission without silently assuming away a failed prerequisite?**

---

# The Most Important Architectural Discovery

The original Enterprise concept implicitly treated Mars propellant production as something that could happen after crew arrival.

That creates a dangerous dependency:

```text
Crew arrives
    ↓
ISRU must work
    ↓
ISRU must produce return propellant
    ↓
Crew can return
```

Project Occam-7 reverses that dependency.

## Architecture B — Precursor Autonomous Robotic ISRU Depot

```text
PHASE A — PRECURSOR

Earth
  │
  ▼
Robotic cargo missions
  │
  ▼
Mars surface
  │
  ├── nuclear power
  ├── excavation
  ├── water extraction
  ├── SOEC electrolysis
  ├── hydrogen processing
  ├── liquefaction
  ├── cryogenic storage
  └── autonomous verification
             │
             ▼
      VERIFIED DEPOT
             │
             ▼
      CREW LAUNCH GATE
             │
             ▼

PHASE B — CREWED

Earth
  │
  ▼
Enterprise X
  │
  ▼
Mars
  │
  ▼
Verified return propellant
  │
  ▼
Earth return
```

The crew is not authorized to depart Earth until the return-resource dependency has already been demonstrated.

This converts a potentially catastrophic **crew-coupled dependency** into a **pre-departure infrastructure gate**.

That architectural principle is more important than any individual propulsion technology in the repository.

---

# Current Canonical Vehicle Baseline

The current baseline models a large reusable deep-space exploration vessel with:

| Parameter | Baseline |
|---|---:|
| Crew | 24 |
| Structural length | 380 m |
| Dry mass | 1,470.96 t |
| Initial mission propellant | 2,500 t |
| Nominal LEO departure mass | 3,970.96 t |
| NTP engines | 4 |
| NTP thrust | 4,000 kN |
| NTP specific impulse | 900 s |
| NEP cruise thrust | ~568 N |
| NEP specific impulse | 3,500 s |
| Ship reactor | 100 MWth / 20 MWe |
| Mars precursor reactor | 25 MWe |
| Mars precursor landers | 2 × 150 t |
| Nominal mission duration | ~850 days |
| Mission digital-twin Δv | 18.534 km/s |
| Verified crew return LH₂ load | 2,200 t |
| Program status | **Engineeringally Conditional** |

These values are **model outputs and design parameters**, not claims that equivalent flight hardware currently exists.

---

# Mars ISRU Is a System, Not a Magic Box

The Mars precursor architecture treats propellant production as an industrial system with explicit resource and energy requirements.

The model includes:

- autonomous excavation;
- water extraction;
- purification;
- high-temperature SOEC electrolysis;
- hydrogen processing;
- cryogenic liquefaction;
- zero-boiloff storage;
- power generation;
- thermal rejection;
- transfer losses;
- inventory accounting;
- maintenance and downtime;
- payload delivery constraints;
- verification gates.

The precursor architecture currently uses:

- **2 × 150 t cargo landers**;
- a dedicated nuclear surface power system;
- modular radiator infrastructure;
- autonomous production;
- machine-readable inventory verification;
- mandatory pre-departure authorization.

The key rule is:

> **The crew cannot manufacture its way out of an unverified precursor failure.**

If the depot is not ready, the mission stops on Earth.

---

# Conservation Is a Hard Boundary

The digital twin explicitly tracks physical inventories across mission events.

For example, return propellant transfer is modeled as:

```text
Depot inventory
      │
      ├── transfer losses
      │
      └── spacecraft credit
```

For a 2,200 t required net load:

```text
Total transfer loss = 3.5%

Gross depot withdrawal
    = 2200 / (1 - 0.035)
    ≈ 2279.79 t
```

The model must debit the depot before crediting the spacecraft.

Repeated mission execution cannot duplicate the same inventory.

Mass conservation is tested explicitly.

This principle generalizes:

> **The simulation is not allowed to create resources merely because the mission requires them.**

---

# Mission State Is Also a Conserved Resource

A mission state cannot advance merely because a later calculation assumes that it has.

The digital twin therefore models explicit prerequisite states such as:

```text
PRECURSOR_NOT_DEPLOYED
        ↓
PRECURSOR_DEPLOYED
        ↓
ISRU_OPERATIONAL
        ↓
PROPULSANT_PRODUCTION_COMPLETE
        ↓
DEPOT_VERIFIED
        ↓
CREW_DEPARTURE_AUTHORIZED
```

Breaking any prerequisite must prevent downstream authorization.

This is tested adversarially.

The same principle applies to:

- payload delivery;
- power;
- thermal rejection;
- propellant inventory;
- trajectory closure;
- crew survivability;
- Earth departure;
- Mars encounter;
- return capture.

---

# Hostile Engineering Is a Feature

The repository intentionally searches for ways to make its own model fail.

Examples of defects that have been discovered and remediated include:

- thermodynamic radiator sizing errors;
- unrealistic structural assumptions;
- insufficient shielding assumptions;
- artificial-gravity physiological problems;
- invalid ISRU architecture;
- impossible lander payload allocation;
- aggregate capacity hiding individual payload failure;
- incomplete surface power accounting;
- peak-power omission;
- thermal capacity without engineering margin;
- Monte Carlo variables disconnected from the underlying model;
- incorrect propellant-transfer loss accounting;
- mass conservation violations;
- state-machine initialization defects;
- duplicate depot inventory;
- production models artificially clamped to target output;
- failure classifications that confused root causes with cascaded predicates.

The desired response to a contradiction is not to hide it.

It is:

```text
FIND
  ↓
CLASSIFY
  ↓
FAIL
  ↓
REMEDIATE
  ↓
TEST
  ↓
REGENERATE
  ↓
RE-EVALUATE
```

---

# Uncertainty Is Part of the Architecture

A nominally successful deterministic simulation is insufficient.

The repository therefore uses Monte Carlo analysis to explore uncertainty in:

- vehicle dry mass;
- propellant inventory;
- propulsion performance;
- electric propulsion efficiency;
- surface nuclear power;
- ISRU efficiency;
- ice concentration;
- plant availability;
- maintenance downtime;
- lander capacity;
- thermal capacity;
- correlated environmental degradation.

The current machine-readable analysis uses **10,000 simulated cases**.

The latest independent uncertainty scenario reports:

**93.10% estimated success probability**

with a 95% Wilson confidence interval of:

**92.59%–93.58%**

A modeled common-cause degradation scenario reduces the result to:

**64.74%**

with a 95% interval of:

**63.80%–65.67%**

This distinction is deliberate.

> **Independent uncertainty can look manageable while correlated degradation exposes architectural fragility.**

The project therefore treats common-cause failure as a first-class engineering problem.

---

# Reality Classification

Every significant technology or claim belongs to an explicit epistemic category.

| Class | Meaning |
|---|---|
| **VERIFIED** | Supported by repository calculations, conservation laws, and automated verification |
| **MODELED** | Numerically represented using explicit physical assumptions |
| **ASSUMED** | Required scenario parameter without sufficient empirical validation |
| **FRONTIER** | Physically plausible but not demonstrated at required scale |
| **SCIENCE FICTION** | Retained as fictional technology rather than engineering reality |

The repository currently contains **no technology that becomes physically credible merely because it has been modeled.**

For example:

- nuclear thermal propulsion is treated as frontier hardware;
- MW-scale MPD propulsion is treated as frontier;
- autonomous Mars industrialization is treated as frontier;
- large surface nuclear power systems are treated as frontier;
- the physics equations governing those systems can nevertheless be modeled.

The distinction is intentional.

---

# The Ship Is More Than a Vehicle

The Enterprise is modeled as an integrated long-duration system:

```text
STRUCTURE
    │
    ├── pressure
    ├── thrust loads
    ├── tanks
    ├── radiation protection
    └── MMOD protection

POWER
    │
    ├── reactor
    ├── conversion
    ├── distribution
    └── storage

THERMAL
    │
    ├── waste heat
    ├── radiators
    ├── degradation margin
    └── transient capacity

PROPULSION
    │
    ├── NTP
    ├── NEP
    ├── propellant inventory
    └── trajectory integration

HABITAT
    │
    ├── ECLSS
    ├── artificial gravity
    ├── radiation protection
    ├── medical systems
    └── crew resources

AUTONOMY
    │
    ├── navigation
    ├── maintenance
    ├── diagnostics
    ├── manufacturing
    └── scientific operations
```

No subsystem is considered complete merely because its own equations close.

Its interfaces must also close.

---

# ShipOS

The proposed Ship Operating System reflects the same philosophy.

Safety-critical control is deliberately separated from probabilistic autonomy.

```text
TIER 1 — SAFETY-CRITICAL CONTROL
          deterministic / hard real-time / no AI authority

TIER 2 — MISSION CONTROL & GNC
          deterministic estimation and optimization

TIER 3 — MAINTENANCE AUTOMATION
          diagnostics / robotics / predictive analysis

TIER 4 — CREW ASSISTANCE
          interfaces / decision support / medical monitoring

TIER 5 — MANUFACTURING
          fabrication / inspection / repair

TIER 6 — SCIENTIFIC AUTONOMY
          science planning / classification / targeting
```

The underlying principle is:

> **Autonomy may increase capability without being allowed to erase authority boundaries.**

A neural system may recommend.

A deterministic safety layer decides whether the physical action is permissible.

---

# The Digital Twin

The mission digital twin is the repository's computational center of gravity.

It propagates a coupled system state containing quantities such as:

- mission time;
- gross mass;
- propellant inventories;
- position;
- velocity;
- reactor power;
- electrical power;
- thermal load;
- radiator capacity;
- crew state;
- system health.

Mission events update the state rather than merely reporting independent calculations.

Examples include:

```text
TMI
 ↓
NEP cruise
 ↓
MOI
 ↓
Mars operations
 ↓
ISRU/refueling
 ↓
TEI
 ↓
NEP return
 ↓
Earth capture
```

The latest baseline records complete event-level mass conservation and evaluates a canonical mission success predicate.

---

# The Success Predicate

Mission success is not a narrative conclusion.

It is the conjunction of physical and state predicates.

Conceptually:

```python
mission_success = all(canonical_predicates.values())
```

The predicate includes conditions such as:

- precursor payload closure;
- precursor deployment;
- ISRU operation;
- production completion;
- depot verification;
- average power closure;
- peak power closure;
- thermal closure;
- thermal margin compliance;
- authorized Earth departure;
- Mars encounter;
- Mars operations;
- return propellant availability;
- return propellant transfer;
- return propellant loading;
- return trajectory closure;
- Earth capture;
- positive reserves;
- crew survivability;
- mass conservation;
- absence of critical failure.

A failed prerequisite cannot be silently bypassed by a later subsystem.

---

# What the Project Has Falsified

The project is valuable partly because it destroys ideas.

Among the major conclusions so far:

### The original onboard-Mars-ISRU concept fails

The Enterprise cannot simply carry a Mars ISRU plant, land on Mars, and manufacture thousands of tonnes of return propellant while the crew waits.

**Architecture: invalid.**

### Aggregate payload capacity is insufficient

A 300 t aggregate capacity does not mean a 256–276 t plant fits if one individual lander is overloaded.

**Component-level packing is mandatory.**

### Average power is insufficient as a sole criterion

A system can have adequate average energy while failing at peak load.

**Average and peak power must be independently gated.**

### Mathematical thermal closure is insufficient

A radiator system can reject exactly the required heat and still have zero engineering margin.

**Capacity and margin must be separate predicates.**

### Nominal Monte Carlo success is insufficient

Independent uncertainty can underestimate correlated failure.

**Common-cause scenarios must be evaluated separately.**

### Vehicle Δv is not trajectory closure

A rocket equation result is not automatically an Earth–Mars mission.

**Vehicle capability and trajectory requirement must remain distinct concepts.**

---

# Current Program Status

## ENGINEERINGALLY CONDITIONAL

The repository currently treats the canonical Architecture B mission as **conditionally closed**.

This does **not** mean:

> "The USS Enterprise X can be built today."

It means:

> **Within the explicitly declared model assumptions, conservation laws, state transitions, and numerical constraints, the mission architecture can be made internally coherent — but critical hardware and operational assumptions remain unvalidated at the required scale.**

The largest remaining risks are concentrated around industrial-scale infrastructure rather than the basic bookkeeping:

- multi-megawatt surface nuclear power;
- autonomous Mars excavation;
- high-throughput SOEC hydrogen production;
- industrial-scale hydrogen liquefaction;
- long-duration cryogenic zero-boiloff storage;
- large deployable thermal systems;
- frontier propulsion;
- autonomous maintenance over multi-year campaigns;
- correlated degradation and common-cause failure.

The project therefore distinguishes:

```text
PHYSICS
   ↓
MATHEMATICAL CLOSURE
   ↓
ENGINEERING CLOSURE
   ↓
HARDWARE DEMONSTRATION
   ↓
FLIGHT VALIDATION
```

The repository currently lives somewhere before the final two stages.

---

# Repository Structure

The numbered engineering records form the project's evolving audit trail.

### Foundational Architecture

| Document | Purpose |
|---|---|
| `01-vision.md` | Program mission and success criteria |
| `02-design-philosophy.md` | First-principles design rules |
| `03-propulsion.md` | Propulsion architecture |
| `04-power-and-thermal.md` | Power and thermal systems |
| `05-hull-structure.md` | Structure and pressure architecture |
| `06-habitation.md` | Crew habitation and survivability |
| `07-ai-autonomy.md` | AI and autonomous operations |
| `08-crew-interface.md` | Crew interface architecture |
| `09-defensive-systems.md` | Defensive and protective systems |
| `10-manufacturing.md` | Manufacturing architecture |
| `11-mission-profile.md` | Mission concept |
| `12-economics.md` | Program economics |
| `13-risk.md` | Risk architecture |
| `14-roadmap.md` | Development roadmap |
| `15-design-language.md` | Resulting physical design language |

### Quantitative Engineering

Documents `16–33` progressively introduce:

- quantitative audits;
- system budgets;
- propulsion trades;
- thermal models;
- structural load paths;
- artificial gravity;
- radiation;
- failure analysis;
- ShipOS;
- manufacturing;
- architecture convergence.

### Mission Closure

Documents `40–70` represent the transition from conceptual spacecraft study to integrated mission engineering:

- defect registers;
- verification reports;
- system reference models;
- digital twin development;
- trajectory closure;
- architecture trades;
- power-state modeling;
- astrodynamics;
- Monte Carlo analysis;
- crew survivability;
- Mars ISRU;
- propellant logistics;
- precursor architecture;
- adversarial remediation;
- mission-integrity closure.

### Computational Model

`engineering/calculations/` contains the executable quantitative layer, including:

- mission digital twin;
- Monte Carlo analysis;
- Mars ISRU model;
- mass budget;
- power budget;
- radiator sizing;
- shielding estimates;
- rocket equation calculations;
- trajectory calculations;
- system consistency tests;
- machine-readable JSON baselines.

---

# How to Read the Repository

If you want the shortest path through the project:

```text
README.md
   ↓
68-system-reference-model-v5.md
   ↓
66-mission-architecture-trade-v2.md
   ↓
67-mission-closure-review-v2.md
   ↓
69-phase8-integrity-remediation-v1.md
   ↓
70-phase8.2-propellant-payload-monte-carlo-integrity-closure-v1.md
   ↓
engineering/calculations/
```

For the historical evolution of the reasoning, read the numbered documents sequentially.

For the current engineering state, prioritize the latest reference model, remediation records, executable calculations, generated JSON artifacts, and tests over early conceptual documents.

---

# Development Philosophy

Project Occam-7 follows several non-negotiable principles.

### Mission before geometry

The mission defines the vehicle.

### Physics before inheritance

A familiar science-fiction feature has no authority over physical constraints.

### Mass is a budget

Every kilogram must have a reason.

### Energy creates thermal obligations

Every significant power flow eventually becomes a heat-rejection problem.

### Resources must have provenance

No propellant, inventory, power source, or infrastructure may appear without a physical source.

### Dependencies must be explicit

If subsystem B depends on subsystem A, B cannot silently assume A succeeded.

### Failure is evidence

A failed test is a discovery about the architecture.

### Margin is not decoration

A zero-margin solution is not equivalent to a robust solution.

### Models must be attackable

Every important claim should have a way to falsify it.

### Reality outranks aesthetics

The Enterprise silhouette is allowed to change.

The physics is not.

---

# What "X" Means

**X is intentionally unresolved.**

It does not mean:

- Enterprise 10;
- Enterprise Extreme;
- a fixed production model;
- a claim of technological readiness.

It means the architecture is permitted to change as evidence accumulates.

The project is therefore not attempting to discover the one true Enterprise.

It is attempting to discover **which Enterprise survives the constraints.**

---

# The Deeper Question

The visible question is:

> **Can we build a real Enterprise?**

The deeper question is:

> **What happens when an engineering system is designed so that every assumption must eventually become either a constraint, an equation, a test, a margin, a gate, or an explicit uncertainty?**

Project Occam-7 is an experiment in answering that question.

The spacecraft is the artifact.

The methodology is the subject.

---

## Current Decision

**Canonical architecture:** Architecture B — Precursor Autonomous Robotic ISRU Depot

**Current program state:** **ENGINEERINGALLY CONDITIONAL**

**Primary remaining challenge:** Demonstrating that the frontier industrial systems required by the model can operate reliably at the required scale and duration.

**Next engineering frontier:**

> Move from **mission closure** toward **technology closure** by replacing assumed frontier capabilities with experimentally validated performance envelopes.

---

## License / Status

This repository is a speculative engineering research and design exercise.

It combines:

- real physics;
- engineering approximations;
- computational models;
- explicit assumptions;
- fictional mission architecture;
- speculative technologies;
- adversarial analysis.

It should not be interpreted as a flight-qualified spacecraft design, an operational mission plan, or evidence that the represented technologies currently exist at the required scale.

**Physics has veto power.**
