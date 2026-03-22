# N_crit by Spatial Dimension

**Date:** 2026-03-22
**Status:** COMPUTED (numerical, all dimensions d = 2,...,5)

## The Result

| d | s = d−2 | N_crit | Interaction | Key observation |
|---|---------|--------|-------------|-----------------|
| 2 | 0 (log) | **7** | Point vortex | Havelock 1931 |
| 3 | 1 (1/r) | **5** | Coulomb | Hexagon LOST |
| 4 | 2 (1/r²) | **5** | 4D potential | Same as d=3 |
| 5 | 3 (1/r³) | **5** | 5D potential | Same as d=3 |

N_crit drops from 7 to 5 at d = 3 and stays at 5 for d ≥ 3.

## The Hexagon is Uniquely 2D

N=6 stability margin by dimension:
- d=2: λ_min = +0.500 (stable, margin 0.5)
- d=3: λ_min = −0.018 (UNSTABLE, barely)
- d=4: λ_min = −1.083 (unstable)
- d=5: λ_min = −2.926 (unstable)

Saturn's hexagon requires the logarithmic (2D) interaction.

## The Soft Havelock Decomposition

For s ≥ 1 (d ≥ 3): the angular Casimir σ_m^(s) is NOT a polynomial
in m, but decomposes as:

$$\sigma_m^{(s)} = a(N,s) \cdot m(N-m)/2 + R_m$$

where a(N,s) is a least-squares fit coefficient and R_m is the residual.
The mode ordering is PRESERVED: |R_m − R_{m'}| < a|f_m − f_{m'}| for
all adjacent pairs, for all tested N = 5,...,20 and s = 1,2,3.

Only s = 2 (the logarithmic case) gives an EXACT polynomial Casimir.
This is because csc²(πp/N) has a closed discrete Fourier transform
while csc^s for s ≠ 2 does not.

## Why the Logarithmic Interaction is Special

The rich algebraic structure of the palindromic hierarchy (Paper I)
arises from the csc² weight function, which is the UNIQUE power of
csc that gives a polynomial Fourier eigenvalue. In higher dimensions:
- The Casimir is transcendental (no closed form)
- The mode ordering is preserved (soft Havelock)
- But the palindromic POLYNOMIALS don't exist
- The algebraic number fields are absent
- The modular forms don't appear

The number theory is a 2D phenomenon.
