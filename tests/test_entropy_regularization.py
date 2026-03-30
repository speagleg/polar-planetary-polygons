"""Tests for the regularized entropy derivative at palindromic thresholds."""
import pytest
from math import tanh, log
from planetary_polygons.proofs.entropy_regularization import (
    spectral_gaps, spectral_sum, regularized_dS_drho,
    spectral_flow_contribution, find_threshold, casimir,
)


@pytest.mark.parametrize("N", range(7, 16))
def test_spectral_gaps_all_positive(N):
    """All spectral gaps at the threshold are positive."""
    gaps = spectral_gaps(N)
    for m, gap in gaps.items():
        assert gap > 0, f"N={N}, m={m}: gap={gap} <= 0"


@pytest.mark.parametrize("N", range(7, 16))
def test_zero_modes_excluded(N):
    """Zero modes (m* and N-m*) are excluded from the spectral sum."""
    m_crit = N // 2
    gaps = spectral_gaps(N)
    # m* should not appear
    f_crit = casimir(m_crit, N)
    for m, gap in gaps.items():
        assert abs(gap) > 1e-12, f"N={N}, m={m}: zero mode not excluded"


@pytest.mark.parametrize("N", range(7, 16))
def test_spectral_sum_positive(N):
    """The spectral sum σ(N) is positive for all N ≥ 7."""
    sigma = spectral_sum(N)
    assert sigma > 0, f"N={N}: σ = {sigma} <= 0"


def test_spectral_sum_N7():
    """σ(7) = 1/3 + 1 + 1 + 1/3 = 8/3."""
    sigma = spectral_sum(7)
    assert abs(sigma - 8 / 3) < 1e-12


def test_spectral_sum_N8():
    """σ(8) = 2/9 + 1/2 + 2 + 2 + 1/2 + 2/9 = 49/9."""
    sigma = spectral_sum(8)
    assert abs(sigma - 49 / 9) < 1e-12


def test_spectral_sum_N9():
    """σ(9) = 1/6 + 1/3 + 1 + 1 + 1/3 + 1/6 = 3."""
    sigma = spectral_sum(9)
    assert abs(sigma - 3.0) < 1e-12


@pytest.mark.parametrize("N", range(7, 16))
def test_regularized_dS_finite(N):
    """The regularized dS'/dρ is finite at every threshold."""
    dS, sigma, rho_star = regularized_dS_drho(N)
    assert dS is not None, f"N={N}: no threshold"
    assert abs(dS) < 100, f"N={N}: dS = {dS} is too large"


@pytest.mark.parametrize("N", range(7, 16))
def test_regularized_dS_negative(N):
    """dS'/dρ < 0: non-zero-mode entropy decreases as ring expands past ρ*."""
    dS, _, _ = regularized_dS_drho(N)
    if dS is not None:
        assert dS < 0, f"N={N}: dS = {dS} should be negative"


def test_spectral_flow_even_N():
    """Even N: single self-palindromic mode, spectral flow = 1/2."""
    n_cross, sf = spectral_flow_contribution(8)
    assert n_cross == 1
    assert sf == 0.5


def test_spectral_flow_odd_N():
    """Odd N: palindromic pair, spectral flow = 1."""
    n_cross, sf = spectral_flow_contribution(7)
    assert n_cross == 2
    assert sf == 1.0


@pytest.mark.parametrize("N", range(7, 16))
def test_old_value_is_wrong(N):
    """The old dS/dρ = coth(ρ*)/2 does NOT match the derived value."""
    dS_new, sigma, rho_star = regularized_dS_drho(N)
    if dS_new is None:
        return
    coth = 1 / tanh(rho_star)
    old_value = coth / 2
    # The ratio should NOT be 1 (they are different)
    ratio = abs(dS_new / old_value)
    assert ratio > 1.1, f"N={N}: old and new suspiciously close (ratio={ratio})"
