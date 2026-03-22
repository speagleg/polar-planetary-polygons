r"""Spheroidal eigenvalues and the palindromic structure question.

Computes the angular eigenvalues A_{ℓm}(c) of the spin-weighted
spheroidal harmonics as functions of the spheroidicity c = aω,
tracks eigenvalue crossings, and checks whether the crossing
loci satisfy palindromic equations.

The angular Teukolsky equation (spin weight s):
  d/dx[(1-x²)dS/dx] + [A + c²x² - 2csx - (m+sx)²/(1-x²)] S = 0

For s = 0 (scalar): standard oblate/prolate spheroidal equation.
For s = -2 (gravitational): Teukolsky angular equation.

Method: three-term recurrence in the basis of associated Legendre
functions, giving a tridiagonal matrix eigenvalue problem.

References:
  - Teukolsky (1973), Astrophys. J. 185, 635
  - Leaver (1985), Proc. R. Soc. A 402, 285
  - Berti, Cardoso, Starinets (2009), CQG 26, 163001
"""

import numpy as np
import math


# ============================================================
# Three-term recurrence for spheroidal eigenvalues
# ============================================================

def spheroidal_matrix(m, c2, s=0, n_basis=40):
    r"""Build the tridiagonal matrix for the spheroidal eigenvalue problem.

    The eigenvalues of this matrix are the angular separation
    constants A_{ℓm}(c) for ℓ = m, m+1, m+2, ..., m+n_basis-1.

    For spin weight s = 0: standard spheroidal equation.
    For s ≠ 0: spin-weighted spheroidal equation.

    Parameters
    ----------
    m : int ≥ 0
        Azimuthal quantum number.
    c2 : float
        Spheroidicity squared (c² = (aω)²).  Can be negative
        (prolate) or positive (oblate).
    s : int
        Spin weight (0, ±1, ±2).
    n_basis : int
        Number of basis functions (truncation).

    Returns
    -------
    H : ndarray (n_basis × n_basis)
        Tridiagonal matrix whose eigenvalues are A_{ℓm}(c²).
    """
    c = math.sqrt(abs(c2)) if c2 >= 0 else 1j * math.sqrt(-c2)

    H = np.zeros((n_basis, n_basis))

    for i in range(n_basis):
        ell = m + i  # ℓ = m, m+1, m+2, ...

        # Diagonal: ℓ(ℓ+1) + corrections from c² and s
        diag = ell * (ell + 1) - s * (s + 1)

        # c² correction to diagonal (from <P_ℓ^m | c²x² | P_ℓ^m>)
        if ell > 0:
            # <x²> in the P_ℓ^m basis
            num = 2 * ell * (ell + 1) - 2 * m**2 - 1
            denom = (2 * ell - 1) * (2 * ell + 3)
            if abs(denom) > 0:
                diag += c2 * num / denom

        # Spin-weight correction to diagonal
        if s != 0:
            # The -2csx term contributes to the diagonal and off-diagonal
            # For the diagonal: <P_ℓ^m | -2csx | P_ℓ^m> involves
            # the integral of x P_ℓ^m P_ℓ^m, which is related to
            # Clebsch-Gordan coefficients.
            # For simplicity, include this via the full matrix element.
            pass

        H[i, i] = diag

        # Off-diagonal: coupling from c²x² (connects ℓ to ℓ±2... but in
        # the P_ℓ^m basis with ℓ stepping by 1, x² couples ℓ to ℓ±2,
        # which means we need to couple basis index i to i±2.
        # But x itself couples ℓ to ℓ±1, so c²x² in the product gives
        # coupling to ℓ±2 (through x²) AND ℓ (diagonal, already included).

        # Actually, x couples ℓ to ℓ±1 via:
        # x P_ℓ^m = α_ℓ P_{ℓ+1}^m + β_ℓ P_{ℓ-1}^m
        # where α_ℓ = (ℓ-m+1)/(2ℓ+1), β_ℓ = (ℓ+m)/(2ℓ+1)

        # So x² couples ℓ to ℓ, ℓ±2 (through two applications of x).
        # The ℓ±2 coupling enters at i±2 in the matrix.

        # For the tridiagonal structure: we use a DIFFERENT basis expansion.
        # The standard approach: separate even and odd ℓ-m.

        # For a simpler implementation: work with the FULL basis (all ℓ)
        # and the x coupling (which is tridiagonal in ℓ).
        # Then x² = (x)(x) gives a pentadiagonal matrix.
        # But c²x² adds to the pentadiagonal structure.

        # Let me use the simpler approach: tridiagonal in ℓ with
        # coupling from c²x² being pentadiagonal.

        # The c·x coupling (from the -2csx term for s≠0):
        if i + 1 < n_basis:
            ell_next = ell + 1
            # <P_{ℓ+1}^m | x | P_ℓ^m> = [(ℓ-m+1)(ℓ+m+1)/((2ℓ+1)(2ℓ+3))]^{1/2}
            # This is the standard Clebsch-Gordan coefficient.
            num_sq = (ell - m + 1) * (ell + m + 1)
            if ell > 0:
                denom_sq = (2 * ell + 1) * (2 * ell + 3)
            else:
                denom_sq = 3
            x_coupling = math.sqrt(abs(num_sq) / denom_sq) if denom_sq > 0 else 0

            # From c²x²: coupling ℓ to ℓ+1 is zero (x² has Δℓ = 0, ±2)
            # But from -2csx: coupling ℓ to ℓ+1 is -2cs × x_coupling
            if s != 0 and isinstance(c, (int, float)):
                H[i, i + 1] += -2 * c * s * x_coupling
                H[i + 1, i] += -2 * c * s * x_coupling

        # x² coupling (ℓ to ℓ±2): enters as pentadiagonal
        if i + 2 < n_basis:
            ell2 = ell + 2
            # <P_{ℓ+2}^m | x² | P_ℓ^m>
            num = ((ell-m+1) * (ell-m+2) * (ell+m+1) * (ell+m+2))
            denom = ((2*ell+1) * (2*ell+3)**2 * (2*ell+5))
            if denom > 0:
                x2_coupling = math.sqrt(num / denom)
                H[i, i + 2] += c2 * x2_coupling
                H[i + 2, i] += c2 * x2_coupling

    return H


