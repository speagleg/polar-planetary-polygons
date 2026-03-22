"""Tests for the polygon-BTZ Euclidean action comparison."""
import math
import pytest
from planetary_polygons.extensions.polygon_btz_action import (
    btz_mass_from_rplus, btz_temperature, btz_entropy,
    btz_rplus_from_mass, btz_action, btz_action_at_hawking_temp,
    cone_mass, cone_action,
    chordal_distance, havelock_energy_h2,
    polygon_total_energy_G, polygon_action,
    polygon_btz_action_difference, transition_temperature,
    hawking_page_temperature,
    C1_h2, havelock_eigenvalue_h2, min_eigenvalue,
    negative_mode_eigenvalue, polygon_onset_xi,
    polygon_btz_entropy_gap,
    decay_channel_analysis, one_loop_bound,
    phase_diagram_row,
)


G = 1.0
ell = 1.0


class TestBTZThermodynamics:
    def test_mass_temperature_consistency(self):
        """M = r_+^2/(8*G*ell^2), T = r_+/(2*pi*ell^2)."""
        r_plus = 1.0
        M = btz_mass_from_rplus(r_plus, G, ell)
        T = btz_temperature(r_plus, ell)
        assert abs(M - 1.0 / 8) < 1e-10
        assert abs(T - 1.0 / (2 * math.pi)) < 1e-10

    def test_rplus_roundtrip(self):
        for M in [0.01, 0.1, 1.0]:
            r = btz_rplus_from_mass(M, G, ell)
            M2 = btz_mass_from_rplus(r, G, ell)
            assert abs(M - M2) < 1e-10

    def test_btz_action_negative(self):
        """BTZ Euclidean action is negative (preferred over vacuum at high T)."""
        for beta in [0.5, 1.0, 2.0]:
            I = btz_action(beta, G, ell)
            assert I < 0

    def test_first_law(self):
        """S = beta*(M - F) = beta*M - I."""
        r_plus = 1.5
        M = btz_mass_from_rplus(r_plus, G, ell)
        T = btz_temperature(r_plus, ell)
        beta = 1.0 / T
        S = btz_entropy(r_plus, G)
        I = btz_action(beta, G, ell)
        # I = beta*F = beta*(M - T*S) = beta*M - S
        assert abs(I - (beta * M - S)) < 1e-8


class TestHawkingPage:
    def test_standard_hp_temperature(self):
        """T_HP = 1/(2*pi*ell)."""
        T_HP = hawking_page_temperature(ell)
        assert abs(T_HP - 1.0 / (2 * math.pi)) < 1e-10

    def test_action_crossing(self):
        """At beta = 2*pi*ell: I_thermal_AdS = I_BTZ."""
        beta_HP = 2 * math.pi * ell
        I_AdS = -beta_HP / (8 * G)  # thermal AdS action
        I_BTZ = btz_action(beta_HP, G, ell)
        assert abs(I_AdS - I_BTZ) < 1e-8

    def test_ads_preferred_low_T(self):
        """Below HP: thermal AdS has lower action."""
        beta = 10.0  # low T
        I_AdS = -beta / (8 * G)
        I_BTZ = btz_action(beta, G, ell)
        assert I_AdS < I_BTZ

    def test_btz_preferred_high_T(self):
        """Above HP: BTZ has lower action."""
        beta = 1.0  # high T
        I_AdS = -beta / (8 * G)
        I_BTZ = btz_action(beta, G, ell)
        assert I_BTZ < I_AdS


class TestConicalSingularity:
    def test_vacuum_limit(self):
        """At Gm = 0: cone action = vacuum action."""
        beta = 5.0
        I_cone = cone_action(beta, 0.0, G, ell)
        I_vac = -beta / (8 * G)
        assert abs(I_cone - I_vac) < 1e-10

    def test_cone_mass_positive(self):
        """Mass above vacuum is positive for Gm > 0."""
        for Gm in [0.01, 0.05, 0.1]:
            assert cone_mass(Gm) > 0

    def test_btz_threshold(self):
        """At Gm = 1/4: alpha = 0, mass = 1/(8G) = BTZ threshold."""
        M = cone_mass(0.25)
        assert abs(M - 1.0 / 8) < 1e-10


class TestChordalDistance:
    def test_symmetry(self):
        """sigma(j,k) = sigma(k,j)."""
        xi = 0.3
        N = 6
        for j in range(N):
            for k in range(j + 1, N):
                s1 = chordal_distance(xi, j, k, N)
                s2 = chordal_distance(xi, k, j, N)
                assert abs(s1 - s2) < 1e-10

    def test_flat_limit(self):
        """At xi -> 0: sigma -> |z_j - z_k| (flat-space distance)."""
        xi = 0.001
        N = 5
        R = math.sqrt(xi)
        for d in range(1, N):
            sigma = chordal_distance(xi, 0, d, N)
            flat = 2 * R * abs(math.sin(math.pi * d / N))
            # sigma ≈ flat for small xi
            assert abs(sigma - flat) / flat < 0.01

    def test_less_than_one(self):
        """Chordal distance is always < 1 on the Poincaré disk."""
        for xi in [0.1, 0.3, 0.5, 0.8]:
            for N in [3, 5, 8]:
                for d in range(1, N):
                    sigma = chordal_distance(xi, 0, d, N)
                    assert 0 < sigma < 1 + 1e-10


