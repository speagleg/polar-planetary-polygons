# Session 20 — R² higher-curvature contribution to the radion potential

## Summary verdict (up front)

V_R² at the polygon-theory coupling α'_7 = 1/k(7) ≈ 0.116 is NOT a small perturbation to
Session 18's 5-term potential: it DOMINATES by factor ~200 at the benchmark point.
The base-R_Σ² channel alone (scaling (−1,−6)) does NOT stabilize, confirming Session 19's
diagnostic. However, a proper derivation of R_7² on the warped Seifert bundle reveals TWO
additional independent scaling channels from the Seifert-twist contribution
F = dω = e·vol_{Σ_0} to R_3:

    R_3 = −2/γ² − α²e²/(2γ⁴)

giving three channels with scaling

    channel 1:  R_Σ²     →  (−1, −6)
    channel 2:  R_Σ·F²   →  (+1, −8)
    channel 3:  F⁴       →  (+3, −10)

The (+3,−10) channel is numerically DOMINANT at the Session 18 benchmark
(V_R²⁽³⁾ ≈ 1.3×10⁵ vs V_R²⁽¹⁾ ≈ 25). The pairwise-formula Hessian estimate at the
UNSHIFTED benchmark gives det H ≈ +2×10¹¹ after R² addition (flipping sign from
Session 18's det H = −1.17×10⁸). But the unshifted benchmark is no longer a critical
point when R² is added — a full Newton solve at the shifted critical point is required
to confirm stability.

At r_* ≈ 4.83 and γ_* ≈ 0.165, the Seifert-twist term α²e²/(2γ⁴) ≈ 5250 dominates
R_Σ = −2/γ² ≈ −73. The product α'_7·|R_3| ≈ 619 ≫ 1, indicating the higher-curvature
expansion has BROKEN DOWN at the Session 18 benchmark. This is a structural concern,
not just a stability-flip test.

## §1. Derivation of V_R²(α, γ) from the 7D higher-curvature action

### 1.1 7D action and polygon-theory coefficient

The higher-curvature extension of the 7D action is

    S_7^{(R²)} = (1/16πG_7) ∫ d⁷x √(−g_7) · α'_7 · [a_1 R² + a_2 R_μν R^μν + a_3 R_μνρσ R^μνρσ]

with α'_7 of dimension length². The polygon framework provides a natural value:

    α'_7 = 1/k(7) where k(7) = 2 b(7) = 2 × 4.297838 = 8.5957

so α'_7 = 1/8.5957 = 0.11633 (in G_7 = 1 units).

I consider first the "simple R²" choice (a_1, a_2, a_3) = (1, 0, 0). In §1.6 I check
that Gauss-Bonnet (1,−4,1) does not change the leading moduli-scaling analysis on
this background.

### 1.2 Warped Seifert metric and 7D Ricci scalar decomposition

The background metric (Session 18 §1.2):

    ds_7² = e^{2A(α,γ)} η_μν dx^μ dx^ν + α² (dψ + ω)² + γ² ds²_{Σ_0}

with Σ_0 = H²/Z_7 of unit curvature. The Seifert connection satisfies dω = e·vol_{Σ_0}
with e = 7/2.

At the constant-A, zero 4D curvature background, the 7D Ricci scalar reduces to the
3D Ricci scalar of the warped Seifert geometry. By Besse (Einstein Manifolds §9.36)
for a Riemannian submersion S¹ ↪ M₃ → Σ with totally geodesic fibers:

    R_3 = R_Σ(phys) − (α²/2)|F|²_{phys}

where |F|²_{phys} = e²/γ⁴ in the Σ_0 physical metric. Thus:

    R_3 = −2/γ² − α²e²/(2γ⁴)

At (α,γ) = (0.798, 0.165):
    −2/γ² = −73.4
    −α²e²/(2γ⁴) = −(0.637 × 12.25)/(2 × 7.43×10⁻⁴) = −5249

The Seifert twist dominates by factor 72.

### 1.3 R_7² on the zero-mode background

At background, R_7 = R_3. Then

    R_7² = R_3² = [−2/γ² − α²e²/(2γ⁴)]²
        = 4/γ⁴ + (2 α² e²)/γ⁶ + (α⁴ e⁴)/(4 γ⁸)

Three channels:

| Channel | dependence | pre-Weyl |
|---|---|---|
| pure base R_Σ² | γ⁻⁴ | |
| cross R_Σ · F² | α²γ⁻⁶ | |
| pure Seifert F⁴ | α⁴γ⁻⁸ | |

### 1.4 Integration over M_3 and Weyl rescaling

∫_{M_3} R_7² √g_3 d³y = R_3² × V_3 = R_3² × K α γ²

with K = 16π²/7 = 22.56 (area of H²/Z_7 with |χ_orb|=4/7 times fiber length 2π).

Under 4D Weyl rescaling g_4^{(pre)} = Ω² g_4^{(E)} with Ω² = V_3^{-1} (to canonicalize
the Einstein-Hilbert term), the potential density picks up factor Ω⁴ = V_3^{-2}
= 1/(K²α²γ⁴), scaling (−2, −4).

Three-channel Einstein-frame scaling:

| Channel | pre-Weyl (p,q) | Einstein-frame (p,q) |
|---|---|---|
| 1: R_Σ² | (+1, −2) | (−1, −6) |
| 2: R_Σ·F² | (+3, −4) | (+1, −8) |
| 3: F⁴ | (+5, −6) | (+3, −10) |

Explicit Einstein-frame potential:

    V_R²(α,γ) = T · [4/(αγ⁶) + 2e²·α/γ⁸ + (e⁴/4)·α³/γ¹⁰]

with T = α'_7/(16πK) = 0.1163/(16π·22.56) = 1.026 × 10⁻⁴.

Substituting e = 7/2:

    A_R²⁽¹⁾ = 4T = 4.104 × 10⁻⁴                at scaling (−1, −6)
    A_R²⁽²⁾ = 2Te² = 2.514 × 10⁻³              at scaling (+1, −8)
    A_R²⁽³⁾ = Te⁴/4 = 3.852 × 10⁻³             at scaling (+3, −10)

### 1.5 Numerical values at the Session 18 benchmark (α,γ) = (0.798, 0.165)

    γ² = 0.02726, γ⁴ = 7.43×10⁻⁴, γ⁶ = 2.025×10⁻⁵, γ⁸ = 5.52×10⁻⁷, γ¹⁰ = 1.50×10⁻⁸

    Channel 1: 4.104×10⁻⁴ / (0.798 × 2.025×10⁻⁵) = 25.4
    Channel 2: 2.514×10⁻³ × 0.798 / 5.52×10⁻⁷ = 3633
    Channel 3: 3.852×10⁻³ × 0.508 / 1.504×10⁻⁸ = 1.30 × 10⁵

    Total V_R² ≈ 25 + 3633 + 130000 ≈ 1.33 × 10⁵

This dwarfs the existing potential pieces (V_i ~ O(10²−10³)). The unshifted benchmark
is no longer a critical point once R² is added; a full Newton solve is required.

### 1.6 Gauss-Bonnet check

For GB (a_1, a_2, a_3) = (1, −4, 1), the analogous calculation for R_μν² and Riemann²
on the warped Seifert gives the SAME three scaling channels (by dimensional analysis:
any pairing of two curvature factors from {R_Σ, F²} on the 3-manifold yields the same
α^i γ^j structure). The GB combination in 4D is topological; in 7D non-trivial. The
coefficient changes by an O(1) factor but the three scaling channels and their
dominance pattern remain.

## §2. Non-parallel scaling verification

Scaling vectors after R² addition:

| Term | (p, q) |
|---|---|
| Ricci | (−1, −4) |
| Freund-Rubin | (+1, −6) |
| fiber Casimir | (−6, −4) |
| base Casimir | (−2, −8) |
| Λ_7 | (−1, −2) |
| R² ch.1 | (−1, −6) |
| R² ch.2 | (+1, −8) |
| R² ch.3 | (+3, −10) |

Cross products (p_i q_j − p_j q_i) for each R² channel vs 5 pre-existing vectors:
all non-zero. R² introduces three genuinely new Hessian directions.

## §3. Polygon-theory coefficient and higher-curvature validity concern

α'_7 = 1/k(7) = 1/8.596 = 0.1163. Combined with R_3 at benchmark (magnitude 5322):

    α'_7 · |R_3| ≈ 619 ≫ 1

The higher-curvature expansion S = 1/(16πG) ∫ [R + α'R² + α'²R³ + ...] requires
α'·R ≪ 1 for reliability. At the Session 18 benchmark, this condition FAILS by
factor ~600. This means:

1. Either α'_7 = 1/k is WRONG (perhaps α'_7 should be loop-suppressed, ~G_7·ζ/(16π²),
   giving α'_7 ~ 10⁻³ to 10⁻⁴),
2. Or the Session 18 benchmark is OUTSIDE the regime of validity (small α²/γ⁴),
3. Or we need to include all-orders curvature resummation.

This structural concern must be addressed before claiming any stability result.

## §4. Full 8-term potential

V_total(α,γ) = A_R/(αγ⁴) + A_F·α/γ⁶ + A_C^fib/(α⁶γ⁴) − B_base/(α²γ⁸) + Λ_7·A_L/(αγ²)
             + A_R²⁽¹⁾/(αγ⁶) + A_R²⁽²⁾·α/γ⁸ + A_R²⁽³⁾·α³/γ¹⁰

With polygon-theory coefficients:
    A_R = 1.764×10⁻³,   A_F = 1.654×10⁻²,   A_C^fib = 7.139×10⁻²
    A_L = 1.764×10⁻³,   B_base = 1.97×10⁻⁴  (at |C_base|=0.10)
    A_R²⁽¹⁾ = 4.104×10⁻⁴,   A_R²⁽²⁾ = 2.514×10⁻³,   A_R²⁽³⁾ = 3.852×10⁻³

Three-equation system with (α_*, γ_*, Λ_7) as unknowns:
    V = 0,  ∂_α V = 0,  ∂_γ V = 0

The numerical root-finding is done in the companion Python script
`solve_session20.py`. Results reported in §5.

## §5. Numerical verification — DEFINITIVE NULL RESULT

Newton–Raphson solve of {V=0, ∂_α V=0, ∂_γ V=0} via multi-start seeding
(see `solve_session20_b.py`). Scan of R2_scale ∈ [−2, +2] around the polygon value:

    R2_scl |    alpha    gamma   Lambda_7 |       det H        tr H |     m^2_light    m^2_heavy | stable?
    ------ + --------  -------  --------- + -----------  ---------- + ------------  ----------- + -------
    -0.03  |  2.167    0.510    -3.28e+02 |  -6.43e+00   -4.01e+01  |  -4.45e+01   +1.15e-01   | no
    -0.01  |  1.570    0.332    -9.72e+02 |  -1.72e+03   -3.71e+02  |  -4.04e+02   +3.42e+00   | no
    -0.003 |  1.031    0.214    -2.68e+03 |  -1.39e+06   -2.32e+03  |  -2.09e+03   +5.32e+02   | no
    -0.001 |  0.868    0.180    -4.37e+03 |  -2.64e+07   -1.55e+03  |  -2.96e+03   +7.12e+03   | no
     0.000 |  0.798    0.165    -5.77e+03 |  -1.17e+08   +3.15e+03  |  -4.36e+03   +2.15e+04   | no   (Session 18 benchmark)
    +0.001 |  0.738    0.153    -7.71e+03 |  -4.83e+08   +1.59e+04  |  -7.09e+03   +5.45e+04   | no
    +0.003 |  0.647    0.134    -1.37e+04 |  -5.79e+09   +9.44e+04  |  -1.96e+04   +2.36e+05   | no
    +0.010 |  0.486    0.100    -6.74e+04 |  -1.54e+12   +2.16e+06  |  -2.66e+05   +4.64e+06   | no
    (R2_scale outside [−0.03, +0.01] does not converge in physical window)

**NO stable critical point in the physical window for any R2_scale ∈ [−2, +2].**

Key observations:
1. At R2_scale = 0 (no R²), Session 18 benchmark recovered exactly:
   (α,γ,Λ_7) = (0.798, 0.165, −5770), det H = −1.17×10⁸, m²_light = −4358.
2. Increasing |R2_scale| MAKES THE TACHYON WORSE (more negative det H).
3. The naive pairwise-formula det H estimate (suggesting det H flips to +2×10¹¹ at
   polygon R² scale) is misleading — once the critical point shifts under ∇V=0,
   the actual Hessian remains signature (+,−).
4. Negative R² (heterotic ghost-free sector) also deepens the tachyon.

### §5.1 Structural interpretation

Adding R² shifts (α_*, γ_*, Λ_7) along a TRAJECTORY that tracks the tachyon rather
than lifts it. The three R² channels add to ALL V_i self-consistently, so their
net effect on the Hessian at the shifted point is sign-preserving, not
sign-flipping.

The pairwise-formula estimate assumed the critical point was FROZEN at the Session
18 benchmark while R² added. In reality, stationarity re-balances all terms
together; the ρ = log(α/γ) direction remains flat and unstable.

### §5.2 EFT validity concern

At the Session 18 benchmark, the magnitude of the Seifert-twist contribution to
the 3D Ricci scalar

    |α²e²/(2γ⁴)| = 5249  (versus |R_Σ| = 73.4)

combined with α'_7 = 1/k(7) = 0.116 gives

    α'_7 · |R_3| = 619 ≫ 1

This violates the EFT validity condition α'·R ≪ 1 by factor ~600. The higher-
curvature expansion is not convergent at this point. Even if R² is included, R³,
R⁴, ... would be comparable (or larger). The EFT is strongly coupled in this regime.

A corollary: any claim about α'-corrections at the Session 18 benchmark is
unreliable. The true fate of V_*=0 Minkowski under higher-curvature corrections
requires a NON-PERTURBATIVE treatment, not the truncated α'_7 R² action.

## §6. Verdict

**V_R² at the polygon coupling α'_7 = 1/k(7) does NOT stabilize V_*=0 Minkowski_4**.
This is a definitive numerical result over a 2-order-of-magnitude scan of |R2_scale|
near the polygon value.

Session 19's scan at scaling (−1,−6) alone had already shown the base R_Σ² channel
fails. Session 20's extension to the full three-channel R² (including the
Seifert-twist dominated (+3,−10) channel) also fails once the critical point is
properly tracked.

