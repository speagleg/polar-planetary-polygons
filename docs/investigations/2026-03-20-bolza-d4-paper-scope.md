# The Bolza D₄ Paper: Scope and Computation Plan

**Date:** 2026-03-20
**Status:** SCOPED (computations identified, partial results computed)
**Target:** Standalone article for J. Number Theory or IMRN

## The Result

The Bolza surface (genus 2, maximal automorphism group order 48) has
a stability threshold satisfying the palindromic quartic
ξ⁴ − 4ξ³ − 2ξ² − 4ξ + 1 = 0, with Galois group D₄ (dihedral, order 8,
NON-ABELIAN). By the Langlands–Tunnell theorem, the Artin L-function
of the 2-dimensional irrep ρ of D₄ corresponds to a weight-1 modular
form f, whose Hecke eigenvalues a_p encode the splitting of the Bolza
threshold at each prime p.

This is the first non-abelian case in the palindromic hierarchy
connecting vortex stability to automorphic forms.

## What Has Been Computed

### Palindromic quartic
ξ⁴ − 4ξ³ − 2ξ² − 4ξ + 1 = 0, coefficients [1,-4,-2,-4,1], palindromic ✓

### Roots
- Real pair: ξ = 0.2168, 4.6116 (product = 1)
- Complex pair: ξ = −0.414 ± 0.910i (on unit circle, |ξ| = 1)

### Field and Galois group
- Splitting field: K = Q(√2, √(2+2√2)) = Q(α), α⁴−4α²−4=0
- Polynomial discriminant: disc(α⁴−4α²−4) = −2¹⁶ = −65536
- Only p=2 ramifies
- Galois group: D₄ (verified: resolvent cubic has one rational root,
  discriminant of quartic is negative)

### Partial splitting table (root-counting mod p)
| p | #roots mod p | Type | a_p |
|---|---|---|---|
| 7 | 2 | partial | 0 |
| 17 | 0 | K-inert | −2 |
| 23 | 2 | partial | 0 |
| 31 | 2 | partial | 0 |
| 41 | 4 | split | 2 |
| 47 | 2 | partial | 0 |

Primes with complete splitting (a_p = 2) up to 200: {41, 113, 137}

## What Needs Sage/Magma/LMFDB

### 1. Artin conductor N
The conductor N = 2^k divides the field discriminant.
Compute: `Sage: NumberField(x^4-4*x^2-4).discriminant()` and
the conductor formula for D₄ representations.

### 2. Weight-1 modular form f
By Langlands–Tunnell: L(s,ρ) = L(s,f) for a weight-1 newform f
of level N and nebentypus det(ρ) = χ₂ = (·/2).
Search LMFDB for weight-1 forms of level 2^k with this nebentypus.

### 3. Full Hecke eigenvalue table
For the "Q(√2)-inert" primes (p ≡ 3,5 mod 8): the value of a_p
requires the full Frobenius computation in the D₄ extension.
The possible values are ±√2 (from the 2-dim irrep evaluated at
order-4 elements of D₄), which would mean a_p is IRRATIONAL —
a signature of the non-abelian case.

### 4. Visibility table for the Bolza surface
Analogous to Proposition 6.6 but with D₄ Frobenius instead of
Legendre symbols. The table would classify primes into 5 types
(one per conjugacy class of D₄).

### 5. Physical prediction
For each prime p: the Hecke eigenvalue a_p of f determines whether
the Bolza stability threshold receives an automorphic correction
on Γ₀(p)\H². The D₄ structure means the correction pattern is
richer than the abelian Z/2 case (split/inert/ramified → five types).

## Paper Structure (Draft)

1. Introduction: palindromic hierarchy, genus escalation
2. The Bolza palindromic quartic: derivation from vortex stability
3. The D₄ Galois group: proof and representation theory
4. The Artin conductor and weight-1 modular form (LMFDB identification)
5. Hecke eigenvalues and the Bolza visibility table
6. Comparison: abelian (genus 0, Legendre symbols) vs non-abelian (genus 2, Hecke)
7. The Takeuchi obstruction: why triangle groups can't go further
8. Open: non-solvable Galois from quaternion algebras over non-abelian fields

## Why This Is Publishable

- First connection between vortex stability and non-abelian Langlands
- Explicit computation (not abstract theory)
- The palindromic hierarchy gives a PHYSICAL escalator through the
  number-theoretic complexity ladder
- The Takeuchi obstruction (§7) shows the limits: all triangle groups
  give solvable Galois, and non-solvable requires leaving SL(2,Z) entirely
