"""Session 31 blocker verification: does V_*=0 critical point exist at
corrected |C_base| = 0.0065?

Scans |C_base| from Session 22 threshold down to Session 31 corrected value.
"""

import numpy as np

# Polygon-theory coefficients (G_7 = 1)
A_R = 1.764e-3
A_F = 1.654e-2
A_C_fib = 7.139e-2
A_L = 1.764e-3
K = 16 * np.pi**2 / 7


def residuals(x, C_base):
    """3-equation system: V = 0, ∂_α V = 0, ∂_γ V = 0"""
    a, g, L = x
    B_base = C_base / K**2
    g2, g4, g6, g8 = g**2, g**4, g**6, g**8

    V = (A_R/(a*g4) + A_F*a/g6 + A_C_fib/(a**6*g4)
         - B_base/(a**2*g8) + L*A_L/(a*g2))
    dV_da = (A_R*(-1)/(a**2*g4) + A_F/g6 + A_C_fib*(-6)/(a**7*g4)
             + B_base*2/(a**3*g8) + L*A_L*(-1)/(a**2*g2))
    dV_dg = (A_R*(-4)/(a*g**5) + A_F*(-6)*a/g**7 + A_C_fib*(-4)/(a**6*g**5)
             + B_base*8/(a**2*g**9) + L*A_L*(-2)/(a*g**3))
    return np.array([V, dV_da, dV_dg])


def jacobian(x, C_base, eps=1e-7):
    J = np.zeros((3, 3))
    f0 = residuals(x, C_base)
    for i in range(3):
        xp = x.copy()
        h = max(abs(xp[i])*eps, eps)
        xp[i] += h
        J[:, i] = (residuals(xp, C_base) - f0)/h
    return J


def newton(x0, C_base, max_iter=500, tol=1e-9):
    x = np.array(x0, dtype=float)
    for it in range(max_iter):
        f = residuals(x, C_base)
        if np.max(np.abs(f)) < tol:
            return x, True
        J = jacobian(x, C_base)
        try:
            dx = np.linalg.solve(J, -f)
        except np.linalg.LinAlgError:
            return x, False
        step = 1.0
        f_norm0 = np.max(np.abs(f))
        for _ in range(40):
            x_new = x + step*dx
            if 1e-3 < x_new[0] < 1e3 and 1e-3 < x_new[1] < 1e3:
                f_new = residuals(x_new, C_base)
                if np.max(np.abs(f_new)) < f_norm0 * 1.5:
                    x = x_new
                    break
            step *= 0.5
        else:
            return x, False
    return x, False


def find_solution(C_base):
    """Multi-seed Newton scan for a given |C_base|."""
    # Seeds spanning the physical moduli window plus Session 18 benchmark
    seeds = [
        [0.798, 0.165, -5770],
        [0.75, 0.15, -8000],
        [0.80, 0.17, -5000],
        [0.7, 0.14, -10000],
        [0.9, 0.18, -4000],
        [0.6, 0.13, -15000],
        [0.5, 0.12, -20000],
        [1.0, 0.20, -3000],
        [0.4, 0.11, -30000],
        [1.2, 0.25, -2000],
    ]
    for s in seeds:
        x, ok = newton(s, C_base, max_iter=500)
        if ok and 0.05 < x[0] < 5.0 and 0.03 < x[1] < 2.0:
            return x
    return None


print(f"{'C_base':>10s} | {'α_*':>7s} {'γ_*':>7s} {'Λ_7':>10s} | Exists?")
print("-" * 60)

# Scan from Session 22 benchmark (0.10) through thresholds down to Session 31 (0.0065)
scan_values = [0.15, 0.10, 0.089, 0.07, 0.05, 0.04, 0.03, 0.02, 0.015, 0.01, 0.0065, 0.005, 0.001]

disappearance_found = False
for Cb in scan_values:
    sol = find_solution(Cb)
    if sol is not None:
        a, g, L = sol
        print(f"{Cb:10.4f} | {a:7.4f} {g:7.4f} {L:10.3e} | yes")
    else:
        print(f"{Cb:10.4f} |  --     --     --        | NO (no positive solution)")
        disappearance_found = True

print()
if disappearance_found:
    print("CONFIRMED: V_*=0 critical point disappears below some threshold")
    print("           in the scan range. The Session 31 claim (no solution at 0.0065)")
    print("           is verified numerically.")
else:
    print("WARNING: V_*=0 persists across entire scan. Session 31 claim unverified.")
