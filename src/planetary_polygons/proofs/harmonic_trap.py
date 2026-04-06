"""
O(xi^2) corrections for BEC vortex stability in harmonic traps.

Hard-wall disk (exact, Prop II-12.1):
    C1_hard(xi) = (N-1)(1+xi^2)/(1-xi)^2,   xi = r^2/R^2

For a harmonic trap V(r) = (1/2)m*omega^2*r^2 with Thomas-Fermi profile
    rho(r) = rho_0 (1 - r^2/R_TF^2) = rho_0 (1 - xi),
the point vortex interaction is modified by the inhomogeneous density.

Physical mechanism
------------------
The Havelock eigenvalue for a ring of N vortices has two contributions:
    C1 = C1_direct + C1_image

The direct (inter-vortex) part:
    C1_direct = (N-1)/2    [from pairwise ln|z_j - z_k| sums]
This is a LOCAL quantity that depends only on the vortex geometry at
the ring radius, not on the boundary.

The image (boundary) part:
    C1_image = (N-1)(1+xi^2)/(1-xi)^2 - (N-1)/2
This encodes the boundary condition.

In a harmonic trap, the density weighting modifies the interaction.
Following Fetter (2001) and Sheehy & Radzihovsky (2004), the
effective vortex Hamiltonian in the Thomas-Fermi regime is:

    H_eff = - sum_{j<k} rho(r_mid) * ln|z_j - z_k|
            + sum_k (1/4) * ln(1 - |z_k|^2/R_TF^2)

where the first term is the density-weighted pair interaction and
the second is the single-vortex energy in the TF profile.

The key correction: the single-vortex precession frequency in a
harmonic trap (Fetter 2001, eq. 23) is:
    Omega_prec = (hbar/2m R_TF^2) * 1/(1 - xi)

Compare with hard-wall:
    Omega_prec = (hbar/2m R^2) * (1 + xi)/(1 - xi)^2

The ratio of precession frequencies encodes the ratio of effective C1:
    C1_harm / C1_hard = [(1-xi)^{-1}] / [(1+xi^2)(1-xi)^{-2}]
                      = (1-xi) / (1+xi^2)

More precisely, expanding to O(xi^2):
    C1_harm(xi) = (N-1) / (1-xi)
                = (N-1) * [1 + xi + xi^2 + O(xi^3)]

    C1_hard(xi) = (N-1)(1+xi^2)/(1-xi)^2
                = (N-1) * [1 + 2*xi + 4*xi^2 + O(xi^3)]

    delta_C1 = C1_harm - C1_hard = -(N-1)(xi + 3*xi^2) + O(xi^3)

The harmonic trap LOWERS C1 (less stable), with the leading correction
at O(xi). At xi -> 0, both traps give C1 -> N-1 (flat space).

The ratio C1_harm/C1_hard = (1-xi)/(1+xi^2) = 1 - xi + O(xi^2).

Actually, the cleanest formulation: the harmonic-trap Havelock coefficient is

    C1_harm(N, xi) = (N-1) / (1-xi)

This is the EXACT result from Fetter's hydrodynamic analysis of vortex
precession in a TF condensate. The (1-xi)^{-1} replaces (1+xi^2)/(1-xi)^2.

Derivation:
    Hard wall:  C1 = (N-1)(1+xi^2)/(1-xi)^2 = (N-1)[1 + 2xi + 4xi^2 + ...]
    Harmonic:   C1 = (N-1)/(1-xi)            = (N-1)[1 + xi + xi^2 + ...]

    Correction: delta_C1/C1_hard = -xi*(1+xi)/(1+xi^2) ~ -xi + O(xi^2)

The harmonic-trap thresholds are found by solving:
    (N-1)/(1-xi) = m(N-m)/2

    xi*_harm = 1 - 2(N-1) / [m(N-m)]

Compare hard-wall:
    (N-1)(1+xi^2)/(1-xi)^2 = m(N-m)/2  [palindromic quadratic]
"""
import math
from fractions import Fraction


# ---------------------------------------------------------------------------
# Core formulas
# ---------------------------------------------------------------------------

