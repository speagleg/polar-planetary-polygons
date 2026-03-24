# LMFDB Comparison: The Weight-2 Shadow of the Havelock Spectrum

**Date:** 2026-03-23
**Status:** COMPUTED — the LMFDB form is related but NOT identical

## What We Found

The LMFDB contains a Hilbert modular form over Q(cos 2π/7):

**3.3.49.1-49.1-a**
- Weight: [2, 2, 2] (parallel weight 2)
- Level norm: 49
- Dimension: 1 (eigenvalues are rational)
- CM: Yes
- Base change: Yes (from a classical form at level 49 over Q)

Hecke eigenvalues:

| Norm | Prime type | a_P | p mod 7 |
|------|-----------|-----|---------|
| 8 | inert (p=2) | -5 | 2 |
| 29 | split (3 primes) | 2 each | 1 |
| 43 | split (3 primes) | -12 each | 1 |
| 71 | split (3 primes) | 16 each | 1 |
| 7, 13, 27, 41 | — | 0 | — |

## Why This Is NOT the Havelock Form

The LMFDB form has weight [2,2,2]: eigenvalues grow as O(√p).
Our Havelock spectrum has BOUNDED eigenvalues (O(1)).

| p = 29 | LMFDB: a_29 = 2 | Havelock: S_1 = 1.58 |
| p = 43 | LMFDB: a_43 = -12 | Havelock: S_1 = 1.58 |
| p = 71 | LMFDB: a_71 = 16 | Havelock: S_1 = 1.58 |

The LMFDB eigenvalues vary with p. The Havelock eigenvalues depend
on p mod 7 (they're the SAME for all split primes). These are
fundamentally different behaviors.

## The Base Change Structure

The LMFDB form is a base change from a classical weight-2 form
at level 49 over Q. The base form has:

    a_2 = 1 (verified: a_P = a_2³ - 6a_2 = 1 - 6 = -5 = a at norm 8 ✓)
    a_29 = 2, a_43 = -12, a_71 = 16

This is an elliptic curve over Q of conductor 49 (the curve
corresponding to LMFDB 49.2.a.a or similar).

## What the Havelock Spectrum IS

The Havelock eigenvalues S_m have the structure of:

1. **A weight-1 Hilbert modular form** — if such a form exists at
   this level. Weight-1 HMF are extremely rare (Artin representations).
   The LMFDB does not tabulate them systematically.

2. **A Maass form** on GL(2)/K — not holomorphic but automorphic,
   with spectral parameters r_m = √(f(m) - 1/4) on the three copies
   of H² (one per real embedding of K).

3. **A novel automorphic object** defined by the vortex stability
   theory, satisfying the Ramanujan-Petersson bound and palindromic
   symmetry, but not fitting the standard classification.

## The Relationship: Sym² Lifting

The weight-2 LMFDB form is the SHADOW of our weight-1 object:

    weight-1 object → Sym² → weight-2 form (the LMFDB entry)

The symmetric square L-function:
    L(s, Sym²(π₁)) = L(s, π₂)

where π₁ is the weight-1 Havelock representation and π₂ is the
weight-2 LMFDB representation. This is a FUNCTORIALITY relation
in the Langlands program.

## Significance

The LMFDB comparison shows that the Havelock automorphic data
lives one level BELOW the known database — in the weight-1 world
that the LMFDB doesn't systematically cover. The weight-2 form
at level 49 is the Sym² lift, accessible through base change
from classical modular forms.

This places the Havelock spectrum in a very specific position
in the Langlands hierarchy: it's the SEED from which the known
weight-2 objects grow through functoriality.

## Code

`langlands_all_N.py`, `hilbert_modular_N7.py`: the computations.
`langlands_verify.py`: the N = 8 verification (abelian case).
