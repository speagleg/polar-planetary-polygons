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


class TestPlancherelPhase:
    """Tests for delta = 2*theta_CS*tanh(pi) from the H^2 Dirac Plancherel density."""

    def test_delta_matches_observed(self):
        """delta = 68.63 deg matches observed 69 +/- 3 deg."""
        from planetary_polygons.extensions.ckm_mixing import eta_invariant_phase
        r = eta_invariant_phase()
        assert abs(r['delta_deg'] - 69) < 3  # within 1 sigma

    def test_delta_is_2_theta_cs_tanh_pi(self):
        """delta = 2 * theta_CS * tanh(pi) exactly (N=7)."""
        from math import tanh, pi
        from planetary_polygons.extensions.ckm_mixing import eta_invariant_phase
        r = eta_invariant_phase()
        expected = 2 * r['theta_CS_rad'] * tanh(pi)
        assert abs(r['delta_rad'] - expected) < 1e-12

    def test_delta_68_63(self):
        """delta = 68.63 deg at N=7 (0.37 deg off PDG, 0.12 sigma)."""
        from planetary_polygons.extensions.ckm_mixing import eta_invariant_phase
        r = eta_invariant_phase()
        assert abs(r['delta_deg'] - 68.63) < 0.01

    def test_theta_cs_34_44(self):
        """theta_CS = 34.44 deg from N=7 (topological, via b(N))."""
        from planetary_polygons.extensions.ckm_mixing import eta_invariant_phase
        r = eta_invariant_phase()
        assert abs(r['theta_CS_deg'] - 34.44) < 0.01

    def test_bf_crossing_dominates(self):
        """Gen 3 mode 3 (BF crossing) contributes > 90% of Plancherel weight."""
        from planetary_polygons.extensions.ckm_mixing import eta_invariant_phase
        r = eta_invariant_phase()
        assert r['bf_fraction'] > 0.90

    def test_j_consistency_check(self):
        """J check with observed angles and predicted delta matches to 5%."""
        from planetary_polygons.extensions.ckm_mixing import eta_invariant_phase
        r = eta_invariant_phase()
        # J = 3.09e-5 (3% off observed 3.0e-5)
        assert abs(r['J_check'] - 3.0e-5) / 3.0e-5 < 0.05

    def test_delta_m_is_unity(self):
        """BF crossing range Delta_m = 1 from the T3 Higgs split."""
        from planetary_polygons.extensions.ckm_mixing import eta_invariant_phase
        r = eta_invariant_phase()
        assert r['delta_m'] == 1.0


class TestBFBarrierTransmission:
    """Tests for the orbifold image barrier T_2 = Q_1(cosh d_image)."""

    def test_T2_from_legendre(self):
        """T_2 = Q_1(cosh d) at rho* = 1.734, N=7."""
        from planetary_polygons.extensions.ckm_mixing import bf_barrier_transmission
        r = bf_barrier_transmission()
        # Q_1(cosh d) should be ~0.024
        assert abs(r['T_2'] - 0.024) < 0.002

    def test_geodesic_distance(self):
        """Geodesic distance to nearest Z_7 image at rho*."""
        from planetary_polygons.extensions.ckm_mixing import bf_barrier_transmission
        r = bf_barrier_transmission()
        assert abs(r['d'] - 2.02) < 0.01

    def test_V_cb_uncorrected(self):
        """Uncorrected V_cb = sqrt(V_cb_pert * T_2) within 15% of observed."""
        from planetary_polygons.extensions.ckm_mixing import bf_barrier_transmission
        r = bf_barrier_transmission()
        assert abs(r['V_cb_uncorrected'] - 0.042) / 0.042 < 0.15

    def test_V_cb_self_consistent(self):
        """Self-consistent V_cb within 10% of observed (linearised image correction).

        The linearised correction rho* = rho*_0 + 2*Q_1*tanh(rho*_0) gives
        V_cb = 0.044, 6% above observed 0.041. The 15% theoretical sensitivity
        (from rho* elasticity -3) is the stated precision tier.
        """
        from planetary_polygons.extensions.ckm_mixing import bf_barrier_transmission
        r = bf_barrier_transmission()
        assert abs(r['V_cb'] - 0.0412) / 0.0412 < 0.10

    def test_rho_star_sc(self):
        """Self-consistent rho* shifted ~3-4% from uncorrected."""
        from planetary_polygons.extensions.ckm_mixing import bf_barrier_transmission
        r = bf_barrier_transmission()
        shift = (r['rho_star_sc'] - r['rho_star']) / r['rho_star']
        assert 0.02 < shift < 0.06

    def test_image_hierarchy(self):
        """Nearest images (k=1,6) dominate over farther ones."""
        from planetary_polygons.extensions.ckm_mixing import bf_barrier_transmission
        r = bf_barrier_transmission()
        nearest = r['images'][0]['Q1']  # k=1
        farther = r['images'][1]['Q1']  # k=2
        assert nearest > 5 * farther  # nearest >> farther

    def test_conformal_dimension(self):
        """BF-crossing mode has c = 3/2, giving Legendre order nu = 1."""
        from planetary_polygons.extensions.ckm_mixing import bf_barrier_transmission
        r = bf_barrier_transmission()
        assert r['nu'] == 1.0
        assert r['c'] == 1.5
