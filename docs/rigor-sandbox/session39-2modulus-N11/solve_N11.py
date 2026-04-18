"""Session 39 — 2-modulus CW+FR at N=11.

Adapts Session 18's 7D Seifert KK machinery (S^1 -> H^2/Z_N) to N=11.
"""
import numpy as np

# N=11 geometric inputs
N = 11
chi_orb = 8.0 / 11
K = 4 * np.pi**2 * chi_orb
e_S = N / 2.0
r_T = e_S / np.sqrt(chi_orb)

# Coefficients (G_7 = V_3^ref = 1 units)
C_fib = 36.33
A_R = 1.0 / (32 * np.pi**3 * chi_orb)
A_F = e_S**2 / (128 * np.pi**3 * chi_orb**3)
A_L = A_R
A_C_fib = C_fib / (16 * np.pi**4 * chi_orb**2)

G_kin = np.array([[0.75, 0.5], [0.5, 2.0]])
G_inv = np.linalg.inv(G_kin)


def V(a, g, L, Cb=0.0):
    Bb = Cb / K**2
    return (A_R/(a*g**4) + A_F*a/g**6 + A_C_fib/(a**6*g**4)
            - Bb/(a**2*g**8) + L*A_L/(a*g**2))


def dVa(a, g, L, Cb=0.0):
    Bb = Cb / K**2
    return (-A_R/(a**2*g**4) + A_F/g**6 - 6*A_C_fib/(a**7*g**4)
            + 2*Bb/(a**3*g**8) - L*A_L/(a**2*g**2))


def dVg(a, g, L, Cb=0.0):
    Bb = Cb / K**2
    return (-4*A_R/(a*g**5) - 6*A_F*a/g**7 - 4*A_C_fib/(a**6*g**5)
            + 8*Bb/(a**2*g**9) - 2*L*A_L/(a*g**3))


def H2(a, g, L, Cb=0.0):
    Bb = Cb / K**2
    Vaa = (2*A_R/(a**3*g**4) + 2*L*A_L/(a**3*g**2)
           + 42*A_C_fib/(a**8*g**4) - 6*Bb/(a**4*g**8))
    Vag = (4*A_R/(a**2*g**5) + 2*L*A_L/(a**2*g**3)
           - 6*A_F/g**7 + 24*A_C_fib/(a**7*g**5) - 16*Bb/(a**3*g**9))
    Vgg = (20*A_R/(a*g**6) + 6*L*A_L/(a*g**4)
           + 42*A_F*a/g**8 + 20*A_C_fib/(a**6*g**6) - 72*Bb/(a**2*g**10))
    return np.array([[a**2*Vaa, a*g*Vag], [a*g*Vag, g**2*Vgg]])


def mass_eigs(Hlog):
    return np.sort(np.linalg.eigvals(G_inv @ Hlog).real)


print("=" * 72)
print(f"Session 39: 2-modulus CW+FR at N=11")
print("=" * 72)
print(f"  |chi_orb|  = {chi_orb:.6f}   (= 8/11)")
print(f"  K          = {K:.4f}")
print(f"  e_Seifert  = {e_S}")
print(f"  r_T        = {r_T:.4f}         (= 11 sqrt(22)/8)")
print(f"  A_R        = {A_R:.4e}")
print(f"  A_F        = {A_F:.4e}")
print(f"  A_L        = {A_L:.4e}")
print(f"  A_C_fib    = {A_C_fib:.4e}")
print()

# Branch (a): Thurston ray, no base Casimir
print("-" * 72)
print("Branch (a): Thurston ray alpha = r_T * gamma, |C_base|=0")
print("-" * 72)
lhs = A_R + 4 * A_F * r_T**2
rhs = 4 * A_C_fib / r_T**5
g_a = (rhs/lhs)**(1/5)
a_a = r_T * g_a
L_a = ((A_F * r_T**2 - A_R) * g_a**5 - 6 * A_C_fib / r_T**5) / (A_L * g_a**7)
print(f"  alpha_* = {a_a:.5f},  gamma_* = {g_a:.5f},  ratio = {a_a/g_a:.5f}")
print(f"  Lambda_7 = {L_a:.3e}")
print(f"  V_*      = {V(a_a, g_a, L_a):.3e}")
print(f"  dV/dalpha = {dVa(a_a, g_a, L_a):.3e}")
print(f"  dV/dgamma = {dVg(a_a, g_a, L_a):.3e}")

Hlog_a = H2(a_a, g_a, L_a)
print(f"  H eigenvalues: tr = {np.trace(Hlog_a):.3e}, det = {np.linalg.det(Hlog_a):.3e}")
eigs_a = mass_eigs(Hlog_a)
print(f"  m^2 (dim-less): m^2_- = {eigs_a[0]:.3e},  m^2_+ = {eigs_a[1]:.3e}")

# Dimensional restoration
L0inv2_Mp2 = (a_a / r_T)**2
m2_minus_Mp = eigs_a[0] * L0inv2_Mp2
m2_plus_Mp = eigs_a[1] * L0inv2_Mp2
print(f"  L_0 = {r_T/a_a:.3f}/M_poly,  L_0^-2 = {L0inv2_Mp2:.4f} M_poly^2")
if m2_minus_Mp > 0:
    print(f"  m_- = {np.sqrt(m2_minus_Mp):.2f} M_poly   [STABLE]")
else:
    print(f"  m_- = {np.sqrt(abs(m2_minus_Mp)):.2f} i M_poly  [TACHYON]")
print(f"  m_+ = {np.sqrt(m2_plus_Mp):.2f} M_poly")

# Branch (c): V_*=0 Minkowski
print()
print("-" * 72)
print("Branch (c): V_*=0 Minkowski scan over |C_base|")
print("-" * 72)

def res3(x, Cb):
    a, g, L = x
    return np.array([V(a, g, L, Cb), dVa(a, g, L, Cb), dVg(a, g, L, Cb)])


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


print(f"  {'|C_base|':>9s}  {'alpha_*':>9s} {'gamma_*':>9s} {'Lambda_7':>12s}  exists?")
for Cb in [0.005, 0.010, 0.020, 0.030, 0.050, 0.080, 0.100, 0.150]:
    found = False
    for seed in [[a_a, g_a, L_a], [0.5, 0.08, -1e5], [0.8, 0.15, -1e4],
                 [1.0, 0.20, -5e3], [0.3, 0.05, -1e6]]:
        x, ok = newton3(seed, Cb)
        if ok and 0.05 < x[0] < 10 and 0.02 < x[1] < 5:
            print(f"  {Cb:9.4f}  {x[0]:9.5f} {x[1]:9.5f} {x[2]:12.3e}  yes")
            found = True
            break
    if not found:
        print(f"  {Cb:9.4f}   ----     ----     ----          NO")
