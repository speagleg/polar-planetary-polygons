"""Tests for the Jensen O(ε⁴) concavity bound."""
import pytest
from planetary_polygons.proofs.jensen_epsilon4_bound import (
    spectral_sums_at_threshold, concavity_ratio,
)


@pytest.mark.parametrize("N", range(7, 25))
def test_concavity_ratio_exceeds_1(N):
    """The concavity ratio (N-1)σ₂/(32α σ₁) > 1 for all N ≥ 7."""
    ratio = concavity_ratio(N)
    assert ratio > 1.0, f"N={N}: ratio={ratio:.4f} <= 1"


@pytest.mark.parametrize("N", range(7, 25))
def test_concavity_ratio_exceeds_7(N):
    """The ratio exceeds 7 for all N ≥ 7 (strong dominance)."""
    ratio = concavity_ratio(N)
    assert ratio > 7.0, f"N={N}: ratio={ratio:.4f} <= 7"


def test_ratio_N7():
    """At N=7: ratio = 7.50 (the minimum across all N ≥ 7)."""
    ratio = concavity_ratio(7)
    assert abs(ratio - 7.50) < 0.01


@pytest.mark.parametrize("N", range(7, 25))
def test_ratio_monotone_in_even_odd(N):
    """The ratio increases within even-N and odd-N subsequences."""
    if N >= 9:
        ratio_N = concavity_ratio(N)
        ratio_N2 = concavity_ratio(N - 2)
        assert ratio_N >= ratio_N2 - 0.01, (
            f"N={N}: ratio {ratio_N:.2f} < ratio(N-2)={ratio_N2:.2f}"
        )


def test_spectral_sums_N7():
    """σ₁(7) = 8/3, σ₂(7) = 20/9."""
    s1, s2 = spectral_sums_at_threshold(7)
    assert abs(s1 - 8/3) < 1e-12
    assert abs(s2 - 20/9) < 1e-12
