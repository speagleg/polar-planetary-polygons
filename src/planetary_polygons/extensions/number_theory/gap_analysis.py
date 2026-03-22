"""
Prime gap analysis with Bolza Hecke eigenvalues: gaps 2, 4, 6, 8, 10, 12.

The anti-correlation a_p ≠ 0 ⟹ a_{p+g} = 0 holds for all g ≢ 0 mod 8.
Gap 8 is the BILATERAL case: both a_p and a_{p+8} can be nonzero,
giving a product weight a_p · a_{p+8} ∈ {+4, -4, 0} with no variance
amplification.

Computes:
- Character sums κ_g for each gap from the Mellin L'/L values
- GPY ratios for each gap (constrained to Hecke-active classes)
- Bilateral correlator statistics for gap 8
- Variance analysis: unilateral (gaps 2,4,6) vs bilateral (gap 8)
"""

import math
from .sieve import primes_up_to
from .arithmetic import hecke_eigenvalue_ap


def character_sums_all_gaps():
    """
    Compute character sums κ_g for gaps g = 2, 4, 6, 8, 10, 12.

    κ_g = Σ_{χ mod 5} χ̄(g) · (L'/L)(1, f⊗χ)

    where g enters through χ̄(g) because the character projection
    extracts primes p with p ≡ -g (mod 5) from the twin/cousin/sexy sum.

    The four (L'/L) values are from the Mellin integral computation.
    """
    import mpmath
    mpmath.mp.dps = 30

    # L'/L values from Mellin integral (definitive computation)
    LpL = [
        mpmath.mpf('0.37734131416980061133'),   # trivial
        mpmath.mpf('-0.20295999827694278395'),   # real (·/5)
        mpmath.mpc('-0.28296445474845743146', '0.20568653972905920547'),  # order 4
        mpmath.mpc('-0.28296445474845743146', '-0.20568653972905920547'),  # conjugate
    ]

    # Character table mod 5: χ_i(n) for n = 1,2,3,4
    # χ₀: {1,1,1,1}, χ₁: {1,-1,-1,1}, χ₂: {1,i,-i,-1}, χ₃: {1,-i,i,-1}
    im = mpmath.mpc(0, 1)
    chi_table = [
        {1: 1, 2: 1, 3: 1, 4: 1},
        {1: 1, 2: -1, 3: -1, 4: 1},
        {1: 1, 2: im, 3: -im, 4: -1},
        {1: 1, 2: -im, 3: im, 4: -1},
    ]

    results = {}

    for g in [2, 4, 6, 8, 10, 12]:
        g_mod5 = g % 5
        if g_mod5 == 0:
            # χ(g) = 0 for non-trivial characters → degenerate
            results[g] = {
                'kappa': None,
                'degenerate': True,
                'reason': f'g = {g} ≡ 0 mod 5: character projection vanishes',
            }
            continue

        # κ_g = Σ_i χ̄_i(g) · LpL_i
        # χ̄(g) = conj(χ(g mod 5))
        kappa = mpmath.mpc(0)
        terms = []
        for i in range(4):
            chi_g = chi_table[i].get(g_mod5, 0)
            chi_bar_g = mpmath.conj(mpmath.mpc(chi_g))
            term = chi_bar_g * LpL[i]
            kappa += term
            terms.append(term)

        kappa_re = float(mpmath.re(kappa))
        kappa_im = float(mpmath.im(kappa))

        results[g] = {
            'kappa': kappa_re,
            'kappa_im': kappa_im,
            'degenerate': False,
            'anti_correlated': (g % 8 != 0),
            'bilateral': (g % 8 == 0),
            'chi_bar_g_values': [str(mpmath.conj(mpmath.mpc(chi_table[i].get(g_mod5, 0)))) for i in range(4)],
        }

    return results


