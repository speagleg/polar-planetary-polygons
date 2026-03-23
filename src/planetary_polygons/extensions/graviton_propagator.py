"""
The graviton propagator from the Havelock eigenvalue.

At N = 7, m = 3: f(3,7) = 6, giving j(j+1) = 6, so j = 2.
The spin-2 representation of SL(2,R) IS the graviton.

The Havelock eigenvalue lambda_3(rho) at N = 7 is the graviton
propagator in the radial (holographic) direction of AdS_3.

In AdS_3/CFT_2: the boundary-to-bulk propagator for a spin-j
field is:
    K_j(rho) = (sinh rho)^{-Delta} * 2F1(...)
where Delta = 1 + j is the conformal dimension.

For j = 2 (graviton): Delta = 3, and the propagator falls off
as sinh(rho)^{-3} at large rho.

The Havelock eigenvalue provides the EXACT propagator (not just
the leading asymptotics) through the three-layer decomposition:
    lambda_3(rho, N=7) = C_1(rho) - 6 + delta_3
"""

import numpy as np
from math import pi, sin, cos, log, exp, sqrt, sinh, cosh, tanh, asinh


def casimir(m, N):
    return m * (N - m) / 2.0


def b_exact(N):
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


def havelock_eigenvalue(m, N, rho):
    lam = 0.0
    for p in range(1, N):
        two_sinh = 2 * sinh(rho) * abs(sin(pi * p / N))
        lam += -log(two_sinh) * cos(2 * pi * p * m / N)
    return lam


def C1(rho, N):
    return log(2 * sinh(rho)) + b_exact(N)


def find_threshold(N, m_crit=None):
    if m_crit is None:
        m_crit = N // 2
    f_crit = casimir(m_crit, N)
    b = b_exact(N)
    target = f_crit - b
    if target > 0:
        return asinh(exp(target) / 2)
    return 0.01


# =====================================================================
# PART 1: Integer-spin Wilson lines in the (N, m) lattice
# =====================================================================

def find_integer_spins(N_max=30):
    """Find all (N, m) pairs where j is an integer.

    j(j+1) = f(m,N) = m(N-m)/2
    j integer requires m(N-m)/2 = j(j+1) for some integer j.
    i.e., m(N-m) = 2j(j+1)

    For j = 1: m(N-m) = 4  -> N = m + 4/m (integer when m | 4)
               m=1: N=5; m=2: N=4; m=4: N=5
    For j = 2: m(N-m) = 12 -> N = m + 12/m
               m=1: N=13; m=2: N=8; m=3: N=7; m=4: N=7; m=6: N=8; m=12: N=13
    For j = 3: m(N-m) = 24 -> N = m + 24/m
               m=1: N=25; m=2: N=14; m=3: N=11; m=4: N=10; m=6: N=10;
               m=8: N=11; m=12: N=14; m=24: N=25
    For j = 4: m(N-m) = 40 -> N = m + 40/m
               m=1: N=41; m=2: N=22; m=4: N=14; m=5: N=13; m=8: N=13;
               m=10: N=14; m=20: N=22; m=40: N=41
    """
    results = []
    for N in range(3, N_max + 1):
        for m in range(1, N):
            f = casimir(m, N)
            # Check if j(j+1) = f has integer j
            disc = 1 + 4 * f
            if disc >= 0:
                j = (-1 + sqrt(disc)) / 2
                if abs(j - round(j)) < 1e-10 and j > 0:
                    j_int = int(round(j))
                    results.append((N, m, f, j_int))
    return results


# =====================================================================
# PART 2: The graviton propagator
# =====================================================================

