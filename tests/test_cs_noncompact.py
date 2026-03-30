"""Tests for well-definedness of CS at irrational level."""
import pytest
from planetary_polygons.proofs.cs_noncompact_welldefined import (
    cs_level, is_irrational, pi3_sl2r, nearest_pole, verify_convergence,
)


def test_pi3_zero():
    """π₃(SL(2,R)) = 0: no topological obstruction."""
    assert pi3_sl2r() == 0


@pytest.mark.parametrize("N", range(3, 16))
def test_level_irrational(N):
    """k = 2b(N) is irrational for all N ≥ 3."""
    assert is_irrational(N)


@pytest.mark.parametrize("N", range(3, 16))
def test_level_positive(N):
    """k = 2b(N) > 0 for all N ≥ 3."""
    assert cs_level(N) > 0


@pytest.mark.parametrize("N", range(3, 16))
def test_convergent_region(N):
    """k = 2b(N) is in the convergent region (k > -h∨ = -2)."""
    conv, k, k_pole = verify_convergence(N)
    assert conv
    assert k > k_pole


def test_nearest_pole():
    """The nearest pole is at k = -h∨(SL(2,R)) = -2."""
    assert nearest_pole() == -2


def test_level_grows():
    """k = 2b(N) grows monotonically with N."""
    prev = cs_level(3)
    for N in range(4, 16):
        curr = cs_level(N)
        assert curr > prev
        prev = curr


def test_N7_level():
    """At N=7: k ≈ 8.60 (well into the convergent region)."""
    k = cs_level(7)
    assert abs(k - 8.596) < 0.01
