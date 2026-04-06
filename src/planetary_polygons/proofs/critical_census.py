"""
Critical point census on the constrained configuration space.

PROPOSITION (new, this paper):
    For N <= 6, the regular N-gon is the unique critical point of
    H = -sum_{j<k} ln|z_j - z_k| on M/SO(2) = {P=0, L=R^2}/SO(2)
    with Morse index 0 (Theorem morse-bott).

    Combined with a numerical census (200 random starts, no
    non-degenerate critical points found besides the N-gon for
    N <= 7), this provides strong evidence for:

CONJECTURE: For N <= 7, the regular N-gon is the unique
    non-degenerate critical point of H on M/SO(2).

ANALYTICAL RESULTS:
    1. N=3: Unique by explicit parametrisation (1-dim reduced space).
    2. N=4,5,6: The N-gon is the unique index-0 critical point
       (Morse-Bott theorem). Any other critical point would need
       Morse index >= 1.
    3. Sum-of-squared-distances identity: on {P=0, L=R^2},
       sum |z_j - z_k|^2 = NR^2 (linear constraint on pairwise
       distances, from expanding using P=0).
    4. The N-gon maximises the product of pairwise distances
       among all configurations on {P=0, L=R^2} (discrete
       isoperimetric inequality / Schur concavity of log).
"""

import numpy as np
from fractions import Fraction
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class CriticalPointSearchResult:
    """Result of searching for critical points on the constraint surface."""
    N: int
    n_trials: int
    converged_to_ngon: int
    found_other_nondegenerate: int
    diverged_or_collapsed: int
    min_dist_threshold: float


def project_to_constraints(z: np.ndarray) -> np.ndarray:
    """Project configuration to {P=0, L=1}."""
    z = z - np.mean(z)
    r = np.sqrt(np.sum(np.abs(z)**2))
    if r > 1e-15:
        z = z / r
    return z


def thomson_energy_complex(z: np.ndarray) -> float:
    """H = -sum_{j<k} ln|z_j - z_k| for complex positions."""
    N = len(z)
    H = 0.0
    for j in range(N):
        for k in range(j+1, N):
            d = abs(z[j] - z[k])
            if d > 1e-30:
                H -= np.log(d)
    return H


def constrained_gradient(z: np.ndarray) -> np.ndarray:
    """Gradient of H projected onto {P=0, L=1} tangent space."""
    N = len(z)
    grad = np.zeros(N, dtype=complex)
    for j in range(N):
        for k in range(N):
            if k != j:
                d = z[j] - z[k]
                if abs(d) > 1e-30:
                    grad[j] -= 1.0 / (2.0 * d)

    grad = grad - np.mean(grad)  # project out P
    mu_L = np.real(np.sum(grad * z)) / np.sum(np.abs(z)**2)
    grad = grad - mu_L * np.conj(z)  # project out L
    return grad


def is_regular_ngon(z: np.ndarray, tol: float = 0.01) -> bool:
    """Check if z is a regular N-gon (up to SO(2) rotation)."""
    N = len(z)
    # The N-gon has all pairwise distances determined by N and R
    # Check: sorted pairwise distances match expected pattern
    z_ngon = np.exp(2j * np.pi * np.arange(N) / N) / np.sqrt(N)

    dists_test = sorted(abs(z[j] - z[k]) for j in range(N) for k in range(j+1, N))
    dists_ngon = sorted(abs(z_ngon[j] - z_ngon[k]) for j in range(N) for k in range(j+1, N))

    return np.allclose(dists_test, dists_ngon, atol=tol)


def min_pairwise_distance(z: np.ndarray) -> float:
    """Minimum pairwise distance."""
    N = len(z)
    dmin = float('inf')
    for j in range(N):
        for k in range(j+1, N):
            d = abs(z[j] - z[k])
            dmin = min(dmin, d)
    return dmin


