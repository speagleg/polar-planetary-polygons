"""
GPY sieve with anti-correlation CONSTRAINT (not weight).

Instead of multiplying by a_p (which amplifies errors), we use the
anti-correlation theorem as a structural constraint:

    a_p ≠ 0  ⟹  a_{p+2} = 0  ⟹  p+2 ≡ 3 mod 8

This fixes the residue class of p+2, reducing the sieve's work.
The question: does this improve the GPY ratio S₁/S₂?

Three testable predictions:
1. Twin prime counts in p ≡ 17 mod 40 converge FASTER to Hardy-Littlewood
   (the Hecke constraint reduces the arithmetic error)
2. The BV-type error term is smaller for the constrained residue class
3. The anti-correlation provides a Chebotarev-type saving beyond mod-8
"""

import math
from .sieve import primes_up_to
from .arithmetic import hecke_eigenvalue_ap


def convergence_rate_comparison(max_limit=100_000_000):
    """
    Compare convergence of twin prime counts to Hardy-Littlewood prediction
    for the constrained (p ≡ 17 mod 40) vs unconstrained case.

    Hardy-Littlewood predicts:
        π₂(x) ~ 2C₂ · x / (ln x)²                     [unconstrained]
        π₂(x; 40, 17) ~ S_{40,17} · x / (ln x)²        [constrained]

    The ERROR TERM determines sieve quality:
        E(x) = |π₂(x) - prediction| / prediction

    If E_constrained(x) < E_unconstrained(x), the Hecke class has
    better convergence.
    """
    C2_narrow = 0.6601618158
    S2 = 2 * C2_narrow  # twin prime constant (standard)

    # S_{40,17} from Bateman-Horn: (10/3) * C2_wide = (10/3) * 2 * C2_narrow
    S_40_17 = (10 / 3) * 2 * C2_narrow  # ≈ 4.401

    results = []

    # Compute at geometrically spaced checkpoints
    checkpoints = []
    x = 10000
    while x <= max_limit:
        checkpoints.append(int(x))
        x *= 2

    primes = primes_up_to(max_limit)
    pset = set(primes)

    # Precompute twin primes and classify
    twins_all = []
    twins_mod40 = []
    for p in primes:
        if p <= 5:
            continue
        if (p + 2) in pset:
            twins_all.append(p)
            if p % 40 == 17:
                twins_mod40.append(p)

    # At each checkpoint, compute counts and errors
    idx_all = 0
    idx_mod40 = 0

    print(f"{'X':>12s} {'π₂(X)':>8s} {'π₂_17':>7s} {'pred_all':>10s} "
          f"{'pred_17':>10s} {'E_all':>8s} {'E_17':>8s} {'ratio':>8s}")
    print("-" * 80)

    for X in checkpoints:
        # Count twins up to X
        while idx_all < len(twins_all) and twins_all[idx_all] <= X:
            idx_all += 1
        while idx_mod40 < len(twins_mod40) and twins_mod40[idx_mod40] <= X:
            idx_mod40 += 1

        count_all = idx_all
        count_mod40 = idx_mod40

        log_X = math.log(X)

        # Hardy-Littlewood predictions
        pred_all = S2 * X / log_X ** 2
        pred_mod40 = S_40_17 * X / (40 * log_X ** 2)
        # Note: the 1/40 accounts for the residue class restriction
        # (density of n ≡ 17 mod 40 among all n)

        # Relative errors
        E_all = abs(count_all - pred_all) / pred_all if pred_all > 0 else 0
        E_mod40 = abs(count_mod40 - pred_mod40) / pred_mod40 if pred_mod40 > 0 else 0

        ratio = E_mod40 / E_all if E_all > 0 else float('inf')

        results.append({
            'X': X, 'count_all': count_all, 'count_mod40': count_mod40,
            'pred_all': pred_all, 'pred_mod40': pred_mod40,
            'E_all': E_all, 'E_mod40': E_mod40, 'ratio': ratio,
        })

        print(f"{X:>12,d} {count_all:>8d} {count_mod40:>7d} {pred_all:>10.1f} "
              f"{pred_mod40:>10.1f} {E_all:>8.4f} {E_mod40:>8.4f} {ratio:>8.4f}")

    return results


