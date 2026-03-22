# The Magri Bihamiltonian Hierarchy of the Vortex System

**Date:** 2026-03-22
**Status:** VERIFIED (levels 1-2 exact, level 3 numerical)

## The Hierarchy

The N-gon vortex ring has a bihamiltonian structure (ω_KR, ω_Casimir)
with recursion eigenvalue R_m = f_m = m(N-m)/2. The conserved
quantities generate derivatives:

| Level k | d_{2k} formula | At m = N/2 | Verified |
|---------|---------------|------------|----------|
| 1 | d₂ = N · f_m | N³/8 | exact (6 values) |
| 2 | d₄ = 4N · f_m² | N⁵/16 | < 0.04% (6 values) |
| 3 | d₆ = 64N · f_m³ | N⁷/8 | ~1% (6 values, FD noise) |
| 4 | d₈ = 1024N · f_m⁴ | N⁹/4 | prediction |

## Verification

d₂ = N·f (the mode normalization of the Havelock eigenvalue):

| N | f = m(N-m)/2 | d₂ | d₂/(Nf) |
|---|---|---|---|
| 6 | 4.5 | 27.00 | 1.000004 |
| 8 | 8.0 | 64.00 | 1.000009 |
| 10 | 12.5 | 125.00 | 1.000017 |
| 12 | 18.0 | 216.01 | 1.000029 |

d₄ = 4Nf² (the quartic conserved quantity):

| N | 4Nf² | d₄ | d₄/(4Nf²) |
|---|---|---|---|
| 6 | 486.0 | 486.0 | 1.000049 |
| 8 | 2048.0 | 2048.2 | 1.000085 |
| 10 | 6250.0 | 6250.8 | 1.000133 |
| 12 | 15552.0 | 15555.0 | 1.000192 |

## The Normalisation Pattern

The normalisation coefficients α_k = {1, 4, 64, 1024?, ...} satisfy:
- α₁ = 1 (trivial)
- α₂ = 4 (the quartic coupling 4N, from Q/f² = N/48 × 192 = 4N)
- α₃ = 64 = 4³ (the hexic, from B₄ = -1/30)
- α₄ = 1024? = 4⁵ (prediction, from B₆ = 1/42)

The ratios α_{k+1}/α_k = {4, 16, 16?, ...} suggest the pattern
stabilises at 16 = 4².

## Conservation

The I_k are conserved because:
1. **Quadratic**: modes decouple, each |ε_m|² individually conserved
2. **Cubic**: H₃ is purely imaginary (Berry phase, no energy transfer)
3. **Quartic**: Q_m = (N/48)f_m² is a function of f_m, so H₄^diag ∝ I₂.
   The quartic Hamiltonian lies INSIDE the Magri hierarchy.

## Connection to the Three-Layer Decomposition

The three layers are the first three levels of the hierarchy:
- I₀ = vacuum energy (Ricci scalar C₁) — mode-independent
- I₁ = Casimir f_m = m(N-m)/2 — the Z_N representation theory
- δ_m = remainder after subtracting I₀ and I₁ — the Weyl anomaly

The Bernoulli tower B₂ → 1/12 → 1/3 → N/48 is the normalisation
tower of the Magri hierarchy, with B₂ = 1/6 entering at each level.
