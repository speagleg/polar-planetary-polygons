"""
Bernoulli-Havelock structural backbone.

The Havelock Casimir f(m,N) = m(N-m)/2 is an affine function of the second
Bernoulli polynomial:

    f(m,N) = (N^2/12)(1 - 6 B_2(m/N))

where B_2(x) = x^2 - x + 1/6.  This identity connects every eigenvalue-based
prediction in the series to Bernoulli polynomials and, through the
Bernoulli-zeta bridge, to values of the Riemann zeta function.

Ported from spiral-hexagon/bernoulli_bridge.py with two algebraic corrections:
  1. The identity is AFFINE (1 - 6 B_2), not multiplicative (6 B_2).
  2. The integral of B_2^2 on [0,1] is 1/180, not 1/30.

References:
  - Havelock (1931), Phil. Mag. 11, 617-633
  - Euler (1738), product formula for Bernoulli polynomials
  - DLMF 24.2, 24.4, 25.6  (Bernoulli numbers, polynomials, zeta values)
"""

from fractions import Fraction
from math import factorial, comb, pi, sqrt, log, exp, atan
import cmath

# ============================================================
# Bernoulli numbers (exact, as Fractions)
# ============================================================

# B_0 through B_12 (odd indices > 1 vanish)
BERNOULLI = [
    Fraction(1),        # B_0
    Fraction(-1, 2),    # B_1
    Fraction(1, 6),     # B_2
    Fraction(0),        # B_3
    Fraction(-1, 30),   # B_4
    Fraction(0),        # B_5
    Fraction(1, 42),    # B_6
    Fraction(0),        # B_7
    Fraction(-1, 30),   # B_8
    Fraction(0),        # B_9
    Fraction(5, 66),    # B_10
    Fraction(0),        # B_11
    Fraction(-691, 2730),  # B_12
]


def bernoulli_number(n):
    """Return B_n as a Fraction.  Supports n <= 12."""
    if n < 0 or n >= len(BERNOULLI):
        raise ValueError(f"B_{n} not in table (max index {len(BERNOULLI)-1})")
    return BERNOULLI[n]


def bernoulli_poly(n, x):
    """Evaluate B_n(x) = sum_{k=0}^{n} C(n,k) B_k x^{n-k}.

    If x is a Fraction, returns exact Fraction.
    If x is a float, returns float.
    """
    return sum(comb(n, k) * BERNOULLI[k] * x**(n - k) for k in range(n + 1))


def bernoulli_poly_float(n, x):
    """Float evaluation of B_n(x)."""
    B = [float(b) for b in BERNOULLI]
    return sum(comb(n, k) * B[k] * x**(n - k) for k in range(n + 1))


# ============================================================
# The core identity: Havelock Casimir = affine B_2
# ============================================================

def havelock_casimir(m, N):
    """f(m,N) = m(N-m)/2, the Havelock Casimir (exact Fraction)."""
    return Fraction(m * (N - m), 2)


def havelock_from_bernoulli(m, N):
    """Compute f(m,N) via the Bernoulli identity:

        f(m,N) = (N^2/12)(1 - 6 B_2(m/N))

    Returns exact Fraction.  Must equal havelock_casimir(m,N).
    """
    x = Fraction(m, N)
    B2_val = bernoulli_poly(2, x)
    return Fraction(N * N, 12) * (1 - 6 * B2_val)


def normalized_havelock(m, N):
    """The normalized Havelock function f_norm(m/N) = 1 - 6 B_2(m/N).

    This is f(m,N) / (N^2/12).  Range: [0, 3/2] for m/N in [0, 1].
    Maximum 3/2 at m/N = 1/2.  Zeros at m/N = (3 +/- sqrt(3))/6.
    """
    x = Fraction(m, N) if isinstance(m, int) and isinstance(N, int) else m / N
    B2 = bernoulli_poly(2, x)
    return 1 - 6 * B2


def parabola_form(x):
    """The normalized Havelock function is the parabola 6x(1-x).

    Proof: 1 - 6 B_2(x) = 1 - 6(x^2 - x + 1/6) = 6x - 6x^2 = 6x(1-x).

    This is the key simplification: the continuum limit of the Havelock
    Casimir is a Beta(2,2) density (up to normalization).  All moments
    reduce to Beta function evaluations.

    Returns exact Fraction if x is Fraction, float otherwise.
    """
    return 6 * x * (1 - x)


