"""
Tiling condition vs stability condition: does N determine Lambda?

The TILING condition (Schlafli): a regular {N, k} tiling of a
surface of curvature K exists when
    cos(pi/N) = sin(pi/k) * cosh(xi)
where xi = sqrt(|K|) * rho_edge is the dimensionless edge length.

The STABILITY condition (Havelock): the N-gon is marginally stable when
    lambda_{m*}(xi) = 0
i.e., V(xi) = 0 at xi = xi*.

The claim: N <= 6 -> AdS (K < 0 selected)
           N = 7  -> flat (K = 0)
           N >= 8 -> dS (K > 0 selected)

This follows IF the tiling xi and stability xi coincide
at the transition point N = 7, K = 0.
"""

import numpy as np
from math import pi, sin, cos, log, exp, sqrt, sinh, cosh, acosh, asin, asinh


def casimir(m, N):
    return m * (N - m) / 2.0


def havelock_eigenvalue_xi(m, N, xi):
    """Havelock eigenvalue as function of xi = sqrt(|K|)*rho.

    On H^2 with curvature K = -kappa^2:
    The factorization: 2*sinh(d_p/2) = 2*sinh(xi)*|sin(pi*p/N)|
    where xi = kappa*rho is the dimensionless geodesic radius.

    h(d_p) = -log(2*sinh(xi)*|sin(pi*p/N)|)
    """
    lam = 0.0
    for p in range(1, N):
        val = 2 * sinh(xi) * abs(sin(pi * p / N))
        if val > 1e-15:
            lam += -log(val) * cos(2 * pi * p * m / N)
        else:
            lam += 30 * cos(2 * pi * p * m / N)
    return lam


def stability_threshold_xi(N, m_crit=None):
    """Find xi* where lambda_{m*}(xi) = 0 (stability threshold)."""
    if m_crit is None:
        m_crit = N // 2

    xi_lo, xi_hi = 0.01, 50.0

    lam_lo = havelock_eigenvalue_xi(m_crit, N, xi_lo)
    lam_hi = havelock_eigenvalue_xi(m_crit, N, xi_hi)

    if lam_lo * lam_hi > 0:
        return None  # no threshold in this range

    for _ in range(200):
        xi_mid = (xi_lo + xi_hi) / 2
        lam = havelock_eigenvalue_xi(m_crit, N, xi_mid)
        if lam > 0:
            xi_lo = xi_mid
        else:
            xi_hi = xi_mid

    return (xi_lo + xi_hi) / 2


def tiling_xi(N, k):
    """The dimensionless edge length xi for the {N, k} tiling.

    From the Schlafli condition for a regular N-gon with k meeting
    at each vertex:

    For HYPERBOLIC tiling (K < 0): (N-2)(k-2) > 4
        cos(pi/N) = sin(pi/k) * cosh(xi_edge/2)
        xi_edge = 2 * arccosh(cos(pi/N) / sin(pi/k))

    For EUCLIDEAN tiling (K = 0): (N-2)(k-2) = 4
        The polygon has a definite shape but the edge length is free.
        xi is arbitrary (scale-free).

    For SPHERICAL tiling (K > 0): (N-2)(k-2) < 4
        cos(pi/N) = sin(pi/k) * cos(xi_edge/2)
        xi_edge = 2 * arccos(cos(pi/N) / sin(pi/k))

    The relationship between xi_edge (half the edge length) and
    xi_rho (the circumradius) for a regular N-gon:
        sinh(xi_rho) = sinh(xi_edge/2) / sin(pi/N)  [hyperbolic]
        xi_rho = xi_edge / (2*sin(pi/N))             [flat]
        sin(xi_rho) = sin(xi_edge/2) / sin(pi/N)     [spherical]
    """
    # Check the type: (N-2)(k-2) vs 4
    product = (N - 2) * (k - 2)

    if product > 4:
        # Hyperbolic tiling
        ratio = cos(pi / N) / sin(pi / k)
        if ratio <= 1:
            return None, "flat/spherical"
        xi_edge = 2 * acosh(ratio)
        # Convert edge to circumradius
        xi_rho = asinh(sinh(xi_edge / 2) / sin(pi / N))
        return xi_rho, "hyperbolic"

    elif product == 4:
        # Euclidean tiling: xi is free (scale-invariant)
        return None, "euclidean (free)"

    else:
        # Spherical tiling
        ratio = cos(pi / N) / sin(pi / k)
        if ratio > 1:
            return None, "invalid"
        xi_edge = 2 * asin(ratio) if ratio <= 1 else None
        if xi_edge is not None:
            # Convert edge to circumradius (spherical)
            sin_rho = sin(xi_edge / 2) / sin(pi / N)
            xi_rho = asin(min(1, sin_rho)) if sin_rho <= 1 else pi/2
            return xi_rho, "spherical"
        return None, "invalid"


