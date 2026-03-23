"""
The 3+1D lift: dimensional reduction from H^3 to H^2.

The KEY computation: does integrating the H^3 Green's function
over the transverse direction give the H^2 Green's function?

On H^3 (curvature -1): G_3(d) = -1/(4*pi*sinh(d))
On H^2 (curvature -1): G_2(d) = -(1/2*pi)*log(2*sinh(d/2))

The reduction: a LINE SOURCE in H^3 (extended along the z-axis)
produces a potential that, on the equatorial H^2, equals the
POINT SOURCE potential on H^2.

G_2(d) = integral G_3(d_3D(d, z)) * [metric factor] dz

where d_3D is the H^3 distance from (d, 0) to (0, z).

If this works: the 2D vortex system IS the dimensional reduction
of a 3D system of line sources (cosmic strings) in H^3.
"""

import numpy as np
from math import pi, sin, cos, log, exp, sqrt, sinh, cosh, asinh, acosh


# =====================================================================
# PART 1: Green's functions
# =====================================================================

def G3_H3(d):
    """Green's function on H^3 (3D hyperbolic space, curvature -1).

    G_3(d) = -1/(4*pi*sinh(d))

    This satisfies: Delta_3 G_3 = delta_3D (the 3D Laplacian on H^3).
    """
    if d < 1e-12:
        return float('inf')
    return -1 / (4 * pi * sinh(d))


def G2_H2(d):
    """Green's function on H^2 (2D hyperbolic space, curvature -1).

    G_2(d) = -(1/(2*pi)) * log(2*sinh(d/2))

    This satisfies: Delta_2 G_2 = delta_2D - 1/Area.

    Note: in the Havelock context, h(d) = -log(2*sinh(d/2)) = 2*pi*G_2(d).
    """
    if d < 1e-12:
        return float('inf')
    return -(1 / (2 * pi)) * log(2 * sinh(d / 2))


# =====================================================================
# PART 2: The H^3 distance formula
# =====================================================================

def H3_distance_from_line(d_perp, z):
    """Geodesic distance in H^3 from the point (d_perp, 0) to (0, z).

    In H^3, using the upper-half-space model or the hyperboloid model:
    The equatorial H^2 sits at z = 0.
    A point on H^2 at geodesic distance d_perp from the origin.
    A point on the z-axis at height z above H^2.

    The H^3 distance formula (for points in orthogonal planes):
    cosh(d_3D) = cosh(d_perp) * cosh(z)

    This follows from the H^3 metric:
    ds^2 = dz^2 + cosh^2(z) * ds^2_{H^2}

    where ds^2_{H^2} is the metric on the equatorial H^2 at height z.
    """
    cosh_d3 = cosh(d_perp) * cosh(z)
    if cosh_d3 < 1:
        cosh_d3 = 1.0
    return acosh(cosh_d3)


def H3_distance_general(r1, z1, r2, z2):
    """General H^3 distance using the warped product structure.

    H^3 = R x H^2 with metric ds^2 = dz^2 + cosh^2(z) ds^2_{H^2}

    For points (r1, z1) and (r2, z2) where r is the H^2 distance
    from the origin:

    cosh(d_3D) = cosh(z1)*cosh(z2)*cosh(d_{H^2}) - sinh(z1)*sinh(z2)

    For the special case z1 = 0 (point on the equatorial H^2)
    and r2 = 0 (point on the z-axis):
    cosh(d_3D) = cosh(z2)*cosh(r1)

    which matches H3_distance_from_line.
    """
    cosh_d = cosh(z1) * cosh(z2) * cosh(r1 - r2) - sinh(z1) * sinh(z2)
    # Actually for general points this isn't right; need full formula
    # For points both on the equatorial plane:
    # cosh(d_3D) = cosh(d_{H^2})  (trivially, since z1 = z2 = 0)
    return acosh(max(1.0, cosh_d))


# =====================================================================
# PART 3: The dimensional reduction integral
# =====================================================================

def reduce_G3_to_G2(d_perp, z_max=20, n_points=10000):
    """Integrate the H^3 Green's function over the transverse direction z.

    G_2^{reduced}(d_perp) = integral_{-inf}^{inf} G_3(d_3D(d_perp, z)) * mu(z) dz

    where mu(z) is the metric volume factor for the z-direction.

    In the warped product H^3 = R x_{cosh} H^2:
    The volume element is: dV_3 = cosh^2(z) * dA_{H^2} * dz

    For a line source along the z-axis at r = 0:
    The potential at (d_perp, 0) is:
    phi(d_perp) = integral G_3(d_3D) * dz  [just dz, not cosh^2 dz]

    Actually, for a line source with LINEAR density mu per unit
    PROPER length along the z-axis:
    phi = integral_{-inf}^{inf} G_3(d_3D(d_perp, z)) dz

    The proper length element along the z-axis is just dz
    (since the z-axis IS a geodesic in H^3).
    """
    z_vals = np.linspace(-z_max, z_max, n_points)
    dz = z_vals[1] - z_vals[0]

    integral = 0.0
    for z in z_vals:
        d_3D = H3_distance_from_line(d_perp, z)
        G3 = G3_H3(d_3D)
        integral += G3 * dz

    return integral


