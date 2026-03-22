"""Prime sieve using the Sieve of Eratosthenes."""


def primes_up_to(n: int) -> list[int]:
    """Return a list of all primes <= n using a bytearray sieve.

    Uses Sieve of Eratosthenes with bytearray for memory efficiency.
    """
    if n < 2:
        return []

    # sieve[i] == 0 means i is prime; 1 means composite
    sieve = bytearray(n + 1)
    sieve[0] = sieve[1] = 1

    i = 2
    while i * i <= n:
        if sieve[i] == 0:
            # Mark multiples of i starting from i*i
            for j in range(i * i, n + 1, i):
                sieve[j] = 1
        i += 1

    return [i for i in range(2, n + 1) if sieve[i] == 0]
