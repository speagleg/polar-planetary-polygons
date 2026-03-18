"""tests/test_h2_stability.py"""
import numpy as np
from planetary_polygons.extensions.h2_stability import (
    H_hyp, J_hyp, get_Omega, fourier_eigenvalue, min_eigenvalue,
    ncrit_h2, C1_h2_exact, ncrit_h2_exact, threshold_78_exact,
    ncrit_h2_table, XI_STAR_78, GAMMA_78,
    h2_geodesic_distance, h2_green_identity_residual,
)


def test_constants():
    """ξ* and γ satisfy (ξ*)²γ = 1 exactly."""
    assert abs(XI_STAR_78 - (8 - 3 * np.sqrt(7))) < 1e-12
    assert abs(GAMMA_78 - (127 + 48 * np.sqrt(7))) < 1e-10
    assert abs(XI_STAR_78**2 * GAMMA_78 - 1.0) < 1e-10


def test_threshold_78():
    xi_star, gamma = threshold_78_exact()
    assert abs(xi_star - XI_STAR_78) < 1e-12
    assert abs(gamma - GAMMA_78) < 1e-10


def test_C1_h2_flat_limit():
    """C₁(H², ξ→0) → N-1."""
    for N in [5, 7, 8, 12]:
        val = C1_h2_exact(N, 1e-10)
        assert abs(val - (N - 1)) < 1e-6, f"N={N}: C1={val} != {N-1}"


def test_C1_h2_threshold_N8():
    """C₁(H², ξ*) = 8 exactly (defines the 7→8 threshold)."""
    val = C1_h2_exact(8, XI_STAR_78)
    assert abs(val - 8.0) < 1e-9, f"C1_h2_exact(8, xi*) = {val:.12f} != 8"


def test_ncrit_h2_exact_flat_limit():
    """Near flat limit (small ρ/a), N_crit = 7."""
    ncrit = ncrit_h2_exact(rho=0.01, a=1.0)
    assert ncrit == 7, f"Expected N_crit=7 near flat limit, got {ncrit}"


def test_ncrit_h2_exact_rho1():
    """At ρ/a=1.0, N_crit = 12 (known from numerical sweep)."""
    ncrit = ncrit_h2_exact(rho=1.0, a=1.0)
    assert ncrit == 12, f"Expected N_crit=12 at ρ/a=1.0, got {ncrit}"


def test_ncrit_h2_table():
    """Table function returns dict of ρ → N_crit."""
    rho_vals = [0.3, 1.0, 2.0]
    table = ncrit_h2_table(rho_vals)
    assert set(table.keys()) == set(rho_vals)
    assert table[0.3] == 7
    assert table[1.0] == 12


def test_fourier_eigenvalue_n7_m3_marginal():
    """
    N=7, m=3 at small ρ/a: eigenvalue should be near 0 (marginal in flat limit).
    With H² curvature: should be slightly positive.
    """
    rho = 0.3  # small curvature
    lam = fourier_eigenvalue(3, 7, rho, a=1.0)
    # Should be near 0 but positive (curvature stabilizes)
    assert lam > -1e-4, f"N=7 m=3 should be marginal/stable, got {lam:.6f}"


def test_min_eigenvalue_n8_unstable_flat():
    """N=8 should be unstable at very small ρ/a (near flat, below ξ* threshold)."""
    lam = min_eigenvalue(8, 0.2, a=1.0)
    assert lam < 0, f"N=8 at ρ/a=0.2 should be unstable near flat limit, got {lam:.6f}"


def test_hamiltonian_finite():
    """H_hyp should be finite for well-separated vortices."""
    N = 6
    k = np.arange(N)
    r_E = 0.5
    z = r_E * np.exp(2j * np.pi * k / N)
    H = H_hyp(z.real, z.imag, a=1.0)
    assert np.isfinite(H)


def test_get_Omega_sign():
    """Ω should be negative for standard N-vortex ring (retrograde orbit)."""
    Omega = get_Omega(6, 0.5, 1.0)
    assert Omega < 0, f"Expected Ω < 0, got {Omega:.6f}"


# ── H² Green's function identity tests ───────────────────────────────────────

def test_h2_geodesic_distance_origin():
    """Distance from origin to z = r·e^{iθ} = 2·arctanh(r/a)·a."""
    a = 1.0
    for r in [0.2, 0.5, 0.8]:
        d = h2_geodesic_distance(0.0, r, a)
        expected = 2.0 * a * np.arctanh(r / a)
        assert abs(d - expected) < 1e-12, (
            f"r={r}: d={d:.10f}, expected={expected:.10f}"
        )


def test_h2_geodesic_symmetry():
    """Geodesic distance is symmetric: d(z_j, z_k) = d(z_k, z_j)."""
    z1, z2, a = 0.3 + 0.1j, -0.2 + 0.4j, 1.0
    assert abs(h2_geodesic_distance(z1, z2, a) - h2_geodesic_distance(z2, z1, a)) < 1e-14


def test_h2_green_identity_unit_disk():
    """H_hyp = Σ -ln sinh(d/2) + 0 for a=1 (constant term vanishes)."""
    for N in [4, 6, 7]:
        for rho in [0.3, 0.7, 1.2]:
            residual = h2_green_identity_residual(N, rho, a=1.0)
            assert abs(residual) < 1e-10, (
                f"N={N}, rho={rho}: identity residual = {residual:.2e}"
            )


def test_h2_green_identity_rescaled_disk():
    """Identity holds for a=2.0 (nontrivial constant N(N-1)/2·ln a)."""
    for N in [5, 8]:
        for rho in [0.5, 1.5]:
            residual = h2_green_identity_residual(N, rho, a=2.0)
            assert abs(residual) < 1e-10, (
                f"N={N}, rho={rho}, a=2: identity residual = {residual:.2e}"
            )
