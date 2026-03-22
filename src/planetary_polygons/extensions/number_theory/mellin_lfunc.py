"""
Mellin integral computation of L(1, f⊗χ) and L'(1, f⊗χ) for the Bolza form.

Uses the functional equation to fold the Mellin integral into an
EXPONENTIALLY CONVERGENT form requiring only ~50 q-expansion terms
for 15+ digit precision.

For f of weight 1, level N, root number ε (self-dual):

  (2π)^{-s} Γ(s) L(s) = ∫₀^∞ f(iy) y^{s-1} dy

Atkin-Lehner for weight 1: f(i/(Ny)) = -ε·√N·y·f(iy)

Folding at y₀ = 1/√N:
  L(s) = (2π)^s/Γ(s) · ∫_{y₀}^∞ f(iy)·[y^{s-1} - ε·N^{1/2-s}·y^{-s}] dy

At s = 1:
  L(1) = 2π · ∫_{y₀}^∞ f(iy)·[1 - ε·y₀/y] dy

For L'(1): differentiate and evaluate.
"""

import mpmath

mpmath.mp.dps = 50

from .bolza_form import bolza_coefficients
from .l_functions import dirichlet_chars_mod5
from .singular_series import twin_prime_constant_c2


def _f_iy(y, coeffs, chi_fn=None):
    """Compute f_χ(iy) = Σ a_n·χ(n)·exp(-2πny)."""
    total = mpmath.mpf(0)
    two_pi = 2 * mpmath.pi
    for n in range(1, len(coeffs)):
        an = coeffs[n]
        if an == 0:
            continue
        if chi_fn is not None:
            cv = chi_fn(n)
            if cv == 0:
                continue
            term = mpmath.mpf(an) * cv * mpmath.exp(-two_pi * n * y)
        else:
            term = mpmath.mpf(an) * mpmath.exp(-two_pi * n * y)
        total += term
        # Early exit: if exp(-2πny) < 10^{-40}, remaining terms are negligible
        if two_pi * n * y > 92:  # exp(-92) ≈ 10^{-40}
            break
    return total


def _determine_root_number(coeffs, N_level, chi_fn=None, chi_bar_fn=None):
    """Determine root number ε empirically by testing both signs."""
    y0 = 1 / mpmath.sqrt(N_level)

    def integrand_plus(y):
        fiy = _f_iy(y, coeffs, chi_fn)
        return fiy * (1 - y0 / y)

    def integrand_minus(y):
        fiy = _f_iy(y, coeffs, chi_fn)
        return fiy * (1 + y0 / y)

    y_max = mpmath.mpf(10)
    I_plus = mpmath.quad(integrand_plus, [y0, y_max])
    I_minus = mpmath.quad(integrand_minus, [y0, y_max])

    L_plus = 2 * mpmath.pi * I_plus
    L_minus = 2 * mpmath.pi * I_minus

    return L_plus, L_minus


def mellin_l_value(coeffs, N_level, epsilon, chi_fn=None, chi_bar_fn=None):
    """Compute L(1, f⊗χ) via the Mellin integral.

    For self-dual twists (chi_bar_fn is None):
      L(1) = 2π · ∫_{y₀}^∞ f_χ(iy)·[1 - ε·y₀/y] dy

    For non-self-dual twists:
      L(1) = 2π · [∫_{y₀}^∞ f_χ(iy) dy - ε·N^{-1/2}·∫_{y₀}^∞ f_{χ̄}(iy)/y dy]
    """
    y0 = 1 / mpmath.sqrt(N_level)
    y_max = mpmath.mpf(10)

    if chi_bar_fn is None:
        # Self-dual case
        def integrand(y):
            fiy = _f_iy(y, coeffs, chi_fn)
            return fiy * (1 - epsilon * y0 / y)

        I = mpmath.quad(integrand, [y0, y_max])
        return 2 * mpmath.pi * I
    else:
        # Non-self-dual case
        def integrand1(y):
            return _f_iy(y, coeffs, chi_fn) * mpmath.power(y, 0)

        def integrand2(y):
            return _f_iy(y, coeffs, chi_bar_fn) / y

        I1 = mpmath.quad(integrand1, [y0, y_max])
        I2 = mpmath.quad(integrand2, [y0, y_max])
        return 2 * mpmath.pi * (I1 - epsilon * mpmath.power(N_level, mpmath.mpf('-0.5')) * I2)


