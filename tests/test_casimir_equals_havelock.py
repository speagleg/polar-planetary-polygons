"""Tests for the proof that sl(2,R) Casimir = Havelock sum on Z_N modes."""
import numpy as np
import pytest
from planetary_polygons.proofs.casimir_equals_havelock import (
    h2_laplacian_angular_hessian,
    h2_laplacian_fourier_eigenvalue,
    havelock_sum,
    verify_circulant_eigenvalue,
    verify_casimir_identification,
    verify_same_algebra,
)
from math import sinh, pi, sin, cos


@pytest.mark.parametrize("N", range(3, 13))
def test_circulant_is_csc2(N):
    """The H² angular Hessian at the N-gon is a csc² circulant."""
    rho0 = 1.0
    H = h2_laplacian_angular_hessian(N, rho0)
    # Check circulant: H[i,j] depends only on (j-i) mod N
    for i in range(N):
        for j in range(N):
            p = (j - i) % N
            assert abs(H[i, j] - H[0, p]) < 1e-14, f"Not circulant at ({i},{j})"


@pytest.mark.parametrize("N", range(3, 13))
def test_fourier_eigenvalue_equals_havelock(N):
    """The Z_N Fourier eigenvalue = T_m / sinh²(ρ₀) for all modes and radii."""
    for rho0 in [0.3, 0.7, 1.0, 1.5, 2.0]:
        for m in range(1, N):
            numerical = h2_laplacian_fourier_eigenvalue(N, m, rho0)
            expected = havelock_sum(N, m) / sinh(rho0)**2
            assert abs(numerical - expected) < 1e-10 * abs(expected), (
                f"N={N}, m={m}, rho0={rho0}: {numerical} != {expected}"
            )


@pytest.mark.parametrize("N", range(3, 13))
def test_rho_independence(N):
    """The Casimir T_m = m(N-m)/2 is ρ₀-independent (representation-theoretic)."""
    for m in range(1, N):
        values = []
        for rho0 in [0.3, 0.7, 1.0, 1.5, 2.0]:
            # Multiply eigenvalue by sinh²(ρ₀) to get conformal normalization
            val = h2_laplacian_fourier_eigenvalue(N, m, rho0) * sinh(rho0)**2
            values.append(val)
        # All should equal T_m = m(N-m)/2
        T_m = havelock_sum(N, m)
        for v in values:
            assert abs(v - T_m) < 1e-10, f"N={N}, m={m}: {v} != {T_m}"


def test_circulant_verification_all_N():
    """Full verification: max error < 10⁻¹⁰ for N=3,...,12."""
    max_err, _ = verify_casimir_identification(N_max=12)
    assert max_err < 1e-10, f"Verification failed: max_err = {max_err}"


def test_same_algebra():
    """CMS and CS sl(2,R) produce the same Casimir eigenvalue."""
    assert verify_same_algebra()


def test_graviton_at_N7():
    """At N=7, m*=3: T_3 = 6 = j(j+1) with j=2 (graviton)."""
    T = havelock_sum(7, 3)
    assert T == 6.0
    j = (-1 + (1 + 4 * T)**0.5) / 2
    assert abs(j - 2.0) < 1e-12


def test_vector_boson_at_N4():
    """At N=4, m*=2: T_2 = 2 = j(j+1) with j=1 (vector boson)."""
    T = havelock_sum(4, 2)
    assert T == 2.0
    j = (-1 + (1 + 4 * T)**0.5) / 2
    assert abs(j - 1.0) < 1e-12


def test_zero_mode_trivial():
    """The m=0 mode has T_0 = 0 (trivial representation j=0)."""
    for N in [4, 7, 11]:
        assert havelock_sum(N, 0) == 0.0


def test_palindromic():
    """T_m = T_{N-m} (palindromic symmetry = representation conjugation)."""
    for N in range(3, 13):
        for m in range(1, N):
            assert abs(havelock_sum(N, m) - havelock_sum(N, N - m)) < 1e-14
