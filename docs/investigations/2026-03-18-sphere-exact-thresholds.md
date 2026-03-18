# Q3: S² stability thresholds — exact rational fractions and geometric interpretation

**Date:** 2026-03-18
**Status:** Resolved — ξ_crit(N) ∈ ℚ exactly; C₁(S²,ξ) = (N-1)cos φ.

---

## The question

The colatitude table in the paper gave numerical values
(φ_crit(6) ≈ 26.6°).  Are there exact closed forms, and what geometric
quantity does ξ_crit represent?

---

## The stereographic identity

In stereographic projection from the south pole, the Poincaré disk
parameter ξ = tan²(φ/2) (where φ is the colatitude).  The spherical
Green's function C₁ becomes:

    C₁(S², ξ) = (N-1)(1-ξ)/(1+ξ) = (N-1) cos φ

using cos φ = (1-ξ)/(1+ξ).  So the stability coefficient is simply
**(N-1) times the cosine of the colatitude**.

---

## Marginal stability condition

Setting C₁ = T_half = m(N-m)/2 (m = floor(N/2)) gives:

    cos(φ_crit) = m(N-m) / (2(N-1))   ∈ ℚ   (always rational)

Exact threshold table:

| N | m(N-m)/2 | cos(φ_crit) | ξ_crit  | φ_crit    |
|---|----------|-------------|---------|-----------|
| 3 | 1        | 1/2         | 1/3     | 60.0°     |
| 4 | 2        | 2/3         | 1/5     | 48.2°     |
| 5 | 3        | 3/4         | 1/7     | 41.4°     |
| 6 | 9/2      | 9/10        | 1/19    | 25.84°    |
| 7 | 6        | 6/6 = 1     | 0       | 0° (marginal) |
| ≥8 | >N-1   | <0          | None    | none      |

---

## Why the thresholds are rational despite transcendental Green's function

The S² Green's function h(θ) = -ln(2 sin(θ/2)) is transcendental in θ.
Yet the stability threshold is rational because:

1. C₁(S², ξ) = (N-1)(1-ξ)/(1+ξ) is a rational function of ξ
2. The marginal condition C₁ = T_half is linear in (1-ξ)/(1+ξ)
3. Solving for ξ gives a ratio of linear functions → ξ_crit ∈ ℚ

The transcendentality is "hidden" in the conversion θ ↔ ξ; the stability
analysis is algebraic in ξ.

---

## The 1/(2N-3) pattern and its break at N=6

For N=3,4,5: m(N-m)/2 = N-2 exactly, so:
- numerator of ξ_crit = (N-1) - (N-2) = 1
- denominator = (N-1) + (N-2) = 2N-3
- ξ_crit = 1/(2N-3)

At N=6: m(N-m)/2 = 9/2 ≠ N-2 = 4, because the hexagonal mode
(m=3, N-m=3) has a larger Havelock eigenvalue (λ_min = 1/2 vs 1 for
N≤5).  This gives ξ_crit(6) = 1/19, not 1/9.

---

## Exact vs numerical comparison

The paper's value φ_crit(6) = 26.6° (from a dimensionless λ̄ = sin²φ · λ
convention) vs the exact value arccos(9/10) ≈ 25.84°.  The <1°
discrepancy reflects the normalization convention; the exact result
is cos(φ_crit(6)) = 9/10 regardless.

---

## Relevant code

- `algebraic_thresholds.sphere_stability_threshold(N)` — exact Fraction result
- `algebraic_thresholds.sphere_threshold_table()` — table for N=3..12
- `test_algebraic_thresholds.test_sphere_threshold_satisfies_C1_condition` —
  exact rational verification using Python Fraction arithmetic
