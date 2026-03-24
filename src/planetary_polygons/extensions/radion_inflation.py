r"""
Radion inflation in the Havelock Field Theory.

The radion σ (S¹ modulus) has potential:
  V(σ) = N²/(8σ²) - c/(12σ) + Λσ

where N²/(8σ²) = flux energy, c/(12σ) = Casimir, Λσ = cosmological.

At large σ: V ≈ Λσ (linear potential inflation).
Stabilized at σ_min ≈ 1.35 (for N=11).

Predictions at 60 e-folds:
  n_s = 0.973 (observed: 0.965 ± 0.004, ~2σ high)
  r = 0.070 (bound: r < 0.06, slightly above)

The model is MARGINAL with current data but TESTABLE:
LiteBIRD and CMB-S4 will measure r to ±0.001,
decisively testing the linear radion potential.
"""

from math import sqrt, log, exp, pi


def b_exact(N):
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


def V_radion(sigma, N=11):
    """The radion effective potential."""
    c = 12 * b_exact(N)
    Lambda = (N**2 - 16) / 16
    return N**2 / (8 * sigma**2) - c / (12 * sigma) + Lambda * sigma


def V_prime(sigma, N=11, ds=1e-8):
    return (V_radion(sigma + ds, N) - V_radion(sigma - ds, N)) / (2 * ds)


def V_dprime(sigma, N=11, ds=1e-6):
    return (V_radion(sigma + ds, N) - 2 * V_radion(sigma, N) + V_radion(sigma - ds, N)) / ds**2


def find_minimum(N=11):
    """Find the radion minimum by scanning."""
    best_s, best_vp = 1.0, abs(V_prime(1.0, N))
    for s1000 in range(100, 5000):
        s = s1000 / 1000
        vp = abs(V_prime(s, N))
        if vp < best_vp:
            best_s, best_vp = s, vp
    return best_s


def slow_roll(sigma, N=11):
    """Compute slow-roll parameters at given σ."""
    c = 12 * b_exact(N)
    M_P = sqrt(c / (24 * pi**2))
    V = V_radion(sigma, N)
    Vp = V_prime(sigma, N)
    Vpp = V_dprime(sigma, N)
    if V <= 0 or abs(Vp) == 0:
        return None
    eps = (M_P**2 / 2) * (Vp / V)**2
    eta = M_P**2 * Vpp / V
    return {'epsilon': eps, 'eta': eta, 'V': V}


def inflation_predictions(N=11, N_efolds=60):
    """Compute inflationary predictions at N_efolds before end.

    Returns n_s, r, and the starting σ.
    """
    c = 12 * b_exact(N)
    M_P = sqrt(c / (24 * pi**2))
    sigma_min = find_minimum(N)

    # σ_start from N_e = (σ² - σ_min²) / (2 M_P²)
    sigma_start = sqrt(2 * N_efolds * M_P**2 + sigma_min**2)

    sr = slow_roll(sigma_start, N)
    if sr is None:
        return None

    n_s = 1 - 6 * sr['epsilon'] + 2 * sr['eta']
    r = 16 * sr['epsilon']

    return {
        'N': N,
        'N_efolds': N_efolds,
        'sigma_min': sigma_min,
        'sigma_start': sigma_start,
        'epsilon': sr['epsilon'],
        'eta': sr['eta'],
        'n_s': n_s,
        'r': r,
        'n_s_observed': 0.965,
        'n_s_error': 0.004,
        'r_bound': 0.06,
        'n_s_tension_sigma': abs(n_s - 0.965) / 0.004,
        'r_within_bound': r < 0.06,
    }
