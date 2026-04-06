"""Tests for the Bolza surface tau(P_-) computation.

Tests cover:
- Octagon geometry (circumradius, edge length, apothem)
- Systole length
- Generator consistency (displacement, inverse pairing)
- delta_C1 positivity
- tau(P_-) convergence toward 0.644
- tau in (0, 1) at all truncation levels
- Spectral radius bounded
"""

import math
import pytest
import numpy as np

from planetary_polygons.proofs.bolza_tau import (
    _octagon_geometry,
    _octagon_vertices,
    bolza_generators,
    bolza_systole,
    bolza_geodesic_lengths,
    delta_C1_selberg,
    enumerate_group_bfs,
    build_convolution_matrix,
    tau_P_minus_counting,
    tau_P_minus_weighted,
    compute_tau_bolza,
    disk_distance_complex,
    green_function_h2,
)


# ============================================================
# Octagon geometry
# ============================================================

class TestOctagonGeometry:
    def test_circumradius(self):
        """Circumradius satisfies cosh(R) = cos(pi/8)/sin(pi/8)."""
        R_hyp, R_disk, _, _ = _octagon_geometry()
        expected_cosh = math.cos(math.pi / 8) / math.sin(math.pi / 8)
        assert abs(math.cosh(R_hyp) - expected_cosh) < 1e-10

    def test_disk_radius_in_unit_disk(self):
        _, R_disk, _, _ = _octagon_geometry()
        assert 0 < R_disk < 1

    def test_edge_length_equals_circumradius(self):
        """For the regular octagon with angle pi/4, edge = circumradius."""
        R_hyp, _, a_hyp, _ = _octagon_geometry()
        assert abs(a_hyp - R_hyp) < 1e-10

    def test_eight_vertices(self):
        verts = _octagon_vertices()
        assert len(verts) == 8
        _, R_disk, _, _ = _octagon_geometry()
        for v in verts:
            assert abs(abs(v) - R_disk) < 1e-10


# ============================================================
# Systole
# ============================================================

class TestSystole:
    def test_systole_value(self):
        """Systole = 2*arccosh(1+sqrt(2)) ~ 3.057."""
        sys = bolza_systole()
        assert abs(sys - 3.0571418390) < 1e-6

    def test_systole_from_length_spectrum(self):
        """First entry in length spectrum is the systole."""
        spec = bolza_geodesic_lengths(n_terms=1)
        assert len(spec) == 1
        ell, mult = spec[0]
        assert abs(ell - bolza_systole()) < 1e-10
        assert mult == 12


# ============================================================
# Generators
# ============================================================

class TestGenerators:
    def test_eight_generators(self):
        gens, labels, inv_map = bolza_generators()
        assert len(gens) == 8
        assert len(labels) == 8
        assert len(inv_map) == 8

    def test_generator_displacement(self):
        """All generators displace origin by 2*d_apothem."""
        gens, _, _ = bolza_generators()
        _, _, _, d_apo = _octagon_geometry()
        expected = 2 * d_apo
        for g in gens:
            z = g(0j)
            d = disk_distance_complex(0j, z)
            assert abs(d - expected) < 1e-6, f"d={d}, expected={expected}"

    def test_inverse_pairing(self):
        """Generator i composed with inverse gives identity."""
        gens, _, inv_map = bolza_generators()
        for i in range(8):
            z = gens[i](0j)
            z_back = gens[inv_map[i]](z)
            d = disk_distance_complex(0j, z_back)
            assert d < 0.01, f"gen {i}: d(0, T_inv(T(0))) = {d}"

    def test_vertex_mapping(self):
        """Generator a maps v_2->v_1 and v_3->v_0."""
        gens, _, _ = bolza_generators()
        v = _octagon_vertices()
        gen_a = gens[0]
        err1 = abs(gen_a(v[2]) - v[1])
        err2 = abs(gen_a(v[3]) - v[0])
        assert err1 < 1e-10
        assert err2 < 1e-10


# ============================================================
# Selberg delta_C1
# ============================================================

class TestDeltaC1:
    def test_positive(self):
        """delta_C1 > 0."""
        assert delta_C1_selberg() > 0

    def test_convergence(self):
        """Adding more terms changes delta_C1 by a decreasing amount."""
        d5 = delta_C1_selberg(n_terms=5)
        d10 = delta_C1_selberg(n_terms=10)
        d20 = delta_C1_selberg(n_terms=20)
        # Each doubling of terms adds less
        assert abs(d20 - d10) < abs(d10 - d5)

    def test_value_range(self):
        """delta_C1 ~ 6.75 from 20 geodesic classes."""
        d = delta_C1_selberg()
        assert 6.0 < d < 7.5


# ============================================================
# Group enumeration
# ============================================================

class TestEnumeration:
    def test_level_1_count(self):
        """Word length 1 gives 8 elements."""
        _, _, nbl = enumerate_group_bfs(1)
        assert nbl[0] == 8

    def test_level_2_count(self):
        """Word length 2 gives 56 new elements (8*7 minus group relations)."""
        _, _, nbl = enumerate_group_bfs(2)
        assert 40 <= nbl[1] <= 56

    def test_all_inside_disk(self):
        images, _, _ = enumerate_group_bfs(2)
        for z in images:
            assert abs(z) < 1.0

    def test_distances_positive(self):
        _, dists, _ = enumerate_group_bfs(2)
        assert all(d > 0 for d in dists)

    def test_sorted_by_distance(self):
        _, dists, _ = enumerate_group_bfs(2)
        for i in range(len(dists) - 1):
            assert dists[i] <= dists[i + 1] + 1e-10


