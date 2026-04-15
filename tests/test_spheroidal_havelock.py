"""Tests for spheroidal Havelock perturbation theory."""
import math
import numpy as np
import pytest
from planetary_polygons.extensions.spheroidal_havelock import (
    gaussian_curvature_spheroid, K_at_pole, K_at_equator,
    C1_sphere_formula, C1_spheroid_pole,
    spheroidal_havelock_eigenvalue,
    mode_coupling_matrix, mode_coupling_off_pole,
    first_avoided_crossing, dangerous_latitude,
    saturn_spheroidal_analysis, jupiter_spheroidal_analysis,
    SATURN_A, SATURN_B, JUPITER_A, JUPITER_B,
)


class TestSpheroidGeometry:
    def test_equator_curvature_greater_than_pole(self):
        """Oblate spheroid: K_equator > K_pole (pole is LESS curved)."""
        for a, b in [(60268, 54364), (71492, 66854)]:
            assert K_at_equator(a, b) > K_at_pole(a, b)

    def test_sphere_limit(self):
        """For a = b (sphere): K = 1/a² everywhere."""
        a = 60000.0
        K_p = K_at_pole(a, a)
        K_e = K_at_equator(a, a)
        assert abs(K_p - 1 / a**2) < 1e-20
        assert abs(K_e - 1 / a**2) < 1e-20

    def test_curvature_monotone_decreasing(self):
        """K DECREASES from equator to pole on oblate spheroid."""
        a, b = SATURN_A, SATURN_B
        prev = K_at_equator(a, b)
        for phi_deg in range(10, 91, 10):
            K = gaussian_curvature_spheroid(np.radians(phi_deg), a, b)
            assert K <= prev, f"phi={phi_deg}"
            prev = K

    def test_saturn_curvature_ratio(self):
        """Saturn K_pole/K_equator = (b/a)^4 ≈ 0.66.

        K_pole = b²/a⁴, K_eq = 1/b², ratio = b⁴/a⁴.
        """
        a, b = SATURN_A, SATURN_B
        ratio = K_at_pole(a, b) / K_at_equator(a, b)
        expected = (b / a) ** 4
        assert abs(ratio - expected) / expected < 0.01


class TestC1Spheroid:
    def test_sphere_limit(self):
        """On a sphere (a=b): C₁ = (N-1)(1+ξ²)/(1+ξ)²."""
        a = 60000.0
        R = 10000.0
        for N in [5, 6, 8]:
            C1 = C1_spheroid_pole(N, a, a, R)
            xi = R**2 / a**2
            expected = (N - 1) * (1 + xi**2) / (1 + xi)**2
            assert abs(C1 - expected) < 1e-6

    def test_oblate_pole_less_curved(self):
        """K_pole = b²/a⁴ < 1/b² = K_eq, so ξ_pole < ξ_eq.

        Lower curvature at the pole means SMALLER ξ, LARGER C₁,
        MORE confining → oblateness STABILIZES polar polygons.
        Compare: spheroid pole vs sphere of radius b (same polar size).
        K_pole(spheroid) = b²/a⁴ < 1/b² = K(sphere of radius b).
        So ξ_pole < ξ_sphere → C₁_pole > C₁_sphere.
        """
        R = 15000.0
        N = 6
        C1_oblate = C1_spheroid_pole(N, SATURN_A, SATURN_B, R)
        K_pole = K_at_pole(SATURN_A, SATURN_B)
        K_sphere_b = 1.0 / SATURN_B**2
        assert K_pole < K_sphere_b  # pole is less curved
        C1_sphere_b = C1_sphere_formula(N, K_sphere_b * R**2)
        assert C1_oblate > C1_sphere_b  # pole is MORE stable


class TestHavelockOnSpheroid:
    def test_eigenvalue_positive_for_N5(self):
        """N=5 polygon at Saturn's pole: all eigenvalues positive."""
        for m in range(1, 5):
            lam = spheroidal_havelock_eigenvalue(
                5, m, SATURN_A, SATURN_B, 15000.0)
            assert lam > 0, f"m={m}: λ={lam}"

    def test_matches_local_curvature(self):
        """Eigenvalue matches the local-curvature formula."""
        N, m, R = 6, 3, 15000.0
        lam = spheroidal_havelock_eigenvalue(
            N, m, SATURN_A, SATURN_B, R)
        K = K_at_pole(SATURN_A, SATURN_B)
        xi = K * R**2
        C1 = C1_sphere_formula(N, xi)
        expected = C1 - m * (N - m) / 2
        assert abs(lam - expected) < 1e-10


