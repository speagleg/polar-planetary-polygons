"""Tests for the 4D Riemann curvature on the Seifert manifold."""

import math
import pytest


class TestSeifertParameters:
    """Layer 1: All background metric parameters are functions of N."""

    def test_lambda3(self):
        """Lambda_3 = (N^2 - 16)/16."""
        from planetary_polygons.extensions.weyl_tensor import seifert_parameters
        p = seifert_parameters(7)
        assert p['Lambda3'] == pytest.approx((49 - 16) / 16)

    def test_lambda4(self):
        """Lambda_4 = N^2/16."""
        from planetary_polygons.extensions.weyl_tensor import seifert_parameters
        p = seifert_parameters(11)
        assert p['Lambda4'] == pytest.approx(121 / 16)

    def test_all_determined(self):
        """Every metric parameter is a pure function of N."""
        from planetary_polygons.extensions.weyl_tensor import seifert_parameters
        for N in [5, 7, 8, 11, 15]:
            p1 = seifert_parameters(N)
            p2 = seifert_parameters(N)
            for key in p1:
                assert p1[key] == p2[key], f"Non-deterministic: {key} at N={N}"

    def test_fiber_stabilised(self):
        """Fiber radius sigma = 1 for all N."""
        from planetary_polygons.extensions.weyl_tensor import seifert_parameters
        for N in range(3, 20):
            assert seifert_parameters(N)['sigma'] == 1.0


class TestWeylDimension:
    """Weyl tensor component counts by dimension."""

    def test_vanishes_3d(self):
        """Weyl tensor has 0 components in d <= 3."""
        from planetary_polygons.extensions.weyl_tensor import weyl_dimension
        assert weyl_dimension(2) == 0
        assert weyl_dimension(3) == 0

    def test_ten_in_4d(self):
        """Weyl tensor has 10 components in d = 4."""
        from planetary_polygons.extensions.weyl_tensor import weyl_dimension
        assert weyl_dimension(4) == 10

    def test_grows(self):
        """Components grow with dimension."""
        from planetary_polygons.extensions.weyl_tensor import weyl_dimension
        for d in range(4, 8):
            assert weyl_dimension(d + 1) > weyl_dimension(d)


class TestKKRiemannDetermined:
    """Layer 1: The KK Riemann decomposition is fully determined by N."""

    def test_base_riemann_determined(self):
        """3D Riemann is fixed by Ricci (Weyl = 0 in 3D)."""
        from planetary_polygons.extensions.weyl_tensor import kk_riemann_determined
        for N in [7, 8, 11]:
            result = kk_riemann_determined(N)
            assert result['base_riemann_determined'] is True
            assert result['weyl_components_3d'] == 0

    def test_all_20_determined(self):
        """All 20 independent 4D Riemann components are determined."""
        from planetary_polygons.extensions.weyl_tensor import kk_riemann_determined
        for N in [5, 7, 8, 11]:
            result = kk_riemann_determined(N)
            assert result['all_20_components_determined'] is True
            assert result['weyl_components_4d'] == 10

    def test_mixed_vanishes(self):
        """R^(4)_phi_ijk = 0 for uniform flux on constant-curvature base."""
        from planetary_polygons.extensions.weyl_tensor import kk_riemann_determined
        for N in [7, 8, 11]:
            assert kk_riemann_determined(N)['mixed_vanishes'] is True

    def test_sectional_curvatures_equal_in_3d(self):
        """In 3D, all sectional curvatures equal Lambda3/2 (Schur)."""
        from planetary_polygons.extensions.weyl_tensor import sectional_curvatures_3d
        for N in [7, 8, 11]:
            K = sectional_curvatures_3d(N)
            assert K['all_equal'] is True
            expected = (N**2 - 16) / 32
            assert K['value'] == pytest.approx(expected, rel=1e-12)


