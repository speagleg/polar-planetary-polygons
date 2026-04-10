"""PMNS neutrino mixing from the Z_7 pair structure.

The three PMNS mixing angles are conjectured to be simple algebraic
functions of N = 7 alone (Conjecture, Paper IV §pmns):

  sin²(2θ₁₂) = (N-1)/N = 6/7           → θ₁₂ = 33.9°
  sin²(θ₂₃)  = (N+1)/(2N) = 4/7        → θ₂₃ = 49.1°
  sin²(θ₁₃)  = 1/(N²-1) = 1/48         → θ₁₃ = 8.3°
  δ_CP        = arctan(√N) = 69.3°      (same Gauss sum as CKM)

Derivation status:
  - θ₂₃ = π/4 PROVED from pair cosine DFT (character orthogonality)
  - The shift from 45° → 49° comes from Klein quartic modular forms
    at the CM point τ₀ = (1+i√7)/2 (numerically verified)
  - The exact Z_7 fraction formulas are CONJECTURED (0.1σ, 0.6σ, 1.6σ)
  - Complete group-theoretic derivation remains OPEN

Key identity: cos(2θ₂₃) = -1/N.
"""

from math import pi, sqrt, atan, asin, sin, cos, degrees

from planetary_polygons.extensions.bernoulli_havelock import N_CRIT


def pmns_z7_fractions(N=N_CRIT):
    """Z_7 fraction predictions for PMNS mixing angles.

    These are parameter-free predictions from N alone.
    Status: CONJECTURED (match PDG to < 2σ).
    """
    s12_sq = (1 - 1 / sqrt(N)) / 2
    s23_sq = (N + 1) / (2 * N)
    s13_sq = 1 / (N ** 2 - 1)
    delta = atan(sqrt(N))

    theta_12 = asin(sqrt(s12_sq))
    theta_23 = asin(sqrt(s23_sq))
    theta_13 = asin(sqrt(s13_sq))

    return {
        'sin2_2theta12': (N - 1) / N,
        'sin2_theta23': s23_sq,
        'sin2_theta13': s13_sq,
        'cos_2theta23': -1 / N,
        'theta_12_rad': theta_12,
        'theta_12_deg': degrees(theta_12),
        'theta_23_rad': theta_23,
        'theta_23_deg': degrees(theta_23),
        'theta_13_rad': theta_13,
        'theta_13_deg': degrees(theta_13),
        'delta_CP_rad': delta,
        'delta_CP_deg': degrees(delta),
    }


def maximal_atmospheric_mixing():
    """Pair cosine DFT gives θ₂₃ = π/4 exactly.

    PROVED: by character orthogonality,
    Σ_k cos²(2πk·2/N) = Σ_k cos²(2πk·3/N) = (N-2)/4
    for k = 1,...,(N-1)/2 and any odd N.
    The pair modes m=2 and m=3 have identical column norms
    in the pair cosine matrix, giving maximal 2-3 mixing
    at leading order.
    """
    N = N_CRIT
    # Verify character orthogonality
    pairs = (N - 1) // 2
    sum_cos2_m2 = sum(cos(2 * pi * k * 2 / N) ** 2 for k in range(1, pairs + 1))
    sum_cos2_m3 = sum(cos(2 * pi * k * 3 / N) ** 2 for k in range(1, pairs + 1))
    expected = (N - 2) / 4

    return {
        'theta_23': pi / 4,
        'theta_23_deg': 45.0,
        'sum_cos2_m2': sum_cos2_m2,
        'sum_cos2_m3': sum_cos2_m3,
        'expected': expected,
        'proved': abs(sum_cos2_m2 - sum_cos2_m3) < 1e-12,
    }


def complementarity_identity():
    """Verify arctan(1/2) + arctan(1/3) = π/4.

    This identity connects the CKM (index-3 subgroup QR)
    and PMNS (index-2 subgroup, pairs) mixing scales.
    """
    return abs(atan(0.5) + atan(1.0 / 3) - pi / 4) < 1e-14


def reactor_angle(s12_ckm):
    """sin²(θ₁₃^PMNS) from the Z_7 fraction formula.

    The conjectured formula sin²(θ₁₃) = 1/(N²-1) = 1/48
    gives θ₁₃ = 8.3° (PDG: 8.54 ± 0.15°, 1.6σ).
    """
    N = N_CRIT
    return 1 / (N ** 2 - 1)


def pmns_angles(s12_ckm=None, sigma=None):
    """PMNS predictions from the Z_7 backbone.

    Uses the Z_7 fraction conjectures (parameter-free).
    The s12_ckm and sigma arguments are accepted for
    backward compatibility but ignored.
    """
    return pmns_z7_fractions()