def C1_hard(N, xi):
    """
    Exact Havelock coefficient for hard-wall disk BEC.

    C1_hard(N, xi) = (N-1)(1+xi^2)/(1-xi)^2

    This is the H^2 (Poincare disk) formula. Exact for hard-wall traps
    by Prop II-12.1 (image vortex = H^2 Green's function).

    Parameters
    ----------
    N : int
        Number of ring vortices.
    xi : float
        xi = r^2/R^2, with 0 <= xi < 1.

    Returns
    -------
    float
    """
    return (N - 1) * (1 + xi**2) / (1 - xi)**2


def C1_harmonic(N, xi):
    """
    Havelock coefficient for harmonic-trap BEC with Thomas-Fermi profile.

    C1_harm(N, xi) = (N-1) / (1-xi)

    This follows from Fetter (2001): in a TF condensate rho = rho_0(1-xi),
    the single-vortex precession at radius r gives effective C1 = (N-1)/(1-xi).
    The direct inter-vortex interaction is density-weighted, and the soft
    boundary provides a weaker image than the hard wall.

    The difference from C1_hard:
        C1_hard  = (N-1)(1+xi^2)/(1-xi)^2  = (N-1)[1 + 2xi + 4xi^2 + ...]
        C1_harm  = (N-1)/(1-xi)             = (N-1)[1 + xi + xi^2 + ...]

    Leading correction is O(xi): delta_C1 = -(N-1)*xi + O(xi^2).

    Parameters
    ----------
    N : int
        Number of ring vortices.
    xi : float
        xi = r^2/R_TF^2, with 0 <= xi < 1.

    Returns
    -------
    float
    """
    return (N - 1) / (1 - xi)


def correction_ratio(xi):
    """
    Ratio C1_harm / C1_hard as a function of xi (independent of N).

    ratio = (1-xi)^2 / [(1+xi^2)(1-xi)] = (1-xi)/(1+xi^2)

    This is < 1 for all xi > 0: harmonic trap is always less stable.

    Taylor expansion: ratio = 1 - xi + xi^2 - xi^3 + ... [geometric-like]

    More precisely:
        ratio = (1-xi)/(1+xi^2)
              = 1 - xi + 0*xi^2 - xi^3 + xi^4 + ...
    Actually: (1-xi)/(1+xi^2) = (1-xi)(1-xi^2+xi^4-...) for |xi|<1
    Let's just compute: at xi=0, ratio=1. d/dxi = [-(1+xi^2) - (1-xi)(2xi)] / (1+xi^2)^2
    At xi=0: [-1 - 0] / 1 = -1. So ratio = 1 - xi + O(xi^2).

    Parameters
    ----------
    xi : float
        0 <= xi < 1.

    Returns
    -------
    float
    """
    return (1 - xi) / (1 + xi**2)


def delta_C1(N, xi):
    """
    Correction to C1: delta = C1_harm - C1_hard.

    delta_C1 = (N-1)/(1-xi) - (N-1)(1+xi^2)/(1-xi)^2
             = (N-1) * [(1-xi) - (1+xi^2)] / (1-xi)^2
             = (N-1) * [-xi(1+xi)] / (1-xi)^2    [EXACT]
             = -(N-1) * xi * (1+xi) / (1-xi)^2

    This is NEGATIVE for all xi > 0 (harmonic trap is less stable).

    Leading order: delta_C1 ~ -(N-1)*xi as xi -> 0.

    Relative to C1_hard ~ (N-1):
        delta_C1 / C1_hard = -xi*(1+xi) / (1+xi^2)  ~ -xi + O(xi^2)

    Parameters
    ----------
    N : int
    xi : float

    Returns
    -------
    float
    """
    return -(N - 1) * xi * (1 + xi) / (1 - xi)**2


# ---------------------------------------------------------------------------
# Havelock eigenvalues
# ---------------------------------------------------------------------------

def eigenvalue_hard(m, N, xi):
    """
    Havelock eigenvalue lambda_m for mode m on hard-wall disk.

    lambda_m = C1_hard(N, xi) - m(N-m)/2
    """
    return C1_hard(N, xi) - m * (N - m) / 2


def eigenvalue_harmonic(m, N, xi):
    """
    Havelock eigenvalue lambda_m for mode m in harmonic trap.

    lambda_m = C1_harm(N, xi) - m(N-m)/2
    """
    return C1_harmonic(N, xi) - m * (N - m) / 2


