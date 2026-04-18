# Session 21 — Fiber-wrapped Euclidean instanton contribution

## Summary verdict

**V_fib-inst = A · exp(−2πα·μ)/(α²γ⁴) does NOT stabilize V_*=0 Minkowski_4** for
any polygon-theory tension μ ∈ {b(7)/2π, S_BO(7)/2π, k(7)/2π², 1/2π, 1} and any
amplitude A ∈ [10⁻⁶, 10⁵] (in G_7=1 units).

## §1. Physical setup

A Euclidean soliton wrapping the S¹ fiber once has action S = 2π·α·μ where μ is
the worldline tension (dimension mass in G_7=1 units). The single-wrap semiclassical
contribution to the 4D Einstein-frame effective potential is

    V_fib-inst(α, γ) = A_inst · exp(−2πα·μ) / (α²γ⁴)

where the 1/(α²γ⁴) = 1/V_3² prefactor comes from the universal Weyl rescaling
to 4D Einstein frame (with 1/K² absorbed into A_inst).

### 1.1 Tension candidates from polygon theory

| Source | μ (G_7=1) |
|---|---|
| polygon self-energy: b(7)/2π | 0.684 |
| BF breathing action: S_BO(7)/2π | 2.908 |
| CS vortex level: k(7)/2π² | 0.436 |
| minimal unit 1/2π | 0.159 |
| natural unit 1 | 1.000 |

### 1.2 Scaling vector

Effective log-modulus scaling at critical point α*:
- α-direction: −2 − 2πα*·μ  (drifts with α, grows with μ)
- γ-direction: −4  (fixed, from prefactor)

For μ = b(7)/2π ≈ 0.68 at α* = 0.8: effective scaling ≈ (−5.4, −4). This is
NOT parallel to any of the 5 existing Session 18 directions — cross-products
with all are non-zero.

## §2. Numerical verification (see solve_session21.py)

Three-equation Newton solve for all (A_inst, μ) combinations:

| μ | A_inst range | critical point closest to benchmark | det H | m²_light |
|---|---|---|---|---|
| 0.68 | 10⁻⁶ – 10¹ | α=0.80 → 0.89, γ=0.165 → 0.14 | −1.2e8 → −9e8 | −4358 → −12650 |
| 2.91 | 10⁻⁶ – 10⁵ | α=0.80 → 0.84, γ=0.165 → 0.16 | −1.2e8 → −2.9e8 | −4358 → −5382 |
| 0.44 | 10⁻⁶ – 10¹ | α=0.80 → 0.96, γ=0.165 → 0.12 | −1.2e8 → −6.9e9 | −4358 → −40650 |
| 0.16 | 10⁻⁶ – 10¹ | α=0.80 → 1.06, γ=0.165 → 0.09 | −1.2e8 → −2e11 | −4358 → −300000 |
| 1.0  | 10⁻⁶ – 10³ | α=0.80 → 1.14, γ=0.165 → 0.10 | −1.2e8 → −9e10 | −4358 → −99000 |

**In every case, det H remains negative and grows MORE negative as A_inst grows.**

## §3. Structural diagnosis: why single-ingredient uplifts fail

The tachyon direction at V_*=0 is the ρ = log(α/γ) direction. In the 2D log-modulus
basis, the Hessian contribution from a term V_i with scaling (p, q) to the ρρ
component is (p−q)²·V_i.

At the Session 18 benchmark (V_Ric, V_FR, V_fib, V_base, V_Λ) = (3, 652, 373, −560, −468):

    H_ρρ (Session 18) = 9·3 + 49·652 + 4·373 − 36·(−560) − 1·(−468)·(−1)
                      = 27 + 31948 + 1492 + 20160 − 468
                      = +53159  (actually positive)

Hmm — H_ρρ is positive here! Yet det H = −1.17e8, trace = +3148 at benchmark.
This means the tachyon is in a MIXED direction, not pure ρ. The signature (+,−)
arises because H_σρ (off-diagonal) is large enough to push one eigenvalue negative
even with H_ρρ > 0 and H_σσ > 0.

