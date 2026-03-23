"""
4D Einstein equations with the EXACT Weyl anomaly.

The full Havelock eigenvalue:
    lambda_m = log(2sinh rho) + b(N) - m(N-m)/2 + L(m,N) - S2(m,N)/4 + c(N)

Now compute the 4D Einstein equations on R x (H^2 x_N S^1) using
the COMPLETE matter content, including the exact orbifold correction.

The stress-energy tensor of the KK tower has contributions from:
1. The Casimir mass spectrum: mu_m^2 = (m - N/2)^2
2. The orbifold correction: delta_m = L(m,N) - S2(m,N)/4 + c(N)
3. The zero-point energy: E_zp = N^2/8

The Einstein equations G_{mu nu} + Lambda g_{mu nu} = 8 pi G T_{mu nu}
give constraints on the geometry from the matter content.
"""

import numpy as np
from math import pi, sin, cos, log, exp, sqrt, sinh, cosh


def casimir(m, N):
    return m * (N - m) / 2.0


def b_exact(N):
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


def kk_mass_sq(m, N):
    return (m - N / 2)**2


def logsin_sum(m, N):
    """L(m,N) = Sigma [-log(sin(pi p/N))] cos(2pi pm/N)."""
    return sum(-log(sin(pi * p / N)) * cos(2 * pi * p * m / N)
               for p in range(1, N))


def csc2_sum(m, N):
    """S2(m,N) = Sigma csc^2(pi p/N) cos(2pi pm/N)."""
    return sum(1 / sin(pi * p / N)**2 * cos(2 * pi * p * m / N)
               for p in range(1, N))


def weyl_anomaly(m, N):
    """delta_m = L(m,N) - (1/4) S2(m,N) + c(N)."""
    L = logsin_sum(m, N)
    S2 = csc2_sum(m, N)
    return L - S2 / 4  # c(N) is mode-independent, absorbed into b


def havelock_flat(m, N):
    """The flat Havelock eigenvalue S_m."""
    return sum(-log(2 * abs(sin(pi * p / N))) * cos(2 * pi * p * m / N)
               for p in range(1, N))


# =====================================================================
# PART 1: The complete stress-energy tensor
# =====================================================================

def stress_energy_kk(N, rho):
    """The stress-energy tensor of the KK tower at the N-gon.

    For each mode m: T^{(m)}_{mu nu} depends on:
    - The KK mass: mu_m^2 = (m - N/2)^2
    - The orbifold correction: delta_m
    - The mode amplitude: |epsilon_m|^2

    At the palindromic threshold (epsilon_{m*} -> 0):
    Only the frozen modes contribute.

    The energy density: rho = sum_{m != m*} lambda_m |epsilon_m|^2
    The pressure: anisotropic (different along base and fiber)
    """
    m_crit = N // 2

    # All eigenvalues at this rho
    eigenvalues = []
    mu_sq_vals = []
    delta_vals = []
    casimir_vals = []

    for m in range(1, N):
        lam = havelock_flat(m, N) + log(2 * sinh(rho))
        mu2 = kk_mass_sq(m, N)
        delta = weyl_anomaly(m, N)
        f_m = casimir(m, N)

        eigenvalues.append(lam)
        mu_sq_vals.append(mu2)
        delta_vals.append(delta)
        casimir_vals.append(f_m)

    eigenvalues = np.array(eigenvalues)
    mu_sq = np.array(mu_sq_vals)
    deltas = np.array(delta_vals)
    casimirs = np.array(casimir_vals)

    # The stress-energy components:
    # T_tt = energy density = sum lambda_m |eps_m|^2
    # T_{ij} = base pressure (from H^2 gradients)
    # T_{phi phi} = fiber pressure (from KK momentum)

    # At unit amplitude (|eps_m|^2 = 1 for all modes):
    T_tt = np.sum(eigenvalues)

    # The base pressure: from the gradient of psi_m on H^2
    # P_base = sum (d lambda_m / d rho) |eps_m|^2
    # d lambda_m / d rho = coth(rho) (same for all m)
    coth_rho = cosh(rho) / sinh(rho) if rho > 0.01 else 1 / rho
    P_base = coth_rho * (N - 1)  # sum of all mode contributions

    # The fiber pressure: from the KK momentum
    # P_fiber = sum mu_m^2 |eps_m|^2
    P_fiber = np.sum(mu_sq)

    # The orbifold correction to the pressure:
    # delta_P = sum delta_m |eps_m|^2
    delta_P = np.sum(deltas)  # should be ~0 (traceless)

    return {
        'T_tt': T_tt,
        'P_base': P_base,
        'P_fiber': P_fiber,
        'delta_P': delta_P,
        'eigenvalues': eigenvalues,
        'mu_sq': mu_sq,
        'deltas': deltas,
        'casimirs': casimirs,
    }


