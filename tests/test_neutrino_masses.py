"""Tests for neutrino masses from the seesaw mechanism."""

import pytest
from planetary_polygons.extensions.neutrino_masses import neutrino_seesaw


class TestNeutrinoSeesaw:
    def test_normal_hierarchy(self):
        """Predicts normal hierarchy: m₃ >> m₂ >> m₁."""
        result = neutrino_seesaw()
        masses = [g['m_nu_eV'] for g in result['generations']]
        assert masses[2] > masses[1] > masses[0]
        assert result['hierarchy'] == 'normal'

    def test_three_generations(self):
        """Three neutrino generations from (N_grav-1)/2 = 3."""
        result = neutrino_seesaw()
        assert len(result['generations']) == 3

    def test_mass_scale_correct_ballpark(self):
        """Neutrino masses in the 10⁻⁴ to 1 eV range."""
        result = neutrino_seesaw()
        for g in result['generations']:
            assert 1e-6 < g['m_nu_eV'] < 10

    def test_majorana_scale_from_instanton(self):
        """M_R ~ 10^{12}-10^{13} GeV from the CS instanton."""
        result = neutrino_seesaw()
        assert 1e11 < result['M_R_GeV'] < 1e14

    def test_dm32_larger_than_dm21(self):
        """Δm²₃₂ >> Δm²₂₁ (normal hierarchy pattern)."""
        result = neutrino_seesaw()
        assert result['dm32_sq'] > result['dm21_sq']

    def test_dirac_masses_hierarchical(self):
        """Dirac masses: m_D(gen3) >> m_D(gen2) >> m_D(gen1)."""
        result = neutrino_seesaw()
        m_D = [g['m_D_GeV'] for g in result['generations']]
        assert m_D[2] > m_D[1] > m_D[0]

    def test_neutrino_contributes_to_matter(self):
        """Ω_ν > 0 (neutrinos add to the matter budget)."""
        result = neutrino_seesaw()
        assert result['omega_nu'] > 0
