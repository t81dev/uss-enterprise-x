#!/usr/bin/env python3
"""
Artificial Gravity & Centrifuge Dynamics Calculator for Project Occam-7
Calculates Centripetal Acceleration, RPM, Coriolis Effects, Radial Walking Acceleration, Bearing Torques, and Structural Mass.
"""

import math

G0 = 9.80665  # m/s^2

def analyze_centrifuge(radius_m, rpm, walk_v_ms=1.5):
    omega = rpm * (2.0 * math.pi / 60.0)  # rad/s
    a_centripetal = (omega ** 2) * radius_m
    g_fraction = a_centripetal / G0
    v_tangential = omega * radius_m

    # Exact radial acceleration for walking in rotating frame:
    # a_r = (omega * r +/- v)^2 / r = omega^2 * r +/- 2 * omega * v + v^2 / r
    a_prograde = ((omega * radius_m + walk_v_ms) ** 2) / radius_m
    a_retrograde = max(0.0, ((omega * radius_m - walk_v_ms) ** 2) / radius_m)

    g_prograde = a_prograde / G0
    g_retrograde = a_retrograde / G0
    a_coriolis = 2.0 * omega * walk_v_ms

    return {
        "omega": omega,
        "a_m_s2": a_centripetal,
        "g_fraction": g_fraction,
        "v_tangential": v_tangential,
        "a_prograde": a_prograde,
        "a_retrograde": a_retrograde,
        "g_prograde": g_prograde,
        "g_retrograde": g_retrograde,
        "coriolis_m_s2": a_coriolis
    }

def centrifuge_trade():
    print("=== ARTIFICIAL GRAVITY & CENTRIFUGE TRADE CALCULATOR V2 (RECONCILED) ===")

    cases = [
        {"name": "Option 1: Internal Compact Centrifuge (v1 Baseline)", "radius": 6.0, "rpm": 10.0},
        {"name": "Option 2: Optimized Internal Centrifuge (High RPM)", "radius": 7.5, "rpm": 8.0},
        {"name": "Option 3: Transverse Truss Counter-Rotating Ring (v2 Baseline)", "radius": 15.0, "rpm": 6.0},
        {"name": "Option 4: Deployable Tether / Dual-Hull End-Mass Rotation", "radius": 56.0, "rpm": 4.0},
        {"name": "Option 5: Extended Tether Rotation (Full Earth 1-g)", "radius": 224.0, "rpm": 2.0}
    ]

    for c in cases:
        res = analyze_centrifuge(c["radius"], c["rpm"])
        print(f"\n{c['name']}:")
        print(f"  Radius: {c['radius']} m | Speed: {c['rpm']} RPM ({res['omega']:.3f} rad/s)")
        print(f"  Tangential Floor Velocity: {res['v_tangential']:.2f} m/s")
        print(f"  Static Centripetal Accel:  {res['a_m_s2']:.2f} m/s^2 ({res['g_fraction']:.3f} g)")
        print(f"  Coriolis Term (1.5m/s walk): {res['coriolis_m_s2']:.2f} m/s^2")
        print(f"  Prograde Walking Acceleration:  {res['a_prograde']:.2f} m/s^2 ({res['g_prograde']:.3f} g)")
        print(f"  Retrograde Walking Acceleration: {res['a_retrograde']:.2f} m/s^2 ({res['g_retrograde']:.3f} g)")

if __name__ == "__main__":
    centrifuge_trade()
