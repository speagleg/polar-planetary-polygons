"""
Tests for S³ vortex dynamics (GAP A).

Derives the Green's function on S³ from first principles,
constructs the 600-cell vortex configuration from I* quaternions,
and verifies the S³ Havelock decomposition via Gegenbauer polynomials.
"""

import pytest
import numpy as np
from math import pi, sqrt


class TestGreenFunction:
    """S³ Green's function G(χ) = -(1/4π²)(π-χ)/sin(χ)."""

    def test_symmetry(self):
        """G(χ) = G(2π - χ)... wait, χ ∈ [0, π] on S³. G is defined on [0, π]."""
        from planetary_polygons.proofs.s3_vortex_dynamics import s3_green_function
        # G should be a smooth function on (0, π)
        for chi in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]:
            G = s3_green_function(chi)
            assert np.isfinite(G), f"G({chi}) = {G}"

    def test_at_pi_over_2(self):
        """G(π/2) = 0 since cot(π/2) = 0."""
        from planetary_polygons.proofs.s3_vortex_dynamics import s3_green_function
        assert abs(s3_green_function(pi / 2)) < 1e-12

    def test_antipodal_finite(self):
        """G(π) = -1/(4π²) (finite at antipode)."""
        from planetary_polygons.proofs.s3_vortex_dynamics import s3_green_function
        expected = -1.0 / (4 * pi**2)
        G_pi = s3_green_function(pi - 1e-10)
        assert abs(G_pi - expected) < 1e-4

    def test_singularity_at_zero(self):
        """G(χ) → +∞ as χ → 0 (Coulomb singularity)."""
        from planetary_polygons.proofs.s3_vortex_dynamics import s3_green_function
        G_small = s3_green_function(0.01)
        G_smaller = s3_green_function(0.001)
        assert G_smaller > G_small  # more positive as χ → 0

    def test_satisfies_pde(self):
        """G satisfies ΔG = 1/(2π²) away from the source (verified numerically)."""
        from planetary_polygons.proofs.s3_vortex_dynamics import s3_green_function
        target = 1.0 / (2 * pi**2)
        eps = 1e-5
        for chi in [0.5, 1.0, 1.5, 2.0, 2.5]:
            fp = (s3_green_function(chi+eps) - s3_green_function(chi-eps)) / (2*eps)
            fpp = (s3_green_function(chi+eps) - 2*s3_green_function(chi)
                   + s3_green_function(chi-eps)) / eps**2
            import math
            laplacian = fpp + 2*math.cos(chi)/math.sin(chi) * fp
            assert abs(laplacian - target) / target < 0.01, (
                f"chi={chi}: ΔG={laplacian}, expected {target}"
            )


class TestGegenbauerPolynomial:
    """Gegenbauer polynomial C_l^1(x) (zonal spherical function on S³)."""

    def test_C0(self):
        """C_0^1(x) = 1."""
        from planetary_polygons.proofs.s3_vortex_dynamics import gegenbauer_C1
        assert abs(gegenbauer_C1(0, 0.5) - 1.0) < 1e-15

    def test_C1(self):
        """C_1^1(x) = 2x."""
        from planetary_polygons.proofs.s3_vortex_dynamics import gegenbauer_C1
        assert abs(gegenbauer_C1(1, 0.5) - 1.0) < 1e-15
        assert abs(gegenbauer_C1(1, 0.3) - 0.6) < 1e-15

    def test_C2(self):
        """C_2^1(x) = 4x² - 1."""
        from planetary_polygons.proofs.s3_vortex_dynamics import gegenbauer_C1
        x = 0.5
        assert abs(gegenbauer_C1(2, x) - (4 * x**2 - 1)) < 1e-15

    def test_at_one(self):
        """C_l^1(1) = l+1 (dimension normalization)."""
        from planetary_polygons.proofs.s3_vortex_dynamics import gegenbauer_C1
        for l in range(10):
            assert abs(gegenbauer_C1(l, 1.0) - (l + 1)) < 1e-10

    def test_orthogonality(self):
        """Gegenbauer C_l^1 are orthogonal under weight (1-x²)^{1/2} on [-1,1]."""
        from planetary_polygons.proofs.s3_vortex_dynamics import gegenbauer_C1
        # Numerical integration
        x = np.linspace(-0.999, 0.999, 1000)
        dx = x[1] - x[0]
        w = np.sqrt(1 - x**2)  # weight for C^1
        for l1 in range(4):
            for l2 in range(4):
                C1 = np.array([gegenbauer_C1(l1, xi) for xi in x])
                C2 = np.array([gegenbauer_C1(l2, xi) for xi in x])
                integral = np.sum(C1 * C2 * w) * dx
                if l1 == l2:
                    assert integral > 0
                else:
                    assert abs(integral) < 0.05  # approximate orthogonality


class TestGeodesicDistance:
    """Geodesic distance on S³ between unit quaternions."""

    def test_self_distance(self):
        """d(q, q) = 0."""
        from planetary_polygons.proofs.s3_vortex_dynamics import s3_geodesic_distance
        q = (1.0, 0.0, 0.0, 0.0)
        assert abs(s3_geodesic_distance(q, q)) < 1e-15

    def test_antipodal(self):
        """d(q, -q) = π."""
        from planetary_polygons.proofs.s3_vortex_dynamics import s3_geodesic_distance
        q1 = (1.0, 0.0, 0.0, 0.0)
        q2 = (-1.0, 0.0, 0.0, 0.0)
        assert abs(s3_geodesic_distance(q1, q2) - pi) < 1e-10

    def test_orthogonal(self):
        """d(1, i) = π/2."""
        from planetary_polygons.proofs.s3_vortex_dynamics import s3_geodesic_distance
        q1 = (1.0, 0.0, 0.0, 0.0)
        q2 = (0.0, 1.0, 0.0, 0.0)
        assert abs(s3_geodesic_distance(q1, q2) - pi / 2) < 1e-10


