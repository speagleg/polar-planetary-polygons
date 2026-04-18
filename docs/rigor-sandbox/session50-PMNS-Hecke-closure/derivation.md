# Session 50 — Klein-quartic Hecke closure of PMNS Conjecture 16.6

**Date**: 2026-04-18
**Goal**: Close Session 15's PMNS Conjecture 16.6 by computing Hecke eigenvalues on S_2(Γ(7)) at CM point τ_0 = (1+i√7)/2 and matching to the three PMNS fractions.
**Status**: **PARTIAL — closure is NOT achieved by the Klein-quartic Hecke spectrum alone.** The Hecke eigenvalues on S_2(Γ(7)) live in the real cubic ℚ(cos 2π/7), NOT in ℚ(√−7). They do not directly produce the rational coefficients (N−1)/N, (N+1)/(2N), 1/(N²−1). A genuine gap remains, specified precisely in §7.

---

## 1. Bottom line

The Klein-quartic Hecke computation at τ_0 = (1+i√7)/2 **does not close** Conjecture 16.6. What it achieves:

- **CONFIRMS** the Session 15 √N = √7 field signature: both the real cubic K_3 = ℚ(cos 2π/7) (Hecke-eigenvalue field on S_2(Γ(7))) and the imaginary quadratic K_2 = ℚ(√−7) (CM field at τ_0) contain ℚ(√7) as a common sub-object via the biquadratic extension ℚ(√7, √−7) ⊂ ℚ(ζ_7).
- **DOES NOT PRODUCE** the specific rational coefficients 1/2, (N−1)/N, (N+1)/(2N), 1/(N²−1) from pure Hecke-eigenvalue arithmetic. The T_2-eigenvalues on S_2(Γ(7)) are the roots of x³+x²−2x−1, with power sums Σα = −1, Σα² = 5, Σα³ = −4, Σα⁴ = 13. None of these (nor simple rational combinations) reproduces (N−1)/N = 6/7, (N+1)/(2N) = 4/7, or 1/(N²−1) = 1/48.

Precise status:
- Structural field signature (Session 15): **derived**.
- Power-counting hierarchy x, x², x⁴ (Session 15): **motivated** but not proved from Hecke.
- Specific rational coefficients: **STILL OPEN**; the naive Klein-quartic Hecke route does not close them.

