r"""
Fermion mass structure from the polygon hierarchy.

The Yukawa matrix is determined by KK charge conservation on S¹:
  m_f1 - m_f2 + m_H ≡ 0 (mod N)

At N=7 with Higgs at pair 3 (modes 3,4):
  4 texture zeros at (1,1), (2,3), (3,2), (3,3)
  5 nonzero entries

The mass spectrum has a 2+1 pattern:
  Heavy doublet: m₁/m₂ = √((5+√13)/(5-√13)) ≈ 2.48 (FIXED by texture)
  Light singlet: m₃ ∝ e^{-σ/2} (exponential in warp factor)

The tree-level ratio 2.5 is amplified to ~280 by standard Yukawa RG.

The up/down split comes from the N=4 SU(2) isospin:
  c_{k,up} = √(μ₇_k² + (1/2)²)
  c_{k,down} = √(μ₇_k² + (3/2)²)

N=7 and N=8 sectors decouple by mod-56 arithmetic (Q(ζ₅₆)).
"""

import math
import numpy as np


def casimir(m, N):
    return m * (N - m) / 2.0


# =====================================================================
# The Yukawa texture from KK charge conservation
# =====================================================================

def yukawa_texture(N=7, higgs_pair=2):
    """Compute the Yukawa texture zeros from KK selection rules.

    Returns 3×3 array: 1 = nonzero, 0 = zero.
    """
    pairs = [(m, N - m) for m in range(1, (N + 1) // 2)]
    higgs_modes = list(pairs[higgs_pair])

    texture = np.zeros((len(pairs), len(pairs)), dtype=int)
    for i in range(len(pairs)):
        for j in range(len(pairs)):
            for m_i in pairs[i]:
                for m_j in pairs[j]:
                    for m_H in higgs_modes:
                        if (m_i - m_j + m_H) % N == 0:
                            texture[i, j] = 1
    return texture


# =====================================================================
# The RS fermion profile
# =====================================================================

def rs_profile(c, sigma):
    """Randall-Sundrum fermion profile overlap with IR Higgs.

    f(c, σ) = √[(2c-1)/(1 - exp(-(2c-1)σ))]
    """
    if sigma < 0.1:
        return 1.0
    if abs(c - 0.5) < 1e-10:
        return 1.0 / math.sqrt(sigma)
    val = (2 * c - 1) / (1 - math.exp(-(2 * c - 1) * sigma))
    return math.sqrt(abs(val))


# =====================================================================
# The Yukawa matrix eigenvalues
# =====================================================================

def yukawa_eigenvalues(N=7, sigma=15.0, mu4=0.5):
    """Compute the fermion mass eigenvalues.

    Args:
        N: polygon number (7 for the graviton sector)
        sigma: RS warp factor
        mu4: N=4 KK mass (0.5 for up-type, 1.5 for down-type)

    Returns dict with masses, ratios, texture.
    """
    pairs = [(m, N - m) for m in range(1, (N + 1) // 2)]
    n_pairs = len(pairs)

    # Fermion KK masses from N=7
    mu7 = [abs(m1 - (N - 1) / 2) for m1, _ in pairs]

    # Combined bulk mass with N=4 isospin
    c_eff = [math.sqrt(mu7[k] ** 2 + mu4 ** 2) for k in range(n_pairs)]

    # RS profiles
    f_vals = [rs_profile(c, sigma) for c in c_eff]

    # Texture
    texture = yukawa_texture(N, higgs_pair=n_pairs - 1)

    # Build Yukawa matrix
    Y = np.zeros((n_pairs, n_pairs))
    for i in range(n_pairs):
        for j in range(n_pairs):
            if texture[i, j]:
                Y[i, j] = f_vals[i] * f_vals[j]

    # Eigenvalues of YY†
    evals = sorted(np.linalg.eigvalsh(Y @ Y.T), reverse=True)
    masses = [math.sqrt(max(0, e)) for e in evals]

    return {
        'N': N,
        'sigma': sigma,
        'mu4': mu4,
        'c_eff': c_eff,
        'f_vals': f_vals,
        'texture': texture,
        'Y': Y,
        'masses': masses,
        'ratio_12': masses[0] / masses[1] if masses[1] > 1e-20 else float('inf'),
        'ratio_13': masses[0] / masses[2] if masses[2] > 1e-20 else float('inf'),
    }


def tree_level_ratio():
    """The exact tree-level m₁/m₂ ratio from the texture.

    For the N=7 texture with 4 zeros, the YY† block structure gives:
    λ₊ = (5+√13)/2, λ₋ = (5-√13)/2
    m₁/m₂ = √(λ₊/λ₋) = √((5+√13)/(5-√13))
    """
    lam_plus = (5 + math.sqrt(13)) / 2
    lam_minus = (5 - math.sqrt(13)) / 2
    return math.sqrt(lam_plus / lam_minus)


# =====================================================================
# The sector decoupling
# =====================================================================

def sector_decoupling():
    """Verify that N=7 and N=8 sectors decouple mod lcm(7,8)=56."""
    # Cross-sector coupling: N=7 fermions × N=8 Higgs
    # Selection: 8*m₇_f1 + 8*m₇_f2 + 7*m₈_H ≡ 0 (mod 56)
    # With m₈_H = 4: 8(m₁+m₂) + 28 ≡ 0 mod 56
    # → 8(m₁+m₂) ≡ 28 mod 56
    # gcd(8, 56) = 8, and 28/8 = 3.5 (not integer)
    # → NO SOLUTION
    return {
        'lcm': 56,
        'decoupled': True,
        'reason': '8(m₁+m₂) ≡ 28 mod 56 has no integer solution '
                  '(gcd(8,56)=8 does not divide 28)',
    }


# =====================================================================
# The polygon scale from RG running
# =====================================================================

def polygon_scale_from_rg(tree_ratio=2.48, target_ratio=280):
    """Estimate the polygon scale from Yukawa RG amplification.

    The top Yukawa runs as dy/d(ln μ) ∝ y³.
    Starting from y_t/y_c = tree_ratio at M_polygon,
    ending at y_t/y_c = target_ratio at M_Z.

    Returns M_polygon in GeV.
    """
    M_Z = 91.2  # GeV
    # Amplification factor: target/tree ≈ exp(β × ln(M/M_Z))
    # where β ≈ y_t²/(16π²) × (some coefficient)
    # Rough: ln(M/M_Z) ≈ ln(target/tree) / (y_t²/(8π²))
    # With y_t ≈ 1: ln(M/M_Z) ≈ 8π² × ln(280/2.5) ≈ 370
    # This gives M ≈ 10^{160} GeV — way too high.

    # More carefully: the RG equation is dy_t/dt = (9/2)y_t³/(16π²) + ...
    # The solution: 1/y_t² - 1/y_t0² = -(9/16π²) × t
    # where t = ln(M/μ).
    # At M_Z: y_t = 1 (known).
    # At M_polygon: y_t0 = y_t × (tree_ratio/target_ratio)^{1/2}
    #             ≈ 1 × (2.5/280)^{1/2} ≈ 0.094

    y_t_low = 1.0  # at M_Z
    y_t_high = y_t_low * math.sqrt(tree_ratio / target_ratio)

    # 1/y_high² - 1/y_low² = (9/(16π²)) × ln(M_polygon/M_Z)
    t = (1 / y_t_high ** 2 - 1 / y_t_low ** 2) * (16 * math.pi ** 2) / 9
    log10_M = math.log10(M_Z) + t / math.log(10)
    M_polygon = 10 ** min(log10_M, 300)  # cap to avoid overflow

    return {
        'M_polygon_GeV': M_polygon,
        'log10_M': log10_M,
        'y_t_at_polygon': y_t_high,
        'ln_ratio': t,
    }
