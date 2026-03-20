# Twin Primes and Shared Fibonacci Divisibility

**Date:** 2026-03-20
**Status:** VERIFIED (structural claim exact for p < 5000)

## The Result

For twin primes (p, p+2) with p ≡ 2 mod 5:
- (5/p) = −1, so α(p) | p+1
- (5/(p+2)) = +1, so α(p+2) | (p+2)−1 = p+1
- **Both Fibonacci entry points divide the same integer p+1**

Verified for all 40 such twin pairs up to p = 5000.

## Why This Is Unique to Twin Primes

The shared constraint requires g = (5/(p+g)) − (5/p) where g is the gap.
Since Legendre symbols are ±1, the maximum |g| is 2.
- g = 2 (twin primes): achievable when (5/p)=−1, (5/(p+2))=+1 ✓
- g = 4 (cousin primes): requires difference 4, IMPOSSIBLE
- g > 2: always impossible

**Twin primes are the ONLY prime gap with a shared Fibonacci
divisibility constraint.**

## Physical Interpretation

Both primes in a shared-constraint twin pair have their Fibonacci
stability thresholds controlled by the factorization of the single
integer p+1. If p+1 has only large prime factors, both α(p) and
α(p+2) are large → both primes are "stability-transparent" (weak
topological correction). If p+1 has small factors, the entry points
can be small → both primes are "stability-sensitive."

The stability fingerprints of twin primes are CORRELATED through
the arithmetic of p+1 — a phenomenon with no analogue for any
other prime gap.

## Connection to the Complementarity Proposition

For p ≡ 2 mod 5 (hence p ≡ 2 or 3 mod 5, (5/p) = −1):
- If also p ≡ 1 mod 4: α(p) is ODD (Proposition A.4(ii))
  → a_p(Bolza) ∈ {±2} (Proposition A.4(iii))
- The twin prime p+2 has (5/(p+2)) = +1
  → α(p+2) can be even or odd (not forced)

So the complementarity forces the Bolza threshold to be maximally
active at p but not necessarily at p+2. The twin prime pair has
ASYMMETRIC Bolza fingerprints even though their Fibonacci constraints
are symmetric (both | p+1).

## Examples

| p | p+2 | p+1 | α(p) | α(p+2) | gcd | Note |
|---|-----|-----|------|---------|-----|------|
| 17 | 19 | 18 | 9 | 18 | 9 | α(17) odd, a₁₇=-2 |
| 107 | 109 | 108 | 36 | 27 | 9 | |
| 227 | 229 | 228 | 228 | 114 | 114 | α(p) = p+1 (Wall prime) |
| 1487 | 1489 | 1488 | 1488 | 744 | 744 | Both near-maximal |
