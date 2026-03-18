# tests/test_two_ring.py
"""Tests for the two-ring stability analysis and center-ring dichotomy."""
import numpy as np
from planetary_polygons.extensions.two_ring import (
    two_ring_positions,
    two_ring_constrained_eigenvalues,
    symmetry_breaking_theorem_check,
)


def test_positions_correct_count():
    z = two_ring_positions(N=6, M=3, R1=0.5, R2=1.0)
    assert len(z) == 9


def test_positions_on_circles():
    z = two_ring_positions(N=6, M=3, R1=0.5, R2=1.5)
    assert np.allclose(np.abs(z[:3]), 0.5)
    assert np.allclose(np.abs(z[3:]), 1.5)


def test_inner_ring_destabilizes_stable_base():
    """
    CENTER-RING DICHOTOMY, part (i):
    For N <= 7 (base stable), adding M >= 2 inner vortices
    always introduces at least one negative eigenvalue.
    """
    for N in [5, 6, 7]:
        for M in [2, 3, 4]:
            for ratio in [1.5, 2.0, 3.0]:
                R1 = 0.4
                R2 = R1 * ratio
                evals = two_ring_constrained_eigenvalues(N, M, R1, R2)
                n_neg = int(np.sum(evals < -1e-6))
                assert n_neg >= 1, (
                    f"N={N}, M={M}, R2/R1={ratio}: expected destabilization "
                    f"but got n_neg={n_neg}"
                )


def test_inner_ring_cannot_fully_stabilize():
    """
    CENTER-RING DICHOTOMY, part (ii):
    For N >= 8 (base unstable), an inner ring of M >= 2 vortices
    cannot achieve n_neg = 0 (full stabilization).
    """
    for N in [8, 9, 10]:
        for M in [2, 3, 4, 5]:
            if M >= N:
                continue
            for ratio in [1.5, 2.0, 3.0, 5.0]:
                R1 = 0.4
                R2 = R1 * ratio
                evals = two_ring_constrained_eigenvalues(N, M, R1, R2)
                n_neg = int(np.sum(evals < -1e-6))
                assert n_neg >= 1, (
                    f"N={N}, M={M}, R2/R1={ratio}: inner ring achieved "
                    f"full stabilization (n_neg=0), contradicting dichotomy"
                )


def test_full_survey_consistent():
    """Run the full symmetry-breaking check and verify summary statistics."""
    results = symmetry_breaking_theorem_check()
    stable_base = [r for r in results if r['base_n_neg'] == 0]
    unstable_base = [r for r in results if r['base_n_neg'] > 0]

    # All stable-base cases are destabilized
    assert all(r['two_ring_n_neg'] > 0 for r in stable_base)

    # No unstable-base case is fully stabilized
    assert all(r['two_ring_n_neg'] > 0 for r in unstable_base)
