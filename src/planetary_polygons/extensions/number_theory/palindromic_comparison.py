"""
Comparison of palindromic forms as prime gap probes.

Five palindromic polynomials from the vortex stability hierarchy,
each associated to a number field and a Hecke-active congruence:

  D=7 (N=8):  Q(√(-7))     (7/p)=1  ↔  p ≡ 1,2,4 mod 7
  D=6 (N=9):  Q(√(-3))     (3/p)=1  ↔  p ≡ 1 mod 3
  D=2 (N=11): Q(√2,√(-2))  Bolza    ↔  p ≡ 1 mod 8
  D=3 (N=15): Q(√(-3))     (-3/p)=1 ↔  p ≡ 1 mod 3
  D=5 (N=23): Q(√5)        (5/p)=1  ↔  p ≡ ±1 mod 5

For twin primes (p, p+2), the anti-correlation holds when the
Hecke condition on p forces p+2 OUT of the active class.

The key computation: for each form, find the optimal residue class
for twin primes and compute the GPY ratio. Then compare to an
exhaustive search over ALL mod-q classes to see if the palindromic
forms actually find the best classes.
"""

import math
from .sieve import primes_up_to
from .arithmetic import legendre_symbol


def exhaustive_gpy_search(limit=10_000_000, max_q=120):
    """
    Search ALL congruence classes mod q for the one with the highest
    twin prime GPY ratio.

    For each q from 3 to max_q, for each a coprime to q:
    - Count twin primes (p, p+2) with p ≡ a mod q
    - Count primes p ≡ a mod q
    - Compute GPY ratio = (twin density) × ln(limit)

    Returns the top classes ranked by GPY ratio.
    """
    primes = primes_up_to(limit + 2)
    pset = set(primes)
    log_limit = math.log(limit)

    # Count twins and primes in each class
    results = []

    for q in range(3, max_q + 1):
        for a in range(q):
            if math.gcd(a, q) != 1:
                continue

            n_primes = 0
            n_twins = 0

            for p in primes:
                if p <= max(5, q) or p > limit:
                    continue
                if p % q != a:
                    continue
                n_primes += 1
                if (p + 2) in pset:
                    n_twins += 1

            if n_primes < 10:
                continue

            density = n_twins / n_primes
            gpy = density * log_limit
            activation = n_primes / len([p for p in primes if p > max(5, q) and p <= limit])

            results.append({
                'q': q, 'a': a,
                'n_primes': n_primes, 'n_twins': n_twins,
                'density': density, 'gpy': gpy,
                'activation': activation,
                'class': f"p ≡ {a} mod {q}",
            })

    results.sort(key=lambda x: -x['gpy'])
    return results


