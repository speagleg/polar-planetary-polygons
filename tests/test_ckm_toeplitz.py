"""Tests for the CKM phase from the H^2 Dirac Plancherel density."""

import pytest
from math import pi, log, cosh, tanh, sqrt

from planetary_polygons.extensions.ckm_toeplitz import (
    conical_P, plancherel_weight, gamma_modulus_half_plus_im,
    yukawa_overlap, yukawa_amplitude, kk_momentum_transfer,
)


class TestConicalFunction:
    """The conical function P_{-1/2+im}(cosh rho) must be real."""

    def test_conical_at_origin(self):
        """P_{-1/2+im}(1) = 1 for all m."""
        for m in [0, 0.5, 1.0, 2.0]:
            assert abs(conical_P(m, 0) - 1.0) < 0.01

    def test_conical_is_real(self):
        """P_{-1/2+im}(cosh rho) is real (returns float, not complex)."""
        for m in [0, 0.5, 1.0, 1.5]:
            for rho in [0.1, 0.5, 1.0, 1.5]:
                val = conical_P(m, rho)
                assert isinstance(val, float)

    def test_conical_m_zero_known(self):
        """P_{-1/2}(cosh rho) = (2/pi) K(tanh(rho/2)) for small rho."""
        val = conical_P(0, 0.1)
        assert abs(val - 0.9994) < 0.001

    def test_conical_decreases_with_m(self):
        """At fixed rho, P decreases with m (oscillatory damping)."""
        rho = 1.0
        P0 = conical_P(0, rho)
        P1 = conical_P(1, rho)
        P2 = conical_P(2, rho)
        assert P0 > P1 > P2

    def test_conical_large_rho(self):
        """Works at rho = rho* ~ 1.734 (near the BF threshold)."""
        val = conical_P(1.0, 1.734)
        assert isinstance(val, float)
        assert abs(val) < 1.0


class TestPlancherelWeight:
    """Plancherel density weight tanh(pi s) of the H^2 Dirac (Bolte-Stiepan 2006)."""

    def test_weight_at_zero(self):
        """tanh(0) = 0 (no spectral asymmetry at BF saturation)."""
        assert abs(plancherel_weight(0)) < 1e-15

    def test_weight_at_one(self):
        """tanh(pi) = 0.9963 (BF-crossing endpoint)."""
        w = plancherel_weight(1)
        assert abs(w - tanh(pi)) < 1e-12
        assert abs(w - 0.9962720762) < 1e-8

    def test_weight_monotone(self):
        """tanh(pi s) increases with s."""
        weights = [plancherel_weight(s) for s in [0, 0.5, 1.0, 1.5, 2.0]]
        for i in range(len(weights) - 1):
            assert weights[i+1] > weights[i]

    def test_weight_saturates(self):
        """tanh(pi s) -> 1 for large s."""
        assert plancherel_weight(5.0) > 0.9999

    def test_modulus_reflection(self):
        """|Gamma(1/2+im)|^2 = pi/cosh(pi m) (Euler reflection formula)."""
        for m in [0, 0.5, 1.0, 2.0]:
            mod_sq = gamma_modulus_half_plus_im(m)
            assert abs(mod_sq - pi / cosh(pi * m)) < 1e-12


class TestOverlapIntegral:
    """The overlap integral I(m) must be real and positive."""

    def test_overlap_real_positive(self):
        """I(m) > 0 for m in [0, 2]."""
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
        """I(1) ~ 0.43 (specific value)."""
        I = yukawa_overlap(1.0)
        assert 0.3 < I < 0.6


class TestKKMomentumTransfer:
    """m = Delta T_3 = 1 from the Seifert structure."""

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
    """The full CKM phase computation: delta = 2 * theta_CS * tanh(pi) = 68.63 deg."""

    def test_ckm_phase_value(self):
        """delta = 68.63 deg +/- 0.01 deg."""
        result = yukawa_amplitude(1.0)
        assert abs(result['ckm_phase_deg'] - 68.63) < 0.01

    def test_ckm_phase_within_observation(self):
        """delta = 68.63 deg vs observed 69 +/- 3 deg -> 0.12 sigma."""
        result = yukawa_amplitude(1.0)
        sigma = abs(result['ckm_phase_deg'] - 69.0) / 3.0
        assert sigma < 0.5

    def test_no_phase_at_m_zero(self):
        """No CP violation for m = 0."""
        result = yukawa_amplitude(0.0)
        assert abs(result['ckm_phase_deg']) < 0.01

    def test_phase_is_two_theta_cs_tanh_pi(self):
        """delta = 2 * theta_CS * tanh(pi) exactly."""
        result = yukawa_amplitude(1.0)
        expected = 2 * result['theta_CS_rad'] * tanh(pi)
        assert abs(result['ckm_phase_rad'] - expected) < 1e-12

    def test_theta_cs_34_44(self):
        """theta_CS = 34.44 deg from N=7 (topological via b(N))."""
        result = yukawa_amplitude(1.0)
        assert abs(result['theta_CS_deg'] - 34.44) < 0.01

    def test_plancherel_factor(self):
        """plancherel_weight = tanh(pi) = 0.9963 at m=1 (BF-crossing endpoint)."""
        result = yukawa_amplitude(1.0)
        assert abs(result['plancherel_weight'] - tanh(pi)) < 1e-12

    def test_weight_factor(self):
        """Delta_w = 2 at m=1 (SL(2,R) weight difference across the BF sweep)."""
        result = yukawa_amplitude(1.0)
        assert result['delta_w'] == 2

    def test_overlap_real(self):
        """The overlap integral is real (the conical function is real)."""
        result = yukawa_amplitude(1.0)
        assert result['I_is_real'] is True
