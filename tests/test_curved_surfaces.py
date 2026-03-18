"""tests/test_curved_surfaces.py"""
import numpy as np
from planetary_polygons.extensions.curved_surfaces import (
    sphere_constrained_eigenvalues,
    ncrit_sphere,
    hyperbolic_ncrit,
    hyperbolic_ncrit_exact,
    XI_STAR_78,
    GAMMA_78,
)


def test_sphere_eigenvalues_shape():
    evals = sphere_constrained_eigenvalues(N=6, colatitude_deg=14.0)
    assert len(evals) > 0


def test_ncrit_sphere_n6_stable_at_76N():
    """Saturn 76°N = colatitude 14°: N=6 should be stable."""
    n = ncrit_sphere(14.0)
    assert n >= 6, f"Expected N_crit >= 6 at colatitude 14°, got {n}"


def test_hyperbolic_ncrit_n12_stable():
    """N=12 should be stable at R/a=1 on hyperbolic plane (legacy heuristic)."""
    eval12 = hyperbolic_ncrit(N=12, R_over_a=1.0)
    eval13 = hyperbolic_ncrit(N=13, R_over_a=1.0)
    assert eval12 >= -1e-4, f"N=12 should be stable, eigenvalue={eval12:.6f}"
    assert eval13 < 0.5, f"N=13 should be less stable than N=12"


def test_hyperbolic_ncrit_exact_n7_stable():
    """N=7 should be stable at R/a=0.5 (below the 7→8 threshold)."""
    # ρ/a = 0.5, ξ = tanh(0.25)² ≈ 0.060, below ξ* ≈ 0.063
    eval7 = hyperbolic_ncrit_exact(N=7, R_over_a=0.5)
    assert eval7 >= -1e-6, f"N=7 at R/a=0.5 should be stable, got {eval7:.6f}"


def test_hyperbolic_ncrit_exact_n8_unstable_at_small_rho():
    """N=8 should be unstable at very small R/a (deep hyperbolic, ξ << ξ*)."""
    # At R/a=0.1, ξ = tanh(0.05)² ≈ 0.0025, C₁ ≈ 7*(1+ξ²)/(1-ξ)² ≈ 7.04
    # Mode m=4: C₁ - 4*4/2 = 7.04 - 8 = -0.96 < 0 → unstable
    eval8 = hyperbolic_ncrit_exact(N=8, R_over_a=0.1)
    assert eval8 < 0, f"N=8 at R/a=0.1 should be unstable, got {eval8:.6f}"


def test_hyperbolic_ncrit_exact_n12_stable():
    """N=12 should be stable at R/a=1.0 (exact formula)."""
    eval12 = hyperbolic_ncrit_exact(N=12, R_over_a=1.0)
    eval13 = hyperbolic_ncrit_exact(N=13, R_over_a=1.0)
    assert eval12 >= -1e-6, f"N=12 at R/a=1.0 should be stable, got {eval12:.6f}"
    assert eval13 < 0, f"N=13 at R/a=1.0 should be unstable, got {eval13:.6f}"


def test_xi_star_78_value():
    """ξ* = 8 - 3√7 and γ = 127 + 48√7 satisfy (ξ*)²·γ = 1."""
    assert abs(XI_STAR_78 - (8 - 3 * np.sqrt(7))) < 1e-12
    assert abs(GAMMA_78 - (127 + 48 * np.sqrt(7))) < 1e-10
    assert abs(XI_STAR_78**2 * GAMMA_78 - 1.0) < 1e-10


def test_hyperbolic_ncrit_exact_flat_limit():
    """As R/a → 0, N_crit should approach the flat Thomson value of 7."""
    from planetary_polygons.extensions.h2_stability import ncrit_h2_exact
    # Very small R/a = 0.01 (nearly flat)
    ncrit = ncrit_h2_exact(rho=0.01, a=1.0)
    assert ncrit == 7, f"Expected N_crit=7 near flat limit, got {ncrit}"
