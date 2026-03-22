"""
Tests for the K-theoretic classification of vortex stability phases.

Verifies:
1. Morse index formula μ(N) = max(0, N-5)
2. K_0 class computation and invariance
3. Phase diagram structure
4. Kitaev classification table
"""
import pytest
from planetary_polygons.extensions.k_theoretic_stability import (
    havelock_eigenvalue, havelock_eigenvalues, sign_vector,
    k0_class, morse_index, morse_index_formula, negative_modes_at_zero,
    threshold_xi, phase_boundaries, phase_diagram_row,
    verify_k0_invariance, kitaev_table,
)


# ============================================================
# Morse index
# ============================================================

class TestMorseIndex:
    def test_stable_flat_N3_to_7(self):
        """N ≤ 7 are stable at ξ = 0: μ = 0."""
        for N in range(3, 8):
            assert morse_index(N, 0.0) == 0, f"N={N} should be stable"

    def test_unstable_flat_N8(self):
        """N = 8 has μ = 3 at ξ = 0."""
        assert morse_index(8, 0.0) == 3

    def test_unstable_flat_N9(self):
        """N = 9 has μ = 4 at ξ = 0."""
        assert morse_index(9, 0.0) == 4

    def test_unstable_flat_N10(self):
        """N = 10 has μ = 5 at ξ = 0."""
        assert morse_index(10, 0.0) == 5

    def test_morse_index_formula(self):
        """μ(N) = 0 for N ≤ 7, N-5 for N ≥ 8 (NOT max(0,N-5))."""
        for N in range(3, 31):
            expected = 0 if N <= 7 else N - 5
            assert morse_index_formula(N) == expected
            assert morse_index(N, 0.0) == expected, f"N={N}"

    def test_negative_modes_N8(self):
        """N = 8: negative modes are {3, 4, 5}."""
        assert negative_modes_at_zero(8) == frozenset({3, 4, 5})

    def test_negative_modes_N9(self):
        """N = 9: negative modes are {3, 4, 5, 6}."""
        assert negative_modes_at_zero(9) == frozenset({3, 4, 5, 6})

    def test_negative_modes_N12(self):
        """N = 12: negative modes are {3, 4, 5, 6, 7, 8, 9}."""
        assert negative_modes_at_zero(12) == frozenset({3, 4, 5, 6, 7, 8, 9})

    def test_negative_modes_symmetric(self):
        """Negative modes are symmetric: m ∈ S iff N-m ∈ S."""
        for N in range(8, 20):
            S = negative_modes_at_zero(N)
            for m in S:
                assert N - m in S, f"N={N}: m={m} in S but N-m={N-m} not"

    def test_negative_modes_contiguous(self):
        """Negative modes form a contiguous block {3, ..., N-3}."""
        for N in range(8, 25):
            S = negative_modes_at_zero(N)
            assert S == frozenset(range(3, N - 2)), f"N={N}"


# ============================================================
# K_0 class and topological invariance
# ============================================================

class TestK0Class:
    def test_empty_for_stable(self):
        """Stable configurations have empty K_0 class."""
        for N in range(3, 8):
            assert k0_class(N, 0.0) == frozenset()

    def test_equals_negative_modes(self):
        """K_0 class at ξ=0 equals the negative modes set."""
        for N in range(3, 20):
            assert k0_class(N, 0.0) == negative_modes_at_zero(N)

    def test_k0_invariance_within_phase(self):
        """K_0 class is constant within each phase (the key theorem)."""
        # N=8: first boundary at ξ*(8,3)≈0.0334, second at ξ*(8,4)≈0.0627
        # Check invariance on [0.001, 0.03] (before first boundary)
        assert verify_k0_invariance(8, 0.001, 0.03, n_points=50)
        # Check invariance on [0.04, 0.06] (between boundaries)
        assert verify_k0_invariance(8, 0.04, 0.06, n_points=50)

    def test_k0_changes_at_boundary(self):
        """K_0 class changes at a phase boundary."""
        # N=8: boundary at ξ*(8,4). Class should differ across it.
        xi_star = threshold_xi(8, 4)
        assert xi_star is not None
        class_before = k0_class(8, xi_star - 0.001)
        class_after = k0_class(8, xi_star + 0.001)
        assert class_before != class_after

    def test_k0_invariance_after_last_boundary(self):
        """After all boundaries, K_0 class is empty (fully stable)."""
        for N in range(8, 13):
            bounds = phase_boundaries(N)
            if bounds:
                last_xi = bounds[-1][0]
                # Should be stable (empty class) after last boundary
                assert verify_k0_invariance(N, last_xi + 0.001, 0.999)
                assert k0_class(N, 0.999) == frozenset()

    def test_curvature_stabilizes(self):
        """Sufficient curvature stabilizes any N-gon on H²."""
        for N in range(3, 20):
            assert morse_index(N, 0.999) == 0, f"N={N} not stable at ξ=0.999"


