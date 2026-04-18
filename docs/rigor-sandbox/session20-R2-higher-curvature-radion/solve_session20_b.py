"""Session 20 part B: fine-grained scan over R2_scale (including negatives),
with multi-start seeding to find the benchmark-branch critical point.

Also: check if the SIGN of R^2 matters (heterotic has a_1 > 0 but higher-curvature
corrections can effectively appear with either sign after field redefinitions).
"""

import numpy as np

# Polygon-theory coefficients (G_7 = 1)
A_R = 1.764e-3
A_F = 1.654e-2
A_C_fib = 7.139e-2
A_L = 1.764e-3
K = 16 * np.pi**2 / 7
B_base = 0.10 / K**2
alpha_7 = 1.0 / 8.5957
e_Seifert = 3.5
T = alpha_7 / (16 * np.pi * K)
A_R2_1 = 4 * T
A_R2_2 = 2 * T * e_Seifert**2
A_R2_3 = T * e_Seifert**4 / 4


def residuals(x, R2_scale=1.0):
    a, g, L = x
    g2, g4, g6, g8, g10 = g**2, g**4, g**6, g**8, g**10

    Vi = {
        "Ric": A_R / (a * g4),
        "FR":  A_F * a / g6,
        "fib": A_C_fib / (a**6 * g4),
        "base": -B_base / (a**2 * g8),
        "Lam": L * A_L / (a * g2),
        "R2_1": R2_scale * A_R2_1 / (a * g6),
        "R2_2": R2_scale * A_R2_2 * a / g8,
        "R2_3": R2_scale * A_R2_3 * a**3 / g10,
    }
    pq = {
        "Ric":  (-1, -4),
        "FR":   (+1, -6),
        "fib":  (-6, -4),
        "base": (-2, -8),
        "Lam":  (-1, -2),
        "R2_1": (-1, -6),
        "R2_2": (+1, -8),
        "R2_3": (+3, -10),
    }
    V = sum(Vi.values())
    dV_da = sum(pq[n][0] * Vi[n] / a for n in Vi)
    dV_dg = sum(pq[n][1] * Vi[n] / g for n in Vi)
    return np.array([V, dV_da, dV_dg]), Vi


def jacobian(x, R2_scale=1.0, eps=1e-7):
    J = np.zeros((3, 3))
    f0, _ = residuals(x, R2_scale=R2_scale)
    for i in range(3):
        xp = x.copy()
        h = max(abs(xp[i]) * eps, eps)
        xp[i] += h
        f1, _ = residuals(xp, R2_scale=R2_scale)
        J[:, i] = (f1 - f0) / h
    return J


def newton(x0, R2_scale=1.0, max_iter=500, tol=1e-9):
    x = np.array(x0, dtype=float)
    for it in range(max_iter):
        f, _ = residuals(x, R2_scale=R2_scale)
        if np.max(np.abs(f)) < tol:
            return x, it, True
        J = jacobian(x, R2_scale=R2_scale)
        try:
            dx = np.linalg.solve(J, -f)
        except np.linalg.LinAlgError:
            return x, it, False
        step = 1.0
        f_norm0 = np.max(np.abs(f))
        for _ in range(30):
            x_new = x + step * dx
            if x_new[0] > 1e-3 and x_new[0] < 1e3 and x_new[1] > 1e-3 and x_new[1] < 1e3:
                f_new, _ = residuals(x_new, R2_scale=R2_scale)
                if np.max(np.abs(f_new)) < f_norm0 * 1.1:
                    x = x_new
                    break
            step *= 0.5
        else:
            return x, it, False
    return x, max_iter, False


def hessian_log(x, R2_scale=1.0):
    a, g, L = x
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


G = np.array([[3.0/4, 0.5], [0.5, 2.0]])


def radion_masses(H):
    Ginv = np.linalg.inv(G)
    eigs = np.linalg.eigvals(Ginv @ H)
    return np.sort(eigs.real)


def find_near_benchmark(R2_scale):
    """Try multiple starting points to find a critical point near Session 18 benchmark."""
    seeds = [
        [0.798, 0.165, -5770.0],
        [0.8, 0.17, -6000],
        [0.7, 0.15, -4000],
        [0.9, 0.18, -8000],
        [0.6, 0.14, -3000],
        [1.0, 0.2, -12000],
        [0.5, 0.12, -1500],
        [1.2, 0.25, -20000],
        [0.4, 0.1, -500],
    ]
    best = None
    for s in seeds:
        x, it, ok = newton(s, R2_scale=R2_scale, max_iter=500)
        if not ok:
            continue
        a, g, L = x
        # Require physical window
        if 0.05 < a < 5.0 and 0.03 < g < 2.0:
            if best is None or abs(a - 0.798) + abs(g - 0.165) < abs(best[0] - 0.798) + abs(best[1] - 0.165):
                best = x
    return best


# Scan R2_scale from -2 to +2 (polygon value = +1.0)
print(f"{'R2_scl':>8s} | {'alpha':>8s} {'gamma':>8s} {'Lambda_7':>10s} | "
      f"{'det H':>11s} {'tr H':>11s} | {'m^2_light':>11s} {'m^2_heavy':>11s} | stable?")
print("-" * 120)

stability_region = []

scales = [-2.0, -1.0, -0.5, -0.2, -0.1, -0.03, -0.01, -0.003, -0.001,
          0.0, 0.001, 0.003, 0.01, 0.03, 0.1, 0.2, 0.5, 1.0, 2.0]

for s in scales:
    x = find_near_benchmark(s)
    if x is None:
        print(f"{s:8.3f} | NO CONVERGENCE IN PHYSICAL WINDOW")
        continue
    a, g, L = x
    H = hessian_log(x, R2_scale=s)
    dH, trH = np.linalg.det(H), np.trace(H)
    m2 = radion_masses(H)
    stable = "YES" if (m2[0] > 0 and m2[1] > 0) else "no"
    if stable == "YES":
        stability_region.append((s, x, m2))
    print(f"{s:8.3f} | {a:8.4f} {g:8.4f} {L:10.3e} | "
          f"{dH:+11.3e} {trH:+11.3e} | {m2[0]:+11.3e} {m2[1]:+11.3e} | {stable}")

print()
print("=" * 80)
if stability_region:
    print(f"STABLE POINTS FOUND at R2_scale values: {[s for s,_,_ in stability_region]}")
    for s, x, m2 in stability_region:
        a, g, L = x
        print(f"  R2={s:.4f}: (a,g,L) = ({a:.4f}, {g:.4f}, {L:.3e})")
        print(f"    m_light = {np.sqrt(m2[0]):.3f} M_poly, m_heavy = {np.sqrt(m2[1]):.3f} M_poly")
else:
    print("NO stable critical points in scan range (R2_scale ∈ [-2, +2])")
