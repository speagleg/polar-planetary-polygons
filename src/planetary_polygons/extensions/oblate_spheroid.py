"""
Vortex stability on oblate spheroids.

Critical finding: Saturn's 10% oblateness flips the N=6 hexagon eigenvalue
from λ₃ = -0.12 (unstable on mean sphere) to λ₃ = +0.01 (marginally stable).
The oblateness determines WHETHER the hexagon exists, not just its fine structure.

The analysis proceeds in three levels:
1. Local curvature approximation: use spherical C₁ with local K(φ)
2. Mode coupling: curvature variation δK along the ring couples Fourier modes
3. Critical latitude: the latitude φ_crit where λ₃ changes sign

Key formulas:
    Oblate spheroid: x²/a² + y²/a² + z²/b² = 1  (a > b)
    Gaussian curvature: K(φ) = 1/(M(φ)·N(φ))
    where M = a(1-e²)/(1-e²sin²φ)^{3/2}  (meridional radius)
          N = a/(1-e²sin²φ)^{1/2}          (prime vertical radius)
          e² = 1 - b²/a²                    (eccentricity squared)

    At the pole: K_pole = a²/b⁴ × b² = a²/b² (simplified)
    At the equator: K_eq = b²/a⁴ × a² = b²/a² (simplified)

Run: PYTHONPATH=src python3 -m planetary_polygons.extensions.oblate_spheroid
"""
import numpy as np


def gaussian_curvature(phi, a, b):
    """
    Gaussian curvature K(φ) on an oblate spheroid at geodetic latitude φ.

    Parameters
    ----------
    phi : float or array
        Geodetic latitude in radians.
    a : float
        Equatorial semi-axis (km).
    b : float
        Polar semi-axis (km).

    Returns
    -------
    K : float or array
        Gaussian curvature (km⁻²).
    """
    e2 = 1 - (b / a) ** 2
    s2 = np.sin(phi) ** 2
    M = a * (1 - e2) / (1 - e2 * s2) ** 1.5  # meridional radius
    N_pv = a / (1 - e2 * s2) ** 0.5            # prime vertical radius
    return 1.0 / (M * N_pv)


def curvature_gradient(phi, a, b, dphi=1e-5):
    """
    dK/dφ at latitude φ on the oblate spheroid (numerical).
    """
    K_plus = gaussian_curvature(phi + dphi, a, b)
    K_minus = gaussian_curvature(phi - dphi, a, b)
    return (K_plus - K_minus) / (2 * dphi)


def effective_radius(phi, a, b):
    """Effective radius of curvature R_eff = 1/√K at latitude φ."""
    K = gaussian_curvature(phi, a, b)
    return 1.0 / np.sqrt(K)


def C1_sphere(N, xi):
    """
    C₁ on a sphere: (N-1)(1+ξ²)/(1+ξ)² where ξ = K·R².

    This is the constant-curvature formula used as a local approximation
    on the spheroid.
    """
    return (N - 1) * (1 + xi**2) / (1 + xi)**2


def havelock_eigenvalue_spheroid(N, m, phi, R_ring, a, b):
    """
    Havelock eigenvalue λ_m on an oblate spheroid at latitude φ,
    using the local curvature approximation.

    Parameters
    ----------
    N : int
        Number of vortices.
    m : int
        Fourier mode (1 ≤ m ≤ N-1).
    phi : float
        Geodetic latitude (radians).
    R_ring : float
        Physical ring radius (km).
    a, b : float
        Spheroid semi-axes (km).

    Returns
    -------
    lambda_m : float
        Stability eigenvalue.
    """
    K = gaussian_curvature(phi, a, b)
    xi = K * R_ring ** 2
    C1 = C1_sphere(N, xi)
    f_m = m * (N - m) / 2
    return C1 - f_m


def critical_latitude(N, R_ring, a, b, m=None):
    """
    Find the latitude φ_crit where the binding eigenvalue λ_m changes sign.

    Below φ_crit: the N-gon is unstable on the spheroid.
    Above φ_crit: the N-gon is marginally stable.

    Returns φ_crit in degrees, or None if no transition.
    """
    if m is None:
        m = N // 2

    # Bisection on latitude
    phi_lo = np.radians(0.1)
    phi_hi = np.radians(89.9)

    lam_lo = havelock_eigenvalue_spheroid(N, m, phi_lo, R_ring, a, b)
    lam_hi = havelock_eigenvalue_spheroid(N, m, phi_hi, R_ring, a, b)

    if lam_lo * lam_hi > 0:
        return None  # no sign change

    for _ in range(100):
        phi_mid = (phi_lo + phi_hi) / 2
        lam_mid = havelock_eigenvalue_spheroid(N, m, phi_mid, R_ring, a, b)
        if lam_mid * lam_lo < 0:
            phi_hi = phi_mid
        else:
            phi_lo = phi_mid

    return np.degrees((phi_lo + phi_hi) / 2)


def mode_coupling_strength(N, phi, R_ring, a, b):
    """
    Estimate the mode-coupling amplitude from curvature variation
    along the vortex ring.

    At latitude φ ≠ 90°, the Gaussian curvature varies around the ring:
      K(θ) ≈ K₀ + δK·cos(2θ)
    where δK ∝ (dK/dφ)·(R_ring/R_eff).

    The cos(2θ) term couples modes m and m±2 with amplitude
      coupling ≈ (δK/K₀) · C₁.

    Returns (delta_K_over_K, coupling_amplitude, stability_margin).
    """
    K0 = gaussian_curvature(phi, a, b)
    R_eff = effective_radius(phi, a, b)
    dK = curvature_gradient(phi, a, b)

    # Curvature variation across the ring
    delta_K = abs(dK) * (R_ring / R_eff)
    delta_K_over_K = delta_K / K0

    # Coupling amplitude
    xi = K0 * R_ring ** 2
    C1 = C1_sphere(N, xi)
    coupling = delta_K_over_K * C1

    # Stability margin
    m_bind = N // 2
    f_bind = m_bind * (N - m_bind) / 2
    margin = abs(C1 - f_bind)

    return delta_K_over_K, coupling, margin