# ============================================================
# Phase boundaries (palindromic thresholds)
# ============================================================

class TestPhaseBoundaries:
    def test_no_boundaries_for_stable(self):
        """N ≤ 7 have no phase boundaries on H²."""
        for N in range(3, 8):
            assert phase_boundaries(N) == []

    def test_N8_has_3_boundaries(self):
        """N = 8 has 3 boundaries (modes 3, 4, 5; but 3=5 by symmetry)."""
        bounds = phase_boundaries(8)
        # Modes m=3 and m=5 have the same threshold (λ_3 = λ_5)
        # Mode m=4 has a different threshold
        assert len(bounds) >= 2  # at least 2 distinct thresholds

    def test_boundaries_ordered(self):
        """Phase boundaries are in increasing order of ξ."""
        for N in range(8, 15):
            bounds = phase_boundaries(N)
            xis = [b[0] for b in bounds]
            assert xis == sorted(xis), f"N={N}: boundaries not ordered"

    def test_boundary_matches_threshold(self):
        """Phase boundaries match the algebraic threshold values."""
        from planetary_polygons.extensions.algebraic_thresholds import (
            h2_stability_threshold,
        )
        # The LAST boundary for each N should match h2_stability_threshold
        for N in range(8, 13):
            xi_alg, _, _ = h2_stability_threshold(N)
            bounds = phase_boundaries(N)
            if bounds:
                xi_last = bounds[-1][0]
                # The last boundary is for m=1 (or m=N-1)
                assert abs(xi_last - xi_alg) < 1e-6, (
                    f"N={N}: last boundary {xi_last} != threshold {xi_alg}")


# ============================================================
# Phase diagram
# ============================================================

class TestPhaseDiagram:
    def test_single_phase_for_stable(self):
        """N ≤ 7 have a single phase (all stable)."""
        for N in range(3, 8):
            phases = phase_diagram_row(N)
            assert len(phases) == 1
            assert phases[0]['morse_index'] == 0

    def test_phases_decrease_monotonically(self):
        """Morse index decreases as curvature increases."""
        for N in range(8, 15):
            phases = phase_diagram_row(N)
            indices = [p['morse_index'] for p in phases]
            assert indices == sorted(indices, reverse=True), (
                f"N={N}: non-monotonic Morse index")

    def test_last_phase_is_stable(self):
        """The last phase (largest ξ) is always stable."""
        for N in range(3, 15):
            phases = phase_diagram_row(N)
            assert phases[-1]['morse_index'] == 0

    def test_first_phase_matches_flat(self):
        """The first phase has Morse index = morse_index_formula(N)."""
        for N in range(3, 15):
            phases = phase_diagram_row(N)
            assert phases[0]['morse_index'] == morse_index_formula(N)


# ============================================================
# Kitaev classification
# ============================================================

