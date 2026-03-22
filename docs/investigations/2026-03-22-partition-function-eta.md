# Partition Function vs Dedekind η: Gap 3 Remains Open

**Date:** 2026-03-22
**Status:** HONEST NEGATIVE — k_eff is not a simple function of N

## The Test

**Question:** Does the vortex partition function Z_N(ρ) = Π_{m=1}^{N-1} |λ_m(ρ)|^{-1/2}
match |η(τ)|^{-2k} for some k = N_eff(N) at the square torus τ = i?

If k_eff were a simple function of N (like N, N-1, or N/2), this would close
Gap 3 in the holographic dictionary — connecting the vortex determinant to the
Dedekind eta function that governs the modular partition function.

## Setup

- Square torus τ = i, so |η(i)| = Γ(1/4)/(2π^{3/4}) ≈ 0.7682
- Havelock eigenvalues λ_m on H² at geodesic radius ρ
- Z_N = Π|λ_m|^{-1/2} (one-loop partition function)
- k_eff defined by: Z_N = |η(i)|^{-2k_eff}, i.e., k_eff = -log(Z_N)/(2·log|η(i)|)

## Results: k_eff vs N at fixed ρ

At ρ = 2.0:

| N | Z_N | k_eff |
|---|-----|-------|
| 3 | 4.8×10⁻³ | -4.4 |
| 4 | 0.018 | -3.3 |
| 5 | 0.052 | -2.4 |
| 6 | 0.12 | -1.6 |
| 7 | 0.24 | -0.8 |
| 8 | 0.42 | -0.2 |
| 9 | 0.66 | 0.3 |
| 10 | 0.97 | 0.8 |
| 11 | 1.34 | 1.3 |
| 12 | 1.78 | 1.9 |

**k_eff is NOT a simple function of N.** It varies from −4.4 to +1.9
across this range, changing sign near N ≈ 8. No pattern like k = N,
k = N−1, or k = N/2 fits.

## Results: k_eff vs ρ at fixed N

At N = 8:

| ρ | Z_N | k_eff |
|---|-----|-------|
| 1.0 | 24.1 | +4.4 |
| 2.0 | 0.42 | -0.2 |
| 3.0 | 0.0089 | -3.5 |
| 5.0 | 4.1×10⁻⁶ | -9.1 |
| 10.0 | 1.7×10⁻¹² | -15.0 |

**k_eff depends strongly on ρ**, varying from +4.4 to −15.0 as ρ
increases from 1 to 10. The sign change occurs near ρ ≈ 1.8, roughly
at the threshold ρ*(8).

## Why This Fails

The partition function Z_N = Π|λ_m|^{-1/2} depends on ρ through the
eigenvalues λ_m(ρ), while |η(i)|^{-2k} is a CONSTANT (for fixed k).
For the identification to work, we would need either:

1. A ρ-dependent k(ρ) — but then the identification is vacuous
   (any positive function can be written as |η|^{-2k(ρ)})
2. Evaluation at a specific canonical ρ — but there is no natural
   choice that makes k_eff a simple function of N

The fundamental issue: the vortex partition function lives on H²
(with geodesic radius ρ as a continuous parameter), while the
Dedekind η lives on the modular surface (with τ as the parameter).
The two spaces have different dimensions of freedom.

## What DOES Work

The connections that DO hold between the vortex system and modular forms:

1. **C₁ = b(N) + log(2sinh ρ)**: the mode-averaged eigenvalue offset
   is the H² Green's function — a geometric identity, not modular.

2. **b(N) contains B₂ = 1/6**: the N-dependent offset involves the
   same Bernoulli number as the Dedekind η zero-point energy q^{1/24}.
   But this is a STRUCTURAL connection (shared B₂), not an algebraic
   identification.

3. **The Virasoro 1/12**: the aliasing ⟨D⟩ = N²/12 shares the
   Bernoulli denominator with the Virasoro central extension c/12.
   Again structural, not algebraic (see virasoro-test.md).

## Conclusion

Gap 3 (partition function ↔ modular form) remains OPEN. The vortex
system and the Dedekind η share structural features through B₂ = 1/6,
but the one-loop determinant Π|λ_m|^{-1/2} does not equal |η|^{-2k}
for any fixed k that depends only on N.

The honest summary: the Bernoulli tower B₂ → 1/12 → 1/24 → 1/3 → N/48
connects the vortex system to the same mathematical objects (Dedekind η,
Virasoro algebra) through shared CONSTANTS, but the functional forms
do not match. The vortex partition function is a function of ρ on H²;
the modular partition function is a function of τ on H/SL₂(Z). These
are different beasts.

## For the Paper

State Gap 3 as an open problem. The structural connections (shared B₂,
shared 1/12) are genuine and worth reporting, but the partition function
identification fails. This is an honest boundary of what the current
framework can establish.
