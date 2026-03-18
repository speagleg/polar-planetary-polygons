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
