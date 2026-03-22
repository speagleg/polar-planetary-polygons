"""Tests for tessellation stability computation."""
import math
import pytest
import sys
import numpy as np
sys.path.insert(0, 'src')

from planetary_polygons.extensions.tessellation_stability import (
    pairwise_hessian_block, build_hessian,
    hexagon_tessellation, square_tessellation, triangle_tessellation,
    tessellation_stability_margin,
)


class TestAnalyticalHessian:
    """Test the analytical Hessian against finite differences."""

    def _numerical_hessian(self, verts, Delta, eps=1e-5):
        M = len(verts)
        pos = np.concatenate([verts[:, 0], verts[:, 1]])

        def energy(p):
            x, y = p[:M], p[M:]
            E = 0.0
            for i in range(M):
                for j in range(i + 1, M):
                    r2 = (x[i]-x[j])**2 + (y[i]-y[j])**2
                    if r2 < 1e-30: continue
                    if abs(Delta) < 1e-10: E -= 0.5 * np.log(r2)
                    else: E += r2 ** (-Delta)
            return E

        H = np.zeros((2*M, 2*M))
        for i in range(2*M):
            for j in range(i, 2*M):
                pp = pos.copy(); pp[i] += eps; pp[j] += eps
                pm = pos.copy(); pm[i] += eps; pm[j] -= eps
                mp = pos.copy(); mp[i] -= eps; mp[j] += eps
                mm = pos.copy(); mm[i] -= eps; mm[j] -= eps
                H[i, j] = (energy(pp)-energy(pm)-energy(mp)+energy(mm))/(4*eps**2)
                H[j, i] = H[i, j]
        return H

    def test_log_case(self):
        verts = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, 0.866]])
        H_a = build_hessian(verts, 0.0)
        H_n = self._numerical_hessian(verts, 0.0)
        assert np.max(np.abs(H_a - H_n)) < 1e-4

    def test_power_law(self):
        verts = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, 0.866]])
        for Delta in [0.5, 1.0, 2.0]:
            H_a = build_hessian(verts, Delta)
            H_n = self._numerical_hessian(verts, Delta)
            assert np.max(np.abs(H_a - H_n)) < 1e-3, \
                f"Δ={Delta}: max diff = {np.max(np.abs(H_a - H_n))}"

    def test_symmetry(self):
        verts = np.array([[0.0, 0.0], [1.0, 0.3], [0.2, 0.9]])
        H = build_hessian(verts, 1.0)
        assert np.max(np.abs(H - H.T)) < 1e-12


class TestGeometry:
    """Test tessellation geometry builders."""

    def test_hexagon_counts(self):
        v, f, m = hexagon_tessellation(n_rings=1)
        assert len(f) == 7, f"Expected 7 hexagonal faces, got {len(f)}"
        assert np.sum(m) == 6, f"Expected 6 interior vertices, got {np.sum(m)}"
        assert len(v) == 24, f"Expected 24 vertices, got {len(v)}"

    def test_square_counts(self):
        v, f, m = square_tessellation(n_side=3)
        assert len(f) == 9
        assert len(v) == 16
        assert np.sum(m) == 4

    def test_triangle_interior_exists(self):
        v, f, m = triangle_tessellation(n_rings=2)
        assert np.sum(m) > 0, "No interior vertices found"

    def test_edge_lengths(self):
        """All edges within a face have the correct length."""
        edge = 1.0
        for builder in [lambda: hexagon_tessellation(1, edge),
                        lambda: square_tessellation(3, edge)]:
            v, f, _ = builder()
            for face in f:
                for k in range(len(face)):
                    i, j = face[k], face[(k+1) % len(face)]
                    d = np.linalg.norm(v[i] - v[j])
                    assert abs(d - edge) < 0.01, \
                        f"Edge length {d} != {edge}"


class TestMainResult:
    """The core physics tests."""

    def test_triangle_stable_at_delta_2(self):
        """Triangular tessellation is stable at Δ=2."""
        v, f, m = triangle_tessellation(n_rings=2)
        margin = tessellation_stability_margin(v, m, 2.0)
        assert margin > 0, f"Triangle margin {margin} should be > 0 at Δ=2"

    def test_hexagon_unstable_at_delta_2(self):
        """Hexagonal tessellation is unstable at Δ=2."""
        v, f, m = hexagon_tessellation(n_rings=1)
        margin = tessellation_stability_margin(v, m, 2.0)
        assert margin < -0.1, f"Hexagon margin {margin} should be < 0 at Δ=2"

    def test_triangle_stable_at_delta_5(self):
        """Triangular tessellation stable at Δ=5 (short-range)."""
        v, f, m = triangle_tessellation(n_rings=2)
        margin = tessellation_stability_margin(v, m, 5.0)
        assert margin > 0

    def test_hexagon_unstable_at_delta_10(self):
        """Hexagonal tessellation still unstable at Δ=10."""
        v, f, m = hexagon_tessellation(n_rings=1)
        margin = tessellation_stability_margin(v, m, 10.0)
        assert margin < -0.1
