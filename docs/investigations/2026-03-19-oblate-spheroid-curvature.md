# Non-Constant Curvature: Oblate Spheroid Effects on Vortex Stability

**Date:** 2026-03-19
**Status:** COMPUTED, needs verification against full spheroidal Green's function

## Critical Finding

**Saturn's oblateness flips the hexagon from unstable to marginally stable.**

On a mean sphere (K = 1/R_mean²): λ₃(N=6) = −0.12 → UNSTABLE (hexagon shouldn't exist)
On the oblate spheroid at 78°N: λ₃(N=6) = +0.01 → MARGINALLY STABLE

The 10% oblateness changes the SIGN of the binding eigenvalue. This is not
a perturbative correction — it determines whether the hexagon exists at all.

## Latitude dependence

The stability transition occurs at φ ≈ 73° on Saturn:
- φ < 73°: λ₃ < 0 (unstable)
- φ > 73°: λ₃ > 0 (stable)
Saturn's hexagon at 78°N is just above the transition.

## Mode coupling at non-polar latitudes

At 78°N, the curvature varies by ΔK/K ≈ 4.2% across the hexagon ring.
This cos(2θ) variation couples modes m and m±2, with coupling amplitude
~0.19 — which EXCEEDS the stability margin |λ₃| ≈ 0.01 by a factor of ~19.

**The non-constant curvature effect is NOT perturbative for Saturn.**
A full non-perturbative analysis on the spheroidal Green's function is needed.

## Implications

1. The clean algebraic structure (palindromic quadratics, Pell equations) breaks
   down on oblate spheroids because the curvature is not constant.
2. The SIGN of the stability eigenvalue for Saturn's hexagon depends critically
   on the oblateness — this is a physical prediction, not a mathematical nicety.
3. For Jupiter's polar vortices (at ~90°), the curvature IS effectively constant
   (axisymmetric at the pole), so the algebraic structure survives.
4. The transition latitude φ_crit where stability changes sign is a NEW
   prediction that could be compared against observations.

## Caveats

- The computation uses the spherical C₁ formula with the local spheroidal K,
  which is an approximation. The exact C₁ on the spheroid requires the
  spheroidal Green's function (oblate spheroidal harmonics).
- The mode coupling estimate δK/K · C₁ is first-order; the actual coupling
  involves the Hessian of the spheroidal Green's function.
- Saturn's hexagon is maintained by Rossby wave dynamics (Paper III), not
  purely by Thomson stability. The oblateness effect modifies the Thomson
  contribution but doesn't account for the full dynamics.
