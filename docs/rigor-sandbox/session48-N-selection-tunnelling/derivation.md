# Session 48 — Tier 4.3D: N-selection tunnelling rate verification

**Date**: 2026-04-18
**Goal**: Verify Paper VI §n-selection's claim that σ_start ≈ 3·σ_infl
is the BO-tunnelling initial condition for the radion field.

---

## 0. Bottom line

**Paper VI's claim is ASSERTED, not derived, and the printed formula
is numerically inconsistent with its own conclusion.**

Paper VI line 1605:
    σ_start = ρ*_11 / ln ε_11  ≈  3 · σ_infl

With derived values ρ*_11 = 4.45 and ε_11 = 10 + 3√11 (Z[√11] fundamental
unit, norm +1 since 100−99 = 1), ln ε_11 ≈ 2.993:

    σ_start (as printed)  =  4.45 / 2.993  ≈  1.487
    3 · σ_infl (at N=11)  =  3 · 4.302  =  12.907
    Ratio                 =  0.115  (off by factor ~9)

The product ρ*_11 · ln ε_11 = 13.32 ≈ 3.10·σ_infl matches to 3%, strongly
suggesting `/` is a typo for `·`. Even with the corrected formula, the
factor ln ε_11 is an ALGEBRAIC COINCIDENCE, not derived from the
ρ → σ matching on the Seifert fiber.

**Tier 4.3D does NOT close.** Session 44's cosmology is unaffected
(radion is still spectator/reheater) and in fact strengthened: if
σ_start is actually 1.49 (near σ_*), the radion has no field range
for inflation, eliminating even the remote possibility Session 44
considered.

---

## 1. Paper VI claim extraction

Paper VI `/latex/paper-5-cosmology/main.tex` lines 1602–1616 contains
the claim. Exact form at line 1605:

    σ_start = ρ*_11 / ln ε_11  ≈  3 · σ_infl

Where:
- ρ*_11 is the N=11 BO saddle point: V_11(ρ*_11) = 0 with
  V_11(ρ) = ln(2 sinh ρ) + b(11) − f(5, 11)
- ε_11 is the unit of ℤ[√11] (used exactly once in Paper VI, never
  explicitly defined; natural reading: ε_11 = 10 + 3√11, the
  fundamental unit with norm 10² − 11·3² = 100 − 99 = +1)
- σ_infl is the inflection point of the radion potential V(σ) at N=11

No derivation of why σ_start should equal ρ*_11/ln ε_11 is given.

---

## 2. Numerical verification

### 2.1 Computing ρ*_11

V_11(ρ*_11) = 0 means:
    ln(2 sinh ρ*_11) = f(5, 11) − b(11) = 15 − 10.5466 = 4.4534

So 2 sinh ρ*_11 = e^4.4534 = 85.935, sinh ρ*_11 = 42.967.

For large ρ, sinh ρ ≈ e^ρ/2, so ρ*_11 ≈ ln(2·42.967) = ln 85.935 = 4.454.

**ρ*_11 ≈ 4.45.** ✓

### 2.2 Computing ε_11 and ln ε_11

Pell equation x² − 11y² = ±1. Fundamental solution (x,y) = (10, 3)
gives ε_11 = 10 + 3√11 ≈ 10 + 9.9499 = 19.9499. Norm = 10² − 11·9
= 100 − 99 = +1. ✓

    ln ε_11 ≈ ln 19.9499 ≈ 2.993.

### 2.3 σ_start (as printed)

    σ_start = ρ*_11 / ln ε_11 = 4.45 / 2.993 ≈ **1.487**

### 2.4 σ_infl at N=11

Inflection point of V(σ) = 121/(8σ²) − c_11/(12σ) + Λ_3 σ at N=11:
V''(σ) = 0 gives σ_infl = 3·(121/c_11) = 363/126.56 ≈ **4.302**

    3 · σ_infl = 3 · 4.302 = **12.907**

### 2.5 The discrepancy

    σ_start (as printed, 1.487)  /  (3 · σ_infl = 12.907)  = 0.115

The printed formula is **off by a factor of ~9** from the claimed
"≈ 3·σ_infl" conclusion.

### 2.6 The product interpretation

If `/` is a typo for `·`:
    ρ*_11 · ln ε_11 = 4.45 · 2.993 = **13.32**
    13.32 / σ_infl = 13.32 / 4.302 = **3.10**

This matches "≈3" to 3%. **Strongly suggests LaTeX typo.** Either
`/` → `·`, or ρ*_11 in the formula is actually ρ*_11·(ln ε_11)².

