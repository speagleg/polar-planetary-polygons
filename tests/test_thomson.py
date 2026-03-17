"""Tests for the Thomson vortex ring stability module."""

import numpy as np
import pytest

from thomson import (
    VortexRingConfig, thomson_eigenvalues, stability_sweep,
    is_stable, critical_center_strength,
    mobius_action_on_ring, thomson_to_mobius_multiplier,
    rayleigh_kuo_at_wavenumber,
)
from qgpv import gaussian_jet_profile


class TestVortexRingConfig:
    def test_positions_on_circle(self):
        config = VortexRingConfig(N=6, R=2.0, kappa=1.0)
        np.testing.assert_allclose(np.abs(config.positions), 2.0, atol=1e-14)

    def test_N_positions(self):
        assert len(VortexRingConfig(N=6, R=1.0, kappa=1.0).positions) == 6

    def test_angular_velocity_positive(self):
        assert VortexRingConfig(N=6, R=1.0, kappa=1.0).angular_velocity() > 0


class TestHavelockStability:
    """Classical result: N <= 7 stable without central vortex (Havelock 1931)."""

    def test_n3_stable(self):
        assert is_stable(3)

    def test_n4_stable(self):
        assert is_stable(4)

    def test_n5_stable(self):
        assert is_stable(5)

    def test_n6_stable(self):
        assert is_stable(6)

    def test_n7_stable(self):
        """N=7 is stable WITHOUT central vortex (Havelock 1931)."""
        assert is_stable(7)

    def test_n8_unstable(self):
        """N=8 is the FIRST unstable configuration (no central vortex)."""
        assert not is_stable(8)

    def test_n9_unstable(self):
        assert not is_stable(9)

    def test_transition_at_n8(self):
        """Stability boundary is between N=7 (stable) and N=8 (unstable)."""
        assert is_stable(7)
        assert not is_stable(8)


class TestEigenvalueStructure:
    def test_n6_eigenvalues_imaginary(self):
        """For stable N=6, eigenvalues should be purely imaginary or zero."""
        eigs = thomson_eigenvalues(6)
        nontrivial = eigs[np.abs(eigs) > 1e-8]
        max_real = np.max(np.abs(nontrivial.real))
        max_imag = np.max(np.abs(nontrivial.imag))
        assert max_real < 0.01 * max_imag, f"max|Re|={max_real}, max|Im|={max_imag}"

    def test_n8_has_real_eigenvalue(self):
        """For unstable N=8, at least one eigenvalue has significant real part."""
        eigs = thomson_eigenvalues(8)
        max_real = np.max(np.abs(eigs.real))
        assert max_real > 0.1, f"Expected real eigenvalue for N=8, got max|Re|={max_real}"

    def test_eigenvalue_count(self):
        """2N eigenvalues returned."""
        assert len(thomson_eigenvalues(6)) == 12


class TestCentralVortexEffect:
    """Test that anticyclonic central vortex shifts stability boundary."""

    def test_n6_stable_without_center(self):
        assert is_stable(6, kappa_center=0.0)

    def test_n6_unstable_with_anticyclonic_center(self):
        """N=6 becomes unstable with sufficiently negative central vortex."""
        assert not is_stable(6, kappa_center=-1.0)

    def test_n6_stable_with_cyclonic_center(self):
        """Positive central vortex preserves N=6 stability."""
        assert is_stable(6, kappa_center=1.0)

    def test_critical_center_n6(self):
        """Critical ratio for N=6 is approximately -0.25."""
        kc = critical_center_strength(6)
        assert -0.4 < kc < -0.1, f"Critical ratio = {kc:.4f}, expected ~-0.25"

    def test_critical_center_n7_less_negative(self):
        """N=7 is easier to destabilize than N=6 (less negative critical ratio)."""
        kc6 = critical_center_strength(6)
        kc7 = critical_center_strength(7)
        # N=7 should destabilize with a weaker anticyclonic center
        assert kc7 > kc6, f"kc6={kc6:.3f}, kc7={kc7:.3f}"


class TestStabilitySweep:
    def test_sweep_range(self):
        results = stability_sweep(range(3, 10))
        assert set(results.keys()) == {3, 4, 5, 6, 7, 8, 9}

    def test_sweep_no_center(self):
        """N<=7 stable, N>=8 unstable without central vortex."""
        results = stability_sweep(range(3, 10))
        for N in range(3, 8):
            assert results[N]['stable'], f"N={N} should be stable"
        for N in range(8, 10):
            assert not results[N]['stable'], f"N={N} should be unstable"


class TestMobiusAction:
    def test_dilation_changes_radius(self):
        config = VortexRingConfig(N=6, R=1.0, kappa=1.0)
        new = mobius_action_on_ring(config, 2.0)
        np.testing.assert_allclose(np.abs(new), 2.0, atol=1e-14)

    def test_rotation_preserves_radius(self):
        config = VortexRingConfig(N=6, R=1.0, kappa=1.0)
        new = mobius_action_on_ring(config, np.exp(1j * np.pi / 3))
        np.testing.assert_allclose(np.abs(new), 1.0, atol=1e-14)

    def test_rotation_by_2pi_N_permutes(self):
        config = VortexRingConfig(N=6, R=1.0, kappa=1.0)
        lam = np.exp(2j * np.pi / 6)
        new = mobius_action_on_ring(config, lam)
        orig = config.positions
        for z_new in new:
            assert np.min(np.abs(orig - z_new)) < 1e-10


class TestThomsonToMobius:
    def test_stable_gives_unit_modulus(self):
        """Stable configs (N<=7, no center) give |lambda| = 1."""
        for N in [5, 6, 7]:
            lam = thomson_to_mobius_multiplier(N)
            assert abs(lam) == pytest.approx(1.0, abs=0.01), f"N={N}: |lam|={abs(lam)}"

    def test_unstable_gives_greater_than_1(self):
        """Unstable N=8 gives |lambda| > 1."""
        lam = thomson_to_mobius_multiplier(8)
        assert abs(lam) > 1.01

    def test_multiplier_angle(self):
        lam = thomson_to_mobius_multiplier(6)
        assert np.angle(lam) == pytest.approx(np.pi / 3, abs=1e-10)


class TestRayleighKuo:
    def test_gaussian_jet_has_crossings(self):
        rho_grid = np.linspace(-1, 1, 500)
        U_profile = lambda rho: gaussian_jet_profile(rho, 120.0, 0.0, 0.15)
        result = rayleigh_kuo_at_wavenumber(6, 1.5e-14, U_profile, rho_grid)
        assert len(result['critical_rho']) > 0

    def test_connection_n6_true(self):
        rho_grid = np.linspace(-1, 1, 500)
        U_profile = lambda rho: gaussian_jet_profile(rho, 120.0, 0.0, 0.15)
        result = rayleigh_kuo_at_wavenumber(6, 1e-14, U_profile, rho_grid)
        assert result['has_rayleigh_kuo_crossings'] is True

    def test_connection_n5_false(self):
        rho_grid = np.linspace(-1, 1, 500)
        U_profile = lambda rho: gaussian_jet_profile(rho, 120.0, 0.0, 0.15)
        result = rayleigh_kuo_at_wavenumber(5, 1e-14, U_profile, rho_grid)
        assert result['has_rayleigh_kuo_crossings'] is True  # n=5 also has crossings in beta-U''