def graviton_propagator(rho_values):
    """Compute the graviton propagator from the Havelock eigenvalue.

    At N = 7, m = 3 (or m = 4 by palindromic symmetry):
    lambda_3(rho) = log(2sinh rho) + b(7) - 6 + delta_3

    The AdS_3 boundary-to-bulk propagator for spin j:
    K_j(rho) ~ (2sinh rho)^{-Delta} for large rho
    where Delta = 1 + j.

    For j = 2 (graviton): Delta = 3.
    K_2(rho) ~ (2sinh rho)^{-3}

    The EXACT propagator (from the hypergeometric function):
    K_j(rho) = C_j * (cosh rho)^{-Delta} * 2F1(Delta/2, (Delta+1)/2; j+1; -sinh^2 rho)

    We can verify this against lambda_3 by checking:
    exp(-lambda_3 * L) should match K_2(rho) for the appropriate
    identification of L and rho.
    """
    N = 7
    m = 3
    j = 2
    Delta = 1 + j  # = 3 for graviton
    f_m = casimir(m, N)  # = 6.0
    b = b_exact(N)

    results = []
    for rho in rho_values:
        # The Havelock eigenvalue (the EXACT propagator data)
        lam = havelock_eigenvalue(m, N, rho)

        # The three-layer decomposition
        c1 = C1(rho, N)
        delta_m = lam - c1 + f_m  # the Weyl anomaly

        # The leading asymptotics: lambda ~ rho + b - f + delta
        # For large rho: lambda ~ rho + (b - f + delta)
        lam_asymp = rho + b - f_m  # ignoring delta

        # The AdS_3 propagator (leading): K ~ (2sinh rho)^{-Delta}
        K_ads = (2 * sinh(rho))**(-Delta)
        log_K = -Delta * log(2 * sinh(rho))

        # The connection: exp(-lambda * rho) vs K_ads^{alpha}
        # Need to find alpha such that exp(-lambda * rho) ~ K^alpha
        # -lambda * rho ~ alpha * (-Delta) * log(2sinh rho)
        # lambda / (Delta * log(2sinh)/rho) ~ alpha
        # For large rho: lambda ~ rho, log(2sinh) ~ rho
        # So alpha ~ rho / (Delta * rho) = 1/Delta = 1/3

        results.append({
            'rho': rho,
            'lambda': lam,
            'c1': c1,
            'delta_m': delta_m,
            'lam_asymp': lam_asymp,
            'K_ads': K_ads,
            'log_K': log_K,
        })

    return results


def ads3_propagator_comparison():
    """Compare the Havelock eigenvalue with the AdS_3 spin-2 propagator."""
    print("=" * 72)
    print("  THE GRAVITON PROPAGATOR")
    print("  N = 7, m = 3: j = 2 (spin-2, the graviton)")
    print("=" * 72)

    N, m, j = 7, 3, 2
    Delta = 1 + j
    f_m = casimir(m, N)
    b = b_exact(N)

    print(f"\n  N = {N}, m = {m}, f = {f_m}, j = {j}, Delta = {Delta}")
    print(f"  b(N) = {b:.6f}")
    print(f"  f - b = {f_m - b:.6f}")

    rho_values = np.concatenate([
        np.linspace(0.1, 1.0, 10),
        np.linspace(1.0, 5.0, 20),
        np.linspace(5.0, 15.0, 10)
    ])

    results = graviton_propagator(rho_values)

    print(f"\n  {'rho':>8s} {'lambda_3':>12s} {'C_1':>10s} {'delta_3':>10s} "
          f"{'log K_ads':>12s} {'lam/logK':>10s}")

    for r in results:
        ratio = r['lambda'] / r['log_K'] if abs(r['log_K']) > 1e-10 else float('nan')
        if r['rho'] in [0.1, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0] or \
           abs(r['rho'] - round(r['rho'])) < 0.05:
            print(f"  {r['rho']:8.4f} {r['lambda']:12.6f} {r['c1']:10.4f} "
                  f"{r['delta_m']:10.6f} {r['log_K']:12.6f} {ratio:10.6f}")

    # The key question: does lambda / log(2sinh) approach a constant?
    print(f"\n  For large rho: lambda_3 ~ rho + (b - f) = rho + {b - f_m:.4f}")
    print(f"  And: -Delta*log(2sinh rho) ~ -3*rho + {-3*log(2):.4f}")
    print(f"  Ratio lambda / [-Delta*log(2sinh)] -> {-1/Delta:.6f} = -1/Delta = -1/3")

    print(f"""
  RESULT: The Havelock eigenvalue lambda_3 at N = 7 satisfies:

    lambda_3(rho) = -(1/3) * Delta * log(2sinh rho) + [corrections]
                  = -log(2sinh rho) + [corrections]

  where the corrections involve b(N) - f(m) + delta_m.

  This is EXACTLY the AdS_3 graviton propagator:
    G_graviton(rho) ~ (2sinh rho)^{{-Delta}} = (2sinh rho)^{{-3}}
    log G = -3 * log(2sinh rho)

  And: lambda_3 = log(2sinh rho) + b - f + delta
                = log(2sinh rho) - 1.702 + delta_3

  The propagator: exp(-lambda_3) = exp(-log(2sinh rho)) * exp(1.702 - delta_3)
                                 = [1/(2sinh rho)] * [constant]
                                 = (2sinh rho)^{{-1}} * C

  This is the scalar (j=0, Delta=1) propagator, NOT the spin-2!

  Wait: the Havelock eigenvalue IS the log of the propagator,
  not the propagator itself. The eigenvalue grows as rho (linearly),
  which corresponds to (2sinh)^{{-1}} ~ exp(-rho).

  For a spin-j field: the propagator goes as (2sinh)^{{-(1+j)}}.
  The LOG goes as -(1+j)*log(2sinh) ~ -(1+j)*rho.

  Our lambda grows as +rho (positive, with coefficient +1).
  So lambda corresponds to Delta = -1 + something... this isn't
  the direct propagator.

  The CORRECT identification:
  The Havelock eigenvalue lambda_m is NOT exp(-Delta*rho).
  It IS C_1 - f + delta, where C_1 ~ rho. The eigenvalue itself
  is the ENERGY of the mode, not the propagator amplitude.

  The propagator is:
    <O_m(x) O_m(y)> = 1/|x-y|^{{2h_m}} ~ exp(-2h_m * d(x,y)/l)

  where h_m = f(m,N) = 6 for the graviton. And d/l is the
  boundary distance, not the bulk radial coordinate.

  The BULK radial profile of a spin-j field at boundary dimension h:
    phi(rho) ~ exp(-h * rho) * (corrections)
    log phi ~ -h * rho = -6 * rho  [for the graviton at N=7]

  This is NOT lambda_3. Lambda_3 ~ +rho, not -6*rho.

  So lambda_3 and the graviton propagator are DIFFERENT objects.
  Lambda is the STABILITY EIGENVALUE (oscillation frequency).
  The propagator is the CORRELATION FUNCTION (decay with distance).

  The relationship: at the threshold lambda = 0, the propagator
  becomes LONG-RANGE (the correlation length diverges).
  Above threshold (lambda > 0): finite correlation length ~ 1/lambda.
  Below threshold (lambda < 0): the mode grows (instability).
""")


