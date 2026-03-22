# The Virasoro Test: Havelock Modes and the Central Extension

**Date:** 2026-03-22
**Status:** TESTED — partial connection, not full Virasoro

## The Question

Does the Havelock mode algebra on the vortex ring reproduce the
Virasoro algebra in the N → ∞ limit, with the 1/12 aliasing
coefficient playing the role of c/12 in the central extension?

## What Was Computed

### The aliasing profile D(m, N)

D(m, N) is the deviation of the discrete Havelock sum from the
continuum prediction, computed for N = 12, 20, 30, 50 across all modes.

The quadratic fit D(m) = α·m² + β·m + γ gives:
- The m² coefficient α is NEGATIVE (≈ -0.32 to -0.48)
- This gives a negative "effective central charge" c_eff ≈ -50 to -290
- The Virasoro prediction requires POSITIVE m² coefficient

### The scaling D(m, N) at fixed r = m/N

D/N grows linearly in N at fixed r, confirming D ∝ N² overall.
The profile D(m, N)/N² does NOT match π·cot(πr)/2 (the digamma
prediction) — the ratio varies from 0.9 to 10⁴ depending on r.

## What Connects

### The 1/12 coefficient IS the Bernoulli number B₂/2

The mean aliasing ⟨D⟩ = N²/12 and the Virasoro central term c/12
share the factor 1/12. Both arise from B₂ = 1/6:
- **Havelock:** ⟨D⟩ = B₂·N²/2 from the Euler-Maclaurin correction
  to the log-sine Fourier sum on Z/NZ.
- **Virasoro:** c/12 = B₂·c/2 from the regularisation of the
  commutator [L_m, L_n] via zeta function (ζ(-1) = -B₂/2 = -1/12).

Both are Euler-Maclaurin corrections to the same log-sine kernel,
but at different levels: the Havelock on Z/NZ (finite polygon),
the Virasoro on Z (the full infinite tower of modes).

### The Casimir limit

For m ≪ N: the Havelock Casimir m(N-m)/2 ≈ mN/2 becomes linear
in m, matching the U(1) charge (the L₀ eigenvalue). The Virasoro
structure requires the QUADRATIC correction m² which enters through
the aliasing D(m, N). But D has the WRONG SIGN for the Virasoro
central extension at finite N.

## What Doesn't Connect

### The mode profile is wrong

D(m, N) = -0.45·m² + 13.6·m + 7.5 (for N = 30). The negative
m² coefficient means the aliasing DECREASES faster than m(N-m)/2
for central modes. The Virasoro central extension (m³-m) would
require D to GROW for large m. The profile is concave when it
should be convex.

### The Poisson bracket structure is absent

The vortex modes on a finite ring are ZN Fourier modes. Their Poisson
brackets {A_m, A_n} are diagonal at quadratic order (different modes
are independent). The Virasoro commutator [L_m, L_n] = (m-n)L_{m+n}
requires OFF-DIAGONAL coupling, which appears only at CUBIC order
in the vortex Hamiltonian. The cubic coupling C_{m,n,-(m+n)} exists
but was not computed.

## The Honest Conclusion

The 1/12 in the Havelock aliasing and the 1/12 in the Virasoro central
charge have a COMMON ORIGIN (the Bernoulli number B₂) but are NOT
the same object. The Havelock aliasing is a SCALAR correction to the
mode-averaged eigenvalue; the Virasoro central extension is a STRUCTURE
CONSTANT of an infinite-dimensional Lie algebra. They share the 1/12
because both involve the Euler-Maclaurin correction to the log-sine
kernel, but the Havelock version is the TRACE of the correction
(averaged over modes) while the Virasoro version is the MODE-DEPENDENT
correction (the m³ - m pattern).

The N → ∞ limit of the Havelock modes likely DOES produce the Virasoro
algebra, but the identification requires going beyond the quadratic
(Havelock eigenvalue) level to the CUBIC (mode-mode coupling) level
of the vortex Hamiltonian. The central charge would emerge from the
third-order Hamiltonian, not from the second-order aliasing.

## For the Paper

State the B₂ connection as a STRUCTURAL parallel, not as a derivation
of the Virasoro algebra from the Havelock modes. The growth law
theorem (a = 1/3 from B₂) is rigorous. The Virasoro interpretation
is suggestive but unproven — it would require computing the cubic
coupling and taking the N → ∞ limit, which is a separate project.

## Code

- D(m, N) profile: discrete Havelock sum vs continuum prediction
- Quadratic fit: D = α·m² + β·m + γ at each N
- Effective central charge: c_eff = 12·α·N (gives negative values)
- All computation inline