# ============================================================
# Stability transitions from B_2 zeros
# ============================================================

def b2_zeros():
    """Zeros of B_2(x) = x^2 - x + 1/6 at x = (3 +/- sqrt(3))/6.

    Returns (x_lower, x_upper) as floats.
    The stable fraction of modes is 2*x_lower = (3-sqrt(3))/3.
    """
    s3 = sqrt(3)
    x_lo = (3 - s3) / 6
    x_hi = (3 + s3) / 6
    return x_lo, x_hi


def stable_fraction():
    """Fraction of modes with f_norm > 0, i.e. B_2(m/N) < 0.

    Equals 2*x_lower = (3-sqrt(3))/3 ~ 0.4226.
    """
    x_lo, _ = b2_zeros()
    return 2 * x_lo


# ============================================================
# Moment identities (exact where possible)
# ============================================================

def moment_M2_exact():
    """M_2 = <(1 - 6 B_2)^2> on [0,1] = 6/5 (exact).

    Derivation:
      (1 - 6B_2(x))^2 = 1 - 12 B_2(x) + 36 B_2(x)^2
      integral of 1 on [0,1] = 1
      integral of B_2 on [0,1] = 0  (first moment vanishes)
      integral of B_2^2 on [0,1] = 1/180
      M_2 = 1 + 0 + 36/180 = 1 + 1/5 = 6/5
    """
    return Fraction(6, 5)


def integral_B2_squared():
    """Exact: integral_0^1 B_2(x)^2 dx = 1/180.

    Via the identity: integral B_n^2 = (-1)^{n+1} (n!)^2 / (2n)! * B_{2n}
    For n=2: (-1)^3 * 4/24 * B_4 = (-1)(1/6)(-1/30) = 1/180.
    """
    return Fraction(1, 180)


def integral_B2_power(k):
    """Exact integral_0^1 B_2(x)^k dx for small k.

    Uses symmetry B_2(x) = B_2(1-x) to note odd powers integrate to zero
    (not quite: B_2 is symmetric about x=1/2, but (B_2)^k is too, so we
    need actual computation).  Returns Fraction for k <= 6.
    """
    # Known exact values
    exact = {
        0: Fraction(1),
        1: Fraction(0),         # integral of B_2 on [0,1] = 0
        2: Fraction(1, 180),    # proved: (-1)^3 (2!)^2/(4!) B_4 = 1/180
        3: Fraction(1, 3780),   # symbolic expansion and integration
        4: Fraction(1, 15120),  # = (B_2^2)^2 integrated term by term
    }
    if k in exact:
        return exact[k]
    raise ValueError(f"integral B_2^{k} not in exact table")


def moment_even(k):
    """M_{2k} = integral_0^1 (1 - 6 B_2(x))^{2k} dx.

    Expand via binomial theorem and use integral_B2_power.
    Returns exact Fraction for small k.
    """
    total = Fraction(0)
    for j in range(2 * k + 1):
        sign = (-1)**j
        binom = comb(2 * k, j)
        coeff = sign * binom * Fraction(6**j)
        try:
            integ = integral_B2_power(j)
        except ValueError:
            raise ValueError(f"M_{2*k} requires integral B_2^{j}, not in table")
        total += coeff * integ
    return total


def moment_M4_exact():
    """M_4 = integral_0^1 (1 - 6 B_2)^4 dx = 72/35."""
    return moment_even(2)


def moment_closed_form(k):
    """M_k = integral_0^1 [6x(1-x)]^k dx = 6^k * (k!)^2 / (2k+1)!.

    Since 1 - 6 B_2(x) = 6x(1-x) (the parabola identity), all moments
    reduce to the Beta function B(k+1, k+1) = (k!)^2 / (2k+1)!.

    This is EXACT for all k >= 0.  Returns Fraction.
    """
    return Fraction(6**k * factorial(k)**2, factorial(2 * k + 1))


def moment_tower(max_k=8):
    """The complete moment tower M_1 through M_{max_k}.

    Returns list of (k, M_k) pairs as Fractions.
    """
    return [(k, moment_closed_form(k)) for k in range(1, max_k + 1)]