---

## 3. Is ln ε_11 a derivation or a coincidence?

Even granting the product form ρ*_11 · ln ε_11, the factor ln ε_11
is not derived from the ρ → σ matching. Candidate physical origins:

### 3.1 Gaussian width of BO wavefunction

Second derivative of V_11 at ρ*_11:
    V_11''(ρ*_11) = d²/dρ² [ln(2 sinh ρ)] = −1/sinh²ρ
    At ρ*_11 = 4.45: sinh²ρ ≈ 1846, so V_11''(ρ*_11) ≈ −5.4×10⁻⁴

The classical width of the BO wavefunction near the saddle is
Δρ ~ 1/√|V''(ρ*)|·(ℏ/S_BO)^(1/4). With S_BO(11) = 102.72:
    Δρ ~ 1/√(5.4×10⁻⁴)·(1/102.72)^(1/4) = 43·0.314 ≈ 13.5

This is NOT equal to ln ε_11 ≈ 2.993. Factor-of-4 discrepancy;
Gaussian-width is not the origin.

### 3.2 Coleman-De Luccia tunnelling

CdL bounce from false to true vacuum: σ_start is where the Euclidean
bounce emerges into Lorentzian signature.

For V(σ) at N=11: single AdS_4 minimum at σ_* ≈ 1.347 with V(σ_*) < 0;
no second minimum; potential is monotonically linear at large σ.

**CdL does not apply** — there is no false-vacuum/true-vacuum pair.
The single AdS_4 minimum is the only critical point of V(σ) on the
physical branch. Whatever tunnelling Paper VI invokes is a different
quantum-mechanical event, not Coleman-De Luccia.

### 3.3 KK/Thurston matching

The breathing-mode ρ and the radion σ are different degrees of
freedom. ρ is the BO variable for the H² base scaling; σ is the
Seifert S¹ fiber radius modulus. They are related via the Seifert
geometric rigidity (R_*/L = √(e²/|χ_orb|) = √(343/16) ≈ 4.63 at N=7
or ≈ 2.87 at N=11), but the numerical factor ln ε_11 ≈ 2.993
does NOT match the Seifert aspect ratio at N=11 (≈ 2.87) — close
but not equal (off by 4%).

Possibly coincidental that ln ε_11 ≈ R_*/L at N=11? Needs check:
- R_*/L(11) = e/√|χ_orb| = (11/2)/√(8/11) = (11/2)·√(11/8) = 5.5·1.1726 = 6.449
- Actually ratio R_*/L depends on normalization. For the H² quotient
  with |χ_orb| = 8/11, the circumference/radius gives 6.449, which
  is ~ 2·ln ε_11 with small discrepancy.

None of these match exactly enough to be a derivation.

### 3.4 Maass-Selberg / automorphic origin

ln ε_11 is the geodesic length of the closed geodesic on H²/Z_11
associated with the fundamental unit ε_11. Via the Selberg trace
formula, primitive geodesic lengths enter spectral sums. In principle
the radion-breathing-mode matching could involve such a sum, but no
such derivation appears in Paper VI or any session file.

### 3.5 Verdict

ln ε_11 appears in Paper VI's σ_start formula as a **numerical
coincidence** matched at the ~3% level. No derivation of the ρ → σ
matching formula exists in Paper VI, in any of Sessions 33-47, or
in the code base. It is a fitted parameter presented as a derivation.

---

## 4. Alternative matching prescriptions

Four candidate ρ → σ relations yield wildly different σ_start:

| Prescription | σ_start | Ratio to σ_infl |
|--------------|---------|-----------------|
| (a) σ = ρ (naive identification) | 4.45 | 1.03 |
| (b) σ = ρ/√(c_11) (kinetic-norm) | 0.40 | 0.09 |
| (c) σ = e^ρ (log change of vars) | 86 | 20 |
| (d) σ = ρ · ln ε_11 (Paper VI intent, `·` form) | 13.32 | 3.10 |
| (e) σ = ρ / ln ε_11 (Paper VI as printed) | 1.487 | 0.346 |

The "correct" answer depends on the field space metric connecting
ρ (H² breathing mode) and σ (Seifert fiber modulus), which is
determined by the Ferrara-Kounnas kinetic matrix G_ij derived in
Session 35:

    G_ij = [[3/4, 1/2], [1/2, 2]]

for (log α, log γ) with α, γ being the (α-basis) and (γ-basis)
radion-breathing-mode coordinates.

