# 31 — Ship Operating System (ShipOS) Architecture v1

**Document ID:** `31-ship-operating-system.md`
**System Architecture:** Deterministic Distributed Real-Time Operating System (DDRTOS)
**Primary Directive:** Bounded Edge Autonomy & Fail-Safe Graceful Degradation
**Compute Hardware Topology:** 4x Quadrant Triple-Modular Redundant (TMR) Rad-Hard Optical Processing Cores

---

## 1. Domain-Isolated Functional Architecture

To prevent single-point software failures and catastrophic AI halluncinations from jeopardizing vehicle survival, ShipOS partitions autonomy into six strictly air-gapped domain tiers:

```
+---------------------------------------------------------------------------------------------------+
| TIER 1: SAFETY-CRITICAL CONTROL  (HARD REAL-TIME, Deterministic, Zero-AI, <1 ms, Hard Override)   |
+---------------------------------------------------------------------------------------------------+
                                                  | (Read-Only State Vector)
                                                  v
+---------------------------------------------------------------------------------------------------+
| TIER 2: MISSION CONTROL & GNC    (SOFT REAL-TIME, Constrained Kalman/Opt, <50 ms, Earth-Independent)|
+---------------------------------------------------------------------------------------------------+
                                                  | (State Vector & Telemetry)
                                                  v
+---------------------------------------------------------------------------------------------------+
| TIER 3: MAINTENANCE AUTOMATION   (Predictive ML, Robotic RMS Control, Fault Tree Diagnostics)     |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
| TIER 4: CREW ASSISTANCE & INTERFACE (Contextual Natural Language, HUD Synthesis, Medical Mon)     |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
| TIER 5: MANUFACTURING AUTOMATION (3D Print Slicing, CNC Pathing, Inspection Quality Verification)  |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
| TIER 6: SCIENTIFIC AUTONOMY     (Sample Prioritization, Spectral Classification, Probe Target ML) |
+---------------------------------------------------------------------------------------------------+
```

### Tier 1 — Safety-Critical Control (Level 0 Autonomy)
* **Scope:** Reactor rod actuation, pyrotechnic valve isolation, pressure bulkhead seals, attitude rate damping, flight bus power switching.
* **Logic Engine:** Deterministic state-machines compiled in verified Rust/Ada. Zero probabilistic AI or neural models permitted. Execution clock: $1.0\text{ kHz}$ ($1.0\text{ ms}$ fixed frame rate).
* **Authority:** Non-overridable by crew or upper AI layers during emergency containment states.

### Tier 2 — Mission Control & Guidance Navigation Control (GNC)
* **Scope:** Trajectory optimization, orbital entry calculation, thruster gating, state estimation via optical star trackers and LiDAR.
* **Logic Engine:** Extended Kalman Filters (EKF) and convex optimization algorithms operating without Earth ground telemetry.

### Tier 3 — Maintenance Automation
* **Scope:** Structural strain-gauge monitoring, predictive vibration analysis, automated RMS robotic drone dispatch, cassette swapping.

### Tier 4 — Crew Assistance & Decision Support
* **Scope:** Human-vehicle interfaces, voice/HUD diagnostic telemetry, medical monitoring, crew schedule balancing.

### Tier 5 — Manufacturing & Repair Automation
* **Scope:** Automated G-code generation for 3D metal printing, ultrasonic weld quality verification, component fabrication.

### Tier 6 — Scientific Autonomy
* **Scope:** Autonomous probe sensor targeting, spectral anomaly filtering, exobiology sample processing.

---

## 2. Authority Boundaries & Unsafe Command Interlocking

```
[CREW COMMAND: "Disable Reactor Coolant Valve 3"]
                     |
                     v
   [TIER 1 SAFETY INTERLOCK CHECK]
   - Is Reactor Operating Power > 5%? YES
   - Will Loop Temperature exceed 950 K? YES
   - Is Alternate Coolant Path Active? NO
                     |
                     v
   [COMMAND REJECTED: Safety Interlock Violation]
   - Override Code Required: Commander + Chief Engineer Dual Key
```

1. **Unsafe Command Interlocking:** If a human operator issues a command that violates Tier 1 physical safety boundaries (e.g. dumping life-support pressure or opening main propellant valves without pre-chill), ShipOS rejects the command, logs the incident, and displays the physical safety equation violation on the flight deck HUD.
2. **Dual-Key Override Protocol:** Overriding Tier 1 safety interlocks requires simultaneous physical hardware key turn by the Commanding Officer and Chief Engineer.

---

## 3. Five-State Graceful Degradation Logic

| Failure Scenario | ShipOS Operating Degraded Mode | System Action & Response |
|---|---|---|
| **Earth Communication Unavailable (Deep-Space Latency / Blackout)** | **Autonomous Autonomous Flight Mode (AAFM)** | Local GNC executes planned burn profiles autonomously using dark-sky optical navigation. Telemetry stored locally. |
| **Network Partition / Fiber Bus Fracture** | **Quadrant Autonomous Isolation Mode** | TMR compute cores split into local quadrant nodes. Forward Core controls habitat; Aft Core controls reactor/propulsion. |
| **Sensor Disagreement (2 vs 1 Pressure Gauge Delta)** | **Majority Voting & Sensor Exclusion** | EKF algorithm drops outlier sensor reading; flags sensor for robotic maintenance check; relies on TMR agreement. |
| **Crew Issues Unsafe Structural Command** | **Tier 1 Hard Interlock Override Rejection** | Command blocked; HUD displays stress strain boundary violation; dual-key physical override demanded. |
| **AI Model Confidence Loss ($<70\%$ Neural Certainty)** | **Fallback to Deterministic Heuristic Routine** | Neural maintenance/GNC engine disengages; control reverts to conservative pre-programmed lookup tables. |
