"""Modular arithmetic primitives for number-theoretic computations.

Implements Legendre symbol, Tonelli-Shanks, Fibonacci entry point,
Hecke eigenvalue computation for the Bolza form, and prime sieve.
"""


def legendre_symbol(a: int, p: int) -> int:
    """Compute the Legendre symbol (a/p) via Euler's criterion.

    Returns 1 if a is a quadratic residue mod p,
    -1 if a is a non-residue, 0 if p divides a.
    """
    if p < 2:
        raise ValueError(f"p must be an odd prime, got {p}")
    a = a % p
    if a == 0:
        return 0
    result = pow(a, (p - 1) // 2, p)
    # pow returns p-1 for non-residue; normalize to -1
    return result if result <= 1 else -1


def tonelli_shanks(n: int, p: int) -> int:
    """Compute r such that r^2 = n (mod p) using the Tonelli-Shanks algorithm.

    Returns the smaller of the two roots.
    Raises ValueError if n is not a quadratic residue mod p.
    """
    if legendre_symbol(n, p) != 1:
        raise ValueError(f"{n} is not a quadratic residue mod {p}")

    n = n % p

    # Special case: p = 2
    if p == 2:
        return n % 2

    # Case p ≡ 3 (mod 4): direct formula
    if p % 4 == 3:
        r = pow(n, (p + 1) // 4, p)
        return min(r, p - r)

    # Factor out powers of 2: p - 1 = Q * 2^S
    Q = p - 1
    S = 0
    while Q % 2 == 0:
        Q //= 2
        S += 1

    # Find a quadratic non-residue z
    z = 2
    while legendre_symbol(z, p) != -1:
        z += 1

    M = S
    c = pow(z, Q, p)
    t = pow(n, Q, p)
    R = pow(n, (Q + 1) // 2, p)

    while True:
        if t == 1:
            return min(R, p - R)

        # Find the least i such that t^{2^i} ≡ 1 (mod p)
        i = 1
        temp = (t * t) % p
        while temp != 1:
            temp = (temp * temp) % p
            i += 1

        # Update
        b = pow(c, 1 << (M - i - 1), p)
        M = i
        c = (b * b) % p
        t = (t * c) % p
        R = (R * b) % p


def sqrt2_mod_p(p: int) -> int:
    """Compute sqrt(2) mod p.

    Requires p ≡ 1 (mod 8) so that 2 is a quadratic residue.
    Returns the smaller root.
    """
    if p % 8 != 1:
        raise ValueError(f"p ≡ {p % 8} (mod 8), need p ≡ 1 (mod 8) for sqrt(2) to exist")
    return tonelli_shanks(2, p)


def _mat_mul_mod(A, B, mod):
    """Multiply two 2x2 matrices mod `mod`."""
    return [
        [(A[0][0] * B[0][0] + A[0][1] * B[1][0]) % mod,
         (A[0][0] * B[0][1] + A[0][1] * B[1][1]) % mod],
        [(A[1][0] * B[0][0] + A[1][1] * B[1][0]) % mod,
         (A[1][0] * B[0][1] + A[1][1] * B[1][1]) % mod],
    ]


def _mat_pow_mod(M, n, mod):
    """Compute M^n mod `mod` for a 2x2 matrix via repeated squaring."""
    result = [[1, 0], [0, 1]]  # identity
    base = [row[:] for row in M]
    while n > 0:
        if n % 2 == 1:
            result = _mat_mul_mod(result, base, mod)
        base = _mat_mul_mod(base, base, mod)
        n //= 2
    return result


def _fib_mod(k: int, p: int) -> int:
    """Compute F_k mod p using matrix exponentiation."""
    if k <= 0:
        return 0
    Q = [[1, 1], [1, 0]]
    return _mat_pow_mod(Q, k, p)[0][1]


def fibonacci_entry_point(p: int) -> int:
    """Compute alpha(p), the smallest k > 0 with F_k ≡ 0 (mod p).

    Uses the Pisano period bound:
      - If (5/p) = -1 (p ≡ ±2 mod 5): alpha(p) | (p+1)
      - If (5/p) =  1 (p ≡ ±1 mod 5): alpha(p) | (p-1)
      - If (5/p) =  0 (p = 5):         alpha(p) = 5

    Enumerates divisors in ascending order, returns the first where F_d ≡ 0.
    """
    if p == 5:
        return 5

    leg5 = legendre_symbol(5, p)
    if leg5 == -1:
        bound = p + 1
    else:
        bound = p - 1

    # Collect divisors of bound in ascending order
    divisors = []
    i = 1
    while i * i <= bound:
        if bound % i == 0:
            divisors.append(i)
            if i != bound // i:
                divisors.append(bound // i)
        i += 1
    divisors.sort()

    for d in divisors:
        if d > 0 and _fib_mod(d, p) == 0:
            return d

    # Fallback: should not reach here for prime p
    raise RuntimeError(f"Failed to find Fibonacci entry point for p={p}")


def hecke_eigenvalue_ap(p: int) -> int:
    """Compute a_p for the Bolza form eta(8z)*eta(16z) (level 128, weight 1).

    For p = 2 or p not ≡ 1 (mod 8): returns 0.
    Otherwise: s = sqrt(2) mod p; returns 2 * legendre_symbol(1 + s, p).
    """
    if p == 2 or p % 8 != 1:
        return 0
    s = sqrt2_mod_p(p)
    return 2 * legendre_symbol((1 + s) % p, p)


def primes_up_to(n):
    """Sieve of Eratosthenes: all primes up to n."""
    if n < 2:
        return []
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, n + 1, i):
                sieve[j] = False
    return [i for i in range(2, n + 1) if sieve[i]]
