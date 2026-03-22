"""
The number-theoretic partition function for quantum gravity.

Z_gravity = Sum_Gamma exp(-I[Gamma])

where the sum is over Fuchsian groups Gamma organized by:
1. The polygon number N (the Z_N symmetry)
2. The trace field Q(sqrt(D)) (the algebraic number field)
3. The conductor f (the arithmetic level)

The Baum-Connes assembly map mu: K_0^Gamma(EGamma) -> K_0(C*_r(Gamma))
connects the equivariant index (topology) to the C*-algebra (observables).

For the vortex system:
    Left side:  ind_m = f(m,N) + b(N)  [equivariant RR]
    Right side: c = 12*b(N) = N^2 + O(N)  [central charge]
    The map:    mu sends ind_m to the orbifold CFT data

The partition function:
    Z = Sum_N Sum_{D} w(N,D) * exp(-c(N)/12) * Z_frozen(N)

where w(N,D) counts the Fuchsian groups with Z_N symmetry and
trace field Q(sqrt(D)), weighted by the Selberg zeta.
"""

import numpy as np
from math import pi, sin, cos, log, exp, sqrt, gcd


def casimir(m, N):
    """The Casimir f(m,N) = m(N-m)/2."""
    return m * (N - m) / 2.0


def b_exact(N):
    """Exact vacuum energy offset b(N) = N(N+1)/12 - log(2) + log(N)/(N-1)."""
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


# =====================================================================
# PART 1: The palindromic polynomials and their trace fields
# =====================================================================

def palindromic_polynomial_discriminant(N):
    """The discriminant D of the trace field Q(sqrt(D)) for the
    palindromic polynomial of the N-gon stability threshold.

    Returns (discriminant, degree, field_name).

    The trace field of the N-gon is Q(cos(2pi/N)) = Q(zeta_N + zeta_N^{-1}),
    the maximal real subfield of the cyclotomic field Q(zeta_N).
    Its degree over Q is phi(N)/2.
    """
    # Degree-1 cases (rational field):
    if N in [1, 2, 3, 4, 6]:
        return 1, 1, "Q"

    # Degree-2 cases:
    if N == 5 or N == 10:
        return 5, 2, "Q(sqrt(5))"  # golden ratio field
    if N == 8:
        return 2, 2, "Q(sqrt(2))"  # silver ratio field
    if N == 12:
        return 3, 2, "Q(sqrt(3))"

    # Higher degree: use phi(N)/2
    phi_N = sum(1 for k in range(1, N + 1) if gcd(k, N) == 1)
    degree = phi_N // 2

    # Known discriminants for small N
    disc_table = {
        7: (49, 3, "Q(cos(2pi/7))"),
        9: (81, 3, "Q(cos(2pi/9))"),
        11: (11**4, 5, "Q(cos(2pi/11))"),
        13: (13**5, 6, "Q(cos(2pi/13))"),
        15: (225, 4, "Q(cos(2pi/15))"),
        16: (256, 4, "Q(cos(2pi/16))"),
        17: (17**7, 8, "Q(cos(2pi/17))"),
        19: (19**8, 9, "Q(cos(2pi/19))"),
        20: (2000, 4, "Q(cos(2pi/20))"),
        23: (23**10, 11, "Q(cos(2pi/23))"),
    }
    if N in disc_table:
        return disc_table[N]

    # Default: conductor proxy
    return N**max(1, degree - 1), degree, f"Q(cos(2pi/{N}))"


# =====================================================================
# PART 2: The Legendre symbol pattern
# =====================================================================

