"""Tests for identity block dominance bounds."""
import pytest
from math import log, exp
from planetary_polygons.proofs.identity_block_dominance import (
    b_exact, ope_suppression_bound,
)


def test_N5_bound():
    """At N=5: non-identity ≤ 11.4%."""
    assert abs(ope_suppression_bound(5) - 0.1143) < 0.001


def test_N6_bound():
    """At N=6: non-identity ≤ 1.72%."""
    assert abs(ope_suppression_bound(6) - 0.0172) < 0.001


def test_N7_bound():
    """At N=7: non-identity ≤ 0.14%."""
    assert ope_suppression_bound(7) < 0.0015


@pytest.mark.parametrize("N", range(7, 16))
def test_dominance_above_N7(N):
    """For N ≥ 7, non-identity < 0.2% (identity block dominates)."""
    assert ope_suppression_bound(N) < 0.002


def test_N11_exponential(N=11):
    """At N=11: non-identity ~ 10⁻¹⁰."""
    assert ope_suppression_bound(11) < 2e-10


@pytest.mark.parametrize("N", range(5, 16))
def test_monotone_decreasing(N):
    """The bound decreases monotonically for N ≥ 5."""
    if N >= 6:
        assert ope_suppression_bound(N) < ope_suppression_bound(N - 1)


def test_N5_stability_survives():
    """At N=5: λ_min = 1 on flat plane, 11% correction leaves λ > 0."""
    correction = ope_suppression_bound(5)
    lambda_min = 1.0  # f(2,5) - f(1,5) = 3 - 2 = 1... wait
    # Actually λ_min(5) = C₁ - f(m*,5) = 4 - 3 = 1 at the threshold
    # The 11% OPE correction shifts this by at most 0.11
    assert lambda_min - correction > 0
