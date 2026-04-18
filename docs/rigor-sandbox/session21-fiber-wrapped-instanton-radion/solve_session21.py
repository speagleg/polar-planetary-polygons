"""Session 21: fiber-wrapped Euclidean instanton contribution to the radion potential.

A Euclidean soliton wrapping the S^1 fiber has action S = 2*pi*alpha*mu where mu
is the worldline tension (in G_7=1 units). Leading single-wrap contribution:

    V_fib(alpha, gamma) = A_inst * exp(-2*pi*alpha*mu) / (alpha^2 * gamma^4)

where the 1/(alpha^2 gamma^4) = 1/V_3^2 comes from Weyl rescaling to 4D Einstein frame
(V_3 = K*alpha*gamma^2, so 1/V_3^2 = 1/(K^2 alpha^2 gamma^4), with 1/K^2 absorbed
into A_inst).

Scaling vector at critical point (for gradient-based Hessian analysis):
    alpha d/d(log alpha) log|V_fib| = -2*pi*alpha*mu - 2 + 1   (the +1 comes if A_inst
                                    carries a prefactor alpha^1 from moduli-space vol)
For simplicity, treat A_inst as constant (no alpha-prefactor beyond 1/V_3^2).
Effective scaling in alpha at critical point: -2 - 2*pi*alpha_*·mu  (LARGE and negative)
Effective scaling in gamma: -4

Cross-product with Lambda_7 scaling (-1,-2):
    (-2 - 2*pi*alpha*mu)(-2) - (-1)(-4) = 4 + 4*pi*alpha*mu - 4 = 4*pi*alpha*mu
Non-zero for mu > 0. Genuinely non-parallel.

This script solves the 3-equation system {V=0, dV/da=0, dV/dg=0} with the 6-term
potential (Session 18 + fiber-wrapped instanton) and scans over (A_inst, mu) to find
stability regions.
"""

import numpy as np

# Polygon-theory coefficients (G_7 = 1)
A_R = 1.764e-3
A_F = 1.654e-2
A_C_fib = 7.139e-2
A_L = 1.764e-3
K = 16 * np.pi**2 / 7
B_base = 0.10 / K**2

# Polygon-derived candidate tensions (dimensionless, G_7 = 1)
b7 = 4.297838
S_BO_7 = 18.274
k7 = 2 * b7  # = 8.5957

mu_candidates = {
    "b(7)/2π":      b7 / (2 * np.pi),            # 0.684
    "S_BO(7)/2π":   S_BO_7 / (2 * np.pi),        # 2.908
    "k(7)/2π²":     k7 / (2 * np.pi**2),         # 0.435
    "1/2π":         1.0 / (2 * np.pi),           # 0.159 (minimal)
    "1":            1.0,                          # natural unit
}

print("Candidate fiber tensions mu (G_7=1 units):")
for name, mu in mu_candidates.items():
    print(f"  mu = {name:15s} = {mu:.4f}")
print()


def potential(alpha, gamma, Lambda_7, A_inst, mu):
    a, g = alpha, gamma
    g2, g4, g6, g8 = g**2, g**4, g**6, g**8
    terms = {
        "Ric":  A_R / (a * g4),
        "FR":   A_F * a / g6,
        "fib":  A_C_fib / (a**6 * g4),
        "base": -B_base / (a**2 * g8),
        "Lam":  Lambda_7 * A_L / (a * g2),
        "inst": A_inst * np.exp(-2 * np.pi * a * mu) / (a**2 * g4),
    }
    return terms


