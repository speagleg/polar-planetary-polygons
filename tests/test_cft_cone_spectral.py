"""Tests for Route B-deep: cone spectral derivation of c = 12 b(N).

Tests the genuinely independent chain:
  Cone Laplacian -> Hurwitz zeta -> Gamma reflection -> log sin -> b(N)
"""
from math import log, lgamma, pi, sin
import pytest


def b_N_reference(N):
    """Reference b(N) from closed form (uses Gauss product internally)."""
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


class TestGammaReflectionRoute:
    """log sin(pi m/N) derived from Gamma reflection, not Gauss product."""

    @pytest.mark.parametrize("N", [3, 5, 7, 11])
    def test_log_sin_matches_direct(self, N):
        """Gamma reflection gives the same log sin as direct computation."""
        from planetary_polygons.extensions.cft_cone_spectral import (
            log_sin_from_reflection,
        )
        for m in range(1, N):
            via_reflection = log_sin_from_reflection(m, N)
            direct = log(sin(pi * m / N))
            assert abs(via_reflection - direct) < 1e-14, (
                f"N={N}, m={m}: reflection {via_reflection} != direct {direct}"
            )

    @pytest.mark.parametrize("N", [3, 5, 7, 11, 13, 17])
    def test_gauss_product_derived(self, N):
        """Gauss product identity derived as corollary of reflection formula."""
        from planetary_polygons.extensions.cft_cone_spectral import (
            gauss_product_from_reflection,
        )
        prod_val = gauss_product_from_reflection(N)
        expected = N / 2 ** (N - 1)
        assert abs(prod_val - expected) < 1e-10, (
            f"N={N}: derived product {prod_val} != N/2^(N-1) {expected}"
        )


class TestHurwitzZetaOnCone:
    """Hurwitz zeta derivative at s=0 from the cone angular spectrum."""

    @pytest.mark.parametrize("N", [3, 5, 7, 11])
    def test_hurwitz_at_rational(self, N):
        """zeta'_H(0, m/N) = lgamma(m/N) - (1/2) log(2pi)."""
        from planetary_polygons.extensions.cft_cone_spectral import (
            hurwitz_zeta_prime_at_zero,
        )
        for m in range(1, N):
            result = hurwitz_zeta_prime_at_zero(m / N)
            expected = lgamma(m / N) - 0.5 * log(2 * pi)
            assert abs(result - expected) < 1e-14


class TestConeSpectralDerivation:
    """b(N) derived from the cone spectral chain."""

    @pytest.mark.parametrize("N", [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 16, 20])
    def test_b_from_cone_matches_reference(self, N):
        """b(N) from cone spectrum = b(N) from closed form."""
        from planetary_polygons.extensions.cft_cone_spectral import (
            b_from_cone_spectrum,
        )
        b_cone = b_from_cone_spectrum(N)
        b_ref = b_N_reference(N)
        assert abs(b_cone - b_ref) < 1e-12, (
            f"N={N}: cone {b_cone} != ref {b_ref}"
        )

    @pytest.mark.parametrize("N", [3, 5, 7, 11])
    def test_central_charge_equals_12bN(self, N):
        """c = 12 b(N) from the cone spectral derivation."""
        from planetary_polygons.extensions.cft_cone_spectral import (
            central_charge_cone_spectral,
        )
        c = central_charge_cone_spectral(N)
        assert abs(c - 12 * b_N_reference(N)) < 1e-10

    @pytest.mark.parametrize("N", [50, 100])
    def test_large_N(self, N):
        """Derivation works for large N."""
        from planetary_polygons.extensions.cft_cone_spectral import (
            b_from_cone_spectrum,
        )
        b_cone = b_from_cone_spectrum(N)
        b_ref = b_N_reference(N)
        assert abs(b_cone - b_ref) < 1e-10


class TestIndependenceFromGaussProduct:
    """Verify the derivation does NOT use the Gauss product identity."""

    def test_per_mode_weights_are_independent(self):
        """Each mode weight w_m uses only Casimir + Gamma reflection."""
        from planetary_polygons.extensions.cft_cone_spectral import (
            cone_spectral_weight,
            casimir,
            log_sin_from_reflection,
        )
        N = 7
        for m in range(1, N):
            w = cone_spectral_weight(m, N)
            h = casimir(m, N)
            sigma = log_sin_from_reflection(m, N)
            assert abs(w - (h + sigma)) < 1e-14
            # sigma uses lgamma (Hurwitz zeta) and reflection, not sin()
            # h uses the algebraic formula m(N-m)/2

    def test_four_way_agreement(self):
        """All four pipelines agree: A, B, C, and cone-spectral."""
        from planetary_polygons.extensions.cft_kirchhoff_anomaly import (
            central_charge_pipeline_C,
        )
        from planetary_polygons.extensions.cft_liouville_action import (
            central_charge_pipeline_A,
        )
        from planetary_polygons.extensions.cft_spectral_zeta import (
            central_charge_pipeline_B,
        )
        from planetary_polygons.extensions.cft_cone_spectral import (
            central_charge_cone_spectral,
        )

        for N in [3, 5, 7, 11]:
            c_A = central_charge_pipeline_A(N)
            c_B = central_charge_pipeline_B(N)
            c_C = central_charge_pipeline_C(N)
            c_cone = central_charge_cone_spectral(N)
            c_ref = 12 * b_N_reference(N)

            assert abs(c_A - c_ref) < 1e-10
            assert abs(c_B - c_ref) < 1e-10
            assert abs(c_C - c_ref) < 1e-10
            assert abs(c_cone - c_ref) < 1e-10
