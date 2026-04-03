"""
Onsager N-selection: H(N+1) > H(N) for kappa_0/kappa >= 1/2 and R > 1. (§4.x)

At negative temperature (Onsager regime), the equilibrium maximizes H subject
to fixed angular impulse L = Γ·R² (ring radius fixed). The energy difference:

    H(N+1) - H(N) = Γ² · [(2r-1)/(2N(N+1)) · ln R
                            + (ln N/N - ln(N+1)/(N+1))/2]

where r = κ₀/κ (central-to-ring vortex ratio), Γ = N·κ (fixed total circulation),
R = ring radius in units of vortex core radius.

Both terms are non-negative for r >= 1/2 and R > 1:
  - (2r-1) >= 0 and ln R > 0 → term1 >= 0
  - ln(N)/N is strictly decreasing for N > e → term2 > 0

So H is monotone increasing in N over the stable range.
Onsager negative-T selects N = N_max = max{N': κ_crit(N') ≤ r}.
For Jupiter north: r ≥ 0.5, N_max = 8 (κ_crit(8) = 1/2). QED.
"""
import math


def H_N(N, R, r, Gamma=1.0):
    """
    Thomson ring + central vortex Hamiltonian at fixed Gamma = N*kappa, ring radius R.

    Parameters
    ----------
    N : int
        Number of ring vortices.
    R : float
        Ring radius (in units of vortex core radius, R > 1).
    r : float
        Ratio kappa_0/kappa (central to ring vortex strength).
    Gamma : float
        Total ring circulation N*kappa (default 1.0).
    """
    kappa = Gamma / N
    kappa_0 = r * kappa
    ring_pair = -(kappa**2) * (N * (N - 1) / 2 * math.log(R) + N / 2 * math.log(N))
    center_ring = -N * kappa_0 * kappa * math.log(R)
    return ring_pair + center_ring


def H_diff(N, R, r, Gamma=1.0):
    """
    Analytic formula for H(N+1) - H(N) at fixed Gamma and R.

    H(N+1) - H(N) = Γ² · [(2r-1)/(2N(N+1)) · ln R + (ln N/N - ln(N+1)/(N+1))/2]

    Both terms are non-negative for r >= 1/2 and R > 1.
    """
    term1 = Gamma**2 * (2 * r - 1) / (2 * N * (N + 1)) * math.log(R)
    term2 = Gamma**2 / 2 * (math.log(N) / N - math.log(N + 1) / (N + 1))
    return term1 + term2


def verify_monotonicity(r_min=0.5, r_max=1.5, N_max=12, R_min=1.01, R_max=1000):
    """
    Verify H is monotone increasing in N for all r >= r_min and R > 1.

    Returns True if H(N+1) > H(N) for all tested (r, N, R) combinations.
    """
    r_vals = [r_min, (r_min + r_max) / 2, r_max]
    R_vals = [R_min, 2, 10, 100, R_max]
    for r in r_vals:
        for N in range(3, N_max):
            for R in R_vals:
                if H_diff(N, R, r) <= 0:
                    return False
    return True


# ── Onsager contraction and Sobolev bounds (Paper III) ──────────────


# Bolza surface constants
BOLZA_LAMBDA1 = 3.839      # First nonzero Laplacian eigenvalue (Buser 1992)
BOLZA_VOL = 4 * math.pi    # Area of genus-2 surface with K=-1
BOLZA_SYSTOLE = 2 * math.acosh(2)  # ≈ 2.634


def bolza_sobolev_bound(var_R=2.0, grad_R_sq=2.0):
    """
    Heat-kernel Sobolev bound on the Bolza surface.

    ||u||_inf^2 <= (lambda_1/(4*pi)) * ||u||_2^2
                 + (1/(e*lambda_1)) * ||nabla u||_2^2

    Parameters
    ----------
    var_R : float
        Var(R) = ||u||_2^2 for zero-mean u (basin condition).
    grad_R_sq : float
        ||nabla R||_2^2 (gradient energy condition).

    Returns
    -------
    sup_bound : float
        ||R - R_0||_inf
    C_S : float
        Sobolev constant (half of sup_bound at basin boundary).
    sigma_sq : float
        Hoeffding sub-Gaussian parameter.
    """
    coeff1 = BOLZA_LAMBDA1 / (4 * math.pi)       # 0.3055
    coeff2 = 1.0 / (math.e * BOLZA_LAMBDA1)      # 0.0958
    sup_sq = coeff1 * var_R + coeff2 * grad_R_sq
    sup_bound = math.sqrt(sup_sq)
    C_S = sup_bound / math.sqrt(var_R + grad_R_sq)
    sigma_sq = sup_sq  # Hoeffding: sigma^2 <= (sup-inf)^2/4 = sup^2
    return sup_bound, C_S, sigma_sq


def onsager_contraction(N, rho_star=None):
    """
    Onsager contraction factor at polygon number N.

    contraction = |beta_eff|^2 * R_0^2 * (1 + 2|V_2/V_1|*sqrt(sigma^2))^2

    Parameters
    ----------
    N : int
        Polygon number (>= 7).
    rho_star : float or None
        Palindromic threshold radius. If None, uses 1.734 for N=7.

    Returns
    -------
    float
        Contraction factor (must be < 1 for convergence).
    """
    if rho_star is None:
        # Default rho_star values at palindromic threshold
        _rho_stars = {7: 1.734, 8: 2.40, 9: 2.80, 10: 3.10, 11: 3.35}
        rho_star = _rho_stars.get(N, 1.734)

    m_star = N // 2
    f_mstar = m_star * (N - m_star) / 2
    beta_eff = 1.0 / f_mstar
    R_0 = 1.0  # |R_0| = 1 on Bolza surface

    V1 = 1.0 / math.tanh(rho_star)   # coth(rho*)
    V2 = -1.0 / math.sinh(rho_star)**2  # -csch^2(rho*)
    V2_over_V1 = abs(V2 / V1)

    _, _, sigma_sq = bolza_sobolev_bound()
    nonlinear = (1 + 2 * V2_over_V1 * math.sqrt(sigma_sq))**2
    contraction = beta_eff**2 * R_0**2 * nonlinear
    return contraction


def non_crossing_bound(N):
    """
    Non-crossing bound R_max = (N^2 - 2) / (4*N^2).

    This is strictly less than 1/4 for all N >= 2.

    Parameters
    ----------
    N : int
        Polygon number.

    Returns
    -------
    float
        R_max value.
    """
    return (N**2 - 2) / (4 * N**2)


def bath_correlation_time(N):
    """
    Bath correlation time for the CL decoherence of the breathing mode.

    The smallest positive eigenvalue among bath modes (excluding marginal)
    is lambda_min = (N - 2*m_star + 1) / 2.

    tau_bath = 1 / sqrt(lambda_min) <= sqrt(2).

    Parameters
    ----------
    N : int
        Polygon number (>= 7).

    Returns
    -------
    lambda_min : float
        Smallest positive bath eigenvalue.
    tau_bath : float
        Bath correlation time.
    """
    m_star = N // 2
    lambda_min = (N - 2 * m_star + 1) / 2
    tau_bath = 1.0 / math.sqrt(lambda_min)
    return lambda_min, tau_bath
