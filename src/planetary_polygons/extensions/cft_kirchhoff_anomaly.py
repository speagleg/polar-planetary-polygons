"""
Pipeline C: Kirchhoff Hamiltonian = regularized Liouville action.

THEOREM (Kirchhoff-Liouville decomposition).
The polygon self-energy constant b(N) decomposes as:

    b(N) = (1/(N-1)) * sum_{m=1}^{N-1} [f(m,N) + log sin(pi*m/N)]

where:
  - f(m,N) = m(N-m)/2 is the Havelock Casimir (conformal weight of the
    m-th Z_N twist field)
  - log sin(pi*m/N) is the logarithmic cone-angle contribution from the
    m-th puncture on the N-punctured sphere

The Polyakov anomaly identification c/12 = b(N) then gives c = 12 b(N).

DERIVATION.
On the N-punctured sphere S^2 \\ {z_1,...,z_N} with equal cone angles
2*pi/N at each puncture, the one-loop effective action of the scalar
Laplacian decomposes mode-by-mode under Z_N:

  W_eff = sum_m W_m = sum_m [h_m * A_WP + sigma_m]

where h_m = f(m,N) is the conformal weight (from the equivariant Chern
character), A_WP is the Weil-Petersson area element, and
sigma_m = log sin(pi*m/N) is the conical defect's spectral contribution
(from the conical zeta function at the m-th Fourier mode, Cheeger 1979).

The anomaly coefficient per mode is (h_m + sigma_m).
Averaging over the (N-1) non-trivial Z_N modes gives b(N) = c/12.
"""
from __future__ import annotations

from math import log, pi, sin


def casimir(m: int, N: int) -> float:
    """Havelock Casimir f(m,N) = m(N-m)/2."""
    return m * (N - m) / 2.0


def b_N(N: int) -> float:
    """Polygon self-energy constant."""
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


# ================================================================
# Structural decomposition of b(N)
# ================================================================

def casimir_contribution(N: int) -> float:
    """Mean Casimir: (1/(N-1)) * sum_{m=1}^{N-1} f(m,N) = N(N+1)/12.

    Proof (exact):
      sum_{m=1}^{N-1} m(N-m)/2 = N(N-1)(N+1)/12
      Dividing by (N-1): N(N+1)/12.
    """
    total = sum(casimir(m, N) for m in range(1, N))
    return total / (N - 1)


def cone_angle_contribution(N: int) -> float:
    """Cone-angle part: (1/(N-1)) * sum_{m=1}^{N-1} log(sin(pi*m/N)).

    Uses the Gauss product: prod sin(pi*m/N) = N / 2^{N-1}.
    So sum log sin = log(N) - (N-1) log 2.
    Dividing by (N-1): log(N)/(N-1) - log 2.
    """
    total = sum(log(sin(pi * m / N)) for m in range(1, N))
    return total / (N - 1)


def mode_weight(m: int, N: int) -> float:
    """Per-mode anomaly weight: f(m,N) + log sin(pi*m/N).

    This is the m-th term in the Kirchhoff-Liouville decomposition.
    The conformal weight h_m = f(m,N) comes from the equivariant
    Chern character; the log sin term comes from the conical defect.
    """
    return casimir(m, N) + log(sin(pi * m / N))


def b_from_mode_decomposition(N: int) -> float:
    """Compute b(N) via the mode decomposition.

    b(N) = (1/(N-1)) * sum_{m=1}^{N-1} [f(m,N) + log sin(pi*m/N)]

    This is the DEFINITION-FREE computation: no reference to the
    formula N(N+1)/12 - log 2 + log(N)/(N-1).  The equality of
    this sum with that formula IS the structural identity.
    """
    total = sum(mode_weight(m, N) for m in range(1, N))
    return total / (N - 1)


# ================================================================
# Polyakov anomaly identification
# ================================================================

def cone_defect_coefficient(N: int) -> float:
    """Polyakov-Alvarez conical defect coefficient.

    For cone angle 2*pi*alpha at a point, the anomaly picks up:
      (1/12)(alpha + 1/alpha - 2)

    For alpha = 1/N: coefficient = 1/N + N - 2.
    """
    alpha = 1.0 / N
    return alpha + 1.0 / alpha - 2


def gauss_product(N: int) -> float:
    """Gauss product: prod_{m=1}^{N-1} 2 sin(pi*m/N) = N.

    Standard identity (DLMF 4.21.31).
    """
    result = 1.0
    for m in range(1, N):
        result *= 2 * sin(pi * m / N)
    return result


def orbifold_euler_char(N: int) -> float:
    """Orbifold Euler characteristic of S^2 with N cone points of angle 2pi/N.

    chi_orb = chi(S^2) + sum_k (1/alpha_k - 1)
            = 2 + N * (N - 1)

    where alpha_k = 1/N for each of the N punctures.
    """
    return 2 + N * (N - 1)


def central_charge_pipeline_C(N: int) -> float:
    """Extract c from the Kirchhoff-Liouville decomposition.

    The mode-averaged anomaly weight is b(N), and the Polyakov
    identification gives c = 12 * b(N).

    This is Pipeline C: no external CFT data used, only:
    1. Havelock Casimir f(m,N) = m(N-m)/2 (from the eigenvalue formula)
    2. Gauss product identity (from the log-sin kernel)
    3. Polyakov anomaly normalization (c/12 per scalar field)
    """
    return 12 * b_from_mode_decomposition(N)