def bv_error_comparison(limit=10_000_000):
    """
    Compare Barban-Davenport-Halberstam type errors for constrained
    vs unconstrained twin prime counts in arithmetic progressions.

    BDH theorem: Σ_{q≤Q} Σ_{a mod q, (a,q)=1} |π₂(x;q,a) - pred|² ≪ x²/(log x)^A

    Compute this sum empirically for:
    1. All (q, a) pairs [unconstrained]
    2. Only (q, a) with a ≡ 17 mod gcd(q, 40) [constrained by Hecke]
    """
    primes = primes_up_to(limit)
    pset = set(primes)

    # Find all twins
    twins = [(p, p + 2) for p in primes if p > 5 and (p + 2) in pset]
    total_twins = len(twins)

    max_q = 50
    log_limit = math.log(limit)

    # For each modulus q, compute the BDH error
    bdh_unconstrained = 0.0
    bdh_constrained = 0.0
    n_classes_unconstrained = 0
    n_classes_constrained = 0

    for q in range(3, max_q + 1):
        # Count twins in each residue class
        counts = {}
        for p, p2 in twins:
            a = p % q
            counts[a] = counts.get(a, 0) + 1

        # Expected count per class
        # π₂(x; q, a) ~ S₂(q,a) · x / (φ(q) · (log x)²)
        # For simplicity, use the average: total_twins / φ(q)
        phi_q = sum(1 for a in range(q) if math.gcd(a, q) == 1)
        if phi_q == 0:
            continue

        expected = total_twins / phi_q

        for a in range(q):
            if math.gcd(a, q) != 1:
                continue

            actual = counts.get(a, 0)
            error_sq = (actual - expected) ** 2

            # Unconstrained: all classes
            bdh_unconstrained += error_sq
            n_classes_unconstrained += 1

            # Constrained: only classes compatible with a ≡ 17 mod gcd(q, 40)
            g = math.gcd(q, 40)
            if a % g == 17 % g:
                bdh_constrained += error_sq
                n_classes_constrained += 1

    # Normalize by number of classes
    avg_unconstrained = bdh_unconstrained / max(n_classes_unconstrained, 1)
    avg_constrained = bdh_constrained / max(n_classes_constrained, 1)

    return {
        'bdh_unconstrained': bdh_unconstrained,
        'bdh_constrained': bdh_constrained,
        'n_classes_unconstrained': n_classes_unconstrained,
        'n_classes_constrained': n_classes_constrained,
        'avg_error_unconstrained': avg_unconstrained,
        'avg_error_constrained': avg_constrained,
        'ratio': avg_constrained / avg_unconstrained if avg_unconstrained > 0 else 0,
    }


def chebotarev_advantage(limit=10_000_000):
    """
    Test whether the D₄ Galois structure provides a sieve advantage
    BEYOND the mod-8 congruence.

    The anti-correlation says a_p ≠ 0 ⟹ a_{p+2} = 0. At the mod-8 level:
    p ≡ 1 mod 8 ⟹ p+2 ≡ 3 mod 8. This is just congruence arithmetic.

    But a_p encodes MORE than mod 8: it gives the Legendre symbol
    ((1+√2)/p), which depends on the splitting of p in Q(√2, √(-2)).
    The sign of a_p (±2) carries information about the Frobenius
    at p in this number field.

    Test: does sign(a_p) correlate with properties of p+2 beyond
    what mod-8 congruence predicts?

    Specifically: among twin primes (p, p+2) with p ≡ 17 mod 40,
    is the distribution of p+2 mod 24 (or mod 120, etc.) different
    for a_p = +2 vs a_p = -2?
    """
    primes = primes_up_to(limit)
    pset = set(primes)

    # Qualifying twins: p ≡ 17 mod 40, (p, p+2) both prime
    twins_plus = []  # a_p = +2
    twins_minus = []  # a_p = -2

    for p in primes:
        if p <= 5 or p % 40 != 17:
            continue
        if (p + 2) not in pset:
            continue
        ap = hecke_eigenvalue_ap(p)
        if ap == 2:
            twins_plus.append(p)
        elif ap == -2:
            twins_minus.append(p)

    # Distribution of p+2 modulo various q for + vs - twins
    results = {}
    for q in [3, 8, 12, 24, 40, 120]:
        dist_plus = {}
        dist_minus = {}

        for p in twins_plus:
            r = (p + 2) % q
            dist_plus[r] = dist_plus.get(r, 0) + 1
        for p in twins_minus:
            r = (p + 2) % q
            dist_minus[r] = dist_minus.get(r, 0) + 1

        # Chi-squared test for independence of sign and p+2 mod q
        all_residues = sorted(set(list(dist_plus.keys()) + list(dist_minus.keys())))
        n_plus = len(twins_plus)
        n_minus = len(twins_minus)
        n_total = n_plus + n_minus

        chi_sq = 0.0
        for r in all_residues:
            o_plus = dist_plus.get(r, 0)
            o_minus = dist_minus.get(r, 0)
            o_total = o_plus + o_minus
            if o_total == 0:
                continue
            e_plus = n_plus * o_total / n_total
            e_minus = n_minus * o_total / n_total
            if e_plus > 0:
                chi_sq += (o_plus - e_plus) ** 2 / e_plus
            if e_minus > 0:
                chi_sq += (o_minus - e_minus) ** 2 / e_minus

        df = max(len(all_residues) - 1, 1)
        results[q] = {
            'chi_sq': chi_sq,
            'df': df,
            'chi_sq_per_df': chi_sq / df,
            'n_residues': len(all_residues),
            'significant': chi_sq / df > 2.0,  # rough threshold
        }

    return {
        'n_plus': len(twins_plus),
        'n_minus': len(twins_minus),
        'sign_ratio': len(twins_plus) / max(len(twins_minus), 1),
        'mod_tests': results,
    }


