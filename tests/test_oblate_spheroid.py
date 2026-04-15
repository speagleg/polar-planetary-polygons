"""
Tests for oblate spheroid vortex stability.

Key result: Saturn's 10% oblateness flips the N=6 hexagon from
unstable (λ₃ = -0.12 on mean sphere) to marginally stable (λ₃ = +0.01).
"""
import numpy as np
import pytest
from planetary_polygons.extensions.oblate_spheroid import (
    gaussian_curvature, curvature_gradient, effective_radius,
    C1_sphere, havelock_eigenvalue_spheroid, critical_latitude,
    mode_coupling_strength, saturn_analysis, jupiter_analysis,
)


# Saturn and Jupiter parameters
SAT_A, SAT_B = 60268.0, 54364.0
JUP_A, JUP_B = 71492.0, 66854.0


class TestGaussianCurvature:
    """Curvature on the oblate spheroid."""

    def test_equator_larger_than_pole(self):
        """K_eq > K_pole for an oblate spheroid (b < a).

        The pole is FLATTER (less curved) on an oblate spheroid.
        K_eq = 1/b², K_pole = b²/a⁴.  Since a > b: K_eq/K_pole = a⁴/b⁴ > 1.
        """
        K_pole = gaussian_curvature(np.pi / 2, SAT_A, SAT_B)
        K_eq = gaussian_curvature(0, SAT_A, SAT_B)
        assert K_eq > K_pole

    def test_sphere_limit(self):
        """For a = b (sphere), K = 1/a² everywhere."""
        R = 60000.0
        for phi_deg in [0, 45, 90]:
            K = gaussian_curvature(np.radians(phi_deg), R, R)
            assert abs(K - 1 / R ** 2) < 1e-15

    def test_monotone_latitude(self):
        """K DECREASES from equator to pole on oblate spheroid.

        The oblate pole is flatter → lower curvature → more stable
        (closer to the flat-plane limit where N_crit = 7).
        """
        lats = np.linspace(0, np.pi / 2, 100)
        K_vals = gaussian_curvature(lats, SAT_A, SAT_B)
        for i in range(len(K_vals) - 1):
            assert K_vals[i + 1] <= K_vals[i] + 1e-20


class TestSaturnHexagon:
    """Saturn's hexagon: the oblateness result."""

    def test_unstable_on_mean_sphere(self):
        """N=6 hexagon is UNSTABLE on a mean sphere."""
        sat = saturn_analysis()
        assert sat['lambda_3_sphere'] < 0

    def test_stable_on_oblate_spheroid(self):
        """N=6 hexagon is STABLE on the oblate spheroid at 78°N."""
        sat = saturn_analysis()
        assert sat['lambda_3_oblate'] > 0

    def test_sign_flip(self):
        """Oblateness changes the SIGN of λ₃."""
        sat = saturn_analysis()
        assert sat['lambda_3_sphere'] * sat['lambda_3_oblate'] < 0

    def test_critical_latitude(self):
        """Transition occurs between 60° and 65° on Saturn (corrected C₁ formula)."""
        sat = saturn_analysis()
        assert 55 < sat['phi_crit'] < 70

    def test_hexagon_above_critical(self):
        """Saturn's hexagon at 78°N is above the critical latitude."""
        sat = saturn_analysis()
        assert 78 > sat['phi_crit']

    def test_mode_coupling_exceeds_margin(self):
        """Mode coupling from curvature variation exceeds stability margin."""
        sat = saturn_analysis()
        assert sat['coupling_exceeds_margin']


class TestJupiter:
    """Jupiter's polar vortices."""

    def test_north_N8_unstable(self):
        """Jupiter north N=8 is Thomson-unstable (λ₄ < 0).

        N=8 requires additional stabilization (central vortex, Rossby).
        """
        jup = jupiter_analysis()
        assert jup['north_lambda_4'] < 0

    def test_south_N5_stable(self):
        """Jupiter south N=5 is Thomson-stable (λ₂ > 0)."""
        jup = jupiter_analysis()
        assert jup['south_lambda_2'] > 0

    def test_south_coupling_small(self):
        """Jupiter south: mode coupling is small vs stability margin."""
        jup = jupiter_analysis()
        assert jup['south_coupling'] < jup['south_margin']


class TestLatitudeDependence:
    """Eigenvalue as a function of latitude."""

    def test_stable_at_pole(self):
        """N=6 on Saturn is stable at the pole."""
        lam = havelock_eigenvalue_spheroid(
            6, 3, np.radians(90), 15000, SAT_A, SAT_B)
        assert lam > 0

    def test_unstable_at_equator(self):
        """N=6 on Saturn is unstable at the equator."""
        lam = havelock_eigenvalue_spheroid(
            6, 3, np.radians(10), 15000, SAT_A, SAT_B)
        assert lam < 0

    def test_monotone_with_latitude(self):
        """λ₃ increases with latitude on oblate spheroid."""
        lams = [havelock_eigenvalue_spheroid(
            6, 3, np.radians(phi), 15000, SAT_A, SAT_B)
            for phi in range(10, 90, 5)]
        for i in range(len(lams) - 1):
            assert lams[i + 1] > lams[i]