def residuals(x, A_inst, mu):
    """{V=0, dV/dalpha=0, dV/dgamma=0}"""
    a, g, L = x
    terms = potential(a, g, L, A_inst, mu)
    V = sum(terms.values())

    # Partial derivatives — analytic where feasible
    g2, g4, g6, g8 = g**2, g**4, g**6, g**8

    # dV/da for each term (all have form c * a^p * g^q * (possibly exp factor)):
    dV_da = (
        A_R * (-1) / (a**2 * g4)
        + A_F * (+1) / g6
        + A_C_fib * (-6) / (a**7 * g4)
        + (-B_base) * (-2) / (a**3 * g8)
        + L * A_L * (-1) / (a**2 * g2)
        + A_inst * np.exp(-2 * np.pi * a * mu) * (-2 - 2 * np.pi * a * mu) / (a**3 * g4)
    )

    dV_dg = (
        A_R * (-4) / (a * g**5)
        + A_F * (-6) * a / g**7
        + A_C_fib * (-4) / (a**6 * g**5)
        + (-B_base) * (-8) / (a**2 * g**9)
        + L * A_L * (-2) / (a * g**3)
        + A_inst * np.exp(-2 * np.pi * a * mu) * (-4) / (a**2 * g**5)
    )

    return np.array([V, dV_da, dV_dg])


def jacobian(x, A_inst, mu, eps=1e-7):
    J = np.zeros((3, 3))
    f0 = residuals(x, A_inst, mu)
    for i in range(3):
        xp = x.copy()
        h = max(abs(xp[i]) * eps, eps)
        xp[i] += h
        J[:, i] = (residuals(xp, A_inst, mu) - f0) / h
    return J


def newton(x0, A_inst, mu, max_iter=500, tol=1e-8):
    x = np.array(x0, dtype=float)
    for it in range(max_iter):
        f = residuals(x, A_inst, mu)
        if np.max(np.abs(f)) < tol:
            return x, it, True
        J = jacobian(x, A_inst, mu)
        try:
            dx = np.linalg.solve(J, -f)
        except np.linalg.LinAlgError:
            return x, it, False
        # Damped step
        step = 1.0
        f_norm0 = np.max(np.abs(f))
        for _ in range(30):
            x_new = x + step * dx
            if x_new[0] > 1e-4 and x_new[0] < 1e3 and x_new[1] > 1e-4 and x_new[1] < 1e3:
                f_new = residuals(x_new, A_inst, mu)
                if np.max(np.abs(f_new)) < f_norm0 * 1.5:
                    x = x_new
                    break
            step *= 0.5
        else:
            return x, it, False
    return x, max_iter, False


def hessian_log(x, A_inst, mu):
    """Hessian w.r.t. (log alpha, log gamma) = second derivatives times alpha, gamma factors."""
    a, g, L = x
    exp_factor = np.exp(-2 * np.pi * a * mu)
    # Compute V and its first and second derivatives, then convert
    # For each term with form V_i = C * a^p * g^q (power-law), contribution to
    # Hessian in (log a, log g) basis is:
    #   H_aa += p^2 * V_i
    #   H_ag += p*q * V_i
    #   H_gg += q^2 * V_i
    # For the exponential instanton term, must work out explicitly.

    H = np.zeros((2, 2))

    power_law = [
        (A_R, -1, -4),
        (A_F, +1, -6),
        (A_C_fib, -6, -4),
        (-B_base, -2, -8),
        (L * A_L, -1, -2),
    ]
    for c, p, q in power_law:
        vi = c * (a**p) * (g**q)
        H[0, 0] += p * p * vi
        H[0, 1] += p * q * vi
        H[1, 1] += q * q * vi

    # Instanton term: V_inst = A_inst * exp(-2pi a mu) / (a^2 g^4)
    # Let x = log a, y = log g, so a = e^x, g = e^y
    # V_inst(x,y) = A_inst * exp(-2pi e^x mu) * e^(-2x - 4y)
    # log V = log A_inst - 2pi mu e^x - 2x - 4y
    # dV/dx = V * (-2pi mu e^x - 2) = V * (-2pi a mu - 2)
    # d^2 V/dx^2 = V * (-2pi mu e^x - 2)^2 + V * (-2pi mu e^x)
    #            = V * [(-2pi a mu - 2)^2 - 2pi a mu]
    # dV/dy = V * (-4)
    # d^2 V/dy^2 = V * 16
    # d^2 V/dxdy = dV/dx * (-4) = V * (-2pi a mu - 2) * (-4)
    V_inst = A_inst * exp_factor / (a**2 * g**4)
    pa = -2 * np.pi * a * mu - 2
    H[0, 0] += V_inst * (pa * pa - 2 * np.pi * a * mu)
    H[0, 1] += V_inst * pa * (-4)
    H[1, 1] += V_inst * 16

    H[1, 0] = H[0, 1]
    return H