def constrained_gpy_ratio(limit=10_000_000):
    """
    Compute the GPY ratio S₁/S₂ for the constrained case and compare
    to the unconstrained case.

    The GPY ratio determines whether the sieve can detect twin primes:
    if S₁ > 2·S₂, twins exist in the range.

    For the constrained case (p ≡ 17 mod 40):
    - Main term S₁' involves S_{40,17} (the restricted singular series)
    - Diagonal term S₂' involves 1/φ(40) (the class density)
    - The anti-correlation CONSTRAINS p+2 ≡ 3 mod 8 for free

    The "free sieve" from the anti-correlation means the sieve only
    needs to enforce primality of p+2 among {m : m ≡ 3 mod 8},
    not among all integers. This reduces the effective φ(q) in the
    BV error by a factor involving the density of primes ≡ 3 mod 8.
    """
    C2_narrow = 0.6601618158
    S2_standard = 2 * C2_narrow  # ≈ 1.320

    # For the constrained case:
    # The "effective singular series" accounts for the residue class restriction
    # AND the free information from the anti-correlation.

    # Without anti-correlation: standard S₂ for p ≡ 17 mod 40
    # This is just S_{40,17} / φ(40) ≈ 4.401 / 16 ≈ 0.275

    # With anti-correlation: we know p+2 ≡ 3 mod 8.
    # The standard sieve for "p+2 prime" needs to eliminate composites.
    # The sieve works by removing multiples of small primes.
    # Knowing p+2 ≡ 3 mod 8 means:
    #   - p+2 is odd (free from mod 8)
    #   - p+2 ≢ 0 mod 4 (free from mod 8)
    #   - The sieve only starts at q = 3

    # The saving: in the standard sieve, the q=2 contribution to the
    # Selberg sieve is significant. Removing it saves a factor.

    # Quantify: the Selberg sieve gives
    # #{n ≤ x : n ≡ a mod q, n prime} ≤ (2 + o(1)) · x / (φ(q) · ln(x/q))
    # The "2" is the Selberg constant, which comes from Σ 1/φ(d) over d|q.
    # Removing the d=2 factor gives a saving of (1 - 1/(φ(2)·2)) = 1 - 1/2 = 1/2.

    # More precisely: the Selberg upper bound sieve for primes in [1, x] gives
    # an upper bound of 2x/ln(x) (the "2" is the sieve constant).
    # For primes ≡ 3 mod 8 in [1, x]: upper bound 2x/(φ(8)·ln(x)) = x/(2·ln(x)).
    # For primes in [1, x] without congruence restriction: 2x/ln(x).
    # The ratio is φ(8)/2 = 2. So the constrained case is "easier" by factor 2
    # in the sieve upper bound.

    # But this factor 2 is already accounted for in the singular series!
    # The real question: does the anti-correlation give ADDITIONAL information
    # beyond the congruence p+2 ≡ 3 mod 8?

    # The answer depends on whether a_p = ±2 correlates with p+2 mod q
    # for q > 8. If it does, the anti-correlation carries Chebotarev information.
    # If not, it's just the mod-8 congruence.

    # Empirical test: compute the constrained GPY ratio
    primes = primes_up_to(limit)
    pset = set(primes)

    # Count: primes p ≡ 17 mod 40 with p+2 prime
    twins_constrained = sum(1 for p in primes
                           if p > 5 and p % 40 == 17 and (p + 2) in pset)
    primes_constrained = sum(1 for p in primes if p > 5 and p % 40 == 17)

    # Count: all twin primes
    twins_all = sum(1 for p in primes if p > 5 and (p + 2) in pset)
    primes_all = len(primes) - 3  # exclude 2, 3, 5

    log_limit = math.log(limit)

    # Empirical "GPY ratio" ≈ (twin density) × ln(x)
    # This measures how far we are from the GPY threshold
    gpy_all = (twins_all / primes_all) * log_limit
    gpy_constrained = (twins_constrained / primes_constrained) * log_limit

    return {
        'limit': limit,
        'twins_all': twins_all,
        'primes_all': primes_all,
        'twin_density_all': twins_all / primes_all,
        'twins_constrained': twins_constrained,
        'primes_constrained': primes_constrained,
        'twin_density_constrained': twins_constrained / primes_constrained,
        'gpy_ratio_all': gpy_all,
        'gpy_ratio_constrained': gpy_constrained,
        'ratio_improvement': gpy_constrained / gpy_all,
        'S2_standard': S2_standard,
    }