# ============================================================
# Bernoulli-zeta bridge
# ============================================================

def zeta_from_bernoulli(k):
    """zeta(2k) = (-1)^{k+1} (2 pi)^{2k} B_{2k} / (2 (2k)!).

    Returns float.  This is the Euler formula connecting Bernoulli
    numbers to zeta values at positive even integers.
    """
    if k < 1:
        raise ValueError("k must be >= 1")
    B_2k = float(bernoulli_number(2 * k))
    return abs((-1)**(k + 1) * (2 * pi)**(2 * k) * B_2k / (2 * factorial(2 * k)))


def M2_as_zeta_ratio():
    """M_2 = 6/5 = 3 * zeta(4) / zeta(2)^2.

    Proof:
      zeta(2) = pi^2/6,  zeta(4) = pi^4/90
      zeta(4)/zeta(2)^2 = (pi^4/90) / (pi^4/36) = 36/90 = 2/5
      3 * 2/5 = 6/5 = M_2.  QED.
    """
    z2 = zeta_from_bernoulli(1)  # pi^2/6
    z4 = zeta_from_bernoulli(2)  # pi^4/90
    return 3.0 * z4 / z2**2


# ============================================================
# Particle physics predictions as B_2 evaluations
# ============================================================

def weinberg_angle_from_bernoulli():
    """sin^2(theta_W) = 3/11 from B_2 at m/N = 2/4.

    The Weinberg angle uses f(2,4) = 2 and f(1,3) = 1.
    f(2,4) = (16/12)(1 - 6 B_2(1/2)) = (4/3)(1 - 6(-1/12)) = (4/3)(3/2) = 2.
    f(1,3) = (9/12)(1 - 6 B_2(1/3)) = (3/4)(1 - 6(1/18)) = (3/4)(2/3) = 1/2.

    sin^2(theta_W) = 3 / (3 + 8) = 3/11 uses the ratio
    of Casimir values at N=3 (SU(2)) and N=4 (SU(3)) polygons.

    Returns dict with all intermediate values.
    """
    B2_half = bernoulli_poly(2, Fraction(1, 2))     # -1/12
    B2_third = bernoulli_poly(2, Fraction(1, 3))     # 1/18
    f_24 = havelock_from_bernoulli(2, 4)             # = 2
    f_13 = havelock_from_bernoulli(1, 3)             # = 1

    return {
        'B2_at_half': B2_half,       # -1/12
        'B2_at_third': B2_third,     # 1/18
        'f_24': f_24,                # 2 (SU(3) Casimir)
        'f_13': f_13,                # 1 (SU(2) Casimir)
        'sin2_theta_W': Fraction(3, 11),
        'derivation': 'f(2,4)/f(1,3) = 2 => hypercharge normalization => 3/11'
    }


def fermion_mass_bernoulli_table(N=7):
    """Express each Havelock Casimir f(m,N) as a B_2 evaluation.

    For N=7: f(m,7) = (49/12)(1 - 6 B_2(m/7)), m = 1,...,6.
    The ratios f(m1)/f(m2) give fermion mass ratios in the framework.

    Returns list of dicts.
    """
    results = []
    for m in range(1, N):
        x = Fraction(m, N)
        B2 = bernoulli_poly(2, x)
        f_val = havelock_from_bernoulli(m, N)
        f_norm = 1 - 6 * B2

        results.append({
            'm': m,
            'x': x,
            'B2': B2,
            'f_norm': f_norm,     # = 1 - 6 B_2(m/N)
            'f': f_val,           # = m(N-m)/2
        })
    return results


def cosmological_constant_from_N(N=7):
    """Lambda_3 = (N^2 - 16)/16, a rational function of N.

    At N=7: Lambda_3 = 33/16.
    The N^2 term is 12 * (N^2/12) = 12 * f_max_scale, connecting
    to the Bernoulli normalization.
    """
    return Fraction(N * N - 16, 16)


def alpha_s_csc_sum(N=7):
    """The csc^2 sum entering alpha_s: sum_{m=1}^{N-1} csc^2(pi m/N).

    This is a Bernoulli number identity:
      sum_{m=1}^{N-1} csc^2(pi m/N) = (N^2 - 1)/3

    For N=7: (49-1)/3 = 16.
    """
    return Fraction(N * N - 1, 3)


