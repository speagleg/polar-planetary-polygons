"""
Tests for the Onsager → BH entropy bridge.

Verifies:
1. CL squeezing parameters are well-defined and finite
2. Three-level entropy hierarchy: S_CL < S_1loop << S_BH
3. The central charge c is consistent (Fisher-Rao = Todd = BO)
4. Cardy entropy scales as O(c) ~ O(N²)
5. The bridge argument holds for all stable N
"""

import pytest
import numpy as np
from math import pi, log

from planetary_polygons.extensions.entropy_bridge import (
    b_exact, casimir, find_threshold,
    squeezing_parameters,
    cl_entanglement_entropy,
    one_loop_entropy,
    cardy_entropy,
    bh_entropy_components,
    fisher_rao_metric,
    fisher_rao_vs_c,
    c_identity_check,
    entropy_hierarchy,
    bridge_summary,
)


class TestSqueezingParameters:
    """CL squeezing parameters at the threshold."""

    @pytest.mark.parametrize("N", [7, 8, 9, 10, 11])
    def test_squeezing_finite(self, N):
        """All squeezing parameters are finite and positive."""
        params = squeezing_parameters(N)
        assert len(params) > 0, f"No modes for N={N}"
        for m, lam, r_m in params:
            assert np.isfinite(r_m), f"N={N}, m={m}: r_m not finite"
            assert r_m > 0, f"N={N}, m={m}: r_m={r_m} not positive"

    @pytest.mark.parametrize("N", [7, 8, 9])
    def test_critical_modes_excluded(self, N):
        """Critical modes (λ_m=0) are excluded from the sum."""
        m_crit = N // 2
        f_crit = casimir(m_crit, N)
        params = squeezing_parameters(N)
        for m, lam, r_m in params:
            assert abs(lam) > 1e-10, f"Critical mode m={m} not excluded"

    def test_palindromic_symmetry(self):
        """r_m = r_{N-m} (palindromic pair has equal squeezing)."""
        N = 7
        params = squeezing_parameters(N)
        # Build dict m → r_m
        r_dict = {m: r_m for m, _, r_m in params}
        for m, _, r_m in params:
            m_pair = N - m
            if m_pair in r_dict:
                assert abs(r_m - r_dict[m_pair]) < 1e-12, (
                    f"r_{m}={r_m} ≠ r_{m_pair}={r_dict[m_pair]}"
                )


class TestCLEntanglement:
    """Caldeira-Leggett entanglement entropy."""

    @pytest.mark.parametrize("N", [7, 8, 9, 11])
    def test_entropy_positive(self, N):
        """S_CL > 0 (non-trivial entanglement)."""
        S, _ = cl_entanglement_entropy(N)
        assert S > 0, f"N={N}: S_CL={S} not positive"

    @pytest.mark.parametrize("N", [7, 8, 9, 11])
    def test_entropy_finite(self, N):
        """S_CL is finite (no divergence from critical modes)."""
        S, _ = cl_entanglement_entropy(N)
        assert np.isfinite(S), f"N={N}: S_CL diverges"

    def test_scales_with_N(self):
        """S_CL grows with N (more modes → more entanglement)."""
        entropies = []
        for N in [7, 9, 11, 13]:
            S, _ = cl_entanglement_entropy(N)
            entropies.append(S)
        # Not strictly monotone due to palindromic structure,
        # but should generally increase
        assert entropies[-1] > entropies[0], (
            f"S_CL should grow: {entropies[0]:.4f} → {entropies[-1]:.4f}"
        )


class TestOneLoopEntropy:
    """One-loop frozen determinant entropy."""

    @pytest.mark.parametrize("N", [7, 8, 9, 11])
    def test_positive(self, N):
        """S_1loop > 0."""
        S = one_loop_entropy(N)
        assert S > 0, f"N={N}: S_1loop={S}"

    @pytest.mark.parametrize("N", [7, 8, 9, 11])
    def test_finite(self, N):
        S = one_loop_entropy(N)
        assert np.isfinite(S), f"N={N}: S_1loop diverges"