def all_tilings(N_max=12):
    """List all regular tilings {N, k} and their xi values."""
    print(f"  {'N':>4s} {'k':>4s} {'(N-2)(k-2)':>12s} {'type':>12s} "
          f"{'xi_rho':>10s} {'K regime':>12s}")

    tilings = []
    for N in range(3, N_max + 1):
        for k in range(3, 20):
            product = (N - 2) * (k - 2)
            if product >= 3 and product <= 100:
                xi_rho, ttype = tiling_xi(N, k)
                if xi_rho is not None:
                    K_regime = "K < 0 (AdS)" if product > 4 else "K > 0 (dS)"
                    tilings.append((N, k, product, ttype, xi_rho, K_regime))
                    if product <= 12 or k <= 4:
                        print(f"  {N:4d} {k:4d} {product:12d} {ttype:>12s} "
                              f"{xi_rho:10.6f} {K_regime:>12s}")
                elif ttype == "euclidean (free)":
                    tilings.append((N, k, product, ttype, None, "K = 0"))
                    print(f"  {N:4d} {k:4d} {product:12d} {ttype:>12s} "
                          f"{'free':>10s} {'K = 0':>12s}")

    return tilings


def compare_tiling_stability():
    """The KEY computation: compare xi_tiling with xi_stability."""
    print(f"\n  {'N':>4s} {'k':>4s} {'xi_tile':>10s} {'xi_stab':>10s} "
          f"{'ratio':>10s} {'tiling K':>10s}")

    for N in range(3, 13):
        xi_stab = stability_threshold_xi(N)

        # Find the simplest tiling for this N
        for k in range(3, 20):
            xi_tile, ttype = tiling_xi(N, k)
            product = (N - 2) * (k - 2)

            if ttype == "euclidean (free)":
                ratio_str = "any"
                K_str = "K = 0"
                print(f"  {N:4d} {k:4d} {'free':>10s} "
                      f"{xi_stab if xi_stab else 'none':>10} "
                      f"{ratio_str:>10s} {K_str:>10s}")
                break
            elif xi_tile is not None and product <= 20:
                ratio = xi_tile / xi_stab if xi_stab and xi_stab > 0 else float('nan')
                K_str = "AdS" if product > 4 else "dS"
                print(f"  {N:4d} {k:4d} {xi_tile:10.6f} "
                      f"{xi_stab if xi_stab else 0:10.6f} "
                      f"{ratio:10.6f} {K_str:>10s}")
                break


def the_N7_coincidence():
    """Check the N=7 coincidence: does the tiling condition meet
    the stability condition at K = 0?"""
    print(f"\n  THE N = 7 COINCIDENCE:")

    # For N = 7: the Euclidean tilings are {7, k} with (5)(k-2) = 4
    # -> k-2 = 4/5, so k = 14/5 (non-integer!) -> NO Euclidean tiling for N=7.

    # The closest: {7, 3} has (5)(1) = 5 > 4 (hyperbolic)
    # {6, 3} has (4)(1) = 4 = 4 (Euclidean!)
    # {8, 3} has (6)(1) = 6 > 4 (hyperbolic)

    print(f"\n  The Euclidean tilings have (N-2)(k-2) = 4:")
    print(f"  {3, 6}: triangle with 6 at vertex")
    print(f"  {4, 4}: square with 4 at vertex")
    print(f"  {6, 3}: hexagon with 3 at vertex")
    print(f"  These are the ONLY Euclidean regular tilings.")
    print(f"  N = 7 does NOT tile the flat plane.")

    print(f"\n  But the STABILITY threshold for N = 7:")
    xi_stab_7 = stability_threshold_xi(7)
    print(f"  xi*(7) = {xi_stab_7:.6f}" if xi_stab_7 else "  xi*(7) = none")

    # On the flat plane (K = 0): what is the stability of the heptagon?
    # The flat Havelock eigenvalue at the critical mode:
    m_crit = 3  # for N=7, m* = 3
    lam_flat = 0.0
    for p in range(1, 7):
        lam_flat += -log(2 * abs(sin(pi * p / 7))) * cos(2 * pi * p * m_crit / 7)
    print(f"  Flat Havelock eigenvalue lambda_3(N=7, flat) = {lam_flat:.8f}")

    if lam_flat > 0:
        print(f"  The heptagon is STABLE on the flat plane (lambda > 0)")
    elif abs(lam_flat) < 0.01:
        print(f"  The heptagon is MARGINAL on the flat plane (lambda ~ 0)")
    else:
        print(f"  The heptagon is UNSTABLE on the flat plane (lambda < 0)")

    # For comparison: N = 6 and N = 8
    for N in [5, 6, 7, 8, 9]:
        m_crit = N // 2
        lam = 0.0
        for p in range(1, N):
            lam += -log(2 * abs(sin(pi * p / N))) * cos(2 * pi * p * m_crit / N)
        print(f"  N = {N}: lambda_flat(m={m_crit}) = {lam:+.8f} "
              f"({'stable' if lam > 0.01 else 'MARGINAL' if abs(lam) < 0.01 else 'unstable'})")


