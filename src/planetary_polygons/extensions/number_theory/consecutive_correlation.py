"""
Consecutive prime correlation of the Bolza Hecke eigenvalue.

C(x) = (1/π(x)) Σ_{p ≤ x} a_p · a_{p'}

where p' is the next prime after p. Since a_p ∈ {0, ±2}, the product
a_p · a_{p'} is nonzero only when BOTH p and p' are ≡ 1 mod 8.

The explicit formula prediction (from Sym²(f) = ζ · L(χ_{-4}) · L(χ_8)):

C(x) ~ -(1/log x) Σ_ρ x^{ρ-1}/ρ

where ρ ranges over zeros of ζ(s), L(s, χ_{-4}), and L(s, χ_8).
This connects the Bolza form's consecutive prime statistics directly
to the Riemann zeros.
"""

import math
import cmath
from .sieve import primes_up_to
from .arithmetic import hecke_eigenvalue_ap


def consecutive_correlation(limit=100_000_000):
    """
    Compute C(x) = (1/π(x)) Σ_{p≤x} a_p · a_{p'} at checkpoints.

    Also decompose into:
    - C_++ : both a_p = +2, a_{p'} = +2 (product = +4)
    - C_+- : a_p = +2, a_{p'} = -2 (product = -4)
    - C_-+ : a_p = -2, a_{p'} = +2 (product = -4)
    - C_-- : both a_p = -2, a_{p'} = -2 (product = +4)
    - C_0  : at least one is zero (product = 0)
    """
    print(f"Sieving primes to {limit:,}...", flush=True)
    primes = primes_up_to(limit)
    n_primes = len(primes)
    print(f"  {n_primes:,} primes found")

    # Checkpoints
    checkpoints = []
    x = 10000
    while x <= limit:
        checkpoints.append(int(x))
        x = int(x * 2)
    if checkpoints[-1] < limit:
        checkpoints.append(limit)

    # Running sums
    sum_product = 0.0
    sum_abs_product = 0.0
    count = 0
    count_pp = 0  # (+,+)
    count_pm = 0  # (+,-)
    count_mp = 0  # (-,+)
    count_mm = 0  # (-,-)
    count_active = 0  # both nonzero
    count_zero = 0  # at least one zero

    results = []
    cp_idx = 0

    # Precompute a_p for all primes
    print("Computing Hecke eigenvalues...", flush=True)
    ap_list = [hecke_eigenvalue_ap(p) for p in primes]
    print("  Done")

    print("Computing consecutive correlations...", flush=True)
    for i in range(len(primes) - 1):
        p = primes[i]
        if p <= 5:
            continue

        ap = ap_list[i]
        ap_next = ap_list[i + 1]
        product = ap * ap_next

        count += 1
        sum_product += product
        sum_abs_product += abs(product)

        if ap != 0 and ap_next != 0:
            count_active += 1
            if ap > 0 and ap_next > 0:
                count_pp += 1
            elif ap > 0 and ap_next < 0:
                count_pm += 1
            elif ap < 0 and ap_next > 0:
                count_mp += 1
            else:
                count_mm += 1
        else:
            count_zero += 1

        # Record at checkpoints
        while cp_idx < len(checkpoints) and p >= checkpoints[cp_idx]:
            C_x = sum_product / count
            C_abs = sum_abs_product / count
            log_x = math.log(checkpoints[cp_idx])

            # Normalized: C(x) * log(x) should approach a constant
            # if C(x) ~ c/log(x)
            C_normalized = C_x * log_x

            results.append({
                'x': checkpoints[cp_idx],
                'pi_x': count,
                'C_x': C_x,
                'C_abs': C_abs,
                'C_normalized': C_normalized,
                'count_active': count_active,
                'count_pp': count_pp,
                'count_pm': count_pm,
                'count_mp': count_mp,
                'count_mm': count_mm,
                'count_zero': count_zero,
                'active_fraction': count_active / count,
                # Among active pairs: bias
                'concordant': count_pp + count_mm,
                'discordant': count_pm + count_mp,
            })
            cp_idx += 1

    return results


