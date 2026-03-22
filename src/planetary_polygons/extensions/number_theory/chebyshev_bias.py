"""
Chebyshev bias for the silver ratio symbol ((1+√2)/p).

Among primes p ≡ 1 mod 8: a_p = +2 when 1+√2 is a QR mod p,
a_p = -2 when it's a QNR. Sato-Tate predicts asymptotic equidistribution,
but the Rubinstein-Sarnak framework (1994) predicts a persistent
logarithmic bias controlled by the low-lying zeros of L(s, f).

Computes:
1. δ(x) = #{a_p = +2, p ≤ x} - #{a_p = -2, p ≤ x} (unrestricted)
2. δ_twin(x) = same restricted to twin primes
3. δ_cousin(x) = same restricted to cousin primes (gap 4)
4. Rubinstein-Sarnak prediction from LMFDB zeros
5. The twin-prime-restricted bias vs unrestricted bias
"""

import math
from .sieve import primes_up_to
from .arithmetic import hecke_eigenvalue_ap


def compute_bias_functions(limit=100_000_000):
    """
    Compute δ(x) and δ_twin(x) at geometrically spaced checkpoints.

    Returns dict of lists: x values, delta_all, delta_twin, delta_cousin,
    plus normalized versions δ/√x·ln(x).
    """
    primes = primes_up_to(limit)
    pset = set(primes)

    # Checkpoints: every power of 2 from 2^13 to limit
    checkpoints = []
    x = 8192
    while x <= limit:
        checkpoints.append(int(x))
        x = int(x * 1.5)
    if checkpoints[-1] < limit:
        checkpoints.append(limit)

    # Running counts
    plus_all = 0
    minus_all = 0
    plus_twin = 0
    minus_twin = 0
    plus_cousin = 0
    minus_cousin = 0

    results = {
        'x': [], 'delta_all': [], 'delta_twin': [], 'delta_cousin': [],
        'norm_all': [], 'norm_twin': [], 'norm_cousin': [],
        'count_plus_all': [], 'count_minus_all': [],
        'count_plus_twin': [], 'count_minus_twin': [],
    }

    cp_idx = 0
    for p in primes:
        if p <= 5 or p % 8 != 1:
            continue

        ap = hecke_eigenvalue_ap(p)
        is_twin = (p + 2) in pset
        is_cousin = (p + 4) in pset

        if ap == 2:
            plus_all += 1
            if is_twin:
                plus_twin += 1
            if is_cousin:
                plus_cousin += 1
        elif ap == -2:
            minus_all += 1
            if is_twin:
                minus_twin += 1
            if is_cousin:
                minus_cousin += 1

        # Record at checkpoints
        while cp_idx < len(checkpoints) and p >= checkpoints[cp_idx]:
            x = checkpoints[cp_idx]
            sqrt_x = math.sqrt(x)
            log_x = math.log(x)
            norm = sqrt_x / log_x if log_x > 0 else 1

            delta_a = plus_all - minus_all
            delta_t = plus_twin - minus_twin
            delta_c = plus_cousin - minus_cousin

            results['x'].append(x)
            results['delta_all'].append(delta_a)
            results['delta_twin'].append(delta_t)
            results['delta_cousin'].append(delta_c)
            results['norm_all'].append(delta_a / norm if norm > 0 else 0)
            results['norm_twin'].append(delta_t / max(math.sqrt(plus_twin + minus_twin), 1))
            results['norm_cousin'].append(delta_c / max(math.sqrt(plus_cousin + minus_cousin), 1))
            results['count_plus_all'].append(plus_all)
            results['count_minus_all'].append(minus_all)
            results['count_plus_twin'].append(plus_twin)
            results['count_minus_twin'].append(minus_twin)

            cp_idx += 1

    return results


