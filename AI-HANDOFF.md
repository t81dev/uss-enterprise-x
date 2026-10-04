# USS Enterprise X — AI Continuation & Design Plan

**Repository:** `uss-enterprise-x`  
**Internal codename:** `Project Occam-7`  
**Purpose:** hand this project to another AI without losing design intent, engineering discipline, or accumulated decisions.

## 1. Mission of the next AI

Continue the project as a **first-principles starship systems-engineering exercise**.

The objective is not to defend the original Star Trek Enterprise silhouette and not to invent arbitrary science-fiction technology. The objective is to determine what an actual long-duration, reusable, self-sufficient deep-space vehicle would look like if the Enterprise mission were treated as a real engineering program.

The project should progressively move from:

`mission -> requirements -> physics -> budgets -> architecture -> subsystems -> operations -> manufacturing -> economics -> visual form`

Do not reverse that order merely because a visually attractive configuration is easier to imagine.

---

## 2. Canonical project stance

Treat the following as the project's governing design rules:

1. **Mission before geometry.** The ship's shape is an output of requirements.
2. **First principles before inheritance.** Star Trek conventions are hypotheses, not requirements.
3. **Mass is a budget.** Every major mass allocation must have a function and a reason.
4. **Power creates heat.** Every serious power source must have a thermal-rejection solution.
5. **Reusability is mandatory.** The baseline vehicle is intended to return, be inspected, repaired, and fly again.
6. **Autonomy is structural.** Deep-space latency requires local navigation, fault management, and operations competence.
7. **Manufacturing is part of the architecture.** A system that cannot be fabricated, inspected, serviced, or replaced is incomplete.
8. **Human survivability outranks aesthetics.** Crew survival, radiation protection, redundancy, and maintainability dominate visual nostalgia.
9. **Physics has veto power.** Unknown physics may be explored, but it may not silently become an engineering assumption.
10. **X is a variable.** The configuration is expected to change when calculations or evidence say it should.

---

## 3. Reality-classification system

Every important technology or claim must be assigned one of four labels:

### PLAUSIBLE
Known physics and an identifiable engineering development path exist.

### FRONTIER
The physics is broadly credible, but the required performance, materials, manufacturing, or scale is beyond current capability.

### SPECULATIVE
A major unresolved scientific or engineering breakthrough is required.

### FICTIONAL
Retained for narrative/design-language reasons rather than engineering credibility.

A concept may move between categories as evidence improves. The AI should record the reason for each classification change.

**Rule:** never use a speculative component to close a supposedly realistic budget without clearly showing the dependency.

---

## 4. What the repository already contains

The existing documents establish the project framework:

| File | Role |
|---|---|
| `01-vision.md` | Program purpose and reset |
| `02-design-philosophy.md` | Design rules and aesthetic consequences |
| `03-propulsion.md` | Propulsion pathways and FTL branch |
| `04-power-and-thermal.md` | Power generation, distribution, storage, and heat rejection |
| `05-hull-structure.md` | Pressure vessel, primary structure, radiation, debris |
| `06-habitation.md` | Life support, gravity, crew environment |
| `07-ai-autonomy.md` | Shipboard autonomy and fault management |
| `08-crew-interface.md` | Control architecture and neural-interface concept |
| `09-defensive-systems.md` | Passive and active protection concepts |
| `10-manufacturing.md` | Industrialization and servicing |
| `11-mission-profile.md` | Mission progression |
| `12-economics.md` | Program economics and scale |
| `13-risk.md` | Major risks and failure modes |
| `14-roadmap.md` | Development sequence |
| `15-design-language.md` | Visual and spatial consequences |
| `concept/00-internal-design-memo.md` | Fictionalized Musk-inspired design-reset voice |
| `concept/01-original-premise.md` | Original Enterprise reinterpretation |
| `design/README.md` | Visual/design workstream entry point |
| `engineering/README.md` | Quantitative engineering workstream entry point |
| `operations/README.md` | Operations workstream entry point |

The next AI should **read all of these before changing the architecture**.

---

## 5. First assignment: perform an architecture audit

Before adding major concepts, create:

`engineering/architecture-audit.md`

The audit should answer:

- What requirements are explicit?
- What requirements are only implied?
- Which numbers are actual calculations versus placeholders?
- Which claims depend on unresolved physics?
- Which subsystems currently have no mass budget?
- Which subsystems have no power budget?
- Which subsystems have no thermal path?
- Which failure modes have no recovery strategy?
- Which design decisions are reversible?
- Which design decisions would lock the architecture too early?