class TestPolygonEnergy:
    def test_positive_for_small_Gm(self):
        """Total polygon energy is positive for small Gm."""
        for N in [5, 7, 10]:
            E = polygon_total_energy_G(N, 0.01, 0.1)
            assert E > 0

    def test_binding_is_attractive(self):
        """Interaction energy is negative (attractive)."""
        from planetary_polygons.extensions.polygon_btz_action import (
            polygon_binding_energy)
        for N in [5, 8]:
            V = polygon_binding_energy(N, 0.01, 0.3)
            assert V < 0


class TestTransitionTemperature:
    def test_small_mass_approaches_hp(self):
        """T_c approaches T_HP as mass goes to zero."""
        T_HP = hawking_page_temperature(ell)
        # Very small mass: T_c ≈ T_HP
        T_c = transition_temperature(3, 0.001, G, ell, 0.1)
        assert T_c is not None
        assert abs(T_c - T_HP) / T_HP < 0.1  # within 10%

    def test_decreases_with_mass(self):
        """T_c < T_HP for positive mass."""
        T_HP = hawking_page_temperature(ell)
        for N in [5, 7]:
            T_c = transition_temperature(N, 0.01, G, ell, 0.1)
            assert T_c is not None
            assert T_c < T_HP

    def test_increases_with_N(self):
        """More masses → lower T_c (harder for BTZ to form)...
        actually more mass → higher total energy → T_c decreases."""
        Gm = 0.005
        prev = hawking_page_temperature(ell)
        for N in [4, 6, 8, 10]:
            if Gm >= 1.0 / (4 * N):
                continue
            T_c = transition_temperature(N, Gm, G, ell, 0.1)
            if T_c is not None:
                assert T_c < prev
                prev = T_c


class TestNegativeMode:
    def test_n7_marginal_flat(self):
        """N=7 on flat plane: lambda_3 = 0 (marginal)."""
        m, lam = negative_mode_eigenvalue(7, 0.0)
        assert m == 3
        assert abs(lam) < 1e-10

    def test_n8_unstable_flat(self):
        """N=8 on flat plane: lambda_4 < 0 (unstable)."""
        m, lam = negative_mode_eigenvalue(8, 0.0)
        assert m == 4
        assert lam < 0

    def test_n8_stable_large_xi(self):
        """N=8 on H^2 with large xi: stabilized by curvature."""
        from planetary_polygons.extensions.polygon_btz_action import (
            polygon_onset_xi)
        xi_star = polygon_onset_xi(8)
        assert xi_star is not None
        m, lam = negative_mode_eigenvalue(8, xi_star + 0.01)
        assert lam > 0

    def test_onset_xi_matches_algebraic(self):
        """xi*(8) should match 8 - 3*sqrt(7)."""
        xi_star = polygon_onset_xi(8)
        xi_exact = 8 - 3 * math.sqrt(7)
        assert abs(xi_star - xi_exact) < 1e-6


class TestEntropyGap:
    def test_positive(self):
        """BTZ always has higher entropy than polygon at same energy."""
        for N in [5, 7, 10]:
            gap = polygon_btz_entropy_gap(N, 0.01, 0.1)
            assert gap > 0

    def test_grows_with_N(self):
        """More mass → larger BTZ → larger entropy gap."""
        prev = 0
        for N in [4, 6, 8, 10]:
            gap = polygon_btz_entropy_gap(N, 0.01, 0.1)
            assert gap > prev
            prev = gap


class TestDecayChannel:
    def test_stable_polygon(self):
        """N=5 on H^2: locally stable, no decay."""
        result = decay_channel_analysis(5, 0.1, 0.01)
        assert result['unstable'] is False
        assert result['growth_rate'] == 0

    def test_unstable_polygon(self):
        """N=10 on H^2 (small xi): unstable, definite decay."""
        result = decay_channel_analysis(10, 0.01, 0.01)
        assert result['unstable'] is True
        assert result['growth_rate'] > 0
        assert result['decay_endpoint'] == 'BTZ'

    def test_critical_mode_is_half_N(self):
        """The negative mode is m = N//2."""
        for N in [8, 10, 12]:
            result = decay_channel_analysis(N, 0.01, 0.01)
            assert result['m_crit'] == N // 2


class TestOneLopBound:
    def test_bolza_bound(self):
        """On Bolza surface (lambda_1 ≈ 3.839): bound ≈ 0.052."""
        bound = one_loop_bound(3.839)
        assert abs(bound - 2.0 / (4 * math.pi * 3.839)) < 1e-6
        assert bound < 0.06

    def test_modular_surface(self):
        """On modular surface (lambda_1 ≈ 91.1): bound is tiny."""
        bound = one_loop_bound(91.1)
        assert bound < 0.002


class TestPhaseDiagram:
    def test_n5_stable(self):
        """N=5 on H^2: stable and preferred at low T."""
        row = phase_diagram_row(5, 0.01, ell, 0.1)
        assert row['locally_stable'] is True

    def test_n10_unstable(self):
        """N=10 on H^2 (small xi): unstable."""
        row = phase_diagram_row(10, 0.01, ell, 0.01)
        assert row['locally_stable'] is False

    def test_phase_structure_consistent(self):
        """The phase diagram has consistent structure at small xi."""
        xi = 0.01  # small curvature, near flat-plane limit
        for N in range(3, 12):
            Gm = 0.005
            if Gm >= 1.0 / (4 * N):
                continue
            row = phase_diagram_row(N, Gm, ell, xi)
            if N <= 7:
                assert row['locally_stable'] is True, f"N={N}"
            else:
                assert row['locally_stable'] is False, f"N={N}"
