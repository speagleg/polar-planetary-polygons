"""Session 23: 2D integer-lattice (p, q) scan to find any single-ingredient term
that stabilizes V_*=0 Minkowski.

Question: is there ANY (p, q, sign) combination of a new term
    V_new = sign * C * alpha^p * gamma^q
that admits a stable V_*=0 critical point for SOME positive C in a
reasonable amplitude range? If yes, report (p, q, sign, C).

This is an exhaustive integer-lattice scan over (p, q) ∈ [-10, 6] x [-14, 4]
with sign ∈ {+1, -1} and C across 20 orders of magnitude. Total: 17*19*2*20 = 12920 combos.
"""

import numpy as np

A_R = 1.764e-3
A_F = 1.654e-2
A_C_fib = 7.139e-2
A_L = 1.764e-3
K = 16 * np.pi**2 / 7
B_base = 0.089 / K**2   # use Session 22 first-principles value


def residuals(x, p, q, C):
    """V + new term with scaling (p,q) and coefficient C."""
    a, g, L = x
    g2, g4, g6, g8 = g**2, g**4, g**6, g**8
    V = (A_R/(a*g4) + A_F*a/g6 + A_C_fib/(a**6*g4)
         - B_base/(a**2*g8) + L*A_L/(a*g2)
         + C * a**p * g**q)
    dV_da = (A_R*(-1)/(a**2*g4) + A_F/g6 + A_C_fib*(-6)/(a**7*g4)
             + B_base*2/(a**3*g8) + L*A_L*(-1)/(a**2*g2)
             + C * p * a**(p-1) * g**q)
    dV_dg = (A_R*(-4)/(a*g**5) + A_F*(-6)*a/g**7 + A_C_fib*(-4)/(a**6*g**5)
             + B_base*8/(a**2*g**9) + L*A_L*(-2)/(a*g**3)
             + C * q * a**p * g**(q-1))
    return np.array([V, dV_da, dV_dg])


def jacobian(x, p, q, C, eps=1e-7):
    J = np.zeros((3, 3))
    f0 = residuals(x, p, q, C)
    for i in range(3):
        xp = x.copy()
        h = max(abs(xp[i])*eps, eps)
        xp[i] += h
        J[:, i] = (residuals(xp, p, q, C) - f0)/h
    return J


def newton(x0, p, q, C, max_iter=300, tol=1e-9):
    x = np.array(x0, dtype=float)
    for it in range(max_iter):
        f = residuals(x, p, q, C)
        if np.max(np.abs(f)) < tol:
            return x, True
        J = jacobian(x, p, q, C)
        try:
            dx = np.linalg.solve(J, -f)
        except np.linalg.LinAlgError:
            return x, False
        step = 1.0
        f_norm0 = np.max(np.abs(f))
        for _ in range(20):
            x_new = x + step*dx
            if 1e-3 < x_new[0] < 10.0 and 1e-3 < x_new[1] < 5.0:
                f_new = residuals(x_new, p, q, C)
                if np.max(np.abs(f_new)) < f_norm0*1.5:
                    x = x_new
                    break
            step *= 0.5
        else:
            return x, False
    return x, False


def hessian_log(x, p_new, q_new, C):
    a, g, L = x
    terms = [
        (A_R, -1, -4),
        (A_F, +1, -6),
        (A_C_fib, -6, -4),
        (-B_base, -2, -8),
        (L*A_L, -1, -2),
        (C, p_new, q_new),
    ]
    H = np.zeros((2, 2))
    for c, p, q in terms:
        vi = c*(a**p)*(g**q)
        H[0, 0] += p*p*vi
        H[0, 1] += p*q*vi
        H[1, 1] += q*q*vi
    H[1, 0] = H[0, 1]
    return H


G_kin = np.array([[0.75, 0.5], [0.5, 2.0]])
Ginv = np.linalg.inv(G_kin)


def masses(H):
    return np.sort(np.linalg.eigvals(Ginv @ H).real)


# Exclude scalings parallel to existing terms
existing = [(-1, -4), (+1, -6), (-6, -4), (-2, -8), (-1, -2)]


def is_parallel(p, q):
    for pe, qe in existing:
        if p*qe - pe*q == 0:
            return True
    return False


stable_solutions = []

p_range = range(-8, 6)   # integer p
q_range = range(-12, 3)  # integer q

for p in p_range:
    for q in q_range:
        if (p, q) == (0, 0):
            continue
        if is_parallel(p, q):
            continue
        for sign in [+1, -1]:
            for log_C in np.linspace(-8, 4, 25):
                C_val = sign * 10**log_C
                # Try multiple seeds
                seeds = [[0.798, 0.165, -5770], [0.7, 0.15, -4000],
                         [1.0, 0.2, -1000], [0.5, 0.1, -100]]
                for s in seeds:
                    x, ok = newton(s, p, q, C_val, max_iter=300)
                    if not ok:
                        continue
                    if not (0.05 < x[0] < 5.0 and 0.03 < x[1] < 2.0):
                        continue
                    H = hessian_log(x, p, q, C_val)
                    m2 = masses(H)
                    if m2[0] > 0 and m2[1] > 0:
                        stable_solutions.append((p, q, C_val, x.copy(), m2))
                        break  # found stable, no need for more seeds

if stable_solutions:
    print(f"FOUND {len(stable_solutions)} stable critical points across (p,q,C) space:\n")
    # Dedupe and report best
    print(f"{'(p, q)':>10s} | {'sign':>4s} | {'log₁₀|C|':>9s} | "
          f"{'α_*':>7s} {'γ_*':>7s} | {'m²_light':>11s} {'m²_heavy':>11s}")
    print("-" * 90)
    for p, q, C, x, m2 in stable_solutions[:50]:
        sign_str = "+" if C > 0 else "−"
        print(f"({p:+3d},{q:+3d}) | {sign_str:>4s} | {np.log10(abs(C)):>9.3f} | "
              f"{x[0]:>7.4f} {x[1]:>7.4f} | {m2[0]:+11.3e} {m2[1]:+11.3e}")

    # Group by (p, q) to see which scaling vectors admit stable solutions
    from collections import defaultdict
    groups = defaultdict(list)
    for p, q, C, x, m2 in stable_solutions:
        groups[(p, q)].append((C, x, m2))
    print(f"\n\nStable (p, q) directions found: {len(groups)}")
    for (p, q), entries in sorted(groups.items()):
        C_min = min(e[0] for e in entries)
        C_max = max(e[0] for e in entries)
        print(f"  (p,q) = ({p:+3d},{q:+3d}): {len(entries)} solutions, C ∈ [{C_min:+.2e}, {C_max:+.2e}]")
else:
    print("NO STABLE CRITICAL POINTS found across the full (p, q, sign, C) scan.")
    print("Search space: p ∈ [-8, 5], q ∈ [-12, 2], sign ∈ {±1}, log₁₀|C| ∈ [-8, 4].")
    print("Excluding scalings parallel to existing terms.")