Recommendation: keep 16.6 labeled as **"partially structural + deferred"** in the paper (Session 15's framing remains correct).

## 2. Session 15 recap (target)

Session 15 established the following parametrization of the three observed PMNS angles at N = 7 via x = 1/√N = 1/√7:

| Angle | Closed form | Power in x |
|---|---|---|
| sin²θ_12 | (N − √N)/(2N) = 1/2 − x/2 | linear |
| sin²θ_23 | (N+1)/(2N) = 1/2 + x²/2 | quadratic |
| sin²θ_13 | 1/(N²−1) = x⁴/(1−x⁴) | quartic |

PDG comparison (at N = 7): all three angles match at 0.1 σ to 1.6 σ.

The three angles collectively encode the rational coefficients

- T_1 = 1/2 (the S_3-symmetric base)
- T_2 = 1/(2N) (the Z/3 Frobenius correction)
- T_3 = 1/(N²−1) (the double Frobenius correction)

Session 15's working hypothesis (§5): these coefficients arise from Petersson inner products and Hecke eigenvalues on S_2(Γ(7)) at τ_0 = (1+i√7)/2.

## 3. Spiral-hexagon leverage (what was reused)

**Load-bearing**:
- `/mnt/c/Users/gspea/source/repos/spiral-hexagon/src/spiral_hexagon/heegner_d7_klein.py` — CM curve 49a1, a_p structure for split primes ≡ 1, 2, 4 (mod 7), the fundamental prime π = (1+√−7)/2 with |π|² = 2, and the Chowla–Selberg period formula for Ω_{K_2}.
- `/mnt/c/Users/gspea/source/repos/spiral-hexagon/src/spiral_hexagon/hilbert_modular_N7.py` — the cubic trace field K_3 = ℚ(cos 2π/7), minimal polynomial x³+x²−2x−1, discriminant 49 = 7², class number 1, three real embeddings α_k = 2cos(2πk/7) for k = 1, 2, 3.
- `/mnt/c/Users/gspea/source/repos/spiral-hexagon/src/spiral_hexagon/n7_artin_rep.py` — the Galois action on the three Havelock eigenvalues S_m: σ_2(S_1) = S_2, cyclic under Gal(K_3/ℚ) = ℤ/3.
- `/mnt/c/Users/gspea/source/repos/spiral-hexagon/src/spiral_hexagon/bolza_hecke_operator.py` — template for computing Hecke eigenvalues via automorphism-group action on an orbit (base-point independent). Directly applied here to S_2(Γ(7)) ≅ 3-dim standard rep of PSL(2,7).

**Diagnostic (showed the naive approach fails)**:
- `/mnt/c/Users/gspea/source/repos/spiral-hexagon/src/spiral_hexagon/n7_hilbert_match.py` — already found that for N = 7 the "Havelock-as-Hecke" reduction gives a REDUCIBLE Artin representation (sum of two Dirichlet characters), not a genuine Klein-quartic eigenform. The present session extends this: the nontrivial 3-dim irrep of PSL(2,7) is the correct Hecke-module structure, but its eigenvalues lie in K_3 (not in K_2), so τ_0-evaluation does not close the conjecture.

## 4. S_2(Γ(7)): Klein-quartic cusp-form space

**Dimension** (Hurwitz genus formula):
- Γ(7) has index [PSL(2,ℤ) : PSL(2,7)] = 168 in the modular group modulo scalars.
- X(7) = Γ(7)\H* is the Klein quartic, a smooth projective curve of genus g = 3.
- dim S_2(Γ(7)) = g = 3.

**Basis**: S_2(Γ(7)) ≅ H⁰(X(7), Ω¹) ≅ standard 3-dim irrep V_3 of PSL(2,7) (the nontrivial 3-dim irrep over ℚ(ζ_7); its complex conjugate V_3* is the other 3-dim irrep).

**Hecke action**: For each prime p ≠ 7, T_p acts on S_2(Γ(7)). The minimal polynomial of T_2 on S_2(Γ(7)) is (classical, Hecke 1940; see Top 2005, Adler–Ramanan 1996):

    p_{T_2}(x) = x³ + x² − 2x − 1

with roots α_k = 2cos(2πk/7) for k = 1, 2, 3. These are real algebraic integers in K_3 = ℚ(cos 2π/7) (real cubic, discriminant 49, class number 1).

**Verification** (numerical, this session):
- α_1 = +1.2470, α_2 = −0.4450, α_3 = −1.8019.
- Trace Σα_k = −1 (= −coefficient of x²).
- Σα_iα_j = −2 (= coefficient of x).
- α_1α_2α_3 = +1 (= −constant term).
- Power sums: Σα_k² = 5, Σα_k³ = −4, Σα_k⁴ = 13.
- Ramanujan–Petersson for weight 2: |α_k| ≤ 2√2 ≈ 2.83, satisfied (α_3 = −1.80 is the largest in magnitude).

## 5. CM point τ_0 = (1+i√7)/2: what IS and ISN'T computed there

**Critical distinction**: there are TWO different objects that can be called "Hecke eigenvalues at τ_0":

(a) **Hecke-operator eigenvalues**: eigenvalues of T_p acting on S_2(Γ(7)). These are INDEPENDENT of τ_0 — they are global invariants of the form, computed via the Eichler–Selberg trace formula. These are the α_k = 2cos(2πk/7) above.

(b) **CM values**: for a specific eigenform f ∈ S_2(Γ(7)), the complex number f(τ_0). These are transcendental periods; by Shimura's theorem they are algebraic multiples of the CM period Ω_{K_2} where K_2 = ℚ(√−7), with Ω_{K_2} ∝ [Γ(1/7)Γ(2/7)Γ(4/7)]^{1/2} · 7^{1/8} / √(2π) (Chowla–Selberg).

The PMNS target coefficients are **rational** — 1/2, 1/(2N) = 1/14, 1/(N²−1) = 1/48. They CANNOT be f(τ_0)/Ω_{K_2} for generic f (those ratios are transcendental in general).

**Therefore**: the Session 15 phrase "Hecke eigenvalues at CM point τ_0" must mean (a), not (b). But the Hecke eigenvalues (a) are the α_k in the REAL cubic K_3, not in the imaginary quadratic K_2. The τ_0 = (1+i√7)/2 is a red herring: the Hecke spectrum on S_2(Γ(7)) is defined independently of the chosen CM point.

## 6. Attempted match to PMNS and why it fails

Explicit test: build the PMNS rational coefficients from the α_k.

- Target 1/2 = (N−1)/(2(N−1)) = ? No simple α_k combination.
- Target 6/7 = (N−1)/N = 1 − 1/N. Test: 1 − (α_1α_2α_3)/N = 1 − 1/7 = 6/7 ✓ **This works formally** using N(α) = 1 (the norm of α), but the specific identification N(α) = 1 is just "any unit in K_3 has norm ±1," not a distinctive Hecke prediction.
- Target 4/7 = (N+1)/(2N) = (N+1)/(2N). Test: (−Tr(α) + 1 + N)/(2N) = (1 + 1 + 7)/14 = 9/14 ≠ 4/7. No simple fit.
- Target 1/48 = 1/(N²−1) = 1/(7²−1). Test: 1/(Σα_k² + Σα_iα_j·... ) — no simple identity. Numerator 1 must come from trivial product; denominator 48 = 7²−1 is related to |PSL(2,7)|/8·... but not naturally to the Hecke spectrum of S_2(Γ(7)) alone.

**Conclusion**: the Hecke spectrum α_k does NOT, via any simple rational combination, yield the PMNS coefficients. The "6/7 from norm-1 unit" is too weak to count as a derivation — it reduces to "there exists a unit," true for any real cubic.

## 7. What is actually needed to close Conjecture 16.6

The rational coefficients (N−1)/N, (N+1)/(2N), 1/(N²−1) are STRUCTURAL RATIONALS tied to:

- (N−1) = dimension of the reduced character lattice of PSL(2,7) minus trivial
- N = |ℤ/N| = the cyclic group order
- N² − 1 = (N−1)(N+1) = |PSL(2,7)|/24 for N = 7, a dimension of Hecke algebra / representation theory quantity

These come from **representation theory of PSL(2,7) and the vortex-polygon Yukawa structure**, NOT from Hecke eigenvalues on S_2(Γ(7)). Specifically, what is needed:

1. **Yukawa Y^ν_{ij}** for 3 × 3 neutrino matrix from the polygon vortex cusp-localized basis (i, j = 1, 2, 3 labeling pair orbits {1,6}, {2,5}, {3,4}).
2. **Petersson inner product matrix G_{ij} = ⟨ω_i, ω_j⟩** on S_2(Γ(7)) in the cusp-localized basis. This IS computable via Rankin–Selberg (spiral-hexagon has `petersson_inner_product.py` and `rankin_selberg_wronskian.py` as templates).
3. **PMNS matrix U = U_ℓ^† U_ν** where U_{ν,ℓ} diagonalize G^{−1/2}·Y·Y^†·G^{−1/2}. The Hecke eigenvalues α_k enter ONLY as diagonal entries of M² after diagonalization, weighted by Yukawa-profile factors (Havelock eigenvalues).
4. **Final identification**: verify that after diagonalization U_12 = √(1/2 − x/2), etc.

Step 2 is standard Eichler–Shimura (doable in sage with existing infrastructure). Step 1 requires choosing the correct Yukawa texture; Session 15 §7 tried the Z/7 texture Y_{ij} ∝ 1[m_i + m_j + m_H ≡ 0 mod 7] and found it DOES NOT reproduce PMNS — so the texture itself is still unknown.

**Missing piece for closure**: the correct Yukawa texture in the cusp-localized basis, together with the Petersson inner product matrix. Neither is derivable from the Hecke spectrum alone.

## 8. Numerical check of PMNS

(For completeness; no new computation this session, values from Session 15.)

| Angle | Polygon | PDG 2024 | σ |
|---|---|---|---|
| θ_12 | 33.90° | 33.41° ± 0.79° | +0.6σ |
| θ_23 | 49.10° | 49.0° ± 1.3° | +0.08σ |
| θ_13 | 8.30° | 8.54° ± 0.15° | −1.6σ |

The parametrization is correct; only the derivation of the coefficients remains open.

## 9. Paper impact

**No CHANGE 16 to PAPER4_REVISION_DRAFT.md**. Session 15's Conjecture 16.6 framing should be **kept as partial-structural + deferred-technical**. Specifically, do NOT claim closure via Klein-quartic Hecke: that claim would be wrong.

The correct statement for the paper: the √7 field signature is derived, the x, x², x⁴ power counting is motivated, and the specific coefficients require a Yukawa-texture-plus-Petersson-inner-product computation that is NOT equivalent to computing Hecke eigenvalues at a CM point.

## 10. Honest gap statement

Conjecture 16.6 remains open because:

- The Hecke eigenvalues on S_2(Γ(7)) are roots of x³+x²−2x−1, in real cubic K_3, NOT in imaginary quadratic K_2.
- CM-point evaluation f(τ_0) gives transcendental periods, not rationals.
- The rational PMNS coefficients 1/2, 1/(2N), 1/(N²−1) come from the Yukawa texture + Petersson inner product diagonalization, a distinct calculation from Hecke spectrum.
- Session 15 §7 showed the naive Yukawa texture does NOT work; the correct texture is not yet identified.

The spiral-hexagon machinery does all it can: it gives K_2, K_3, the 49a1 CM curve, the Hecke spectrum, the Chowla–Selberg periods, the Artin-rep reducibility verdict. What it does NOT supply is the polygon-specific cusp-localized Yukawa matrix, which is the missing ingredient.

## 11. References

- Hecke, E. 1940. "Über die Bestimmung Dirichletscher Reihen durch ihre Funktionalgleichung."
- Gross, B. 1978. "On the periods of abelian integrals and a formula of Chowla and Selberg."
- Elkies, N. D. 1999. "The Klein quartic in number theory." In *The Eightfold Way*, MSRI Pub. 35.
- Shimura, G. 1971. *Introduction to the Arithmetic Theory of Automorphic Functions*. Princeton.
- Top, J. 2005. "Descent by 3-isogeny and 3-rank of quadratic fields."
- Adler, A., Ramanan, S. 1996. *Moduli of Abelian Varieties*. LNM 1644.
- Darmon, H., Pollack, R. 2006. "Efficient calculation of Stark-Heegner points via overconvergent modular symbols."
- Hida, H. 1988. "Modules of congruence of Hecke algebras and L-functions."

## 12. Conclusion

**Conjecture 16.6 status: STILL PARTIAL.** The Klein-quartic Hecke computation clarifies what the deferred step is NOT: it is not a Hecke spectrum computation. The actual missing step is a cusp-localized Yukawa-texture + Petersson inner product diagonalization, which is a distinct and harder computation. The spiral-hexagon resources do not supply this; it is genuine new technical work.

**Do not upgrade 16.6 to a theorem in Paper IV.**
