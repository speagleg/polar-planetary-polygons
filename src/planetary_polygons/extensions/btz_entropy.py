"""
BTZ entropy from palindromic wall-crossing: microscopic accounting.

The L^2-Morse index tau(P_-) on the Bolza surface counts (with signs)
the eigenvalues of the Havelock Hessian below zero. For a fractional
index, the non-integer part encodes geometric information.

The BTZ entropy: S_BTZ = 2*pi*r_+ / (4*G) = pi*sqrt(c/6) * sqrt(E)
At the threshold E ~ 0, so S is controlled by palindromic wall-crossing.

Each palindromic threshold contributes:
  - log(2) per crossing (self-paired mode, even N)
  - 2*log(2) per crossing (paired modes, odd N)
from the Z/2 Galois action (palindromic symmetry m <-> N-m).
"""

import numpy as np
from math import pi, sin, cos, log, exp, sqrt, sinh


def casimir(m, N):
    return m * (N - m) / 2.0


def b_exact(N):
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


def havelock_eigenvalue_h2(m, N, rho):
    """Havelock eigenvalue on H^2 at geodesic radius rho."""
    lam = 0.0
    for p in range(1, N):
        two_sinh = 2 * sinh(rho) * abs(sin(pi * p / N))
        lam += -log(two_sinh) * cos(2 * pi * p * m / N)
    return lam


def find_threshold(N, m_crit=None):
    """Find palindromic threshold rho*(N)."""
    if m_crit is None:
        m_crit = N // 2
    f_crit = casimir(m_crit, N)
    b = b_exact(N)
    target = f_crit - b
    if target > 0:
        return np.arcsinh(exp(target) / 2)
    return 0.01


# =====================================================================
# Bolza eigenvalues (Strohmaier-Uski, trivial representation)
# =====================================================================

BOLZA_EIGENVALUES_TRIVIAL = [
    3.8388872588, 3.8388872588, 3.8388872588,  # lambda_1 (mult 3)
    15.046564631, 15.046564631, 15.046564631,   # lambda_5 (mult 3)
    18.658498707,                                # lambda_7 (mult 1)
    23.027091498, 23.027091498, 23.027091498,   # lambda_10 (mult 3)
    28.079633028,                                # lambda_13 (mult 1)
    33.591056207, 33.591056207, 33.591056207,   # lambda_16 (mult 3)
    38.937561909,                                # lambda_19 (mult 1)
    41.304610975, 41.304610975, 41.304610975,   # lambda_21 (mult 3)
    45.888853503, 45.888853503, 45.888853503,   # lambda_24 (mult 3)
    50.284938384,                                # lambda_27 (mult 1)
    55.130693285, 55.130693285, 55.130693285,   # lambda_30 (mult 3)
]


# =====================================================================
# L^2-Morse index
# =====================================================================

def morse_index_L2(N, rho, bolza_eigenvalues=None):
    """L^2-Morse index with optional Bolza regularisation.

    Returns (tau, n_negative, eigenvalues).
    """
    eigenvalues = [havelock_eigenvalue_h2(m, N, rho) for m in range(1, N)]
    n_negative = sum(1 for lam in eigenvalues if lam < 0)

    if bolza_eigenvalues is not None:
        tau = 0.0
        neg_evals = sorted([lam for lam in eigenvalues if lam < 0])
        for i, lam in enumerate(neg_evals):
            if i < len(bolza_eigenvalues):
                tau += abs(lam) / (4 * pi * bolza_eigenvalues[i])
            else:
                mu_asymp = 4 * pi * (i + 1)
                tau += abs(lam) / mu_asymp
    else:
        tau = float(n_negative)

    return tau, n_negative, eigenvalues


def fractional_morse_index(N, rho):
    """Fractional L^2-Morse index at (N, rho).

    Returns (tau, n_neg, (|lam|, mode, lam) for closest-to-zero mode).
    """
    tau, n_neg, eigenvalues = morse_index_L2(N, rho, BOLZA_EIGENVALUES_TRIVIAL)
    abs_evals = [(abs(lam), m + 1, lam) for m, lam in enumerate(eigenvalues)]
    abs_evals.sort()
    return tau, n_neg, abs_evals[0]