End the audit with a **Top 10 Unknowns** table ranked by how strongly each unknown can change the vehicle architecture.

Do not redesign the ship during this step.

---

## 6. Second assignment: build the quantitative backbone

The next AI should then create the engineering documents below.

### `engineering/requirements.md`
Define measurable mission requirements.

Minimum categories:

- crew size and maximum crew duration
- mission duration
- range
- delta-v / acceleration profile
- launch and landing assumptions, if applicable
- radiation environment
- artificial-gravity requirement
- atmospheric requirements, if applicable
- cargo and scientific payload
- autonomy level
- abort criteria
- refurbishment interval
- design life

### `engineering/mass-budget.md`
Build an explicit mass budget by subsystem.

At minimum:

- primary structure
- pressure hull
- radiation shielding
- propulsion
- propellant
- tanks
- power generation
- power conversion/distribution
- thermal system
- avionics/computing
- communications
- life support
- habitat equipment
- crew accommodations
- docking/airlock systems
- landing/flight hardware if retained
- science payload
- defensive systems
- reserve / growth margin

Use ranges when precision is unjustified.

### `engineering/power-budget.md`
Create:

`generation -> conversion -> distribution -> loads -> storage -> emergency loads`

Separate:

- continuous load
- peak load
- transient load
- startup load
- emergency load

### `engineering/thermal-budget.md`
Every high-energy subsystem must have a thermal pathway.

Calculate or bound:

- waste heat
- radiator area
- radiator temperature assumptions
- transient heat storage
- emergency thermal mode
- radiator degradation / damage tolerance

### `engineering/delta-v-and-trajectory.md`
Do not hide propulsion performance inside prose. Define mission phases, acceleration, propellant assumptions, and trajectory classes.

### `engineering/crew-resource-budget.md`
Track:

- water
- oxygen
- nitrogen / buffer gases
- food
- waste
- spare parts
- medical supplies
- clothing / consumables

The AI should close these budgets before claiming the ship is self-sufficient.

---

## 7. Propulsion development logic

Keep propulsion as a **technology ladder**, not a single magic engine.

Recommended sequence:

### Stage A — Near-term chemical
Use chemical propulsion where realistic, especially for launch, landing, and high-thrust maneuvers.

### Stage B — Nuclear thermal / nuclear electric
Evaluate where higher specific impulse or long-duration electric thrust improves the mission.

### Stage C — Fusion
Treat fusion as a major frontier program. Define the physical performance required rather than assuming an unspecified “fusion reactor.”

### Stage D — Advanced plasma / beamed propulsion
Study alternatives that could reduce onboard propellant requirements.

### Stage E — FTL / warp branch
Maintain a separate speculative branch.

The FTL branch must answer:

- What metric or spacetime model is assumed?
- What energy density is required?
- What exotic matter or field condition is required?
- What experimental evidence exists?
- What new failure modes appear?
- What happens to causality, navigation, radiation, and arrival conditions?

Until those questions have credible answers, FTL must remain **architecturally isolated** from the realistic baseline.

---

## 8. Structural architecture investigation

Do not lock the design to either a saucer or a cylinder because of aesthetics.

Generate at least three serious configurations:

1. **Integrated cylinder / lifting-body**
2. **Distributed long-axis habitat with separated propulsion modules**
3. **Hybrid Enterprise configuration** that preserves some recognizable Enterprise geometry without inheriting structurally weak features

For each configuration compare:

- structural efficiency
- bending moments
- radiation protection
- artificial gravity
- thermal management
- engine integration
- maintenance access
- docking
- crew movement
- manufacturing complexity
- launch/assembly requirements

Then select or combine configurations based on the evidence.

---

## 9. Crew interface and neural interface

Treat neural interface technology as a **research branch**, not a prerequisite.

The baseline control system must remain usable without invasive neural technology.

Design hierarchy:

`autonomous flight control -> conventional human controls -> advanced non-invasive interface -> neural interface research`

The question is not “how do we make the bridge look futuristic?”

The question is:

> What is the lowest-latency, lowest-cognitive-load, highest-reliability method for a human to supervise or override a highly autonomous spacecraft?

Also investigate whether a traditional “bridge” is even the right architecture. A distributed operations center may be safer.

---

## 10. Defensive systems

Do not begin with weapons.

Begin with **survival engineering**:

