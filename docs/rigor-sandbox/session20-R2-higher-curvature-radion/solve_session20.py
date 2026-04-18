"""Session 20: full 8-term radion potential with higher-curvature R^2 corrections.

Solves {V=0, dV/dalpha=0, dV/dgamma=0} in unknowns (alpha, gamma, Lambda_7) via
manual Newton-Raphson (no scipy available).
"""

import numpy as np

# ---------- Polygon-theory coefficients (G_7 = 1 units) ----------
A_R = 1.764e-3     # Ricci: A_R / (alpha * gamma^4)           scaling (-1, -4)
A_F = 1.654e-2     # Freund-Rubin: A_F * alpha / gamma^6      scaling (+1, -6)
A_C_fib = 7.139e-2 # fiber Casimir: A_C_fib / (alpha^6 gamma^4)  scaling (-6, -4)
A_L = 1.764e-3     # Lambda_7 * A_L / (alpha * gamma^2)       scaling (-1, -2)

# base Casimir at |C_base| = 0.10:
C_base_val = 0.10
K = 16 * np.pi**2 / 7
B_base = C_base_val / K**2       # -B_base / (alpha^2 * gamma^8)  scaling (-2, -8)

# R^2 coefficients (simple R^2, a_1 = 1):
alpha_7 = 1.0 / (2.0 * 4.297838)  # = 1/k(7) = 1/8.596 = 0.11633
e_Seifert = 7.0 / 2.0             # Seifert Euler class
T = alpha_7 / (16 * np.pi * K)    # = 1.026e-4

A_R2_1 = 4 * T                     # scaling (-1, -6)
A_R2_2 = 2 * T * e_Seifert**2      # scaling (+1, -8)
A_R2_3 = T * e_Seifert**4 / 4      # scaling (+3, -10)

print(f"Polygon coefficients (G_7=1 units):")
print(f"  A_R      = {A_R:.3e}")
print(f"  A_F      = {A_F:.3e}")
print(f"  A_C_fib  = {A_C_fib:.3e}")
print(f"  A_L      = {A_L:.3e}")
print(f"  B_base   = {B_base:.3e}")
print(f"  alpha_7  = {alpha_7:.4f}")
print(f"  T        = {T:.3e}")
print(f"  A_R2_1   = {A_R2_1:.3e}  (-1, -6)")
print(f"  A_R2_2   = {A_R2_2:.3e}  (+1, -8)")
print(f"  A_R2_3   = {A_R2_3:.3e}  (+3, -10)")
print()


def potential_and_derivs(alpha, gamma, Lambda_7, R2_scale=1.0):
    """Return (V, dV_dalpha, dV_dgamma, dV_dLambda) for current (alpha, gamma, Lambda_7).

    R2_scale multiplies the three R^2 channel coefficients (for scan).
    """
    a, g = alpha, gamma
    g2, g4, g6, g8, g10 = g**2, g**4, g**6, g**8, g**10

    # Term list: (name, coeff, p, q)  where V_i = coeff * alpha^p * gamma^q
    terms = [
        ("Ric",  A_R, -1, -4),
        ("FR",   A_F, +1, -6),
        ("fib",  A_C_fib, -6, -4),
        ("base", -B_base, -2, -8),
        ("Lam",  Lambda_7 * A_L, -1, -2),
        ("R2_1", R2_scale * A_R2_1, -1, -6),
        ("R2_2", R2_scale * A_R2_2, +1, -8),
        ("R2_3", R2_scale * A_R2_3, +3, -10),
    ]

    V = 0.0
    dV_da = 0.0
    dV_dg = 0.0
    Vs = {}
    for name, c, p, q in terms:
        vi = c * (a**p) * (g**q)
        V += vi
        dV_da += p * vi / a
        dV_dg += q * vi / g
        Vs[name] = vi

    # dV / dLambda_7 = A_L / (alpha * gamma^2)
    dV_dL = A_L / (a * g2)

    return V, dV_da, dV_dg, dV_dL, Vs


def residuals(x, R2_scale=1.0):
    """F = [V, dV/dalpha, dV/dgamma]"""
    a, g, L = x
    V, dVa, dVg, dVL, _ = potential_and_derivs(a, g, L, R2_scale=R2_scale)
    return np.array([V, dVa, dVg])


def jacobian(x, R2_scale=1.0, eps=1e-6):
    """Numerical Jacobian."""
    J = np.zeros((3, 3))
    f0 = residuals(x, R2_scale=R2_scale)
    for i in range(3):
        xp = x.copy()
        h = max(abs(xp[i]) * eps, eps)
        xp[i] += h
        f1 = residuals(xp, R2_scale=R2_scale)
        J[:, i] = (f1 - f0) / h
    return J


