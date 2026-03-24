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
        assert abs(J - 3.5e-5) / 3.5e-5 < 0.1  # within 10%
