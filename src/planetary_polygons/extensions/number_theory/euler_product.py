"""Euler product computation of L'/L(s, f tensor chi) for the Bolza form.

Replaces the Abel-smoothed Dirichlet series approach (which gave ~3 digits)
with the Euler product over primes, which converges absolutely for Re(s) > 1.
Richardson-extrapolates from multiple s > 1 values to s = 1.

The Bolza form f = eta(8z)*eta(16z) has:
  - Level N = 128, weight 1, nebentypus eps_f = Kronecker(-2/.)
  - Euler factor at p (p nmid 128):
      (1 - a_p T + eps_f(p) T^2)^{-1}  where T = p^{-s}
  - Euler factor at p = 2: trivial (1)

For the twist by chi mod 5:
  (1 - a_p chi(p) p^{-s} + eps_f(p) chi^2(p) p^{-2s})^{-1}

LMFDB label: 128.1.d.a
"""

import mpmath

from .sieve import primes_up_to
from .arithmetic import hecke_eigenvalue_ap
from .bolza_form import _kronecker_minus2
from .singular_series import twin_prime_constant_c2
from .l_functions import _richardson_extrapolate

mpmath.mp.dps = 50

# Module-level prime cache
_prime_cache = {}


def _get_primes(bound):
    """Return cached list of primes up to bound."""
    if bound not in _prime_cache:
        _prime_cache[bound] = primes_up_to(bound)
    return _prime_cache[bound]


def _chi_table(chi_index):
    """Return the character table for chi_{chi_index} mod 5.

    Returns a dict mapping residue mod 5 -> mpmath value.
    Residue 0 always maps to 0.
    """
    one = mpmath.mpf(1)
    zero = mpmath.mpf(0)
    im = mpmath.mpc(0, 1)

    tables = [
        {0: zero, 1: one,  2: one,  3: one,   4: one},    # trivial
        {0: zero, 1: one,  2: -one, 3: -one,  4: one},    # real (Legendre)
        {0: zero, 1: one,  2: im,   3: -im,   4: -one},   # order 4
        {0: zero, 1: one,  2: -im,  3: im,    4: -one},   # order 4 conjugate
    ]
    return tables[chi_index]


def _chi_value(chi_index, n, table=None):
    """Evaluate chi_{chi_index}(n) mod 5."""
    if table is None:
        table = _chi_table(chi_index)
    return table[n % 5]


def euler_product_l_and_lpl(s, chi_index, prime_bound=1_000_000):
    """Compute L(s, f tensor chi) and (L'/L)(s, f tensor chi) via Euler product.

    For Re(s) > 1, the Euler product converges absolutely.

    Parameters
    ----------
    s : float or mpmath number
        Evaluation point, must satisfy Re(s) > 1.
    chi_index : int
        Index 0..3 for Dirichlet characters mod 5.
    prime_bound : int
        Sieve primes up to this bound.

    Returns
    -------
    (L_value, LpL_value) : tuple of mpmath.mpc
        L_value = exp(log L(s))
        LpL_value = (L'/L)(s)
    """
    s = mpmath.mpc(s)
    primes = _get_primes(prime_bound)
    chi_tab = _chi_table(chi_index)

    log_L = mpmath.mpc(0)
    LpL = mpmath.mpc(0)

    for p in primes:
        # p = 2 divides level 128: trivial Euler factor (contribution = 0)
        if p == 2:
            continue

        ap = hecke_eigenvalue_ap(p)
        eps_p = mpmath.mpc(_kronecker_minus2(p))
        chi_p = chi_tab[p % 5]

        # For p = 5 (divides character modulus): chi(5) = 0
        # Twist disappears, Euler factor is the original one for f
        # But chi_tab[0] = 0 already handles this correctly for the twist terms.
        # When chi_p = 0: factor becomes (1 - 0 + 0)^{-1} = 1, no contribution.
        # However, for p = 5, the ORIGINAL Euler factor of f still contributes.
        # We need to handle this: when p divides the character modulus (p=5),
        # the twisted Euler factor is (1 - a_p * p^{-s})^{-1} at ramified primes.
        # But for p=5, a_5 = 0 (since 5 mod 8 = 5, not 1), so the factor is 1.
        # So chi_p = 0 correctly gives factor = 1 and no contribution.

        p_neg_s = mpmath.power(p, -s)
        p_neg_2s = p_neg_s * p_neg_s
        log_p = mpmath.log(p)

        ap_mpc = mpmath.mpc(ap)
        chi_p_sq = chi_p * chi_p

        # Denominator: 1 - a_p * chi(p) * p^{-s} + eps_f(p) * chi^2(p) * p^{-2s}
        denom = 1 - ap_mpc * chi_p * p_neg_s + eps_p * chi_p_sq * p_neg_2s

        # log L contribution: -log(denom)
        log_L -= mpmath.log(denom)

        # L'/L contribution: -d/ds log(denom)
        # d/ds denom = a_p * chi(p) * log(p) * p^{-s}
        #            - 2 * eps_f(p) * chi^2(p) * log(p) * p^{-2s}
        d_denom_ds = ap_mpc * chi_p * log_p * p_neg_s \
            - 2 * eps_p * chi_p_sq * log_p * p_neg_2s

        # L'/L += -d_denom_ds / denom  (chain rule on -log(denom))
        LpL -= d_denom_ds / denom

    L_value = mpmath.exp(log_L)
    return (L_value, LpL)