def mellin_l_derivative(coeffs, N_level, epsilon, chi_fn=None, chi_bar_fn=None):
    """Compute L'(1, f⊗χ) via the Mellin integral.

    L'(1) = 2π·[log(2π)+γ]·I₀ + 2π·I₁

    where:
      I₀ = ∫_{y₀}^∞ f_χ(iy)·[1 - ε·y₀/y] dy
      I₁ = ∫_{y₀}^∞ f_χ(iy)·[log(y) + ε·(y₀/y)·(log N + log y)] dy
    """
    y0 = 1 / mpmath.sqrt(N_level)
    logN = mpmath.log(N_level)
    y_max = mpmath.mpf(10)
    gamma = mpmath.euler
    log2pi = mpmath.log(2 * mpmath.pi)

    if chi_bar_fn is None:
        # Self-dual case
        def integrand_I0(y):
            fiy = _f_iy(y, coeffs, chi_fn)
            return fiy * (1 - epsilon * y0 / y)

        def integrand_I1(y):
            fiy = _f_iy(y, coeffs, chi_fn)
            logy = mpmath.log(y)
            return fiy * (logy + epsilon * (y0 / y) * (logN + logy))

        I0 = mpmath.quad(integrand_I0, [y0, y_max])
        I1 = mpmath.quad(integrand_I1, [y0, y_max])

        return 2 * mpmath.pi * (log2pi + gamma) * I0 + 2 * mpmath.pi * I1
    else:
        # Non-self-dual: use finite differences as fallback
        h = mpmath.mpf('0.0001')
        Lp = _mellin_at_s(coeffs, N_level, epsilon, 1 + h, chi_fn, chi_bar_fn)
        Lm = _mellin_at_s(coeffs, N_level, epsilon, 1 - h, chi_fn, chi_bar_fn)
        return (Lp - Lm) / (2 * h)


def _mellin_at_s(coeffs, N_level, epsilon, s, chi_fn=None, chi_bar_fn=None):
    """Compute L(s, f⊗χ) for general s via the Mellin integral."""
    y0 = 1 / mpmath.sqrt(N_level)
    y_max = mpmath.mpf(10)
    prefactor = mpmath.power(2 * mpmath.pi, s) / mpmath.gamma(s)

    if chi_bar_fn is None:
        def integrand(y):
            fiy = _f_iy(y, coeffs, chi_fn)
            return fiy * (mpmath.power(y, s - 1) - epsilon * mpmath.power(N_level, mpmath.mpf(0.5) - s) * mpmath.power(y, -s))

        I = mpmath.quad(integrand, [y0, y_max])
        return prefactor * I
    else:
        def integrand1(y):
            return _f_iy(y, coeffs, chi_fn) * mpmath.power(y, s - 1)

        def integrand2(y):
            return _f_iy(y, coeffs, chi_bar_fn) * mpmath.power(y, -s)

        I1 = mpmath.quad(integrand1, [y0, y_max])
        I2 = mpmath.quad(integrand2, [y0, y_max])
        return prefactor * (I1 - epsilon * mpmath.power(N_level, mpmath.mpf(0.5) - s) * I2)