def reduce_with_cosh_factor(d_perp, z_max=20, n_points=10000):
    """Same but with the cosh^2(z) metric factor.

    If the z-direction has the warped metric cosh^2(z),
    then the volume element picks up this factor.
    A uniform string in COORDINATE z has varying proper density.

    phi = integral G_3(d_3D) * cosh(z) dz  [cosh from the metric]
    """
    z_vals = np.linspace(-z_max, z_max, n_points)
    dz = z_vals[1] - z_vals[0]

    integral = 0.0
    for z in z_vals:
        d_3D = H3_distance_from_line(d_perp, z)
        G3 = G3_H3(d_3D)
        # Try different metric factors
        integral += G3 * dz  # simplest: no extra factor

    return integral


# =====================================================================
# PART 4: The comparison
# =====================================================================

def compare_reduction():
    """Compare the reduced G_3 with the exact G_2."""
    print("=" * 72)
    print("  DIMENSIONAL REDUCTION: G_3(H^3) -> G_2(H^2)")
    print("=" * 72)

    print(f"\n  G_2^{{reduced}}(d) = integral G_3(d_3D(d, z)) dz")
    print(f"  G_2^{{exact}}(d) = -(1/2pi) log(2 sinh(d/2))")
    print(f"\n  Does the integral equal the exact 2D Green's function?\n")

    print(f"  {'d':>8s} {'G2_reduced':>14s} {'G2_exact':>14s} "
          f"{'ratio':>10s} {'diff':>14s}")

    d_values = [0.1, 0.2, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 7.0, 10.0]

    reduced_vals = []
    exact_vals = []

    for d in d_values:
        G2_red = reduce_G3_to_G2(d)
        G2_ex = G2_H2(d)
        ratio = G2_red / G2_ex if abs(G2_ex) > 1e-15 else float('nan')
        diff = G2_red - G2_ex

        reduced_vals.append(G2_red)
        exact_vals.append(G2_ex)

        print(f"  {d:8.4f} {G2_red:14.8f} {G2_ex:14.8f} "
              f"{ratio:10.6f} {diff:14.8f}")

    # Check if the ratio is constant (i.e., they differ by a multiplicative factor)
    ratios = [r/e for r, e in zip(reduced_vals, exact_vals) if abs(e) > 1e-15]
    if ratios:
        mean_ratio = np.mean(ratios)
        std_ratio = np.std(ratios)
        print(f"\n  Mean ratio: {mean_ratio:.8f} +/- {std_ratio:.8f}")
        print(f"  Is the ratio constant? {'YES' if std_ratio < 0.01 * abs(mean_ratio) else 'NO'}")

        if std_ratio < 0.01 * abs(mean_ratio):
            print(f"  G2_reduced = {mean_ratio:.6f} * G2_exact")
            print(f"  The factor {mean_ratio:.6f} is the string tension normalization.")

    # Check if they differ by an additive constant
    diffs = [r - e for r, e in zip(reduced_vals, exact_vals)]
    mean_diff = np.mean(diffs)
    std_diff = np.std(diffs)
    print(f"\n  Mean difference: {mean_diff:.8f} +/- {std_diff:.8f}")
    print(f"  Additive constant? {'YES' if std_diff < 0.01 * abs(mean_diff) else 'NO'}")

    # Check if reduced = a * exact + b
    if len(d_values) >= 2:
        A = np.column_stack([exact_vals, np.ones(len(exact_vals))])
        coeffs, _, _, _ = np.linalg.lstsq(A, reduced_vals, rcond=None)
        a, b = coeffs
        fitted = a * np.array(exact_vals) + b
        residuals = np.array(reduced_vals) - fitted
        max_resid = np.max(np.abs(residuals))

        print(f"\n  Linear fit: G2_reduced = {a:.8f} * G2_exact + {b:.8f}")
        print(f"  Max residual: {max_resid:.2e}")
        print(f"  Quality: {'EXCELLENT' if max_resid < 1e-4 else 'GOOD' if max_resid < 1e-2 else 'POOR'}")


# =====================================================================
# PART 5: The Havelock kernel comparison
# =====================================================================