G_kin = np.array([[3.0/4, 0.5], [0.5, 2.0]])
Ginv = np.linalg.inv(G_kin)


def masses(H):
    eigs = np.linalg.eigvals(Ginv @ H)
    return np.sort(eigs.real)


def find_near_benchmark(A_inst, mu):
    seeds = [
        [0.798, 0.165, -5770.0],
        [0.8, 0.17, -6000],
        [0.7, 0.15, -4000],
        [0.9, 0.18, -8000],
        [0.6, 0.14, -3000],
        [1.0, 0.2, -12000],
        [0.5, 0.12, -1500],
        [1.2, 0.25, -20000],
        [0.4, 0.10, -500],
        [0.3, 0.08, -200],
        [1.5, 0.30, -40000],
        [2.0, 0.40, -100000],
    ]
    solutions = []
    for s in seeds:
        x, it, ok = newton(s, A_inst, mu, max_iter=500)
        if not ok:
            continue
        a, g, L = x
        if 0.05 < a < 5.0 and 0.03 < g < 2.0:
            solutions.append(x)
    if not solutions:
        return None
    # Prefer solution nearest Session 18 benchmark
    benchmark = np.array([0.798, 0.165, -5770.0])
    solutions.sort(key=lambda x: abs(x[0] - benchmark[0]) + abs(x[1] - benchmark[1]))
    return solutions[0]


print("=" * 110)
print("Stability scan: fiber-wrapped instanton, V_fib = A_inst * exp(-2π·α·μ) / (α²γ⁴)")
print("=" * 110)
print(f"{'μ':>12s} | {'A_inst':>10s} | {'α_*':>7s} {'γ_*':>7s} {'Λ_7':>10s} | "
      f"{'det H':>11s} | {'m²_light':>11s} {'m²_heavy':>11s} | stable?")
print("-" * 120)

stable_points = []

for mu_name, mu in mu_candidates.items():
    for A_inst in [1e-6, 1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100, 1e3, 1e4, 1e5]:
        x = find_near_benchmark(A_inst, mu)
        if x is None:
            # print(f"{mu_name:>12s} | {A_inst:>10.2e} | NO CONVERGENCE")
            continue
        a, g, L = x
        H = hessian_log(x, A_inst, mu)
        dH = np.linalg.det(H)
        m2 = masses(H)
        stable = (m2[0] > 0 and m2[1] > 0)
        tag = "YES" if stable else "no"
        # Print all results
        print(f"{mu_name:>12s} | {A_inst:>10.2e} | {a:7.4f} {g:7.4f} {L:10.3e} | "
              f"{dH:+11.3e} | {m2[0]:+11.3e} {m2[1]:+11.3e} | {tag}")
        if stable:
            stable_points.append((mu_name, mu, A_inst, x, m2))

print()
print("=" * 110)
if stable_points:
    print(f"STABLE POINTS FOUND ({len(stable_points)} total):")
    for mu_name, mu, A_inst, x, m2 in stable_points:
        a, g, L = x
        m_light = np.sqrt(m2[0])
        m_heavy = np.sqrt(m2[1])
        print(f"  μ={mu_name:12s} (={mu:.3f})  A_inst={A_inst:.2e}")
        print(f"    (α*, γ*, Λ_7) = ({a:.4f}, {g:.4f}, {L:.3e})")
        print(f"    m_radion: light = {m_light:.3f} M_poly, heavy = {m_heavy:.3f} M_poly")
else:
    print("NO STABLE POINTS found in the scan.")
    print()
    print("But let's check: even with tachyon, does det H flip positive anywhere?")
    print("(This was shown above in the partial printout — det H > 0 solutions if any.)")
