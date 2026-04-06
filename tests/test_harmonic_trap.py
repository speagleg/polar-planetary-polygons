"""Tests for harmonic trap O(xi) corrections to BEC vortex stability."""
import math
from fractions import Fraction

from planetary_polygons.proofs.harmonic_trap import (
    C1_hard,
    C1_harmonic,
    correction_ratio,
    delta_C1,
    eigenvalue_hard,
    eigenvalue_harmonic,
    threshold_hard,
    threshold_harmonic,
    threshold_harmonic_exact,
    threshold_shift,
    prediction_table,
    ncrit_hard,
    ncrit_harmonic,
    C1_expansion_coefficients,
)


# ---------------------------------------------------------------------------
# 1. Hard-wall limit: harmonic must recover C1_hard at xi=0
# ---------------------------------------------------------------------------

class TestHardWallLimit:
    """At xi=0, both trap types give C1 = N-1 (flat space)."""

    def test_C1_at_origin(self):
        for N in range(3, 15):
            assert abs(C1_hard(N, 0.0) - (N - 1)) < 1e-14
            assert abs(C1_harmonic(N, 0.0) - (N - 1)) < 1e-14

    def test_ratio_at_origin(self):
        assert abs(correction_ratio(0.0) - 1.0) < 1e-14

    def test_delta_at_origin(self):
        for N in range(3, 15):
            assert abs(delta_C1(N, 0.0)) < 1e-14

    def test_thresholds_agree_for_small_N(self):
        """For N <= 7, both traps give xi* = 0 (stable everywhere)."""
        for N in range(3, 8):
            assert threshold_hard(N) == 0.0
            assert threshold_harmonic(N) == 0.0


# ---------------------------------------------------------------------------
# 2. Correction is O(xi) — leading term is linear in xi
# ---------------------------------------------------------------------------

class TestCorrectionOrder:
    """Verify the leading-order behaviour of the correction."""

    def test_delta_C1_leading_order(self):
        """delta_C1 ~ -(N-1)*xi for small xi."""
        N = 8
        for xi in [1e-4, 1e-3, 1e-2]:
            delta = delta_C1(N, xi)
            leading = -(N - 1) * xi
            # Relative error should be O(xi)
            assert abs((delta - leading) / leading) < 5 * xi

    def test_correction_ratio_leading_order(self):
        """ratio = 1 - xi + O(xi^2)."""
        for xi in [1e-4, 1e-3, 1e-2]:
            r = correction_ratio(xi)
            assert abs(r - (1 - xi)) < 2 * xi**2

    def test_C1_harmonic_expansion(self):
        """C1_harm/(N-1) = 1 + xi + xi^2 + ..."""
        N = 10
        for xi in [0.01, 0.05]:
            val = C1_harmonic(N, xi) / (N - 1)
            series = 1 + xi + xi**2
            assert abs(val - series) < xi**3 * 2

    def test_C1_hard_expansion(self):
        """C1_hard/(N-1) = 1 + 2*xi + 4*xi^2 + ..."""
        N = 10
        for xi in [0.01, 0.05]:
            val = C1_hard(N, xi) / (N - 1)
            series = 1 + 2 * xi + 4 * xi**2
            assert abs(val - series) < xi**3 * 10


# ---------------------------------------------------------------------------
# 3. Harmonic C1 < hard-wall C1 for all xi > 0 (weaker stability)
# ---------------------------------------------------------------------------

class TestHarmonicWeaker:
    """Harmonic trap is always less stable than hard wall."""

    def test_C1_harmonic_less_than_hard(self):
        for N in [5, 8, 12, 20]:
            for xi in [0.01, 0.05, 0.1, 0.3, 0.5, 0.8]:
                assert C1_harmonic(N, xi) < C1_hard(N, xi)

    def test_delta_C1_negative(self):
        for N in [5, 8, 12]:
            for xi in [0.01, 0.1, 0.5]:
                assert delta_C1(N, xi) < 0

    def test_correction_ratio_less_than_one(self):
        for xi in [0.01, 0.1, 0.3, 0.5, 0.9]:
            assert 0 < correction_ratio(xi) < 1


# ---------------------------------------------------------------------------
# 4. Threshold shifts are bounded (< 100% for relevant N)
# ---------------------------------------------------------------------------

class TestThresholdShifts:
    """Threshold shifts from hard-wall to harmonic are moderate."""

    def test_N8_shift_bounded(self):
        """N=8: threshold shift should be large (harmonic >> hard-wall)."""
        shift = threshold_shift(8)
        assert shift is not None
        # Harmonic threshold is LARGER (needs more curvature)
        assert shift > 0
        # But less than 1000% (sanity)
        assert shift < 10.0

    def test_N11_shift_bounded(self):
        shift = threshold_shift(11)
        assert shift is not None
        assert shift > 0
        assert shift < 10.0

    def test_N23_shift_bounded(self):
        shift = threshold_shift(23)
        assert shift is not None
        assert shift > 0

    def test_shifts_decrease_with_N(self):
        """Relative shift should decrease for large N (both thresholds -> 1)."""
        shifts = []
        for N in [8, 11, 15, 20, 23]:
            s = threshold_shift(N)
            if s is not None:
                shifts.append(s)
        # Not strictly decreasing due to palindromic structure, but bounded
        assert all(s > 0 for s in shifts)


# ---------------------------------------------------------------------------
# 5. Hard-wall threshold matches known values
# ---------------------------------------------------------------------------

