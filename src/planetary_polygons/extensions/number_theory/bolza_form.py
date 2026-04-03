"""Bolza form f = eta(8z)*eta(16z): weight-1 newform, level 128.

LMFDB label: 128.1.d.a
Nebentypus: Kronecker symbol (-2/n).

Two independent methods to compute Fourier coefficients:
  1. eta_product_coefficients: direct q-expansion of eta(8z)*eta(16z)
  2. bolza_coefficients: Hecke multiplicativity from prime eigenvalues
"""

from .arithmetic import hecke_eigenvalue_ap
from .arithmetic import primes_up_to


def _kronecker_minus2(n: int) -> int:
    """Compute the Kronecker symbol (-2/n).

    (-2/n) = (-1/n) * (2/n) where:
      (-1/n) = (-1)^((n-1)/2)
      (2/n)  = (-1)^((n^2-1)/8)

    Returns 0 if n <= 0 or n is even.
    """
    if n <= 0 or n % 2 == 0:
        return 0

    # (-1/n) = (-1)^((n-1)/2)
    sign_minus1 = 1 if (n % 4 == 1) else -1

    # (2/n) = (-1)^((n^2-1)/8)
    r = n % 8
    sign_2 = 1 if r in (1, 7) else -1

    return sign_minus1 * sign_2


def eta_product_coefficients(N: int) -> list[int]:
    """Compute a_n for n=0..N-1 of eta(8z)*eta(16z) via direct q-expansion.

    eta(tau) = q^{1/24} * prod_{k>=1} (1 - q^k)

    eta(8z)*eta(16z) = q * prod_{k>=1} (1-q^{8k}) * prod_{k>=1} (1-q^{16k})

    where q = e^{2*pi*i*z}. We compute the product as polynomial multiplication
    in integer coefficients.
    """
    if N <= 0:
        return []

    coeffs = [0] * N
    if N > 1:
        coeffs[1] = 1  # leading term q^1

    # Multiply by prod_{k>=1} (1 - q^{8k})
    k = 1
    while 8 * k < N:
        step = 8 * k
        for j in range(N - 1, step - 1, -1):
            coeffs[j] -= coeffs[j - step]
        k += 1

    # Multiply by prod_{k>=1} (1 - q^{16k})
    k = 1
    while 16 * k < N:
        step = 16 * k
        for j in range(N - 1, step - 1, -1):
            coeffs[j] -= coeffs[j - step]
        k += 1

    return coeffs


def bolza_coefficients(N: int) -> list[int]:
    """Compute a_n for n=0..N-1 via Hecke multiplicativity.

    Uses the recurrence for prime powers:
      a_{p^{k+1}} = a_p * a_{p^k} - chi(p) * a_{p^{k-1}}

    where chi = Kronecker(-2/p) is the nebentypus.

    For composite n = m1 * m2 with gcd(m1, m2) = 1:
      a_n = a_{m1} * a_{m2}   (multiplicativity)
    """
    if N <= 0:
        return []

    coeffs = [0] * N
    if N > 1:
        coeffs[1] = 1

    primes = primes_up_to(N - 1)

    for p in primes:
        ap = hecke_eigenvalue_ap(p)
        chi_p = _kronecker_minus2(p)

        # Fill prime powers: a_{p^k} for k >= 1
        # a_{p^1} = a_p
        pk = p  # p^k
        a_prev = 1       # a_{p^0} = a_1 = 1
        a_curr = ap       # a_{p^1} = a_p

        while pk < N:
            # Multiply a_{p^k} into all coprime indices already computed
            # For each m with coeffs[m] != 0 and gcd(m, p) = 1 and m*pk < N:
            if a_curr != 0:
                # Walk through existing nonzero entries coprime to p
                for m in range(1, N // pk + 1):
                    if m % p == 0:
                        continue
                    if coeffs[m] != 0:
                        coeffs[m * pk] += coeffs[m] * a_curr

            # Advance to next power
            pk_next = pk * p
            if pk_next >= N:
                break
            a_next = ap * a_curr - chi_p * a_prev
            a_prev = a_curr
            a_curr = a_next
            pk = pk_next

    return coeffs
