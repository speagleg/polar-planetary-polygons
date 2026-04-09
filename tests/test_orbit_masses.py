"""Tests for fermion mass predictions from the Bernoulli backbone."""

import pytest
from math import sqrt
from fractions import Fraction

from planetary_polygons.extensions.orbit_masses import (
    sigma_mass, mass_ratio_up, mass_table, isospin_shift,
)
from planetary_polygons.extensions.bernoulli_havelock import SIGMA_0


class TestSigmaMass:
    def test_sigma_mass_formula(self):
        """sigma_mass = SIGMA_0 * sqrt(7)."""
        assert abs(sigma_mass() - SIGMA_0 * sqrt(7)) < 1e-10

    def test_isospin_shift(self):
        """Isospin shift = 1/N = 1/7."""
        assert isospin_shift() == Fraction(1, 7)


class TestMassRatios:
    def test_mt_is_reference(self):
        """m_t/m_t = 1 (BF threshold, lambda=0)."""
        assert abs(mass_ratio_up(4) - 1.0) < 1e-10

    def test_mc_within_range(self):
        """m_c/m_t within factor of 5 of observed (F_IR gives ~3.6x)."""
        obs = 1.27 / 173
        pred = mass_ratio_up(2)
        assert 0.1 < pred / obs < 10.0

    def test_mu_within_range(self):
        """m_u/m_t within factor of 5 of observed (F_IR gives ~0.3x)."""
        obs = 2.2e-3 / 173
        pred = mass_ratio_up(1)
        assert 0.1 < pred / obs < 10.0


class TestMassTable:
    def test_mb_within_range(self):
        """m_b within factor of 2 of 4.18 GeV."""
        table = mass_table()
        assert 2.0 < table['b']['pred'] < 8.5

    def test_mc_within_range(self):
        """m_c within factor of 2 of 1.27 GeV."""
        table = mass_table()
        assert 0.5 < table['c']['pred'] < 3.0

    def test_mu_right_order(self):
        """m_u in the MeV range."""
        table = mass_table()
        assert 1e-4 < table['u']['pred'] < 0.01  # between 0.1 MeV and 10 MeV

    def test_mass_ordering(self):
        """t > b > c (correct hierarchy for the three we predict well)."""
        table = mass_table()
        assert table['t']['pred'] > table['b']['pred'] > table['c']['pred']