def gap_sieve_analysis(limit=10_000_000):
    """
    For each gap g, compute:
    - Count of prime pairs (p, p+g)
    - Count of Hecke-active pairs (a_p ≠ 0)
    - For bilateral gaps (g ≡ 0 mod 8): count of DOUBLY active (both a_p, a_{p+g} ≠ 0)
    - Anti-correlation verification
    - GPY ratio
    - Variance statistics
    """
    primes = primes_up_to(limit + 20)
    pset = set(primes)
    log_limit = math.log(limit)

    results = {}

    for g in [2, 4, 6, 8, 10, 12]:
        # Find all prime pairs (p, p+g) with p ≤ limit
        pairs = [(p, p + g) for p in primes if p > max(g, 5) and (p + g) in pset and p <= limit]
        total_pairs = len(pairs)

        # Classify by Hecke activity
        unilateral = 0  # a_p ≠ 0, a_{p+g} = 0
        bilateral = 0   # a_p ≠ 0, a_{p+g} ≠ 0
        reverse = 0      # a_p = 0, a_{p+g} ≠ 0
        both_zero = 0    # a_p = 0, a_{p+g} = 0

        # Sign statistics for bilateral pairs
        product_plus = 0   # a_p · a_{p+g} = +4
        product_minus = 0  # a_p · a_{p+g} = -4

        # For GPY: Hecke-active density
        hecke_active_p = 0  # pairs where a_p ≠ 0

        for p, q in pairs:
            ap = hecke_eigenvalue_ap(p)
            aq = hecke_eigenvalue_ap(q)

            if ap != 0 and aq == 0:
                unilateral += 1
            elif ap != 0 and aq != 0:
                bilateral += 1
                if ap * aq > 0:
                    product_plus += 1
                else:
                    product_minus += 1
            elif ap == 0 and aq != 0:
                reverse += 1
            else:
                both_zero += 1

            if ap != 0:
                hecke_active_p += 1

        # Anti-correlation check
        anti_corr_expected = (g % 8 != 0)
        anti_corr_holds = (bilateral == 0) if anti_corr_expected else True

        # GPY ratio: (pair density among Hecke-active) × ln(X)
        # Hecke-active primes: p ≡ 1 mod 8
        all_primes_count = len([p for p in primes if p > max(g, 5) and p <= limit])
        hecke_primes_count = len([p for p in primes if p > max(g, 5) and p <= limit and p % 8 == 1])

        pair_density_all = total_pairs / max(all_primes_count, 1)
        pair_density_hecke = hecke_active_p / max(hecke_primes_count, 1) if hecke_primes_count > 0 else 0

        gpy_all = pair_density_all * log_limit
        gpy_hecke = pair_density_hecke * log_limit

        # For mod-40 restricted classes (the specific Hecke-active classes)
        # Determine which mod-40 classes are active for this gap
        active_classes = []
        for a in range(1, 40):
            if a % 8 != 1:  # p ≡ 1 mod 8
                continue
            if math.gcd(a, 40) != 1:  # p coprime to 40
                continue
            b = (a + g) % 5
            if b == 0:  # p+g not divisible by 5
                continue
            active_classes.append(a)

        mod40_count = sum(1 for p in primes if p > max(g, 5) and p <= limit and (p % 40) in active_classes)
        mod40_pairs = sum(1 for p, q in pairs if (p % 40) in active_classes)
        pair_density_mod40 = mod40_pairs / max(mod40_count, 1)
        gpy_mod40 = pair_density_mod40 * log_limit

        # Variance analysis for bilateral gap
        variance_info = None
        if g % 8 == 0 and bilateral > 0:
            # For bilateral: product weight a_p · a_{p+g} = ±4
            # Mean of product: (product_plus - product_minus) * 4 / bilateral
            # Variance of product: always 16 (magnitude 4, no zero terms among active pairs)
            mean_product = (product_plus - product_minus) * 4.0 / bilateral
            # Compare to unilateral: weight a_p = ±2 or 0
            # Among all pairs, fraction with a_p ≠ 0 = hecke_active_p / total_pairs
            # Variance of unilateral weight: 4 * (hecke fraction) [from a_p² = 4 when active, 0 otherwise]
            hecke_frac = hecke_active_p / max(total_pairs, 1)
            var_unilateral = 4 * hecke_frac  # E[a_p²] over all pairs
            var_bilateral = 16.0  # a_p · a_{p+g} always ±4 for active pairs (no zeros)
            # But bilateral only fires for doubly-active pairs
            doubly_active_frac = bilateral / max(total_pairs, 1)
            var_bilateral_effective = 16 * doubly_active_frac

            variance_info = {
                'product_plus': product_plus,
                'product_minus': product_minus,
                'mean_product': mean_product,
                'sign_bias': (product_plus - product_minus) / max(bilateral, 1),
                'doubly_active_fraction': doubly_active_frac,
                'var_unilateral': var_unilateral,
                'var_bilateral_eff': var_bilateral_effective,
                'var_ratio': var_bilateral_effective / max(var_unilateral, 1e-10),
            }

        results[g] = {
            'gap': g,
            'total_pairs': total_pairs,
            'unilateral': unilateral,
            'bilateral': bilateral,
            'reverse': reverse,
            'both_zero': both_zero,
            'anti_corr_expected': anti_corr_expected,
            'anti_corr_holds': anti_corr_holds,
            'active_classes_mod40': active_classes,
            'n_active_classes': len(active_classes),
            'gpy_all': gpy_all,
            'gpy_hecke': gpy_hecke,
            'gpy_mod40': gpy_mod40,
            'density_ratio': pair_density_mod40 / max(pair_density_all, 1e-10),
            'variance_info': variance_info,
        }

    return results