def extrapolate_to_s1(chi_index, prime_bound=1_000_000):
    """Compute L(1) and (L'/L)(1) via Richardson extrapolation from s > 1.

    Evaluates the Euler product at multiple s-values approaching 1 from above,
    then uses Neville-Aitken polynomial extrapolation in h = s - 1.

    Parameters
    ----------
    chi_index : int
        Index 0..3 for Dirichlet characters mod 5.
    prime_bound : int
        Sieve primes up to this bound.

    Returns
    -------
    dict with keys:
        'L_1'       : extrapolated L(1, f tensor chi)
        'LpL_1'     : extrapolated (L'/L)(1, f tensor chi)
        's_values'  : list of s values used
        'L_values'  : list of L(s) at each s
        'LpL_values': list of (L'/L)(s) at each s
        'convergence_L'  : successive Richardson estimates for L
        'convergence_LpL': successive Richardson estimates for L'/L
    """
    s_list = [3.0, 2.5, 2.0, 1.8, 1.6, 1.5, 1.4, 1.3, 1.2, 1.15, 1.1]
    s_vals_mp = [mpmath.mpf(s) for s in s_list]
    h_vals = [s - 1 for s in s_vals_mp]

    L_vals = []
    LpL_vals = []

    for s in s_vals_mp:
        L_s, LpL_s = euler_product_l_and_lpl(s, chi_index, prime_bound)
        L_vals.append(L_s)
        LpL_vals.append(LpL_s)

    # Richardson extrapolation
    L_extrap = _richardson_extrapolate(h_vals, L_vals)
    LpL_extrap = _richardson_extrapolate(h_vals, LpL_vals)

    # Convergence info: successive extrapolations using first k points
    conv_L = []
    conv_LpL = []
    for k in range(3, len(h_vals) + 1):
        conv_L.append(_richardson_extrapolate(h_vals[:k], L_vals[:k]))
        conv_LpL.append(_richardson_extrapolate(h_vals[:k], LpL_vals[:k]))

    return {
        'L_1': L_extrap,
        'LpL_1': LpL_extrap,
        's_values': s_list,
        'L_values': L_vals,
        'LpL_values': LpL_vals,
        'convergence_L': conv_L,
        'convergence_LpL': conv_LpL,
    }


def compute_character_sum(prime_bound=1_000_000):
    """Compute sum_{chi mod 5} chi_bar(2) * (L'/L)(1, f tensor chi).

    The conjugate character values at 2:
      chi_bar_0(2) = 1
      chi_bar_1(2) = -1
      chi_bar_2(2) = -i
      chi_bar_3(2) = i

    By conjugate symmetry of chi_2 and chi_3, the sum is real.

    Parameters
    ----------
    prime_bound : int
        Sieve primes up to this bound.

    Returns
    -------
    dict with keys:
        'char_sum'      : the character sum (should be real)
        'LpL_values'    : list of (L'/L)(1) for each chi
        'L_values'      : list of L(1) for each chi
        'details'       : list of full extrapolation results
    """
    one = mpmath.mpf(1)
    im = mpmath.mpc(0, 1)
    chi_bar_2 = [one, -one, -im, im]

    labels = ['trivial', 'real', 'order4', 'order4_conj']

    LpL_vals = []
    L_vals = []
    details = []

    for i in range(4):
        print(f"\n{'='*60}")
        print(f"Computing chi_{i} ({labels[i]})...")
        print(f"{'='*60}")

        result = extrapolate_to_s1(i, prime_bound)
        LpL_vals.append(result['LpL_1'])
        L_vals.append(result['L_1'])
        details.append(result)

        print(f"  L(1, f x chi_{i})     = {mpmath.nstr(result['L_1'], 15)}")
        print(f"  (L'/L)(1, f x chi_{i}) = {mpmath.nstr(result['LpL_1'], 15)}")

        # Print convergence
        print(f"  Richardson convergence (L'/L):")
        for k, val in enumerate(result['convergence_LpL']):
            print(f"    k={k+3}: {mpmath.nstr(val, 15)}")

    # Compute character sum
    char_sum = mpmath.mpc(0)
    for i in range(4):
        char_sum += chi_bar_2[i] * LpL_vals[i]

    print(f"\n{'='*60}")
    print("Character sum decomposition:")
    for i in range(4):
        term = chi_bar_2[i] * LpL_vals[i]
        print(f"  chi_bar_{i}(2) * (L'/L)(1, f x chi_{i}) = "
              f"{mpmath.nstr(chi_bar_2[i], 5)} * {mpmath.nstr(LpL_vals[i], 12)} "
              f"= {mpmath.nstr(term, 12)}")

    print(f"\nCharacter sum = {mpmath.nstr(char_sum, 15)}")
    print(f"  Real part:      {mpmath.nstr(mpmath.re(char_sum), 15)}")
    print(f"  Imaginary part: {mpmath.nstr(mpmath.im(char_sum), 15)}")

    return {
        'char_sum': char_sum,
        'LpL_values': LpL_vals,
        'L_values': L_vals,
        'details': details,
    }


