"""
Analytic proof of the Sign Rule (Proposition 2).

THEOREM (Sign Rule):
For the centered spiral deformation of the regular N-gon (N >= 3) with
pairwise interaction h(r), the second derivative of energy at sigma=0 is:

    H''(0) = Sum_{m=1}^{N-1} { A_m * S_m + B_m }

where:
    d_m = 2R sin(pi m/N)           [pairwise distance for separation m]
    S_m = Sum_{k=0}^{N-m-1} C_{s,k}^2   [>= 0 always]
    C_{s,k} = (2k + m - (N-1)) / (2N)

    A_m = d_m^2 h''(d_m) + d_m h'(d_m)  = d_m (d_m h''(d_m) + h'(d_m))
    B_m = h'(d_m) m^2 (N-m) / (N^2 d_m)

SUFFICIENT CONDITIONS for H''(0) < 0:
    (i)  h'(r) < 0 for all r > 0      (decreasing interaction)
    (ii) (r h'(r))' <= 0 for all r > 0  (r*h' is non-increasing)

Under (i): B_m < 0 for all m.
Under (ii): A_m = d_m * (d_m h'' + h') = d_m * (r h')' |_{r=d_m} <= 0.
Since S_m >= 0: A_m * S_m <= 0.
Therefore H''(0) = Sum(A_m * S_m + B_m) < 0. QED.

EXAMPLES:
    h(r) = -ln r:   h'=-1/r, (rh')'=0      Borderline case (A_m = 0 exactly)
    h(r) = -r^alpha: h'=-alpha*r^{alpha-1}, (rh')'=-alpha^2*r^{alpha-1} < 0
    h(r) = -1/r^n:  h'=n/r^{n+1},          (rh')'=-(n^2+n-n)/r^{n+1} = -n^2/r^{n+1} < 0
                     Wait: h'(r) = n/r^{n+1} > 0 for h(r) = -1/r^n!
                     These have h' > 0, so condition (i) fails.

    The sign rule applies to 2D-type interactions where h' < 0:
    -ln r, -r^alpha (alpha > 0), log-type interactions.

NOTE ON PHYSICS:
    The 2D Green's function gives h(r) = -ln r, which satisfies both
    conditions with (rh')' = 0 (borderline). This means the logarithmic
    interaction is the LEAST negative case among all interactions satisfying
    (i) and (ii) — for any other such interaction, H''(0) is even more negative.

NOTE ON CONSTRAINED ANALYSIS:
    H''(0) < 0 along the spiral does NOT mean the N-gon is an energy maximum.
    The constrained Hessian analysis (see constrained_hessian.py) shows the
    N-gon is an energy MINIMUM on the physically accessible surface. The spiral
    direction changes conserved quantities, making it dynamically inaccessible.
"""

import numpy as np


def pairwise_distances(N: int, R: float = 1.0) -> np.ndarray:
    """d_m = 2R sin(pi m/N) for m = 1,...,N-1."""
    m = np.arange(1, N)
    return 2 * R * np.sin(np.pi * m / N)


def center_of_mass_sum(N: int, m: int) -> float:
    """S_m = Sum_{k=0}^{N-m-1} C_{s,k}^2 where C_{s,k} = (2k+m-(N-1))/(2N)."""
    S = 0.0
    for k in range(N - m):
        C_s = (2 * k + m - (N - 1)) / (2 * N)
        S += C_s**2
    return S


def H_double_prime_analytic(N: int, h_prime, h_double_prime,
                             R: float = 1.0) -> float:
    """
    Compute H''(0) analytically for general pairwise interaction h(r).

    Parameters
    ----------
    N : int
        Number of vortices (>= 3)
    h_prime : callable
        First derivative h'(r)
    h_double_prime : callable
        Second derivative h''(r)
    R : float
        Ring radius

    Returns
    -------
    float
        H''(0) for the centered spiral deformation
    """
    result = 0.0
    for m in range(1, N):
        d_m = 2 * R * np.sin(np.pi * m / N)
        S_m = center_of_mass_sum(N, m)

        A_m = d_m**2 * h_double_prime(d_m) + d_m * h_prime(d_m)
        B_m = h_prime(d_m) * m**2 * (N - m) / (N**2 * d_m)

        result += A_m * S_m + B_m

    return result


def H_double_prime_numerical(N: int, h_func, R: float = 1.0,
                              eps: float = 1e-5) -> float:
    """Numerical H''(0) via finite differences for verification."""
    def energy(sigma):
        k = np.arange(N)
        factor = (k - (N - 1) / 2) / N
        z = R * np.exp(sigma * factor) * np.exp(2j * np.pi * k / N)
        H = 0.0
        for j in range(N):
            for m in range(j + 1, N):
                d = abs(z[j] - z[m])
                H += h_func(d)
        return H
    return (energy(eps) - 2 * energy(0) + energy(-eps)) / eps**2


def check_sign_rule_conditions(h_prime, h_double_prime,
                                r_values=None) -> dict:
    """
    Check whether h satisfies the sign rule conditions at given r values.

    Condition (i):  h'(r) < 0
    Condition (ii): r h''(r) + h'(r) <= 0, i.e., (r h'(r))' <= 0
    """
    if r_values is None:
        r_values = np.logspace(-2, 1, 100)

    hp_vals = np.array([h_prime(r) for r in r_values])
    cond_vals = np.array([r * h_double_prime(r) + h_prime(r) for r in r_values])

    return {
        'condition_i': bool(np.all(hp_vals < 0)),       # h' < 0 everywhere
        'condition_ii': bool(np.all(cond_vals <= 1e-12)), # (rh')' <= 0
        'h_prime_values': hp_vals,
        'rh_prime_derivative': cond_vals,
        'sign_rule_applies': bool(np.all(hp_vals < 0) and np.all(cond_vals <= 1e-12)),
    }


def verify_sign_rule(N_range=range(3, 10), verbose=True) -> bool:
    """
    Verify the analytic formula against numerical computation for -ln r.

    Returns True if all checks pass.
    """
    all_pass = True
    h = lambda r: -np.log(r)
    hp = lambda r: -1 / r
    hpp = lambda r: 1 / r**2

    for N in N_range:
        H_anal = H_double_prime_analytic(N, hp, hpp)
        H_num = H_double_prime_numerical(N, h)
        rel_err = abs(H_anal - H_num) / max(abs(H_num), 1e-10)
        ok = rel_err < 0.01
        all_pass = all_pass and ok
        if verbose:
            print(f"N={N}: H_anal={H_anal:.6f}, H_num={H_num:.6f}, "
                  f"rel_err={rel_err:.2e}  {'OK' if ok else 'FAIL'}")

    return all_pass
