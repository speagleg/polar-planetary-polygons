# Session 34 — Derivation of M_rad at N=11: Scenario B (approximate ≈ N/2 at 10% level)

## Bottom line

**M_rad = N/2 is NOT exactly derivable from the Paper VI tree-level radion potential.**
The derived value is ω ∈ [5.86, 6.77] depending on kinetic normalization, vs the
asserted N/2 = 5.5. Paper VI's claimed 0.3σ Planck agreement for Ω_Λ relies on this
assertion; after derivation, agreement is 0.4σ (log-frame K=1) to 1.4σ (Session 18
Einstein frame G_11=3/4). Framework prediction Ω_Λ ≈ 68.5-69.5% survives, but not at
the sub-σ precision Paper VI claims.

## Inputs at N=11

- b(11) = 10.547 (Paper III closed form)
- c_11 = 12·b(11) = 126.56
- Λ = (N²-16)/16 = 105/16 = 6.5625 (Paper VI prop:lambda)
- N/2 = 5.5 (target, per Paper VI assertion)

## The potential

Paper VI eq `V-radion` (line 1592 of paper-5-cosmology/main.tex):

    V(σ) = N²/(8σ²) - c_N/(12σ) + Λ·σ

Three physical contributions:
- N²/(8σ²): Freund-Rubin flux (F² energy for e = N/2 Euler class)
- -c_N/(12σ): 1-loop matter Casimir on S¹ fiber
- Λ·σ: 3D cosmological constant derived in Paper VI §prop:lambda

## Stationarity: σ_min

V'(σ) = -N²/(4σ³) + c_N/(12σ²) + Λ = 0

Multiplying by σ³: Λσ³ + (c_N/12)σ - N²/4 = 0 (stationarity cubic)

At N=11: 6.5625 σ³ + 10.547 σ - 30.25 = 0

Newton iteration → **σ_min = 1.34706** (to 5 significant figures).

**This is NOT σ = 1.** Paper VI line 1049 says "stabilized at unit radius" —
inconsistent with line 1598 which says σ_min ≈ 1.35. Internal inconsistency in
Paper VI; line 1049 is factually wrong.

## Second derivative

V''(σ) = 3N²/(4σ⁴) - c_N/(6σ³)

Using stationarity N²/(4σ³) = Λ + c_N/(12σ²), two clean forms:

    V''(σ_*) = 2Λ/σ_* + N²/(4σ_*⁴)     [Form 2, cleanest]

At σ_min = 1.34706, σ_*² = 1.8146, σ_*³ = 2.444, σ_*⁴ = 3.293:

V''(σ_min) = 9.744 + 9.187 = **18.931**

## ω under different canonicalizations

ω² = V''(σ_*)/K_σ depends on kinetic normalization:

| Canonical variable | K_σ | ω² | ω |
|---|---|---|---|
| σ (linear) | 1 | 18.931 | 4.352 |
| log σ | 1 | σ_*²V'' = 34.346 | **5.8605** |
| log σ, G_11=3/4 (Session 18) | 3/4 | 45.795 | 6.7672 |
| log σ, G=15/4 | 15/4 | 9.159 | 3.026 |

**Closest match to N/2 = 5.5**: log σ with K=1, giving ω = 5.86 (6.5% high).
**Most rigorous (Session 18 Einstein frame)**: G_11 = 3/4, giving ω = 6.77 (23% high).

## Cross-check at N=7

Apply same analysis: b(7) = 4.298, c_7 = 51.57, Λ = 33/16 = 2.0625.

Cubic: 2.0625 σ³ + 4.298 σ - 12.25 = 0 → σ_min = 1.4344.

V''(σ_min) = 5.768, σ²V'' = 11.869, ω_log = **3.4452**.

**At N=7**: ω = 3.445 vs N/2 = 3.5, **1.57% LOW**.
**At N=11**: ω = 5.861 vs N/2 = 5.5, **6.55% HIGH**.

**Sign flips** between N=7 and N=11. Structural evidence that M_rad = N/2 is a
heuristic coincidence at O(10%) level, not an exact identity.

## Asymptotic at large N

Cubic tends to (N²/16)σ³ + (N²/12)σ - N²/4 = 0, giving σ_∞ ≈ 1.311.
Then ω_log/(N/2) → √1.237 = **1.112**. Error grows with N.

## What Λ would make M_rad = N/2 exact?

