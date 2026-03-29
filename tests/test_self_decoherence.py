"""Tests for the self-decoherence proposition."""
import pytest
from planetary_polygons.proofs.self_decoherence import (
    decoherence_rate,
    decoherence_length,
    verify_strong_decoherence,
)


@pytest.mark.parametrize("N", [5, 7, 9, 11])
def test_strong_decoherence(N):
    """γ >> 1 for all physically relevant N."""
    gamma = decoherence_rate(N, rho=0.5)
    assert gamma > 1, f"N={N}: γ = {gamma} not >> 1"


def test_decoherence_rate_positive():
    """γ > 0 for all N ≥ 4 at generic ρ."""
    for N in range(4, 15):
        gamma = decoherence_rate(N, rho=0.3)
        assert gamma > 0, f"N={N}: γ = {gamma} ≤ 0"


def test_decoherence_length_finite():
    """The coherence length is finite for all N ≥ 4."""
    for N in range(4, 15):
        dl = decoherence_length(N, rho=0.5)
        assert dl < 10, f"N={N}: Δρ = {dl} too large"


def test_strong_decoherence_all():
    """Verify strong decoherence for N=5,7,9,11."""
    results = verify_strong_decoherence()
    for N, r in results.items():
        assert r['strong'], f"N={N}: γ = {r['gamma']} not strong"


def test_gamma_positive_range():
    """γ > 0 across a range of ρ values."""
    for rho in [0.1, 0.3, 0.5, 0.8, 1.0, 1.5]:
        g = decoherence_rate(7, rho=rho)
        assert g > 0, f"rho={rho}: γ = {g} ≤ 0"
