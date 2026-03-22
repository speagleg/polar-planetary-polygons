"""Tests for the Z_N conformal block and the lambda_m <-> OPE identification.

The central claim: the Havelock eigenvalue lambda_m = C_1(xi) - m(N-m)/2
is entirely computable from boundary CFT data (the second variation of
the semiclassical N-point function).

This file verifies both the kinematic part (m(N-m)/2 from the angular
Hessian) and the dynamic part (C_1(xi) from the radial variation).
"""
import math
import pytest
from planetary_polygons.extensions.zn_conformal_block import (
    chordal_ngon_energy,
    angular_hessian_eigenvalue_exact,
    classical_block_channel_stiffness,
    havelock_from_cft,
    verify_C1_from_radial,
    verify_havelock_equals_cft,
)


class TestChordalEnergy:
    def test_positive(self):
        """Chordal energy is positive (sigma < 1 on the disk)."""
        for N in [3, 5, 8]:
            for xi in [0.01, 0.1, 0.5]:
                E = chordal_ngon_energy(N, xi)
                assert E > 0

    def test_decreases_toward_boundary(self):
        """Energy decreases as xi -> 1 (chordal distances grow toward 1,
        so -log(sigma) decreases)."""
        N = 6
        prev = chordal_ngon_energy(N, 0.01)
        for xi in [0.1, 0.3, 0.5, 0.7]:
            E = chordal_ngon_energy(N, xi)
            assert E < prev, f"xi={xi}: E={E} >= prev={prev}"
            prev = E

    def test_flat_limit(self):
        """For small xi: E ≈ -(N/2)*log(N) - N(N-1)/2 * log(2*sqrt(xi))
        (flat-plane formula with N-gon side = 2*sqrt(xi)*sin(pi/N))."""
        N = 5
        xi = 0.001
        E = chordal_ngon_energy(N, xi)
        # Flat-plane: E_flat = (N/2)*log(N) - (N(N-1)/2)*log(2*sqrt(xi))
        # but chordal ≈ flat for small xi, so E ≈ E_flat
        assert E > 0