# ============================================================
# Green's function
# ============================================================

class TestGreenFunction:
    def test_positive(self):
        """G(d) > 0 for all d > 0."""
        for d in [0.1, 1.0, 3.0, 10.0]:
            assert green_function_h2(d) > 0

    def test_decreasing(self):
        """G(d) is monotonically decreasing."""
        prev = float('inf')
        for d in [0.01, 0.1, 0.5, 1, 2, 5, 10]:
            g = green_function_h2(d)
            assert g < prev
            prev = g


# ============================================================
# Convolution matrix
# ============================================================

class TestConvolutionMatrix:
    def test_symmetric(self):
        images, _, _ = enumerate_group_bfs(1)
        H = build_convolution_matrix(images)
        assert np.allclose(H, H.T, atol=1e-12)

    def test_zero_diagonal(self):
        images, _, _ = enumerate_group_bfs(1)
        H = build_convolution_matrix(images)
        assert np.allclose(np.diag(H), 0.0)

    def test_positive_off_diagonal(self):
        """Off-diagonal entries are positive (G > 0)."""
        images, _, _ = enumerate_group_bfs(1)
        H = build_convolution_matrix(images)
        n = len(images)
        for i in range(n):
            for j in range(n):
                if i != j:
                    assert H[i, j] > 0


# ============================================================
# tau(P_-) computation
# ============================================================

class TestTau:
    def test_tau_L1(self):
        """tau = 5/8 = 0.625 at word length 1."""
        r = compute_tau_bolza(1, verbose=False)
        assert abs(r['tau_counting'] - 0.625) < 1e-10

    def test_tau_L2(self):
        """tau = 0.625 at word length 2 (stable)."""
        r = compute_tau_bolza(2, verbose=False)
        assert abs(r['tau_counting'] - 0.625) < 1e-10

    def test_tau_L3_isotypic(self):
        """tau at L=3 matches the 31/48 Aut-isotypic fraction."""
        r = compute_tau_bolza(3, verbose=False)
        assert abs(r['tau_counting'] - 31 / 48) < 0.01

    def test_tau_in_unit_interval(self):
        """tau in (0, 1) at all levels."""
        for L in [1, 2, 3]:
            r = compute_tau_bolza(L, verbose=False)
            assert 0 < r['tau_counting'] < 1

    def test_tau_near_paper_value(self):
        """tau at L=3..4 is within 0.02 of the paper's 0.644."""
        r3 = compute_tau_bolza(3, verbose=False)
        r4 = compute_tau_bolza(4, verbose=False)
        mean = (r3['tau_counting'] + r4['tau_counting']) / 2
        assert abs(mean - 0.644) < 0.02

    def test_spectral_radius_bounded(self):
        """Spectral radius stays bounded (< 0.5) at all levels."""
        for L in [1, 2, 3]:
            r = compute_tau_bolza(L, verbose=False)
            assert r['spectral_radius'] < 0.5

    def test_weighted_tau_half(self):
        """Weighted tau = 0.5 (eigenvalue distribution is symmetric about 0)."""
        r = compute_tau_bolza(2, verbose=False)
        assert abs(r['tau_weighted'] - 0.5) < 1e-10


# ============================================================
# tau helper functions
# ============================================================

class TestTauHelpers:
    def test_counting_all_negative(self):
        eigs = np.array([-3.0, -2.0, -1.0])
        assert abs(tau_P_minus_counting(eigs) - 1.0) < 1e-10

    def test_counting_all_positive(self):
        eigs = np.array([1.0, 2.0, 3.0])
        assert abs(tau_P_minus_counting(eigs) - 0.0) < 1e-10

    def test_counting_mixed(self):
        eigs = np.array([-2.0, -1.0, 1.0, 2.0, 3.0])
        assert abs(tau_P_minus_counting(eigs) - 0.4) < 1e-10

    def test_weighted_symmetric(self):
        eigs = np.array([-2.0, -1.0, 1.0, 2.0])
        assert abs(tau_P_minus_weighted(eigs) - 0.5) < 1e-10

    def test_counting_with_offset(self):
        eigs = np.array([-1.0, 0.0, 1.0, 2.0])
        tau = tau_P_minus_counting(eigs, c=-1.5)
        # shifted: [-2.5, -1.5, -0.5, 0.5], 3 of 4 negative
        assert abs(tau - 0.75) < 1e-10


# ============================================================
# Length spectrum
# ============================================================

class TestLengthSpectrum:
    def test_sorted(self):
        spec = bolza_geodesic_lengths()
        for i in range(len(spec) - 1):
            assert spec[i][0] <= spec[i + 1][0]

    def test_multiplicities_positive(self):
        spec = bolza_geodesic_lengths()
        for _, mult in spec:
            assert mult > 0
            assert mult % 12 == 0  # Aut symmetry forces mult divisible by 12

    def test_twenty_classes(self):
        spec = bolza_geodesic_lengths()
        assert len(spec) == 20