1. avoid collision
2. detect threats
3. absorb or disperse impact
4. isolate damage
5. recover from subsystem failure
6. protect the crew
7. only then examine active defensive systems

Study:

- Whipple / layered impact shielding
- water and consumable placement as radiation/impact mass
- magnetic shielding concepts
- autonomous debris avoidance
- laser-based debris ablation or ranging
- interceptor concepts
- high-energy defensive systems only as a separate speculative branch

Any weapon system must be evaluated first as a mass, power, cooling, storage, and safety problem.

---

## 11. Manufacturing doctrine

The manufacturing workstream should be treated as a design constraint, not an afterthought.

For every major subsystem ask:

- Can it be produced repeatedly?
- Can it be inspected automatically?
- Can it be repaired in the field?
- Can a failed module be swapped without dismantling the ship?
- Can the manufacturing process be automated?
- What special materials are bottlenecks?
- What tolerance stack-up dominates cost?
- What component has the worst supply-chain risk?

Investigate the “best part is no part” principle critically. Removing a part is valuable only when its function is unnecessary; eliminating redundancy, shielding, or service access merely transfers cost into failures.

---

## 12. Economics

Do not accept arbitrary targets such as “under $500M” merely because they sound ambitious.

Instead build three scenarios:

- **minimum viable prototype**
- **operational vehicle**
- **mass-production architecture**

For each, estimate:

- development cost
- prototype count
- test-flight count
- production throughput
- recurring vehicle cost
- launch/assembly infrastructure
- refurbishment cost
- crew operations cost
- major consumables
- expected mission cost

The economic model should identify which assumptions dominate the result.

---

## 13. Operations and autonomy

Create an operational doctrine around the principle:

> The ship must remain competent when Earth is unavailable.

Define autonomy for:

- navigation
- propulsion management
- life-support control
- fault detection
- damage isolation
- maintenance scheduling
- logistics
- medical support
- scientific operations
- communication prioritization
- emergency decision support

Do not give the AI unrestricted authority by default. Define:

- permitted autonomous actions
- human approval thresholds
- hard safety interlocks
- degraded modes
- auditability
- recovery after software faults

---

## 14. Failure-first design review

Before finalizing v2, perform an adversarial review.

Assume:

- one engine fails
- one power source fails
- one radiator panel is lost
- pressure hull is punctured
- primary computer fails
- navigation sensors disagree
- communications are unavailable
- one crew member is incapacitated
- a fire occurs
- a long-duration life-support component degrades
- the vehicle is struck by debris
- resupply is impossible

For each scenario, answer:

`detect -> isolate -> stabilize -> recover -> continue / abort`

Any subsystem that cannot answer those five steps requires redesign or an explicit risk acceptance.

---

## 15. Visual design comes after architecture

Only after the quantitative architecture has stabilized should the AI produce detailed visual configurations.

Create:

`design/configuration-study.md`

with at least three variants.

Each drawing/render should be traceable to engineering requirements. For example:

- thick center section = radiation/pressure volume
- separated habitat = gravity / thermal / mission requirement
- radiator geometry = heat rejection requirement
- engine spacing = structural and maintenance requirement
- docking positions = logistics requirement

The desired aesthetic is **industrial, precise, severe, repairable, and unmistakably purposeful**.

The ship should look like the consequence of its engineering.

---

## 16. AI operating protocol

The next AI should follow this procedure on every major change.

### Step 1 — Read before editing
Read the README and the affected subsystem documents.

### Step 2 — State the changed assumption
Write down what assumption or requirement is being changed.

### Step 3 — Trace dependencies
Identify which budgets, interfaces, and downstream documents are affected.

### Step 4 — Calculate before narrating
Do the simplest useful calculation before writing persuasive prose.

### Step 5 — Mark uncertainty
Every important value should be one of:

- measured / sourced
- derived
- estimated
- assumed
- speculative

### Step 6 — Update the smallest number of files necessary
Avoid creating duplicate explanations.

### Step 7 — Record the decision
Use a lightweight architecture-decision record when a choice changes the system.

### Step 8 — Challenge the decision
Ask what would make the decision wrong.

### Step 9 — Commit coherently
One conceptual change per logical commit where practical.

---

## 17. Architecture decision records

Create a directory:

`engineering/adr/`

Use files such as:

- `ADR-001-vehicle-configuration.md`
- `ADR-002-gravity-strategy.md`
- `ADR-003-propulsion-baseline.md`
- `ADR-004-power-architecture.md`
- `ADR-005-radiation-strategy.md`
- `ADR-006-autonomy-boundaries.md`
- `ADR-007-thermal-architecture.md`
- `ADR-008-manufacturing-strategy.md`

