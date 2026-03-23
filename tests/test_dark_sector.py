"""Tests for the dark sector cosmological predictions."""

import math
import pytest
from planetary_polygons.extensions.dark_sector import (
    dark_sector_budget, dark_matter_spectrum, required_mass_gap,
)


class TestDarkSectorBudget:
    def test_n11_de_within_1sigma(self):
        """DE at N=11 with radion is within 1σ of Planck."""
        r = dark_sector_budget(N=11, delta_E=0.81, include_radion=True)
        assert r['sigma_DE'] < 1.0

    def test_n11_dm_within_1sigma(self):
        """DM at N=11 with radion is within 1σ of Planck."""
        r = dark_sector_budget(N=11, delta_E=0.81, include_radion=True)
        assert r['sigma_DM'] < 1.0

    def test_de_dm_ratio(self):
        """DE/DM ratio matches Planck to < 1%."""
        r = dark_sector_budget(N=11, delta_E=0.81, include_radion=True)
        observed = 68.47 / 26.60
        assert abs(r['DE_DM_ratio'] - observed) / observed < 0.01

    def test_total_dark_sector(self):
        """Total dark sector (DE+DM) ≈ 95%."""
        r = dark_sector_budget(N=11, delta_E=0.81, include_radion=True)
        total_dark = r['DE_pct'] + r['DM_pct']
        assert 93 < total_dark < 97

    def test_radion_matters(self):
        """The radion correction significantly improves the fit."""
        with_radion = dark_sector_budget(N=11, include_radion=True)
        without_radion = dark_sector_budget(N=11, include_radion=False)
        assert with_radion['sigma_DE'] < without_radion['sigma_DE']


class TestDarkMatterSpectrum:
    def test_n11_four_dm_pairs(self):
        """N=11 has 4 frozen pairs (DM candidates) + 1 critical."""
        spec = dark_matter_spectrum(11)
        n_frozen = sum(1 for s in spec if not s['is_critical'])
        assert n_frozen == 4

    def test_triangular_number_gaps(self):
        """The Casimir gaps at N=11 are triangular numbers 1,3,6,10."""
        spec = dark_matter_spectrum(11)
        gaps = sorted([s['eigenvalue_gap'] for s in spec if not s['is_critical']])
        assert gaps == [1.0, 3.0, 6.0, 10.0]

    def test_mass_ratios(self):
        """DM masses ∝ √(triangular numbers)."""
        spec = dark_matter_spectrum(11)
        masses = sorted([s['mass'] for s in spec if s['mass'] > 0])
        ratios = [m / masses[0] for m in masses]
        expected = [1, math.sqrt(3), math.sqrt(6), math.sqrt(10)]
        for r, e in zip(ratios, expected):
            assert abs(r - e) < 0.01

    def test_eight_dm_species(self):
        """8 DM species total (4 pairs × degeneracy 2)."""
        spec = dark_matter_spectrum(11)
        total = sum(s['degeneracy'] for s in spec if not s['is_critical'])
        assert total == 8


class TestRequiredMassGap:
    def test_positive(self):
        gap = required_mass_gap(11)
        assert gap > 0

    def test_order_of_magnitude(self):
        """The required mass gap should be O(1) in polygon units."""
        gap = required_mass_gap(11)
        assert 0.1 < gap < 5.0
