"""Tests for the dimension theorem: polynomial eigenvalues iff d = 2."""

import pytest
import numpy as np
from math import pi

from planetary_polygons.extensions.dimension_proof import (
    csc_alpha_sum, second_difference, second_difference_formula,
    verify_second_difference, proof_table,
    holomorphic_factorization, verify_factorization,
    dimension_theorem_check,
)


class TestSecondDifference:
    """Δ²S_α(m) is constant iff α = 2."""

    @pytest.mark.parametrize("N", [7, 10, 13])
    def test_alpha2_constant(self, N):
        """α = 2: Δ² = -4 (constant) for all m."""
        _, is_const, rel_dev = verify_second_difference(N, 2.0)
        assert is_const, f"N={N}: α=2 should give constant Δ² (dev={rel_dev:.2e})"

    @pytest.mark.parametrize("N", [7, 10, 13])
    def test_alpha2_equals_minus4(self, N):
        """α = 2: Δ² = -4 exactly."""
        vals, _, _ = verify_second_difference(N, 2.0)
        for v in vals:
            if v['numeric'] is not None:
                assert abs(v['numeric'] - (-4.0)) < 1e-10, (
                    f"N={N}, m={v['m']}: Δ²={v['numeric']}, expected -4"
                )

    @pytest.mark.parametrize("N,alpha", [(7, 1.5), (7, 3.0), (10, 3.0), (13, 4.0)])
    def test_alpha_neq2_not_constant(self, N, alpha):
        """α ≠ 2: Δ² varies with m."""
        _, is_const, rel_dev = verify_second_difference(N, alpha)
        assert not is_const, (
            f"N={N}, α={alpha}: should NOT be constant (dev={rel_dev:.2e})"
        )

    @pytest.mark.parametrize("N", [7, 10])
    def test_formula_matches_numeric(self, N):
        """The analytic formula Δ² = 4Σcos·sin^{2-α} matches numeric."""
        for alpha in [2.0, 3.0]:
            vals, _, _ = verify_second_difference(N, alpha)
            for v in vals:
                if v['numeric'] is not None:
                    assert v['match'], (
                        f"N={N}, α={alpha}, m={v['m']}: "
                        f"numeric={v['numeric']:.6f} vs formula={v['formula']:.6f}"
                    )


class TestHolomorphicFactorization:
    """[1-cos(2πpm/N)]/sin²(πp/N) = 2|Σω^{pk}|² (per-p identity)."""

    @pytest.mark.parametrize("N", [7, 10, 13, 16])
    def test_factorization_exact(self, N):
        """The holomorphic factorization holds to machine precision."""
        max_err = verify_factorization(N)
        assert max_err < 1e-10, f"N={N}: factorization error {max_err:.2e}"


class TestDimensionTheorem:
    """The full theorem: polynomial iff d = 2."""

    @pytest.mark.parametrize("N", [7, 10, 13])
    def test_theorem_holds(self, N):
        results = dimension_theorem_check([N])
        assert results[0]['theorem_holds'], (
            f"N={N}: theorem failed — "
            f"α2={results[0]['alpha2_polynomial']}, "
            f"α3={results[0]['alpha3_polynomial']}, "
            f"fact={results[0]['factorization_error']:.1e}"
        )

    def test_proof_table_only_alpha2(self):
        """In the full proof table, only α = 2.0 rows are polynomial."""
        for r in proof_table([7, 10], [1.5, 2.0, 2.5, 3.0]):
            if abs(r['alpha'] - 2.0) < 0.01:
                assert r['polynomial'], f"N={r['N']}, α=2.0 should be poly"
            else:
                assert not r['polynomial'], (
                    f"N={r['N']}, α={r['alpha']} should NOT be poly"
                )