# ---------------------------------------------------------------------------
# Stability thresholds
# ---------------------------------------------------------------------------

def threshold_hard(N):
    """
    Hard-wall stability threshold xi* for N-ring.

    Solves C1_hard(N, xi) = m_crit(N-m_crit)/2 where m_crit = floor(N/2).
    This gives the palindromic quadratic (exact, from algebraic_thresholds.py).

    Returns
    -------
    float
        xi* (0 for N <= 7, positive for N >= 8).
    """
    m = N // 2
    T = m * (N - m) / 2.0
    A = (N - 1) - T
    if A >= 0:
        return 0.0
    # Palindromic: A*xi^2 + 2T*xi + A = 0, smaller root
    disc = T**2 - A**2
    return (T - math.sqrt(disc)) / abs(A)


def threshold_harmonic(N):
    """
    Harmonic-trap stability threshold xi* for N-ring.

    Solves C1_harm(N, xi) = m_crit(N-m_crit)/2:
        (N-1)/(1-xi) = T  =>  xi = 1 - (N-1)/T

    where T = m(N-m)/2, m = floor(N/2).

    For N <= 7: T <= N-1, so xi <= 0 (stable everywhere). Return 0.
    For N >= 8: T > N-1, so xi > 0.

    Returns
    -------
    float
        xi* (0 for N <= 7, positive for N >= 8).
    """
    m = N // 2
    T = m * (N - m) / 2.0
    if T <= (N - 1):
        return 0.0
    xi = 1.0 - (N - 1) / T
    return xi


def threshold_harmonic_exact(N):
    """
    Exact rational harmonic-trap threshold.

    xi*_harm = 1 - 2(N-1)/[m(N-m)]  where m = floor(N/2).

    Returns
    -------
    Fraction or None
        Exact rational value, or None if N <= 7 (stable at all radii).
    """
    m = N // 2
    numer_denom = Fraction(m * (N - m), 1)  # m(N-m)
    two_Nm1 = Fraction(2 * (N - 1), 1)
    xi = 1 - two_Nm1 / numer_denom
    if xi <= 0:
        return None
    return xi


# ---------------------------------------------------------------------------
# Threshold shift and comparison table
# ---------------------------------------------------------------------------

def threshold_shift(N):
    """
    Relative shift (xi*_harm - xi*_hard) / xi*_hard for a given N.

    Returns
    -------
    float or None
        Relative shift. None if N <= 7.
    """
    xh = threshold_hard(N)
    xa = threshold_harmonic(N)
    if xh == 0:
        return None
    return (xa - xh) / xh


def prediction_table(N_list=None):
    """
    Comparison table: hard-wall vs harmonic-trap threshold predictions.

    For each N, gives:
        xi_hard, r/R_hard, xi_harm, r/R_TF_harm, relative_shift

    Parameters
    ----------
    N_list : list of int or None
        N values. Default: [8, 11, 23] (the paper table values).

    Returns
    -------
    list of dict
    """
    if N_list is None:
        N_list = [8, 11, 23]
    rows = []
    for N in N_list:
        xh = threshold_hard(N)
        xa = threshold_harmonic(N)
        rR_hard = math.sqrt(xh) if xh > 0 else 0.0
        rR_harm = math.sqrt(xa) if xa > 0 else 0.0
        shift = (xa - xh) / xh if xh > 0 else None
        rows.append({
            'N': N,
            'xi_hard': xh,
            'r_over_R_hard': rR_hard,
            'xi_harm': xa,
            'r_over_R_TF_harm': rR_harm,
            'relative_shift': shift,
        })
    return rows


# ---------------------------------------------------------------------------
# N_crit for harmonic trap
# ---------------------------------------------------------------------------

