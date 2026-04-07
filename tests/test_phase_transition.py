"""Tests for the K=0 phase transition (GAP C)."""

import pytest
from math import log


class TestPolygonStability:
    """Polygon stability on R²: N ≤ 7 stable, N ≥ 8 unstable."""

    def test_hexagon_stable(self):
        from planetary_polygons.proofs.phase_transition import polygon_stability
        assert polygon_stability(6)['stable']

    def test_heptagon_marginal(self):
        from planetary_polygons.proofs.phase_transition import polygon_stability
        result = polygon_stability(7)
        assert result['marginal']
        assert result['morse_index'] == 0

    def test_octagon_unstable(self):
        from planetary_polygons.proofs.phase_transition import polygon_stability
        result = polygon_stability(8)
        assert not result['stable']
        assert result['morse_index'] > 0

    def test_max_stable_is_7(self):
        from planetary_polygons.proofs.phase_transition import polygon_stability
        for N in range(3, 8):
            assert polygon_stability(N)['stable'] or polygon_stability(N)['marginal']
        assert not polygon_stability(8)['stable']


class TestEnergyScaling:
    """Energy on S²(R) scales with R-independent ordering."""

    def test_icosa_always_beats_7gon(self):
        """Icosahedron has higher energy than 7-gon for all R ≥ 1."""
        from planetary_polygons.proofs.phase_transition import transition_energy_gap
        for R in [1.0, 2.0, 10.0, 100.0]:
            assert transition_energy_gap(R) > 0

    def test_gap_grows_with_R(self):
        """Energy gap grows as 45 × ln(R)."""
        from planetary_polygons.proofs.phase_transition import transition_energy_gap
        gap_10 = transition_energy_gap(10.0)
        gap_100 = transition_energy_gap(100.0)
        # Difference should be ≈ 45 × (ln 100 - ln 10) = 45 × ln 10 ≈ 103.6
        expected_diff = 45 * log(10)
        actual_diff = gap_100 - gap_10
        assert abs(actual_diff - expected_diff) / expected_diff < 0.01


class TestFirstOrderTransition:
    """The K=0 transition is first-order (discontinuous)."""

    def test_transition_data(self):
        from planetary_polygons.proofs.phase_transition import verify_first_order_transition
        result = verify_first_order_transition()
        assert result['first_order']
        assert result['s2_stable']
        assert result['broken_generators'] == 236

    def test_symmetry_jump(self):
        """Symmetry group jumps from A₅ (60 elements) to Z₇ (7 elements)."""
        from planetary_polygons.proofs.phase_transition import verify_first_order_transition
        result = verify_first_order_transition()
        assert 'A₅' in result['s2_symmetry']
        assert 'Z_7' in result['r2_symmetry']

    def test_polygon_rings_unstable_on_s2(self):
        """All polygon rings N ≥ 4 are UNSTABLE on S² (proved in ade_partition_function)."""
        from planetary_polygons.proofs.ade_partition_function import (
            polygon_ring, hessian_eigenvalues,
        )
        for N in [4, 5, 6, 7, 8]:
            verts = polygon_ring(N)
            evals = hessian_eigenvalues(verts)
            n_neg = sum(1 for e in evals if e < -0.01)
            assert n_neg > 0, f"N={N} polygon ring should be unstable on S²"
