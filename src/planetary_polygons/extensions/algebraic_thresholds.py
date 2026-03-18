"""
Algebraic structure of stability thresholds on H² and S².

H² threshold field extensions
------------------------------
The N-ring marginal stability condition on H² is C₁(H², ξ*) = m(N-m)/2
where m = floor(N/2). This gives the palindromic quadratic:

    A ξ² + 2T ξ + A = 0,   A = (N-1) - m(N-m)/2,   T = m(N-m)/2

Multiplied through by lcm of denominators to give integer coefficients.
The smaller positive root is the stability threshold ξ*.

Pattern (N ≥ 8):
    Even N:  field = Q(√(squarefree(N-1)))
    Odd  N:  field = Q(√(squarefree(N-3)))

Special case N=10: N-1=9=3², squarefree=1, so ξ*(10) = 1/7 ∈ Q.

S² thresholds: all rational
-----------------------------
On S², C₁(S², ξ) = (N-1)(1-ξ)/(1+ξ) is decreasing in ξ, so curvature
destabilizes the ring. The threshold is:

    ξ_crit = [(N-1) - T] / [(N-1) + T],   T = m(N-m)/2

Explicit rational formulas:
    Even N:  ξ_crit = (8N-8-N²) / (N²+8N-8)
    Odd  N:  ξ_crit = (7-N) / (N+9)

Returns None when ξ_crit ≤ 0 (ring already unstable in flat limit).
Only N ≤ 6 have positive thresholds.
"""
from fractions import Fraction
import math


def _squarefree_part(n):
    """Return the squarefree part of a positive integer n (trial division)."""
    if n <= 0:
        raise ValueError(f"n must be positive, got {n}")
    result = 1
    d = 2
    while d * d <= n:
        cnt = 0
        while n % d == 0:
            n //= d
            cnt += 1
        if cnt % 2 == 1:
            result *= d
        d += 1
    if n > 1:
        result *= n
    return result


def h2_threshold_polynomial(N):
    """
    Integer palindromic polynomial A·ξ² + B·ξ + A = 0 for the N-ring H²
    marginal-stability threshold.

    A = (N-1) - m(N-m)/2,  B = m(N-m),  m = floor(N/2).
    Coefficients are cleared of denominators (multiplied by lcm).

    Returns
    -------
    (A_int, B_int) : (int, int)
        A_int < 0 for N ≥ 8.  The monic form is ξ² - (B_int/|A_int|)ξ + 1 = 0.
    """
    m = N // 2
    T = Fraction(m * (N - m), 2)        # T = m(N-m)/2
    A = Fraction(N - 1) - T              # palindromic coefficient
    B = 2 * T                            # middle coefficient = m(N-m)
    denom = math.lcm(A.denominator, B.denominator)
    return int(A * denom), int(B * denom)


def h2_stability_threshold(N):
    """
    Exact stability threshold ξ* for the N-ring on H².

    For N ≤ 7 the ring is stable in the flat limit, so ξ* = 0.
    For N ≥ 8 the ring needs curvature ξ ≥ ξ* to be stable.

    Returns
    -------
    (xi_star, disc_squarefree, field_str) : (float, int, str)
        xi_star  : float threshold value
        disc_squarefree : squarefree part of the discriminant (determines field)
        field_str : 'Q' or 'Q(sqrt(D))'
    """
    m = N // 2
    T = Fraction(m * (N - m), 2)
    A = Fraction(N - 1) - T

    if A >= 0:
        # N ≤ 7: already stable at ξ = 0
        return 0.0, 1, 'Q'

    # Clear denominators for exact discriminant computation
    denom = math.lcm(A.denominator, T.denominator)
    A_int = int(A * denom)          # negative
    T_int = int(T * denom)          # positive (= B_int // 2 after lcm)

    # Palindromic: A_int·ξ² + 2T_int·ξ + A_int = 0 (after clearing)
    # disc/4 = T_int² - A_int²
    disc4 = T_int * T_int - A_int * A_int
    D = _squarefree_part(abs(disc4))

    # Smaller positive root: ξ* = (T_int - sqrt(T_int² - A_int²)) / |A_int|
    xi_star = (T_int - math.sqrt(disc4)) / abs(A_int)

    field_str = 'Q' if D == 1 else f'Q(sqrt({D}))'
    return xi_star, D, field_str


def h2_threshold_table(N_max=16):
    """
    Table of H² stability thresholds for N = 7, ..., N_max.

    Returns list of dicts with keys:
        N, xi_star (float), disc_squarefree (int), field (str),
        poly_A (int), poly_B (int)

    N=7 is marginal in flat space (ξ* = 0); N ≥ 8 require positive curvature.
    """
    rows = []
    for N in range(7, N_max + 1):
        xi_star, D, field = h2_stability_threshold(N)
        A_int, B_int = h2_threshold_polynomial(N)
        rows.append({
            'N': N,
            'xi_star': xi_star,
            'disc_squarefree': D,
            'field': field,
            'poly_A': A_int,
            'poly_B': B_int,
        })
    return rows


def sphere_stability_threshold(N):
    """
    Exact destabilization threshold ξ_crit for the N-ring on S².

    On S², C₁(S², ξ) = (N-1)(1-ξ)/(1+ξ) decreases with ξ, so curvature
    gradually destabilizes the ring. The ring loses stability at:

        ξ_crit = [(N-1) - m(N-m)/2] / [(N-1) + m(N-m)/2],  m = floor(N/2)

    Explicit closed forms:
        Even N:  ξ_crit = (8N-8-N²) / (N²+8N-8)
        Odd  N:  ξ_crit = (7-N) / (N+9)

    Returns
    -------
    Fraction or None
        Exact rational threshold, or None if ξ_crit ≤ 0 (N ≥ 7 on S²).
    """
    m = N // 2
    T = Fraction(m * (N - m), 2)
    numer = Fraction(N - 1) - T
    denom = Fraction(N - 1) + T
    xi_crit = numer / denom
    return None if xi_crit <= 0 else xi_crit


def sphere_threshold_table(N_max=12):
    """
    Table of S² destabilization thresholds for N = 3, ..., N_max.

    Returns list of dicts with keys: N, xi_crit (Fraction or None).
    Only N ≤ 6 return non-None values.
    """
    return [{'N': N, 'xi_crit': sphere_stability_threshold(N)}
            for N in range(3, N_max + 1)]


if __name__ == '__main__':
    print('H² thresholds:')
    print(f'{"N":>3}  {"xi*":>10}  {"D":>4}  {"field":>14}  {"poly"}')
    for row in h2_threshold_table(16):
        poly = f'{row["poly_A"]}ξ² + {row["poly_B"]}ξ + {row["poly_A"]} = 0'
        print(f'{row["N"]:>3}  {row["xi_star"]:>10.6f}  {row["disc_squarefree"]:>4}  '
              f'{row["field"]:>14}  {poly}')

    print('\nS² thresholds (N ≤ 6 only shown):')
    for row in sphere_threshold_table(10):
        val = str(row['xi_crit']) if row['xi_crit'] is not None else 'None'
        print(f'  N={row["N"]}: xi_crit = {val}')
