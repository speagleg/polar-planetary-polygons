"""Check stability of V_*=0 Minkowski critical points at N=11."""
import numpy as np

N = 11
chi_orb = 8.0 / 11
K = 4 * np.pi**2 * chi_orb
e_S = N / 2.0
r_T = e_S / np.sqrt(chi_orb)

C_fib = 36.33
A_R = 1.0 / (32 * np.pi**3 * chi_orb)
A_F = e_S**2 / (128 * np.pi**3 * chi_orb**3)
A_L = A_R
A_C_fib = C_fib / (16 * np.pi**4 * chi_orb**2)

G_kin = np.array([[0.75, 0.5], [0.5, 2.0]])
G_inv = np.linalg.inv(G_kin)


def res3(x, Cb):
    a, g, L = x
    Bb = Cb / K**2
    V = (A_R/(a*g**4) + A_F*a/g**6 + A_C_fib/(a**6*g**4)
         - Bb/(a**2*g**8) + L*A_L/(a*g**2))
    dVa = (-A_R/(a**2*g**4) + A_F/g**6 - 6*A_C_fib/(a**7*g**4)
           + 2*Bb/(a**3*g**8) - L*A_L/(a**2*g**2))
    dVg = (-4*A_R/(a*g**5) - 6*A_F*a/g**7 - 4*A_C_fib/(a**6*g**5)
           + 8*Bb/(a**2*g**9) - 2*L*A_L/(a*g**3))
    return np.array([V, dVa, dVg])


def H2(a, g, L, Cb):
    Bb = Cb / K**2
    Vaa = (2*A_R/(a**3*g**4) + 2*L*A_L/(a**3*g**2)
           + 42*A_C_fib/(a**8*g**4) - 6*Bb/(a**4*g**8))
    Vag = (4*A_R/(a**2*g**5) + 2*L*A_L/(a**2*g**3)
           - 6*A_F/g**7 + 24*A_C_fib/(a**7*g**5) - 16*Bb/(a**3*g**9))
    Vgg = (20*A_R/(a*g**6) + 6*L*A_L/(a*g**4)
           + 42*A_F*a/g**8 + 20*A_C_fib/(a**6*g**6) - 72*Bb/(a**2*g**10))
    return np.array([[a**2*Vaa, a*g*Vag], [a*g*Vag, g**2*Vgg]])


def newton3(x0, Cb, tol=1e-9, maxit=500):
    x = np.array(x0, float)
    for _ in range(maxit):
        f = res3(x, Cb)
        if np.max(np.abs(f)) < tol:
            return x, True
        h = 1e-7
        J = np.zeros((3, 3))
        for i in range(3):
            xp = x.copy()
            xp[i] += h * max(abs(xp[i]), 1)
            J[:, i] = (res3(xp, Cb) - f) / (h * max(abs(x[i]), 1))
        try:
            dx = np.linalg.solve(J, -f)
        except np.linalg.LinAlgError:
            return x, False
        step = 1.0
        f0 = np.max(np.abs(f))
        for _ in range(40):
            xn = x + step * dx
            if xn[0] > 0 and xn[1] > 0:
                fn = res3(xn, Cb)
                if np.max(np.abs(fn)) < f0 * 1.5:
                    x = xn
                    break
            step *= 0.5
        else:
            return x, False
    return x, False


print("V_*=0 Minkowski critical points at N=11: stability scan")
print("=" * 90)
print(f"{'|C_base|':>9s} {'alpha_*':>8s} {'gamma_*':>8s} {'Lambda_7':>12s} "
      f"{'det(H)':>11s} {'tr(H)':>11s} {'m^2_-':>11s} {'m^2_+':>11s}  Status")
print("-" * 90)

for Cb in [0.005, 0.010, 0.020, 0.030, 0.050, 0.080, 0.100, 0.150, 0.200]:
    for seed in [[0.6, 0.1, -1e5], [0.5, 0.05, -5e5], [0.7, 0.13, -5e4], [0.55, 0.08, -2e5]]:
        x, ok = newton3(seed, Cb)
        if ok and 0.05 < x[0] < 10 and 0.02 < x[1] < 5:
            a, g, L = x
            Hlog = H2(a, g, L, Cb)
            det_H = np.linalg.det(Hlog)
            tr_H = np.trace(Hlog)
            eigs = np.sort(np.linalg.eigvals(G_inv @ Hlog).real)
            if eigs[0] > 0 and eigs[1] > 0:
                status = "STABLE MIN"
            elif eigs[0] < 0 and eigs[1] < 0:
                status = "MAX"
            else:
                status = "SADDLE"
            print(f"{Cb:9.4f} {a:8.4f} {g:8.4f} {L:12.3e} "
                  f"{det_H:+11.3e} {tr_H:+11.3e} {eigs[0]:+11.3e} {eigs[1]:+11.3e}  {status}")
            break
    else:
        print(f"{Cb:9.4f}  no convergence")

print()
print("Physical mass conversion at stable points (L_0^-2 = (a/r_T)^2 M_poly^2):")
print("-" * 90)
for Cb in [0.005, 0.010, 0.020, 0.050, 0.100]:
    for seed in [[0.6, 0.1, -1e5], [0.5, 0.05, -5e5], [0.7, 0.13, -5e4]]:
        x, ok = newton3(seed, Cb)
        if ok and 0.05 < x[0] < 10 and 0.02 < x[1] < 5:
            a, g, L = x
            Hlog = H2(a, g, L, Cb)
            eigs = np.sort(np.linalg.eigvals(G_inv @ Hlog).real)
            L0inv2 = (a / r_T)**2
            if eigs[0] > 0 and eigs[1] > 0:
                m_m = np.sqrt(eigs[0] * L0inv2)
                m_p = np.sqrt(eigs[1] * L0inv2)
                print(f"|C_base|={Cb:.4f}: m_- = {m_m:.2f} M_poly, m_+ = {m_p:.2f} M_poly")
            else:
                print(f"|C_base|={Cb:.4f}: eigenvalues {eigs[0]:.3e}, {eigs[1]:.3e} (not stable)")
            break