Demand σ_*²V''(σ_*) = (N/2)² at the minimum:

    σ_*² + 2c_N·σ_*/(3N²) = 3

For N=11: σ_*² + 0.697 σ_* - 3 = 0 → σ_* = 1.418.
Required Λ: (N²/4 - (c_N/12)·σ_*)/σ_*³ = **5.364**.

Paper VI has Λ = 6.5625 (from (N²-16)/16 derivation). Mismatch is **22.3%**, far
above derivation tolerance. The two expressions are not self-consistent.

## Impact on Ω_Λ

Recompute with derived ω instead of asserted N/2:

| Scenario | M_rad | (1/2)M_rad | F_DE | Ω_Λ | Planck tension |
|---|---|---|---|---|---|
| A (Paper VI assertion) | 5.500 | 2.750 | 13.297 | 0.6849 | +0.07σ |
| B (ω_log, K=1) | 5.861 | 2.930 | 13.477 | **0.6878** | +0.40σ |
| C (ω linear, K=1) | 4.352 | 2.176 | 12.723 | 0.6753 | -1.38σ |
| **D (Einstein frame, G=3/4)** | **6.767** | **3.384** | **13.931** | **0.6950** | **+1.42σ** |
| E (no radion) | 0 | 0 | 10.547 | 0.6330 | -7.4σ (falsified) |

Planck 2018: Ω_Λ = 0.685 ± 0.007.

**Best case (B)**: 0.40σ above Planck. Still within 1σ. Acceptable.
**Rigorous case (D)**: 1.42σ above Planck. Within 2σ. Tensioned but acceptable.
**Without radion (E)**: 7.4σ falsified.

**The radion contribution is essential.** Without it the framework fails. With it,
Planck agreement survives at 1σ precision, not sub-σ as Paper VI claims.

## Structural issues in Paper VI

1. **Line 1049** "stabilized at unit radius": FACTUALLY WRONG. σ_min = 1.347.
   Inconsistent with line 1598 (which correctly says σ ≈ 1.35).

2. **M_rad = N/2 assertion** at line 1050: NOT derivable from the potential.
   Closest derived value is ω = 5.86 (log-frame), 6.5% higher.

3. **Claimed 0.3σ Planck agreement**: SURVIVES at 0.4σ under log-frame kinetic norm,
   degrades to 1.4σ under rigorous Einstein-frame norm.

4. **Which kinetic normalization is CORRECT?** Depends on how Paper VI derives the
   effective theory. Session 18's G_11 = 3/4 is for the 2-modulus (α, γ) case.
   For Paper VI's single-modulus reduction (γ fixed at flux-stabilization scale),
   the canonical norm could be different. This needs a separate derivation.

## Tier 4.1 verdict

**Scenario B**: M_rad = N/2 closes only at the 10% approximation level, not as a
theorem. Framework Ω_Λ prediction survives at ~1σ Planck agreement, not sub-σ.

**What's derived** (after Session 34):
- Ω_Λ = 68.5-69.5% depending on canonicalization (all within 2σ of Planck)
- H_0 ≈ 67-68 km/s/Mpc (within 1-2σ of Planck)
- All from 1 observational input (M_Planck) + pure math

**What remains**:
- Determine correct kinetic normalization for Paper VI's single-modulus N=11 reduction
- If Einstein-frame G_11=3/4 applies: tension rises to 1.4σ (still acceptable but less clean)
- If log-frame K=1 applies: tension stays at 0.4σ (near sub-σ)

## Recommendations

### For Paper VI immediately
1. Remove "stabilized at unit radius" from line 1049 (factually wrong).
2. Replace M_rad = N/2 assertion with derived ω ∈ [5.86, 6.77] with normalization note.
3. Honestly state Planck agreement at 0.4-1.4σ depending on canonicalization.

### For the derivation chain
**Session 35**: determine the correct canonical kinetic term for the Paper VI
single-modulus N=11 radion via first-principles Weyl rescaling. This pins ω to a
single value and closes Tier 4.1 at whatever precision emerges.

## References

- Paper VI `latex/paper-5-cosmology/main.tex` §cc-instanton, §cosmology, eq V-radion line 1592
- Paper VI source `src/planetary_polygons/extensions/radion_inflation.py` lines 28-32
- Session 18 G_11=3/4 kinetic matrix derivation
- Session 33 audit identifying M_rad = N/2 as the asserted step