def palindromic_form_analysis(limit=10_000_000):
    """
    For each palindromic form, determine:
    1. Hecke-active condition
    2. Anti-correlation for twin primes
    3. Optimal twin prime class
    4. GPY ratio
    5. Activation density
    """
    primes = primes_up_to(limit + 2)
    pset = set(primes)
    primes_gt5 = [p for p in primes if p > 5 and p <= limit]
    total_primes = len(primes_gt5)
    log_limit = math.log(limit)

    # Count all twins
    all_twins = sum(1 for p in primes_gt5 if (p + 2) in pset)
    all_density = all_twins / total_primes
    gpy_baseline = all_density * log_limit

    forms = {}

    # ============================================================
    # Form 1: D=2, Bolza (N=11 threshold)
    # Field: Q(√2, √(-2)), Galois D₄
    # Hecke: p ≡ 1 mod 8
    # Anti-corr for twins: p ≡ 1 mod 8 → p+2 ≡ 3 mod 8 → YES
    # ============================================================
    cond = lambda p: p % 8 == 1
    active_primes = [p for p in primes_gt5 if cond(p)]
    active_twins = [p for p in active_primes if (p + 2) in pset]

    # Further restrict to mod-40 class
    # p ≡ 1 mod 8 AND p ≡ 2 mod 5 (so (5/p)=-1): p ≡ 17 mod 40
    mod40_primes = [p for p in active_primes if p % 40 == 17]
    mod40_twins = [p for p in mod40_primes if (p + 2) in pset]

    forms['Bolza (D=2)'] = {
        'field': 'Q(√2, √(-2))',
        'galois': 'D₄',
        'hecke_cond': 'p ≡ 1 mod 8',
        'activation': len(active_primes) / total_primes,
        'anti_corr_twins': True,
        'n_active': len(active_primes),
        'n_active_twins': len(active_twins),
        'gpy_active': (len(active_twins) / len(active_primes)) * log_limit if active_primes else 0,
        'best_class': 'p ≡ 17 mod 40',
        'n_best': len(mod40_primes),
        'n_best_twins': len(mod40_twins),
        'gpy_best': (len(mod40_twins) / len(mod40_primes)) * log_limit if mod40_primes else 0,
    }

    # ============================================================
    # Form 2: D=5, Golden Ratio (N=23 threshold)
    # Field: Q(√5)
    # Hecke: (5/p) = 1, i.e., p ≡ 1 or 4 mod 5
    # Anti-corr for twins:
    #   p ≡ 1 mod 5 → p+2 ≡ 3 mod 5 → (5/3)=-1 → YES
    #   p ≡ 4 mod 5 → p+2 ≡ 1 mod 5 → (5/1)=1 → NO
    # PARTIAL anti-correlation
    # ============================================================
    cond = lambda p: legendre_symbol(5, p) == 1  # p ≡ 1, 4 mod 5
    active_primes = [p for p in primes_gt5 if p % 5 in (1, 4)]
    active_twins = [p for p in active_primes if (p + 2) in pset]

    # Subclass with full anti-corr: p ≡ 1 mod 5 (not p ≡ 4 mod 5)
    sub1_primes = [p for p in primes_gt5 if p % 5 == 1]
    sub1_twins = [p for p in sub1_primes if (p + 2) in pset]
    # Combined with mod-8 for maximum concentration
    # p ≡ 1 mod 5 AND p ≡ 1 mod 8 → p ≡ 1 mod 40
    best_primes = [p for p in primes_gt5 if p % 40 == 1]
    best_twins = [p for p in best_primes if (p + 2) in pset]

    # Also try: p ≡ 1 mod 5 AND p ≡ 1 mod 4 → p ≡ 1 mod 20
    alt_primes = [p for p in primes_gt5 if p % 20 == 1]
    alt_twins = [p for p in alt_primes if (p + 2) in pset]

    forms['Golden (D=5)'] = {
        'field': 'Q(√5)',
        'galois': 'Z/2',
        'hecke_cond': '(5/p) = 1, p ≡ 1,4 mod 5',
        'activation': len(active_primes) / total_primes,
        'anti_corr_twins': 'Partial (p≡1 mod 5 yes, p≡4 mod 5 no)',
        'n_active': len(active_primes),
        'n_active_twins': len(active_twins),
        'gpy_active': (len(active_twins) / len(active_primes)) * log_limit if active_primes else 0,
        'best_class': 'p ≡ 1 mod 40',
        'n_best': len(best_primes),
        'n_best_twins': len(best_twins),
        'gpy_best': (len(best_twins) / len(best_primes)) * log_limit if best_primes else 0,
        'alt_class': 'p ≡ 1 mod 20',
        'n_alt': len(alt_primes),
        'n_alt_twins': len(alt_twins),
        'gpy_alt': (len(alt_twins) / len(alt_primes)) * log_limit if alt_primes else 0,
    }

    # ============================================================
    # Form 3: D=6 (N=9 threshold)
    # Field: Q(√(-3)) = Q(ζ₃)
    # Hecke: (-3/p) = 1, i.e., p ≡ 1 mod 3
    # Anti-corr for twins: p ≡ 1 mod 3 → p+2 ≡ 0 mod 3
    # → p+2 divisible by 3 → NOT PRIME (unless p+2=3, i.e., p=1)
    # TOTAL KILL: NO twin primes possible
    # ============================================================
    active_primes = [p for p in primes_gt5 if p % 3 == 1]
    active_twins = [p for p in active_primes if (p + 2) in pset]
    # Should be 0 (p+2 ≡ 0 mod 3)

    # But this form CAN see cousin primes (gap 4):
    active_cousins = [p for p in active_primes if (p + 4) in pset]
    # p ≡ 1 mod 3, p+4 ≡ 2 mod 3 → coprime to 3 → OK
    cousin_all = sum(1 for p in primes_gt5 if (p + 4) in pset)

    forms['Eisenstein (D=6)'] = {
        'field': 'Q(√(-3))',
        'galois': 'Z/2',
        'hecke_cond': 'p ≡ 1 mod 3',
        'activation': len(active_primes) / total_primes,
        'anti_corr_twins': 'TOTAL — no twin primes possible (p+2 ≡ 0 mod 3)',
        'n_active': len(active_primes),
        'n_active_twins': len(active_twins),
        'gpy_active': 0,
        'note': f'But sees {len(active_cousins)} cousin primes (gap 4)',
        'cousin_gpy': (len(active_cousins) / len(active_primes)) * log_limit if active_primes else 0,
        'cousin_density_ratio': (len(active_cousins) / len(active_primes)) / (cousin_all / total_primes) if cousin_all > 0 else 0,
    }

    # ============================================================
    # Form 4: D=3 (N=15 threshold)
    # Also involves Q(√(-3)) — similar to D=6
    # Hecke: p ≡ 1 mod 3 (same condition)
    # Same twin prime kill; same cousin prime story
    # ============================================================
    forms['D=3 (N=15)'] = {
        'field': 'Q(√(-3)) variant',
        'galois': 'Z/2',
        'hecke_cond': 'p ≡ 1 mod 3',
        'activation': len(active_primes) / total_primes,
        'anti_corr_twins': 'TOTAL — same as Eisenstein',
        'same_as': 'Eisenstein (D=6)',
    }

    # ============================================================
    # Form 5: D=7 (N=8 threshold)
    # Field: Q(√(-7))
    # Hecke: (-7/p) = 1
    # (-7/p) = (-1/p)(7/p). By QR: (-7/p) = 1 iff p ≡ 1,2,4 mod 7
    # (for p ≡ 1 mod 4) or p ≡ 3,5,6 mod 7 (for p ≡ 3 mod 4)
    # Actually: (-7/p) is a Kronecker symbol with conductor 7 (or 28).
    # p splits in Q(√(-7)) iff (-7/p) = 1 iff p ≡ 1,2,4 mod 7 (for odd p ≠ 7)
    # Wait: (-7/p) for odd p: by QR and supplementary laws.
    # (-7/p) = (-1/p)(7/p).
    # (7/p) by QR: (7/p)(p/7) = (-1)^{(7-1)/2·(p-1)/2} = (-1)^{3(p-1)/2}
    # = (-1)^{(p-1)/2} · (-1)^{(p-1)} = (-1/p) · 1 (since (-1)^{p-1}=1)
    # So (7/p) = (-1/p)(p/7). Then (-7/p) = (-1/p)(7/p) = (-1/p)²(p/7) = (p/7).
    # So (-7/p) = (p/7)! Which is 1 iff p ≡ 1, 2, 4 mod 7.
    # ============================================================
    active_primes_7 = [p for p in primes_gt5 if p % 7 in (1, 2, 4)]
    active_twins_7 = [p for p in active_primes_7 if (p + 2) in pset]

    # Anti-correlation check for each subclass:
    # p ≡ 1 mod 7: p+2 ≡ 3 mod 7 → (3/7): 3² ≡ 2, 3³ ≡ 6 ≡ -1 → (3/7) = -1 → anti-corr ✓
    # p ≡ 2 mod 7: p+2 ≡ 4 mod 7 → (4/7) = 1 → NOT anti-corr ✗
    # p ≡ 4 mod 7: p+2 ≡ 6 mod 7 → (6/7): 6 ≡ -1, (-1/7) = -1 → anti-corr ✓
    # Partial: 2 of 3 classes anti-correlated

    # Best class: combine with mod-8 for concentration
    # Try p ≡ 1 mod 7 AND p ≡ 1 mod 8 → p ≡ 57 mod 56... let me use CRT
    # Actually, just try various mod-56 classes
    best_gpy_7 = 0
    best_class_7 = None
    for a in range(1, 56):
        if math.gcd(a, 56) != 1:
            continue
        if a % 7 not in (1, 2, 4):
            continue
        primes_a = [p for p in primes_gt5 if p % 56 == a]
        twins_a = [p for p in primes_a if (p + 2) in pset]
        if len(primes_a) < 10:
            continue
        gpy_a = (len(twins_a) / len(primes_a)) * log_limit
        if gpy_a > best_gpy_7:
            best_gpy_7 = gpy_a
            best_class_7 = (a, len(primes_a), len(twins_a))

    forms['D=7 (N=8)'] = {
        'field': 'Q(√(-7))',
        'galois': 'Z/2',
        'hecke_cond': '(-7/p)=1, p ≡ 1,2,4 mod 7',
        'activation': len(active_primes_7) / total_primes,
        'anti_corr_twins': 'Partial (2/3 classes)',
        'n_active': len(active_primes_7),
        'n_active_twins': len(active_twins_7),
        'gpy_active': (len(active_twins_7) / len(active_primes_7)) * log_limit if active_primes_7 else 0,
        'best_class_mod56': f"p ≡ {best_class_7[0]} mod 56" if best_class_7 else None,
        'gpy_best': best_gpy_7,
    }

    # ============================================================
    # Also: Gaussian form (-1/p) = 1, p ≡ 1 mod 4
    # Anti-corr: p ≡ 1 mod 4 → p+2 ≡ 3 mod 4 → (-1/(p+2)) = -1 → YES
    # ============================================================
    active_gauss = [p for p in primes_gt5 if p % 4 == 1]
    twins_gauss = [p for p in active_gauss if (p + 2) in pset]
    best_gauss_mod20 = 0
    best_gauss_class = None
    for a in range(1, 20):
        if math.gcd(a, 20) != 1:
            continue
        if a % 4 != 1:
            continue
        primes_a = [p for p in primes_gt5 if p % 20 == a]
        twins_a = [p for p in primes_a if (p + 2) in pset]
        if len(primes_a) < 10:
            continue
        gpy_a = (len(twins_a) / len(primes_a)) * log_limit
        if gpy_a > best_gauss_mod20:
            best_gauss_mod20 = gpy_a
            best_gauss_class = (a, len(primes_a), len(twins_a))

    forms['Gaussian (-1/p)'] = {
        'field': 'Q(i)',
        'galois': 'Z/2',
        'hecke_cond': 'p ≡ 1 mod 4',
        'activation': len(active_gauss) / total_primes,
        'anti_corr_twins': True,
        'n_active': len(active_gauss),
        'n_active_twins': len(twins_gauss),
        'gpy_active': (len(twins_gauss) / len(active_gauss)) * log_limit if active_gauss else 0,
        'gpy_best': best_gauss_mod20,
        'best_class': f"p ≡ {best_gauss_class[0]} mod 20" if best_gauss_class else None,
    }

    return forms, gpy_baseline, total_primes, all_twins


