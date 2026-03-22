"""L-function computations for the Bolza form f = eta(8z)*eta(16z).

Computes L(s, f tensor chi) and L'(s, f tensor chi) for Dirichlet characters
chi mod 5.

Strategy for s=1: Abel-smoothed Dirichlet series. Compute
  S(delta) = sum_{n>=1} a_n * chi(n) / n^s * exp(-delta * n)
with delta chosen so the tail is negligible (delta * N >> 1), then
Richardson-extrapolate delta -> 0 to remove the smoothing bias.

By Abel's theorem, S(delta) -> L(s, f x chi) as delta -> 0+ whenever
the Dirichlet series converges at s.

LMFDB label: 128.1.d.a (weight-1, level 128).
"""

import mpmath

from .bolza_form import bolza_coefficients

mpmath.mp.dps = 50  # 50 decimal digits working precision

# Module-level cache for Fourier coefficients
_coeffs_cache = {}


def _get_coefficients(num_terms):
    """Return cached Fourier coefficients, computing if needed."""
    if num_terms not in _coeffs_cache:
        _coeffs_cache[num_terms] = bolza_coefficients(num_terms)
    return _coeffs_cache[num_terms]


def dirichlet_chars_mod5():
    """Return list of 4 Dirichlet characters mod 5 as callables.

    Character table mod 5 (generator g=2, order 4):
      chi_0 (trivial):  {1:1, 2:1, 3:1, 4:1}
      chi_1 = (./5):    {1:1, 2:-1, 3:-1, 4:1}   (real, Legendre symbol)
      chi_2 (order 4):  {1:1, 2:i, 3:-i, 4:-1}
      chi_3 = conj(chi_2): {1:1, 2:-i, 3:i, 4:-1}

    All return 0 for n divisible by 5.
    """
    one = mpmath.mpf(1)
    zero = mpmath.mpf(0)
    im = mpmath.mpc(0, 1)

    tables = [
        {1: one,  2: one,  3: one,   4: one},    # trivial
        {1: one,  2: -one, 3: -one,  4: one},    # real (Legendre)
        {1: one,  2: im,   3: -im,   4: -one},   # order 4
        {1: one,  2: -im,  3: im,    4: -one},   # order 4 conjugate
    ]

    def make_chi(table):
        def chi(n):
            r = n % 5
            if r == 0:
                return zero
            return table[r]
        return chi

    return [make_chi(t) for t in tables]


def _abel_smoothed_sum(coeffs, chi, s, num_terms, delta, weight_fn=None):
    """Compute Abel-smoothed Dirichlet series.

    S(delta) = sum_{n=1}^{N-1} a_n * chi(n) * w(n) / n^s * exp(-delta * n)

    Parameters
    ----------
    coeffs : list
        Fourier coefficients (index n gives a_n).
    chi : callable
        Dirichlet character mod 5.
    s : mpmath number
        Evaluation point.
    num_terms : int
        Sum up to n = num_terms - 1.
    delta : mpmath.mpf
        Smoothing parameter. For delta > 0, must satisfy delta * num_terms >> 1.
    weight_fn : callable or None
        Optional weight (e.g., -log(n) for L').

    Returns
    -------
    mpmath.mpc
    """
    total = mpmath.mpc(0)
    s = mpmath.mpc(s)
    use_smoothing = (delta > 0)
    for n in range(1, num_terms):
        an = coeffs[n]
        if an == 0:
            continue
        cv = chi(n)
        if cv == 0:
            continue
        term = mpmath.mpc(an) * cv / mpmath.power(n, s)
        if use_smoothing:
            term *= mpmath.exp(-delta * n)
        if weight_fn is not None:
            term = term * weight_fn(n)
        total += term
    return total


def _richardson_extrapolate(h_vals, f_vals):
    """Neville-Aitken Richardson extrapolation to h=0.

    Assumes f(h) = f(0) + c_1*h + c_2*h^2 + ... and extrapolates to h=0.

    Parameters
    ----------
    h_vals : list of mpmath.mpf
        Parameter values (positive, decreasing).
    f_vals : list of mpmath.mpc
        Corresponding function values.

    Returns
    -------
    mpmath.mpc
        Extrapolated value f(0).
    """
    n = len(h_vals)
    if n == 1:
        return f_vals[0]

    T = [[None] * n for _ in range(n)]
    for i in range(n):
        T[i][0] = mpmath.mpc(f_vals[i])

    for k in range(1, n):
        for i in range(k, n):
            hi = h_vals[i]
            hik = h_vals[i - k]
            T[i][k] = (hik * T[i][k - 1] - hi * T[i - 1][k - 1]) / (hik - hi)

    return T[n - 1][n - 1]