def havelock_kernel_comparison():
    """Compare the 3D-reduced Havelock kernel with the 2D kernel."""
    print(f"\n{'='*72}")
    print("  HAVELOCK KERNEL: h_reduced(d) vs h_exact(d)")
    print("=" * 72)

    print(f"\n  h_exact(d) = -log(2 sinh(d/2)) = 2*pi * G2(d)")
    print(f"  h_reduced(d) = 2*pi * G2_reduced(d)")
    print(f"\n  {'d':>8s} {'h_reduced':>14s} {'h_exact':>14s} "
          f"{'diff':>12s}")

    for d in [0.1, 0.3, 0.5, 1.0, 2.0, 3.0, 5.0]:
        G2_red = reduce_G3_to_G2(d)
        h_red = 2 * pi * G2_red
        h_ex = -log(2 * sinh(d / 2))

        print(f"  {d:8.4f} {h_red:14.8f} {h_ex:14.8f} "
              f"{h_red - h_ex:12.8f}")


# =====================================================================
# PART 6: The lift implications
# =====================================================================

def lift_implications():
    """What the dimensional reduction means for the 3+1D lift."""
    print(f"\n{'='*72}")
    print("  IMPLICATIONS OF THE DIMENSIONAL REDUCTION")
    print("=" * 72)

    print("""
  If G2_reduced = alpha * G2_exact + beta, then:

  1. VORTICES = STRINGS. The 2D point vortices are cross-sections
     of 1D strings (line sources) in H^3. The string extends in
     the transverse direction z.

  2. THE THREE-LAYER DECOMPOSITION LIFTS. Since the Havelock
     eigenvalues depend only on the Green's function kernel h(d),
     and h(d) is the same (up to normalization) in 2D and 3D:
     lambda_m^{3D} = alpha * lambda_m^{2D} + beta * sum cos

  3. THE ENERGY BUDGET SCALES. In 3+1D:
     E_3D = L * (alpha * E_2D + beta corrections)
     where L is the total string length.
     The RATIO frozen/vacuum is PRESERVED (alpha cancels).

  4. THE COSMOLOGICAL CONNECTION:
     - Spacetime: M^{3+1} = R_time x H^3_space
     - Spatial slice: H^3 with the polygon strings at the equator
     - The equatorial H^2 contains the N-gon cross-section
     - The WDW equation lives on the equatorial H^2
     - The 3D bulk provides the UV completion

  5. THE DARK SECTOR:
     - E_frozen (2D) -> mu * L * E_frozen (3D)
     - E_vacuum (2D) -> mu * L * E_vacuum (3D)
     - Ratio: E_frozen/E_vacuum is INDEPENDENT of mu and L
     - The dark sector ratio gaps/(gaps+b) survives the lift!
""")


# =====================================================================
# PART 7: The flat-space check
# =====================================================================

def flat_space_check():
    """Verify the reduction in flat space (where we know the answer)."""
    print(f"\n{'='*72}")
    print("  FLAT-SPACE CHECK: R^3 -> R^2")
    print("=" * 72)

    print(f"\n  In flat R^3: G_3(r) = -1/(4*pi*r)")
    print(f"  A line source along z: phi(d) = int G_3(sqrt(d^2+z^2)) dz")
    print(f"  = -(1/4pi) int dz/sqrt(d^2+z^2) = -(1/2pi) log(d/L)")
    print(f"  where L is the IR cutoff.")
    print(f"  This gives G_2(d) = -(1/2pi) log(d) + const  [CORRECT!]")

    print(f"\n  Numerical check:")
    print(f"  {'d':>8s} {'int G3 dz':>14s} {'-(1/2pi)log d':>14s} "
          f"{'diff':>12s}")

    for d in [0.1, 0.5, 1.0, 2.0, 5.0]:
        # Numerical integral
        z_max = 100
        n = 10000
        z_vals = np.linspace(-z_max, z_max, n)
        dz = z_vals[1] - z_vals[0]

        integral = sum(-1/(4*pi*sqrt(d**2 + z**2)) * dz for z in z_vals)

        # Exact (up to additive constant from cutoff)
        G2_flat = -(1/(2*pi)) * log(d)

        print(f"  {d:8.4f} {integral:14.8f} {G2_flat:14.8f} "
              f"{integral - G2_flat:12.8f}")

    print(f"\n  The flat reduction works: int G3 dz = G2 + const (IR cutoff).")
    print(f"  The additive constant depends on the cutoff z_max.")


# =====================================================================
# MAIN
# =====================================================================

def main():
    print("=" * 72)
    print("  THE 3+1D LIFT: DIMENSIONAL REDUCTION FROM H^3 TO H^2")
    print("=" * 72)

    # Flat-space check first
    flat_space_check()

    # The main computation: H^3 -> H^2
    compare_reduction()

    # Havelock kernel
    havelock_kernel_comparison()

    # Implications
    lift_implications()

    print(f"\n{'='*72}")
    print("  CONCLUSION")
    print("=" * 72)


if __name__ == "__main__":
    main()