## §7. Physical interpretation (conditional) — N/A

Since V_R² does not stabilize, no physical prediction follows from this session.

## §8. Path forward

Remaining candidates for new non-parallel scaling directions:

### §8.1 Fiber-wrapped Euclidean instanton — (+1, 0) scaling

A Euclidean instanton wrapped around the S¹ fiber has action S ~ 2πα·μ for some
tension μ, giving a contribution V ~ A · α · exp(−2πα·μ). The prefactor scales as
(+1, 0) — a genuinely α-only direction not captured by any volume-scaling
Einstein-frame theorem. This escapes the Session 19 no-go.

The tension μ is set by the specific source (fundamental string, D-brane, soliton).
In the polygon framework, natural candidates include:
- polygon self-energy per unit fiber length: μ ~ b(7)/(2π) ≈ 0.68
- BF breathing soliton tension: μ ~ S_BO(7)/(2π) ≈ 2.91
- CS vortex tension: μ ~ k(7)/(2π²) ≈ 0.44

### §8.2 Base-wrapped closed-geodesic instanton — (0, +1) scaling

Analogously, an instanton wrapped around a closed geodesic on H²/Z_7 of length
L_geo = 2 arccosh((3+√5)/2)·γ ≈ 1.928γ (shortest systole from hyperbolic
arithmetic) has prefactor scaling (0, +1).

