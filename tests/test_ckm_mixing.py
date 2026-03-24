"""Tests for CKM mixing from the Havelock Yukawa texture."""

import numpy as np
import pytest
from planetary_polygons.extensions.ckm_mixing import ckm_matrix, yukawa_texture


class TestYukawaTexture:
    def test_4_zeros(self):
        """The texture has exactly 4 zeros."""
        t = yukawa_texture()
        assert np.sum(t == 0) == 4

    def test_5_nonzero(self):
        """The texture has exactly 5 nonzero entries."""
        t = yukawa_texture()
        assert np.sum(t == 1) == 5


class TestCKMStructure:
    def test_near_diagonal(self):
        """The CKM matrix is near-diagonal (|V_ud|, |V_tb| > 0.9)."""
        ckm = ckm_matrix()
        assert ckm['is_near_diagonal']

    def test_hierarchical(self):
        """The off-diagonal elements are hierarchical: |V_us| > |V_cb| > |V_ub|."""
        ckm = ckm_matrix()
        assert ckm['is_hierarchical']

    def test_unitary(self):
        """The CKM matrix is unitary (V†V = I)."""
        ckm = ckm_matrix()
        VdV = ckm['V_complex'].conj().T @ ckm['V_complex']
        np.testing.assert_allclose(VdV, np.eye(3), atol=1e-10)

    def test_cabibbo_angle(self):
        """The Cabibbo angle is within 20% of the observed 13°."""
        ckm = ckm_matrix()
        assert 8 < ckm['theta_C_deg'] < 18

    def test_V_us_order_of_magnitude(self):
        """|V_us| ≈ 0.2 (observed: 0.224)."""
        ckm = ckm_matrix()
        assert 0.1 < ckm['V_us'] < 0.4

    def test_V_cb_small(self):
        """|V_cb| is small (< 0.1)."""
        ckm = ckm_matrix()
        assert ckm['V_cb'] < 0.15

    def test_V_ub_smallest(self):
        """|V_ub| is the smallest off-diagonal element."""
        ckm = ckm_matrix()
        assert ckm['V_ub'] < ckm['V_cb'] < ckm['V_us']