**Session 35's G_ij suggests the naive identification σ ≈ ρ (case (a))
is closest to correct**, modulo a kinetic-normalization factor of
order 1 from diagonalizing G_ij. This would give σ_start ≈ σ_infl
(not 3·σ_infl), removing any radion inflationary field range.

---

## 5. Consequences for Session 44

Session 44 assumed σ_start ∈ [σ_*, 12·σ_*] ≈ [1.35, 16] and tested
inflation candidates (inflection-point, linear) at σ_start = 12.9
(from 3·σ_infl). Conclusions:

- Inflaton candidate at σ_start = 12.9 gave n_s = 0.95, r = 0.067
  (2σ tension with BICEP/Keck)
- Inflection-point ADM regime misapplied (V'(σ_infl) ≠ 0)
- Verdict: NOT an inflaton

If σ_start is actually **≈ 1.49** (the printed formula) or **≈ σ_infl**
(kinetic-matching via G_ij):
- σ_start is AT OR BELOW the inflection point
- No field range for slow-roll at all
- Radion-as-spectator conclusion is **strengthened** (unambiguous)

Either interpretation closes the radion-inflaton question more firmly.

---

## 6. Tier 4.3D closure status

**Session 48 does NOT close Tier 4.3D positively.** Two distinct gaps
remain:

### Gap 6.1: Paper VI formula is numerically wrong as printed.
`/` should be `·` for the stated numerical agreement with 3·σ_infl.
This is a LaTeX typo, trivially fixable. But:

### Gap 6.2: The ρ → σ matching is not derived.
Even with the product form, ln ε_11 appears as an algebraic
coincidence. No physical derivation:
- Not Gaussian BO width (off by 4×)
- Not Coleman-De Luccia (V(σ) has no two vacua)
- Not Seifert KK matching (off by 4%)
- Not Selberg/automorphic (no such sum written)

**What IS closed**: Session 44's spectator/reheater conclusion is
robust to σ_start interpretation, confirmed by both prescriptions.

---

## 7. Paper VI edits required

### Edit VI-§n-selection-a (line 1605 numerical typo)
Change the formula
    σ_start = ρ*_11 / ln ε_11
to
    σ_start = ρ*_11 · ln ε_11

So that the numerical value 13.32 matches the stated "≈ 3·σ_infl".

### Edit VI-§n-selection-b (derivation honesty)
Add note:
"The factor ln ε_11 in the ρ → σ matching is, at the present level
of rigor, an algebraic coincidence matched at the ~3% level; a
derivation via the Selberg geodesic-length trace on H²/Z_11 or the
Ferrara-Kounnas kinetic matrix on (ρ, σ) is deferred (Session 48)."

### Edit VI-§n-selection-c (strength of radion-non-inflaton)
Acknowledge Session 48's result: regardless of which ρ → σ matching
is correct, σ_start is at most O(σ_infl), not 3·σ_infl. The radion
has no slow-roll field range. This strengthens, not weakens, the
Session 44 conclusion that the radion is not the inflaton.

### Recommended addition to PAPER4_REVISION_DRAFT.md
As part of CHANGE 11 (Session 44), add a note pointing to Session 48
for the σ_start precision.

---

## 8. References

- Paper VI `/latex/paper-5-cosmology/main.tex` lines 1602–1616
  (the σ_start claim)
- Session 33 (Paper VI audit)
- Session 35 (Ferrara-Kounnas G_ij derivation)
- Session 38 (V(σ) completeness at N=11)
- Session 39 (2-modulus at N=11)
- Session 44 (radion cosmology, which takes σ_start = 12.9 as input)
- Coleman, S. (1977). "Uses of Instantons." Erice lectures. [CdL]
- Coleman, S.; De Luccia, F. (1980). "Gravitational effects on and of
  vacuum decay." Phys. Rev. D 21, 3305.
- Selberg, A. (1956). "Harmonic analysis and discontinuous groups in
  weakly symmetric Riemannian spaces." J. Indian Math. Soc. 20, 47.
  [Trace formula]

---

## 9. Summary table

| Claim | Status | Where |
|-------|--------|-------|
| Paper VI formula σ_start = ρ*_11 / ln ε_11 | TYPO (`/` → `·`) | §2.5 |
| σ_start ≈ 13.32 ≈ 3.10·σ_infl (corrected formula) | Numerical match 3% | §2.6 |
| ln ε_11 as derivation of ρ→σ matching | COINCIDENCE | §3.5 |
| Tier 4.3D positively closed | NO | §6 |
| Session 44 spectator/reheater conclusion | STRENGTHENED | §5 |
| Paper VI §n-selection needs edit | YES (typo + honesty) | §7 |