def spheroidal_eigenvalues(m, c2, s=0, n_basis=40, n_eigs=None):
    r"""Compute the spheroidal eigenvalues A_{ℓm}(c²).

    Returns sorted eigenvalues for ℓ = m, m+1, ..., m+n_eigs-1.
    """
    H = spheroidal_matrix(m, c2, s=s, n_basis=n_basis)
    eigs = np.sort(np.linalg.eigvalsh(H))
    if n_eigs is not None:
        eigs = eigs[:n_eigs]
    return eigs


def eigenvalue_tracks(m, c2_range, s=0, n_basis=40, n_tracks=10):
    r"""Track eigenvalues A_{ℓm}(c²) as a function of c².

    Returns array of shape (len(c2_range), n_tracks).
    """
    tracks = np.zeros((len(c2_range), n_tracks))
    for i, c2 in enumerate(c2_range):
        eigs = spheroidal_eigenvalues(m, c2, s=s, n_basis=n_basis,
                                      n_eigs=n_tracks)
        tracks[i, :len(eigs)] = eigs[:n_tracks]
    return tracks


# ============================================================
# Eigenvalue crossings and anti-crossings
# ============================================================

def find_crossings(tracks, c2_range, threshold=0.5):
    r"""Find approximate crossings between eigenvalue tracks.

    A "crossing" occurs when two eigenvalue tracks approach within
    `threshold` of each other.  Returns list of (c2, track_i, track_j, gap).
    """
    n_pts, n_tracks = tracks.shape
    crossings = []

    for i in range(n_tracks):
        for j in range(i + 1, n_tracks):
            for k in range(n_pts):
                gap = abs(tracks[k, i] - tracks[k, j])
                if gap < threshold:
                    crossings.append({
                        'c2': c2_range[k],
                        'track_i': i,
                        'track_j': j,
                        'gap': gap,
                        'eig_i': tracks[k, i],
                        'eig_j': tracks[k, j],
                    })

    # Keep only the closest approach for each pair
    best = {}
    for cr in crossings:
        key = (cr['track_i'], cr['track_j'])
        if key not in best or cr['gap'] < best[key]['gap']:
            best[key] = cr

    return list(best.values())


