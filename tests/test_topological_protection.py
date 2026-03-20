"""
Tests for topological protection of the Morse index μ(N).

The genuine content of the index theorem: μ(N) is invariant under
mode-coupling perturbations when the boundary spectrum is non-degenerate.
"""
import numpy as np
import pytest
from planetary_polygons.proofs.topological_protection import (
    havelock_matrix, havelock_eigenvalue, morse_index,
    coupling_perturbation, random_symmetric_perturbation,
    bump_perturbation,
    compute_eigenvalue_branches, compute_spectral_flow,
    verify_topological_protection, fredholm_stability_proof,
)


class TestDiagonalBaseline:
    """Unperturbed diagonal family: SF = μ(N) by direct counting."""

    @pytest.mark.parametrize("N", [5, 6, 7, 8, 9, 10, 12])
    def test_sf_equals_mu(self, N):
        mu = morse_index(N)
        _, eigs = compute_eigenvalue_branches(N, None, 1000)
        sf, _ = compute_spectral_flow(eigs)
        assert sf == mu, f"N={N}: SF={sf} ≠ μ={mu}"


class TestTopologicalProtection:
    """SF(H + V) = μ(N) for non-degenerate boundary (N ≠ 7)."""

    @pytest.mark.parametrize("N", [8, 9, 10])
    def test_single_mode_coupling(self, N):
        """Coupling binding mode to neighbor preserves SF."""
        m_bind = N // 2
        m_nbr = m_bind - 1

        def V(N_, xi):
            return coupling_perturbation(N_, m_bind, m_nbr, 5.0, xi)

        r = verify_topological_protection(N, V, n_steps=2000)
        assert r['match'], (
            f"N={N}: SF={r['sf_perturbed']} ≠ μ={r['mu']}")

    @pytest.mark.parametrize("N", [8, 9, 10])
    def test_random_symmetric(self, N):
        """Strong random mode coupling preserves SF."""
        def V(N_, xi):
            return random_symmetric_perturbation(N_, 10.0, xi)

        r = verify_topological_protection(N, V, n_steps=2000)
        assert r['match'], (
            f"N={N}: SF={r['sf_perturbed']} ≠ μ={r['mu']}")

    @pytest.mark.parametrize("N", [8, 9, 10])
    def test_strong_localized_bump(self, N):
        """Strong localized bump coupling preserves SF."""
        def V(N_, xi):
            return bump_perturbation(N_, 3, 2, 50.0, xi)

        r = verify_topological_protection(N, V, n_steps=2000)
        assert r['match'], (
            f"N={N}: SF={r['sf_perturbed']} ≠ μ={r['mu']}")

    @pytest.mark.parametrize("N", [8, 9, 10])
    def test_very_strong_coupling(self, N):
        """Very strong perturbation (s=100) still preserves SF."""
        def V(N_, xi):
            return coupling_perturbation(N_, 3, 2, 100.0, xi)

        r = verify_topological_protection(N, V, n_steps=3000)
        assert r['match'], (
            f"N={N}: SF={r['sf_perturbed']} ≠ μ={r['mu']}")

    def test_N6_stable_preserved(self):
        """N=6 (all eigenvalues positive at ξ=0): SF = 0 under perturbation."""
        def V(N_, xi):
            return random_symmetric_perturbation(N_, 10.0, xi)

        r = verify_topological_protection(6, V, n_steps=2000)
        assert r['sf_perturbed'] == 0


class TestN7Marginality:
    """N=7 is the EXCEPTION: zero eigenvalues make SF perturbation-dependent."""

    def test_n7_zero_eigenvalues(self):
        """N=7 has λ₃ = λ₄ = 0 at ξ=0."""
        H0 = havelock_matrix(7, 0.0)
        eigs = np.linalg.eigvalsh(H0)
        n_zero = np.sum(np.abs(eigs) < 1e-10)
        assert n_zero == 2

    def test_n7_sf_can_differ_from_mu(self):
        """A strong perturbation at N=7 can change SF (boundary degenerate)."""
        def V(N_, xi):
            return random_symmetric_perturbation(N_, 10.0, xi)

        _, eigs = compute_eigenvalue_branches(7, V, 4000)
        sf, _ = compute_spectral_flow(eigs)
        # SF can be 0 or 1 depending on whether V pushes zero eigenvalues
        # negative. This is NOT a failure of the theorem — the theorem
        # explicitly requires non-degenerate boundary.
        assert sf in [0, 1], f"N=7: SF={sf}, expected 0 or 1"

    def test_n7_weak_perturbation_preserves_sf(self):
        """Weak perturbation at N=7 preserves SF = 0."""
        def V(N_, xi):
            return random_symmetric_perturbation(N_, 0.1, xi)

        r = verify_topological_protection(7, V, n_steps=2000)
        assert r['sf_perturbed'] == 0


class TestAvoidedCrossings:
    """Perturbations create avoided crossings but preserve SF."""

    def test_avoided_crossing_visible(self):
        """N=8: coupling m=3 (negative) to m=2 (positive) creates
        an avoided crossing. Eigenvalues repel but SF = 3."""
        def V(N_, xi):
            return coupling_perturbation(N_, 3, 2, 8.0, xi)

        xi, eigs = compute_eigenvalue_branches(8, V, 2000)
        sf, crossings = compute_spectral_flow(eigs)
        assert sf == 3

        # Evidence of coupling: at peak perturbation (ξ ≈ 0.5),
        # the eigenvalue gap between the two coupled modes differs
        # from the unperturbed gap (level repulsion)
        _, eigs_diag = compute_eigenvalue_branches(8, None, 2000)
        mid = len(xi) // 2
        gap_pert = eigs[mid, 2] - eigs[mid, 1]  # gap near avoided crossing
        gap_diag = eigs_diag[mid, 2] - eigs_diag[mid, 1]
        assert abs(gap_pert - gap_diag) > 0.1, "No visible coupling effect"


class TestBoundaryConditions:
    """V(0) = 0 and V → 0 as ξ → 1 are essential."""

    def test_V_vanishes_at_zero(self):
        """sin(πξ) envelope ensures V(0) = 0."""
        V = coupling_perturbation(8, 3, 2, 100.0, 0.0)
        assert np.allclose(V, 0)

    def test_V_vanishes_near_one(self):
        """sin(πξ) envelope ensures V → 0 as ξ → 1."""
        V = coupling_perturbation(8, 3, 2, 100.0, 0.999)
        assert np.max(np.abs(V)) < 0.32  # sin(π·0.999) ≈ 0.003


class TestProofStructure:
    """The proof outline is complete and references the right theorems."""

    def test_proof_has_four_steps(self):
        proof = fredholm_stability_proof()
        assert len(proof['proof_steps']) == 4

    def test_proof_references_robbin_salamon(self):
        proof = fredholm_stability_proof()
        step1 = proof['proof_steps'][0]['content']
        assert 'Robbin-Salamon' in step1