def run_constrained_analysis(limit=10_000_000):
    """Full constrained GPY analysis."""
    print("=" * 72)
    print("GPY WITH ANTI-CORRELATION CONSTRAINT")
    print("=" * 72)

    # Step 1: Convergence rate comparison
    print("\n--- Step 1: Convergence to Hardy-Littlewood ---")
    convergence_rate_comparison(limit)

    # Step 2: BDH error comparison
    print("\n--- Step 2: Barban-Davenport-Halberstam errors ---")
    bdh = bv_error_comparison(limit)
    print(f"  Unconstrained: avg error² = {bdh['avg_error_unconstrained']:.2f} "
          f"({bdh['n_classes_unconstrained']} classes)")
    print(f"  Constrained:   avg error² = {bdh['avg_error_constrained']:.2f} "
          f"({bdh['n_classes_constrained']} classes)")
    print(f"  Ratio (constrained/unconstrained): {bdh['ratio']:.4f}")
    print(f"  → {'LOWER' if bdh['ratio'] < 1 else 'HIGHER'} error in constrained case")

    # Step 3: Chebotarev advantage
    print("\n--- Step 3: Chebotarev (beyond mod-8) ---")
    cheb = chebotarev_advantage(limit)
    print(f"  Twins with a_p = +2: {cheb['n_plus']}")
    print(f"  Twins with a_p = -2: {cheb['n_minus']}")
    print(f"  Sign ratio: {cheb['sign_ratio']:.4f} (expect ~1)")
    print()
    print(f"  Chi-squared independence tests (sign vs p+2 mod q):")
    print(f"  {'q':>5s} {'χ²/df':>8s} {'significant?':>14s}")
    for q, data in sorted(cheb['mod_tests'].items()):
        sig = "YES ***" if data['significant'] else "no"
        print(f"  {q:>5d} {data['chi_sq_per_df']:>8.3f} {sig:>14s}")

    # Step 4: GPY ratio
    print("\n--- Step 4: Constrained GPY ratio ---")
    gpy = constrained_gpy_ratio(limit)
    print(f"  Twin density (all):         {gpy['twin_density_all']:.6f}")
    print(f"  Twin density (p≡17 mod 40): {gpy['twin_density_constrained']:.6f}")
    print(f"  GPY ratio (all):            {gpy['gpy_ratio_all']:.4f}")
    print(f"  GPY ratio (constrained):    {gpy['gpy_ratio_constrained']:.4f}")
    print(f"  Improvement factor:         {gpy['ratio_improvement']:.4f}")
    print(f"  → Constrained class is {gpy['ratio_improvement']:.1%} of unconstrained")

    # Step 5: Interpretation
    print("\n--- Step 5: Interpretation ---")
    if cheb['mod_tests'].get(24, {}).get('significant', False):
        print("  *** CHEBOTAREV ADVANTAGE DETECTED ***")
        print("  The sign of a_p correlates with p+2 mod 24 (or higher),")
        print("  meaning the D₄ structure provides information BEYOND mod-8.")
        print("  This is genuine automorphic sieve power.")
    else:
        print("  No Chebotarev advantage beyond mod-8 congruence.")
        print("  The anti-correlation is fully explained by:")
        print("    p ≡ 1 mod 8 ⟹ p+2 ≡ 3 mod 8")
        print("  The D₄ structure does not provide additional sieve power")
        print("  beyond this congruence condition.")

    if bdh['ratio'] < 0.8:
        print(f"\n  BDH error ratio {bdh['ratio']:.3f}: constrained class has")
        print("  significantly lower arithmetic error. This improves the")
        print("  effective BV exponent.")
    elif bdh['ratio'] < 1.0:
        print(f"\n  BDH error ratio {bdh['ratio']:.3f}: modest improvement")
        print("  in constrained class. Constant-factor gain only.")
    else:
        print(f"\n  BDH error ratio {bdh['ratio']:.3f}: no improvement from constraint.")

    print("\n" + "=" * 72)
    return {'convergence': None, 'bdh': bdh, 'chebotarev': cheb, 'gpy': gpy}


if __name__ == '__main__':
    run_constrained_analysis()