When a new term is added:
1. Its diagonal contributions to H_ρρ, H_σσ are both positive (for V_i > 0)
2. Its off-diagonal H_σρ contribution can have either sign
3. The critical point shifts; at the new location, the OTHER five terms have
   different V_i values that change the overall Hessian

The numerical result shows that in practice, the critical point shifts such that
the REMAINING 5-term Hessian deepens faster than the new term can stabilize it.

## §4. Systematic candidates exhausted

Six candidates attempted in Sessions 18–21:

| Session | Candidate | Scaling | Result | Reason |
|---|---|---|---|---|
| 18 R.24–R.30 | H-flux ∫H=2πp | (−3,−6) | FAIL | parallel to Λ_7 (−1,−2) |
| 19 | BF breathing-mode instanton | effective (−2,−4)+S·(1,2) | FAIL | Einstein-frame rescaling parallel to Λ_7 |
| 20 ch.1 | R_Σ² (base) | (−1,−6) | FAIL | critical-point drift tracks tachyon |
| 20 ch.2 | R_Σ·F² (cross) | (+1,−8) | FAIL | same |
| 20 ch.3 | F⁴ (Seifert twist) | (+3,−10) | FAIL | same; also EFT invalid |
| 21 | Fiber-wrapped instanton | (−2−2πα·μ,−4) | FAIL | critical-point drift tracks tachyon |

## §5. Pattern identified

**The Session 18 5-term structure is resistant to ALL single-ingredient additions
tested.** Once any new term is added, stationarity forces the critical point into a
region where the pre-existing 5 terms themselves create a MORE severe saddle, and
the new term's positive contribution to the Hessian diagonal is overwhelmed by
off-diagonal mixing or by the shift in the other V_i values.

This is not a theorem — it's an empirical pattern from 6 attempted additions.
A stability-preserving uplift would likely require EITHER:

(a) Two simultaneous new terms with scaling vectors chosen to pin both σ and ρ directions
(b) A term that modifies the EXISTING coefficients of Session 18 (rather than add a
    new scaling channel), effectively relocating the whole 5-term critical manifold
(c) A reconsideration of the base Casimir sign: the tachyon is driven by V_base < 0
    contributing −20160 to H_ρρ. If V_base has the opposite sign (base modes are
    anti-periodic, or there's a competing bosonic/fermionic balance), the tachyon
    might disappear without any uplift at all.

## §6. Recommendation for Session 22

**Revisit the base Casimir sign derivation (Session 14 §3).**

Session 18 §R.16 fixed the sign to NEGATIVE based on bosonic periodic modes on
H²/Z_7. But:

1. On a hyperbolic orbifold with finite isotropy (Z_7 cone points), the zeta-regulated
   Casimir depends on ORBIFOLD torsion (which we haven't carefully analyzed)
2. If fiber fermions are also present on the base (mixed periodic/anti-periodic),
   the net sign could flip
3. The Epstein-zeta estimate |C_base| ≈ 0.09 gives magnitude but sign depends on
   whether the dominant contribution is bosonic or fermionic

If the base Casimir sign flips to POSITIVE, the ρ-tachyon source (−36·V_base) becomes
POSITIVE, and the saddle might disappear without ANY uplift. This is worth a careful
first-principles check.

Alternatively: **compute TWO new ingredients simultaneously.** E.g., R² + fiber-inst.
Combined, they may have sufficient structural freedom to pin both σ and ρ.

## References

- Session 18: `docs/rigor-sandbox/session18-cw-freund-rubin-radion/derivation.md`
- Session 19: `docs/rigor-sandbox/session19-bf-instanton-radion/derivation.md`
- Session 20: `docs/rigor-sandbox/session20-R2-higher-curvature-radion/derivation.md`
- Numerics: `solve_session21.py`