# =====================================================================
# PART 2: The Einstein equations
# =====================================================================

def einstein_with_matter(N, rho):
    """The 4D Einstein equations with the exact KK matter.

    G_{mu nu} + Lambda g_{mu nu} = 8 pi G T_{mu nu}

    For the metric ds^2 = -dt^2 + ds^2_{H^2} + (dphi + A)^2:

    The geometric side (from the Seifert Ricci tensor):
    G_tt = (1/2) R^{(3)} = -(1 + N^2/16)
    G_{ij} = [R_{ij} - (1/2)R g_{ij}] = ...
    G_{phi phi} = ...

    The matter side: 8 pi G T_{mu nu}

    The constraint: G_tt + Lambda = 8 pi G T_tt
    -> Lambda is determined by the balance of geometry and matter.
    """
    # Geometric side
    R_ij_coeff = -1 - (N/2)**2 / 2  # R_{ij} / g_{ij}
    R_phiphi = (N/2)**2 / 2
    R_scalar = 2 * R_ij_coeff + R_phiphi

    # Einstein tensor for the spatial part:
    # G_ij^{(3)} = R_ij - (1/2) R g_ij
    G_ij = R_ij_coeff - R_scalar / 2
    G_phiphi = R_phiphi - R_scalar / 2

    # For the 4D static spacetime:
    # G_tt = (1/2) R^{(3)} (the Hamiltonian constraint)
    G_tt = R_scalar / 2

    # Matter side
    T = stress_energy_kk(N, rho)
    c = 12 * b_exact(N)
    G_newton = 3 / (2 * c)

    # The Einstein equation G_tt + Lambda = 8 pi G T_tt
    # -> Lambda = 8 pi G T_tt - G_tt
    Lambda_from_matter = 8 * pi * G_newton * T['T_tt'] - G_tt

    return {
        'G_tt': G_tt,
        'G_ij': G_ij,
        'G_phiphi': G_phiphi,
        'R_scalar': R_scalar,
        'Lambda_geom': R_scalar / 2,  # the geometric Lambda
        'Lambda_matter': Lambda_from_matter,
        'T_tt': T['T_tt'],
        'P_base': T['P_base'],
        'P_fiber': T['P_fiber'],
        'G_newton': G_newton,
    }


# =====================================================================
# PART 3: The trace equation and the cosmological constant
# =====================================================================

def trace_equation():
    """The trace of the Einstein equations.

    In 4D: R - 4*Lambda = -8*pi*G*T
    where T = g^{mu nu} T_{mu nu} is the trace of T.

    For our matter: T = -T_tt + T_base + T_base + T_fiber
    = -rho + 2*P_base + P_fiber

    At the threshold (rho* where lambda_{m*} = 0):
    T_tt = E_frozen (sum of frozen eigenvalues)
    """
    print("=" * 72)
    print("  THE TRACE EQUATION AND Lambda")
    print("=" * 72)

    print(f"\n  R - 4*Lambda = -8*pi*G*T")
    print(f"  where T = -T_tt + 2*P_base + P_fiber\n")

    print(f"  {'N':>4s} {'R^(3)':>10s} {'T_tt':>10s} {'P_fiber':>10s} "
          f"{'8piG*T_tt':>12s} {'Lambda_g':>10s} {'Lambda_m':>10s}")

    for N in range(5, 16):
        rho = 2.0  # a representative value
        E = einstein_with_matter(N, rho)

        eight_pi_G_T = 8 * pi * E['G_newton'] * E['T_tt']

        print(f"  {N:4d} {E['R_scalar']:10.4f} {E['T_tt']:10.4f} "
              f"{E['P_fiber']:10.4f} {eight_pi_G_T:12.6f} "
              f"{E['Lambda_geom']:10.4f} {E['Lambda_matter']:10.4f}")


