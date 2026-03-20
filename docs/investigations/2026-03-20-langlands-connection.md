# The Langlands Connection: Genus 0 vs Genus 2

**Date:** 2026-03-20
**Status:** STRUCTURAL OBSERVATION (proven for genus 0; identified for genus 2)

## The Reviewer's Question

Is there a modular form whose Hecke eigenvalues encode the visibility
pattern of the stability thresholds?

## Genus 0: Class Field Theory (shallow)

The five threshold discriminants {5, 12, 32, 96, 252} have square-free
parts {5, 3, 2, 6, 7}, with four independent Legendre symbols
(2/p), (3/p), (5/p), (7/p).

The "vortex L-function" is:
  L_vortex(s) = L(s,χ₂)·L(s,χ₃)·L(s,χ₅)·L(s,χ₇)

This is the Artin L-function of the representation
ρ = χ₂ ⊕ χ₃ ⊕ χ₅ ⊕ χ₇ : Gal(Q̄/Q) → GL(4,C)

which factors through Gal(Q(√2,√3,√5,√7)/Q) ≅ (Z/2)⁴.

Since ρ is ABELIAN (direct sum of 1-dimensional characters), this is
a product of Dirichlet L-functions — class field theory, not Langlands.

## Genus 2 (Bolza): Non-Abelian Langlands (deep)

The Bolza threshold polynomial ξ⁴-4ξ³-2ξ²-4ξ+1 has:
- Splitting field Q(√2, √(2+2√2))
- Galois group **D₄** (dihedral of order 8) — **NON-ABELIAN**
- Discriminant -2¹¹ (negative → Gal ⊄ A₄)

D₄ has a 2-dimensional irreducible representation ρ.
The Artin L-function L(s, ρ) is a degree-2 L-function that is
NOT a product of Dirichlet characters.

By the Langlands correspondence (Tunnell 1981, for dihedral groups):
  L(s, ρ) = L(s, f) for a weight-1 modular form f on Γ₁(N)

where N is the Artin conductor (a power of 2 for this field).

The Hecke eigenvalues a_p of f encode the splitting of primes in
the quartic threshold field:
- a_p = 2: the Bolza threshold is fully visible at p
- a_p = 0: partially visible
- a_p = -2: inert

## Why Genus 2 Reaches Langlands but Genus 0 Doesn't

| Property | Genus 0 | Genus 2 |
|----------|---------|---------|
| Galois group | (Z/2)⁴ (abelian) | D₄ (non-abelian) |
| Representations | All 1-dim (characters) | Has 2-dim irrep ρ |
| L-function | Product of Dirichlet | Genuine Artin L-function |
| Modularity | Trivial (class field theory) | Non-trivial (Tunnell 1981) |
| Connected to | Quadratic reciprocity (1820s) | Langlands program (1970s+) |

The transition from genus 0 to genus 2 upgrades the number theory from
class field theory to the Langlands program. The Galois group changes
from abelian to non-abelian, and the L-function changes from a product
of characters to a genuine automorphic form.

## What Would Need to Be Done

1. Compute the Artin conductor of ρ (a power of 2)
2. Find the weight-1 modular form f on Γ₁(N) with L(s,f) = L(s,ρ)
3. Compute its Fourier coefficients a_p for small primes
4. Verify that a_p encodes the splitting of the Bolza threshold polynomial
5. Interpret a_p physically: what does the Hecke eigenvalue of f predict
   about vortex stability on the Bolza surface at prime p?

This is a concrete computation (not speculative), but requires tools
from computational algebraic number theory (e.g., Magma, Sage, or LMFDB).