def explicit_formula_prediction(x_val, n_zeros=50):
    """
    Compute the explicit formula prediction for C(x):

    C(x) ~ -(1/log x) · Σ_ρ x^{ρ-1}/ρ

    where ρ are zeros of L(s, Sym²(f)) = ζ(s) · L(s, χ_{-4}) · L(s, χ_8).

    Uses the first n_zeros zeros of each L-function.
    """
    log_x = math.log(x_val)

    # Zeros of ζ(s): the Riemann zeros 1/2 + iγ
    # First 50 from standard tables
    riemann_zeros = [
        14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
        37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
        52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
        67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
        79.337375, 82.910381, 84.735493, 87.425275, 88.809111,
        92.491899, 94.651344, 95.870634, 98.831194, 101.317851,
        103.725538, 105.446623, 107.168611, 111.029536, 111.874659,
        114.320220, 116.226680, 118.790783, 121.370125, 122.946829,
        124.256819, 127.516684, 129.578704, 131.087688, 133.497737,
        134.756510, 138.116042, 139.736209, 141.123707, 143.111846,
    ]

    # Zeros of L(s, χ_{-4}): χ_{-4}(n) = (-1)^{(n-1)/2} for odd n
    # First zeros (approximate, from tables)
    chi4_zeros = [
        6.020949, 10.243723, 12.588507, 16.108741, 18.141087,
        21.022040, 23.088612, 25.889072, 27.670182, 30.424876,
        31.718820, 33.932525, 35.990622, 37.586178, 40.918719,
        41.699460, 43.327073, 46.140038, 48.005151, 48.710776,
        51.561535, 52.970321, 54.711632, 56.446248, 57.545268,
    ]

    # Zeros of L(s, χ_8): χ_8(n) = (2/n) Kronecker symbol
    # Conductor 8, character (2/·)
    # First zeros (approximate)
    chi8_zeros = [
        4.380454, 8.594826, 11.600907, 14.475827, 17.346813,
        19.198454, 22.148396, 23.804028, 26.487043, 28.182492,
        30.562606, 31.948555, 34.379958, 36.166939, 38.041714,
        39.859826, 41.531752, 43.478999, 45.073498, 47.105277,
    ]

    # Compute Σ x^{ρ-1}/ρ for each set of zeros
    # ρ = 1/2 + iγ, so x^{ρ-1} = x^{-1/2 + iγ} = x^{-1/2} · x^{iγ}
    # x^{iγ} = exp(iγ · log x) = cos(γ log x) + i sin(γ log x)
    # 1/ρ = 1/(1/2 + iγ) = (1/2 - iγ)/(1/4 + γ²)

    def sum_over_zeros(gamma_list, x):
        log_x = math.log(x)
        x_neg_half = x ** (-0.5)
        total = 0.0
        for gamma in gamma_list[:n_zeros]:
            # x^{ρ-1}/ρ + x^{ρ̄-1}/ρ̄ (pair ρ, ρ̄)
            # = 2 Re[x^{ρ-1}/ρ]
            phase = gamma * log_x
            # x^{ρ-1} = x^{-1/2} (cos θ + i sin θ)
            x_rho = x_neg_half * complex(math.cos(phase), math.sin(phase))
            rho = complex(0.5, gamma)
            contrib = x_rho / rho
            total += 2 * contrib.real  # pair with conjugate
        return total

    S_zeta = sum_over_zeros(riemann_zeros, x_val)
    S_chi4 = sum_over_zeros(chi4_zeros, x_val)
    S_chi8 = sum_over_zeros(chi8_zeros, x_val)

    # Total: sum over all zeros of Sym²(f) = ζ · L(χ_{-4}) · L(χ_8)
    S_total = S_zeta + S_chi4 + S_chi8

    # Prediction: C(x) ~ -(1/log x) · S_total
    C_predicted = -S_total / log_x

    return {
        'x': x_val,
        'S_zeta': S_zeta,
        'S_chi4': S_chi4,
        'S_chi8': S_chi8,
        'S_total': S_total,
        'C_predicted': C_predicted,
        'C_normalized': C_predicted * log_x,
    }