def b6_at_N7():
    """B_6 = 1/42 = 1/(6*7), tying level 6 of the Bernoulli tower to N=7.

    This is the structural coincidence: the denominator of B_6 contains
    the factor 7, which is exactly the critical polygon number.
    By von Staudt-Clausen: denom(B_6) = product of primes p with (p-1)|6
    = 2 * 3 * 7 = 42.  So 7 divides denom(B_6) because 6 = 7-1.
    """
    return {
        'B6': bernoulli_number(6),         # 1/42
        'denominator': 42,
        'factorization': '2 * 3 * 7',
        'von_staudt_clausen': 'primes p with (p-1)|6: {2, 3, 7}',
        'N7_connection': '7 | denom(B_6) because 7-1 = 6',
    }


# ============================================================
# Havelock zeta function (spectral zeta of the Casimir)
# ============================================================

def havelock_zeta(N, s):
    """Z_H(s, N) = sum_{m: f(m,N) > 0} f(m,N)^{-s}.

    The spectral zeta function of the positive Havelock Casimirs.
    For N <= 7, all f(m,N) > 0 for m = 1, ..., N-1.
    """
    total = 0.0
    for m in range(1, N):
        f = float(havelock_casimir(m, N))
        if f > 0:
            total += f**(-s)
    return total


def havelock_zeta_ratio(N):
    """Z_H(2,N) / Z_H(1,N)^2 -- measures departure from log-concavity."""
    z1 = havelock_zeta(N, 1.0)
    z2 = havelock_zeta(N, 2.0)
    return z2 / z1**2 if z1 != 0 else float('inf')


# ============================================================
# Higher Bernoulli tower (conjectural Magri connection)
# ============================================================

def bernoulli_tower_table():
    """The Bernoulli tower B_2, B_4, B_6 and their physical roles.

    Returns list of dicts documenting the tower and conjectured Magri levels.
    """
    return [
        {
            'level': 2,
            'B_2k': bernoulli_number(2),     # 1/6
            'physical': 'Havelock Casimir f(m,N)',
            'normalization': 'N^2/12 = N^2 * B_2',
            'magri': 'PROVED (level 1 of Magri hierarchy)',
        },
        {
            'level': 4,
            'B_2k': bernoulli_number(4),     # -1/30
            'physical': 'Quartic coupling Q = N f^2 / 48',
            'normalization': '48 = 2 * 4! (quartic Bernoulli doubling)',
            'magri': 'PROVED (level 2 of Magri hierarchy, magri_hierarchy.py)',
        },
        {
            'level': 6,
            'B_2k': bernoulli_number(6),     # 1/42
            'physical': 'N=7 critical polygon (7 | 42)',
            'normalization': '1/42 = 1/(6*7), von Staudt-Clausen',
            'magri': 'CONJECTURED (level 3, not yet proved)',
        },
    ]


# ============================================================
# Summary and cross-reference
# ============================================================

def full_decomposition(N=7):
    """Return a complete Bernoulli decomposition of the N=7 framework.

    This is the "Bernoulli backbone": every prediction expressed as
    evaluations of B_2 at rationals m/N, plus the tower identities.
    """
    table = fermion_mass_bernoulli_table(N)
    weinberg = weinberg_angle_from_bernoulli()
    tower = bernoulli_tower_table()

    return {
        'N': N,
        'core_identity': 'f(m,N) = (N^2/12)(1 - 6 B_2(m/N))',
        'M2': moment_M2_exact(),
        'M2_as_zeta': '6/5 = 3 zeta(4)/zeta(2)^2',
        'eigenvalue_table': table,
        'weinberg': weinberg,
        'Lambda_3': cosmological_constant_from_N(N),
        'csc2_sum': alpha_s_csc_sum(N),
        'B6_connection': b6_at_N7(),
        'tower': tower,
        'derivation_chains': derivation_chain_audit(N),
    }


# ============================================================
# Derivation chain audit: trace each prediction to B_2
# ============================================================

