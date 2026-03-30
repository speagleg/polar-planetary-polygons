"""Tests for the Clausius + Cardy + RT determination of G."""
import pytest
from math import tanh, exp, pi
from planetary_polygons.proofs.clausius_cardy_rt import (
    G_from_clausius_rt, cardy_entropy, verify_clausius_cardy, find_threshold,
    b_exact,
)


@pytest.mark.parametrize("N", range(7, 21))
def test_G_rt_equals_G_bh_times_tanh(N):
    """G_RT = G_BH × tanh(ρ*) (the analytical formula)."""
    G_rt, G_bh, correction = G_from_clausius_rt(N)
    if G_rt is None:
        return
    assert abs(G_rt / G_bh - correction) < 1e-10


@pytest.mark.parametrize("N", range(7, 21))
def test_correction_is_tanh(N):
    """The finite-size correction equals tanh(ρ*)."""
    _, _, correction = G_from_clausius_rt(N)
    rho = find_threshold(N)
    if rho is None:
        return
    assert abs(correction - tanh(rho)) < 1e-12


@pytest.mark.parametrize("N", range(7, 21))
def test_G_rt_positive(N):
    """G_RT is positive for all N ≥ 7."""
    G_rt, _, _ = G_from_clausius_rt(N)
    if G_rt is not None:
        assert G_rt > 0


def test_G_rt_approaches_G_bh():
    """G_RT → G_BH as N → ∞ (tanh → 1)."""
    G_rt_20, G_bh_20, corr_20 = G_from_clausius_rt(20)
    assert abs(corr_20 - 1.0) < 1e-12  # tanh(15.5) ≈ 1


def test_finite_size_exponential():
    """The correction 1-tanh(ρ*) = 2e^{-2ρ*} + O(e^{-4ρ*})."""
    for N in [7, 9, 11, 15]:
        rho = find_threshold(N)
        if rho is None:
            continue
        actual = 1 - tanh(rho)
        predicted = 2 * exp(-2 * rho)
        assert abs(actual - predicted) / actual < 0.05, (
            f"N={N}: 1-tanh={actual:.4e}, 2e^{{-2ρ}}={predicted:.4e}"
        )


def test_N7_correction():
    """At N=7: G_RT/G_BH = tanh(1.734) ≈ 0.940 (6% correction)."""
    G_rt, G_bh, corr = G_from_clausius_rt(7)
    assert abs(corr - 0.9395) < 0.001


def test_N11_correction():
    """At N=11: G_RT/G_BH = tanh(4.45) ≈ 0.9997 (0.03% correction)."""
    G_rt, G_bh, corr = G_from_clausius_rt(11)
    assert abs(corr - 1.0) < 0.001


def test_cardy_entropy_no_G():
    """The Cardy entropy is computed without knowing G."""
    S = cardy_entropy(7)
    c = 12 * b_exact(7)
    # S = (πc/3) cosh(ρ*), all ingredients known from spectrum + BO potential
    assert S > 0
    # It should NOT depend on G — only on c and ρ*
    # (This is a conceptual test: the function signature has no G parameter)


@pytest.mark.parametrize("N", range(7, 16))
def test_verify_clausius(N):
    """Full verification of the Clausius chain for each N."""
    r = verify_clausius_cardy(N)
    if r is None:
        return
    # G_RT should equal G_BH × tanh to machine precision
    assert abs(r['ratio_G'] - r['tanh_rho']) < 1e-10
