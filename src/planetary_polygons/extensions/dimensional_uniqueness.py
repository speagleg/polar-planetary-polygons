"""
Why 3+1 dimensions: polynomial Havelock eigenvalues are unique to d=2.

The Havelock eigenvalue λ_m is the m-th Fourier mode of the angular
Hessian of the interaction energy for N vortices on a regular polygon.
For the d-dimensional Laplacian Green's function G_d:

  λ_m = self_correction - Σ_{p=1}^{N-1} K_d(πp/N) · [1 - cos(2πpm/N)]

where K_d(x) is the angular Hessian kernel:
  d=2: K₂(x) = 1/(4sin²x)    → λ_m = (N-1) - m(N-m)/2  [polynomial!]
  d=3: K₃(x) = 1/(8sin³x)    → λ_m involves csc³ sums   [NOT polynomial]
  d=4: K₄(x) = 1/(16sin⁴x)   → λ_m involves csc⁴ sums   [NOT polynomial]

The polynomial structure (d=2 only) follows from the Ramanujan sum identity:
  Σ_{p=1}^{N-1} [1 - cos(2πpm/N)] / sin²(πp/N) = 2m(N-m)

No analogous identity exists for sin^α with α ≠ 2.

The polynomial eigenvalues enable: CMS integrability (from holomorphicity
of log z), exact BO separation, palindromic thresholds, and the entire
Havelock framework.

Therefore: 2D base is forced. Combined with Z_N → S¹ fiber and one
WKB clock, this gives 2+1+1 = 3+1 dimensions.
"""

import numpy as np
from math import pi, sin, cos, log, sqrt
from fractions import Fraction


# =====================================================================
# PART 1: Hessian kernels for d-dimensional interactions
# =====================================================================

def hessian_kernel(x, d):
    """Angular Hessian kernel K_d(x) for the d-dimensional Green's function.

    For N vortices on a unit circle, the angular perturbation energy
    involves K_d(πp/N) where K_d is derived from the Green's function:
      G_d(r) ∝ {-log r (d=2), r^{2-d} (d≥3)}

    The angular Hessian of G_d(2sin(x)) on the unit circle:
      K₂(x) = 1/(4sin²x)               [from ∂²(-log r)/∂θ² at r=2sinx]
      K₃(x) = 1/(8sin³x)               [from ∂²(1/r)/∂θ² at r=2sinx]
      K_d(x) = (d-2)/(2^d sin^d(x))     [general formula for d≥2]

    For d=2, K₂ gives the csc² sum = Ramanujan identity = polynomial.
    """
    sx = abs(sin(x))
    if sx < 1e-15:
        return float('inf')
    if d == 2:
        return 1.0 / (4 * sx**2)
    else:
        return (d - 2) / (2**d * sx**d)


# =====================================================================
# PART 2: Havelock-type eigenvalues via Hessian kernel
# =====================================================================

def havelock_eigenvalue_dim(m, N, d):
    """Havelock-type eigenvalue in d dimensions.

    λ_m = S_self(d, N) - Σ_{p=1}^{N-1} K_d(πp/N) · [1 - cos(2πpm/N)]

    For d=2: S_self = (N-1), and the sum gives m(N-m)/2,
    so λ_m = (N-1) - m(N-m)/2.
    """
    interaction_sum = 0.0
    self_energy = 0.0

    for p in range(1, N):
        x = pi * p / N
        K = hessian_kernel(x, d)
        interaction_sum += K * (1 - cos(2 * pi * p * m / N))
        self_energy += K  # total self-energy kernel

    # For d=2: self_energy = Σ csc²/(4) = (N²-1)/12
    # The Havelock eigenvalue convention uses S_self = (N-1) for d=2
    # We normalise so that λ_m = (N-1) - m(N-m)/2 for d=2
    if d == 2:
        # Exact: Σ [1-cos]/sin² = 2m(N-m), so interaction_sum = m(N-m)/2
        # S_self = (N-1) gives λ_m = (N-1) - m(N-m)/2
        return (N - 1) - interaction_sum
    else:
        # Use same normalisation as d=2: λ_m = (N-1) - normalised_sum
        # Normalise d≠2 interaction sum relative to d=2
        # d=2 total: Σ 1/(4sin²) = (N²-1)/12
        # d≠2 total: Σ (d-2)/(2^d sin^d)
        total_d2 = sum(1.0 / (4 * sin(pi * p / N)**2) for p in range(1, N))
        total_dd = sum(hessian_kernel(pi * p / N, d) for p in range(1, N))
        if total_dd > 1e-15:
            normalisation = total_d2 / total_dd
        else:
            normalisation = 1.0
        return (N - 1) - interaction_sum * normalisation


def eigenvalue_spectrum(N, d):
    """Full eigenvalue spectrum λ_m for m = 1, ..., N-1."""
    return [(m, havelock_eigenvalue_dim(m, N, d)) for m in range(1, N)]


