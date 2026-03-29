"""Tests for the algebraic proof of Riemannian Havelock Step 3."""
import numpy as np
import pytest
from planetary_polygons.proofs.riemannian_havelock_step3 import (
    tangential_circulant_eigenvalue,
    tangential_circulant_eigenvalue_from_DFT,
    verify_step3,
)


@pytest.mark.parametrize("N", range(3, 13))
def test_havelock_identity_all_modes(N):
    """DFT eigenvalue equals m(N-m)/(2ρ²) for all modes."""
    for rho in [0.1, 0.3, 0.5, 0.7, 0.9]:
        for m in range(1, N):
            exact = tangential_circulant_eigenvalue(m, N, rho)
            numerical = tangential_circulant_eigenvalue_from_DFT(m, N, rho)
            assert abs(exact - numerical) < 1e-10 * abs(exact), (
                f"N={N}, m={m}, rho={rho}: {exact} != {numerical}"
            )


def test_zero_mode_vanishes():
    """The m=0 mode (uniform rotation) has zero eigenvalue."""
    for N in [5, 7, 11]:
        lam = tangential_circulant_eigenvalue_from_DFT(0, N, 0.5)
        assert abs(lam) < 1e-10


def test_palindromic_symmetry():
    """λ_m = λ_{N-m} (palindromic symmetry of the Havelock sum)."""
    for N in [5, 7, 11]:
        for m in range(1, N // 2 + 1):
            lam_m = tangential_circulant_eigenvalue(m, N, 0.5)
            lam_Nm = tangential_circulant_eigenvalue(N - m, N, 0.5)
            assert abs(lam_m - lam_Nm) < 1e-12


def test_rho_independence_of_structure():
    """The MODE STRUCTURE m(N-m)/2 is ρ-independent; only the prefactor 1/ρ² changes."""
    N = 7
    for m in range(1, N):
        ratio_prev = None
        for rho in [0.2, 0.4, 0.6, 0.8]:
            lam = tangential_circulant_eigenvalue_from_DFT(m, N, rho)
            ratio = lam * rho**2 / (m * (N - m) / 2)
            if ratio_prev is not None:
                assert abs(ratio - ratio_prev) < 1e-10
            ratio_prev = ratio


def test_step3_comprehensive():
    """Full verification: max relative error < 10⁻¹⁰ for N=3,...,12."""
    err = verify_step3(N_max=12)
    assert err < 1e-10, f"Step 3 verification failed: max_err = {err}"


def test_confining_potential_tangential_zero():
    """The H² confining potential has zero tangential Hessian (analytically).

    V_rad = (N-1)/2 × Σ ln(a² - |z_k|²) depends only on |z_k| = ρ.
    Under tangential perturbation z_k → ρ exp(i(θ_k + ε amp_k)):
      |z_k| = ρ (unchanged)  ⟹  V_rad unchanged  ⟹  ∂²V_rad/∂ε² = 0.

    This is the key to the abstract proof: ALL curvature effects enter
    through V_rad and J, both of which are radial, so the tangential
    eigenvalue is determined purely by the flat csc² interaction.
    """
    # This test just documents the proof — the tangential Hessian is
    # analytically zero because |z_k| is preserved under tangential perturbation.
    N, rho, a = 7, 0.5, 1.0
    for m in range(1, N):
        k = np.arange(N)
        theta = 2 * np.pi * k / N
        amp = np.cos(2 * np.pi * m * k / N)
        # Perturbed positions:
        z_pert = rho * np.exp(1j * (theta + 0.01 * amp))
        # |z_k| is preserved:
        assert np.allclose(np.abs(z_pert), rho, atol=1e-14)
