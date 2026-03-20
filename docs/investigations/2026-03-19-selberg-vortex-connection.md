# Selberg Trace Formula and Vortex Stability on Quotient Surfaces

**Date:** 2026-03-19
**Status:** Framework established; specific computation needed

## The Connection

On a quotient surface Γ\H², the point vortex interaction uses the
**automorphic Green's function**:

G_Γ(z,w) = Σ_{γ∈Γ} G_H²(z, γw)

The stability eigenvalue on the quotient is:

λ_m^Γ = C₁(ξ) + δC₁(Γ) − m(N−m)/2

where δC₁(Γ) sums over non-trivial images:

δC₁ = Σ_{γ≠id} (4/Δ_γ) × F_m(γ)

with Δ_γ = tr(γ)² − 4 and F_m(γ) a mode-dependent geometric factor.

## Two expansions of the same quantity

The Selberg trace formula gives TWO ways to compute δC₁:

**Geometric side** (sum over geodesics):
δC₁ = Σ_γ (4/Δ_γ) × F_m(γ)

**Spectral side** (sum over Maass eigenvalues):
δC₁ = Σ_n a_n(m) / (1/4 + r_n²)

where {r_n} are the Maass eigenvalue parameters and a_n(m) are
Fourier coefficients determined by the test function.

## What this gives

The stability threshold on Γ\H² is determined by λ_m^Γ = 0:

C₁(ξ*_Γ) = m(N−m)/2 − δC₁(Γ)

The δC₁ term shifts the threshold away from the H² value.
On the geometric side, the shift is controlled by the geodesic
spectrum (shortest geodesic dominates). On the spectral side,
it's controlled by the Maass spectrum (lowest eigenvalue dominates).

## What this does NOT give

- No connection to the Riemann zeta function (the modular surface
  Maass spectrum is specific to SL(2,Z), not to ζ(s))
- No new information beyond what the automorphic Green's function
  already provides (the Selberg formula is a re-expansion, not new content)
- The five algebraic-integer thresholds on H² are NOT Maass eigenvalues
  (confirmed by Monte Carlo: p = 0.77, no correlation)

## Assessment

The Selberg connection is FORMAL: it provides an alternative expansion
of the stability correction on quotient surfaces. It does not produce
new predictions beyond what direct computation of the automorphic Green's
function gives. The value is organizational (connecting vortex stability
to spectral theory language) rather than computational.

The more productive direction is the non-constant curvature analysis
(oblate spheroids), which produces quantitative predictions for real
planetary atmospheres.