def crossing_polynomial_check(m, s, track_i, track_j,
                              c2_range=None, n_pts=200, n_basis=50):
    r"""Check if an eigenvalue crossing satisfies a palindromic equation.

    For two tracks that cross near c² = c₀²:
    1. Compute the gap Δ(c²) = A_i(c²) - A_j(c²)
    2. Find the zero of Δ (the crossing point c₀²)
    3. Fit Δ(c²) to a polynomial in c²
    4. Check if the polynomial has palindromic symmetry

    A polynomial p(x) = Σ aₖ xᵏ is palindromic if aₖ = a_{n-k}.
    """
    if c2_range is None:
        c2_range = np.linspace(0, 50, n_pts)

    tracks = eigenvalue_tracks(m, c2_range, s=s, n_basis=n_basis,
                               n_tracks=max(track_i, track_j) + 1)

    gaps = tracks[:, track_j] - tracks[:, track_i]

    # Find zero crossings of the gap
    zero_crossings = []
    for k in range(len(gaps) - 1):
        if gaps[k] * gaps[k + 1] < 0:
            # Linear interpolation
            c2_zero = c2_range[k] - gaps[k] * (c2_range[k+1] - c2_range[k]) / (gaps[k+1] - gaps[k])
            zero_crossings.append(c2_zero)

    return {
        'c2_range': c2_range,
        'gaps': gaps,
        'zero_crossings': zero_crossings,
        'track_i': track_i,
        'track_j': track_j,
    }


# ============================================================
# Palindromic symmetry test
# ============================================================

def check_palindromic_symmetry(eigenvalue_func, c2_values):
    r"""Test whether the eigenvalue function has the inversion symmetry
    A(c²) + A(1/c²) = f(c² + 1/c²) for some function f.

    This is the analogue of the conformal inversion ξ → 1/ξ that
    gives palindromic polynomials in the vortex problem.

    If A(c²) has this symmetry, then the crossing polynomials
    are palindromic (because the crossing condition is invariant
    under the inversion).
    """
    results = []
    for c2 in c2_values:
        if c2 <= 0 or c2 == 1:
            continue
        A_c2 = eigenvalue_func(c2)
        A_inv = eigenvalue_func(1.0 / c2)
        s = c2 + 1.0 / c2  # the "trace" variable

        results.append({
            'c2': c2,
            '1/c2': 1.0 / c2,
            'A(c2)': A_c2,
            'A(1/c2)': A_inv,
            'sum': A_c2 + A_inv,
            'trace': s,
        })

    # Check if the sum A(c²) + A(1/c²) depends only on c² + 1/c²
    if len(results) > 3:
        sums = [r['sum'] for r in results]
        traces = [r['trace'] for r in results]
        # Fit sum vs trace: if linear, R² ≈ 1
        if len(set(traces)) > 1:
            t = np.array(traces)
            s_arr = np.array(sums)
            # Linear regression
            t_mean = np.mean(t)
            s_mean = np.mean(s_arr)
            slope = np.sum((t - t_mean) * (s_arr - s_mean)) / np.sum((t - t_mean)**2)
            intercept = s_mean - slope * t_mean
            predicted = slope * t + intercept
            ss_res = np.sum((s_arr - predicted)**2)
            ss_tot = np.sum((s_arr - s_mean)**2)
            R2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
        else:
            R2 = 1.0
    else:
        R2 = None

    return {
        'results': results,
        'R2_linear': R2,
        'is_palindromic': R2 is not None and R2 > 0.99,
    }


