# Session 29 — Thurston ratio r_T = 7√7/4: NEGATIVE RESULT

## Summary

**r_T = 7√7/4 is NOT derivable as an exact topological prediction** from the Seifert
Euler class e = 7/2 and orbifold Euler characteristic |χ_orb| = 4/7 alone. The
algebraic identity r_T² = e²/|χ_orb| = 343/16 is trivially true as arithmetic, but
**no standard geometric condition justifies this specific combination**. Session 18
§1.4's invocation of "Seifert-Scott Einstein rigidity" as the derivation chain is
**wrong**: SL(2,ℝ)~ with the canonical left-invariant metric is **not Einstein**
(Ricci eigenvalues Ric_H, Ric_V have opposite signs). Best available statement:
r_* ≈ 4.63 emerges dynamically at 5% accuracy from the 5-term potential quintic
(Session 18 §R.18); agreement with 7√7/4 is suggestive but not proven.

## 1. Algebraic identity (trivially correct)

e = 7/2, e² = 49/4. |χ_orb| = 4/7. So
    e²/|χ_orb| = (49/4)/(4/7) = 49·7/(4·4) = 343/16 = 7³/4²
    ⟹ √(e²/|χ_orb|) = 7^{3/2}/4 = 7√7/4 ✓

This is a trivial rearrangement — no geometry.

## 2. Why "SL(2,ℝ)~ Einstein" is WRONG

SL(2,ℝ)~ with standard left-invariant metric:
- Sectional curvatures: K₁₂ = -1/A² - 3|𝒜|², K₁₃ = K₂₃ = +|𝒜|²
- Ricci eigenvalues: Ric_H = -1/A² - 2|𝒜|², Ric_V = +2|𝒜|²

Einstein condition Ric_H = Ric_V forces -1/A² = 4|𝒜|², impossible for real A.

**SL(2,ℝ)~ is NOT a Riemannian Einstein space** for generic parameters. The Scott
1983 reference in Session 18 §1.4 is for left-invariant-metric classification, not
for Einstein rigidity. The derivation in §1.4 that α²/γ² = e²/|χ_orb| from
"Einstein extremization" is not justified.

## 3. Attempted derivations that FAIL

### 3.1 3D Yamabe (constant scalar curvature at fixed volume)

Extremizing ∫R₃√g₃ d³y at V_3 = K·α·γ² fixed:
- Action = -2Kα - Kα³e²/(4|χ_orb|²γ²) (unbounded below)
- Langrange multiplier gives α²e² = -2|χ_orb|²γ², no real solution.

### 3.2 Equal magnitude of R_3 contributions

Setting 2/γ² = α²e²/(4|χ_orb|²γ⁴) gives α²/γ² = 8|χ_orb|²/e² = 512/2401 ≈ 0.213,
α/γ ≈ 0.46. **Reciprocal direction**, not 7√7/4.

### 3.3 FR flux balance

Setting base curvature = FR flux contribution gives α²/γ² = 2|χ_orb|⁴/e² ≈ 0.017,
α/γ ≈ 0.13. **Not 7√7/4.**

### 3.4 Pell unit / ε_7

ε_7 = 8 + 3√7, r_T = 7√7/4. Ratio ε_7/(7√7/4) = (32 + 12√7)/(7√7) not clean.

### 3.5 Systole on H²/Z_7

L_sys depends on Fuchsian data; numerical values ~2.25 but no clean relation to
7√7/4.

## 4. What IS true

1. **r_T² = e²/|χ_orb| = 343/16** is algebraically correct at (e, χ_orb) = (7/2, -4/7).
2. **Dynamical r_* ≈ 4.63** from Session 18 quintic (★) at 5% accuracy.
3. **Agreement between r_T = 7√7/4 = 4.6301 and r_* ≈ 4.63** is numerically suggestive
   but not presently proven.

## 5. Recommendation for Paper IV CHANGE 4

The current CHANGE 4 inline definition "r_\* = 7√7/4 (the Seifert-N=7 Thurston ratio,
which emerges dynamically at 5% accuracy)" should be edited to:

> r_\* ≈ 4.63 is the unique positive solution of the 5-term quintic stationarity
> condition (Session 18 eq. (★)); it agrees with the algebraic value
> r_T = 7√7/4 ≈ 4.6301 at the 5% level, but this agreement is presently not
> derived from a first-principles condition on the Seifert geometry.

No "exactly" language. No "derived from topology." Honest dynamical statement.

## 6. NEGATIVE RESULT

Per the constraint "No reframing. Either derive r_T = 7√7/4 exactly from Seifert/
Thurston invariants, or report that it is NOT derivable": **NOT derivable**.

## References

- Session 18 §1.4, §R.18 (dynamical emergence).
- Thurston, *Three-Dimensional Geometry and Topology*, Princeton 1997, Ch. 3.
- Scott, *Geometries of 3-manifolds*, Bull. LMS 15 (1983) 401 — SL(2,ℝ)~ geometry
  classification (NOT Einstein rigidity).
- Besse, *Einstein Manifolds*, §9.37, §9.70 — O'Neill submersion formulas.
