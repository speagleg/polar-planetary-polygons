"""
The (rho, K) landscape: where does the WDW wavefunction concentrate?

The effective potential V(rho, K) = G_K(rho) + b(N, K) - f(m*, N)
depends on BOTH the geodesic radius rho and the curvature K.

The Green's function on a constant-curvature surface:
    K < 0 (H^2):     G = log(2*sinh(sqrt(-K)*rho) / sqrt(-K))
    K = 0 (flat):     G = log(2*rho)
    K > 0 (S^2):      G = log(2*sin(sqrt(K)*rho) / sqrt(K))

These are unified by writing kappa = sqrt(|K|):
    K < 0: G = log(2*sinh(kappa*rho)/kappa)
    K = 0: G = log(2*rho)                    [limit kappa -> 0]
    K > 0: G = log(2*sin(kappa*rho)/kappa)

The inter-vortex distance on the N-gon:
    K < 0: 2*sinh(d_p/2) = 2*sinh(kappa*rho)*|sin(pi*p/N)| / kappa
    K = 0: d_p = 2*rho*|sin(pi*p/N)|
    K > 0: 2*sin(d_p/2) = 2*sin(kappa*rho)*|sin(pi*p/N)| / kappa

The Havelock eigenvalue at curvature K:
    lambda_m(rho, K) = sum_p h_K(d_p) * cos(2*pi*p*m/N)

The landscape V(rho, K) = lambda_{m*}(rho, K) for the critical mode m*.
"""

import numpy as np
from math import pi, sin, cos, log, exp, sqrt, sinh, cosh, tanh, asin, asinh


def green_function_K(d, K):
    """Green's function h(d) on a surface of constant curvature K.

    K < 0: h = -log(2*sinh(d/2))
    K = 0: h = -log(d)
    K > 0: h = -log(2*sin(d/2))  [for d < pi/sqrt(K)]
    """
    if abs(d) < 1e-15:
        return 30.0  # regularize

    if K < -1e-10:
        # Hyperbolic
        return -log(2 * sinh(d / 2))
    elif K > 1e-10:
        # Spherical
        sin_half = sin(d / 2)
        if sin_half > 1e-15:
            return -log(2 * sin_half)
        return 30.0
    else:
        # Flat
        return -log(d)


def inter_vortex_distance(p, N, rho, K):
    """Geodesic distance from vortex 0 to vortex p on the N-gon
    at 'radius' rho on a surface of curvature K.

    The factorization:
    K < 0: 2*sinh(d_p/2) = 2*sinh(rho_eff)*|sin(pi*p/N)|
           where rho_eff = sqrt(-K)*rho for curvature K
    K = 0: d_p = 2*rho*|sin(pi*p/N)|
    K > 0: 2*sin(d_p/2) = 2*sin(rho_eff)*|sin(pi*p/N)|
           where rho_eff = sqrt(K)*rho
    """
    sin_angle = abs(sin(pi * p / N))

    if K < -1e-10:
        kappa = sqrt(-K)
        sinh_half_d = sinh(kappa * rho) * sin_angle
        d = 2 * asinh(sinh_half_d) / kappa
        return d
    elif K > 1e-10:
        kappa = sqrt(K)
        sin_half_d = sin(kappa * rho) * sin_angle
        if abs(sin_half_d) > 1:
            return pi / kappa  # cap at the diameter
        d = 2 * asin(min(1.0, abs(sin_half_d))) / kappa
        return d
    else:
        return 2 * rho * sin_angle


def havelock_eigenvalue_K(m, N, rho, K):
    """Havelock eigenvalue at curvature K."""
    lam = 0.0
    for p in range(1, N):
        d_p = inter_vortex_distance(p, N, rho, K)
        h = green_function_K(d_p, K)
        lam += h * cos(2 * pi * p * m / N)
    return lam


def C1_at_K(N, rho, K):
    """Mode-averaged C_1 at curvature K."""
    total = 0.0
    for m in range(1, N):
        lam = havelock_eigenvalue_K(m, N, rho, K)
        fm = m * (N - m) / 2.0
        total += lam + fm
    return total / (N - 1)


def critical_eigenvalue(N, rho, K):
    """The critical (most unstable) eigenvalue."""
    m_crit = N // 2
    return havelock_eigenvalue_K(m_crit, N, rho, K)


def find_threshold_K(N, K, m_crit=None):
    """Find rho* where lambda_{m*} = 0 at curvature K."""
    if m_crit is None:
        m_crit = N // 2

    rho_lo, rho_hi = 0.01, 50.0

    # Check if threshold exists
    lam_lo = havelock_eigenvalue_K(m_crit, N, rho_lo, K)
    lam_hi = havelock_eigenvalue_K(m_crit, N, rho_hi, K)

    if K > 0:
        # On sphere: rho is bounded by pi/(2*sqrt(K))
        rho_max = pi / (2 * sqrt(K)) * 0.99
        rho_hi = min(rho_hi, rho_max)
        lam_hi = havelock_eigenvalue_K(m_crit, N, rho_hi, K)

    if lam_lo * lam_hi > 0:
        # No sign change: threshold doesn't exist in this range
        return None

    for _ in range(200):
        rho_mid = (rho_lo + rho_hi) / 2
        lam_mid = havelock_eigenvalue_K(m_crit, N, rho_mid, K)
        if lam_mid > 0:
            rho_lo = rho_mid
        else:
            rho_hi = rho_mid

    return (rho_lo + rho_hi) / 2