def saturn_analysis(R_ring=15000):
    """
    Complete stability analysis for Saturn's hexagon.

    Saturn: a = 60268 km, b = 54364 km, hexagon at ~78°N.
    """
    a, b = 60268.0, 54364.0
    phi_hex = np.radians(78)

    results = {}

    # Critical latitude
    results['phi_crit'] = critical_latitude(6, R_ring, a, b, m=3)

    # Eigenvalue at hexagon latitude
    results['lambda_3_oblate'] = havelock_eigenvalue_spheroid(
        6, 3, phi_hex, R_ring, a, b)

    # Eigenvalue on mean sphere
    R_mean = (2 * a + b) / 3
    K_mean = 1 / R_mean ** 2
    xi_mean = K_mean * R_ring ** 2
    results['lambda_3_sphere'] = C1_sphere(6, xi_mean) - 4.5

    # Mode coupling
    dK_K, coupling, margin = mode_coupling_strength(
        6, phi_hex, R_ring, a, b)
    results['delta_K_over_K'] = dK_K
    results['coupling'] = coupling
    results['margin'] = margin
    results['coupling_exceeds_margin'] = coupling > margin

    # Curvature data
    results['K_local'] = gaussian_curvature(phi_hex, a, b)
    results['K_mean'] = K_mean
    results['R_eff'] = effective_radius(phi_hex, a, b)

    return results


def jupiter_analysis(R_ring_north=5000, R_ring_south=6000):
    """
    Stability analysis for Jupiter's polar vortices.

    Jupiter: a = 71492 km, b = 66854 km.
    North pole: N=8 octagon at ~84°N.
    South pole: N=5 pentagon at ~87°S.
    """
    a, b = 71492.0, 66854.0

    results = {}

    # North pole (N=8)
    phi_north = np.radians(84)
    results['north_lambda_4'] = havelock_eigenvalue_spheroid(
        8, 4, phi_north, R_ring_north, a, b)
    results['north_phi_crit'] = critical_latitude(8, R_ring_north, a, b, m=4)
    dK_K, coupling, margin = mode_coupling_strength(
        8, phi_north, R_ring_north, a, b)
    results['north_coupling'] = coupling
    results['north_margin'] = margin

    # South pole (N=5)
    phi_south = np.radians(87)
    results['south_lambda_2'] = havelock_eigenvalue_spheroid(
        5, 2, phi_south, R_ring_south, a, b)
    dK_K, coupling, margin = mode_coupling_strength(
        5, phi_south, R_ring_south, a, b)
    results['south_coupling'] = coupling
    results['south_margin'] = margin

    return results


if __name__ == '__main__':
    print("=" * 70)
    print("Oblate Spheroid Stability Analysis")
    print("=" * 70)

    # Saturn
    print("\n--- Saturn (a=60268, b=54364, f=0.098) ---")
    sat = saturn_analysis()
    print(f"  Hexagon at 78°N:")
    print(f"    λ₃(oblate) = {sat['lambda_3_oblate']:+.4f}")
    print(f"    λ₃(mean sphere) = {sat['lambda_3_sphere']:+.4f}")
    print(f"    Critical latitude = {sat['phi_crit']:.1f}°")
    print(f"    K_local = {sat['K_local']*1e6:.4f} ×10⁻⁶ km⁻²")
    print(f"    R_eff = {sat['R_eff']:.0f} km")
    print(f"    δK/K along ring = {sat['delta_K_over_K']*100:.2f}%")
    print(f"    Mode coupling amplitude = {sat['coupling']:.4f}")
    print(f"    Stability margin = {sat['margin']:.4f}")
    print(f"    Coupling exceeds margin: {sat['coupling_exceeds_margin']}")

    # Latitude scan
    print(f"\n  Latitude scan (N=6, R=15000 km):")
    a, b = 60268.0, 54364.0
    print(f"  {'φ':>5} {'λ₃':>8} {'stable':>7}")
    for phi_deg in range(60, 91, 2):
        lam = havelock_eigenvalue_spheroid(
            6, 3, np.radians(phi_deg), 15000, a, b)
        print(f"  {phi_deg:5d}° {lam:+8.4f} {'YES' if lam > 0 else 'NO':>7}")

    # Jupiter
    print("\n--- Jupiter (a=71492, b=66854, f=0.065) ---")
    jup = jupiter_analysis()
    print(f"  North (N=8 at 84°N, R=5000 km):")
    print(f"    λ₄ = {jup['north_lambda_4']:+.4f}")
    print(f"    Critical latitude = {jup['north_phi_crit']}")
    print(f"    Coupling/margin = {jup['north_coupling']:.4f}/{jup['north_margin']:.4f}")
    print(f"  South (N=5 at 87°S, R=6000 km):")
    print(f"    λ₂ = {jup['south_lambda_2']:+.4f}")
    print(f"    Coupling/margin = {jup['south_coupling']:.4f}/{jup['south_margin']:.4f}")
