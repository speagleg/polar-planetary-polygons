"""Tests for N=8 instability analysis and Jupiter comparison."""

import numpy as np
import pytest
from n8_instability import (
    analyze_instability,
    jupiter_north_analysis,
    jupiter_south_analysis,
    stability_diagram,
)


class TestAnalyzeInstability:

    def test_n6_stable(self):
        result = analyze_instability(6)
        assert result.is_stable_without_center
        assert result.kappa_crit == 0.0

    def test_n8_unstable(self):
        result = analyze_instability(8)
        assert not result.is_stable_without_center
        assert result.unstable_fourier_modes is not None
        assert result.kappa_crit > 0

    def test_n8_kappa_crit_around_half(self):
        result = analyze_instability(8)
        assert 0.3 < result.kappa_crit < 0.7


class TestJupiterNorth:

    def test_returns_dict(self):
        result = jupiter_north_analysis()
        assert isinstance(result, dict)
        assert result['N'] == 8

    def test_unstable_without_center(self):
        result = jupiter_north_analysis()
        assert result['stable_without_center'] is False

    def test_prediction_met(self):
        result = jupiter_north_analysis()
        assert result['prediction_met'] is True

    def test_dominant_fourier_modes(self):
        result = jupiter_north_analysis()
        modes = result['unstable_mode_fourier']['dominant_m']
        assert 5 in modes  # pentagonal mode
        assert 4 in modes  # tetragonal mode

    def test_kappa_crit_reasonable(self):
        result = jupiter_north_analysis()
        assert 0.3 < result['kappa_crit'] < 0.7


class TestJupiterSouth:

    def test_returns_dict(self):
        result = jupiter_south_analysis()
        assert isinstance(result, dict)
        assert result['N'] == 5

    def test_stable_without_center(self):
        result = jupiter_south_analysis()
        assert result['stable_without_center'] is True
        assert result['kappa_crit'] == 0.0


class TestStabilityDiagram:

    def test_small_N_stable(self):
        diagram = stability_diagram(N_max=7)
        for N in [3, 4, 5, 6, 7]:
            assert diagram[N]['stable_without_center'] is True

    def test_N8_unstable(self):
        diagram = stability_diagram(N_max=8)
        assert diagram[8]['stable_without_center'] is False

    def test_kappa_crit_increases(self):
        diagram = stability_diagram(N_max=10)
        kc_8 = diagram[8]['kappa_crit']
        kc_9 = diagram[9]['kappa_crit']
        kc_10 = diagram[10]['kappa_crit']
        assert kc_8 < kc_9 < kc_10