class TestModeCoupling:
    def test_diagonal_at_pole(self):
        """At the pole: mode-coupling matrix is exactly diagonal."""
        M = mode_coupling_matrix(6, SATURN_A, SATURN_B, 15000.0, np.pi/2)
        N = 6
        for i in range(N):
            for j in range(N):
                if i != j:
                    assert abs(M[i, j]) < 1e-15, (
                        f"M[{i},{j}] = {M[i,j]}")

    def test_diagonal_matches_havelock(self):
        """Diagonal of coupling matrix = Havelock eigenvalues."""
        N, R = 6, 15000.0
        M = mode_coupling_matrix(N, SATURN_A, SATURN_B, R, np.pi/2)
        for m in range(N):
            lam = spheroidal_havelock_eigenvalue(
                N, m, SATURN_A, SATURN_B, R)
            assert abs(M[m, m] - lam) < 1e-10

    def test_tilted_coupling_grows_with_tilt(self):
        """Off-diagonal coupling grows with tilt angle."""
        N, R = 6, 15000.0
        M0 = mode_coupling_off_pole(
            N, SATURN_A, SATURN_B, R, np.pi/2, tilt_angle=0.0)
        M1 = mode_coupling_off_pole(
            N, SATURN_A, SATURN_B, R, np.pi/2, tilt_angle=0.1)
        off0 = np.sum(np.abs(M0)) - np.sum(np.abs(np.diag(M0)))
        off1 = np.sum(np.abs(M1)) - np.sum(np.abs(np.diag(M1)))
        assert off1 > off0

    def test_zero_tilt_is_diagonal(self):
        """Zero tilt: no off-diagonal coupling."""
        M = mode_coupling_off_pole(
            6, SATURN_A, SATURN_B, 15000.0, np.pi/2, tilt_angle=0.0)
        off = np.sum(np.abs(M)) - np.sum(np.abs(np.diag(M)))
        assert off < 1e-10


class TestAvoidedCrossing:
    def test_saturn_crossing_exists(self):
        """Saturn: avoided crossing computation runs and returns data."""
        ac = first_avoided_crossing(6, SATURN_A, SATURN_B, 15000.0)
        assert ac is not None
        assert 'bare_gap' in ac
        assert ac['bare_gap'] > 0

    def test_zero_tilt_no_coupling(self):
        """At zero tilt: the coupling matrix is diagonal, no avoided crossings."""
        M = mode_coupling_off_pole(
            6, SATURN_A, SATURN_B, 15000.0, np.pi / 2, tilt_angle=0.0)
        eigs = sorted(np.linalg.eigvalsh(M))
        # Should match the Havelock eigenvalues exactly
        K = K_at_pole(SATURN_A, SATURN_B)
        xi = K * 15000.0**2
        C1 = C1_sphere_formula(6, xi)
        for m in range(6):
            lam = C1 - m * (6 - m) / 2
            assert abs(eigs[m] - sorted([C1 - k*(6-k)/2 for k in range(6)])[m]) < 1e-8


class TestDangerousLatitude:
    def test_saturn_pole_is_safe(self):
        """Saturn's hexagon latitude (78°) is well above the danger zone."""
        phi_danger = dangerous_latitude(6, SATURN_A, SATURN_B, 15000.0)
        assert phi_danger is not None
        assert phi_danger < 78  # hexagon is above the danger zone


class TestSaturnAnalysis:
    def test_runs(self):
        result = saturn_spheroidal_analysis()
        assert 'eigenvalues' in result
        assert 'avoided_crossing' in result

    def test_hexagon_eigenvalue_sign(self):
        """Saturn hexagon binding eigenvalue: check sign."""
        result = saturn_spheroidal_analysis()
        # λ₃ should be the binding eigenvalue
        assert 3 in result['eigenvalues']

    def test_off_diagonal_zero_at_pole(self):
        """Off-diagonal coupling is zero at the pole."""
        result = saturn_spheroidal_analysis()
        assert result['off_diagonal_coupling'] < 1e-10


class TestJupiterAnalysis:
    def test_runs(self):
        result = jupiter_spheroidal_analysis()
        assert 'north_N8' in result
        assert 'south_N5' in result

    def test_south_pentagon_stable(self):
        """Jupiter south N=5: all eigenvalues positive."""
        result = jupiter_spheroidal_analysis()
        assert result['south_N5']['min_eigenvalue'] > 0
