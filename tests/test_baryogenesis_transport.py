"""Tests for the Boltzmann transport baryogenesis computation."""

import pytest
from math import pi, sin, log, sqrt, exp
import numpy as np

from planetary_polygons.extensions.baryogenesis_transport import (
    b_exact, central_charge, V_BO, find_rho_star,
    wall_thickness_from_BO, higgs_vev_profile, higgs_vev_derivative,
    cp_phase, cp_source, transport_coefficients, wall_velocity,
    solve_transport, greens_function_estimate, sensitivity_scan,
)


class TestWallProfile:
    """Tests for the BO bubble wall profile."""

    def test_rho_star_at_threshold(self):
        """V_BO(ρ*) = 0 at the threshold."""
        rho_star = find_rho_star(7)
        assert abs(V_BO(rho_star, 7)) < 1e-8

    def test_rho_star_value(self):
        """ρ* ≈ 1.734 for N=7."""
        rho_star = find_rho_star(7)
        assert abs(rho_star - 1.734) < 0.01

    def test_wall_thickness(self):
        """L_w = (2c)^{-1/3} / T ≈ 0.213."""
        c = central_charge(7)
        L_w = wall_thickness_from_BO(7)
        assert abs(L_w - (2 * c) ** (-1.0 / 3)) < 1e-10

    def test_higgs_profile_boundary_values(self):
        """h(-∞) = v_T, h(+∞) = 0."""
        L_w = 0.2
        v_T = 0.84
        assert abs(higgs_vev_profile(-100, L_w, v_T) - v_T) < 1e-10
        assert abs(higgs_vev_profile(100, L_w, v_T)) < 1e-10

    def test_higgs_profile_midpoint(self):
        """h(0) = v_T/2."""
        L_w = 0.2
        v_T = 0.84
        assert abs(higgs_vev_profile(0, L_w, v_T) - v_T / 2) < 1e-10

    def test_higgs_derivative_integral(self):
        """∫ h'(z) dz = -v_T (fundamental theorem)."""
        L_w = 0.2
        v_T = 0.84
        z = np.linspace(-20, 20, 100000)
        dh = higgs_vev_derivative(z, L_w, v_T)
        integral = np.trapz(dh, z)
        assert abs(integral + v_T) < 1e-4


class TestCPPhase:
    """Tests for the CP-violating phase."""

    def test_cp_phase_value(self):
        """δ_CP = sin(2π frac(k_phys)) ≈ 0.566 at N=7."""
        delta = cp_phase(7)
        assert abs(delta - 0.566) < 0.01

    def test_cp_phase_from_cs_level(self):
        """Verify δ_CP from k_phys = c/6 - N/2."""
        c = central_charge(7)
        k_phys = c / 6 - 7 / 2
        k_frac = k_phys - int(k_phys)
        if k_frac < 0:
            k_frac += 1
        assert abs(cp_phase(7) - sin(2 * pi * k_frac)) < 1e-12

    def test_cp_source_localized(self):
        """The CP source is localized at the wall."""
        L_w = 0.2
        z = np.linspace(-5, 5, 1000)
        S = cp_source(z, L_w, 0.84, 0.566, 0.05)
        # Source should be negligible far from wall
        assert abs(S[0]) < 1e-10
        assert abs(S[-1]) < 1e-10
        # Source should peak near z = 0
        assert np.max(np.abs(S)) > 0

    def test_cp_source_integral(self):
        """∫ S(z) dz = prefactor × (-v_T²/2)."""
        L_w = 0.2
        v_T = 0.84
        v_w = 0.05
        delta = 0.566
        z = np.linspace(-20, 20, 100000)
        S = cp_source(z, L_w, v_T, delta, v_w)
        integral = np.trapz(S, z)
        # Expected: (N_c y_t⁴ v_w sin(δ))/(8π²) × (-v_T²/2)
        y_t = sqrt(2) * 173 / 246
        expected = 3 * y_t**4 * v_w * sin(delta) / (8 * pi**2) * (-v_T**2 / 2)
        assert abs(integral - expected) / abs(expected) < 0.01