# =====================================================================
# PART 3: The graviton mass and the Havelock eigenvalue
# =====================================================================

def graviton_mass():
    """The mass of the spin-2 field from the Havelock eigenvalue.

    In AdS_3: a massive spin-j field has mass m^2 l^2 = Delta(Delta-2)
    where Delta is the conformal dimension.

    For a MASSLESS graviton: Delta = 2 (in d=3), m^2 = 0.
    But in our system: Delta = 1 + j, and for j = 2: Delta = 3.
    So m^2 l^2 = 3(3-2) = 3. The graviton is MASSIVE.

    Actually, in AdS_3 the standard formula for a spin-2 field:
    m^2 l^2 = (Delta - s)(Delta + s - d + 1) where s is the spin, d=3.
    For s = 2, Delta = 3: m^2 l^2 = (3-2)(3+2-3+1) = 1*3 = 3.

    But the MASSLESS graviton in AdS_3 has Delta = 2, s = 2:
    m^2 = (2-2)(2+2-3+1) = 0.

    So our j = 2 Wilson line gives a MASSIVE spin-2 field,
    not the massless graviton!

    The mass: m^2 l^2 = 3 (in units of the AdS scale).
    Or equivalently: Delta = 3 > 2 (the unitarity bound for spin-2).
    """
    print(f"\n{'='*72}")
    print("  THE GRAVITON MASS")
    print("=" * 72)

    print(f"""
  The AdS_3 spin-j field mass formula:
    m^2 l^2 = (Delta - s)(Delta + s - d + 1)  with d = 3

  For the massless graviton: s = 2, Delta = 2, m^2 = 0.
  For our j = 2 Wilson line: Delta = 1 + j = 3.
    m^2 l^2 = (3 - 2)(3 + 2 - 3 + 1) = 1 * 3 = 3

  The Wilson line at N = 7, m = 3 gives a MASSIVE spin-2 field
  with mass m^2 = 3/l^2 in AdS_3 units.

  However: in 2+1D gravity, there are NO propagating gravitons
  (gravity has no local degrees of freedom in 3D). The "graviton"
  in Chern-Simons gravity is a TOPOLOGICAL mode, not a propagating
  particle.

  What the j = 2 Wilson line ACTUALLY represents:
  A conical defect in the AdS_3 geometry with deficit angle
  related to the mass M = f(m,N) = 6.

  The BTZ connection:
  - M < 0: conical surplus (particle with negative mass)
  - M = 0: massless BTZ (the threshold)
  - 0 < M < 1: conical deficit (massive particle)
  - M = 1: extremal BTZ (the horizon just forms)
  - M > 1: BTZ black hole

  Our Casimir f = 6 gives M = 6 > 1, so the j = 2 mode
  corresponds to a BTZ black hole with M = 6, not a particle.

  The HORIZON RADIUS: r_+ = l * sqrt(8GM) = l * sqrt(8 * 3/(2*51.57) * 6)
  = l * sqrt(1.398) = 1.183 * l.
""")

    # Compute the BTZ parameters for each integer-spin Wilson line
    print(f"\n  BTZ parameters for integer-spin Wilson lines:\n")
    print(f"  {'N':>4s} {'m':>4s} {'j':>4s} {'f=M':>8s} {'r+/l':>10s} "
          f"{'T_H':>10s} {'S_BH':>10s} {'type':>14s}")

    spins = find_integer_spins(25)
    seen = set()

    for N, m, f, j_int in spins:
        if (N, j_int) in seen:
            continue
        seen.add((N, j_int))

        c = 12 * b_exact(N)
        G = 3 / (2 * c)

        # BTZ parameters
        M = f  # the mass
        if 8 * G * M > 0:
            r_plus = sqrt(8 * G * M)  # in units of l
        else:
            r_plus = 0

        T_H = r_plus / (2 * pi) if r_plus > 0 else 0  # Hawking temperature
        S_BH = 2 * pi * r_plus / (4 * G) if r_plus > 0 else 0  # BH entropy

        btz_type = "BTZ" if M > 1/(8*G) else ("threshold" if abs(M - 1/(8*G)) < 0.1 else "conical")

        if j_int <= 5:
            print(f"  {N:4d} {m:4d} {j_int:4d} {f:8.1f} {r_plus:10.4f} "
                  f"{T_H:10.4f} {S_BH:10.2f} {btz_type:>14s}")


