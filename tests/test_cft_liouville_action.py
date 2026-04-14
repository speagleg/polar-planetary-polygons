"""Tests for Pipeline A: Takhtajan-Zograf classical Liouville action."""
import sys
sys.path.insert(0, "/mnt/c/Users/gspea/source/repos/spiral-hexagon")

from math import log, pi, sin
import pytest


def b_N(N):
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


class TestRegularizedLiouvilleAction:
    """Regularized Liouville action at the N-gon saddle."""

    @pytest.mark.parametrize("N", [3, 5, 7, 11])
    def test_SL_at_Ngon_saddle(self, N):
        """S_L at the N-gon saddle is finite and negative."""
        from planetary_polygons.extensions.cft_liouville_action import (
            liouville_action_ngon_saddle,
        )
        S_L = liouville_action_ngon_saddle(N)
        assert S_L < 0, f"S_L should be negative, got {S_L}"

    @pytest.mark.parametrize("N", [3, 5, 7, 11])
    def test_SL_decomposes_bulk_plus_conical(self, N):
        """S_L = S_bulk + S_conical, both computable."""
        from planetary_polygons.extensions.cft_liouville_action import (
            liouville_action_bulk,
            liouville_action_conical,
            liouville_action_ngon_saddle,
        )
        S_bulk = liouville_action_bulk(N)
        S_con = liouville_action_conical(N)
        S_total = liouville_action_ngon_saddle(N)
        assert abs((S_bulk + S_con) - S_total) < 1e-10


class TestCentralChargeFromTZ:
    """Central charge extraction from Takhtajan-Zograf."""

    @pytest.mark.parametrize("N", [3, 5, 7, 11])
    def test_central_charge_equals_12bN(self, N):
        """Pipeline A gives c = 12 b(N)."""
        from planetary_polygons.extensions.cft_liouville_action import (
            central_charge_pipeline_A,
        )
        c = central_charge_pipeline_A(N)
        assert abs(c - 12 * b_N(N)) < 1e-8, (
            f"N={N}: Pipeline A c={c}, expected {12*b_N(N)}"
        )


class TestTZConicalFormula:
    """Takhtajan-Zograf formula on surfaces with equal-angle cones."""

    @pytest.mark.parametrize("N", [3, 5, 7, 11])
    def test_tz_accessory_parameter(self, N):
        """The accessory parameter at the Z_N-symmetric point is zero."""
        from planetary_polygons.extensions.cft_liouville_action import (
            accessory_parameter_ngon,
        )
        c_acc = accessory_parameter_ngon(N)
        assert isinstance(c_acc, float)
        assert abs(c_acc) < 1e-14  # zero by Z_N symmetry

    @pytest.mark.parametrize("N", [3, 4, 5, 6])
    def test_tz_action_finite_and_negative(self, N):
        """For small N: TZ action is finite and negative."""
        from planetary_polygons.extensions.cft_liouville_action import (
            liouville_action_ngon_saddle,
        )
        S_L = liouville_action_ngon_saddle(N)
        assert S_L < 0
        assert abs(S_L) > 1e-6

    @pytest.mark.parametrize("N", [3, 5, 7, 11])
    def test_pair_interaction_gauss(self, N):
        """Pair sum uses Gauss product: sum log(2 sin(pi p/N)) = log N."""
        from planetary_polygons.extensions.cft_liouville_action import (
            pair_interaction_sum,
        )
        s = pair_interaction_sum(N)
        assert abs(s - log(N)) < 1e-12