def _evaluate_at_s1(chi, coeffs, num_terms, weight_fn=None):
    """Evaluate L(1, f x chi) or L'(1, f x chi) via Abel smoothing + Richardson.

    Uses several delta values where the smoothed sum has fully converged
    (delta * num_terms >> 1), then extrapolates delta -> 0.

    Parameters
    ----------
    chi : callable
        Dirichlet character.
    coeffs : list
        Fourier coefficients.
    num_terms : int
        Number of terms.
    weight_fn : callable or None
        For L', use weight_fn(n) = -log(n).

    Returns
    -------
    mpmath.mpc
    """
    # Choose delta values: need delta * num_terms >> 1 (say >= 10)
    # Use 6 geometrically spaced values for Richardson
    min_delta = max(mpmath.mpf(10) / num_terms, mpmath.mpf('0.0001'))
    delta_list = [min_delta * mpmath.mpf(2) ** k for k in range(5, -1, -1)]

    f_list = []
    for delta in delta_list:
        val = _abel_smoothed_sum(coeffs, chi, 1, num_terms, delta, weight_fn)
        f_list.append(val)

    return _richardson_extrapolate(delta_list, f_list)


def l_value(s, chi_index, num_terms=200000, _coeffs=None):
    """Compute L(s, f tensor chi) = sum_{n>=1} a_n * chi(n) / n^s.

    For s = 1: uses Abel-smoothed sum with Richardson extrapolation.
    For s != 1: uses direct Dirichlet series (converges for Re(s) > 1).

    Parameters
    ----------
    s : complex or real
        Evaluation point (typically s=1).
    chi_index : int
        Index 0..3 into dirichlet_chars_mod5().
    num_terms : int
        Number of terms in the Dirichlet series. Default 200000 for
        ~8 digit accuracy at s=1.
    _coeffs : list or None
        Pre-computed coefficients (optimization to avoid recomputation).
    """
    chars = dirichlet_chars_mod5()
    chi = chars[chi_index]
    coeffs = _coeffs if _coeffs is not None else _get_coefficients(num_terms)

    s_mpc = mpmath.mpc(s)
    if abs(s_mpc - 1) < mpmath.mpf('1e-15'):
        return _evaluate_at_s1(chi, coeffs, num_terms)
    else:
        return _abel_smoothed_sum(coeffs, chi, s_mpc, num_terms, mpmath.mpf(0))


def l_derivative(s, chi_index, num_terms=200000, _coeffs=None):
    """Compute L'(s, f tensor chi) = -sum_{n>=1} a_n * chi(n) * ln(n) / n^s.

    For s = 1: uses Abel-smoothed sum with Richardson extrapolation.
    """
    chars = dirichlet_chars_mod5()
    chi = chars[chi_index]
    coeffs = _coeffs if _coeffs is not None else _get_coefficients(num_terms)

    def neg_log(n):
        return -mpmath.log(n)

    s_mpc = mpmath.mpc(s)
    if abs(s_mpc - 1) < mpmath.mpf('1e-15'):
        return _evaluate_at_s1(chi, coeffs, num_terms, weight_fn=neg_log)
    else:
        return _abel_smoothed_sum(coeffs, chi, s_mpc, num_terms, mpmath.mpf(0),
                                  weight_fn=neg_log)


def l_log_derivative(chi_index, num_terms=200000):
    """Compute (L'/L)(1, f tensor chi).

    Returns L'(1, f tensor chi) / L(1, f tensor chi).
    """
    coeffs = _get_coefficients(num_terms)
    lv = l_value(1, chi_index, num_terms, _coeffs=coeffs)
    ld = l_derivative(1, chi_index, num_terms, _coeffs=coeffs)
    return ld / lv


def compute_all_l_values(num_terms=200000):
    """Compute all four L(1, f tensor chi), L'(1, f tensor chi), (L'/L)(1, f tensor chi).

    Shares coefficients across all evaluations for efficiency.

    Returns
    -------
    dict with keys like 'L_1_trivial', 'Lp_1_trivial', 'LpL_1_trivial', etc.
    Labels: ['trivial', 'real', 'order4', 'order4_conj'].
    """
    labels = ['trivial', 'real', 'order4', 'order4_conj']
    coeffs = _get_coefficients(num_terms)
    result = {}

    for i, label in enumerate(labels):
        lv = l_value(1, i, num_terms, _coeffs=coeffs)
        ld = l_derivative(1, i, num_terms, _coeffs=coeffs)
        lpl = ld / lv

        result[f'L_1_{label}'] = lv
        result[f'Lp_1_{label}'] = ld
        result[f'LpL_1_{label}'] = lpl

    return result