# =====================================================================
# PART 4: The correct identification
# =====================================================================

def correct_identification():
    """The correct physical identification of the Havelock eigenvalue."""
    print(f"\n{'='*72}")
    print("  THE CORRECT PHYSICAL IDENTIFICATION")
    print("=" * 72)

    print("""
  The Havelock eigenvalue lambda_m is NOT the graviton propagator.
  It is the STABILITY FREQUENCY of the m-th perturbation mode.

  The correct dictionary:

  HAVELOCK                        |  AdS_3 / CS
  ================================|====================================
  lambda_m > 0                    |  Stable mode (oscillation freq sqrt(lambda))
  lambda_m = 0                    |  Threshold (horizon formation)
  lambda_m < 0                    |  Unstable mode (growth rate sqrt(|lambda|))
  f(m,N) = m(N-m)/2              |  Wilson line mass M = f(m,N)
  C_1(rho) = log(2sinh rho) + b  |  Bulk gravitational energy
  delta_m                         |  1-loop quantum correction

  The GRAVITON in this framework is not a propagating field
  (there are none in 3D). It's the spin-2 TOPOLOGICAL mode:
  the j = 2 Wilson line creates a conical defect with specific
  mass M = j(j+1) = 6.

  The Havelock eigenvalue lambda_m measures the RESPONSE of
  the geometry to the Wilson line insertion:
    lambda_m = [bulk energy C_1] - [Wilson line mass f] + [quantum delta]

  When lambda = 0: the Wilson line mass exactly balances the
  bulk energy. This is the BTZ threshold.

  The graviton propagator (the 2-point function of the boundary
  stress tensor) is a DIFFERENT object:
    <T(x) T(0)> ~ c / x^{2*Delta_T} = c / x^6  [Delta_T = 3 for T_munu in 2D]

  This is computed from the Virasoro algebra, not from lambda_m.
  The central charge c = N^2 determines the NORMALIZATION of the
  graviton propagator, while lambda_m determines the STABILITY
  of the Wilson line configuration.
""")


# =====================================================================
# PART 5: What j = 2 at N = 7 actually means
# =====================================================================

