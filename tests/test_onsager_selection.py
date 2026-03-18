"""tests/test_onsager_selection.py"""
import math
from planetary_polygons.extensions.onsager_selection import H_N, H_diff, verify_monotonicity


def test_H_diff_formula_matches_direct():
    """Analytic H_diff should match H_N(N+1) - H_N(N) to machine precision."""
    for r in [0.0, 0.3, 0.5, 0.7, 1.0]:
        for N in range(3, 10):
            for R in [2, 10, 100]:
                direct = H_N(N + 1, R, r) - H_N(N, R, r)
                analytic = H_diff(N, R, r)
                assert abs(direct - analytic) < 1e-10, \
                    f"r={r}, N={N}, R={R}: direct={direct:.12f} != analytic={analytic:.12f}"


def test_monotonicity_for_r_half():
    """H(N+1) > H(N) for r=0.5, R>1 (boundary case)."""
    for N in range(3, 12):
        for R in [1.01, 2, 10, 100]:
            diff = H_diff(N, R, r=0.5)
            assert diff > 0, f"N={N}, R={R}: H_diff={diff:.8f} <= 0 for r=0.5"


def test_monotonicity_for_r_one():
    """H(N+1) > H(N) for r=1.0 (Thomson + center vortex)."""
    for N in range(3, 12):
        for R in [1.01, 5, 1000]:
            diff = H_diff(N, R, r=1.0)
            assert diff > 0, f"N={N}, R={R}: H_diff={diff:.8f} <= 0 for r=1.0"


def test_verify_monotonicity():
    """verify_monotonicity returns True for standard parameters."""
    assert verify_monotonicity(r_min=0.5, r_max=1.0, N_max=10, R_min=1.01, R_max=100)


def test_jupiter_parameters():
    """For Jupiter parameters (r=0.7, R≈10.7), H(8)>H(7) and H(9)>H(8)."""
    r_J = 0.7
    R_J = 7473e3 / 700e3  # R_ring/r_core ≈ 10.7
    assert H_diff(7, R_J, r_J) > 0, "Jupiter: H(8) should be > H(7)"
    assert H_diff(8, R_J, r_J) > 0, "Jupiter: H(9) should be > H(8)"