def run_gap_analysis(limit=10_000_000):
    """Full gap analysis."""
    print("=" * 78)
    print("PRIME GAP ANALYSIS WITH BOLZA HECKE EIGENVALUES")
    print("=" * 78)

    # Character sums
    print("\n--- Character Sums κ_g from Mellin L'/L values ---")
    char_sums = character_sums_all_gaps()
    print(f"{'Gap':>4s} {'κ_g':>12s} {'Anti-corr?':>11s} {'Type':>10s}")
    print("-" * 42)
    for g in [2, 4, 6, 8, 10, 12]:
        cs = char_sums[g]
        if cs['degenerate']:
            print(f"{g:>4d} {'DEGEN':>12s} {'—':>11s} {'—':>10s}")
        else:
            ac = "Yes" if cs['anti_correlated'] else "No"
            tp = "bilateral" if cs['bilateral'] else "unilateral"
            print(f"{g:>4d} {cs['kappa']:>12.6f} {ac:>11s} {tp:>10s}")

    # Sieve analysis
    print(f"\n--- Gap Sieve Analysis (limit = {limit:,}) ---")
    gaps = gap_sieve_analysis(limit)

    print(f"\n{'Gap':>4s} {'Pairs':>8s} {'Uni':>6s} {'Bi':>6s} {'Anti-corr':>10s} "
          f"{'#cls':>5s} {'GPY_all':>8s} {'GPY_mod40':>10s} {'Ratio':>7s}")
    print("-" * 72)
    for g in [2, 4, 6, 8, 10, 12]:
        r = gaps[g]
        ac = "✓" if r['anti_corr_holds'] else "✗ FAIL"
        if not r['anti_corr_expected']:
            ac = "N/A"
        print(f"{g:>4d} {r['total_pairs']:>8d} {r['unilateral']:>6d} {r['bilateral']:>6d} "
              f"{ac:>10s} {r['n_active_classes']:>5d} {r['gpy_all']:>8.3f} "
              f"{r['gpy_mod40']:>10.3f} {r['density_ratio']:>7.3f}")

    # Gap 8 bilateral detail
    print("\n--- Gap 8: Bilateral Correlator ---")
    g8 = gaps[8]
    if g8['bilateral'] > 0:
        vi = g8['variance_info']
        print(f"  Doubly active pairs: {g8['bilateral']}")
        print(f"  Product +4: {vi['product_plus']}, Product -4: {vi['product_minus']}")
        print(f"  Sign bias: {vi['sign_bias']:.4f} (expect ~0)")
        print(f"  Doubly active fraction: {vi['doubly_active_fraction']:.4f}")
        print(f"  Var(unilateral a_p): {vi['var_unilateral']:.4f}")
        print(f"  Var(bilateral a_p·a_{'{p+8}'}): {vi['var_bilateral_eff']:.4f}")
        print(f"  Variance ratio (bi/uni): {vi['var_ratio']:.4f}")
        if vi['var_ratio'] < 1.0:
            print(f"  → BILATERAL HAS LOWER VARIANCE")
        else:
            print(f"  → Bilateral variance is {vi['var_ratio']:.2f}× unilateral")
    else:
        print("  No doubly active pairs found (increase limit)")

    # GPY comparison table
    print("\n--- GPY Ratio Comparison ---")
    print(f"{'Gap':>4s} {'GPY (all)':>10s} {'GPY (Hecke)':>12s} {'Boost':>7s} {'vs parity':>10s}")
    print("-" * 48)
    for g in [2, 4, 6, 8, 10, 12]:
        r = gaps[g]
        boost = r['density_ratio']
        gap_to_parity = 2.0 - r['gpy_mod40']
        parity_pct = f"{(r['gpy_mod40']/2.0)*100:.1f}%"
        print(f"{g:>4d} {r['gpy_all']:>10.3f} {r['gpy_mod40']:>12.3f} "
              f"{boost:>7.3f} {parity_pct:>10s}")

    # The headline question: does gap 8 beat gap 2?
    print("\n--- Headline: Gap 8 vs Gap 2 ---")
    g2 = gaps[2]
    g8 = gaps[8]
    print(f"  Gap 2 GPY (mod 40): {g2['gpy_mod40']:.4f}")
    print(f"  Gap 8 GPY (mod 40): {g8['gpy_mod40']:.4f}")
    if g8['gpy_mod40'] > g2['gpy_mod40']:
        print(f"  → GAP 8 EXCEEDS GAP 2 by {(g8['gpy_mod40']/g2['gpy_mod40'] - 1)*100:.1f}%")
    else:
        print(f"  → Gap 2 remains higher by {(g2['gpy_mod40']/g8['gpy_mod40'] - 1)*100:.1f}%")

    if g8['gpy_mod40'] > 2.0:
        print(f"\n  *** GAP 8 GPY RATIO EXCEEDS PARITY BARRIER ***")
        print(f"  *** This would be a sieve-theoretic result ***")
    elif g8['gpy_mod40'] > 1.92:
        print(f"\n  Gap 8 exceeds twin prime ratio 1.92 — bilateral advantage confirmed")

    print("\n" + "=" * 78)
    return {'char_sums': char_sums, 'gaps': gaps}


if __name__ == '__main__':
    run_gap_analysis()