def legendre_symbol(a, p):
    """Legendre symbol (a/p) for odd prime p."""
    if a % p == 0:
        return 0
    val = pow(a, (p - 1) // 2, p)
    return val if val <= 1 else -1


def visibility_pattern(D, p_max=100):
    """Which primes p see the palindromic polynomial with discriminant D.

    Returns (visible_primes, invisible_primes).
    """
    visible = []
    invisible = []
    for p in range(3, p_max, 2):
        if all(p % d != 0 for d in range(2, int(sqrt(p)) + 1)):
            ls = legendre_symbol(D % p if D % p >= 0 else D % p + p, p)
            if ls == 1:
                visible.append(p)
            elif ls == -1:
                invisible.append(p)
    return visible, invisible


# =====================================================================
# PART 3: The gravitational action I[Gamma]
# =====================================================================

def gravitational_action(N, genus=0):
    """The gravitational action for a Fuchsian group with Z_N symmetry.

    For genus 0: I = b(N).
    For genus g > 0: I = b(N) + (g-1) * N^2/12.
    """
    b = b_exact(N)
    if genus == 0:
        return b
    else:
        return b + (genus - 1) * N**2 / 12


def frozen_determinant_log(N):
    """Log of the frozen determinant Z_frozen(N).

    Even N: Z_frozen = 2^{3(N-2)/4} / (N-3)!!
    Odd N: computed from Casimir gaps.
    """
    if N % 2 == 0:
        log_Z = 3 * (N - 2) / 4 * log(2)
        k = N - 3
        while k > 0:
            log_Z -= log(k)
            k -= 2
        return log_Z
    else:
        m_crit = (N - 1) // 2
        f_crit = casimir(m_crit, N)
        log_Z = 0
        for m in range(1, N):
            if m == m_crit:
                continue
            gap = abs(f_crit - casimir(m, N))
            if gap > 1e-12:
                log_Z += -0.5 * log(gap)
        return log_Z


# =====================================================================
# PART 4: The partition function
# =====================================================================

def gravity_partition_function(N_max=20):
    """Compute Z = Sum_{N=3}^{N_max} exp(-b(N)) * Z_frozen(N).

    Returns (Z_total, terms) where terms is a list of
    (N, D, field, I_N, exp_neg_I, Z_frozen, term) tuples.
    """
    Z_total = 0.0
    terms = []

    for N in range(3, N_max + 1):
        D, deg, field = palindromic_polynomial_discriminant(N)
        I_N = gravitational_action(N)
        exp_neg_I = exp(-I_N) if I_N < 500 else 0
        log_Z_fr = frozen_determinant_log(N)
        Z_fr = exp(log_Z_fr) if log_Z_fr > -500 else 0

        term = exp_neg_I * Z_fr
        Z_total += term
        terms.append((N, D, field, I_N, exp_neg_I, Z_fr, term))

    return Z_total, terms


# =====================================================================
# PART 5: Organization by trace field
# =====================================================================

def organize_by_field(terms):
    """Organize the partition function by algebraic number field.

    Returns dict: field_name -> list of (N, D, term).
    """
    fields = {}
    for N, D, field, I_N, exp_I, Z_fr, term in terms:
        if field not in fields:
            fields[field] = []
        fields[field].append((N, D, term))
    return fields


# =====================================================================
# PART 6: The assembly map verification
# =====================================================================

def assembly_map_table(N_max=20):
    """Verify c = 12*b(N) ~ N^2 for each N.

    Returns list of (N, b, c, N_sq, c_minus_Nsq) tuples.
    """
    rows = []
    for N in range(3, N_max + 1):
        b = b_exact(N)
        c = 12 * b
        rows.append((N, b, c, N**2, c - N**2))
    return rows


# =====================================================================
# PART 7: The Selberg zeta contribution
# =====================================================================

def selberg_contribution(N):
    """The leading Selberg zeta contribution for the N-gon orbifold.

    Returns (l_0, Z_selberg_leading) where l_0 is the shortest
    geodesic length and Z_selberg ~ 1 - exp(-l_0).
    """
    f_crit = casimir(N // 2, N)
    b = b_exact(N)
    target = f_crit - b

    if target > 0:
        rho_star = np.arcsinh(exp(target) / 2)
        l_0 = 2 * rho_star
    else:
        l_0 = 1.0

    Z_selberg_leading = 1 - exp(-l_0)
    return l_0, Z_selberg_leading


# =====================================================================
# Convenience: full analysis
# =====================================================================

def full_analysis(N_max=20):
    """Run the complete gravity partition function analysis.

    Returns a dict with all results.
    """
    Z_total, terms = gravity_partition_function(N_max)
    fields = organize_by_field(terms)
    assembly = assembly_map_table(N_max)
    selberg = [(N, *selberg_contribution(N)) for N in range(3, N_max + 1)]

    # Field fractions
    field_fracs = {}
    for fname, entries in fields.items():
        Z_field = sum(e[2] for e in entries)
        field_fracs[fname] = Z_field / Z_total if Z_total > 0 else 0

    # Cumulative convergence
    cumulative = 0.0
    convergence = []
    for t in terms:
        cumulative += t[6]
        convergence.append((t[0], cumulative / Z_total))

    return {
        'Z_total': Z_total,
        'terms': terms,
        'fields': fields,
        'field_fractions': field_fracs,
        'assembly': assembly,
        'selberg': selberg,
        'convergence': convergence,
    }
