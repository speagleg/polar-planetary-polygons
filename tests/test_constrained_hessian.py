"""
Tests for constrained Hessian analysis of the regular N-gon.

Verifies:
1. N-gon is constrained energy minimum for N=3,...,7
2. N=8 is constrained saddle (unstable without central vortex)
3. Lagrange multiplier mu_L = -(N-1)/4 exactly
4. Central vortex restores stability for N=8
5. Spiral direction H'' is negative but Lagrangian curvature is positive
"""

import numpy as np
import pytest
from planetary_polygons.core.hessian import (
    constrained_hessian_analysis,
    constrained_hessian_with_central_vortex,
    instability_directions,
    critical_central_vortex_strength,
    thomson_energy,
    ngon_positions,
)


class TestConstrainedMinimum:
    """N-gon should be a constrained energy minimum for N <= 7."""

    @pytest.mark.parametrize("N", [3, 4, 5, 6, 7])
    def test_stable_for_small_N(self, N):
        result = constrained_hessian_analysis(N)
        assert result.is_stable, (
            f"N={N} should be stable (constrained minimum), "
            f"got {result.n_neg} negative eigenvalues"
        )

    @pytest.mark.parametrize("N", [3, 4, 5, 6, 7])
    def test_no_negative_eigenvalues(self, N):
        result = constrained_hessian_analysis(N)
        assert result.n_neg == 0

    @pytest.mark.parametrize("N", [3, 4, 5, 6, 7])
    def test_has_one_zero_from_rotation(self, N):
        """SO(2) rotation symmetry gives exactly one zero eigenvalue."""
        result = constrained_hessian_analysis(N)
        assert result.n_zero >= 1, "Should have at least one zero eigenvalue (rotation)"


class TestInstabilityBoundary:
    """N=8 should be the first unstable N (without central vortex)."""

    def test_N8_is_unstable(self):
        result = constrained_hessian_analysis(8)
        assert not result.is_stable
        assert result.n_neg >= 1

    def test_N8_has_3_negative(self):
        result = constrained_hessian_analysis(8)
        assert result.n_neg == 3, f"Expected 3 negative evals, got {result.n_neg}"

    def test_N9_is_unstable(self):
        result = constrained_hessian_analysis(9)
        assert not result.is_stable

    def test_N10_is_unstable(self):
        result = constrained_hessian_analysis(10)
        assert not result.is_stable


class TestLagrangeMultiplier:
    """mu_L should equal -(N-1)/4 for unit-circulation vortices on unit circle."""

    @pytest.mark.parametrize("N", [3, 4, 5, 6, 7, 8])
    def test_mu_L_value(self, N):
        result = constrained_hessian_analysis(N)
        expected = -(N - 1) / 4
        assert abs(result.mu_L - expected) < 1e-4, (
            f"N={N}: mu_L={result.mu_L}, expected {expected}"
        )


class TestSpiralDirection:
    """The spiral direction should have negative H'' but positive Lagrangian."""

    @pytest.mark.parametrize("N", [4, 5, 6, 7, 8])
    def test_spiral_H_pp_negative(self, N):
        result = constrained_hessian_analysis(N)
        assert result.spiral_H_pp < 0, (
            f"N={N}: H'' along spiral should be negative, got {result.spiral_H_pp}"
        )

    @pytest.mark.parametrize("N", [3, 4, 5, 6, 7, 8])
    def test_spiral_lagrangian_positive(self, N):
        result = constrained_hessian_analysis(N)
        assert result.spiral_lagr > -1e-4, (
            f"N={N}: Lagrangian along spiral tangent should be non-negative, "
            f"got {result.spiral_lagr}"
        )


class TestCriticalPoint:
    """N-gon should be a critical point of H on the constraint surface."""

    @pytest.mark.parametrize("N", [3, 4, 5, 6, 7, 8])
    def test_lagrange_residual_small(self, N):
        result = constrained_hessian_analysis(N)
        assert result.lagrange_residual < 1e-6, (
            f"N={N}: grad H not in span of constraint gradients, "
            f"residual={result.lagrange_residual}"
        )