class TestRadionAndPerturbations:
    """Layer 2: Perturbation spectrum is gapped."""

    def test_radion_mass_positive(self):
        """The radion is massive for all N >= 3."""
        from planetary_polygons.extensions.weyl_tensor import radion_mass_squared
        for N in range(3, 20):
            m2 = radion_mass_squared(N)
            assert m2 > 0, f"Radion tachyonic at N={N}"

    def test_radion_mass_formula(self):
        """V''(1) = N^2/4."""
        from planetary_polygons.extensions.weyl_tensor import radion_mass_squared
        assert radion_mass_squared(7) == pytest.approx(49 / 4)
        assert radion_mass_squared(11) == pytest.approx(121 / 4)

    def test_radion_mass_scales_N2(self):
        """Radion mass ~ N^2 at large N."""
        from planetary_polygons.extensions.weyl_tensor import radion_mass_squared
        ratio = radion_mass_squared(20) / radion_mass_squared(10)
        assert ratio == pytest.approx(4.0, rel=1e-10)

    def test_radion_potential_minimum(self):
        """The flux potential V(sigma) has minimum at sigma = 1."""
        from planetary_polygons.extensions.weyl_tensor import radion_potential
        for N in [7, 8, 11]:
            V_min = radion_potential(N, 1.0)
            assert V_min == pytest.approx(0, abs=1e-15)
            # Nearby points have higher potential
            assert radion_potential(N, 0.9) > 0
            assert radion_potential(N, 1.1) > 0

    def test_graviphoton_gapped(self):
        """The graviphoton has no zero mode on H^2/Z_N."""
        from planetary_polygons.extensions.weyl_tensor import graviphoton_min_eigenvalue
        for N in range(3, 15):
            assert graviphoton_min_eigenvalue(N) > 0

    def test_all_sectors_gapped(self):
        """All three KK perturbation sectors are gapped."""
        from planetary_polygons.extensions.weyl_tensor import perturbation_spectrum_gapped
        for N in range(3, 20):
            result = perturbation_spectrum_gapped(N)
            assert result['all_sectors_gapped'] is True


class TestFGTermination:
    """Layer 3: Fefferman-Graham expansion terminates."""

    def test_fg_terminates_d2(self):
        """For d=2 boundary (AdS_3), FG terminates at order 1."""
        from planetary_polygons.extensions.weyl_tensor import fg_expansion_order
        assert fg_expansion_order(d_boundary=2) == 1

    def test_fg_terminates_d4(self):
        """For d=4 boundary (AdS_5), FG terminates at order 2."""
        from planetary_polygons.extensions.weyl_tensor import fg_expansion_order
        assert fg_expansion_order(d_boundary=4) == 2

    def test_fg_does_not_terminate_d3(self):
        """For d=3 boundary (AdS_4), FG does NOT terminate."""
        from planetary_polygons.extensions.weyl_tensor import fg_expansion_order
        assert fg_expansion_order(d_boundary=3) is None

    def test_bulk_metric_unique(self):
        """Given boundary data, the bulk 3D metric is unique."""
        from planetary_polygons.extensions.weyl_tensor import fg_bulk_determined
        for N in [7, 8, 11]:
            result = fg_bulk_determined(N)
            assert result['unique'] is True
            assert result['fg_order'] == 1
            assert result['boundary_dim'] == 2


class TestFullRiemannDetermined:
    """Integration: all three layers combine to determine the Riemann tensor."""

    def test_full_determination(self):
        """The full 4D Riemann tensor is determined by N."""
        from planetary_polygons.extensions.weyl_tensor import full_riemann_determined
        for N in [5, 7, 8, 11, 15]:
            result = full_riemann_determined(N)
            assert result['full_riemann_determined'] is True

    def test_layers_independent(self):
        """Each layer independently holds."""
        from planetary_polygons.extensions.weyl_tensor import full_riemann_determined
        result = full_riemann_determined(7)
        assert result['layer1_background'] is True
        assert result['layer2_perturbations'] is True
        assert result['layer3_nonlinear'] is True
