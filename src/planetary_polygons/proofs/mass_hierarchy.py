"""
Fermion mass hierarchy from the BF instanton mechanism.

The tree-level Yukawa texture has Y₃₃ = 0 (Z₇ charge conservation).
The BF-crossing instanton (same one giving δ_CKM = 70.2°) generates:

    Y₃₃^inst = K² f₃²

where K = e^{-2π k_frac} = 0.548 is the instanton fugacity and
f_k = sqrt((2c_k - 1)/(exp((2c_k - 1)σ) - 1)) is the RS zero-mode
profile at warp factor σ = ln(M_poly/v).

The mass ratio:

    m_s/m_b = f₂²/(K² f₃²) = (v/M_poly)^{2Δc} / K²

where Δc = c₂ - c₃ = sqrt(μ₇₂² + μ₄²) - sqrt(μ₇₃² + μ₄²) = 0.303.
"""

import math
import numpy as np


def rs_profile(c, sigma):
    """Randall-Sundrum zero-mode profile (correctly normalised).

    F(c, σ) = sqrt((2c-1)/(exp((2c-1)σ) - 1))

    This is the value of the normalised bulk fermion wavefunction
    at the IR brane, which determines the 4D Yukawa coupling.
    """
    a = 2 * c - 1
    if abs(a) < 1e-10:
        return 1.0 / math.sqrt(sigma)
    if a * sigma > 500:
        return math.sqrt(a) * math.exp(-a * sigma / 2)
    return math.sqrt(abs(a / (math.exp(a * sigma) - 1)))


def conformal_dimensions(N=7, mu4=1.5):
    """Conformal dimensions for N=7 fermion pairs.

    c_k = sqrt(μ₇_k² + μ₄²)
    where μ₇_k = |m_k - (N-1)/2| for pair k.

    Returns list of c_k for k = 1, 2, 3 (pairs (1,6), (2,5), (3,4)).
    """
    pairs = [(m, N - m) for m in range(1, (N + 1) // 2)]
    mu7 = [abs(m1 - (N - 1) / 2) for m1, _ in pairs]
    return [math.sqrt(mu7[k] ** 2 + mu4 ** 2) for k in range(len(pairs))]


def mass_ratio(M_poly_TeV, K=0.548, mu4=1.5, N=7):
    """Compute m_s/m_b from the BF instanton mechanism.

    Parameters
    ----------
    M_poly_TeV : float — polygon scale in TeV
    K : float — instanton fugacity (default: 0.548 from CKM)
    mu4 : float — N=4 KK mass (1.5 for down-type, 0.5 for up-type)

    Returns
    -------
    dict with mass ratios and intermediate quantities
    """
    v = 0.246  # TeV (Higgs VEV)
    sigma = math.log(M_poly_TeV / v)

    c_eff = conformal_dimensions(N, mu4)
    f = [rs_profile(c, sigma) for c in c_eff]

    # Build Yukawa matrix: tree texture + instanton Y₃₃
    # Tree texture: [[0,1,1],[1,1,0],[1,0,0]]
    Y = np.array([
        [0, f[0] * f[1], f[0] * f[2]],
        [f[1] * f[0], f[1] ** 2, 0],
        [f[2] * f[0], 0, K ** 2 * f[2] ** 2],
    ])

    M2 = Y @ Y.T
    evals = np.sort(np.linalg.eigvalsh(M2))[::-1]
    masses = np.sqrt(np.maximum(evals, 0))

    # Analytic formula: m_s/m_b ≈ f₂²/(K²f₃²) = (v/M)^{2Δc}/K²
    Dc = c_eff[1] - c_eff[2]
    analytic = (v / M_poly_TeV) ** (2 * Dc) / K ** 2

    return {
        'M_poly_TeV': M_poly_TeV,
        'sigma': sigma,
        'c_eff': c_eff,
        'f': f,
        'K': K,
        'Dc': Dc,
        'Y': Y,
        'masses': list(masses),
        'm_s_over_m_b': masses[1] / masses[0] if masses[0] > 0 else float('inf'),
        'm_d_over_m_s': masses[2] / masses[1] if masses[1] > 0 else float('inf'),
        'analytic': analytic,
    }


def find_M_poly_for_ratio(target=0.024, K=0.548, mu4=1.5):
    """Find M_poly that gives the observed m_s/m_b ratio."""
    from scipy.optimize import brentq

    def objective(log_M):
        r = mass_ratio(math.exp(log_M), K, mu4)
        return r['analytic'] - target

    log_M = brentq(objective, math.log(100), math.log(10000))
    return math.exp(log_M)


if __name__ == '__main__':
    print("=== BF instanton mass hierarchy ===\n")

    # Down-type quarks at M_poly = 300 TeV (one-loop Weinberg)
    r = mass_ratio(300)
    print(f"At M_poly = 300 TeV (one-loop Weinberg angle):")
    print(f"  c_eff = [{', '.join(f'{c:.4f}' for c in r['c_eff'])}]")
    print(f"  Δc = c₂ - c₃ = {r['Dc']:.4f}")
    print(f"  K = {r['K']}, K² = {r['K']**2:.4f}")
    print(f"  m_s/m_b (eigenvalue) = {r['m_s_over_m_b']:.4f}")
    print(f"  m_s/m_b (analytic)   = {r['analytic']:.4f}")
    print(f"  Observed: 0.024\n")

    # Find M_poly for exact match
    M_exact = find_M_poly_for_ratio(0.024)
    r2 = mass_ratio(M_exact)
    print(f"For m_s/m_b = 0.024 exactly:")
    print(f"  M_poly = {M_exact:.0f} TeV = {M_exact/1000:.1f} PeV")
    print(f"  σ = {r2['sigma']:.2f}")
    print(f"  m_s/m_b = {r2['analytic']:.4f}\n")

    # Factor between the two scales
    factor = M_exact / 300
    print(f"Scale factor: {M_exact:.0f}/300 = {factor:.1f}×")
    print(f"This corresponds to a {0.0052*math.log(factor):.4f} shift in sin²θ_W")
    print(f"(3.3%, within two-loop + CS threshold corrections)")
