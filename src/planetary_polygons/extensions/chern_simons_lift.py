"""
The Chern-Simons lift: 2+1D gravity as the bulk of our 2D orbifold CFT.

2+1D gravity with Lambda < 0 is Chern-Simons theory:
    S_CS = (k/4pi) int Tr(A dA + 2/3 A^3)
with gauge group SL(2,R) x SL(2,R) and level k = l/(4G).

The Brown-Henneaux formula: c = 3l/(2G) = 6k + O(1)
Our orbifold gives: c = N^2
Therefore: k = N^2/6 (to leading order)

The vortex polygons are WILSON LINES in the Chern-Simons theory:
    W_m = Tr_R_m P exp(oint A)
where R_m is the SL(2,R) representation with Casimir C_2 = f(m,N) = m(N-m)/2.

The Havelock eigenvalue IS the expectation value of the Wilson line:
    <W_m> = exp(-lambda_m * L)
where L is the length of the Wilson line contour.

The three-layer decomposition:
    lambda_m = C_1 - f(m,N) + delta_m
maps to:
    <W_m> = exp(-(C_1 - f(m) + delta_m) * L)
           = [bulk factor] * [representation factor] * [1-loop factor]
"""

import numpy as np
from math import pi, log, exp, sqrt, sin, cos, sinh, cosh


def casimir(m, N):
    return m * (N - m) / 2.0


def b_exact(N):
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


# =====================================================================
# PART 1: The Chern-Simons parameters from the orbifold
# =====================================================================

def cs_parameters(N):
    """Determine the Chern-Simons level and AdS_3 parameters from N.

    Brown-Henneaux: c = 3l/(2G) where l is the AdS radius and G is
    Newton's constant in 3D.

    Chern-Simons level: k = l/(4G), so c = 6k (at leading order).
    More precisely: c = 6k + O(1) (the O(1) is a quantum correction).

    With c = N^2:
    k = N^2/6 (to leading order)
    or k = (c - 1)/6 (with the quantum shift)

    The AdS radius and Newton's constant:
    l/(4G) = k = N^2/6
    l/G = 2N^2/3

    If we set l = 1 (unit AdS radius):
    G = 3/(2N^2)  [Newton's constant decreases with N]
    """
    c = 12 * b_exact(N)  # exact central charge from our formula
    c_leading = N**2

    # Chern-Simons level
    k_exact = c / 6  # from c = 6k
    k_leading = c_leading / 6

    # AdS parameters (setting l = 1)
    G_newton = 3 / (2 * c)  # G = 3l/(2c) with l = 1
    G_leading = 3 / (2 * c_leading)

    return {
        'N': N,
        'c': c,
        'c_leading': c_leading,
        'k': k_exact,
        'k_leading': k_leading,
        'G': G_newton,
        'G_leading': G_leading,
        'l_over_G': c * 2 / 3,
    }


# =====================================================================
# PART 2: Wilson lines as vortex polygons
# =====================================================================

def wilson_line_representation(m, N):
    """The SL(2,R) representation for the m-th vortex mode.

    In 2+1D Chern-Simons gravity, matter is described by Wilson lines
    in representations R of SL(2,R).

    The representation is labeled by the SL(2,R) Casimir:
    C_2(R_m) = j(j+1) where j is the spin.

    The identification: C_2 = f(m,N) = m(N-m)/2.
    So: j(j+1) = m(N-m)/2

    Solving for j:
    j = (-1 + sqrt(1 + 2m(N-m))) / 2

    For the PRINCIPAL SERIES of SL(2,R):
    j = -1/2 + is (continuous series, s real)
    C_2 = j(j+1) = s^2 + 1/4

    For the DISCRETE SERIES:
    j = n/2 (half-integer)
    C_2 = n(n+2)/4

    Our Casimir f(m,N) = m(N-m)/2:
    For the discrete series: n(n+2)/4 = m(N-m)/2
    -> n(n+2) = 2m(N-m) = 2mN - 2m^2
    -> n = -1 + sqrt(1 + 2mN - 2m^2)
    """
    f_m = casimir(m, N)

    # Solve j(j+1) = f_m
    discriminant = 1 + 4 * f_m
    if discriminant >= 0:
        j = (-1 + sqrt(discriminant)) / 2
    else:
        j = None

    # For the discrete series: n such that n(n+2)/4 = f_m
    # n^2 + 2n - 4f_m = 0 -> n = -1 + sqrt(1 + 4f_m)
    n_discrete = -1 + sqrt(1 + 4 * f_m) if (1 + 4 * f_m) >= 0 else None

    # For the principal series: s^2 + 1/4 = f_m
    # s^2 = f_m - 1/4
    s_principal = sqrt(f_m - 0.25) if f_m >= 0.25 else None

    # The conformal weight h from the Casimir:
    # In the AdS_3/CFT_2 dictionary: h = (1 + sqrt(1 + 4C_2))/2 for heavy operators
    h_heavy = (1 + sqrt(1 + 4 * f_m)) / 2 if (1 + 4 * f_m) >= 0 else None

    return {
        'm': m,
        'f_m': f_m,
        'j': j,
        'n_discrete': n_discrete,
        's_principal': s_principal,
        'h_heavy': h_heavy,
    }


