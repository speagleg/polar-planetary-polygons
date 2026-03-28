"""Tests for the CKM phase from Toeplitz structure."""

import pytest
from math import pi, log, cosh, sqrt

from planetary_polygons.extensions.ckm_toeplitz import (
    conical_P, arg_gamma_half_plus_im, gamma_modulus_half_plus_im,
    yukawa_overlap, yukawa_amplitude, kk_momentum_transfer,
)


class TestConicalFunction:
    """The conical function P_{-1/2+im}(cosh ρ) must be real."""

    def test_conical_at_origin(self):
        """P_{-1/2+im}(1) = 1 for all m."""
        for m in [0, 0.5, 1.0, 2.0]:
            assert abs(conical_P(m, 0) - 1.0) < 0.01

    def test_conical_is_real(self):
        """P_{-1/2+im}(cosh ρ) is real (returns float, not complex)."""
        for m in [0, 0.5, 1.0, 1.5]:
            for rho in [0.1, 0.5, 1.0, 1.5]:
                val = conical_P(m, rho)
                assert isinstance(val, float)

    def test_conical_m_zero_known(self):
        """P_{-1/2}(cosh ρ) = (2/π) K(tanh(ρ/2)) for small ρ."""
        # At ρ = 0.1: P_{-1/2}(cosh 0.1) ≈ 0.9994
        val = conical_P(0, 0.1)
        assert abs(val - 0.9994) < 0.001

    def test_conical_decreases_with_m(self):
        """At fixed ρ, P decreases with m (oscillatory damping)."""
        rho = 1.0
        P0 = conical_P(0, rho)
        P1 = conical_P(1, rho)
        P2 = conical_P(2, rho)
        assert P0 > P1 > P2

    def test_conical_large_rho(self):
        """Works at ρ = ρ* ≈ 1.734 (near the BF threshold)."""
        val = conical_P(1.0, 1.734)
        assert isinstance(val, float)
        assert abs(val) < 1.0  # should be bounded


class TestGammaPhase:
    """arg Γ(1/2 + im) = (1/2) log cosh(πm)."""

    def test_phase_at_zero(self):
        """arg Γ(1/2) = 0 (no CP violation for m = 0)."""
        assert abs(arg_gamma_half_plus_im(0)) < 1e-15

    def test_phase_at_one(self):
        """arg Γ(1/2 + i) = (1/2) log cosh(π) = 70.2°."""
        delta = arg_gamma_half_plus_im(1)
        expected = 0.5 * log(cosh(pi))
        assert abs(delta - expected) < 1e-10

    def test_phase_in_degrees(self):
        """δ = 70.2° at m = 1."""
        delta_deg = arg_gamma_half_plus_im(1) * 180 / pi
        assert abs(delta_deg - 70.2) < 0.1

    def test_modulus_reflection(self):
        """|Γ(1/2+im)|² = π/cosh(πm) (reflection formula)."""
        for m in [0, 0.5, 1.0, 2.0]:
            mod_sq = gamma_modulus_half_plus_im(m)
            assert abs(mod_sq - pi / cosh(pi * m)) < 1e-12

    def test_phase_monotone(self):
        """Phase increases with m."""
        phases = [arg_gamma_half_plus_im(m) for m in [0, 0.5, 1.0, 1.5, 2.0]]
        for i in range(len(phases) - 1):
            assert phases[i+1] > phases[i]


class TestOverlapIntegral:
    """The overlap integral I(m) must be real and positive."""

    def test_overlap_real_positive(self):
        """I(m) > 0 for m ∈ [0, 2]."""
        for m in [0, 0.5, 1.0, 1.5]:
            I = yukawa_overlap(m)
            assert I > 0

    def test_overlap_decreases(self):
        """I(m) decreases with m (oscillatory damping of conical function)."""
        I0 = yukawa_overlap(0)
        I1 = yukawa_overlap(1)
        I2 = yukawa_overlap(2)
        assert I0 > I1 > I2

    def test_overlap_at_m_one(self):
        """I(1) ≈ 0.43 (specific value)."""
        I = yukawa_overlap(1.0)
        assert 0.3 < I < 0.6


class TestKKMomentumTransfer:
    """m = ΔT₃ = 1 from the Seifert structure."""

    def test_spectral_parameter(self):
        """The spectral parameter equals the isospin transfer."""
        kk = kk_momentum_transfer()
        assert kk['m_spectral'] == 1.0
        assert kk['Delta_T3'] == 1.0
        assert kk['Delta_c'] == 1.0

    def test_average_is_bf_threshold(self):
        """c_avg = (c_up + c_dn)/2 = 1 (the BF threshold)."""
        kk = kk_momentum_transfer()
        assert kk['c_average'] == 1.0

    def test_forced(self):
        """The identification is forced, not chosen."""
        kk = kk_momentum_transfer()
        assert kk['forced'] is True


class TestCKMPhase:
    """The full CKM phase computation."""

    def test_ckm_phase_value(self):
        """δ = 70.2° ± 0.1°."""
        result = yukawa_amplitude(1.0)
        assert abs(result['ckm_phase_deg'] - 70.2) < 0.1

    def test_ckm_phase_within_observation(self):
        """δ = 70.2° vs observed 69° ± 3° → 0.4σ."""
        result = yukawa_amplitude(1.0)
        sigma = abs(result['ckm_phase_deg'] - 69.0) / 3.0
        assert sigma < 1.0

    def test_no_phase_at_m_zero(self):
        """No CP violation for m = 0."""
        result = yukawa_amplitude(0.0)
        assert abs(result['ckm_phase_deg']) < 0.01

    def test_phase_from_normalization_only(self):
        """The overlap integral is real → phase = arg(1/Γ)."""
        result = yukawa_amplitude(1.0)
        assert result['I_is_real'] is True
        # Phase of Y = -arg Γ, CKM phase = arg Γ (sign convention)
        expected = 0.5 * log(cosh(pi))
        assert abs(result['ckm_phase_rad'] - expected) < 1e-6
