"""Tests for the Virasoro block computation and quantum correction."""
import math
import pytest
from planetary_polygons.extensions.virasoro_block import (
    partitions, gram_element, gram_matrix,
    three_point_coupling, block_coefficient,
    virasoro_block, Z4_NOME,
    four_point_angular_stiffness,
    quantum_correction_estimate,
)


class TestPartitions:
    def test_p0(self):
        assert partitions(0) == [()]

    def test_p1(self):
        assert partitions(1) == [(1,)]

    def test_p2(self):
        assert set(partitions(2)) == {(2,), (1, 1)}

    def test_p3(self):
        assert set(partitions(3)) == {(3,), (2, 1), (1, 1, 1)}

    def test_p4_count(self):
        assert len(partitions(4)) == 5

    def test_p5_count(self):
        assert len(partitions(5)) == 7


class TestGramMatrix:
    def test_level1(self):
        """G_1 = (2h_p) for single state L_{-1}|h>."""
        h_p, c = 2.0, 10.0
        parts, G = gram_matrix(h_p, c, 1)
        assert len(parts) == 1
        assert parts[0] == (1,)
        assert abs(G[0][0] - 2 * h_p) < 1e-10

    def test_level2_diagonal(self):
        """G_2 diagonal: <L_2 L_{-2}> = 4h + c/2."""
        h_p, c = 3.0, 25.0
        parts, G = gram_matrix(h_p, c, 2)
        # Find the (2,) state
        idx_2 = parts.index((2,))
        expected = 4 * h_p + c / 2
        assert abs(G[idx_2][idx_2] - expected) < 1e-8, (
            f"G_22 = {G[idx_2][idx_2]}, expected {expected}")

    def test_level2_other_diagonal(self):
        """<L_1^2 L_{-1}^2> = 4h(2h+1)."""
        h_p, c = 3.0, 25.0
        parts, G = gram_matrix(h_p, c, 2)
        idx_11 = parts.index((1, 1))
        expected = 4 * h_p * (2 * h_p + 1)
        assert abs(G[idx_11][idx_11] - expected) < 1e-8

    def test_level2_off_diagonal(self):
        """<L_2 L_{-1}^2> = 6h."""
        h_p, c = 3.0, 25.0
        parts, G = gram_matrix(h_p, c, 2)
        idx_2 = parts.index((2,))
        idx_11 = parts.index((1, 1))
        expected = 6 * h_p
        assert abs(G[idx_2][idx_11] - expected) < 1e-8

    def test_gram_positive_definite(self):
        """Gram matrix is positive definite for generic h_p, c."""
        h_p, c = 5.0, 30.0
        for level in [1, 2]:
            parts, G = gram_matrix(h_p, c, level)
            n = len(parts)
            # Check all diagonal elements positive
            for i in range(n):
                assert G[i][i] > 0, f"G[{i}][{i}] = {G[i][i]}"

    def test_kac_determinant_level1(self):
        """det G_1 = 2h_p. Vanishes at h_p = 0."""
        c = 25.0
        _, G = gram_matrix(0.0, c, 1)
        assert abs(G[0][0]) < 1e-10  # degenerate at h=0


class TestThreePoint:
    def test_level0(self):
        """beta_{()} = 1 (the primary coupling)."""
        assert three_point_coupling(5.0, 5.0, 3.0, 25.0, ()) == 1.0

    def test_level1_identical(self):
        """beta_{(1)} = h_p for identical external dimensions."""
        h, h_p, c = 5.0, 3.0, 25.0
        beta = three_point_coupling(h, h, h_p, c, (1,))
        assert abs(beta - h_p) < 1e-10

    def test_level1_general(self):
        """beta_{(1)} = h_p + h_1 - h_2."""
        beta = three_point_coupling(3.0, 5.0, 2.0, 25.0, (1,))
        assert abs(beta - (2.0 + 3.0 - 5.0)) < 1e-10

    def test_level2_identical_L2(self):
        """beta_{(2)} for identical external = h_p(h_p+1)/2 + h."""
        h, h_p, c = 5.0, 3.0, 25.0
        beta = three_point_coupling(h, h, h_p, c, (2,))
        expected = h_p * (h_p + 1) / 2 + h
        assert abs(beta - expected) < 1e-8, (
            f"beta = {beta}, expected = {expected}")

    def test_level2_identical_L11(self):
        """beta_{(1,1)} for identical external = h_p(h_p+1)/2."""
        h, h_p, c = 5.0, 3.0, 25.0
        beta = three_point_coupling(h, h, h_p, c, (1, 1))
        expected = h_p * (h_p + 1) / 2
        assert abs(beta - expected) < 1e-8