# =====================================================================
# PART 4: The exact matter contributions mode by mode
# =====================================================================

def mode_by_mode_4d():
    """The exact 4D contribution of each mode."""
    print(f"\n{'='*72}")
    print("  MODE-BY-MODE 4D CONTRIBUTIONS")
    print("=" * 72)

    for N in [7, 8]:
        rho = 2.0
        T = stress_energy_kk(N, rho)

        print(f"\n  N = {N}, rho = {rho}:")
        print(f"  {'m':>4s} {'lambda_m':>10s} {'mu^2':>8s} {'delta_m':>10s} "
              f"{'f(m)':>8s} {'lam/f':>8s}")

        for m in range(1, N):
            i = m - 1
            lam = T['eigenvalues'][i]
            mu2 = T['mu_sq'][i]
            delta = T['deltas'][i]
            f_m = T['casimirs'][i]
            ratio = lam / f_m if abs(f_m) > 0.01 else float('nan')

            print(f"  {m:4d} {lam:10.4f} {mu2:8.4f} {delta:10.6f} "
                  f"{f_m:8.4f} {ratio:8.4f}")

        print(f"  Sum eigenvalues: {np.sum(T['eigenvalues']):.4f}")
        print(f"  Sum mu^2: {np.sum(T['mu_sq']):.4f}")
        print(f"  Sum delta: {np.sum(T['deltas']):.2e}")


# =====================================================================
# PART 5: The rho-dependent Einstein constraint
# =====================================================================

def rho_dependent_constraint():
    """How the Einstein equations constrain rho."""
    print(f"\n{'='*72}")
    print("  THE rho-DEPENDENT CONSTRAINT")
    print("=" * 72)

    N = 8
    c = 12 * b_exact(N)
    G = 3 / (2 * c)

    print(f"\n  N = {N}, c = {c:.2f}, G = {G:.6f}")
    print(f"\n  {'rho':>8s} {'T_tt':>10s} {'8piG*T':>10s} {'R^(3)':>10s} "
          f"{'Lambda_m':>10s} {'Lambda_g':>10s} {'balance':>10s}")

    R3 = -2 - N**2 / 8
    Lambda_g = R3 / 2

    for rho in np.linspace(0.5, 10, 20):
        T = stress_energy_kk(N, rho)
        matter_term = 8 * pi * G * T['T_tt']
        Lambda_m = matter_term - Lambda_g
        balance = Lambda_m - Lambda_g

        print(f"  {rho:8.4f} {T['T_tt']:10.4f} {matter_term:10.6f} "
              f"{R3:10.4f} {Lambda_m:10.4f} {Lambda_g:10.4f} "
              f"{balance:10.4f}")

    print(f"""
  The geometric Lambda = R^(3)/2 = {Lambda_g:.4f} is FIXED (rho-independent).
  The matter contribution 8*pi*G*T_tt DEPENDS on rho through lambda_m(rho).

  The Einstein constraint Lambda_geom = 8*pi*G*T_tt gives:
  {Lambda_g:.4f} = 8*pi*G * sum lambda_m(rho)

  This is an EQUATION FOR rho: the Einstein equations DETERMINE
  the geodesic radius of the polygon!
""")

    # Solve for the rho that satisfies the constraint
    target = Lambda_g  # G_tt must equal 8piG T_tt
    print(f"  Solving: 8*pi*G * T_tt(rho) = {target:.4f}")
    print(f"  (This determines the equilibrium polygon size from gravity)")

    rho_solution = None
    for rho in np.linspace(0.01, 20, 2000):
        T = stress_energy_kk(N, rho)
        lhs = 8 * pi * G * T['T_tt']
        if rho_solution is None and abs(lhs - target) < 0.1:
            rho_solution = rho

        if abs(lhs - target) < 0.01:
            print(f"  SOLUTION: rho = {rho:.4f}, "
                  f"8piG*T = {lhs:.4f}, target = {target:.4f}")
            break

    if rho_solution:
        print(f"\n  The Einstein equations select rho ~ {rho_solution:.2f}")
        print(f"  This is the DYNAMICAL DETERMINATION of the polygon size.")
    else:
        print(f"\n  No solution found in [0.01, 20].")
        print(f"  The matter contribution may never reach the geometric Lambda.")