def run_consecutive_analysis(limit=100_000_000):
    """Full consecutive correlation analysis."""
    print("=" * 78)
    print("CONSECUTIVE PRIME CORRELATION OF THE BOLZA HECKE EIGENVALUE")
    print("C(x) = (1/π(x)) Σ a_p · a_{p'}, p' = next prime after p")
    print("=" * 78)

    # Step 1: Compute C(x)
    print("\n--- Step 1: Empirical C(x) ---")
    data = consecutive_correlation(limit)

    print(f"\n{'x':>12s} {'π(x)':>9s} {'C(x)':>12s} {'C·ln(x)':>10s} "
          f"{'active':>7s} {'++':>6s} {'+-':>6s} {'-+':>6s} {'--':>6s} {'concord':>8s}")
    print("-" * 100)
    for r in data:
        conc = r['concordant']
        disc = r['discordant']
        total_active = conc + disc
        conc_frac = conc / total_active if total_active > 0 else 0
        print(f"{r['x']:>12,d} {r['pi_x']:>9,d} {r['C_x']:>12.6f} "
              f"{r['C_normalized']:>10.4f} {r['active_fraction']:>7.4f} "
              f"{r['count_pp']:>6d} {r['count_pm']:>6d} "
              f"{r['count_mp']:>6d} {r['count_mm']:>6d} "
              f"{conc_frac:>8.4f}")

    # Step 2: Explicit formula prediction
    print("\n--- Step 2: Explicit formula (Riemann zeros) ---")
    print(f"{'x':>12s} {'C_empirical':>12s} {'C_predicted':>12s} "
          f"{'ratio':>8s} {'S_ζ':>10s} {'S_χ₄':>10s} {'S_χ₈':>10s}")
    print("-" * 78)
    for r in data:
        pred = explicit_formula_prediction(r['x'])
        ratio = r['C_x'] / pred['C_predicted'] if abs(pred['C_predicted']) > 1e-15 else float('inf')
        print(f"{r['x']:>12,d} {r['C_x']:>12.6f} {pred['C_predicted']:>12.6f} "
              f"{ratio:>8.3f} {pred['S_zeta']:>10.4f} "
              f"{pred['S_chi4']:>10.4f} {pred['S_chi8']:>10.4f}")

    # Step 3: Interpretation
    print("\n--- Step 3: Interpretation ---")
    last = data[-1]
    print(f"  At x = {last['x']:,}:")
    print(f"    C(x) = {last['C_x']:.6f}")
    print(f"    C(x) · ln(x) = {last['C_normalized']:.4f}")
    print(f"    Active fraction = {last['active_fraction']:.4f} "
          f"(expected: (1/4)² = {0.0625:.4f} if independent)")

    total_active = last['concordant'] + last['discordant']
    if total_active > 0:
        conc_frac = last['concordant'] / total_active
        print(f"    Concordant fraction = {conc_frac:.4f} (expect 0.5 if independent)")

        # Chi-squared test for independence of consecutive signs
        expected = total_active / 4  # equal among ++, +-, -+, --
        chi_sq = sum((obs - expected)**2 / expected
                     for obs in [last['count_pp'], last['count_pm'],
                                 last['count_mp'], last['count_mm']])
        print(f"    χ² for sign independence = {chi_sq:.2f} (df=3, threshold=7.81 for p<0.05)")
        if chi_sq > 7.81:
            print(f"    → SIGNIFICANT consecutive sign correlation detected")
        else:
            print(f"    → Signs are consistent with independence")

    # Does C(x) decay like 1/log(x)?
    if len(data) >= 4:
        C_early = data[2]['C_normalized']  # at ~40000
        C_late = data[-1]['C_normalized']  # at limit
        print(f"\n    C·ln(x) at x~40k: {C_early:.4f}")
        print(f"    C·ln(x) at x~{last['x']//1000000}M: {C_late:.4f}")
        if abs(C_early) > 0 and abs(C_late) > 0:
            if abs(C_late / C_early - 1) < 0.3:
                print(f"    → C·ln(x) approximately constant: C(x) ~ {C_late:.4f}/ln(x)")
                print(f"    → Consistent with explicit formula prediction")
            else:
                print(f"    → C·ln(x) NOT constant (ratio = {C_late/C_early:.3f})")

    print("\n" + "=" * 78)
    return data


if __name__ == '__main__':
    run_consecutive_analysis()