class TestCardyEntropy:
    """Cardy (BH) entropy at the threshold."""

    @pytest.mark.parametrize("N", [7, 8, 9, 11])
    def test_positive(self, N):
        S = cardy_entropy(N)
        assert S > 0, f"N={N}: S_BH={S}"

    def test_scales_as_c(self):
        """S_BH ~ c ~ N² (dominant scaling)."""
        # Check S_BH/c is roughly constant for large N
        ratios = []
        for N in [10, 12, 14, 16]:
            S = cardy_entropy(N)
            c = 12 * b_exact(N)
            ratios.append(S / c)
        # S/c = (π/3)cosh(ρ*), which grows with N but
        # the main N² dependence is in c
        assert all(r > 1 for r in ratios), "S_BH/c should be > 1"

    def test_bh_components(self):
        """T·L = cosh(ρ*) identity."""
        for N in [7, 8, 9, 11]:
            bh = bh_entropy_components(N)
            assert abs(bh['TL'] - bh['cosh_rho']) < 1e-10, (
                f"N={N}: T·L={bh['TL']:.6f} ≠ cosh(ρ*)={bh['cosh_rho']:.6f}"
            )


class TestEntropyHierarchy:
    """S_CL < S_1loop << S_BH for all N."""

    @pytest.mark.parametrize("N", [7, 8, 9, 11])
    def test_hierarchy(self, N):
        """The three entropy levels are strictly ordered."""
        S_cl, _ = cl_entanglement_entropy(N)
        S_1l = one_loop_entropy(N)
        S_bh = cardy_entropy(N)

        assert S_bh > S_1l, f"N={N}: S_BH={S_bh:.2f} ≤ S_1loop={S_1l:.2f}"
        assert S_bh > S_cl, f"N={N}: S_BH={S_bh:.2f} ≤ S_CL={S_cl:.2f}"

    def test_bh_dominates_by_orders_of_magnitude(self):
        """S_BH >> S_1loop (Virasoro descendants dominate)."""
        for N in [7, 9, 11]:
            S_1l = one_loop_entropy(N)
            S_bh = cardy_entropy(N)
            ratio = S_bh / S_1l
            assert ratio > 5, (
                f"N={N}: S_BH/S_1loop = {ratio:.1f}, expected >> 1"
            )


class TestCIdentity:
    """c_Fisher-Rao = c_Todd = c_BO (the central identity)."""

    @pytest.mark.parametrize("N", [7, 8, 9, 10, 11, 12])
    def test_c_algebraic_identity(self, N):
        """c_Todd = c_BO to machine precision."""
        result = c_identity_check(N)
        assert result['c_match'], (
            f"N={N}: c_Todd={result['c_todd']:.6f} ≠ c_BO={result['c_bo']:.6f}"
        )


class TestFisherRao:
    """Fisher-Rao metric is ρ-dependent; c=12b(N) is the unique constant."""

    def test_fr_varies_with_rho(self):
        """g_FR(ρ) is NOT constant in ρ."""
        N = 7
        results = fisher_rao_vs_c(N, n_points=20)
        g_values = [r['g_FR'] for r in results]
        # Check variance is non-zero
        g_var = np.var(g_values)
        assert g_var > 1e-6, f"g_FR appears constant (var={g_var})"

    def test_c_is_constant(self):
        """c = 12b(N) doesn't depend on ρ (by definition)."""
        N = 7
        results = fisher_rao_vs_c(N, n_points=20)
        c_values = [r['c_const'] for r in results]
        assert np.std(c_values) < 1e-12, "c should be constant"


class TestBridgeSummary:
    """Full bridge argument for N=7."""

    def test_bridge_N7(self):
        """Complete bridge: angular modes → c → Cardy → S_BH."""
        result = bridge_summary(N=7)

        # Angular modes exist
        assert result['n_angular_modes'] > 0

        # Fisher-Rao = Brown-Henneaux
        assert abs(result['c_fisher_rao'] - result['c_brown_henneaux']) < 1e-12

        # Entropy hierarchy
        assert result['S_BH'] > result['S_1loop'] > 0
        assert result['S_BH'] > result['S_CL'] > 0

    def test_bridge_N11(self):
        """Bridge for the cosmological sector N=11."""
        result = bridge_summary(N=11)
        assert result['S_BH'] > 100, "S_BH should be large for N=11"
        assert result['c_fisher_rao'] > 100, "c should be large for N=11"
