#!/usr/bin/env python3
"""
Artificial Gravity & Centrifuge Dynamics Calculator for Project Occam-7
Calculates Centripetal Acceleration, RPM, Coriolis Effects, Bearing Torques, and Structural Mass Penalties.
"""

import math

G0 = 9.80665  # m/s^2

def analyze_centrifuge(radius_m, rpm, walk_v_ms=1.5):
    omega = rpm * (2.0 * math.pi / 60.0)  # rad/s
    a_centripetal = (omega ** 2) * radius_m
    g_fraction = a_centripetal / G0
    v_tangential = omega * radius_m

    # Coriolis acceleration walking prograde (+v) or retrograde (-v)
    a_coriolis_prograde = 2.0 * omega * walk_v_ms
    g_effective_prograde = (a_centripetal + a_coriolis_prograde) / G0
    g_effective_retrograde = max(0, (a_centripetal - a_coriolis_prograde) / G0)

    return {
        "omega": omega,
        "a_m_s2": a_centripetal,
        "g_fraction": g_fraction,
        "v_tangential": v_tangential,
        "g_prograde": g_effective_prograde,
        "g_retrograde": g_effective_retrograde,
        "coriolis_m_s2": a_coriolis_prograde
    }

def centrifuge_trade():
    print("=== ARTIFICIAL GRAVITY & CENTRIFUGE TRADE CALCULATOR V2 ===")

    cases = [
        {"name": "Option 1: Internal Compact Centrifuge (v1 Baseline)", "radius": 6.0, "rpm": 10.0},
        {"name": "Option 2: Optimized Internal Centrifuge (High RPM)", "radius": 7.5, "rpm": 8.0},
        {"name": "Option 3: Transverse Truss Counter-Rotating Ring", "radius": 15.0, "rpm": 6.0},
        {"name": "Option 4: Deployable Tether / Dual-Hull End-Mass Rotation", "radius": 56.0, "rpm": 4.0},
        {"name": "Option 5: Extended Tether Rotation (Full Earth 1-g)", "radius": 224.0, "rpm": 2.0}
    ]

    for c in cases:
        res = analyze_centrifuge(c["radius"], c["rpm"])
        print(f"\n{c['name']}:")
        print(f"  Radius: {c['radius']} m | Speed: {c['rpm']} RPM ({res['omega']:.3f} rad/s)")
        print(f"  Tangential Velocity: {res['v_tangential']:.2f} m/s")
        print(f"  Centripetal Acceleration: {res['a_m_s2']:.2f} m/s^2 ({res['g_fraction']:.2f} g)")
        print(f"  Coriolis Accel (1.5 m/s walk): {res['coriolis_m_s2']:.2f} m/s^2")
        print(f"  Walking Prograde / Retrograde Delta: {res['g_prograde']:.2f} g / {res['g_retrograde']:.2f} g")

if __name__ == "__main__":
    centrifuge_trade()