def run_level1_euler(prime_bound=1_000_000):
    """Complete Level 1 test: Euler product L'/L with Richardson extrapolation.

    Computes the character sum and compares C_FB against -pi^4/512 for
    different normalizations of S.
    """
    print("=" * 70)
    print("LEVEL 1 EULER PRODUCT TEST")
    print("L'/L(s, f tensor chi) via Euler product, Richardson to s=1")
    print(f"Prime bound: {prime_bound:,}")
    print("=" * 70)

    # Step 1: character sum
    cs_result = compute_character_sum(prime_bound)
    char_sum = cs_result['char_sum']
    char_sum_re = mpmath.re(char_sum)

    # Step 2: compute constants
    C2 = twin_prime_constant_c2(prime_bound)
    S_quarter = C2 / 4        # S = C_2 / 4
    S_bh = (mpmath.mpf(10) / 3) * C2   # S = (10/3) * C_2

    pi4_512 = mpmath.power(mpmath.pi, 4) / 512
    target = mpmath.pi ** 4 / (64 * C2)

    print(f"\n{'='*70}")
    print("RESULTS SUMMARY")
    print(f"{'='*70}")

    print(f"\nCharacter sum = sum chi_bar(2) * (L'/L)(1, f x chi):")
    print(f"  Re = {mpmath.nstr(char_sum_re, 15)}")
    print(f"  Im = {mpmath.nstr(mpmath.im(char_sum), 15)}  (should be ~0)")

    print(f"\nC_2 (wide convention) = {mpmath.nstr(C2, 15)}")
    print(f"pi^4/512              = {mpmath.nstr(pi4_512, 15)}")

    # Test 1: S = C_2 / 4
    print(f"\n--- Test with S = C_2/4 = {mpmath.nstr(S_quarter, 15)} ---")
    C_FB_1 = mpmath.mpf('-0.5') * S_quarter * char_sum_re
    print(f"  C_FB = -0.5 * S * char_sum = {mpmath.nstr(C_FB_1, 15)}")
    print(f"  Target -pi^4/512           = {mpmath.nstr(-pi4_512, 15)}")
    ratio1 = C_FB_1 / (-pi4_512)
    print(f"  Ratio C_FB / (-pi^4/512)   = {mpmath.nstr(ratio1, 15)}")

    print(f"\n  If C_FB should equal -pi^4/512:")
    print(f"    char_sum should be pi^4/(64*C_2) = {mpmath.nstr(target, 15)}")
    print(f"    char_sum is                        {mpmath.nstr(char_sum_re, 15)}")
    ratio_cs = char_sum_re / target
    print(f"    Ratio char_sum / target            = {mpmath.nstr(ratio_cs, 15)}")

    # Test 2: S = (10/3) * C_2
    print(f"\n--- Test with S = (10/3)*C_2 = {mpmath.nstr(S_bh, 15)} ---")
    C_FB_2 = mpmath.mpf('-0.5') * S_bh * char_sum_re
    print(f"  C_FB = -0.5 * S * char_sum = {mpmath.nstr(C_FB_2, 15)}")
    print(f"  Target -pi^4/512           = {mpmath.nstr(-pi4_512, 15)}")
    ratio2 = C_FB_2 / (-pi4_512)
    print(f"  Ratio C_FB / (-pi^4/512)   = {mpmath.nstr(ratio2, 15)}")

    # Individual L-values
    print(f"\n{'='*70}")
    print("Individual L-values at s = 1:")
    labels = ['trivial', 'real', 'order4', 'order4_conj']
    for i in range(4):
        L_val = cs_result['L_values'][i]
        LpL_val = cs_result['LpL_values'][i]
        print(f"  chi_{i} ({labels[i]:12s}): "
              f"L(1) = {mpmath.nstr(L_val, 12)},  "
              f"L'/L(1) = {mpmath.nstr(LpL_val, 12)}")

    print(f"\nL(1, f) [trivial char] = {mpmath.nstr(cs_result['L_values'][0], 15)}")
    print(f"  Expected ~0.8154")

    return {
        'char_sum': char_sum,
        'C2': C2,
        'C_FB_quarter': C_FB_1,
        'C_FB_bh': C_FB_2,
        'target_pi4_512': -pi4_512,
        'target_charsum': target,
        'L_values': cs_result['L_values'],
        'LpL_values': cs_result['LpL_values'],
    }


if __name__ == '__main__':
    run_level1_euler()