# =====================================================================
# PART 3: The Wilson line expectation value
# =====================================================================

def wilson_line_vev(m, N, rho):
    """The expectation value of the Wilson line.

    In Chern-Simons gravity, the Wilson line along a geodesic of
    length L in representation R_m has:

    <W_m> = exp(-h_m * L / l)  [for the boundary theory]

    where h_m is the conformal weight and l is the AdS radius.

    In our framework:
    <W_m> = exp(-lambda_m * rho)  [the Havelock eigenvalue times radius]

    The identification: lambda_m * rho = h_m * L / l

    Since our lambda_m = C_1(rho) - f(m) + delta_m and
    C_1 ~ rho + b(N) for large rho:

    lambda_m * rho ~ rho^2 + b(N)*rho - f(m)*rho + ...

    The L = rho identification gives h_m = f(m) [at leading order].
    """
    # The Havelock eigenvalue
    lam = 0.0
    for p in range(1, N):
        two_sinh = 2 * sinh(rho) * abs(sin(pi * p / N))
        lam += -log(two_sinh) * cos(2 * pi * p * m / N)

    # The Wilson line VEV
    W = exp(-lam * rho) if lam * rho < 500 else 0

    return lam, W


# =====================================================================
# PART 4: The energy budget in 3D
# =====================================================================

def energy_budget_3d(N):
    """The 3D energy budget from the Chern-Simons lift.

    In 2+1D:
    E_3D = (1/G) * E_2D_normalized

    where E_2D_normalized is the 2D energy in units of 1/l^2.

    The three components:
    E_vacuum = b(N) / G = b(N) * 2c/3 = b(N) * 2N^2/3 + ...
    E_frozen = gaps / G = gaps * 2c/3
    E_casimir = f_crit / G = f_crit * 2c/3

    The RATIOS are preserved:
    E_frozen / E_vacuum = gaps / b(N) (same as 2D)

    But the ABSOLUTE values scale with 1/G ~ c ~ N^2:
    E_3D ~ N^2 * E_2D
    """
    params = cs_parameters(N)
    c = params['c']
    G = params['G']
    m_crit = N // 2
    f_crit = casimir(m_crit, N)
    b = b_exact(N)

    # Casimir gap sum
    gaps = 0
    for m in range(1, N):
        if m == m_crit:
            continue
        gaps += f_crit - casimir(m, N)

    # 3D energies (in units of 1/l)
    E_vac_3d = b / G
    E_frozen_3d = gaps / G
    E_cas_3d = f_crit / G

    # BTZ mass
    # The BTZ black hole in 2+1D has mass M_BTZ = (r_+^2 + r_-^2)/(8Gl^2)
    # At the threshold: the polygon is at the BTZ threshold
    # M_BTZ = 0 (the massless BTZ = the threshold)

    # The Bekenstein-Hawking entropy at the threshold:
    # S_BH = 2*pi*r_+/(4G) = pi*l*sqrt(8GM)/(4G) = ...
    # At M = 0: S = 0 (the threshold has zero entropy classically)
    # The 1-loop correction: S_1loop = -log(Z_frozen)

    return {
        'N': N,
        'c': c,
        'G': G,
        'gaps': gaps,
        'b': b,
        'f_crit': f_crit,
        'E_vac_3d': E_vac_3d,
        'E_frozen_3d': E_frozen_3d,
        'E_cas_3d': E_cas_3d,
        'ratio_frozen_vac': gaps / b,
        'ratio_3comp': (gaps, b, f_crit, gaps + b + f_crit),
    }