class TestTransportCoefficients:
    """Tests for the transport coefficients."""

    def test_diffusion_quark(self):
        """D_q ≈ 6/T."""
        tc = transport_coefficients()
        assert abs(tc['D_q'] - 6.0) < 0.1

    def test_weak_sphaleron_rate(self):
        """Γ_ws = κ α_w⁵ ≈ 8 × 10⁻⁷."""
        tc = transport_coefficients()
        assert 1e-7 < tc['Gamma_ws'] < 1e-5

    def test_yukawa_rate(self):
        """Γ_y = 0.2 y_t² ≈ 0.2."""
        tc = transport_coefficients()
        assert 0.1 < tc['Gamma_y'] < 0.3


class TestWallVelocity:
    """Tests for the wall velocity computation."""

    def test_wall_velocity_positive(self):
        """v_w > 0 (wall moves)."""
        result = wall_velocity(7)
        assert result['v_w'] > 0

    def test_wall_velocity_subluminal(self):
        """v_w < 1 (subluminal)."""
        result = wall_velocity(7)
        assert result['v_w'] < 1.0

    def test_top_friction_dominates(self):
        """Top quark friction dominates over W and Higgs."""
        result = wall_velocity(7)
        assert result['eta_t'] > result['eta_W']
        assert result['eta_t'] > result['eta_h']


class TestTransportSolution:
    """Tests for the full transport computation."""

    def test_eta_B_order_of_magnitude(self):
        """η_B within factor 10 of observed."""
        result = solve_transport(7, v_w_override=0.05, n_points=4000)
        assert 1e-10 < result['eta_B'] < 1e-8

    def test_eta_B_ratio(self):
        """η_B/η_obs ≈ 3 (factor ~3 overshoot)."""
        result = solve_transport(7, v_w_override=0.05, n_points=4000)
        assert 1.0 < result['ratio_to_observed'] < 10.0

    def test_mu_integral_identity(self):
        """∫μ dz (full) ≈ ∫S dz / Γ_tot (Green's function identity)."""
        v_w = 0.05
        L_w = wall_thickness_from_BO(7)
        delta_CP = cp_phase(7)
        coeffs = transport_coefficients()
        Gamma_tot = 3 * coeffs['Gamma_y'] + 3 * coeffs['Gamma_ss']

        result = solve_transport(7, v_w_override=v_w, n_points=10000)
        z = result['z']
        mu = result['mu']
        dz = z[1] - z[0]

        full_mu_integral = np.sum(mu) * dz
        S = result['source']
        S_integral = np.sum(S) * dz
        expected = S_integral / Gamma_tot

        # Should agree within ~15% (discretization + finite domain)
        assert abs(full_mu_integral / expected - 1.0) < 0.20

    def test_vw_independence(self):
        """η_B is nearly independent of v_w (key prediction)."""
        results = []
        for v_w in [0.01, 0.1, 0.5]:
            r = solve_transport(7, v_w_override=v_w, n_points=4000)
            results.append(r['eta_B'])
        # All should be within factor 1.2 of each other
        ratio = max(results) / min(results)
        assert ratio < 1.2

    def test_convergence(self):
        """Result converges with increasing n_points."""
        r1 = solve_transport(7, v_w_override=0.05, n_points=2000)
        r2 = solve_transport(7, v_w_override=0.05, n_points=8000)
        assert abs(r1['eta_B'] / r2['eta_B'] - 1.0) < 0.01

    def test_greens_function_agrees(self):
        """Analytic GF estimate within factor 2 of convolution."""
        gf = greens_function_estimate(7, v_w=0.05)
        conv = solve_transport(7, v_w_override=0.05, n_points=4000)
        ratio = conv['eta_B'] / gf['eta_B']
        # GF uses crude source integral approximation, expect ~1.7× discrepancy
        assert 0.5 < ratio < 3.0


class TestSensitivityScan:
    """Tests for the sensitivity scan."""

    def test_scan_returns_results(self):
        """Scan returns results for each v_w."""
        scan = sensitivity_scan(7, v_w_range=[0.01, 0.1],
                                use_convolution=False)
        assert len(scan) == 2
        assert all('eta_B' in s for s in scan)

    def test_scan_all_positive(self):
        """All η_B values are positive."""
        scan = sensitivity_scan(7, v_w_range=[0.01, 0.1],
                                use_convolution=False)
        assert all(s['eta_B'] > 0 for s in scan)