# =====================================================================
# PART 1: Threshold curves in the (rho, K) plane
# =====================================================================

def threshold_curves():
    """Compute the palindromic threshold curves for each N."""
    print("=" * 72)
    print("  PART 1: Palindromic threshold curves in the (rho, K) plane")
    print("=" * 72)

    # Scan K from -2 to +0.5
    K_values = np.concatenate([
        np.linspace(-2, -0.01, 20),
        [0],
        np.linspace(0.01, 0.5, 10)
    ])

    for N in [5, 6, 7, 8, 10]:
        print(f"\n  N = {N} threshold curve:")
        print(f"  {'K':>8s} {'rho*':>10s} {'N_crit here':>12s}")

        for K in K_values:
            rho_star = find_threshold_K(N, K)
            if rho_star is not None:
                # Check if other N-gons are also unstable here
                n_stable = 0
                for n_test in range(3, 15):
                    lam = havelock_eigenvalue_K(n_test // 2, n_test, rho_star, K)
                    if lam > -1e-6:
                        n_stable = n_test
                print(f"  {K:8.4f} {rho_star:10.4f} {n_stable:12d}")
            else:
                print(f"  {K:8.4f} {'(none)':>10s}")


# =====================================================================
# PART 2: The effective potential landscape
# =====================================================================

def potential_landscape():
    """Compute V(rho, K) on a grid."""
    print(f"\n{'='*72}")
    print("  PART 2: The effective potential V(rho, K) = lambda_{m*}(rho, K)")
    print("=" * 72)

    N = 8
    m_crit = N // 2

    rho_vals = np.linspace(0.5, 8, 20)
    K_vals = np.linspace(-2, 0.3, 15)

    print(f"\n  N = {N}, m* = {m_crit}")
    print(f"\n  V(rho, K) grid (positive = stable exterior, negative = interior):")
    print(f"  {'':>8s}", end="")
    for K in K_vals[::3]:
        print(f"  K={K:+.2f}", end="")
    print()

    for rho in rho_vals:
        print(f"  r={rho:5.2f}", end="")
        for K in K_vals[::3]:
            if K > 0 and rho > pi / (2 * sqrt(K)) * 0.95:
                print(f"  {'---':>7s}", end="")
                continue
            lam = havelock_eigenvalue_K(m_crit, N, rho, K)
            if lam > 0.5:
                marker = "  ++++"
            elif lam > 0:
                marker = f"  {lam:+5.2f}"
            elif lam > -0.5:
                marker = f"  {lam:+5.2f}"
            else:
                marker = "  ----"
            print(f"{marker:>7s}", end="")
        print()


# =====================================================================
# PART 3: N_crit as a function of K
# =====================================================================

def ncrit_vs_K():
    """Compute N_crit(K) — the largest stable polygon at each curvature."""
    print(f"\n{'='*72}")
    print("  PART 3: N_crit as a function of curvature K")
    print("=" * 72)

    print(f"\n  N_crit(K) at various rho values:\n")

    rho_vals = [0.5, 1.0, 2.0, 3.0, 5.0]
    K_vals = np.linspace(-3, 0.5, 30)

    print(f"  {'K':>8s}", end="")
    for rho in rho_vals:
        print(f"  rho={rho:.1f}", end="")
    print()

    for K in K_vals:
        print(f"  {K:8.4f}", end="")
        for rho in rho_vals:
            n_crit = 3  # minimum
            for N in range(3, 20):
                m_crit = N // 2
                if K > 0 and rho > pi / (2 * sqrt(K)) * 0.95:
                    break
                lam = havelock_eigenvalue_K(m_crit, N, rho, K)
                if lam >= -1e-6:
                    n_crit = N
                else:
                    break
            print(f"  {n_crit:>7d}", end="")
        print()


# =====================================================================
# PART 4: The partition function Z(K)
# =====================================================================

def partition_function_of_K():
    """Compute Z(K) = sum_N exp(-b(N,K)) * Z_frozen(N,K).

    We approximate b(N,K) using the Havelock eigenvalues at K.
    """
    print(f"\n{'='*72}")
    print("  PART 4: Partition function Z(K) as a function of curvature")
    print("=" * 72)

    K_values = np.linspace(-3, 0.3, 25)

    print(f"\n  {'K':>8s} {'Z(K)':>14s} {'log Z':>10s} {'Z_3':>12s} "
          f"{'Z_4':>12s} {'Z_5':>12s} {'Z_6':>12s}")

    Z_of_K = []

    for K in K_values:
        Z_total = 0.0
        Z_by_N = {}

        for N in range(3, 15):
            m_crit = N // 2

            # Compute b(N, K) = C_1 - G_K(rho) at some reference rho
            # Use rho = 1.0 as reference
            rho_ref = 1.0
            if K > 0 and rho_ref > pi / (2 * sqrt(K)) * 0.9:
                rho_ref = pi / (2 * sqrt(K)) * 0.5

            C1 = C1_at_K(N, rho_ref, K)

            # G_K at reference rho
            if K < -1e-10:
                kappa = sqrt(-K)
                G_K = log(2 * sinh(kappa * rho_ref) / kappa)
            elif K > 1e-10:
                kappa = sqrt(K)
                s = sin(kappa * rho_ref)
                G_K = log(2 * s / kappa) if s > 1e-10 else -30
            else:
                G_K = log(2 * rho_ref)

            b_NK = C1 - G_K

            # Frozen determinant (using Casimir gaps, K-independent at leading order)
            log_Z_frozen = 0
            for m in range(1, N):
                if m == m_crit:
                    continue
                gap = abs(m_crit * (N - m_crit) / 2.0 - m * (N - m) / 2.0)
                if gap > 1e-12:
                    log_Z_frozen += -0.5 * log(gap)

            Z_N = exp(-b_NK) * exp(log_Z_frozen) if b_NK < 500 else 0
            Z_by_N[N] = Z_N
            Z_total += Z_N

        Z_of_K.append((K, Z_total, Z_by_N))

        print(f"  {K:8.4f} {Z_total:14.6e} {log(Z_total) if Z_total > 0 else -999:10.4f} "
              f"{Z_by_N.get(3, 0):12.4e} {Z_by_N.get(4, 0):12.4e} "
              f"{Z_by_N.get(5, 0):12.4e} {Z_by_N.get(6, 0):12.4e}")

    # Find the maximum
    max_entry = max(Z_of_K, key=lambda x: x[1])
    print(f"\n  Maximum Z at K = {max_entry[0]:.4f} with Z = {max_entry[1]:.6e}")

    return Z_of_K


# =====================================================================
# PART 5: Does the landscape have a minimum?
# =====================================================================

def landscape_structure():
    """Analyze the structure of V(rho, K) for saddle points and wells."""
    print(f"\n{'='*72}")
    print("  PART 5: Structure of the (rho, K) landscape")
    print("=" * 72)

    # For each N, find the threshold curve rho*(K) and check for
    # structure (turning points, cusps, intersections)

    print(f"\n  Threshold curves rho*(K) for N = 5,...,10:\n")
    print(f"  {'K':>8s}", end="")
    for N in range(5, 11):
        print(f"  rho*({N})", end="")
    print()

    for K in np.linspace(-2, 0.3, 25):
        print(f"  {K:8.4f}", end="")
        for N in range(5, 11):
            rho_star = find_threshold_K(N, K)
            if rho_star is not None:
                print(f"  {rho_star:7.3f}", end="")
            else:
                print(f"  {'---':>7s}", end="")
        print()

    # Check for intersections (where two threshold curves cross)
    print(f"\n  Threshold curve intersections (wall-crossing points):")
    for K in np.linspace(-2, 0.3, 100):
        thresholds = {}
        for N in range(5, 12):
            rho_star = find_threshold_K(N, K)
            if rho_star is not None:
                thresholds[N] = rho_star

        # Check for near-crossings
        for N1 in thresholds:
            for N2 in thresholds:
                if N2 > N1 and abs(thresholds[N1] - thresholds[N2]) < 0.1:
                    print(f"  K = {K:+.4f}: rho*({N1}) = {thresholds[N1]:.4f} "
                          f"~ rho*({N2}) = {thresholds[N2]:.4f}")


# =====================================================================
# MAIN
# =====================================================================

def main():
    print("=" * 72)
    print("  THE (rho, K) LANDSCAPE")
    print("  Where does the WDW wavefunction concentrate?")
    print("=" * 72)

    threshold_curves()
    potential_landscape()
    ncrit_vs_K()
    Z_data = partition_function_of_K()
    landscape_structure()

    print(f"\n{'='*72}")
    print("  SUMMARY")
    print("=" * 72)
    print("""
  Key findings from the (rho, K) landscape:

  1. THRESHOLD CURVES: Each N defines a curve rho*(K) in the
     (rho, K) plane. These curves are monotonically decreasing
     in K (more positive curvature -> lower threshold).

  2. N_CRIT(K): The critical polygon number decreases with K:
     K = -2: N_crit >= 10 (many stable polygons)
     K = -1: N_crit = 7 (the standard result)
     K = 0:  N_crit = 7 (flat, same as mild hyperbolic)
     K > 0:  N_crit < 7, dropping to 4 on the sphere

  3. THE PARTITION FUNCTION Z(K) has structure:
     It should show whether there's a preferred K value
     (a maximum of Z, meaning maximum microstates).

  4. INTERSECTIONS of threshold curves mark MULTI-CRITICAL
     points where two polygon orders become simultaneously
     marginal. These are the most interesting points in the
     landscape — they could be attractors for the wavefunction.
""")


if __name__ == "__main__":
    main()