# =====================================================================
# PART 6: The exact orbifold stress-energy
# =====================================================================

def orbifold_stress_energy():
    """The stress-energy tensor with the exact Weyl anomaly."""
    print(f"\n{'='*72}")
    print("  THE ORBIFOLD STRESS-ENERGY (with exact delta_m)")
    print("=" * 72)

    print(f"""
  The COMPLETE stress-energy of the KK tower:

  T_tt = sum_m lambda_m |eps_m|^2
       = sum_m [C_1 - f(m) + delta_m] |eps_m|^2

  Using the exact anomaly delta_m = L(m) - S2(m)/4 + c(N):

  T_tt = C_1 * sum|eps|^2 - sum f|eps|^2 + sum [L - S2/4] |eps|^2 + c*sum|eps|^2

  The three contributions:
  1. GRAVITATIONAL: C_1 * N_modes (the bulk, rho-dependent)
  2. KK MASS: -sum f |eps|^2 = -sum m(N-m)/2 (the Casimir)
  3. ORBIFOLD: sum [L(m) - S2(m)/4] |eps|^2 (the fixed-point correction)

  At unit amplitude (|eps_m| = 1 for all m):
""")

    for N in [6, 8, 10, 12]:
        rho = 2.0
        C1 = log(2 * sinh(rho)) + b_exact(N)

        grav = C1 * (N - 1)
        kk_mass = -sum(casimir(m, N) for m in range(1, N))
        orb = sum(weyl_anomaly(m, N) for m in range(1, N))
        total = grav + kk_mass + orb

        # Direct computation
        total_direct = sum(havelock_flat(m, N) + log(2*sinh(rho))
                          for m in range(1, N))

        print(f"  N={N:2d}: grav={grav:8.2f}, KK={kk_mass:8.2f}, "
              f"orb={orb:8.4f}, total={total:8.2f}, "
              f"direct={total_direct:8.2f}, match={abs(total-total_direct)<0.01}")


# =====================================================================
# PART 7: The backreaction equation
# =====================================================================

