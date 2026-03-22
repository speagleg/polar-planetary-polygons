"""Level 1 numerical test: C_FB = -pi^4/512 for the Bolza modular form.

Tests the formula:
  C_FB = -1/2 * S_{40,17} * sum_{chi mod 5} chi_bar(2) * (L'/L)(1, f tensor chi)

against the target value -pi^4/512.

Here f = eta(8z)*eta(16z) is the Bolza form (LMFDB 128.1.d.a, weight 1, level 128).
"""

import mpmath

from .l_functions import (
    l_value, l_derivative, dirichlet_chars_mod5, _get_coefficients,
)
from .singular_series import twin_prime_constant_c2, compute_s40_17

mpmath.mp.dps = 50


def run_level1_test(num_terms=200000):
    """Run the Level 1 numerical test and print a detailed report.

    Computes C_FB via the L-function formula and compares to -pi^4/512.
    """
    print("=" * 72)
    print("LEVEL 1 TEST: C_FB = -pi^4/512 for the Bolza form f = eta(8z)*eta(16z)")
    print("=" * 72)
    print()

    # Pre-compute coefficients once
    coeffs = _get_coefficients(num_terms)

    # ---------------------------------------------------------------
    # Step 0: Self-consistency check on L(1, f) convergence
    # ---------------------------------------------------------------
    print("--- Step 0: Convergence check ---")
    half_terms = num_terms // 2
    coeffs_half = _get_coefficients(half_terms)
    L_half = l_value(1, 0, num_terms=half_terms, _coeffs=coeffs_half)
    L_full = l_value(1, 0, num_terms=num_terms, _coeffs=coeffs)
    rel_diff = abs(L_half - L_full) / abs(L_full)
    matching_digits = -mpmath.log10(rel_diff) if rel_diff > 0 else 50
    print(f"  L(1, f) at {half_terms} terms: {mpmath.nstr(L_half, 15)}")
    print(f"  L(1, f) at {num_terms} terms: {mpmath.nstr(L_full, 15)}")
    print(f"  Relative difference:   {mpmath.nstr(rel_diff, 5)}")
    print(f"  Matching digits:       {mpmath.nstr(matching_digits, 4)}")
    print()

    # ---------------------------------------------------------------
    # Step 1: Compute all L-values, L'-values, L'/L values
    # ---------------------------------------------------------------
    print("--- Step 1: L-function values at s=1 ---")
    labels = ['trivial', 'real', 'order4', 'order4_conj']
    chi_names = ['chi_0 (trivial)', 'chi_1 (./5)', 'chi_2 (order 4)', 'chi_3 (conj)']

    L_vals = []
    Lp_vals = []
    LpL_vals = []

    for i, (label, name) in enumerate(zip(labels, chi_names)):
        lv = l_value(1, i, num_terms, _coeffs=coeffs)
        ld = l_derivative(1, i, num_terms, _coeffs=coeffs)
        lpl = ld / lv
        L_vals.append(lv)
        Lp_vals.append(ld)
        LpL_vals.append(lpl)
        print(f"  {name}:")
        print(f"    L(1, f x {label})    = {mpmath.nstr(lv, 15)}")
        print(f"    L'(1, f x {label})   = {mpmath.nstr(ld, 15)}")
        print(f"    (L'/L)(1, f x {label}) = {mpmath.nstr(lpl, 15)}")
        print()

    # ---------------------------------------------------------------
    # Step 2: Character sum  sum_chi chi_bar(2) * (L'/L)(1, f x chi)
    # ---------------------------------------------------------------
    print("--- Step 2: Character sum ---")
    # chi(2) = [1, -1, i, -i], so chi_bar(2) = [1, -1, -i, i]
    chi_bar_2 = [
        mpmath.mpf(1),
        mpmath.mpf(-1),
        mpmath.mpc(0, -1),
        mpmath.mpc(0, 1),
    ]
    print(f"  chi_bar(2) values: {[mpmath.nstr(c, 5) for c in chi_bar_2]}")

    char_sum = mpmath.mpc(0)
    for i in range(4):
        term = chi_bar_2[i] * LpL_vals[i]
        char_sum += term
        print(f"  chi_bar(2) * (L'/L) for {labels[i]}: {mpmath.nstr(term, 15)}")

    print(f"\n  Character sum = {mpmath.nstr(char_sum, 15)}")
    print(f"  |Im(char_sum)| = {mpmath.nstr(abs(mpmath.im(char_sum)), 5)}")
    print()

    # ---------------------------------------------------------------
    # Step 3: Singular series constant S_{40,17}
    # ---------------------------------------------------------------
    print("--- Step 3: Singular series ---")
    c2 = twin_prime_constant_c2()
    s40_17 = compute_s40_17()
    print(f"  C_2 (wide convention) = {mpmath.nstr(c2, 15)}")
    print(f"  S_{{40,17}} = (10/3)*C_2 = {mpmath.nstr(s40_17, 15)}")
    print()

    # ---------------------------------------------------------------
    # Step 4: Compute C_FB
    # ---------------------------------------------------------------
    print("--- Step 4: C_FB computation ---")
    # C_FB = -1/2 * S_{40,17} * character_sum
    C_FB = mpmath.mpf(-0.5) * s40_17 * char_sum
    print(f"  C_FB = -1/2 * S_{{40,17}} * char_sum")
    print(f"       = {mpmath.nstr(C_FB, 15)}")
    print(f"  Re(C_FB) = {mpmath.nstr(mpmath.re(C_FB), 15)}")
    print(f"  Im(C_FB) = {mpmath.nstr(mpmath.im(C_FB), 5)}")
    print()

    # ---------------------------------------------------------------
    # Step 5: Compare to target
    # ---------------------------------------------------------------
    print("--- Step 5: Comparison ---")
    target = -mpmath.pi ** 4 / 512
    print(f"  Target = -pi^4/512 = {mpmath.nstr(target, 15)}")
    print(f"  C_FB (real part)   = {mpmath.nstr(mpmath.re(C_FB), 15)}")

    residual = abs(mpmath.re(C_FB) - target)
    rel_residual = residual / abs(target)
    digits = -mpmath.log10(rel_residual) if rel_residual > 0 else 50

    print(f"\n  Absolute residual: {mpmath.nstr(residual, 5)}")
    print(f"  Relative residual: {mpmath.nstr(rel_residual, 5)}")
    print(f"  Matching digits:   {mpmath.nstr(digits, 4)}")
    print()

    if digits >= 4:
        print(f"  *** LEVEL 1 TEST PASSES: {mpmath.nstr(digits, 4)} matching digits ***")
    else:
        print(f"  *** LEVEL 1 TEST: only {mpmath.nstr(digits, 4)} matching digits ***")
        print(f"  (May need more terms or investigation)")

    print("=" * 72)

    return {
        'C_FB': C_FB,
        'target': target,
        'residual': residual,
        'rel_residual': rel_residual,
        'matching_digits': digits,
        'char_sum': char_sum,
        'S40_17': s40_17,
        'C2': c2,
        'L_vals': L_vals,
        'Lp_vals': Lp_vals,
        'LpL_vals': LpL_vals,
    }


if __name__ == '__main__':
    run_level1_test()
