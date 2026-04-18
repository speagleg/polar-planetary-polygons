# Session 37 — Audit of Paper VI's Λ_3 = (N²-16)/16 derivation

## Bottom line

Paper VI's Λ_3 = (N²-16)/16 is **consistent within its chosen conventions, not a
first-principles theorem**. The "-16" is fixed by requiring Λ_3(N=4) = 0 as the
EW-gauge threshold — a normalization condition, not an independent derivation.

**Critically**: in the RIGOROUS Einstein frame (G_11 = 3/4), the Λ that would give
ω = N/2 exactly is **3.365**, not Session 34's 5.365. Session 34's 5.365 came from
the unphysical K=1 log-σ frame. The real gap is ~48%, not 22%.

**No natural Λ_3 formula** produces Λ ≈ 3.365 at N=11 for any reasonable physics.

**Verdict: gap NOT closable via Λ_3 correction.**

## Q1. KK derivation of |F|² and the (1/4) coefficient

### Rigorous parts

- (1/4) coefficient in 3D from KK reduction of 4D Einstein-Hilbert: TEXTBOOK
  (Pope, Duff, Nilsson; Polchinski vol II). Correct.
- K_base = -1 on H² with curvature radius ℓ = 1: convention-dependent but standard.

### The questionable step

Paper VI asserts `|F|² = (πN/(2π))² = N²/4`, yielding (1/4)|F|² = N²/16.

**Checking alternatives**:
- Uniform flux on H² with area A_base = 2π (unit-H² normalization):
  |F|² = 2·(πN/2π)² = N²/2, so (1/4)|F|² = N²/8 (OFF by 2 from Paper VI).
- Genus-2 hyperbolic surface A_base = 4π (Gauss-Bonnet):
  |F|² = N²/8, so (1/4)|F|² = N²/32 (OFF other way).
- **Topological convention** identifying |F|² with Chern class squared
  = (N/2)² = N²/4: gives Paper VI's answer.

Paper VI uses the **topological/Chern convention**, not local Maxwell. This is
acceptable but not a derivation — it identifies `|F|²` with a topological invariant
rather than the Maxwell energy density.

**Finding**: `|F|² = N²/4` is a **normalization choice**, not a theorem.

## Q2. σ-dependence of Λ_3

Paper VI is ambiguous between:
- Line 79-85 (prop:lambda): Λ_3 = (N²-16)/16 as pure number
- Line 1592 (eq:V-radion): V(σ) = ... + Λ·σ, Λ as coefficient of σ

The σ-exponents in V(σ) (powers -2, -1, +1) are not standard Einstein-frame
exponents. Paper VI doesn't specify the frame.

**Finding (GAP)**: σ-exponents in eq:V-radion not derived; consistent with one
frame choice but not obviously with Einstein frame used elsewhere.

## Q3. The "-16" constant

**Logic chain**:
1. Paper VI line 92 asserts "At N=4 these cancel exactly"
2. Paper IV line 244-248 uses Λ_3(N=4) = 0 as normalization check
3. `|F|² = N²/4` then gives "-16" via `Λ_3 = -1 + N²/16 = 0 at N=4`

So the "-16" is CALIBRATED by requiring Λ_3(N=4) = 0, which is itself motivated by
Paper IV's EW-gauge-threshold identification of N=4.

**Finding**: Not fully circular (EW identification is independent), but the "-16"
emerges from calibration, not independent derivation.

## Q4. Alternative derivations tried

- **b(N)-based**: `Λ_3 = b(N) - 1.436` gives zero at N=4 but is ad hoc.
- **Gauss-Bonnet genus-2**: gives `Λ_3 = -1 + N²/32`, zero at N=√32 ≈ 5.66 (non-integer).
- **Orbifold χ corrections**: no natural way to modify -16 to -8.5.
- **σ ≠ 1 evaluation**: coefficient in V(σ) unchanged.

**Finding**: No natural alternative produces Λ ≈ 3.36 (the target for ω = N/2 in
Einstein frame).

## Q5. What Λ gives ω = N/2 at G_11 = 3/4?

Setup:
- Kinetic: L_kin = -(3/8)(∂ψ)² (Einstein frame, ψ = ln σ)
- Frequency: ω² = (4/3)·σ_*²V''(σ_*)
- Demand ω² = (N/2)² = N²/4 means σ_*²V''(σ_*) = 3N²/16

