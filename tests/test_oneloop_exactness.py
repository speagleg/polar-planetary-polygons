"""Tests for the one-loop exactness proof."""
import pytest
from planetary_polygons.proofs.oneloop_exactness import (
    oneloop_correction, oneloop_entropy, b_exact,
)


@pytest.mark.parametrize("N", range(7, 16))
def test_correction_is_1_over_c(N):
    """The anharmonic correction is 1/c."""
    r = oneloop_correction(N)
    c = 12 * b_exact(N)
    assert abs(r['correction'] - 1.0 / c) < 1e-12


@pytest.mark.parametrize("N", range(7, 16))
def test_correction_small(N):
    """The correction is < 2% for all N ≥ 7."""
    r = oneloop_correction(N)
    assert r['percent'] < 2.0


def test_correction_decreases():
    """The correction decreases monotonically with N."""
    prev = oneloop_correction(7)['correction']
    for N in range(8, 16):
        curr = oneloop_correction(N)['correction']
        assert curr < prev
        prev = curr


def test_N7_correction():
    """At N=7: 1/c = 1/51.57 ≈ 1.9%."""
    r = oneloop_correction(7)
    assert abs(r['percent'] - 1.94) < 0.1


def test_N11_correction():
    """At N=11: 1/c = 1/126.56 ≈ 0.8%."""
    r = oneloop_correction(11)
    assert abs(r['percent'] - 0.79) < 0.1