def derivation_chain_audit(N=7):
    """For each major prediction, trace it back to B_2 evaluations.

    Returns list of dicts, one per prediction, showing the chain:
      physical prediction -> intermediate quantities -> B_2 evaluations.
    """
    chains = []

    # --- 1. Weinberg angle ---
    chains.append({
        'prediction': 'sin^2(theta_W) = 3/11',
        'value': float(Fraction(3, 11)),
        'observed': 0.23122,
        'chain': [
            'f(2,4) = 2 = (16/12)(1 - 6 B_2(1/2))',
            'B_2(1/2) = -1/12',
            'h_SU2 = j(j+1)/(k+2) with j=1 from f(2,4)=j(j+1)=2',
            'h_U1 = Q^2/K = (1/2)^2/1 = 1/4 from Q=m*/N=2/4',
            'sin^2 = h_U1/(h_U1 + h_SU2) = (1/4)/(1/4+2/3) = 3/11',
        ],
        'B2_inputs': {'B_2(1/2)': Fraction(-1, 12)},
        'paper': 'Paper IV, Section 5',
    })

    # --- 2. N_crit = 7 (flat plane stability) ---
    chains.append({
        'prediction': 'N_crit = 7',
        'value': 7,
        'chain': [
            'Stability: f(m,N) < N-1 for all m, i.e. min_m lambda_m >= 0',
            'f(floor(N/2), N) = N^2/8 (even N) or (N^2-1)/8 (odd N)',
            'lambda_min = (N-1) - f_max',
            'lambda_min(7) = 6 - 6 = 0 (marginal)',
            'lambda_min(8) = 7 - 8 = -1 (unstable)',
            'f_max at N=7: f(3,7) = 6 = (49/12)(1 - 6 B_2(3/7))',
        ],
        'B2_inputs': {'B_2(3/7)': bernoulli_poly(2, Fraction(3, 7))},
        'paper': 'Paper I, Theorem 3.1',
    })

    # --- 3. Cosmological constant ---
    chains.append({
        'prediction': 'Lambda_3 = (N^2 - 16)/16 = 33/16 at N=7',
        'value': float(Fraction(33, 16)),
        'chain': [
            'Lambda_3 = (N^2 - 16)/16',
            'N^2 = 12 * (N^2/12) where N^2/12 is the Bernoulli normalization',
            'N^2/12 = (1/2B_2) * N^2 = the Casimir prefactor',
        ],
        'B2_inputs': {'B_2': Fraction(1, 6), 'N^2/12': Fraction(49, 12)},
        'paper': 'Paper V',
    })

    # --- 4. csc^2 sum (enters alpha_s, Einstein equations) ---
    chains.append({
        'prediction': 'sum csc^2(pi m/N) = (N^2-1)/3 = 16 at N=7',
        'value': 16,
        'chain': [
            'sum_{m=1}^{N-1} csc^2(pi m/N) = (N^2-1)/3',
            'This is a Ramanujan identity (polynomial in N)',
            'Connection to B_2: the csc^2 sum is the TRACE of the inverse',
            'Havelock operator in the continuum limit',
            'The 1/3 prefactor = 2*B_2 = 2*(1/6)',
        ],
        'B2_inputs': {'2*B_2': Fraction(1, 3)},
        'paper': 'Paper III, Section 4',
    })

    # --- 5. Fermion mass hierarchy (KK mode separations) ---
    mu7 = []
    for m in range(1, (N + 1) // 2):
        mu = abs(m - (N - 1) / 2.0)
        mu7.append(mu)
    chains.append({
        'prediction': 'Fermion mass hierarchy from N=7 KK charges',
        'chain': [
            f'KK charges mu_7 = |m - (N-1)/2| for pairs (m, N-m)',
            f'mu_7 values at N=7: {mu7}',
            f'f(m,7) = (49/12)(1 - 6 B_2(m/7)) for m=1,2,3',
            f'Ratios f(1,7):f(2,7):f(3,7) = 3:5:6',
            f'These enter RS profile: mass ~ exp(-c_eff * sigma)',
        ],
        'B2_inputs': {
            f'B_2({m}/7)': bernoulli_poly(2, Fraction(m, 7))
            for m in range(1, 4)
        },
        'paper': 'Paper IV, Section 7',
    })

    # --- 6. Vacuum energy c/12 ---
    chains.append({
        'prediction': 'Central charge c = N^2, vacuum energy c/12 = N^2/12',
        'chain': [
            'c = N^2 from the orbifold CFT at the polygon',
            'Vacuum energy = c/12 = N^2/12',
            'N^2/12 is exactly the Bernoulli normalization scale',
            'b(N) = N(N+1)/12 + log N/(N-1) includes 1-loop corrections',
        ],
        'B2_inputs': {'N^2/12 = N^2 * B_2': Fraction(N * N, 12)},
        'paper': 'Paper I, Proposition 6.3',
    })

    # --- 7. Growth law coefficient a = 1/3 ---
    chains.append({
        'prediction': 'Growth law coefficient a(N) -> 1/3 as N -> infinity',
        'chain': [
            'a(N) = (f_crit - <D(N)>) / f_crit',
            '<D(N)> = N(N+1)/12 + log N/(N-1)',
            'f_crit = N^2/8',
            'a(N) -> 1 - (N+1)/12 * 8/N = 1 - 2(N+1)/(3N) -> 1/3',
            'The 1/3 = 2*B_2 = 2*(1/6)',
        ],
        'B2_inputs': {'2*B_2': Fraction(1, 3)},
        'paper': 'Paper I, Corollary 6.6',
    })

    # --- 8. B_6 = 1/42 and N=7 ---
    chains.append({
        'prediction': 'N=7 is special via von Staudt-Clausen for B_6',
        'chain': [
            'B_6 = 1/42 = 1/(2*3*7)',
            'By von Staudt-Clausen: denom(B_6) = prod of p with (p-1)|6',
            'Primes: p=2 (1|6), p=3 (2|6), p=7 (6|6)',
            'So 7 | denom(B_6) BECAUSE 7-1=6',
            'The same reason 7 is critical: the N-th polygon is marginal',
            'when the (N-1)-th Bernoulli number denominator contains N',
        ],
        'B2_inputs': {'B_6': bernoulli_number(6)},
        'paper': 'Paper I, Remark 6.5',
    })

    return chains


# ============================================================
# Gauss sum and CKM phase from the Bernoulli backbone
# ============================================================

def quadratic_residues(p):
    """Quadratic residues mod p (the nonzero squares).

    For p=7: QR = {1, 2, 4} (since 1^2=1, 2^2=4, 3^2=2 mod 7).
    """
    return sorted(set(a * a % p for a in range(1, p)))


def quadratic_nonresidues(p):
    """Quadratic non-residues mod p."""
    qr = set(quadratic_residues(p))
    return sorted(set(range(1, p)) - qr)


def gauss_sum_qr(p):
    """Partial Gauss sum over quadratic residues: G(QR) = sum_{a in QR} omega^a.

    For p = 3 mod 4: G(QR) = (-1 + i*sqrt(p))/2.
    For p = 1 mod 4: G(QR) = (-1 + sqrt(p))/2 (real).

    Returns complex number.
    """
    omega = cmath.exp(2j * pi / p)
    qr = quadratic_residues(p)
    return sum(omega**a for a in qr)


def frobenius_eigenvalue_at_2(p):
    """Frobenius eigenvalue alpha_2 for the CM curve associated to Q(sqrt(-p)).

    For p = 3 mod 4: alpha_2 = (1 + i*sqrt(p))/2.
    This equals -conj(G(QR)) where G(QR) is the partial Gauss sum.
    |alpha_2| = sqrt(2) (Weil bound at the prime 2).

    Returns complex number and metadata.
    """
    if p % 4 != 3:
        return {
            'alpha_2': (-1 + sqrt(p)) / 2,  # real
            'is_complex': False,
            'arg_deg': 0.0,
            'note': 'p = 1 mod 4: Gauss sum is real, no CP phase',
        }

    alpha = (1 + 1j * sqrt(p)) / 2
    G_QR = gauss_sum_qr(p)

    return {
        'alpha_2': alpha,
        'is_complex': True,
        'modulus_sq': abs(alpha)**2,
        'arg_rad': cmath.phase(alpha),
        'arg_deg': cmath.phase(alpha) * 180 / pi,
        'arctan_sqrt_p': atan(sqrt(p)) * 180 / pi,
        'G_QR': G_QR,
        'relation': 'alpha_2 = -conj(G(QR))',
        'match': abs(alpha - (-G_QR.conjugate())) < 1e-12,
    }


def ckm_phase_from_gauss_sum(N=7):
    """Derive the CKM phase from the quadratic Gauss sum at N.

    The complete chain:
      1. B_6 = 1/42 -> von Staudt-Clausen -> 7 | denom(B_6)
      2. N=7 is the critical polygon (Havelock stability)
      3. QR(7) = {1,2,4} (quadratic residues = Frobenius orbit)
      4. Gauss sum G(QR) = (-1+i*sqrt(7))/2
      5. Frobenius eigenvalue alpha_2 = (1+i*sqrt(7))/2 = -conj(G(QR))
      6. delta_CKM = arg(alpha_2) = arctan(sqrt(7)) = 69.295 deg

    CP violation requires N = 3 mod 4.  Since 7 = 3 mod 4, CP is violated.
    If N_crit were 5 (= 1 mod 4), there would be no CP violation.

    Returns dict with all intermediate values.
    """
    # Step 1: von Staudt-Clausen
    B6 = bernoulli_number(6)
    vsc_primes = [p for p in range(2, N + 2)
                  if all(p % d != 0 for d in range(2, p)) and p > 1
                  and (N - 1) % (p - 1) == 0]

    # Step 2: stability (already known)
    f_crit = havelock_casimir(N // 2, N)

    # Step 3: quadratic residues
    qr = quadratic_residues(N)
    qnr = quadratic_nonresidues(N)

    # Step 4: Gauss sum
    G_QR = gauss_sum_qr(N)

    # Step 5: Frobenius eigenvalue
    frob = frobenius_eigenvalue_at_2(N)

    # Step 6: CKM phase
    delta_rad = atan(sqrt(N))
    delta_deg = delta_rad * 180 / pi

    # CP violation requires p = 3 mod 4
    has_cp = N % 4 == 3

    return {
        'N': N,
        'B_N_minus_1': B6,
        'von_staudt_clausen_primes': vsc_primes,
        'N_in_denom': N in vsc_primes,
        'QR': qr,
        'QNR': qnr,
        'G_QR': G_QR,
        'G_QR_expected': (-1 + 1j * sqrt(N)) / 2 if has_cp else (-1 + sqrt(N)) / 2,
        'frobenius': frob,
        'delta_CKM_rad': delta_rad,
        'delta_CKM_deg': delta_deg,
        'PDG_central': 69.0,
        'PDG_error': 3.0,
        'tension_sigma': abs(delta_deg - 69.0) / 3.0,
        'has_CP_violation': has_cp,
        'N_mod_4': N % 4,
        'chain': [
            f'B_{N-1} = {B6}, denom contains {N} (von Staudt-Clausen)',
            f'N={N} is critical polygon (Havelock: f({N//2},{N}) = {f_crit})',
            f'QR({N}) = {qr} (Frobenius orbit)',
            f'G(QR) = (-1+i*sqrt({N}))/2' if has_cp else f'G(QR) = (-1+sqrt({N}))/2 (REAL)',
            f'alpha_2 = (1+i*sqrt({N}))/2, arg = arctan(sqrt({N}))' if has_cp else 'No complex phase',
            f'delta_CKM = {delta_deg:.4f} deg (PDG: 69 +/- 3, tension {abs(delta_deg-69)/3:.2f} sigma)' if has_cp else 'No CKM phase (p = 1 mod 4)',
        ],
        'physical_mechanism': orbifold_sector_coherence(N),
    }


def orbifold_sector_coherence(N=7):
    """Physical mechanism: the CKM phase = arg of orbifold sector amplitude.

    In the Z_N orbifold, the Yukawa coupling receives contributions from:
      - The untwisted sector (m=0): amplitude 1
      - The QR twisted sectors: each contributes omega^m

    Total up-type amplitude:
      A_up = 1 + sum_{m in QR} omega^m = 1 + G(QR) = alpha_2

    Total down-type amplitude:
      A_down = 1 + G(QNR) = conj(alpha_2)  (when N = 3 mod 4)

    The CKM phase is arg(A_up) = arctan(sqrt(N)).

    This is the "orbifold sector coherence" mechanism: the direct (untwisted)
    coupling anchors the phase to the first quadrant, while the twisted sector
    sum provides the imaginary part.
    """
    omega = cmath.exp(2j * pi / N)
    qr = quadratic_residues(N)
    qnr = quadratic_nonresidues(N)

    has_cp = N % 4 == 3

    # Sector amplitudes
    A_up = 1 + sum(omega**m for m in qr)
    A_down = 1 + sum(omega**m for m in qnr)

    # Check conjugation symmetry
    conjugate_symmetric = abs(A_down - A_up.conjugate()) < 1e-12

    return {
        'A_up': A_up,
        'A_down': A_down,
        'A_up_equals_alpha_2': abs(A_up - (1 + 1j * sqrt(N)) / 2) < 1e-12 if has_cp else None,
        'conjugate_symmetric': conjugate_symmetric,
        'arg_A_up_deg': cmath.phase(A_up) * 180 / pi,
        'arg_A_down_deg': cmath.phase(A_down) * 180 / pi,
        'total_phase_content_deg': 2 * abs(cmath.phase(A_up)) * 180 / pi,
        'irremovable_phase_deg': abs(cmath.phase(A_up)) * 180 / pi,
        'mechanism': (
            'Untwisted sector (+1) + QR twisted sectors (G(QR)) = alpha_2. '
            'The +1 anchors the amplitude to the first quadrant. '
            'A_down = conj(A_up) from N=3 mod 4. '
            'After 5 quark rephasing DOF, irremovable phase = arg(A_up).'
        ),
        'heegner': {
            'discriminant': -N,
            'class_number_1': N in [3, 4, 7, 8, 11, 19, 43, 67, 163],
            'unique_CM_point': N in [3, 4, 7, 8, 11, 19, 43, 67, 163],
        },
    }


# ============================================================
# Unified backbone constants and functions
# ============================================================

SIGMA_0 = 5  # The single geometric parameter (tunes s23 via RS profile)

N_CRIT = 7  # Critical polygon from Havelock stability + von Staudt-Clausen

BERNOULLI_PHASES = {
    'aL': Fraction(6, 42),   # = 1/7 = (N-1)/denom(B_6)
    'aR': Fraction(5, 42),   # = (N-2)/denom(B_6)
    'aH': Fraction(4, 42),   # = 2/21 = (N-3)/denom(B_6)
}


def havelock_eigenvalue_unified(m, N=7):
    """The Havelock stability eigenvalue lambda_m = (N-1) - m(N-m)/2.

    This is the COMPLEMENT of the Casimir: f + lambda = N-1.
    lambda = 0 at the marginal mode (BF threshold).
    lambda > 0 for stable modes (further from instability).
    """
    return Fraction(N - 1) - Fraction(m * (N - m), 2)


def conformal_dim_unified(m, N=7):
    """Unified conformal dimension c = 1/2 + lambda_m/N.

    At the BF threshold (lambda=0): c = 1/2.
    For stable modes (lambda > 0): c > 1/2 (UV-localized, lighter).
    """
    lam = havelock_eigenvalue_unified(m, N)
    return Fraction(1, 2) + lam / N


def F_IR(c, sigma):
    """Correct RS IR-brane overlap for the fermion zero mode.

    F(c, sigma) = sqrt((2c-1) / (exp((2c-1)*sigma) - 1))  for c > 1/2
    F(1/2, sigma) = 1/sqrt(sigma)                            at the BF threshold

    This gives EXPONENTIAL SUPPRESSION for UV-localized modes (c > 1/2):
    F ~ sqrt(2c-1) * exp(-(c-1/2)*sigma) for large sigma.
    """
    c = float(c)
    if abs(c - 0.5) < 1e-10:
        return 1.0 / sqrt(sigma)
    x = (2 * c - 1) * sigma
    return sqrt(abs(2 * c - 1) / (exp(x) - 1))


def instanton_fugacity(N=7):
    """K = exp(-2*pi*k_frac) where k_frac = frac(c_N/6 - N/2).

    Uses b(N) = N(N+1)/12 - ln(2) + ln(N)/(N-1) for the central charge.
    At N=7: K = 0.548.
    """
    b_N = N * (N + 1) / 12 - log(2) + log(N) / (N - 1)
    k_phys = 12 * b_N / 6 - N / 2
    k_frac = k_phys - int(k_phys)
    return exp(-2 * pi * k_frac)
