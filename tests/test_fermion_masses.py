"""Tests for fermion mass structure from the polygon hierarchy."""

import math
import pytest
import numpy as np
from planetary_polygons.extensions.fermion_masses import (
    yukawa_texture, rs_profile, yukawa_eigenvalues,
    tree_level_ratio, sector_decoupling, polygon_scale_from_rg,
)


class TestYukawaTexture:
    def test_four_zeros(self):
        """N=7 texture has exactly 4 zeros."""
        T = yukawa_texture(7, higgs_pair=2)
        assert np.sum(T == 0) == 4

    def test_five_nonzero(self):
        T = yukawa_texture(7, higgs_pair=2)
        assert np.sum(T == 1) == 5

    def test_specific_zeros(self):
        T = yukawa_texture(7, higgs_pair=2)
        assert T[0, 0] == 0  # (1,1)
        assert T[1, 2] == 0  # (2,3)
        assert T[2, 1] == 0  # (3,2)
        assert T[2, 2] == 0  # (3,3)


class TestTreeLevelRatio:
    def test_exact_value(self):
        """m₁/m₂ = √((5+√13)/(5-√13)) at tree level."""
        ratio = tree_level_ratio()
        expected = math.sqrt((5 + math.sqrt(13)) / (5 - math.sqrt(13)))
        assert ratio == pytest.approx(expected)

    def test_approximately_2_5(self):
        assert 2.4 < tree_level_ratio() < 2.6


class TestRSProfile:
    def test_large_c_saturates(self):
        """For c >> 1/2: f → √(2c-1) as σ → ∞."""
        f = rs_profile(2.0, 100)
        assert f == pytest.approx(math.sqrt(3), rel=0.01)

    def test_c_zero_decays(self):
        """For c = 0: f → e^{-σ/2}."""
        f = rs_profile(0.0, 20)
        assert f < 0.01  # exponentially small


class TestYukawaEigenvalues:
    def test_three_masses(self):
        result = yukawa_eigenvalues(7, sigma=15, mu4=0.5)
        assert len(result['masses']) == 3
        assert all(m >= 0 for m in result['masses'])

    def test_hierarchy_grows_with_sigma(self):
        r1 = yukawa_eigenvalues(7, sigma=10)['ratio_13']
        r2 = yukawa_eigenvalues(7, sigma=20)['ratio_13']
        assert r2 > r1

    def test_up_down_split(self):
        """Up-type and down-type have different mass spectra."""
        up = yukawa_eigenvalues(7, sigma=15, mu4=0.5)
        dn = yukawa_eigenvalues(7, sigma=15, mu4=1.5)
        # The spectra should differ (SU(2) isospin breaks degeneracy)
        assert abs(up['masses'][0] - dn['masses'][0]) > 0.1


class TestSectorDecoupling:
    def test_decoupled(self):
        result = sector_decoupling()
        assert result['decoupled'] is True
        assert result['lcm'] == 56


class TestPolygonScale:
    def test_rg_amplification_needed(self):
        """RG amplification factor: tree 2.5 → physical 280 = factor ~112."""
        tree = tree_level_ratio()
        target = 280
        amplification = target / tree
        assert 50 < amplification < 200
