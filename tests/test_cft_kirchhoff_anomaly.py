"""Tests for Pipeline C: Kirchhoff-Liouville anomaly decomposition."""
import sys
sys.path.insert(0, "/mnt/c/Users/gspea/source/repos/spiral-hexagon")

from math import log, pi, sin
import pytest


def b_N(N):
    """Reference b(N)."""
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


def casimir(m, N):
    return m * (N - m) / 2.0


class TestBNDecomposition:
    """The structural identity b(N) = (1/(N-1)) sum [f(m,N) + log sin(pi m/N)]."""

    @pytest.mark.parametrize("N", [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 16, 20])
    def test_bN_equals_mode_average(self, N):
        """b(N) = (1/(N-1)) sum_{m=1}^{N-1} [f(m,N) + log sin(pi m/N)]."""
        from planetary_polygons.extensions.cft_kirchhoff_anomaly import (
            b_from_mode_decomposition,
        )
        b_decomp = b_from_mode_decomposition(N)
        assert abs(b_decomp - b_N(N)) < 1e-12, (
            f"N={N}: decomposition {b_decomp} != b(N) {b_N(N)}"
        )

    @pytest.mark.parametrize("N", [3, 5, 7, 11])
    def test_casimir_part_equals_mean_casimir(self, N):
        """The Casimir part of the decomposition = N(N+1)/12."""
        from planetary_polygons.extensions.cft_kirchhoff_anomaly import (
            casimir_contribution,
        )
        cas = casimir_contribution(N)
        expected = N * (N + 1) / 12
        assert abs(cas - expected) < 1e-12

    @pytest.mark.parametrize("N", [3, 5, 7, 11])
    def test_cone_part_equals_log_self_energy(self, N):
        """The cone-angle part = -log 2 + log(N)/(N-1)."""
        from planetary_polygons.extensions.cft_kirchhoff_anomaly import (
            cone_angle_contribution,
        )
        cone = cone_angle_contribution(N)
        expected = -log(2) + log(N) / (N - 1)
        assert abs(cone - expected) < 1e-12


class TestCentralChargeFromAnomaly:
    """c = 12 b(N) from the Polyakov anomaly identification."""

    @pytest.mark.parametrize("N", [3, 5, 7, 11])
    def test_central_charge_equals_12bN(self, N):
        """The anomaly coefficient c_eff = 12 * b(N)."""
        from planetary_polygons.extensions.cft_kirchhoff_anomaly import (
            central_charge_pipeline_C,
        )
        c = central_charge_pipeline_C(N)
        assert abs(c - 12 * b_N(N)) < 1e-10

    @pytest.mark.parametrize("N", [3, 5, 7, 11])
    def test_polyakov_alvarez_cone_coefficient(self, N):
        """Verify (alpha + 1/alpha - 2) for alpha = 1/N."""
        from planetary_polygons.extensions.cft_kirchhoff_anomaly import (
            cone_defect_coefficient,
        )
        coeff = cone_defect_coefficient(N)
        expected = 1.0 / N + N - 2
        assert abs(coeff - expected) < 1e-14

    def test_gauss_product_identity(self):
        """prod_{m=1}^{N-1} 2 sin(pi m/N) = N (Gauss)."""
        from planetary_polygons.extensions.cft_kirchhoff_anomaly import (
            gauss_product,
        )
        for N in [3, 5, 7, 11, 13, 17]:
            assert abs(gauss_product(N) - N) < 1e-10

    @pytest.mark.parametrize("N", [3, 5, 7, 11])
    def test_orbifold_euler_characteristic(self, N):
        """chi_orb for N-punctured sphere with cone angle 2pi/N."""
        from planetary_polygons.extensions.cft_kirchhoff_anomaly import (
            orbifold_euler_char,
        )
        chi = orbifold_euler_char(N)
        expected = 2 + N * (N - 1)
        assert abs(chi - expected) < 1e-12