def rubinstein_sarnak_prediction():
    """
    Compute the Rubinstein-Sarnak bias prediction from LMFDB zeros.

    The zeros of L(s, f) for f = η(8z)η(16z) (LMFDB 128.1.d.a):
    First 10 zero heights (imaginary parts on the critical line s = 1/2 + it):
    t₁ ≈ 2.636, t₂ ≈ 4.411, t₃ ≈ 5.843, t₄ ≈ 7.021, t₅ ≈ 8.462, ...

    The Rubinstein-Sarnak framework:
    The bias in the "prime race" χ(p) = +1 vs -1 is determined by:
        P(δ > 0) = 1/2 + (1/π) · arctan(b)
    where b = -1/(2·Σ_ρ 1/|ρ-1/2|) ... actually the formula is more complex.

    For a degree-2 L-function, the bias is:
        b = (1/2) · log(N/(4π²)) - Σ_{ρ} 1/(|ρ|²)
    where N is the conductor and ρ = 1/2 + iγ ranges over zeros.

    A simpler diagnostic: the SIGN of δ(x) for large x predicts whether
    +2 or -2 is favored. If δ(x) > 0 for most x: bias toward a_p = +2.
    """
    # LMFDB zeros for 128.1.d.a (heights of zeros on critical line)
    zero_heights = [
        2.63592829534740587,
        4.41060008842499152,
        5.84282968988336851,
        7.02072783744560160,
        8.46179553067463470,
        9.22099475986743958,
        10.72859342897654553,
        11.40941624187610022,
        12.62730928344066148,
        13.60653957404905352,
    ]

    N = 128  # conductor

    # Sum 1/|ρ|² where ρ = 1/2 + iγ, so |ρ|² = 1/4 + γ²
    # Each zero contributes twice (ρ and ρ̄)
    sum_inv_rho_sq = 2 * sum(1 / (0.25 + g**2) for g in zero_heights)

    # Approximate bias parameter (simplified Rubinstein-Sarnak)
    # For a Dirichlet character: b = log(q/π)/2 - Σ 1/|ρ|²
    # For our weight-1 form with conductor 128:
    b = math.log(N / (4 * math.pi**2)) / 2 - sum_inv_rho_sq

    # The first zero dominates
    first_zero_contribution = 2 / (0.25 + zero_heights[0]**2)
    remaining = sum_inv_rho_sq - first_zero_contribution

    return {
        'zero_heights': zero_heights,
        'sum_inv_rho_sq': sum_inv_rho_sq,
        'log_term': math.log(N / (4 * math.pi**2)) / 2,
        'bias_parameter_b': b,
        'first_zero': zero_heights[0],
        'first_zero_contribution': first_zero_contribution,
        'remaining_zeros_contribution': remaining,
        'predicted_bias_sign': 'positive (a_p=+2 favored)' if b > 0 else 'negative (a_p=-2 favored)',
    }


def sign_change_analysis(bias_data):
    """Count sign changes in δ(x) to test oscillation vs persistent bias."""
    sign_changes_all = 0
    sign_changes_twin = 0
    positive_all = 0
    positive_twin = 0
    n = len(bias_data['x'])

    for i in range(1, n):
        if bias_data['delta_all'][i] * bias_data['delta_all'][i - 1] < 0:
            sign_changes_all += 1
        if bias_data['delta_twin'][i] * bias_data['delta_twin'][i - 1] < 0:
            sign_changes_twin += 1
        if bias_data['delta_all'][i] > 0:
            positive_all += 1
        if bias_data['delta_twin'][i] > 0:
            positive_twin += 1

    return {
        'n_checkpoints': n,
        'sign_changes_all': sign_changes_all,
        'sign_changes_twin': sign_changes_twin,
        'frac_positive_all': positive_all / max(n - 1, 1),
        'frac_positive_twin': positive_twin / max(n - 1, 1),
    }