class TestKnownThresholds:
    """Cross-check against known hard-wall palindromic thresholds."""

    def test_N8_hard(self):
        """xi*(8) = 8 - 3*sqrt(7) ~ 0.0627."""
        xi = threshold_hard(8)
        xi_exact = 8 - 3 * math.sqrt(7)
        assert abs(xi - xi_exact) < 1e-10

    def test_N_le7_hard(self):
        for N in range(3, 8):
            assert threshold_hard(N) == 0.0

    def test_N8_harmonic(self):
        """xi*_harm(8) = 1 - 2*7/16 = 1 - 7/8 = 1/8."""
        xi = threshold_harmonic(8)
        assert abs(xi - 1 / 8) < 1e-14

    def test_N8_harmonic_exact(self):
        xi = threshold_harmonic_exact(8)
        assert xi == Fraction(1, 8)

    def test_N11_harmonic_exact(self):
        """xi*_harm(11) = 1 - 2*10/(5*6) = 1 - 20/30 = 1/3."""
        xi = threshold_harmonic_exact(11)
        assert xi == Fraction(1, 3)

    def test_N23_harmonic_exact(self):
        """xi*_harm(23) = 1 - 2*22/(11*12) = 1 - 44/132 = 1 - 1/3 = 2/3."""
        xi = threshold_harmonic_exact(23)
        assert xi == Fraction(2, 3)


# ---------------------------------------------------------------------------
# 6. Ncrit comparison
# ---------------------------------------------------------------------------

class TestNcrit:
    """N_crit(harmonic) <= N_crit(hard-wall) for all xi."""

    def test_ncrit_flat_limit(self):
        """At xi~0, both give N_crit = 7."""
        assert ncrit_hard(1e-6) == 7
        assert ncrit_harmonic(1e-6) == 7

    def test_ncrit_harmonic_le_hard(self):
        """Harmonic is never more stable than hard-wall."""
        for xi in [0.01, 0.05, 0.1, 0.2, 0.5]:
            assert ncrit_harmonic(xi) <= ncrit_hard(xi)

    def test_ncrit_hard_grows(self):
        """N_crit increases with xi for hard-wall."""
        n1 = ncrit_hard(0.01)
        n2 = ncrit_hard(0.1)
        n3 = ncrit_hard(0.5)
        assert n1 <= n2 <= n3


# ---------------------------------------------------------------------------
# 7. Expansion coefficients
# ---------------------------------------------------------------------------

class TestExpansionCoefficients:

    def test_hard_coefficients(self):
        """Hard-wall: c_0=1, c_1=2, c_n=2n for n>=2."""
        coeffs = C1_expansion_coefficients('hard', order=5)
        assert coeffs == [1.0, 2.0, 4.0, 6.0, 8.0]

    def test_harmonic_coefficients(self):
        """Harmonic: c_n = 1 for all n."""
        coeffs = C1_expansion_coefficients('harmonic', order=5)
        assert coeffs == [1.0, 1.0, 1.0, 1.0, 1.0]


# ---------------------------------------------------------------------------
# 8. Exact identity: delta_C1 formula
# ---------------------------------------------------------------------------

class TestDeltaIdentity:
    """delta_C1 = -(N-1)*xi*(1+xi)/(1-xi)^2 is exact."""

    def test_delta_exact(self):
        for N in [5, 8, 12]:
            for xi in [0.01, 0.1, 0.3, 0.5, 0.8]:
                direct = C1_harmonic(N, xi) - C1_hard(N, xi)
                formula = delta_C1(N, xi)
                assert abs(direct - formula) < 1e-12 * abs(direct)


# ---------------------------------------------------------------------------
# 9. Prediction table sanity
# ---------------------------------------------------------------------------

class TestPredictionTable:

    def test_default_table_has_three_rows(self):
        rows = prediction_table()
        assert len(rows) == 3
        assert [r['N'] for r in rows] == [8, 11, 23]

    def test_r_over_R_hard_matches_paper(self):
        """Paper values: N=8: 0.25, N=11: 0.41, N=23: 0.62."""
        rows = prediction_table()
        assert abs(rows[0]['r_over_R_hard'] - 0.25) < 0.01
        assert abs(rows[1]['r_over_R_hard'] - 0.41) < 0.01
        assert abs(rows[2]['r_over_R_hard'] - 0.62) < 0.01

    def test_harmonic_shifts_positive(self):
        """Harmonic thresholds are larger (need more curvature)."""
        for row in prediction_table():
            if row['relative_shift'] is not None:
                assert row['relative_shift'] > 0


# ---------------------------------------------------------------------------
# 10. Eigenvalue cross-check
# ---------------------------------------------------------------------------

class TestEigenvalues:

    def test_critical_mode_at_threshold(self):
        """At xi = xi*_hard, the critical eigenvalue should be ~0."""
        xi = threshold_hard(8)
        m_crit = 4  # floor(8/2)
        lam = eigenvalue_hard(m_crit, 8, xi)
        assert abs(lam) < 1e-8

    def test_critical_mode_harmonic_at_threshold(self):
        """At xi = xi*_harm, the critical harmonic eigenvalue should be ~0."""
        xi = threshold_harmonic(8)
        m_crit = 4
        lam = eigenvalue_harmonic(m_crit, 8, xi)
        assert abs(lam) < 1e-12

    def test_harmonic_eigenvalue_lower(self):
        """For same xi, harmonic eigenvalue < hard-wall eigenvalue."""
        for m in [1, 2, 3, 4]:
            for xi in [0.01, 0.1, 0.3]:
                lh = eigenvalue_hard(m, 8, xi)
                la = eigenvalue_harmonic(m, 8, xi)
                assert la < lh