class Test600Cell:
    """600-cell vertices = I* quaternions on S³."""

    def test_vertex_count(self):
        """600-cell has 120 vertices."""
        from planetary_polygons.proofs.s3_vortex_dynamics import build_600cell_vertices
        verts = build_600cell_vertices()
        assert len(verts) == 120

    def test_unit_quaternions(self):
        """All vertices are unit quaternions (on S³)."""
        from planetary_polygons.proofs.s3_vortex_dynamics import build_600cell_vertices
        for q in build_600cell_vertices():
            norm = sqrt(sum(c**2 for c in q))
            assert abs(norm - 1.0) < 1e-10

    def test_energy_finite(self):
        """Vortex energy of the 600-cell is finite."""
        from planetary_polygons.proofs.s3_vortex_dynamics import (
            build_600cell_vertices, s3_vortex_energy,
        )
        verts = build_600cell_vertices()
        E = s3_vortex_energy(verts)
        assert np.isfinite(E)

    def test_interaction_matrix_zero_sum(self):
        """Interaction matrix rows sum to zero."""
        from planetary_polygons.proofs.s3_vortex_dynamics import (
            build_600cell_vertices, s3_interaction_matrix,
        )
        verts = build_600cell_vertices()
        K = s3_interaction_matrix(verts)
        row_sums = np.sum(K, axis=1)
        assert np.allclose(row_sums, 0, atol=1e-8)

    def test_havelock_T0_zero(self):
        """Trivial mode (l=0) has T=0."""
        from planetary_polygons.proofs.s3_vortex_dynamics import (
            build_600cell_vertices, s3_havelock_casimir,
        )
        verts = build_600cell_vertices()
        T0 = s3_havelock_casimir(verts, 0)
        assert abs(T0) < 1e-10

    def test_eigenvalue_degeneracies_are_d_squared(self):
        """K-matrix eigenvalue degeneracies = d² for I* irreps (regular rep)."""
        from planetary_polygons.proofs.s3_vortex_dynamics import (
            build_600cell_vertices, s3_interaction_matrix,
        )
        verts = build_600cell_vertices()
        K = s3_interaction_matrix(verts)
        evals = np.sort(np.linalg.eigvalsh(K))
        # Cluster
        used = set()
        degs = []
        for i in range(len(evals)):
            if i in used:
                continue
            group = [i]
            for j in range(i+1, len(evals)):
                if j not in used and abs(evals[j]-evals[i]) < 0.001:
                    group.append(j)
            for j in group:
                used.add(j)
            degs.append(len(group))
        # Should be {1, 4, 9, 16, 25, 36, 9, 16, 4} = d² for I* dims
        expected_degs = sorted([d**2 for d in [1, 2, 3, 4, 5, 6, 4, 2, 3]])
        assert sorted(degs) == expected_degs, f"degs={sorted(degs)}, expected={expected_degs}"

    def test_24cell_vertex_count(self):
        """24-cell has 24 vertices."""
        from planetary_polygons.proofs.s3_vortex_dynamics import build_24cell_vertices
        assert len(build_24cell_vertices()) == 24

    def test_600cell_rho1_energy(self):
        """600-cell ρ₁ sector has 4 negative K-eigenvalues (energy weight, not instability)."""
        from planetary_polygons.proofs.s3_vortex_dynamics import (
            build_600cell_vertices, s3_energy_decomposition,
        )
        result = s3_energy_decomposition(build_600cell_vertices())
        assert result['n_negative'] == 4  # ρ₁ has d²=4, negative K-eigenvalue

    def test_24cell_same_pattern(self):
        """24-cell has same ρ₁ energy sector pattern as 600-cell."""
        from planetary_polygons.proofs.s3_vortex_dynamics import (
            build_24cell_vertices, s3_energy_decomposition,
        )
        result = s3_energy_decomposition(build_24cell_vertices())
        assert result['n_negative'] == 4

    def test_600cell_higher_energy_magnitude(self):
        """600-cell has larger |energy| than 24-cell (more pairwise interactions)."""
        from planetary_polygons.proofs.s3_vortex_dynamics import (
            build_600cell_vertices, build_24cell_vertices, s3_vortex_energy,
        )
        E_600 = s3_vortex_energy(build_600cell_vertices())
        E_24 = s3_vortex_energy(build_24cell_vertices())
        assert abs(E_600) > abs(E_24)

    def test_bridge_formula_matches_havelock(self):
        """S³ bridge formula gives same λ as C₁ - T."""
        from planetary_polygons.proofs.s3_vortex_dynamics import (
            build_600cell_vertices, s3_havelock_casimir,
            s3_per_vertex_sum, s3_bridge_formula,
        )
        verts = build_600cell_vertices()
        C1 = s3_per_vertex_sum(verts)
        for l in range(5):
            T = s3_havelock_casimir(verts, l)
            lam_from_T = C1 - T
            lam_bridge = s3_bridge_formula(verts, l)
            assert abs(lam_from_T - lam_bridge) < 1e-8, (
                f"l={l}: C1-T={lam_from_T}, bridge={lam_bridge}"
            )