Using stationarity V'(σ_*) = 0:
    σ_*²V''(σ_*) = 3Λσ_* + c/(12σ_*)

Setting equal to 3N²/16 and combining with stationarity:
    N²σ_*² + (8c/9)σ_* - 4N² = 0

At N=11, c=126.56:
    121σ_*² + 112.50σ_* - 484 = 0
    σ_* = [-112.50 + √(12656 + 234256)]/242 = [-112.50 + 496.91]/242 = **1.5885**

Then from stationarity:
    Λ = (N²/4 - (c/12)·σ_*)/σ_*³
      = (30.25 - 10.547·1.5885)/4.011
      = 13.495/4.011
      = **3.365**

**In G_11 = 3/4 Einstein frame**: ω = N/2 requires **Λ = 3.365, σ_* = 1.589**.

Paper VI has Λ = 6.5625. Gap: **Λ would need to be reduced by 49%**.

### Session 34 cross-check (log-σ, K=1 frame)

Session 34 computed Λ* = 5.365 in the K=1 frame. Verified: with demand
σ²V'' = (N/2)², algebra gives σ² + (2c·σ/3N²) = 3, at N=11 gives σ=1.418, Λ=5.365.

But this frame is **unphysical per Session 35** (K_ψ = 3/4 is rigorous).

**In the correct frame**: target Λ = 3.365, gap is 49% not 22%.

## Additional findings

### Paper IV line 241-243 — mathematically vacuous

"this differs from the Besse normalization (∮dA = 2πe) by a factor of N/(2e) = N/2"

With e = N/2 stated on line 234: N/(2·N/2) = N/N = **1**, not N/2. The claimed
factor is mathematically wrong. Besse and Chern normalizations are identical when
e = N/2 (both give ∮dA = πN). **Needs correction.**

### Paper VI line 1049 — factually wrong

"stabilized at unit radius by the flux N/2"

σ_min = 1.347 (Session 34), NOT 1.0. Line 1598 correctly says σ_min ≈ 1.35.
Internal inconsistency.

### Paper VI line 110-112 — incomplete Maxwell stress-energy

"T^{flux}_{μν} = (1/4)|F|² g^{(3)}_{μν}"

Standard Maxwell is `T_{μν} = F_{μα}F_ν^α - (1/4)|F|²g_{μν}`. The first term is
missing. For pure flux on 2D base, `F_{μα}F_ν^α = |F|²/2·g_{μν}` gives net
`T_{μν} = (|F|²/2 - |F|²/4)·g = |F|²/4·g`, which recovers Paper VI's expression.
So the formula is correct for this case, but the derivation is sketchy.

## Final verdict

**Λ_3 = (N²-16)/16 cannot be revised to a value that closes the ω = N/2 gap.**

1. The formula is consistent within Paper VI's conventions but not derived from
   first principles.
2. The "-16" is a calibration to Λ_3(N=4) = 0, not independent.
3. In the rigorous Einstein frame, target Λ for ω = N/2 is **3.365**, which no
   natural derivation produces.
4. Paper VI has some internal inconsistencies (line 1049 σ=1 vs 1598 σ=1.35;
   Paper IV line 241-243 mathematically vacuous).

**Tier 4.1 CANNOT be closed at sub-σ precision via the current Paper VI mechanism.**

Honest framework precision: Ω_Λ = 0.695 ± 0.005, Planck tension +1.4σ ± 0.7σ.

## Recommendations

**Option B**: Accept 1.4σ precision, correct Paper VI text:
- Line 1049: remove "stabilized at unit radius"
- Line 1050: "M_rad = N/2" → "M_rad ≈ 6.77 at N=11, derived from V(σ) with G_11 = 3/4"
- Paper IV line 241-243: fix mathematically vacuous statement
- Paper VI prop:cosmology: Planck tension 0.3σ → 1.4σ

## References

- Paper VI prop:lambda lines 73-155
- Paper VI eq:V-radion line 1592, prop:cosmology line 1061
- Paper IV eq:metric-4d line 342, flux normalization lines 238-248
- Session 34 (σ_min, V'' computation)
- Session 35 (G_11 = 3/4 Einstein frame)
- Session 36 (cumulative corrections widen gap)
- Bott-Tu §6.1 (Chern class convention)
- Polchinski vol II (KK reduction)
- Ferrara-Kounnas Nucl. Phys. B328 (1989) 406