Each ADR should contain:

- Context
- Options considered
- Decision
- Rationale
- Consequences
- Reversal conditions

---

## 18. Research standard

When external evidence is needed, prefer primary or technically authoritative sources:

- peer-reviewed papers
- NASA / ESA / JAXA / national laboratories
- standards organizations
- university technical publications
- original engineering papers
- manufacturer technical data where appropriate

Avoid treating social posts, videos, speculative blogs, or AI-generated claims as evidence.

Every externally derived important number should have a source recorded near the number or in a references file.

When the evidence is weak, say so.

---

## 19. What the next AI must not do

Do **not**:

- silently turn science fiction into fact
- defend a geometry because it resembles the Enterprise
- add technologies merely because they sound advanced
- use magic numbers without explaining their origin
- close mass, power, or thermal budgets by hand-waving
- make the ship invulnerable
- assume infinite energy
- assume infinite propellant
- assume infinite manufacturing throughput
- treat autonomy as magic intelligence
- use “AI” as an excuse not to specify interfaces and failure modes
- make Elon Musk appear to have actually written fictional material
- optimize the bridge before optimizing the spacecraft

---

## 20. Definition of “good progress”

Progress is not the number of Markdown files.

Progress means reducing the number of unresolved assumptions that can materially change the architecture.

The project is progressing when:

- mission requirements are measurable
- mass budget closes within a declared margin
- power budget closes
- thermal budget closes
- crew resources close
- propulsion has explicit performance assumptions
- failure recovery is credible
- manufacturing constraints shape the geometry
- economics expose the dominant cost drivers
- the visual form follows those decisions

---

## 21. Recommended v2 sequence

Execute in this order:

### Phase 0 — Audit
Create `engineering/architecture-audit.md`.

### Phase 1 — Requirements
Create `engineering/requirements.md`.

### Phase 2 — Budgets
Create mass, delta-v, power, thermal, and crew-resource budgets.

### Phase 3 — Configuration trade study
Evaluate at least three vehicle architectures.

### Phase 4 — Select baseline
Create the first formal architecture decision records.

### Phase 5 — Subsystem closure
Bring propulsion, structure, habitat, power, thermal, avionics, and autonomy into one integrated model.

### Phase 6 — Operations
Write nominal, degraded, abort, rescue, and recovery procedures.

### Phase 7 — Manufacturing and economics
Turn the ship into an industrial program rather than a one-off object.

### Phase 8 — Adversarial review
Try to break the architecture.

### Phase 9 — Design synthesis
Only now update the physical silhouette and interior design.

### Phase 10 — v2 release
Update README, create a changelog, summarize what changed from v1, and identify the next three highest-value unknowns.

---

## 22. First prompt for the next AI

Use the following as the continuation prompt:

> You are continuing Project Occam-7 in the `uss-enterprise-x` repository.
>
> Read `README.md`, `AI-HANDOFF.md`, and every existing Markdown document before proposing major changes.
>
> Do not redesign the ship yet.
>
> First create `engineering/architecture-audit.md` and perform a hostile audit of the existing concept. Separate established engineering, frontier technology, speculative technology, and fictional design elements. Identify every unresolved assumption that could materially alter the architecture.
>
> Then create a ranked Top 10 Unknowns list and recommend the minimum set of calculations required to reduce those unknowns.
>
> Do not use aesthetic preference as evidence. Do not close a budget with magic technology. Treat the familiar Enterprise silhouette as optional.
>
> Preserve the project's first-principles philosophy and fictionalized Musk-inspired voice only where explicitly appropriate. Do not present fictional dialogue or memos as authentic statements by Elon Musk.
>
> Your output should improve the engineering model, not merely increase the amount of prose.

---

## 23. Long-term endpoint

The project should eventually produce a coherent **Enterprise Systems Definition Package** containing:

- mission requirements
- system architecture
- mass budget
- propulsion model
- power model
- thermal model
- structural concept
- radiation strategy
- habitat and gravity concept
- autonomy architecture
- crew interface
- defensive/survival architecture
- manufacturing system
- operations doctrine
- cost model
- risk register
- configuration drawings
- technology readiness map
- explicit boundary between real engineering and speculative fiction

The final product should be valuable even to a skeptical engineer who does not care about Star Trek.

That is the test.