def backreaction():
    """The backreaction of the KK matter on the geometry.

    The 4D Einstein equation with the COMPLETE matter content
    determines BOTH the spatial geometry AND the polygon size rho.

    The two equations:
    (1) R^{(3)} = const (from the small-ring expansion)
        -> satisfied automatically for the Seifert manifold
    (2) Lambda = 8*pi*G * T_tt (the Hamiltonian constraint)
        -> determines rho as a function of N

    Equation (2) is the BACKREACTION: the matter tells spacetime
    how to curve, and the curvature (through Lambda) determines
    the matter configuration (through rho).
    """
    print(f"\n{'='*72}")
    print("  THE BACKREACTION EQUATION")
    print("=" * 72)

    print(f"""
  The self-consistent equation for rho:

    R^(3)/2 = 8*pi*G * sum_m lambda_m(rho, N)

  Left side: -(1 + N^2/16) [fixed by the Seifert geometry]
  Right side: depends on rho through lambda_m = log(2sinh rho) + ...

  This is ONE equation for ONE unknown (rho), given N.
  The solution rho_eq(N) is the EQUILIBRIUM polygon size.
""")

    print(f"  {'N':>4s} {'Lambda_g':>10s} {'rho_eq':>10s} {'C_1(rho_eq)':>12s} "
          f"{'f_crit':>8s}")

    for N in range(5, 16):
        c = 12 * b_exact(N)
        G = 3 / (2 * c)
        R3 = -2 - N**2 / 8
        Lambda_g = R3 / 2
        target = Lambda_g / (8 * pi * G)  # = T_tt needed

        # T_tt = sum lambda_m(rho) = (N-1)*C_1(rho) - sum f + sum delta
        # = (N-1)*(log(2sinh rho) + b(N)) - N(N^2-1)/12 + 0
        # = (N-1)*log(2sinh rho) + (N-1)*b(N) - N(N^2-1)/12

        b = b_exact(N)
        sum_f = sum(casimir(m, N) for m in range(1, N))  # = N(N^2-1)/12
        const_part = (N - 1) * b - sum_f  # rho-independent part of T_tt

        # Target: (N-1)*log(2sinh rho) + const_part = target
        # log(2sinh rho) = (target - const_part) / (N-1)
        log_2sinh_target = (target - const_part) / (N - 1) if N > 1 else 0

        if log_2sinh_target > -20:
            sinh_rho = exp(log_2sinh_target) / 2
            if sinh_rho > 0:
                rho_eq = np.arcsinh(sinh_rho)
            else:
                rho_eq = float('nan')
        else:
            rho_eq = float('nan')

        C1_eq = log(2 * sinh(rho_eq)) + b if not np.isnan(rho_eq) and rho_eq > 0 else float('nan')
        f_crit = casimir(N // 2, N)

        if not np.isnan(rho_eq):
            print(f"  {N:4d} {Lambda_g:10.4f} {rho_eq:10.4f} "
                  f"{C1_eq:12.4f} {f_crit:8.2f}")
        else:
            print(f"  {N:4d} {Lambda_g:10.4f} {'(none)':>10s} "
                  f"{'':>12s} {f_crit:8.2f}")

    print(f"""
  The backreaction equation determines rho_eq for each N.

  The STABILITY question: is rho_eq above or below the palindromic
  threshold rho*(N)?

  If rho_eq < rho*: the polygon is STABLE at the Einstein equilibrium.
  If rho_eq > rho*: the polygon is UNSTABLE (past the BTZ threshold).
  If rho_eq = rho*: the polygon is MARGINAL (at the horizon).
""")

    # Compare with palindromic thresholds
    print(f"  {'N':>4s} {'rho_eq':>10s} {'rho*':>10s} "
          f"{'rho_eq < rho*?':>16s} {'stability':>12s}")

    for N in range(5, 16):
        c = 12 * b_exact(N)
        G = 3 / (2 * c)
        R3 = -2 - N**2 / 8
        target = R3 / (2 * 8 * pi * G)

        b = b_exact(N)
        sum_f = sum(casimir(m, N) for m in range(1, N))
        const_part = (N - 1) * b - sum_f
        log_target = (target - const_part) / (N - 1) if N > 1 else 0

        if log_target > -20:
            rho_eq = np.arcsinh(exp(log_target) / 2)
        else:
            rho_eq = float('nan')

        # Palindromic threshold
        f_crit = casimir(N // 2, N)
        target_rho_star = f_crit - b
        if target_rho_star > 0:
            rho_star = np.arcsinh(exp(target_rho_star) / 2)
        else:
            rho_star = 0.01

        if not np.isnan(rho_eq):
            is_stable = rho_eq < rho_star
            print(f"  {N:4d} {rho_eq:10.4f} {rho_star:10.4f} "
                  f"{'YES' if is_stable else 'NO':>16s} "
                  f"{'STABLE' if is_stable else 'UNSTABLE':>12s}")
        else:
            print(f"  {N:4d} {'(none)':>10s} {rho_star:10.4f} "
                  f"{'':>16s} {'':>12s}")


# =====================================================================
# MAIN
# =====================================================================

def main():
    print("=" * 72)
    print("  4D EINSTEIN EQUATIONS WITH EXACT ORBIFOLD MATTER")
    print("=" * 72)

    trace_equation()
    mode_by_mode_4d()
    rho_dependent_constraint()
    orbifold_stress_energy()
    backreaction()

    print(f"\n{'='*72}")
    print("  CONCLUSION")
    print("=" * 72)
    print("""
  The 4D Einstein equations on R x (H^2 x_N S^1) with the EXACT
  orbifold matter content give:

  1. The Hamiltonian constraint determines rho_eq(N): the polygon
     size is FIXED by the Einstein equations (not a free parameter).

  2. The stability condition rho_eq vs rho* determines whether the
     gravitationally equilibrium polygon is above or below the
     palindromic threshold.

  3. The COMPLETE matter content includes:
     - The Casimir mass spectrum m(N-m)/2 (the KK tower)
     - The exact Weyl anomaly L(m) - S2(m)/4 (the orbifold correction)
     - The vacuum energy b(N) (the Todd class)

  4. The backreaction closes the system: geometry determines rho,
     rho determines the matter, matter determines geometry.
     This is the SELF-CONSISTENT Einstein equation.
""")


if __name__ == "__main__":
    main()