def newton(x0, R2_scale=1.0, max_iter=200, tol=1e-10, damp=1.0):
    x = np.array(x0, dtype=float)
    for it in range(max_iter):
        f = residuals(x, R2_scale=R2_scale)
        if np.max(np.abs(f)) < tol:
            return x, it, True
        J = jacobian(x, R2_scale=R2_scale)
        try:
            dx = np.linalg.solve(J, -f)
        except np.linalg.LinAlgError:
            return x, it, False
        # Line search
        for _ in range(20):
            x_new = x + damp * dx
            if x_new[0] > 0 and x_new[1] > 0:
                f_new = residuals(x_new, R2_scale=R2_scale)
                if np.max(np.abs(f_new)) < np.max(np.abs(f)) or damp < 1e-6:
                    x = x_new
                    break
            damp *= 0.5
        else:
            return x, it, False
        damp = min(1.0, damp * 2.0)
    return x, max_iter, False


def hessian_log(x, R2_scale=1.0):
    """Hessian in (log alpha, log gamma) basis at critical point."""
    a, g, L = x
    # terms = (coeff, p, q)
    terms = [
        (A_R, -1, -4),
        (A_F, +1, -6),
        (A_C_fib, -6, -4),
        (-B_base, -2, -8),
        (L * A_L, -1, -2),
        (R2_scale * A_R2_1, -1, -6),
        (R2_scale * A_R2_2, +1, -8),
        (R2_scale * A_R2_3, +3, -10),
    ]
    H = np.zeros((2, 2))
    for c, p, q in terms:
        vi = c * (a**p) * (g**q)
        H[0, 0] += p * p * vi
        H[0, 1] += p * q * vi
        H[1, 0] += p * q * vi
        H[1, 1] += q * q * vi
    return H


def kinetic_matrix():
    """From Session 18 §4: G_ij = [[3/4, 1/2], [1/2, 2]] in (log alpha, log gamma)."""
    return np.array([[3.0/4, 0.5], [0.5, 2.0]])


def radion_masses(H, G):
    """m^2 eigenvalues of G^{-1} H, in M_poly^2 units."""
    Ginv = np.linalg.inv(G)
    M = Ginv @ H
    eigs = np.linalg.eigvals(M)
    return np.sort(eigs.real)


# ---------- Solve for several R2_scale values ----------
print("=" * 70)
print("Newton solves across R2_scale (= scaling of A_R2 coefficients)")
print("=" * 70)
# Session 18 benchmark as initial guess
x0_base = [0.798, 0.165, -5770.0]

results = []
for R2_scale in [0.0, 0.001, 0.01, 0.1, 0.3, 1.0, 3.0, 10.0]:
    x0 = x0_base.copy()
    x, it, ok = newton(x0, R2_scale=R2_scale, max_iter=500)
    if not ok:
        # try different starting points
        for seed in [(0.5, 0.3, -500), (1.5, 0.3, -1000), (0.8, 0.1, -10000),
                     (2.0, 0.5, -100), (0.3, 0.1, -30000)]:
            x, it, ok = newton(list(seed), R2_scale=R2_scale, max_iter=500)
            if ok:
                break

    line = f"R2_scale={R2_scale:6.3f} | "
    if ok:
        a, g, L = x
        V, dVa, dVg, dVL, Vs = potential_and_derivs(a, g, L, R2_scale=R2_scale)
        H = hessian_log(x, R2_scale=R2_scale)
        G = kinetic_matrix()
        try:
            m2 = radion_masses(H, G)
            dethess = np.linalg.det(H)
            trhess = np.trace(H)
        except Exception as ex:
            m2 = [np.nan, np.nan]
            dethess = np.nan
            trhess = np.nan

        line += f"a*={a:.4f}, g*={g:.4f}, L7={L:.3e} | "
        line += f"V={V:+.2e}, det(H)={dethess:+.3e}, tr(H)={trhess:+.3e} | "
        line += f"m^2=({m2[0]:+.3e}, {m2[1]:+.3e})"
        results.append((R2_scale, x, m2, dethess, trhess, Vs))
    else:
        line += "NO CONVERGENCE"
    print(line)

print()
print("=" * 70)
print("Detail at R2_scale = 1.0 (polygon-theory value)")
print("=" * 70)
for R2_scale, x, m2, dethess, trhess, Vs in results:
    if abs(R2_scale - 1.0) < 1e-9:
        a, g, L = x
        print(f"Critical point: (alpha, gamma, Lambda_7) = ({a:.4f}, {g:.4f}, {L:.3e})")
        print(f"V_i contributions at this point:")
        for name, vi in Vs.items():
            print(f"  {name:6s} = {vi:+.4e}")
        print(f"Sum V   = {sum(Vs.values()):+.4e}")
        print(f"Hessian eigenvalues (log basis): det = {dethess:+.4e}, trace = {trhess:+.4e}")
        print(f"Radion masses^2 (M_poly^2 units): {m2[0]:+.4e}, {m2[1]:+.4e}")
        if m2[0] > 0 and m2[1] > 0:
            print(f"BOTH EIGENVALUES POSITIVE — STABLE MINIMUM")
            print(f"  m_radion_light = {np.sqrt(m2[0]):.3f} M_poly")
            print(f"  m_radion_heavy = {np.sqrt(m2[1]):.3f} M_poly")
        else:
            print(f"At least one eigenvalue non-positive — saddle or unstable")
