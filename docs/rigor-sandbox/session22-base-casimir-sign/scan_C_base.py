"""Session 22 extension: does the ρ-tachyon disappear anywhere in the physical
|C_base| range [0.05, 0.30]?

Session 22 first-principles derivation gave |C_base| ≈ 0.089 with band [0.05, 0.15].
Session 18 used 0.10 as benchmark. If smaller |C_base| reduces V_base (less negative),
the tachyon-driving q² V_base contribution to H[log γ, log γ] shrinks.

This scans the 5-term Session 18 potential over |C_base| and checks Hessian
signature at V_*=0 critical points.
"""

import numpy as np

A_R = 1.764e-3
A_F = 1.654e-2
A_C_fib = 7.139e-2
A_L = 1.764e-3
K = 16 * np.pi**2 / 7


def residuals(x, C_base):
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
        for _ in range(30):
            x_new = x + step*dx
            if 1e-3 < x_new[0] < 1e3 and 1e-3 < x_new[1] < 1e3:
                f_new = residuals(x_new, C_base)
                if np.max(np.abs(f_new)) < f_norm0*1.5:
                    x = x_new
                    break
            step *= 0.5
        else:
            return x, False
    return x, False


def hessian_log(x, C_base):
    a, g, L = x
    B_base = C_base/K**2
    terms = [
        (A_R, -1, -4),
        (A_F, +1, -6),
        (A_C_fib, -6, -4),
        (-B_base, -2, -8),
        (L*A_L, -1, -2),
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


print(f"{'C_base':>8s} | {'α_*':>7s} {'γ_*':>7s} {'Λ_7':>10s} | "
      f"{'H_aa':>10s} {'H_gg':>10s} {'H_ag':>10s} | "
      f"{'det H':>11s} | {'m²_light':>11s} {'m²_heavy':>11s}")
print("-" * 120)

for C_base in [0.05, 0.06, 0.07, 0.08, 0.089, 0.10, 0.12, 0.15, 0.20, 0.30]:
    # Try multiple seeds
    seeds = [[0.798, 0.165, -5770], [0.7, 0.15, -4000], [0.9, 0.18, -8000],
             [1.0, 0.2, -12000], [0.5, 0.12, -1000]]
    best = None
    for s in seeds:
        x, ok = newton(s, C_base, max_iter=500)
        if ok and 0.05 < x[0] < 5.0 and 0.03 < x[1] < 2.0:
            if best is None or abs(x[0]-0.8)+abs(x[1]-0.17) < abs(best[0]-0.8)+abs(best[1]-0.17):
                best = x
    if best is None:
        print(f"{C_base:8.3f} | NO CONVERGENCE in physical window")
        continue
    a, g, L = best
    H = hessian_log(best, C_base)
    m2 = masses(H)
    stable = m2[0] > 0 and m2[1] > 0
    tag = "STABLE" if stable else "saddle"
    print(f"{C_base:8.3f} | {a:7.4f} {g:7.4f} {L:10.3e} | "
          f"{H[0,0]:+10.3e} {H[1,1]:+10.3e} {H[0,1]:+10.3e} | "
          f"{np.linalg.det(H):+11.3e} | {m2[0]:+11.3e} {m2[1]:+11.3e} [{tag}]")