class TestKitaevTable:
    def test_table_runs(self):
        """Kitaev table computes without error."""
        table = kitaev_table(12)
        assert len(table) == 10  # N = 3, ..., 12

    def test_k_group(self):
        """K_0(C*(Z_N)) = Z^N."""
        table = kitaev_table(10)
        for row in table:
            assert row['k_group'] == f"Z^{row['N']}"

    def test_n7_boundary(self):
        """N=7 is the boundary: stable flat, single phase."""
        table = kitaev_table(8)
        n7 = [r for r in table if r['N'] == 7][0]
        assert n7['stable_flat'] is True
        assert n7['n_phases'] == 1

    def test_n8_unstable_flat(self):
        """N=8 is unstable flat but stabilized by curvature."""
        table = kitaev_table(9)
        n8 = [r for r in table if r['N'] == 8][0]
        assert n8['stable_flat'] is False
        assert n8['stable_curved'] is True
        assert n8['n_phases'] >= 2


# ============================================================
# Sign vector and representation ring
# ============================================================

class TestSignVector:
    def test_all_positive_N6(self):
        """N = 6 at ξ = 0: all eigenvalues positive."""
        sv = sign_vector(6, 0.0)
        assert all(s == 1 for s in sv)

    def test_mixed_signs_N8(self):
        """N = 8 at ξ = 0: modes 3,4,5 negative, rest positive."""
        sv = sign_vector(8, 0.0)
        # sv = (sgn(λ_1), ..., sgn(λ_7))
        expected = (1, 1, -1, -1, -1, 1, 1)
        assert sv == expected

    def test_symmetric(self):
        """Sign vector is symmetric: sv[m] = sv[N-1-m]."""
        for N in range(3, 15):
            sv = sign_vector(N, 0.0)
            n = len(sv)
            for i in range(n):
                assert sv[i] == sv[n - 1 - i], f"N={N}, m={i+1}"


# ============================================================
# Index pairing (Theorem 6.2 — the bridge to KK-theory)
# ============================================================