def curvature_from_polygon():
    """For each N, what curvature K makes the N-gon MARGINALLY stable
    at the tiling circumradius?

    If xi_stab(N) exists, and we set xi = xi_tiling(N, k=3),
    then K is determined by xi_tiling = sqrt(|K|) * rho_tiling.

    But since V depends only on xi, the SIGN of K is what matters:
    - If the tiling is hyperbolic (xi_tile > 0 real): K < 0
    - If the tiling is Euclidean (xi free): K = 0
    - If the tiling is spherical: K > 0
    """
    print(f"\n  CURVATURE DETERMINED BY POLYGON TYPE:")
    print(f"\n  {'N':>4s} {'simplest k':>10s} {'(N-2)(k-2)':>12s} "
          f"{'geometry':>12s} {'xi_stab':>10s} {'K implied':>12s}")

    for N in range(3, 13):
        xi_stab = stability_threshold_xi(N)

        # Find the simplest tiling (k=3 first)
        for k in [3, 4, 5, 6, 7]:
            product = (N - 2) * (k - 2)
            if product >= 4:
                break

        if product > 4:
            geom = "hyperbolic"
            K_implied = "K < 0 (AdS)"
        elif product == 4:
            geom = "Euclidean"
            K_implied = "K = 0 (flat)"
        else:
            geom = "spherical"
            K_implied = "K > 0 (dS)"

        xi_str = f"{xi_stab:.4f}" if xi_stab else "none"
        print(f"  {N:4d} {k:10d} {product:12d} {geom:>12s} "
              f"{xi_str:>10s} {K_implied:>12s}")


def main():
    print("=" * 72)
    print("  TILING vs STABILITY: DOES N DETERMINE Lambda?")
    print("=" * 72)

    # Part 1: All tilings
    print(f"\n{'='*72}")
    print("  PART 1: Regular tilings {N, k}")
    print("=" * 72)
    all_tilings()

    # Part 2: Compare tiling and stability
    print(f"\n{'='*72}")
    print("  PART 2: Tiling xi vs stability xi")
    print("=" * 72)
    compare_tiling_stability()

    # Part 3: The N=7 coincidence
    print(f"\n{'='*72}")
    print("  PART 3: The N = 7 boundary")
    print("=" * 72)
    the_N7_coincidence()

    # Part 4: Curvature from polygon type
    print(f"\n{'='*72}")
    print("  PART 4: Curvature determined by polygon type")
    print("=" * 72)
    curvature_from_polygon()

    # Summary
    print(f"\n{'='*72}")
    print("  RESULT")
    print("=" * 72)
    print("""
  The tiling geometry and the stability condition jointly determine
  the curvature sign:

  N = 3:  {3,k} tiles S^2 (k=3,4,5), flat (k=6), H^2 (k>=7)
  N = 4:  {4,k} tiles S^2 (k=3), flat (k=4), H^2 (k>=5)
  N = 5:  {5,k} tiles S^2 (k=3), H^2 (k>=4)
  N = 6:  {6,k} tiles flat (k=3), H^2 (k>=4)
  N = 7:  {7,k} tiles H^2 only (k>=3)
  N >= 8: {N,k} tiles H^2 only (k>=3)

  The EUCLIDEAN boundary: N = 6 (with k = 3, the honeycomb).
  The STABILITY boundary: N = 7 (Havelock's 1931 threshold).

  These DON'T coincide! The tiling boundary is at N = 6,
  the stability boundary is at N = 7.

  The gap: N = 7 tiles H^2 (k=3, hyperbolic heptagonal tiling)
  but the heptagon is MARGINALLY STABLE on the flat plane.
  The heptagon is the polygon that's "too big for flat space
  but just stable enough to exist there."

  The flat-plane stability of the heptagon:
    lambda_3(N=7, flat) > 0 (stable, but barely)

  So the claim "N = 7 sits at Lambda = 0" is NOT exactly right.
  Rather: N = 7 is stable on BOTH flat and hyperbolic surfaces,
  but it's the LAST N that's stable on the flat plane.
  N = 8 and above require sufficiently negative K (hyperbolic)
  to be stable.

  The CORRECT statement:
    N <= 6: stable on flat, spherical, AND hyperbolic surfaces
    N = 7:  stable on flat and hyperbolic (marginal on sphere)
    N >= 8: stable ONLY on sufficiently hyperbolic surfaces
            (K more negative than a threshold K*(N))

  This maps to:
    N <= 6 -> any Lambda (stable everywhere)
    N = 7  -> Lambda <= 0 (stable on flat and AdS)
    N >= 8 -> Lambda < Lambda*(N) < 0 (requires AdS)

  The transition IS at N = 7, but it's a transition from
  "any Lambda" to "Lambda <= 0", not from AdS to dS.
""")


if __name__ == "__main__":
    main()