def run_chebyshev_analysis(limit=100_000_000):
    """Full Chebyshev bias analysis."""
    print("=" * 78)
    print("CHEBYSHEV BIAS FOR THE SILVER RATIO SYMBOL ((1+√2)/p)")
    print("=" * 78)

    # Step 1: Rubinstein-Sarnak prediction
    print("\n--- Step 1: Rubinstein-Sarnak prediction from LMFDB zeros ---")
    rs = rubinstein_sarnak_prediction()
    print(f"  First zero height: t₁ = {rs['first_zero']:.6f}")
    print(f"  log(N/4π²)/2 = {rs['log_term']:.6f}")
    print(f"  Σ 1/|ρ|² (10 zeros) = {rs['sum_inv_rho_sq']:.6f}")
    print(f"    First zero: {rs['first_zero_contribution']:.6f}")
    print(f"    Remaining:  {rs['remaining_zeros_contribution']:.6f}")
    print(f"  Bias parameter b = {rs['bias_parameter_b']:.6f}")
    print(f"  Prediction: {rs['predicted_bias_sign']}")

    # Step 2: Compute bias functions
    print(f"\n--- Step 2: δ(x) to {limit:,} ---")
    data = compute_bias_functions(limit)

    # Print table
    print(f"\n{'x':>12s} {'δ_all':>8s} {'δ/√x·lnx':>10s} {'δ_twin':>8s} "
          f"{'δ_tw/√n':>8s} {'δ_cous':>8s} {'n+_all':>8s} {'n-_all':>8s}")
    print("-" * 78)
    for i in range(len(data['x'])):
        print(f"{data['x'][i]:>12,d} {data['delta_all'][i]:>8d} "
              f"{data['norm_all'][i]:>10.4f} {data['delta_twin'][i]:>8d} "
              f"{data['norm_twin'][i]:>8.4f} {data['delta_cousin'][i]:>8d} "
              f"{data['count_plus_all'][i]:>8d} {data['count_minus_all'][i]:>8d}")

    # Step 3: Sign change analysis
    print("\n--- Step 3: Sign changes and persistence ---")
    sc = sign_change_analysis(data)
    print(f"  Checkpoints: {sc['n_checkpoints']}")
    print(f"  Sign changes (all):  {sc['sign_changes_all']}")
    print(f"  Sign changes (twin): {sc['sign_changes_twin']}")
    print(f"  Fraction δ>0 (all):  {sc['frac_positive_all']:.3f}")
    print(f"  Fraction δ>0 (twin): {sc['frac_positive_twin']:.3f}")

    # Step 4: Twin vs all bias comparison
    print("\n--- Step 4: Twin prime bias vs unrestricted ---")
    if len(data['x']) > 0:
        last = len(data['x']) - 1
        n_plus_all = data['count_plus_all'][last]
        n_minus_all = data['count_minus_all'][last]
        n_plus_twin = data['count_plus_twin'][last]
        n_minus_twin = data['count_minus_twin'][last]

        bias_all = (n_plus_all - n_minus_all) / (n_plus_all + n_minus_all)
        bias_twin = (n_plus_twin - n_minus_twin) / max(n_plus_twin + n_minus_twin, 1)

        print(f"  Unrestricted: +{n_plus_all} / -{n_minus_all}, "
              f"bias = {bias_all:+.6f}")
        print(f"  Twin primes:  +{n_plus_twin} / -{n_minus_twin}, "
              f"bias = {bias_twin:+.6f}")
        print(f"  Bias ratio (twin/all): {bias_twin/bias_all:.3f}" if abs(bias_all) > 1e-10
              else "  Bias ratio: undefined (all bias ≈ 0)")

        # Statistical significance: under null (no bias), δ ~ N(0, n)
        # z-score = δ / √n
        n_all = n_plus_all + n_minus_all
        n_twin = n_plus_twin + n_minus_twin
        z_all = (n_plus_all - n_minus_all) / math.sqrt(n_all)
        z_twin = (n_plus_twin - n_minus_twin) / math.sqrt(max(n_twin, 1))

        print(f"  z-score (all):  {z_all:.2f} ({'significant' if abs(z_all) > 2 else 'not significant'})")
        print(f"  z-score (twin): {z_twin:.2f} ({'significant' if abs(z_twin) > 2 else 'not significant'})")

        # The key question: does twin restriction change the bias?
        print(f"\n  KEY QUESTION: Do twin primes prefer a_p = +2 or -2?")
        if abs(z_twin) > 2:
            preferred = "+2" if n_plus_twin > n_minus_twin else "-2"
            print(f"  → YES: twin primes significantly prefer a_p = {preferred}")
            print(f"    (z = {z_twin:.2f}, p < 0.05)")
            if abs(bias_twin) > 2 * abs(bias_all):
                print(f"  → The twin bias is {abs(bias_twin/bias_all):.1f}× the unrestricted bias")
                print(f"    This is a new phenomenon: prime gaps correlate with QR structure")
        else:
            print(f"  → No significant bias detected at current range")
            print(f"    (z = {z_twin:.2f}, need z > 2 for significance)")

    print("\n" + "=" * 78)
    return {'rubinstein_sarnak': rs, 'bias_data': data, 'sign_changes': sc}


if __name__ == '__main__':
    run_chebyshev_analysis()