def run_palindromic_comparison(limit=10_000_000):
    """Full comparison of palindromic forms as prime gap probes."""
    print("=" * 78)
    print("PALINDROMIC FORMS AS PRIME GAP PROBES")
    print("Which palindromic polynomial sees twin primes most clearly?")
    print("=" * 78)

    forms, gpy_baseline, total_primes, all_twins = palindromic_form_analysis(limit)

    print(f"\nBaseline: {all_twins} twin primes among {total_primes:,} primes ≤ {limit:,}")
    print(f"GPY ratio (unrestricted): {gpy_baseline:.4f}")
    print(f"Parity barrier: 2.000")

    # Comparison table
    print(f"\n{'Form':<20s} {'Hecke cond':<22s} {'Activ':>6s} {'Anti-corr':>10s} "
          f"{'GPY(active)':>11s} {'GPY(best)':>10s} {'vs baseline':>11s}")
    print("-" * 95)

    for name in ['Bolza (D=2)', 'Golden (D=5)', 'D=7 (N=8)', 'Gaussian (-1/p)',
                  'Eisenstein (D=6)', 'D=3 (N=15)']:
        f = forms[name]
        if 'same_as' in f:
            print(f"{name:<20s} {'(same as ' + f['same_as'] + ')':>60s}")
            continue

        activ = f'{f["activation"]:.3f}'
        ac = str(f['anti_corr_twins'])[:10]
        gpy_a = f['gpy_active']
        gpy_b = f.get('gpy_best', gpy_a)
        ratio = gpy_b / gpy_baseline if gpy_baseline > 0 else 0

        print(f"{name:<20s} {f['hecke_cond']:<22s} {activ:>6s} {ac:>10s} "
              f"{gpy_a:>11.3f} {gpy_b:>10.3f} {ratio:>10.3f}x")

    # Detail for each form
    for name in ['Bolza (D=2)', 'Golden (D=5)', 'D=7 (N=8)', 'Gaussian (-1/p)', 'Eisenstein (D=6)']:
        f = forms[name]
        print(f"\n--- {name} ---")
        print(f"  Field: {f['field']}, Galois: {f['galois']}")
        print(f"  Hecke condition: {f['hecke_cond']}")
        print(f"  Activation density: {f['activation']:.4f}")
        print(f"  Anti-correlation (twins): {f['anti_corr_twins']}")
        print(f"  Active primes: {f['n_active']:,}, active twins: {f['n_active_twins']:,}")
        print(f"  GPY (active class): {f['gpy_active']:.4f}")
        if 'best_class' in f and f.get('gpy_best', 0) > 0:
            print(f"  Best class: {f.get('best_class', f.get('best_class_mod56', '?'))}")
            print(f"  GPY (best class): {f['gpy_best']:.4f}")
        if 'note' in f:
            print(f"  NOTE: {f['note']}")
            if 'cousin_gpy' in f:
                print(f"  Cousin GPY: {f['cousin_gpy']:.4f}")

    # Exhaustive search
    print("\n" + "=" * 78)
    print("EXHAUSTIVE SEARCH: Best congruence classes for twin primes")
    print("=" * 78)

    top = exhaustive_gpy_search(limit, max_q=60)[:20]
    print(f"\n{'Rank':>4s} {'Class':>20s} {'Twins':>7s} {'Primes':>8s} {'Density':>8s} "
          f"{'GPY':>7s} {'Activ':>7s}")
    print("-" * 68)
    for i, r in enumerate(top):
        print(f"{i+1:>4d} {r['class']:>20s} {r['n_twins']:>7d} {r['n_primes']:>8d} "
              f"{r['density']:.5f} {r['gpy']:>7.3f} {r['activation']:.4f}")

    # Does Bolza's class appear in the top?
    bolza_rank = None
    for i, r in enumerate(top):
        if r['q'] == 40 and r['a'] == 17:
            bolza_rank = i + 1
            break

    if bolza_rank:
        print(f"\n  Bolza class (p ≡ 17 mod 40) is rank #{bolza_rank}")
    else:
        # Search further
        for i, r in enumerate(exhaustive_gpy_search(limit, max_q=60)):
            if r['q'] == 40 and r['a'] == 17:
                bolza_rank = i + 1
                break
        if bolza_rank:
            print(f"\n  Bolza class (p ≡ 17 mod 40) is rank #{bolza_rank}")

    print("\n" + "=" * 78)
    return forms


if __name__ == '__main__':
    run_palindromic_comparison()
