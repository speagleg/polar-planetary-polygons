# Q2: Does χ (Euler characteristic) enter N_crit at O(K²)?

**Date:** 2026-03-18
**Status:** Resolved — χ enters at O(χ), not O(K²).

---

## The question

On a compact surface with Euler characteristic χ, does the critical polygon
count N_crit receive an O(K²) correction (where K is total circulation)
mediated by the Gauss-Bonnet theorem?

---

## The mechanism: background vorticity neutrality

On a compact surface (S², torus, etc.) with total area A, global vorticity
conservation forces

    Σ_k κ_k + κ_background · A = 0

where κ_background is the background vorticity density (images, "anti-vortex
sheet") required by the Green's function having no constant term.

For S² (χ = 2), the Gauss-Bonnet theorem gives

    ∫_S² K_Gaussian dA = 4π = 2πχ

This introduces an additive constant into the Green's function:

    G_{S²}(z, w) = -½ ln|z - w|² + ½ ln|z|² + ½ ln|w|² + C(N, R)

The correction C(N, R) shifts **all** Havelock eigenvalues uniformly by a
term of order χ/N (after normalization), not O(K²).

---

## Why O(χ), not O(K²)

The Havelock eigenvalue formula on H² is (§5, Riemannian Havelock identity):

    λ_m · r_E² = C₁(surface, ξ) - m(N-m)/2

The curvature-dependent coefficient C₁ enters at O(1) in the ring geometry
parameters.  The O(K²) expansion of the energy arises from the *amplitude*
of each vortex pair interaction, not from the topological correction.

The Gauss-Bonnet correction modifies C₁ by adding a term proportional to χ:

    C₁(S², ξ)   = (N-1)(1-ξ)/(1+ξ)      [no O(K²) dependence]
    C₁(H², ξ)   = (N-1)(1+ξ²)/(1-ξ)²    [no O(K²) dependence]

Both are independent of K.  The topology enters through the geometry of the
Green's function on the surface — this is an O(χ) correction to the
*eigenvalue constant*, not a K-dependent amplitude.

---

## Explicit check: N_crit on S² vs H²

| Surface  | N_crit (flat limit) | Mechanism               |
|----------|---------------------|-------------------------|
| Flat ℝ²  | 7 (Thomson)         | no topology             |
| S²       | ≤ 6 (destabilized)  | χ = +2 decreases C₁     |
| H²       | ≥ 7 (stabilized)    | χ = -∞ (neg curvature)  |

The S² result (N_crit drops from 7 to ≤ 6) is entirely captured by
C₁(S², ξ) < N-1 for ξ > 0 — a **topological/geometric** O(χ) effect.

---

## Conclusion

The Euler characteristic enters N_crit at **O(χ)** through the surface Green's
function and Havelock eigenvalue constant C₁(surface, ξ), not at O(K²).
The K² dependence would require a coupling between total circulation strength
and the eigenvalue structure that is not present in the point-vortex model at
leading order.

An O(K²) correction *would* appear if one considered finite-area vortex patches
(blob corrections, §6.4) — but that is a self-energy effect independent of
surface topology.

---

## Relevant code

- `h2_stability.C1_h2_exact(N, xi)` — C₁ on H²
- `riemannian_havelock.C1_sphere(N, xi)` — C₁ on S²
- `algebraic_thresholds.sphere_stability_threshold(N)` — exact rational S² thresholds
- `algebraic_thresholds.h2_stability_threshold(N)` — H² thresholds and field extensions