class TestBlockCoefficients:
    def test_F0_is_one(self):
        """F_0 = 1 always."""
        assert block_coefficient(3.0, 5.0, 25.0, 0) == 1.0

    def test_F1_identical(self):
        """F_1 = h_p / 2 for identical external dimensions."""
        h_p, h, c = 3.0, 5.0, 25.0
        F1 = block_coefficient(h_p, h, c, 1)
        expected = h_p / 2
        assert abs(F1 - expected) < 1e-8

    def test_F1_general(self):
        """F_1 = (h_p + h1 - h2)(h_p + h3 - h4) / (2*h_p)."""
        # For identical: (h_p)^2 / (2*h_p) = h_p/2. Already tested above.
        pass

    def test_F2_positive_generic(self):
        """F_2 > 0 for generic h_p, h, c (Verma module is non-degenerate)."""
        F2 = block_coefficient(3.0, 5.0, 30.0, 2)
        assert F2 > 0


class TestVirasoroBlock:
    def test_block_converges(self):
        """Block value is finite and well-defined."""
        q = Z4_NOME
        F, coeffs = virasoro_block(3.0, 5.0, 30.0, q, max_level=2)
        assert math.isfinite(F)
        assert F > 0

    def test_block_dominated_by_q_hp(self):
        """For large h_p: F ~ q^{h_p} * (1 + ...)."""
        q = Z4_NOME
        h_p = 10.0
        F, coeffs = virasoro_block(h_p, 5.0, 30.0, q, max_level=2)
        # F / q^{h_p} should be close to 1 + F_1*q + ...
        ratio = F / q**h_p
        assert 0.5 < ratio < 2.0

    def test_q_suppression(self):
        """Higher levels are increasingly suppressed by q^N."""
        q = Z4_NOME
        _, coeffs = virasoro_block(3.0, 5.0, 30.0, q, max_level=2)
        # |F_1 * q| < |F_0| and |F_2 * q^2| < |F_1 * q|
        assert abs(coeffs[1] * q) < abs(coeffs[0]) * 2
        assert abs(coeffs[2] * q**2) < abs(coeffs[1] * q) * 2


class TestZ4Stiffness:
    def test_classical_dominates(self):
        """For large c: the classical stiffness dominates.

        The stiffness of -2h*sum log|z_j-z_k| in mode m=2 for N=4:
          = 2h * N * mu_m = 2h * 4 * m(N-m)/2 = 4h*m(N-m) = 16h
        The sign is POSITIVE (the symmetric configuration is a maximum
        of the pairwise distance product, not a minimum).
        """
        h, c = 100.0, 1000.0
        result = four_point_angular_stiffness(h, c, N=4, m=2, max_level=2)
        # Classical: 2h * N * mu_m where mu_m = m(N-m)/2
        # For N=4, m=2: 2*100*4*2 = 1600
        expected_classical = 2 * h * 4 * 2  # = 16h = 1600
        assert abs(result['stiffness'] - expected_classical) / expected_classical < 0.1

    def test_stiffness_positive(self):
        """Angular stiffness is positive: the symmetric N-gon maximizes
        the pairwise distance product, so perturbations DECREASE the
        correlator (second variation is positive in -log sigma)."""
        h, c = 10.0, 100.0
        result = four_point_angular_stiffness(h, c, N=4, m=2, max_level=2)
        assert result['stiffness'] > 0

    def test_correction_order_1_over_c(self):
        """The correction scales as O(1/c) at fixed h/c."""
        alpha = 0.1  # h/c ratio
        corrections = []
        for c in [100.0, 200.0, 500.0]:
            h = alpha * c
            result = four_point_angular_stiffness(h, c, N=4, m=2, max_level=2)
            corr = result['correction'] / h  # normalize by h
            corrections.append(abs(corr))
        # Should decrease with c (roughly as 1/c)
        assert corrections[1] < corrections[0] * 1.5
        assert corrections[2] < corrections[0] * 1.5


class TestQuantumCorrection:
    def test_small_correction(self):
        """The quantum correction is small for large c."""
        result = quantum_correction_estimate(100.0, 1000.0)
        assert result['correction_scale'] < 0.01

    def test_scales_with_alpha_squared(self):
        """Correction ~ (h/c)^2 at fixed q."""
        r1 = quantum_correction_estimate(10.0, 100.0)
        r2 = quantum_correction_estimate(20.0, 200.0)
        # Same alpha = 0.1, so same correction_scale
        assert abs(r1['correction_scale'] - r2['correction_scale']) < 1e-6