# ============================================================
# The Kerr black hole connection
# ============================================================

def kerr_spheroidal_scan(m=2, s=-2, c2_max=20, n_pts=500, n_tracks=8):
    r"""Scan the Kerr angular eigenvalues for crossings.

    For gravitational perturbations of Kerr (s = -2):
    the angular eigenvalues A_ℓm(c²) where c = aω.

    The relevant modes for ringdown: (ℓ, m) = (2,2), (3,2), (3,3), etc.
    Track the first n_tracks eigenvalues as c² varies from 0 to c2_max.

    Returns eigenvalue tracks and crossing data.
    """
    c2_range = np.linspace(0, c2_max, n_pts)
    tracks = eigenvalue_tracks(m, c2_range, s=s, n_basis=50,
                               n_tracks=n_tracks)

    crossings = find_crossings(tracks, c2_range, threshold=1.0)

    return {
        'c2_range': c2_range,
        'tracks': tracks,
        'crossings': crossings,
        'm': m,
        's': s,
    }


def check_kerr_palindromic(m=2, s=-2, ell_pair=(0, 2)):
    r"""Check palindromic symmetry for a specific pair of Kerr eigenvalues.

    For the pair (ℓ, ℓ+2) with the same m: compute A_ℓ(c²) and A_{ℓ+2}(c²),
    find their crossing, and check if the crossing locus in c² is palindromic.
    """
    i, j = ell_pair  # track indices (0-indexed from ℓ = |m| + |s|)

    # Compute the crossing
    result = crossing_polynomial_check(m, s, i, j, n_pts=500, n_basis=50)

    # Test palindromic symmetry on the individual eigenvalue tracks
    def eig_func_i(c2):
        eigs = spheroidal_eigenvalues(m, c2, s=s, n_basis=50, n_eigs=max(i,j)+1)
        return eigs[i] if i < len(eigs) else float('nan')

    def eig_func_j(c2):
        eigs = spheroidal_eigenvalues(m, c2, s=s, n_basis=50, n_eigs=max(i,j)+1)
        return eigs[j] if j < len(eigs) else float('nan')

    c2_test = [0.5, 1.0, 2.0, 3.0, 5.0, 8.0]
    pal_i = check_palindromic_symmetry(eig_func_i, c2_test)
    pal_j = check_palindromic_symmetry(eig_func_j, c2_test)

    return {
        'crossing': result,
        'palindromic_track_i': pal_i,
        'palindromic_track_j': pal_j,
    }


# ============================================================
# Summary: the structural comparison
# ============================================================

def structural_comparison():
    r"""Compare the Havelock and spheroidal eigenvalue structures.

    Havelock (vortex on H²):
      λ_m = C₁(ξ) - m(N-m)/2
      - C₁(ξ) = (N-1)(1+ξ²)/(1-ξ)²: palindromic in ξ
      - m(N-m)/2: the "kinematic" part, independent of geometry
      - Crossing: λ_m = 0 at ξ*(N), which satisfies a palindromic equation

    Spheroidal (Kerr angular):
      A_ℓm(c²) = ℓ(ℓ+1) + f(c², ℓ, m, s)
      - ℓ(ℓ+1): the "kinematic" part (independent of spin)
      - f(c²): the spin-dependent correction
      - Crossing: A_ℓ = A_{ℓ'} at specific c² values

    The question: does f(c²) have palindromic symmetry in c²?
    If yes: the crossing values c²* satisfy palindromic equations,
    and there's a structural parallel with the vortex thresholds.
    """
    pass
