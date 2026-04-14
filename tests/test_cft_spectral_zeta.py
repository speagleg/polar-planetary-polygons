"""Tests for Pipeline B: Polyakov-Alvarez spectral zeta anomaly."""
import sys
sys.path.insert(0, "/mnt/c/Users/gspea/source/repos/spiral-hexagon")

from math import log, pi, sin
import pytest


def b_N(N):
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


class TestHeatKernelCoefficients:
    """Heat-kernel Seeley-DeWitt coefficients on the conical sphere."""

    @pytest.mark.parametrize("N", [3, 5, 7, 11])
    def test_a0_coefficient(self, N):
        """a_0 = Area / (4 pi) for the conical sphere."""
        from planetary_polygons.extensions.cft_spectral_zeta import (
            heat_kernel_a0,
        )
        a0 = heat_kernel_a0(N)
        assert a0 > 0

    @pytest.mark.parametrize("N", [3, 5, 7, 11])
    def test_a1_coefficient_smooth_plus_conical(self, N):
        """a_1 = chi(Sigma)/6 + conical correction."""
        from planetary_polygons.extensions.cft_spectral_zeta import (
            heat_kernel_a1,
        )
        a1 = heat_kernel_a1(N)
        assert isinstance(a1, float)
        # a1 should be positive for all N >= 3
        assert a1 > 0

    @pytest.mark.parametrize("N", [3, 5, 7, 11])
    def test_a1_conical_correction(self, N):
        """Conical correction to a_1: N * (N^2 - 1)/(12 N) = (N^2 - 1)/12."""
        from planetary_polygons.extensions.cft_spectral_zeta import (
            conical_heat_correction,
        )
        corr = conical_heat_correction(N)
        expected = (N * N - 1) / 12
        assert abs(corr - expected) < 1e-12


class TestPolyakovAlvarezAnomaly:
    """The Polyakov-Alvarez anomaly on conical surfaces."""

    @pytest.mark.parametrize("N", [3, 5, 7, 11])
    def test_anomaly_coefficient_is_bN(self, N):
        """The anomaly coefficient c/12 = b(N)."""
        from planetary_polygons.extensions.cft_spectral_zeta import (
            anomaly_coefficient,
        )
        coeff = anomaly_coefficient(N)
        assert abs(coeff - b_N(N)) < 1e-8, (
            f"N={N}: anomaly coeff {coeff} != b(N) {b_N(N)}"
        )

    @pytest.mark.parametrize("N", [3, 5, 7, 11])
    def test_central_charge_equals_12bN(self, N):
        """Pipeline B gives c = 12 b(N)."""
        from planetary_polygons.extensions.cft_spectral_zeta import (
            central_charge_pipeline_B,
        )
        c = central_charge_pipeline_B(N)
        assert abs(c - 12 * b_N(N)) < 1e-8

    @pytest.mark.parametrize("N", [3, 5, 7, 11])
    def test_anomaly_splits_bulk_and_conical(self, N):
        """Anomaly = bulk (mean Casimir) + conical (cone defects)."""
        from planetary_polygons.extensions.cft_spectral_zeta import (
            anomaly_bulk_part,
            anomaly_conical_part,
            anomaly_coefficient,
        )
        bulk = anomaly_bulk_part(N)
        conical = anomaly_conical_part(N)
        total = anomaly_coefficient(N)
        assert abs(bulk + conical - total) < 1e-10

    @pytest.mark.parametrize("N", [3, 5, 7, 11])
    def test_bulk_part_is_mean_casimir(self, N):
        """Bulk anomaly = N(N+1)/12 (mean Casimir)."""
        from planetary_polygons.extensions.cft_spectral_zeta import (
            anomaly_bulk_part,
        )
        bulk = anomaly_bulk_part(N)
        expected = N * (N + 1) / 12
        assert abs(bulk - expected) < 1e-12

    @pytest.mark.parametrize("N", [3, 5, 7, 11])
    def test_conical_part_is_log_self_energy(self, N):
        """Conical anomaly = -log 2 + log(N)/(N-1)."""
        from planetary_polygons.extensions.cft_spectral_zeta import (
            anomaly_conical_part,
        )
        conical = anomaly_conical_part(N)
        expected = -log(2) + log(N) / (N - 1)
        assert abs(conical - expected) < 1e-12