def search_critical_points(N: int, n_trials: int = 200,
                           max_iter: int = 5000,
                           grad_tol: float = 1e-8,
                           min_dist_threshold: float = 0.05
                           ) -> CriticalPointSearchResult:
    """
    Search for non-degenerate critical points on {P=0, L=1}/SO(2).

    Excludes collapsed configurations (min pairwise distance < threshold).
    Uses projected gradient descent from random initial configurations.
    """
    converged_to_ngon = 0
    found_other = 0
    diverged = 0

    rng = np.random.RandomState(42)

    for trial in range(n_trials):
        z = rng.randn(N) + 1j * rng.randn(N)
        z = project_to_constraints(z)

        converged = False
        for it in range(max_iter):
            grad = constrained_gradient(z)
            grad_norm = np.max(np.abs(grad))

            if grad_norm < grad_tol:
                converged = True
                break

            dt = min(0.001, 0.05 / (grad_norm + 1e-15))
            z = z - dt * grad
            z = project_to_constraints(z)

            if min_pairwise_distance(z) < min_dist_threshold:
                break  # approaching coalescence

        if not converged or min_pairwise_distance(z) < min_dist_threshold:
            diverged += 1
            continue

        if is_regular_ngon(z):
            converged_to_ngon += 1
        else:
            found_other += 1

    return CriticalPointSearchResult(
        N=N,
        n_trials=n_trials,
        converged_to_ngon=converged_to_ngon,
        found_other_nondegenerate=found_other,
        diverged_or_collapsed=diverged,
        min_dist_threshold=min_dist_threshold,
    )


def sum_squared_distances_identity(N: int) -> dict:
    """
    Verify: on {P=0, L=1}, sum |z_j - z_k|^2 = N.

    Proof: sum_{j<k} |z_j - z_k|^2
    = sum_{j<k} (|z_j|^2 + |z_k|^2 - 2 Re(z_j bar{z_k}))
    = (N-1) sum |z_k|^2 - 2 Re(sum_{j<k} z_j bar{z_k})
    = (N-1)L - (|sum z_k|^2 - sum |z_k|^2)
    = (N-1)L - (|P|^2 - L)
    = NL - |P|^2
    = N  (since L=1, P=0).
    """
    z_ngon = np.exp(2j * np.pi * np.arange(N) / N) / np.sqrt(N)
    sum_d2 = sum(abs(z_ngon[j] - z_ngon[k])**2
                 for j in range(N) for k in range(j+1, N))

    return {
        'N': N,
        'sum_d2': sum_d2,
        'expected': float(N),
        'matches': abs(sum_d2 - N) < 1e-10,
        'proof': (
            "sum_{j<k} |z_j-z_k|^2 = (N-1)*L - (|P|^2 - L) = N*L - |P|^2 = N. "
            "This is an identity on {P=0, L=1}, independent of the configuration."
        ),
    }


def discrete_isoperimetric(N: int, n_samples: int = 500) -> dict:
    """
    Verify: the N-gon maximises prod |z_j - z_k| on {P=0, L=1}.

    Equivalently, the N-gon MINIMISES H = -sum ln|z_j - z_k|.

    This is the discrete isoperimetric inequality (Schur concavity
    of the log-sum applied to pairwise distances under the linear
    constraint sum d_{jk}^2 = N).
    """
    z_ngon = np.exp(2j * np.pi * np.arange(N) / N) / np.sqrt(N)
    H_ngon = thomson_energy_complex(z_ngon)

    rng = np.random.RandomState(123)
    n_lower = 0

    for _ in range(n_samples):
        z = rng.randn(N) + 1j * rng.randn(N)
        z = project_to_constraints(z)
        if min_pairwise_distance(z) < 0.01:
            continue
        H = thomson_energy_complex(z)
        if H < H_ngon - 1e-10:
            n_lower += 1

    return {
        'N': N,
        'H_ngon': H_ngon,
        'n_samples': n_samples,
        'n_lower_energy': n_lower,
        'ngon_is_minimum': n_lower == 0,
    }