class TestCentralVortex:
    """Central vortex should restore stability for large N."""

    def test_N8_stabilised_by_central_vortex(self):
        """N=8 with sufficiently strong central vortex should be stable."""
        # Try kappa_ratio = 5 (should be more than enough)
        result = constrained_hessian_with_central_vortex(8, kappa_ratio=5.0)
        assert result.is_stable, (
            f"N=8 with kappa_ratio=5 should be stable, "
            f"got {result.n_neg} negative eigenvalues"
        )

    def test_N8_critical_strength_exists(self):
        """There should be a finite critical central vortex strength for N=8."""
        kappa_crit = critical_central_vortex_strength(8)
        assert 0 < kappa_crit < 50, f"Critical strength={kappa_crit}, expected finite"


class TestInstabilityDirections:
    """For N=8, identify what deformations are unstable."""

    def test_N8_unstable_modes_exist(self):
        result = instability_directions(8)
        assert result['n_unstable'] > 0

    def test_N8_fourier_content(self):
        """Unstable modes should have identifiable Fourier structure."""
        result = instability_directions(8)
        for modes in result['fourier_decomposition']:
            assert np.max(modes) > 0.01, "Fourier mode should have nonzero content"


class TestEnergyMinimumProperty:
    """Verify the N-gon minimises H on the constraint surface.

    NOTE: A tangent-plane projection (first-order) goes OFF the constraint
    surface at O(eps^2). The change in H on the actual constraint surface
    is governed by the LAGRANGIAN Hessian, not the plain Hessian. We test
    this by iteratively projecting onto the constraint surface via Newton.
    """

    @staticmethod
    def _project_to_constraint_surface(pos, N, R=1.0, max_iter=20):
        """Iteratively project pos onto {L=NR^2, Px=0, Py=0}."""
        for _ in range(max_iter):
            x, y = pos[:N], pos[N:]
            L_val = np.sum(x**2 + y**2) - N * R**2
            Px_val = np.sum(x)
            Py_val = np.sum(y)
            residual = np.array([L_val, Px_val, Py_val])
            if np.linalg.norm(residual) < 1e-14:
                break
            grad_L = 2 * pos
            grad_Px = np.concatenate([np.ones(N), np.zeros(N)])
            grad_Py = np.concatenate([np.zeros(N), np.ones(N)])
            G = np.column_stack([grad_L, grad_Px, grad_Py])
            correction = G @ np.linalg.solve(G.T @ G, residual)
            pos = pos - correction
        return pos

    @pytest.mark.parametrize("N", [3, 4, 5, 6])
    def test_perturbations_increase_energy_on_surface(self, N):
        """Perturbations projected onto the constraint SURFACE increase H."""
        pos0 = ngon_positions(N)
        H0 = thomson_energy(pos0)

        rng = np.random.default_rng(42)
        for _ in range(20):
            dpos = rng.normal(0, 0.02, 2 * N)

            # First-order tangent projection
            grad_L = 2 * pos0
            grad_Px = np.concatenate([np.ones(N), np.zeros(N)])
            grad_Py = np.concatenate([np.zeros(N), np.ones(N)])
            G = np.column_stack([grad_L, grad_Px, grad_Py])
            GtG_inv = np.linalg.inv(G.T @ G)
            dpos_proj = dpos - G @ GtG_inv @ G.T @ dpos

            # Then iteratively project onto the actual surface
            pos_new = self._project_to_constraint_surface(pos0 + dpos_proj, N)
            H_new = thomson_energy(pos_new)

            assert H_new >= H0 - 1e-8, (
                f"N={N}: Found surface perturbation that decreases H "
                f"by {H0 - H_new:.6e}"
            )
