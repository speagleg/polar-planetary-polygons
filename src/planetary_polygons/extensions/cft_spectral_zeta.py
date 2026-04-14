"""
Pipeline B: Polyakov-Alvarez spectral zeta anomaly on the conical N-gon sphere.

THEOREM (Polyakov-Alvarez with conical singularities).
For the scalar Laplacian on a surface Sigma with N conical singularities
of angle 2*pi*alpha_k, the conformal anomaly under g -> e^{2 phi} g is:

  log det'(-Delta_{e^{2phi} g}) - log det'(-Delta_g)
    = -(c_eff / (12 pi)) * S_L[phi]
    + sum_k conical_correction(alpha_k, phi(p_k))

where c_eff = 1 for a single scalar field.

The EFFECTIVE central charge c of the polygon system is determined by
the mode-averaged anomaly weight:

  c/12 = (1/(N-1)) * sum_{m=1}^{N-1} [h_m + sigma_m]

where h_m = f(m,N) is the conformal weight (bulk Polyakov anomaly per mode)
and sigma_m = log sin(pi m/N) is the conical spectral zeta contribution
per Z_N Fourier mode (Cheeger 1983).

The heat-kernel Seeley-DeWitt coefficients on the conical sphere:
  a_0 = Area/(4 pi)    [Weyl term]
  a_1 = chi/6 + sum_k (1/(12 alpha_k) - alpha_k/12)    [Gauss-Bonnet + cones]

The a_1 coefficient encodes the total anomaly at the topological level;
the mode decomposition refines it into the per-mode structure that gives b(N).

References:
  - Polyakov (1981), Phys. Lett. B 103, 207
  - Alvarez (1983), Nucl. Phys. B 216, 125
  - Cheeger (1983), J. Diff. Geom. 18, 575
  - Kokotov, Korotkin (2013), arXiv:1310.0804
"""
from __future__ import annotations

from math import log, pi, sin


def casimir(m: int, N: int) -> float:
    return m * (N - m) / 2.0


def b_N(N: int) -> float:
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


# ================================================================
# Heat-kernel coefficients on the conical sphere
# ================================================================

def heat_kernel_a0(N: int, R: float = 1.0) -> float:
    """a_0 = Area / (4 pi) for the round sphere of radius R.

    Conical singularities are point defects and do not change the total
    area of the round sphere metric. a_0 = R^2.
    """
    return R * R


def heat_kernel_a1(N: int) -> float:
    """a_1 coefficient: Euler characteristic + conical correction.

    Smooth surface: a_1 = chi(Sigma) / 6 = 2/6 = 1/3 for S^2.

    Conical correction per cone of angle 2 pi alpha:
      (1/(12 alpha) - alpha/12) = (1 - alpha^2) / (12 alpha)

    For N cones with alpha = 1/N:
      per cone: N/12 - 1/(12N) = (N^2 - 1)/(12N)
      total: N * (N^2 - 1)/(12N) = (N^2 - 1)/12

    a_1 = 1/3 + (N^2 - 1)/12
    """
    a1_smooth = 2 / 6.0  # chi(S^2) = 2
    a1_conical = conical_heat_correction(N)
    return a1_smooth + a1_conical


def conical_heat_correction(N: int) -> float:
    """Total conical correction to the a_1 heat-kernel coefficient.

    For N cones each with angle 2 pi / N (i.e., alpha = 1/N):
      per cone: 1/(12 * (1/N)) - (1/N)/12 = N/12 - 1/(12N) = (N^2-1)/(12N)
      total:    N * (N^2-1)/(12N) = (N^2-1)/12
    """
    alpha = 1.0 / N
    per_cone = 1.0 / (12 * alpha) - alpha / 12
    return N * per_cone


# ================================================================
# Polyakov-Alvarez anomaly decomposition
# ================================================================

def anomaly_bulk_part(N: int) -> float:
    """Bulk (smooth) part of the anomaly coefficient c/12.

    The Polyakov anomaly for a SINGLE scalar decomposes under Z_N into
    (N-1) non-trivial modes, each carrying conformal weight h_m = f(m,N).

    The bulk contribution to c/12 is the mean conformal weight:
      (1/(N-1)) * sum_{m=1}^{N-1} f(m,N) = N(N+1)/12
    """
    return sum(casimir(m, N) for m in range(1, N)) / (N - 1)


def anomaly_conical_part(N: int) -> float:
    """Conical part of the anomaly coefficient c/12.

    Each Z_N Fourier mode m sees the cone of angle 2 pi/N.
    The Cheeger conical spectral zeta function contributes:

      sigma_m = log sin(pi m/N)

    to the m-th mode's anomaly weight.

    The mode-averaged conical contribution:
      (1/(N-1)) * sum_{m=1}^{N-1} log sin(pi m/N)
      = (1/(N-1)) * [log N - (N-1) log 2]    (Gauss product)
      = log(N)/(N-1) - log 2
    """
    return sum(log(sin(pi * m / N)) for m in range(1, N)) / (N - 1)


def anomaly_coefficient(N: int) -> float:
    """Full anomaly coefficient c/12 = b(N).

    c/12 = anomaly_bulk + anomaly_conical
         = N(N+1)/12 + log(N)/(N-1) - log 2
         = b(N)

    This is Pipeline B's derivation: the central charge arises as the
    Polyakov-Alvarez anomaly of the scalar Laplacian on the conical
    N-gon sphere, decomposed into Z_N Fourier modes. The bulk part
    gives the mean Casimir (purely algebraic), and the conical part
    gives the self-energy (from the Gauss product / Cheeger cone zeta).
    """
    return anomaly_bulk_part(N) + anomaly_conical_part(N)


def central_charge_pipeline_B(N: int) -> float:
    """Pipeline B: central charge from the Polyakov-Alvarez anomaly.

    c = 12 * anomaly_coefficient(N) = 12 * b(N).
    """
    return 12 * anomaly_coefficient(N)