# =====================================================================
# Wall-crossing entropy
# =====================================================================

def palindromic_field(N):
    """Trace field for the N-gon palindromic polynomial."""
    if N in [3, 4, 6]:
        return 1, 1, "Q"
    if N in [5, 10, 15, 20]:
        return 5, 2, "Q(sqrt(5))"
    if N in [8, 16]:
        return 2, 2, "Q(sqrt(2))"
    if N == 12:
        return 3, 2, "Q(sqrt(3))"
    if N == 7:
        return 49, 3, "Q(cos(2pi/7))"
    if N == 9:
        return 81, 3, "Q(cos(2pi/9))"
    if N == 11:
        return 14641, 5, "Q(cos(2pi/11))"
    return N, (N - 1) // 2, f"Q(cos(2pi/{N}))"


def wall_crossing_entropy(N):
    """Wall-crossing entropy at the N-th palindromic threshold.

    Even N (self-paired m = N/2): Delta_S = log(2) (1 bit)
    Odd N (paired m, N-m):        Delta_S = 2*log(2) (2 bits)

    Returns (delta_S, is_self_paired, field_name).
    """
    is_self_paired = (N % 2 == 0)
    delta_S = log(2) if is_self_paired else 2 * log(2)
    _, _, field = palindromic_field(N)
    return delta_S, is_self_paired, field


# =====================================================================
# BTZ entropy from CFT
# =====================================================================

def btz_entropy_cardy(c, E=0):
    """Cardy formula: S = 2*pi*sqrt(c*E/6). Zero at threshold."""
    if E > 0:
        return 2 * pi * sqrt(c * E / 6)
    return 0.0


def one_loop_entropy(N):
    """One-loop entropy from the frozen determinant.

    S_1loop = -log(Z_frozen) = log((N-3)!!) - 3(N-2)/4 * log(2)
    """
    m_crit = N // 2
    log_Z = 0.0
    for m in range(1, N):
        if m == m_crit:
            continue
        gap = abs(casimir(m_crit, N) - casimir(m, N))
        if gap > 1e-12:
            log_Z += -0.5 * log(gap)
    return -log_Z


# =====================================================================
# Full entropy accounting
# =====================================================================

def entropy_decomposition(N_min=7, N_max=17):
    """Full entropy decomposition of the palindromic staircase.

    Returns dict with:
      terms: list of (N, S_1loop, S_wc, field, is_self_paired)
      S_wc_total, S_1loop_total, S_total
    """
    terms = []
    S_wc_total = 0.0
    S_1loop_total = 0.0

    for N in range(N_min, N_max + 1):
        S_1loop = one_loop_entropy(N)
        delta_S, is_self_paired, field = wall_crossing_entropy(N)

        S_wc_total += delta_S
        S_1loop_total += S_1loop

        terms.append({
            'N': N,
            'S_1loop': S_1loop,
            'S_wc': delta_S,
            'field': field,
            'is_self_paired': is_self_paired,
            'rho_star': find_threshold(N),
        })

    return {
        'terms': terms,
        'S_wc_total': S_wc_total,
        'S_1loop_total': S_1loop_total,
        'S_total': S_wc_total + S_1loop_total,
        'bits_wc': S_wc_total / log(2),
        'bits_total': (S_wc_total + S_1loop_total) / log(2),
    }


def wall_crossing_table(N_max=12):
    """Wall-crossing table: N, type, Delta_S, field, cumulative bits.

    Returns list of (N, delta_S, is_self_paired, field, cum_bits).
    """
    rows = []
    cum = 0.0
    for N in range(7, N_max + 1):
        delta_S, is_self_paired, field = wall_crossing_entropy(N)
        cum += delta_S
        rows.append((N, delta_S, is_self_paired, field, cum / log(2)))
    return rows
