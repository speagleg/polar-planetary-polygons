"""Tests for the orbit-based CKM matrix from the Bernoulli backbone."""

import pytest
import numpy as np
from math import pi, sqrt, atan, degrees, sin, asin
import cmath

from planetary_polygons.extensions.orbit_ckm import (
    UP_L, DN_L, HIGGS,
    build_orbit_yukawa, diag_left, ckm_matrix,
    instanton_correction, unitarity_triangle,
)


class TestConstants:
    def test_up_modes_are_QR(self):
        assert UP_L == [1, 2, 4]

    def test_dn_modes_are_QNR(self):
        assert DN_L == [6, 5, 3]

    def test_higgs_modes(self):
        assert HIGGS == [3, 4]


class TestYukawaTexture:
    def test_texture_shape(self):
        """5 nonzero entries, 4 zeros."""
        Y = build_orbit_yukawa(UP_L)
        nonzero = np.count_nonzero(np.abs(Y) > 1e-10)
        assert nonzero == 5

    def test_texture_pattern(self):
        """Texture is [0,*,*; *,*,0; *,0,0]."""
        Y = build_orbit_yukawa(UP_L)
        assert abs(Y[0, 0]) < 1e-10
        assert abs(Y[1, 2]) < 1e-10
        assert abs(Y[2, 1]) < 1e-10
        assert abs(Y[2, 2]) < 1e-10
        assert abs(Y[0, 1]) > 1e-10
        assert abs(Y[0, 2]) > 1e-10
        assert abs(Y[1, 0]) > 1e-10
        assert abs(Y[1, 1]) > 1e-10
        assert abs(Y[2, 0]) > 1e-10

    def test_YYdag_02_zero(self):
        """(YY^dag)[0,2] = 0 to machine precision."""
        Y = build_orbit_yukawa(UP_L)
        YYd = Y @ Y.conj().T
        assert abs(YYd[0, 2]) < 1e-12

    def test_up_down_same_texture(self):
        """Up and down Yukawa have identical zero pattern."""
        Y_up = build_orbit_yukawa(UP_L)
        Y_dn = build_orbit_yukawa(DN_L)
        tex_up = (np.abs(Y_up) > 1e-10).astype(int)
        tex_dn = (np.abs(Y_dn) > 1e-10).astype(int)
        np.testing.assert_array_equal(tex_up, tex_dn)


class TestLeftRotation:
    def test_left_uses_YYdag(self):
        """diag_left diagonalizes YY^dag, not Y^dag Y."""
        Y = build_orbit_yukawa(UP_L)
        m_L, U_L = diag_left(Y)
        YYd = Y @ Y.conj().T
        D = U_L.conj().T @ YYd @ U_L
        np.testing.assert_allclose(np.abs(D - np.diag(np.diag(D))), 0, atol=1e-10)

    def test_ckm_unitarity(self):
        """V^dag V = I within machine precision."""
        result = ckm_matrix()
        V = result['V']
        VdV = V.conj().T @ V
        np.testing.assert_allclose(VdV, np.eye(3), atol=1e-10)


class TestCKMObservables:
    def test_delta_ckm(self):
        """beta (= PDG gamma) within ~10 deg of arctan(sqrt(7))."""
        result = ckm_matrix()
        assert abs(result['beta'] - 69) < 10

    def test_s12(self):
        """Cabibbo angle within 15% of PDG 0.2245."""
        result = ckm_matrix()
        assert abs(result['s12'] - 0.2245) / 0.2245 < 0.15

    def test_s23(self):
        """V_cb within 20% of PDG 0.0421."""
        result = ckm_matrix()
        assert abs(result['s23'] - 0.0421) / 0.0421 < 0.20

    def test_s13_tree_significant(self):
        """Tree-level s13 > 0.05 (before instanton correction)."""
        result = ckm_matrix()
        assert result['s13_tree'] > 0.05

    def test_s13_corrected(self):
        """Instanton-corrected s13 within 40% of PDG 0.00365."""
        result = ckm_matrix()
        assert abs(result['s13_corrected'] - 0.00365) / 0.00365 < 0.40

    def test_jarlskog(self):
        """Jarlskog invariant within 35% of PDG 3.08e-5."""
        result = ckm_matrix()
        assert abs(result['J'] - 3.08e-5) / 3.08e-5 < 0.35

    def test_sin2_delta(self):
        """sin^2(delta) close to 7/8 = N/(N+1)."""
        target = 7 / 8
        delta_rad = atan(sqrt(7))
        assert abs(sin(delta_rad) ** 2 - target) < 0.001


class TestInstantonCorrection:
    def test_instanton_formula(self):
        """s13_corrected = s13_tree * K^(N-1)."""
        from planetary_polygons.extensions.bernoulli_havelock import instanton_fugacity
        K = instanton_fugacity()
        s13_tree = 0.145
        s13_corr = instanton_correction(s13_tree, K)
        expected = s13_tree * K ** 6
        assert abs(s13_corr - expected) < 1e-10

    def test_instanton_changes_vub(self):
        """s13_tree != s13_corrected (instanton changes V_ub)."""
        result = ckm_matrix()
        assert result['s13_tree'] != result['s13_corrected']

    def test_sigma_independence_of_phases(self):
        """beta is approximately sigma-independent (within 20 deg)."""
        r3 = ckm_matrix(sigma=3)
        r10 = ckm_matrix(sigma=10)
        assert abs(r3['beta'] - r10['beta']) < 20


class TestUnitarityTriangle:
    def test_triangle_sums_to_180(self):
        """alpha + beta + gamma = 180 degrees."""
        result = ckm_matrix()
        total = result['alpha'] + result['beta'] + result['gamma']
        assert abs(total - 180) < 0.1