def run_mellin_level1(num_terms=200):
    """Complete Level 1 + Level 2 test using Mellin integral."""
    print("=" * 72)
    print("MELLIN INTEGRAL: L-values for f = η(8z)η(16z)")
    print("=" * 72)

    coeffs = bolza_coefficients(num_terms)
    chars = dirichlet_chars_mod5()
    labels = ['trivial', 'real', 'order4', 'order4_conj']
    chi_names = ['χ₀', 'χ₁=(·/5)', 'χ₂ (order 4)', 'χ₃=conj(χ₂)']

    # Character properties
    # χ₀, χ₁ are real (self-dual twists)
    # χ₂, χ₃ are conjugates (non-self-dual)
    is_self_dual = [True, True, False, False]
    conjugate_index = [0, 1, 3, 2]  # χ₂ ↔ χ₃

    # Levels: trivial → 128, non-trivial mod 5 → 128·25 = 3200
    levels = [128, 3200, 3200, 3200]

    # Step 1: Determine root numbers empirically
    print("\n--- Step 1: Determine root numbers ---")
    epsilons = [None, None, None, None]

    for i in range(4):
        if not is_self_dual[i]:
            continue
        chi_fn = None if i == 0 else chars[i]
        Lp, Lm = _determine_root_number(coeffs, levels[i], chi_fn)
        print(f"  {chi_names[i]} (N={levels[i]}): L(ε=+1)={mpmath.nstr(Lp, 10)}, L(ε=-1)={mpmath.nstr(Lm, 10)}")

        # Expected: L(1,f) ≈ 0.815, L(1,f⊗χ₁) ≈ 1.051
        if i == 0:
            expected = mpmath.mpf('0.815')
        elif i == 1:
            expected = mpmath.mpf('1.051')
        else:
            expected = mpmath.mpf('1.0')

        if abs(Lp - expected) < abs(Lm - expected):
            epsilons[i] = 1
            print(f"    → ε = +1 (matches expected {mpmath.nstr(expected, 4)})")
        else:
            epsilons[i] = -1
            print(f"    → ε = -1 (matches expected {mpmath.nstr(expected, 4)})")

    # For non-self-dual: determine from the pair
    # Try both signs and pick the one giving conjugate L-values
    print(f"\n  Determining ε for order-4 twist...")
    for eps_try in [1, -1]:
        L_chi2 = _mellin_at_s(coeffs, 3200, eps_try, mpmath.mpf(1),
                               chi_fn=chars[2], chi_bar_fn=chars[3])
        print(f"    ε={eps_try:+d}: L(1, f⊗χ₂) = {mpmath.nstr(L_chi2, 10)}")
        # Expected: ≈ 1.134 - 0.102i
        if abs(mpmath.re(L_chi2) - 1.134) < 0.1:
            epsilons[2] = eps_try
            epsilons[3] = eps_try  # same root number for conjugate pair
            print(f"    → ε = {eps_try:+d}")
            break

    if epsilons[2] is None:
        print("    WARNING: Could not determine ε for order-4 twist, trying ε=+1")
        epsilons[2] = epsilons[3] = 1

    # Step 2: Compute all L-values and derivatives
    print("\n--- Step 2: L-values and L'/L via Mellin integral ---")
    L_vals = []
    Lp_vals = []
    LpL_vals = []

    for i in range(4):
        chi_fn = None if i == 0 else chars[i]
        chi_bar_fn = None
        if not is_self_dual[i]:
            chi_bar_fn = chars[conjugate_index[i]]

        L1 = mellin_l_value(coeffs, levels[i], epsilons[i], chi_fn, chi_bar_fn)
        Ld1 = mellin_l_derivative(coeffs, levels[i], epsilons[i], chi_fn, chi_bar_fn)
        LpL1 = Ld1 / L1

        L_vals.append(L1)
        Lp_vals.append(Ld1)
        LpL_vals.append(LpL1)

        print(f"  {chi_names[i]} (N={levels[i]}, ε={epsilons[i]:+d}):")
        print(f"    L(1)   = {mpmath.nstr(L1, 15)}")
        print(f"    L'(1)  = {mpmath.nstr(Ld1, 15)}")
        print(f"    L'/L(1)= {mpmath.nstr(LpL1, 15)}")
        print()

    # Step 3: Character sum
    print("--- Step 3: Character sum ---")
    chi_bar_2 = [mpmath.mpf(1), mpmath.mpf(-1), mpmath.mpc(0, -1), mpmath.mpc(0, 1)]
    char_sum = sum(chi_bar_2[i] * LpL_vals[i] for i in range(4))
    print(f"  Σ χ̄(2)·(L'/L)(1, f⊗χ) = {mpmath.nstr(char_sum, 15)}")
    print(f"  Re = {mpmath.nstr(mpmath.re(char_sum), 15)}")
    print(f"  Im = {mpmath.nstr(mpmath.im(char_sum), 10)} (should be ~0)")
    char_sum_re = mpmath.re(char_sum)
    print()

    # Step 4: C₂ and S_{40,17}
    print("--- Step 4: Constants ---")
    C2 = twin_prime_constant_c2()
    print(f"  C₂ (wide) = {mpmath.nstr(C2, 15)}")
    print()

    # Step 5: Test multiple S normalizations
    print("--- Step 5: Level 1 test — C_FB = -π⁴/512? ---")
    target = -mpmath.pi ** 4 / 512
    print(f"  Target: -π⁴/512 = {mpmath.nstr(target, 15)}")
    print()

    candidates = [
        ("C₂/4 = C₂/φ(5)", C2 / 4),
        ("(10/3)·C₂", mpmath.mpf(10) / 3 * C2),
        ("C₂/16 = C₂/φ(40)", C2 / 16),
        ("C₂", C2),
    ]

    for name, S in candidates:
        cfb = mpmath.mpf('-0.5') * S * char_sum_re
        ratio = cfb / target
        digits = -mpmath.log10(abs(ratio - 1)) if abs(ratio - 1) > 0 else 50
        marker = " ← BEST" if abs(ratio - 1) < 0.05 else ""
        print(f"  S = {name:<25s}: C_FB = {mpmath.nstr(cfb, 10)}, ratio = {mpmath.nstr(ratio, 8)}, digits = {mpmath.nstr(digits, 3)}{marker}")

    # Step 6: Level 2 test — does C₂ cancel?
    print("\n--- Step 6: Level 2 — does C₂ cancel? ---")
    # If C_FB = -π⁴/512 with S = C₂/4:
    # Then char_sum = π⁴/(64·C₂)
    predicted_char_sum = mpmath.pi ** 4 / (64 * C2)
    print(f"  If C_FB = -π⁴/512 with S = C₂/4:")
    print(f"    Predicted char_sum = π⁴/(64·C₂) = {mpmath.nstr(predicted_char_sum, 15)}")
    print(f"    Computed char_sum  = {mpmath.nstr(char_sum_re, 15)}")
    ratio2 = char_sum_re / predicted_char_sum
    print(f"    Ratio = {mpmath.nstr(ratio2, 10)}")
    print(f"    → C₂ {'CANCELS' if abs(ratio2 - 1) < 0.001 else 'does NOT cancel (or formula needs correction)'}")

    # Also test: does char_sum have a closed form independent of C₂?
    print(f"\n  char_sum · 64 = {mpmath.nstr(char_sum_re * 64, 15)}")
    print(f"  π⁴/C₂         = {mpmath.nstr(mpmath.pi ** 4 / C2, 15)}")
    print(f"  π⁴             = {mpmath.nstr(mpmath.pi ** 4, 15)}")

    print("\n" + "=" * 72)

    return {
        'L_vals': L_vals,
        'Lp_vals': Lp_vals,
        'LpL_vals': LpL_vals,
        'char_sum': char_sum,
        'epsilons': epsilons,
        'target': target,
    }


if __name__ == '__main__':
    run_mellin_level1()
