"""Three-way agreement test: Pipelines A, B, C all give c = 12 b(N)."""
import sys
sys.path.insert(0, "/mnt/c/Users/gspea/source/repos/spiral-hexagon")

from math import log
import pytest


def b_N(N):
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


class TestThreeWayAgreement:
    """All three pipelines agree: c_A = c_B = c_C = 12 b(N)."""

    @pytest.mark.parametrize("N", [3, 5, 7, 11])
    def test_all_pipelines_agree(self, N):
        from planetary_polygons.extensions.cft_kirchhoff_anomaly import (
            central_charge_pipeline_C,
        )
        from planetary_polygons.extensions.cft_liouville_action import (
            central_charge_pipeline_A,
        )
        from planetary_polygons.extensions.cft_spectral_zeta import (
            central_charge_pipeline_B,
        )

        c_A = central_charge_pipeline_A(N)
        c_B = central_charge_pipeline_B(N)
        c_C = central_charge_pipeline_C(N)
        c_ref = 12 * b_N(N)

        # All three agree with reference
        assert abs(c_A - c_ref) < 1e-10, f"Pipeline A: {c_A} != {c_ref}"
        assert abs(c_B - c_ref) < 1e-10, f"Pipeline B: {c_B} != {c_ref}"
        assert abs(c_C - c_ref) < 1e-10, f"Pipeline C: {c_C} != {c_ref}"

        # All three agree with each other
        assert abs(c_A - c_B) < 1e-12, f"A != B: {c_A} vs {c_B}"
        assert abs(c_B - c_C) < 1e-12, f"B != C: {c_B} vs {c_C}"

    @pytest.mark.parametrize("N", [3, 5, 7, 11])
    def test_anomaly_decomposition_consistent(self, N):
        """Bulk + conical = total, across all pipelines."""
        from planetary_polygons.extensions.cft_kirchhoff_anomaly import (
            casimir_contribution,
            cone_angle_contribution,
        )
        from planetary_polygons.extensions.cft_spectral_zeta import (
            anomaly_bulk_part,
            anomaly_conical_part,
        )

        # Pipeline C decomposition
        cas_C = casimir_contribution(N)
        cone_C = cone_angle_contribution(N)

        # Pipeline B decomposition
        bulk_B = anomaly_bulk_part(N)
        cone_B = anomaly_conical_part(N)

        # Bulk parts agree (both = mean Casimir = N(N+1)/12)
        assert abs(cas_C - bulk_B) < 1e-12

        # Conical parts agree (both = -log 2 + log(N)/(N-1))
        assert abs(cone_C - cone_B) < 1e-12

    @pytest.mark.parametrize("N", [3, 4, 5, 6, 7, 8, 10, 12, 16, 20])
    def test_large_N_scaling(self, N):
        """c ~ N^2 + N for large N."""
        from planetary_polygons.extensions.cft_kirchhoff_anomaly import (
            central_charge_pipeline_C,
        )
        c = central_charge_pipeline_C(N)
        # Leading term: N(N+1) = N^2 + N
        leading = N * (N + 1)
        # Subleading: -12 log 2 + 12 log(N)/(N-1) -> -12 log 2
        correction = -12 * log(2) + 12 * log(N) / (N - 1)
        expected = leading + correction
        assert abs(c - expected) < 1e-10