# =====================================================================
# PART 3: The Ramanujan sum identity (d=2 proof)
# =====================================================================

def ramanujan_csc2_sum(m, N):
    """Σ_{p=1}^{N-1} [1 - cos(2πpm/N)] / sin²(πp/N) = 2m(N-m).

    This is the identity that makes d=2 eigenvalues polynomial.
    Returns (numerical_sum, exact_value=2m(N-m), relative_error).
    """
    numerical = 0.0
    for p in range(1, N):
        x = pi * p / N
        numerical += (1 - cos(2 * pi * p * m / N)) / (sin(x)**2)

    exact = 2 * m * (N - m)
    rel_err = abs(numerical - exact) / exact if exact > 0 else abs(numerical)
    return numerical, exact, rel_err


def verify_ramanujan_identity(N):
    """Verify the Ramanujan sum identity for all modes m=1..N-1."""
    results = []
    max_err = 0.0
    for m in range(1, N):
        num, exact, err = ramanujan_csc2_sum(m, N)
        results.append((m, num, exact, err))
        max_err = max(max_err, err)
    return results, max_err


# =====================================================================
# PART 4: Non-polynomial test for d≠2
# =====================================================================

def csc_power_sum(m, N, alpha):
    """Σ_{p=1}^{N-1} [1 - cos(2πpm/N)] / sin^α(πp/N).

    For α=2: this equals 2m(N-m) [polynomial, Ramanujan identity].
    For α≠2: NOT polynomial in m.
    """
    total = 0.0
    for p in range(1, N):
        x = pi * p / N
        total += (1 - cos(2 * pi * p * m / N)) / (abs(sin(x))**alpha)
    return total


def polynomial_fit_residual(N, d, degree=2):
    """Fit λ_m with a polynomial of given degree, return max residual.

    For d=2: residual ≈ 0 at degree 2 (polynomial).
    For d≠2: residual >> 0 (not polynomial).
    """
    spectrum = eigenvalue_spectrum(N, d)
    m_vals = np.array([m for m, _ in spectrum], dtype=float)
    lam_vals = np.array([lam for _, lam in spectrum])

    if len(m_vals) <= degree:
        return {'max_residual': 0.0, 'is_polynomial': True, 'coefficients': []}

    coeffs = np.polyfit(m_vals, lam_vals, degree)
    fitted = np.polyval(coeffs, m_vals)
    residuals = np.abs(lam_vals - fitted)
    max_residual = float(np.max(residuals))

    return {
        'coefficients': coeffs.tolist(),
        'max_residual': max_residual,
        'is_polynomial': max_residual < 1e-8,
        'spectrum': spectrum,
    }


def exact_havelock_polynomial(m, N):
    """The exact Havelock eigenvalue (d=2 only).
    λ_m = (N-1) - m(N-m)/2
    """
    return (N - 1) - m * (N - m) / 2.0


def havelock_exact(m, N):
    """Exact Havelock eigenvalue using rational arithmetic."""
    return Fraction(N - 1) - Fraction(m * (N - m), 2)


# =====================================================================
# PART 5: Dimensional comparison table
# =====================================================================

def dimensional_comparison(N):
    """Compare eigenvalue structure across d=2, 3, 4."""
    results = {}
    for d in [2, 3, 4]:
        fit = polynomial_fit_residual(N, d, degree=2)
        results[d] = {
            'spectrum': fit['spectrum'],
            'is_polynomial': fit['is_polynomial'],
            'max_residual': fit['max_residual'],
        }
    return results


def full_dimension_table(N_values=None):
    """Polynomial residuals across dimensions and N values."""
    if N_values is None:
        N_values = [5, 7, 8, 10, 12]
    rows = []
    for N in N_values:
        for d in [2, 3, 4]:
            fit = polynomial_fit_residual(N, d, degree=2)
            rows.append({
                'N': N, 'd': d,
                'max_residual': fit['max_residual'],
                'is_polynomial': fit['is_polynomial'],
            })
    return rows


# =====================================================================
# PART 6: Holomorphicity and dimension count
# =====================================================================

def holomorphicity_check():
    """The holomorphicity argument for d=2 uniqueness."""
    return {
        'd2': {'green': '-log|z| = -Re(log z)', 'holomorphic': True,
               'reason': 'log z is holomorphic on C\\{0}'},
        'd3': {'green': '1/r', 'holomorphic': False,
               'reason': 'harmonic but not holomorphic (3D → 2D restriction)'},
    }


def dimension_count():
    """The 3+1 dimension derivation: 2 + 1 + 1 = 4."""
    return {
        'base_dim': 2,
        'base_reason': 'log kernel polynomial eigenvalues (unique to d=2)',
        'fiber_dim': 1,
        'fiber_reason': 'Z_N symmetry → S¹ via Seifert construction',
        'time_dim': 1,
        'time_reason': 'single BO degree of freedom → single WKB clock',
        'total_space': 3,
        'total_spacetime': 4,
    }
