# tests/test_riemannian_havelock.py
import numpy as np
from fractions import Fraction
from planetary_polygons.extensions.riemannian_havelock import (
    havelock_sum, havelock_exact, trace_formula_delta,
    C1_hyperbolic, C1_sphere, riemannian_havelock_eigenvalue,
)


def test_havelock_sum_exact():
    for N in range(3, 8):
        for m in range(1, N):
            num = havelock_sum(N, m)
            exact = float(havelock_exact(N, m))
            assert abs(num - exact) < 1e-8, \
                f"N={N}, m={m}: T_m={num:.10f} != exact={exact}"


def test_trace_formula_sphere():
    for N in [4, 6, 8]:
        delta = trace_formula_delta(N, surface='sphere', R=1.0)
        expected = -N / (4 * np.pi)
        assert abs(delta - expected) / abs(expected) < 1e-10


def test_C1_flat_limit():
    """C₁(H², ξ→0) → N-1 (flat-plane limit)."""
    for N in [5, 7, 8]:
        val = C1_hyperbolic(N, 1e-8)
        assert abs(val - (N - 1)) < 1e-5, f"N={N}: C1={val:.8f} != {N-1}"


def test_C1_sphere_flat_limit():
    """C₁(S², ξ→0) → N-1 (flat-plane limit)."""
    for N in [5, 7, 8]:
        val = C1_sphere(N, 1e-8)
        assert abs(val - (N - 1)) < 1e-5, f"N={N}: C1_sphere={val:.8f} != {N-1}"


def test_C1_threshold_N8():
    """C₁(H², ξ*) = 8 defines the 7→8 transition threshold."""
    xi_star = 8 - 3 * np.sqrt(7)
    val = C1_hyperbolic(8, xi_star)
    assert abs(val - 8.0) < 1e-10, f"C1_hyperbolic(8, xi_star) = {val:.12f} != 8"


def test_riemannian_havelock_eigenvalue_flat():
    """In flat limit (ξ→0, r_E=1), eigenvalue ≈ (N-1) - m(N-m)/2."""
    for N in [6, 7, 8]:
        for m in range(1, N // 2 + 1):
            lam = riemannian_havelock_eigenvalue(N, m, xi=1e-8, surface='hyperbolic', r_E=1.0)
            expected = (N - 1) - m * (N - m) / 2
            assert abs(lam - expected) < 1e-4, \
                f"N={N}, m={m}: λ={lam:.6f} != {expected:.6f}"


def test_riemannian_havelock_n7_m3_marginal():
    """On H², N=7 m=3 mode: λ=0 at ξ=0 (flat limit), positive for ξ>0."""
    # Flat limit: C1=6, m(N-m)/2 = 3*4/2 = 6 → λ·r_E² = 0
    lam_flat = riemannian_havelock_eigenvalue(7, 3, xi=1e-8, surface='hyperbolic', r_E=1.0)
    assert abs(lam_flat) < 1e-3, f"N=7 m=3 should be marginal in flat limit, got {lam_flat:.6f}"
    # For ξ > 0: C1 > N-1, so λ > 0 (stabilized by curvature)
    lam_curved = riemannian_havelock_eigenvalue(7, 3, xi=0.05, surface='hyperbolic', r_E=1.0)
    assert lam_curved > 0, f"N=7 m=3 should be stabilized by H² curvature, got {lam_curved:.6f}"