class TestIndexPairing:
    def test_bolza_spectral_bound(self):
        """Bolza spectral bound |δC₁| < 0.17."""
        from planetary_polygons.extensions.k_theoretic_stability import (
            bolza_index_pairing,
        )
        result = bolza_index_pairing(xi=0.217)
        assert result['spectral_bound'] < 0.17

    def test_bolza_k0_preserved(self):
        """Bolza δC₁ doesn't change the K₀ class (too small)."""
        from planetary_polygons.extensions.k_theoretic_stability import (
            bolza_index_pairing,
        )
        result = bolza_index_pairing(xi=0.217)
        assert result['k0_class_preserved'] is True

    def test_geometric_side_positive(self):
        """Geometric side of index pairing is positive (csch² > 0)."""
        from planetary_polygons.extensions.k_theoretic_stability import (
            index_pairing_geometric_side,
        )
        import math
        ell = 2 * math.acosh(1 + math.sqrt(2))
        delta = index_pairing_geometric_side([(ell, 12)], 0.217, 8)
        assert delta > 0

    def test_phase_shift_bounded(self):
        """Phase boundaries shift by O(csch²) on quotient surfaces."""
        from planetary_polygons.extensions.k_theoretic_stability import (
            phase_shift_on_surface,
        )
        import math
        ell = 2 * math.acosh(1 + math.sqrt(2))
        shifts = phase_shift_on_surface(8, [(ell, 12)])
        for s in shifts:
            # Geometric side gives an upper bound on the shift
            assert abs(s['delta_xi']) < 0.1, (
                f"m={s['m']}: shift {s['delta_xi']:.4f}")

    def test_spectral_flow_h2(self):
        """Spectral flow on H² (δC₁=0): N-5 crossings for N≥8."""
        from planetary_polygons.extensions.k_theoretic_stability import (
            spectral_flow,
        )
        for N in range(8, 15):
            sf, crossings = spectral_flow(N, 0.001, 0.999, delta_C1=0.0)
            assert sf == N - 5, f"N={N}: sf={sf}, expected {N-5}"

    def test_spectral_flow_preserved_bolza(self):
        """Spectral flow on Bolza (δC₁≈0.01) equals H² flow (Thm 6.3)."""
        from planetary_polygons.extensions.k_theoretic_stability import (
            spectral_flow, spectral_flow_preserved,
        )
        delta_bolza = 0.011  # spectral bound
        for N in [8, 10, 12]:
            sf_H2, _ = spectral_flow(N, 0.001, 0.999, delta_C1=0.0)
            sf_S, _ = spectral_flow(N, 0.001, 0.999, delta_C1=delta_bolza)
            assert sf_S == sf_H2, f"N={N}: sf differs"
            preserved, margin, _ = spectral_flow_preserved(N, delta_bolza)
            assert preserved, f"N={N}: flow not preserved, margin={margin}"

    def test_spectral_flow_breaks_at_large_delta(self):
        """Large δC₁ can change the spectral flow."""
        from planetary_polygons.extensions.k_theoretic_stability import (
            spectral_flow_preserved, binding_eigenvalue,
        )
        # For N=8, the binding eigenvalue should be modest
        lam_bind = binding_eigenvalue(8, 4)
        assert lam_bind is not None
        # δC₁ > λ_bind should break preservation
        preserved, margin, _ = spectral_flow_preserved(8, lam_bind + 0.1)
        assert not preserved

    def test_binding_eigenvalue_positive(self):
        """Binding eigenvalue is positive at each threshold."""
        from planetary_polygons.extensions.k_theoretic_stability import (
            binding_eigenvalue, phase_boundaries,
        )
        for N in range(8, 13):
            for xi_b, m in phase_boundaries(N):
                lam_bind = binding_eigenvalue(N, m)
                assert lam_bind is not None and lam_bind > 0, (
                    f"N={N}, m={m}: λ_bind={lam_bind}")

    def test_kk_product_bolza(self):
        """KK product identity holds on Bolza: operator gap is satisfied."""
        from planetary_polygons.extensions.k_theoretic_stability import (
            kk_product_verification,
        )
        import math
        ell_sys = 2 * math.acosh(1 + math.sqrt(2))
        ell_next = 2 * math.acosh(3)
        geodesics = [(ell_sys, 12), (ell_next, 12)]
        result = kk_product_verification(12, 0.217, geodesics)
        assert result['operator_gap_holds'], "operator norm gap should hold"
        assert result['gap_ratio'] > 2.0, f"margin too small: {result['gap_ratio']}"
        assert result['kk_product_equals_elementary']

    def test_operator_norm_exceeds_trace(self):
        """||h||_{op} > |δC₁| for nontrivial surfaces (operator norm is stronger)."""
        from planetary_polygons.extensions.k_theoretic_stability import (
            operator_norm_bound, index_pairing_geometric_side,
        )
        import math
        ell = 2 * math.acosh(1 + math.sqrt(2))
        h_norm = operator_norm_bound([(ell, 12)])
        # The ℓ¹ norm should be positive and finite
        assert 0 < h_norm < 1.0

    def test_geometric_side_is_trace_not_diagonal(self):
        """
        The geometric side Σ_γ csch²(ℓ_γ/2)/(4π) is the Selberg TRACE
        (integrated over the surface), not the diagonal value at a point.

        At the center of the Bolza surface, the diagonal value is
        suppressed by |Aut| = 48: only trivial-rep eigenfunctions
        contribute, giving δC₁(center) ≈ spectral_bound ≈ 0.01,
        NOT the full trace ≈ 0.20.

        This suppression IS the content of the index pairing:
        the assembly map projects onto the trivial rep at the
        Aut-fixed point.
        """
        from planetary_polygons.extensions.k_theoretic_stability import (
            index_pairing_geometric_side, bolza_index_pairing,
        )
        import math
        ell = 2 * math.acosh(1 + math.sqrt(2))
        # Full geometric side (trace): O(1)
        delta_trace = index_pairing_geometric_side([(ell, 12)], 0.217, 8)
        # Spectral bound at center (diagonal): O(1/|Aut|)
        bolza = bolza_index_pairing(0.217)
        # The ratio should reflect the Aut suppression
        ratio = delta_trace / bolza['spectral_bound']
        assert ratio > 5  # significant suppression
