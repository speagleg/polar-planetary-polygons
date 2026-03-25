"""Tests for CKM mixing from the Havelock Yukawa texture."""

import numpy as np
import pytest
from planetary_polygons.extensions.ckm_mixing import ckm_matrix, yukawa_texture


class TestYukawaTexture:
    def test_4_zeros(self):
        t = yukawa_texture()
        assert np.sum(t == 0) == 4

    def test_5_nonzero(self):
        t = yukawa_texture()
        assert np.sum(t == 1) == 5


class TestCKMStructure:
    def test_near_diagonal(self):
        assert ckm_matrix()['is_near_diagonal']

    def test_hierarchical(self):
        assert ckm_matrix()['is_hierarchical']

    def test_unitary(self):
        ckm = ckm_matrix()
        VdV = ckm['V_complex'].conj().T @ ckm['V_complex']
        np.testing.assert_allclose(VdV, np.eye(3), atol=1e-10)

    def test_cabibbo_angle(self):
        assert 10 < ckm_matrix()['theta_C_deg'] < 18

    def test_V_us_order(self):
        assert 0.15 < ckm_matrix()['V_us'] < 0.35

    def test_V_ub_smallest(self):
        ckm = ckm_matrix()
        assert ckm['V_ub'] < ckm['V_cb'] < ckm['V_us']


class TestCPViolation:
    def test_jarlskog_nonzero(self):
        """J ≠ 0: CP violation exists from the CS instanton."""
        assert abs(ckm_matrix()['J']) > 1e-6

    def test_jarlskog_order_of_magnitude(self):
        """J within factor 2 of observed 3 × 10⁻⁵."""
        J = abs(ckm_matrix()['J'])
        assert 1.5e-5 < J < 6e-5

    def test_jarlskog_from_localization(self):
        """J = 3.5 × 10⁻⁵ from localization-dependent CS phase."""
        J = abs(ckm_matrix()['J'])
        assert abs(J - 3.5e-5) / 3.5e-5 < 0.15  # within 15%

    def test_delta_if_vcb_correct(self):
        """With observed mixing angles and J_obs, delta ≈ 65° (obs 69°)."""
        ckm = ckm_matrix()
        assert 55 < ckm['delta_if_Vcb_correct'] < 80

    def test_j_near_maximal(self):
        """Model J is close to J_max for observed angles (near-maximal CP)."""
        ckm = ckm_matrix()
        # J_model / J_max(obs) ≈ 1.06 means sin δ ≈ 1 → near-maximal
        assert 0.8 < ckm['J_ratio_to_max'] < 1.3

    def test_sin_delta_positive(self):
        """sin delta > 0: correct CP sign from CS instanton."""
        assert ckm_matrix()['sin_delta'] > 0


class TestEtaInvariantPhase:
    """Tests for delta = 2*theta_CS * tanh(pi) from the APS eta invariant."""

    def test_delta_matches_observed(self):
        """delta = 68.63 deg matches observed 69 +/- 3 deg."""
        from planetary_polygons.extensions.ckm_mixing import eta_invariant_phase
        r = eta_invariant_phase()
        assert abs(r['delta_deg'] - 69) < 3  # within 1 sigma

    def test_bf_crossing_dominates(self):
        """Gen 3 mode 3 (BF crossing) contributes > 90% of eta difference."""
        from planetary_polygons.extensions.ckm_mixing import eta_invariant_phase
        r = eta_invariant_phase()
        assert r['bf_fraction'] > 0.90

    def test_j_consistency(self):
        """Predicted J from eta invariant delta matches observed J to 10%."""
        from planetary_polygons.extensions.ckm_mixing import eta_invariant_phase
        r = eta_invariant_phase()
        assert abs(r['J_predicted'] - 3.0e-5) / 3.0e-5 < 0.10

    def test_theta_cs_from_n7(self):
        """theta_CS = 34.44 deg, determined by N=7."""
        from planetary_polygons.extensions.ckm_mixing import eta_invariant_phase
        r = eta_invariant_phase()
        assert abs(r['theta_CS_deg'] - 34.44) < 0.01

    def test_tanh_pi_near_unity(self):
        """tanh(pi) = 0.9963, confirming near-maximal CP."""
        from planetary_polygons.extensions.ckm_mixing import eta_invariant_phase
        r = eta_invariant_phase()
        assert abs(r['tanh_factor'] - 0.9963) < 0.001