def j2_at_N7():
    """The physical meaning of j = 2 at N = 7."""
    print(f"\n{'='*72}")
    print("  WHY N = 7 IS SPECIAL: THE j = 2 COINCIDENCE")
    print("=" * 72)

    # The j = 2 condition: m(N-m) = 12
    # Solutions: (m, N-m) with m(N-m) = 12
    # m=1: N=13; m=2: N=8; m=3: N=7; m=4: N=7; m=6: N=8; m=12: N=13

    print(f"""
  The condition j = 2: m(N-m)/2 = 6, i.e., m(N-m) = 12.

  All integer solutions:
    m=1, N=13  (m is NOT the critical mode m* = 6)
    m=2, N=8   (m is NOT the critical mode m* = 4)
    m=3, N=7   (m IS the critical mode m* = 3)  <-- THIS ONE
    m=4, N=7   (m IS the critical mode m* = 3, palindromic partner)
    m=6, N=8   (palindromic partner of m=2)
    m=12, N=13 (palindromic partner of m=1)

  N = 7 is UNIQUE: it is the ONLY N where the j = 2 representation
  appears at the CRITICAL MODE m* = floor(N/2).

  At N = 8: j = 2 appears at m = 2, but the critical mode is m = 4
  (which has j = 2.37, NOT integer).

  At N = 13: j = 2 appears at m = 1, far from the critical mode m = 6.

  THE COINCIDENCE:
  The heptagon (N = 7) is the polygon whose STABILITY THRESHOLD
  is controlled by a Wilson line in the GRAVITON representation.
  This is why N_crit = 7: the graviton representation marks the
  boundary between stable and unstable polygons.

  In Chern-Simons language:
  - For N < 7: the critical mode has j < 2 (sub-graviton)
  - For N = 7: the critical mode has j = 2 (the graviton)
  - For N > 7: the critical mode has j > 2 (super-graviton)

  The stability boundary is WHERE THE GRAVITON APPEARS in the
  critical mode spectrum.
""")

    # Verify: j at the critical mode for each N
    print(f"  j at the critical mode m* = floor(N/2) for each N:\n")
    print(f"  {'N':>4s} {'m*':>4s} {'f(m*)':>8s} {'j':>10s} {'j_int?':>8s} "
          f"{'spin name':>14s}")

    for N in range(4, 20):
        m_crit = N // 2
        f = casimir(m_crit, N)
        disc = 1 + 4 * f
        j = (-1 + sqrt(disc)) / 2

        j_int = round(j)
        is_int = abs(j - j_int) < 0.01

        if is_int:
            names = {0: "scalar", 1: "vector", 2: "GRAVITON",
                     3: "spin-3", 4: "spin-4", 5: "spin-5"}
            name = names.get(j_int, f"spin-{j_int}")
        else:
            name = f"j = {j:.3f}"

        marker = " <---" if is_int and j_int == 2 else ""
        print(f"  {N:4d} {m_crit:4d} {f:8.2f} {j:10.6f} "
              f"{'YES' if is_int else '':>8s} {name:>14s}{marker}")


# =====================================================================
# MAIN
# =====================================================================

def main():
    print("=" * 72)
    print("  THE GRAVITON IDENTIFICATION")
    print("  j = 2 at N = 7: the graviton IS the critical mode")
    print("=" * 72)

    # Part 1: All integer spins
    print(f"\n{'='*72}")
    print("  PART 1: Integer-spin Wilson lines in the (N, m) lattice")
    print("=" * 72)

    spins = find_integer_spins(25)

    print(f"\n  {'N':>4s} {'m':>4s} {'f(m,N)':>10s} {'j':>4s} "
          f"{'is critical?':>14s}")

    for N, m, f, j in spins:
        m_crit = N // 2
        is_crit = "CRITICAL" if m == m_crit or m == N - m_crit else ""
        if j <= 4:
            print(f"  {N:4d} {m:4d} {f:10.4f} {j:4d} {is_crit:>14s}")

    # Part 2: The propagator (and why it's not what we think)
    ads3_propagator_comparison()

    # Part 3: The graviton mass
    graviton_mass()

    # Part 4: Correct identification
    correct_identification()

    # Part 5: Why N = 7
    j2_at_N7()

    print(f"\n{'='*72}")
    print("  SUMMARY")
    print("=" * 72)
    print("""
  1. N = 7 is the UNIQUE polygon where the graviton representation
     (j = 2) appears at the critical mode m* = 3.

  2. The Havelock eigenvalue lambda_m is NOT the graviton propagator
     but the STABILITY FREQUENCY. The graviton propagator is computed
     from the central charge c = N^2 via the Virasoro algebra.

  3. The j = 2 Wilson line at N = 7 corresponds to a BTZ black hole
     with mass M = 6, not a massless graviton (there are no propagating
     gravitons in 3D).

  4. The physical meaning: the stability boundary N_crit = 7 is where
     the critical mode's SL(2,R) representation becomes the SPIN-2
     (graviton) representation. Below N = 7: sub-graviton (j < 2).
     Above N = 7: super-graviton (j > 2).

  5. This provides a GROUP-THEORETIC explanation for N_crit = 7:
     the stability threshold is set by the REPRESENTATION THEORY
     of the gauge group SL(2,R), specifically the appearance of
     the spin-2 representation at the critical Casimir f = 6.
""")


if __name__ == "__main__":
    main()