# =====================================================================
# PART 5: The BTZ black hole from the palindromic threshold
# =====================================================================

def btz_from_threshold(N):
    """The BTZ black hole parameters at the palindromic threshold.

    At rho = rho*(N): lambda_{m*} = 0 (the threshold).

    In the Chern-Simons description:
    - The polygon phase (rho < rho*) = thermal AdS_3
    - The BTZ phase (rho > rho*) = the BTZ black hole
    - The threshold = the Hawking-Page transition

    The BTZ parameters at the threshold:
    - Mass: M = 0 (the massless BTZ)
    - Horizon radius: r_+ = 0
    - Temperature: T = 0 (zero temperature)
    - Entropy: S_BH = 0 (classically)
    - 1-loop entropy: S = -log(Z_frozen) = log((N-3)!!) - 3(N-2)/4 * log(2)

    The Brown-Henneaux energy:
    E_BH = M - c/24 = -c/24 = -N^2/24  [the Casimir energy of the boundary CFT]
    """
    params = cs_parameters(N)
    c = params['c']
    G = params['G']

    # BTZ parameters
    M_btz = 0  # at the threshold
    r_plus = 0
    T_hawking = 0

    # The Casimir energy (ground state of the boundary CFT)
    E_casimir_cft = -c / 24

    # The 1-loop entropy (from the frozen determinant)
    m_crit = N // 2
    if N % 2 == 0:
        log_Z = 3 * (N - 2) / 4 * log(2)
        k = N - 3
        while k > 0:
            log_Z -= log(k)
            k -= 2
        S_1loop = -log_Z
    else:
        S_1loop = 0  # need different formula for odd N

    # The Cardy entropy (at the threshold, extrapolated)
    # S_Cardy = 2*pi*sqrt(c*h/6) for a primary of weight h
    # At the threshold: h = f(m*) for the matter, so
    S_cardy = 2 * pi * sqrt(c * casimir(m_crit, N) / 6)

    return {
        'N': N,
        'c': c,
        'G': G,
        'M_btz': M_btz,
        'r_plus': r_plus,
        'T_hawking': T_hawking,
        'E_casimir': E_casimir_cft,
        'S_1loop': S_1loop,
        'S_cardy': S_cardy,
    }


# =====================================================================
# MAIN
# =====================================================================