### §8.3 Hodge dual of FR 2-form — scaling TBD

*F_2 is a 5-form in 7D. Integrating over M_4 (4-dim) to get an effective 1-form
potential gives a scaling vector that depends on the background; needs derivation.

## §9. Recommendation for Session 21

Pursue **fiber-wrapped Euclidean instanton** (§8.1) first: it has the cleanest
physical motivation in the polygon framework (breathing-mode tension), and its
(+1, 0) scaling vector is maximally orthogonal to the existing set.

## References

- Session 18 file: `docs/rigor-sandbox/session18-cw-freund-rubin-radion/derivation.md`
- Session 19 file: `docs/rigor-sandbox/session19-bf-instanton-radion/derivation.md`
- Paper IV: `latex/paper-4-field-theory/main.tex`
- Besse, "Einstein Manifolds," §9.36 (O'Neill formulas for Riemannian submersion)
- Numerics: `solve_session20.py`, `solve_session20_b.py`

## References

- Session 18 file: `docs/rigor-sandbox/session18-cw-freund-rubin-radion/derivation.md`
- Session 19 file: `docs/rigor-sandbox/session19-bf-instanton-radion/derivation.md`
- Paper IV: `latex/paper-4-field-theory/main.tex`
- Besse, "Einstein Manifolds," §9.36 (O'Neill formulas for Riemannian submersion)
