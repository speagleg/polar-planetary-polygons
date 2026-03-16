"""Tests for Jupiter convergence: do cyclone rings sit at |lambda|=1?"""

import numpy as np
import pytest

from spiral_hexagon.data.jupiter import (
    JupiterParameters, juno_cyclone_positions,
    jupiter_sigma_test, jupiter_full_convergence,
)


class TestJunoCycloneData:
    def test_north_has_8_cyclones(self):
        pos = juno_cyclone_positions('north')
        assert len(pos['latitudes']) == 8

    def test_south_has_5_cyclones(self):
        pos = juno_cyclone_positions('south')
        assert len(pos['latitudes']) == 5

    def test_north_latitudes_near_83(self):
        pos = juno_cyclone_positions('north')
        assert all(80 < lat < 87 for lat in pos['latitudes'])


class TestJupiterSigma:
    def test_north_sigma_finite(self):
        result = jupiter_sigma_test('north')
        assert np.isfinite(result['sigma_geom'])

    def test_south_sigma_finite(self):
        result = jupiter_sigma_test('south')
        assert np.isfinite(result['sigma_geom'])

    def test_r_mobius_positive(self):
        result = jupiter_sigma_test('north')
        assert result['r_mobius'] > 0


class TestJupiterFullConvergence:
    def test_returns_both_poles(self):
        result = jupiter_full_convergence()
        assert 'north' in result
        assert 'south' in result

    def test_has_thomson_data(self):
        result = jupiter_full_convergence()
        assert 'kappa_crit' in result['north']

    def test_has_sigma_data(self):
        result = jupiter_full_convergence()
        assert 'sigma_geom' in result['north']

    def test_has_entry_mechanism(self):
        result = jupiter_full_convergence()
        assert 'entry_mechanism' in result['north']
