"""Tests for the AdS3/CFT2 dictionary."""
import math
import pytest
from planetary_polygons.extensions.ads_cft_dictionary import (
    brown_henneaux, mass_to_conformal_dim, conformal_dim_to_mass,
    deficit_angle, max_polygon_mass, max_h_over_c,
    ope_pairwise_energy, ope_pairwise_energy_exact,
    hessian_log_interaction_fourier, havelock_casimir,
    havelock_eigenvalue_flat, C1_flat,
    stability_bound_h_over_c, palindromic_threshold_cft,
)


class TestBulkBoundaryMap:
    def test_brown_henneaux(self):
        assert brown_henneaux(1.0, 1.0) == 1.5
        assert brown_henneaux(10.0, 0.1) == 150.0

    def test_mass_dimension_roundtrip(self):
        """Gm → h → Gm roundtrip (Gm < 1/8 for monotonicity)."""
        for Gm in [0.001, 0.01, 0.05, 0.1, 0.12]:
            c = 100.0
            h = mass_to_conformal_dim(Gm, c)
            Gm_back = conformal_dim_to_mass(h, c)
            assert abs(Gm - Gm_back) < 1e-10

    def test_small_mass_linear(self):
        """For small Gm: h ≈ (2c/3)Gm."""
        c = 1000.0
        Gm = 0.001
        h = mass_to_conformal_dim(Gm, c)
        h_linear = (2 * c / 3) * Gm
        assert abs(h - h_linear) / h_linear < 0.01

    def test_deficit_angle(self):
        assert abs(deficit_angle(0.125) - math.pi) < 1e-10

    def test_max_polygon_mass(self):
        assert max_polygon_mass(4) == 0.0625
        assert max_polygon_mass(8) == 0.03125


class TestOPEEnergy:
    def test_ope_energy_matches_exact(self):
        """Σ log|z_j-z_k| = (N/2)log(N)."""
        for N in [3, 4, 5, 6, 8, 12]:
            E_num = ope_pairwise_energy(N)
            E_exact = ope_pairwise_energy_exact(N)
            assert abs(E_num - E_exact) < 1e-8, f"N={N}"


class TestChiralCasimir:
    """The core dictionary test: T_m = m(N-m) = 2 × Havelock Casimir."""

    def test_fourier_eigenvalue_equals_twice_casimir(self):
        """T_m = m(N-m) for all N and m (the chiral OPE identity)."""
        for N in range(3, 16):
            for m in range(1, N):
                T_m = hessian_log_interaction_fourier(N, m)
                expected = m * (N - m)
                assert abs(T_m - expected) < 1e-8, (
                    f"N={N}, m={m}: T_m={T_m}, expected={expected}")

    def test_havelock_casimir_is_half(self):
        """f(m,N) = m(N-m)/2 = T_m / 2."""
        for N in range(3, 12):
            for m in range(1, N):
                T_m = hessian_log_interaction_fourier(N, m)
                f_m = havelock_casimir(N, m)
                assert abs(f_m - T_m / 2) < 1e-10

    def test_factor_of_2_all_N(self):
        """The factor of 2 holds universally."""
        for N in range(3, 30):
            for m in range(1, N):
                T_m = hessian_log_interaction_fourier(N, m)
                assert abs(T_m - 2 * havelock_casimir(N, m)) < 1e-8

    def test_havelock_eigenvalue_flat(self):
        """λ_m = (N-1) - m(N-m)/2 on the flat plane."""
        for N in range(3, 12):
            for m in range(1, N):
                lam = havelock_eigenvalue_flat(N, m)
                assert abs(lam - ((N - 1) - m * (N - m) / 2)) < 1e-10


class TestStabilityBound:
    def test_stable_flat_N_le_7(self):
        for N in range(3, 8):
            bound = stability_bound_h_over_c(N)
            assert bound['stable_flat'] is True

    def test_unstable_flat_N_ge_8(self):
        for N in range(8, 13):
            bound = stability_bound_h_over_c(N)
            assert bound['stable_flat'] is False

    def test_h_over_c_decreases_with_N(self):
        """Maximum h/c decreases with N (more masses = each lighter)."""
        prev = 1.0
        for N in range(3, 20):
            h_c = max_h_over_c(N)
            assert h_c < prev
            prev = h_c


class TestPalindromicCFT:
    def test_threshold_N8_field(self):
        data = palindromic_threshold_cft(8)
        assert data['field'] == 'Q(sqrt(7))'
        assert abs(data['xi_star'] - (8 - 3 * math.sqrt(7))) < 1e-6

    def test_threshold_N23_golden(self):
        """N=23 threshold is φ⁻² (golden ratio)."""
        phi = (1 + math.sqrt(5)) / 2
        data = palindromic_threshold_cft(23)
        assert abs(data['xi_star'] - 1 / phi**2) < 1e-6

    def test_threshold_C1_equals_fmax(self):
        """At threshold: C₁(ξ*) = f_max(N) exactly."""
        for N in range(8, 16):
            data = palindromic_threshold_cft(N)
            if data['xi_star'] > 0:
                m_crit = N // 2
                f_max = m_crit * (N - m_crit) / 2
                assert abs(data['C1_at_threshold'] - f_max) < 0.01, (
                    f"N={N}: C1={data['C1_at_threshold']}, f_max={f_max}")