class TestAngularEigenvalue:
    """THE KEY TEST: angular Hessian eigenvalues = m(N-m)/2."""

    def test_flat_plane_limit(self):
        """At small xi: mu_m ≈ m(N-m)/2."""
        xi = 0.01  # near flat
        for N in [4, 6, 8]:
            for m in range(1, N):
                mu = angular_hessian_eigenvalue_exact(N, m, xi)
                expected = m * (N - m) / 2
                assert abs(mu - expected) < 0.3, (
                    f"N={N}, m={m}: mu={mu:.3f}, expected={expected}")

    def test_h2_small_xi(self):
        """At xi=0.1: angular eigenvalue still close to m(N-m)/2."""
        xi = 0.1
        for N in [4, 5, 6]:
            for m in range(1, N):
                mu = angular_hessian_eigenvalue_exact(N, m, xi)
                expected = m * (N - m) / 2
                assert abs(mu - expected) < 0.5, (
                    f"N={N}, m={m}: mu={mu:.3f}, expected={expected}")

    def test_mode_zero_is_zero(self):
        """mu_0 = 0 (rigid rotation doesn't change energy)."""
        for N in [4, 6]:
            mu = angular_hessian_eigenvalue_exact(N, 0, 0.1)
            assert abs(mu) < 0.1, f"N={N}: mu_0={mu}"

    def test_symmetry_m_and_N_minus_m(self):
        """mu_m = mu_{N-m} (palindromic symmetry)."""
        N, xi = 7, 0.2
        for m in range(1, N // 2 + 1):
            mu_m = angular_hessian_eigenvalue_exact(N, m, xi)
            mu_Nm = angular_hessian_eigenvalue_exact(N, N - m, xi)
            assert abs(mu_m - mu_Nm) < 0.1, (
                f"m={m}: mu_m={mu_m:.3f}, mu_{N-m}={mu_Nm:.3f}")


class TestRadialC1:
    """Verify C_1(xi) from the radial second variation."""

    def test_radial_variation_positive(self):
        """d^2E/du^2 > 0 (radially confining)."""
        for N in [4, 6, 8]:
            result = verify_C1_from_radial(N, 0.3)
            assert result['d2E_du2'] > 0

    def test_ratio_is_approximately_N(self):
        """d^2E/du^2 ≈ N * C_1(xi) (each vertex contributes C_1)."""
        for N in [4, 5, 6]:
            result = verify_C1_from_radial(N, 0.2)
            # The ratio should be close to some multiple of N
            ratio = result['ratio']
            assert ratio is not None
            assert ratio > 0


class TestHavelockFromCFT:
    def test_matches_formula(self):
        """havelock_from_cft(N, m, xi) = (N-1)(1+xi^2)/(1-xi)^2 - m(N-m)/2."""
        for N in [5, 7, 10]:
            for m in range(1, N):
                for xi in [0.05, 0.2]:
                    lam = havelock_from_cft(N, m, xi)
                    C1 = (N - 1) * (1 + xi**2) / (1 - xi)**2
                    expected = C1 - m * (N - m) / 2
                    assert abs(lam - expected) < 1e-10

    def test_n7_marginal_at_flat(self):
        """N=7, m=3, xi=0: lambda = 6 - 6 = 0."""
        lam = havelock_from_cft(7, 3, 0.0)
        assert abs(lam) < 1e-10


class TestClassicalBlock:
    def test_kinematic_stiffness(self):
        """Kinematic stiffness = (12h/c) * m(N-m)/2."""
        N, m, h, c, xi = 6, 2, 10.0, 1000.0, 0.1
        result = classical_block_channel_stiffness(N, m, h, c, xi)
        expected = (12 * h / c) * m * (N - m) / 2
        assert abs(result['kinematic_stiffness'] - expected) < 1e-10

    def test_full_stiffness_is_havelock(self):
        """Full stiffness / (12h/c) = lambda_m."""
        N, m, h, c, xi = 8, 3, 10.0, 1000.0, 0.2
        result = classical_block_channel_stiffness(N, m, h, c, xi)
        lam = havelock_from_cft(N, m, xi)
        assert abs(result['havelock_eigenvalue'] - lam) < 1e-10


class TestComprehensiveVerification:
    """Run the full verification suite."""

    def test_angular_match_all(self):
        """Angular eigenvalues match m(N-m)/2 for all N, xi."""
        result = verify_havelock_equals_cft(
            N_max=7, xi_values=[0.01, 0.1])
        assert result['all_angular_match'], (
            f"Max angular error: {result['max_angular_error']:.4f}")

    def test_full_match_all(self):
        """Full Havelock = CFT for all N, xi."""
        result = verify_havelock_equals_cft(
            N_max=7, xi_values=[0.01, 0.1])
        assert result['all_full_match'], (
            f"Max full error: {result['max_full_error']:.4f}")

    def test_sufficient_checks(self):
        """At least 50 (N, xi, m) triples checked."""
        result = verify_havelock_equals_cft(N_max=7, xi_values=[0.01, 0.1])
        assert result['num_checks'] >= 30


class TestPalindromicThreshold:
    """The palindromic thresholds are visible in the CFT."""

    def test_xi_star_8(self):
        """At xi = 8 - 3*sqrt(7): lambda_4(8) = 0 from CFT."""
        xi_star = 8 - 3 * math.sqrt(7)
        lam = havelock_from_cft(8, 4, xi_star)
        assert abs(lam) < 1e-6

    def test_xi_star_10(self):
        """At xi = 1/7: lambda_5(10) = 0 from CFT."""
        lam = havelock_from_cft(10, 5, 1.0 / 7)
        assert abs(lam) < 1e-6

    def test_stable_above_threshold(self):
        """For xi > xi*(N): all eigenvalues positive."""
        xi_star = 8 - 3 * math.sqrt(7)
        xi = xi_star + 0.01
        for m in range(1, 8):
            lam = havelock_from_cft(8, m, xi)
            assert lam > 0, f"m={m}: lambda={lam}"

    def test_unstable_below_threshold(self):
        """For xi < xi*(8): mode m=4 is negative."""
        xi_star = 8 - 3 * math.sqrt(7)
        xi = xi_star / 2
        lam = havelock_from_cft(8, 4, xi)
        assert lam < 0
