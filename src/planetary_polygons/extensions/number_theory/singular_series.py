"""Singular series constants for twin-prime-type problems.

Computes the twin prime constant C_2 and the Bateman-Horn constant
S_{40,17} for primes p with p, p+2 both prime and p = 17 mod 40.
"""

import mpmath

from .sieve import primes_up_to

mpmath.mp.dps = 50


def twin_prime_constant_c2(prime_bound=1_000_000):
    """Compute the Hardy-Littlewood twin prime constant C_2.

    C_2 = 2 * prod_{p >= 3} p(p-2)/(p-1)^2

    This is the "wide" convention that includes the factor of 2 for the
    p=2 sieve weight:
        C_2 ~ 1.3203236316...

    Parameters
    ----------
    prime_bound : int
        Upper bound for the prime product. Larger gives more digits.

    Returns
    -------
    mpmath.mpf
        The twin prime constant C_2 (wide convention).
    """
    primes = primes_up_to(prime_bound)

    product = mpmath.mpf(1)
    for p in primes:
        if p < 3:
            continue
        product *= mpmath.mpf(p) * (p - 2) / mpmath.mpf(p - 1) ** 2

    return 2 * product


def compute_s40_17(prime_bound=1_000_000):
    """Compute S_{40,17} = (10/3) * C_2.

    This is the Bateman-Horn constant for the twin prime counting function
    restricted to p = 17 mod 40, derived from local factors:
      - ell=2 contributes factor 4
      - ell=5 contributes factor 25/16
      - Combined with C_2 gives (10/3)*C_2

    S_{40,17} ~ 4.401...

    Parameters
    ----------
    prime_bound : int
        Upper bound for the prime product in C_2.

    Returns
    -------
    mpmath.mpf
    """
    c2 = twin_prime_constant_c2(prime_bound)
    return (mpmath.mpf(10) / 3) * c2