def main():
    print("=" * 72)
    print("  THE CHERN-SIMONS LIFT")
    print("  2+1D gravity as the bulk of the orbifold CFT")
    print("=" * 72)

    # Part 1: CS parameters
    print(f"\n{'='*72}")
    print("  PART 1: Chern-Simons parameters from c = N^2")
    print("=" * 72)

    print(f"\n  Brown-Henneaux: c = 3l/(2G) = 6k + O(1)")
    print(f"  Our orbifold: c = 12*b(N) = N^2 + O(N)\n")

    print(f"  {'N':>4s} {'c=12b':>10s} {'k=c/6':>10s} {'G=3/(2c)':>10s} "
          f"{'l/G':>10s} {'k integer?':>12s}")

    for N in range(4, 16):
        p = cs_parameters(N)
        k_int = round(p['k'])
        is_int = abs(p['k'] - k_int) < 0.5
        print(f"  {N:4d} {p['c']:10.2f} {p['k']:10.4f} {p['G']:10.6f} "
              f"{p['l_over_G']:10.2f} "
              f"{'~' + str(k_int) if is_int else '':>12s}")

    # Part 2: Wilson line representations
    print(f"\n{'='*72}")
    print("  PART 2: Vortex modes as SL(2,R) representations")
    print("=" * 72)

    print(f"\n  The Casimir f(m,N) = m(N-m)/2 determines the SL(2,R) spin j:")
    print(f"  j(j+1) = f(m,N) -> j = (-1 + sqrt(1 + 4f))/2\n")

    print(f"  {'N':>4s} {'m':>4s} {'f(m,N)':>10s} {'j':>10s} "
          f"{'h_heavy':>10s} {'series':>14s}")

    for N in [6, 7, 8, 10]:
        for m in range(1, min(N, 6)):
            w = wilson_line_representation(m, N)
            if w['f_m'] < 0.25:
                series = "light"
            elif w['j'] and w['j'] == int(w['j']):
                series = f"discrete j={int(w['j'])}"
            elif w['s_principal']:
                series = f"principal s={w['s_principal']:.3f}"
            else:
                series = "continuous"

            print(f"  {N:4d} {m:4d} {w['f_m']:10.4f} "
                  f"{w['j']:10.4f} {w['h_heavy']:10.4f} {series:>14s}")

    # Part 3: 3D energy budget
    print(f"\n{'='*72}")
    print("  PART 3: The 3D energy budget")
    print("=" * 72)

    print(f"\n  E_3D = E_2D / G, where G = 3/(2c) = 3/(2N^2)")
    print(f"  Ratios are PRESERVED in the lift.\n")

    print(f"  {'N':>4s} {'G':>10s} {'E_vac/G':>12s} {'E_fr/G':>12s} "
          f"{'E_cas/G':>12s} {'fr/vac':>10s} {'fr/(fr+vac)':>12s}")

    for N in range(6, 16, 2):
        b = energy_budget_3d(N)
        fr_vac = b['ratio_frozen_vac']
        fr_frvac = b['gaps'] / (b['gaps'] + b['b'])
        print(f"  {N:4d} {b['G']:10.6f} {b['E_vac_3d']:12.2f} "
              f"{b['E_frozen_3d']:12.2f} {b['E_cas_3d']:12.2f} "
              f"{fr_vac:10.4f} {fr_frvac:12.6f}")

    print(f"\n  The ratio gaps/(gaps+b) is IDENTICAL in 2D and 3D.")
    print(f"  The lift preserves all energy ratios (1/G cancels).")

    # Part 4: BTZ parameters
    print(f"\n{'='*72}")
    print("  PART 4: BTZ black hole at the palindromic threshold")
    print("=" * 72)

    print(f"\n  {'N':>4s} {'c':>8s} {'G':>10s} {'E_Cas':>10s} "
          f"{'S_1loop':>10s} {'S_Cardy':>10s} {'S_1l/S_C':>10s}")

    for N in range(6, 16, 2):
        btz = btz_from_threshold(N)
        ratio = btz['S_1loop'] / btz['S_cardy'] if btz['S_cardy'] > 0 else 0
        print(f"  {N:4d} {btz['c']:8.2f} {btz['G']:10.6f} "
              f"{btz['E_casimir']:10.2f} {btz['S_1loop']:10.4f} "
              f"{btz['S_cardy']:10.4f} {ratio:10.6f}")

    # Part 5: The complete dictionary
    print(f"\n{'='*72}")
    print("  PART 5: The complete AdS_3/CFT_2 dictionary")
    print("=" * 72)

    print("""
  BULK (AdS_3 Chern-Simons)     |  BOUNDARY (orbifold CFT)
  ==============================|=================================
  Gauge group: SL(2,R) x SL(2,R)|  Virasoro x Virasoro
  Level: k = N^2/6              |  Central charge: c = N^2
  AdS radius: l = 1             |  b(N) = N(N+1)/12 - log2 + ...
  Newton's constant: G = 3/(2c) |  [the coupling]
  Wilson line in R_m             |  Primary operator O_m
    Casimir: j(j+1) = f(m,N)   |    Weight: h_m = m(N-m)/2
    Contour: the N-gon          |    Insertion: the Z_N orbifold
  Flat connection (A = 0)        |  Vacuum state |0>
  BTZ black hole (M > 0)        |  Thermal state at T > 0
  Hawking-Page transition        |  Palindromic threshold
  Geodesic length rho            |  Conformal cross-ratio
  sinh(rho) [exterior]           |  The Havelock kernel h(d)
  cosh(rho) [interior]           |  The JT kernel (fails)
  """)

    # Part 6: The matter coupling
    print(f"{'='*72}")
    print("  PART 6: Matter coupling through Wilson lines")
    print("=" * 72)

    print("""
  The vortex polygon IS a Wilson line network in the CS theory:

  1. Each vortex at position z_p is an endpoint of a Wilson line
     that extends from the boundary into the bulk.

  2. The N vortices of the regular N-gon form an N-pointed star
     graph in the bulk, with all Wilson lines meeting at the
     CENTER of AdS_3 (the bulk point dual to the polygon center).

  3. The Z_N symmetry is the rotational symmetry of this star graph.

  4. The Havelock eigenvalue lambda_m is the HOLONOMY of the
     flat connection around the m-th Wilson line loop.

  5. The palindromic threshold (lambda = 0) is where the
     holonomy becomes TRIVIAL — the Wilson line can be
     contracted to a point. This IS the BTZ threshold
     (the horizon forms when the bulk geometry degenerates).

  6. The frozen determinant Z_frozen is the ONE-LOOP
     partition function of the Chern-Simons theory around
     the flat connection, with the Wilson line insertion.

  The MATTER contribution to the 3D action:
    S_matter = sum_m f(m,N) * (Wilson line length)
             = sum_m [m(N-m)/2] * rho
             = [N(N^2-1)/12] * rho   [the total Casimir]

  This is the SUM OF ALL CASIMIRS times the geodesic radius.
  In the CS theory, this is the total MASS of the Wilson line
  network.
""")

    # Part 7: The quantum gravity partition function in 3D
    print(f"{'='*72}")
    print("  PART 7: The 3D quantum gravity partition function")
    print("=" * 72)

    print("""
  The CS partition function with Wilson lines:

    Z_3D = sum_N Z_CS(N) * Z_Wilson(N)

  where:
    Z_CS(N) = exp(-k * S_0)  [the CS action on the saddle]
            = exp(-N^2/6 * I_grav)

    Z_Wilson(N) = prod_m <W_m>
                = prod_m exp(-lambda_m * rho)
                = exp(-sum_m lambda_m * rho)
                = exp(-(E_frozen + E_critical) * rho)

  At the threshold (E_critical = 0):
    Z_3D(threshold) = exp(-k * S_0) * exp(-E_frozen * rho*)

  The RATIO of the two contributions:
    CS action / Wilson contribution = k * S_0 / (E_frozen * rho*)
    ~ (N^2/6) * O(1) / (N^3/48 * rho*)
    ~ 8/(N * rho*)

  For N = 8, rho* = 2.4: ratio ~ 8/(8*2.4) ~ 0.42
  The CS action and the Wilson contribution are COMPARABLE at
  the palindromic threshold. Neither dominates.

  This is the regime where the full quantum gravity computation
  matters — perturbation theory (in 1/k) is not enough.
""")

    # Compute the ratio for each N
    print(f"  {'N':>4s} {'k':>8s} {'gaps':>8s} {'rho*':>8s} "
          f"{'k/gaps':>8s} {'k/(gaps*rho)':>12s}")

    for N in range(6, 16, 2):
        p = cs_parameters(N)
        k = p['k']
        gaps_val = sum(casimir(N//2, N) - casimir(m, N) for m in range(1, N) if m != N//2)
        f_crit = casimir(N // 2, N)
        b = b_exact(N)
        target = f_crit - b
        rho_star = np.arcsinh(exp(target) / 2) if target > 0 else 1.0

        ratio_simple = k / gaps_val if gaps_val > 0 else 0
        ratio_full = k / (gaps_val * rho_star) if gaps_val * rho_star > 0 else 0

        print(f"  {N:4d} {k:8.2f} {gaps_val:8.1f} {rho_star:8.4f} "
              f"{ratio_simple:8.4f} {ratio_full:12.6f}")


if __name__ == "__main__":
    main()
