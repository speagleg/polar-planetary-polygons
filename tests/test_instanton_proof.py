"""Tests for the formal instanton action derivation."""

import pytest
import numpy as np
from math import pi, log

from planetary_polygons.proofs.instanton_proof import (
    texture_zero_proof, winding_numbers, instanton_action, selectivity_proof,
)


class TestTextureZero:
    def test_YYdag_02_is_zero(self):
        """(YY^dag)_{02} = 0 algebraically from the texture."""
        result = texture_zero_proof()
        assert result['YYdag_02_is_zero']

    def test_texture_has_5_nonzero(self):
        result = texture_zero_proof()
        assert result['nonzero_count'] == 5


class TestWindingNumbers:
    def test_vub_winding(self):
        """V_ub: w_total = N-1 = 6."""
        table = winding_numbers()
        vub = [r for r in table if r['element'] == 'V_ub'][0]
        assert vub['w_total'] == 6
        assert vub['level'] == 'INSTANTON'

    def test_vus_winding(self):
        """V_us: w_total = 2, tree level."""
        table = winding_numbers()
        vus = [r for r in table if r['element'] == 'V_us'][0]
        assert vus['w_total'] == 2
        assert vus['level'] == 'TREE'

    def test_vcb_winding(self):
        """V_cb: w_total = 4, tree level."""
        table = winding_numbers()
        vcb = [r for r in table if r['element'] == 'V_cb'][0]
        assert vcb['w_total'] == 4
        assert vcb['level'] == 'TREE'

    def test_max_intra_orbit_gap(self):
        """Max gap within QR and QNR is (N-1)/2 = 3."""
        table = winding_numbers()
        vub = [r for r in table if r['element'] == 'V_ub'][0]
        assert vub['w_up'] == 3
        assert vub['w_dn'] == 3


class TestInstantonAction:
    def test_action_value(self):
        """exp(-S) should equal K^(N-1)."""
        from planetary_polygons.extensions.bernoulli_havelock import instanton_fugacity
        K = instanton_fugacity()
        result = instanton_action()
        assert abs(result['exp_neg_S'] - K ** 6) < 1e-10

    def test_action_formula(self):
        """S = (N-1) * 2*pi*k_frac."""
        result = instanton_action()
        expected = result['N_minus_1'] * 2 * pi * result['k_frac']
        assert abs(result['S_inst'] - expected) < 1e-10


class TestSelectivity:
    def test_only_vub_corrected(self):
        """Only V_ub gets the instanton correction."""
        result = selectivity_proof()
        assert result['V_us_corrected'] is False
        assert result['V_cb_corrected'] is False
        assert result['V_ub_corrected'] is True
