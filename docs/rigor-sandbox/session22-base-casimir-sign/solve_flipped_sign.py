"""Session 22 confirmation: does flipping base Casimir sign (−B_base → +B_base)
eliminate the V_* = 0 Minkowski_4 solution?

If YES, the ρ-tachyon CANNOT be cured by flipping the sign (since no critical point
exists), confirming the agent's analytical claim based on Session 18 §R.17.
"""

import numpy as np

# Polygon-theory coefficients (G_7 = 1)
A_R = 1.764e-3
A_F = 1.654e-2
A_C_fib = 7.139e-2
A_L = 1.764e-3
K = 16 * np.pi**2 / 7
B_base = 0.10 / K**2      # always positive; sign flip is via coefficient below


def residuals(x, base_sign=-1):
    """Returns [V, dV/dα, dV/dγ] for 5-term potential with
    V_base = base_sign · B_base / (α² γ⁸).

    base_sign = -1: Session 18 original (attractive base Casimir)
    base_sign = +1: flipped sign (repulsive)
    """
    a, g, L = x
    g2, g4, g6, g8 = g**2, g**4, g**6, g**8

    V = (
        A_R / (a * g4)
        + A_F * a / g6
        + A_C_fib / (a**6 * g4)
        + base_sign * B_base / (a**2 * g8)
        + L * A_L / (a * g2)
    )
    dV_da = (
        A_R * (-1) / (a**2 * g4)
        + A_F * (+1) / g6
        + A_C_fib * (-6) / (a**7 * g4)
        + base_sign * B_base * (-2) / (a**3 * g8)
        + L * A_L * (-1) / (a**2 * g2)
    )
    dV_dg = (
        A_R * (-4) / (a * g**5)
        + A_F * (-6) * a / g**7
        + A_C_fib * (-4) / (a**6 * g**5)
        + base_sign * B_base * (-8) / (a**2 * g**9)
        + L * A_L * (-2) / (a * g**3)
    )
    return np.array([V, dV_da, dV_dg])


def jacobian(x, base_sign, eps=1e-7):
    J = np.zeros((3, 3))
    f0 = residuals(x, base_sign)
    for i in range(3):
        xp = x.copy()
        h = max(abs(xp[i]) * eps, eps)
        xp[i] += h
        J[:, i] = (residuals(xp, base_sign) - f0) / h
    return J


def newton(x0, base_sign, max_iter=500, tol=1e-9):
    x = np.array(x0, dtype=float)
    for it in range(max_iter):
        f = residuals(x, base_sign)
        if np.max(np.abs(f)) < tol:
            return x, it, True
        J = jacobian(x, base_sign)
        try:
            dx = np.linalg.solve(J, -f)
        except np.linalg.LinAlgError:
            return x, it, False
        step = 1.0
        f_norm0 = np.max(np.abs(f))
        for _ in range(30):
            x_new = x + step * dx
            if x_new[0] > 1e-4 and x_new[0] < 1e3 and x_new[1] > 1e-4 and x_new[1] < 1e3:
                f_new = residuals(x_new, base_sign)
                if np.max(np.abs(f_new)) < f_norm0 * 1.5:
                    x = x_new
                    break
            step *= 0.5
        else:
            return x, it, False
    return x, max_iter, False


print("=" * 80)
print("Session 22: does flipping base Casimir sign eliminate V_*=0 Minkowski?")
print("=" * 80)
print()

seeds = [
    [0.798, 0.165, -5770.0],   # Session 18 benchmark
    [0.5, 0.3, -500],
    [1.5, 0.3, -1000],
    [0.8, 0.1, -10000],
    [2.0, 0.5, -100],
    [0.3, 0.1, -30000],
    [1.0, 0.2, -2000],
    [0.4, 0.15, -500],
    [0.6, 0.08, -50000],
    [1.2, 0.4, -200],
]

for base_sign, label in [(-1, "ORIGINAL (-B_base)  [Session 18 sign]"),
                          (+1, "FLIPPED  (+B_base)  [hypothesized uplift]")]:
    print(f"\n{label}")
    print("-" * 80)
    solutions = []
    for s in seeds:
        x, it, ok = newton(s, base_sign, max_iter=500)
        if not ok:
            continue
        a, g, L = x
        if 0.05 < a < 10.0 and 0.03 < g < 5.0:
            # Check V
            V = residuals(x, base_sign)[0]
            # Dedupe by (a, g) proximity
            is_dup = False
            for prev in solutions:
                if abs(prev[0] - a) < 0.01 and abs(prev[1] - g) < 0.01:
                    is_dup = True
                    break
            if not is_dup:
                solutions.append((a, g, L, V))

    if solutions:
        print(f"Found {len(solutions)} distinct physical-window critical points:")
        for a, g, L, V in solutions:
            print(f"  (α, γ, Λ_7) = ({a:.4f}, {g:.4f}, {L:.3e})   V = {V:+.3e}")
    else:
        print(f"NO critical point converged in physical window [0.05, 10] x [0.03, 5]")

print()
print("=" * 80)
print("CONCLUSION:")
print("  If flipped sign yields no critical points, the ρ-tachyon cannot be")
print("  cured by flipping the sign — the V_*=0 vacuum simply disappears.")
print("=" * 80)