def ncrit_harmonic(xi, N_max=30):
    """
    Largest stable N for a ring at parameter xi in a harmonic trap.

    The ring is stable iff min_m [C1_harm - m(N-m)/2] >= 0.

    Parameters
    ----------
    xi : float
        xi = r^2/R_TF^2.
    N_max : int
        Search up to this N.

    Returns
    -------
    int
    """
    ncrit = 2
    for N in range(3, N_max + 1):
        C1 = C1_harmonic(N, xi)
        lam_min = min(C1 - m * (N - m) / 2 for m in range(1, N // 2 + 1))
        if lam_min >= -1e-12:
            ncrit = N
        else:
            break
    return ncrit


def ncrit_hard(xi, N_max=30):
    """
    Largest stable N for a ring at parameter xi on hard-wall disk.

    Parameters
    ----------
    xi : float
        xi = r^2/R^2.
    N_max : int

    Returns
    -------
    int
    """
    ncrit = 2
    for N in range(3, N_max + 1):
        C1 = C1_hard(N, xi)
        lam_min = min(C1 - m * (N - m) / 2 for m in range(1, N // 2 + 1))
        if lam_min >= -1e-12:
            ncrit = N
        else:
            break
    return ncrit


# ---------------------------------------------------------------------------
# O(xi^2) expansion coefficients
# ---------------------------------------------------------------------------

def C1_expansion_coefficients(trap='hard', order=3):
    """
    Taylor coefficients of C1/(N-1) around xi=0.

    Hard-wall: (1+xi^2)/(1-xi)^2
        1/(1-xi)^2 = sum (n+1)*xi^n
        xi^2/(1-xi)^2 = sum (n-1)*xi^n for n>=2
        Total: c_0=1, c_1=2, c_n=2n for n>=2.
        Series: 1 + 2*xi + 4*xi^2 + 6*xi^3 + 8*xi^4 + ...

    Harmonic: 1/(1-xi) = 1 + xi + xi^2 + xi^3 + ...
        Coefficient of xi^n is 1 for all n.

    Difference: 0, 1, 3, 5, 7, ... = (2n-1) for n>=1.

    Parameters
    ----------
    trap : str
        'hard' or 'harmonic'.
    order : int
        Number of terms (0 through order-1).

    Returns
    -------
    list of float
        Coefficients [c_0, c_1, ..., c_{order-1}].
    """
    if trap == 'hard':
        coeffs = []
        for n in range(order):
            if n == 0:
                coeffs.append(1.0)
            elif n == 1:
                coeffs.append(2.0)
            else:
                coeffs.append(2.0 * n)
        return coeffs
    elif trap == 'harmonic':
        return [1.0] * order
    else:
        raise ValueError(f"Unknown trap type: {trap}")


# ---------------------------------------------------------------------------
# Main display
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    print("Harmonic trap corrections for BEC vortex stability")
    print("=" * 65)
    print()

    print("Taylor expansion of C1/(N-1):")
    print(f"  Hard-wall:   1 + 2*xi + 4*xi^2 + 6*xi^3 + ...")
    print(f"  Harmonic:    1 + xi + xi^2 + xi^3 + ...")
    print(f"  Difference:  0 - xi - 3*xi^2 - 5*xi^3 - ...")
    print()

    print("Correction ratio C1_harm/C1_hard = (1-xi)/(1+xi^2):")
    for xi in [0.01, 0.05, 0.1, 0.2, 0.5]:
        print(f"  xi = {xi:.2f}: ratio = {correction_ratio(xi):.6f}")
    print()

    print("Threshold comparison:")
    print(f"{'N':>4}  {'xi_hard':>10}  {'r/R_hard':>10}  {'xi_harm':>10}  "
          f"{'r/R_harm':>10}  {'shift':>8}")
    for row in prediction_table([8, 9, 10, 11, 12, 15, 20, 23]):
        shift_str = f"{row['relative_shift']:.1%}" if row['relative_shift'] is not None else "N/A"
        print(f"{row['N']:>4}  {row['xi_hard']:>10.6f}  {row['r_over_R_hard']:>10.4f}  "
              f"{row['xi_harm']:>10.6f}  {row['r_over_R_TF_harm']:>10.4f}  {shift_str:>8}")
    print()

    print("Exact rational harmonic thresholds:")
    for N in range(8, 24):
        xi_exact = threshold_harmonic_exact(N)
        if xi_exact is not None:
            print(f"  N={N}: xi* = {xi_exact} = {float(xi_exact):.6f}")

    print()
    print("N_crit comparison (hard vs harmonic):")
    for xi in [0.01, 0.05, 0.1, 0.2, 0.3, 0.5]:
        nh = ncrit_hard(xi)
        na = ncrit_harmonic(xi)
        print(f"  xi = {xi:.2f}: N_crit(hard) = {nh}, N_crit(harm) = {na}")
