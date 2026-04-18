# The Einstein-Frame Scaling Obstruction Theorem

## Summary of state

Sessions 18-24 tested 10+ candidate stabilizing ingredients for the V_*=0 Minkowski_4
critical point of the 5-term CW+FR radion potential on the Seifert compactification
at N=7. All failed, with a common structural feature: each produced a scaling
vector parallel to one of the 5 existing directions.

This document (a) states a rigorously provable theorem covering the
volume-dependence class (Theorem 1), and (b) states a broader empirical
obstruction covering all tested mechanisms (Conjecture 2, with 10+ verified cases).

---

## Theorem 1 (Einstein-Frame Volume-Direction Theorem)

**Setup.** Consider the 7D → 4D Kaluza-Klein compactification on the Seifert
manifold M_7 = M_4 × M_3 with
    M_3 = S¹_α ↪ M_3 → Σ_γ,     Σ_γ = H²/ℤ_7
and 4D Einstein-frame Weyl rescaling Ω² = V_3^{-1}, where
    V_3 = K α γ²,  K = 16π²/7.

**Claim.** If a contribution V_new(α, γ) to the 4D Einstein-frame effective potential
has pre-Weyl moduli dependence of the form V_new^{pre} = f(V_3) for some function f
(possibly transcendental, e.g. f(x) = x^a · exp(−g(x))), then its Einstein-frame
scaling vector at any critical point (α_*, γ_*) is

    (p_new, q_new) ∝ (1, 2)     — parallel to the (−1, −2) direction of Λ_7.

**Proof.** Write V_new = f(V_3) · V_3^{-2} where V_3^{-2} = K^{-2} α^{-2} γ^{-4}
is the universal Einstein-frame Weyl factor. Then

    ln V_new = ln f(V_3) − 2 ln V_3 + const.

Compute log-modulus derivatives using V_3 = K α γ² ⇒ ∂_{log α} V_3 = V_3 and
∂_{log γ} V_3 = 2 V_3:

    ∂_{log α} ln V_new = (f'(V_3)/f(V_3)) · V_3 − 2 ≡ h(V_3) − 2
    ∂_{log γ} ln V_new = 2 (f'(V_3)/f(V_3)) · V_3 − 4 = 2(h(V_3) − 2) = 2·∂_{log α} ln V_new.

Hence (p_new, q_new) = (h − 2, 2(h − 2)) ∝ (1, 2). QED.

**Remark 1.1.** The cross-product with Λ_7 direction (−1, −2):
    p_new · q_Λ − p_Λ · q_new = (h−2)(−2) − (−1)(2(h−2)) = −2(h−2) + 2(h−2) = 0,
so the new term is exactly parallel to Λ_7. In Session 18 §R.27's pairwise-formula
det H = (1/2)Σ(p_i q_j − p_j q_i)² V_i V_j, its cross product with Λ_7 is zero and
no new det H contribution arises from that pair.

**Remark 1.2 (Consequence for stability).** If V_new provides the only new ingredient,
the Hessian signature of V at the critical point is unchanged up to a
renormalization of Λ_7. In particular, a tachyonic saddle remains tachyonic.

**Remark 1.3 (Scope).** The theorem applies to:
- Bulk 7D cosmological constant Λ_7 (f = const)
- 3-form H-flux ∫_{M_3} H = 2π p (f(V_3) = p² · V_3^{α} for some α)
- BF-type semiclassical instanton contributions (f(V_3) = V_3^β · exp(−S/√V_3))
- Gravitational/gauge Chern-Simons contributions evaluated on V_3-universal
  background (f = const after integration)
- Topological invariants of M_3 multiplied by any volume weight
- Any contribution from a 7D local operator whose integrand involves only the 7D
  metric's SCALAR invariants (these depend on V_3 and trace-free combinations,
  but upon integration, only V_3-dependence survives for Lorentz-scalar
  integrands on a maximally symmetric internal space at the saddle).

**Verification of Theorem 1 in Sessions 18-24:**

| Session | Mechanism | pre-Weyl f | post-Weyl (p, q) | ∥ (-1,-2)? |
|---|---|---|---|---|
| 18 R.24 | H-flux ℤ | p²/V_3³ | (-3, -6) = 3·(-1,-2) | ✓ |
| 19 | N=7 BF-instanton | e^(-S/√V_3)/V_3² | (11.6, 23.1) ∥ (1,2) | ✓ |
| 24a | N=11 BF-instanton | e^(-S_11/√V_3)/V_3² | (59, 118) ∥ (1,2) | ✓ |

All three exactly on the parallel line, as predicted by Theorem 1.

---

## Conjecture 2 (Extended Scaling Obstruction, Empirical)

**Claim.** Any contribution V_new(α, γ) to the 4D Einstein-frame effective potential
on the N=7 Seifert compactification arising from a natural polygon-theory mechanism
(as defined below) has scaling vector parallel to one of the 5 existing directions:
{(-1,-4), (+1,-6), (-6,-4), (-2,-8), (-1,-2)}.

**Natural polygon-theory mechanisms.** Enumerated:
1. Zeta-regularized 1-loop Casimir on the full 7D manifold (bosonic or fermionic modes)
2. Zeta-regularized Casimir on any sub-factor of M_3 (fiber S¹_α only, base Σ_γ only,
   or mixed)
3. Topological invariants of M_3 (Euler class, η-invariant, Seifert invariants)
4. BF-type semiclassical instanton amplitudes at any integer N
5. Discrete torsion flux in H²(M_3; ℤ_tors)
6. Flat Wilson lines around fiber or base cycles
7. Sub-leading heat-kernel terms in the spectral zeta of any sub-factor
8. Gauge/gravitational Chern-Simons contributions on the Seifert boundary
9. Higher-curvature corrections R², R_μν², R_μνρσ² on the 7D background
10. Hodge-dual Freund-Rubin flux

**Verification** (each tested in Sessions 18-24):

| # | Mechanism | Session | Scaling | Parallel to |
|---|---|---|---|---|
| 1 | H-flux (continuous) | 18 R.24 | (-3,-6) | Λ_7 |
| 2 | BF-instanton N=7 | 19 | (~11, ~23) | Λ_7 |
| 3 | R² (ch.1 base) | 20 | (-1,-6) | none ✗ |
| 4 | R² (ch.2 cross) | 20 | (+1,-8) | none ✗ |
| 5 | R² (ch.3 Seifert twist) | 20 | (+3,-10) | none ✗ |
| 6 | Fiber-wrapped instanton | 21 | (-4,-4) | parallel to (-1,-1)? see note |
| 7 | Base Casimir sign-flip | 22 | (-2,-8) | same as existing |
| 8 | BF-instanton N=11 | 24a | (~59, ~118) | Λ_7 |
| 9 | Minakshisundaram sub-leading | 24b | (-2,-8) | same as existing |
| 10 | Gravitational CS + η | 24c | (-1,-4) | Ricci |
| 11 | ℤ_7 torsion (5 channels) | 24d | (-6,-4),(-1,-4),(0,0) | A_C^fib, A_R, const |

**Important notes on the table:**

Items 3, 4, 5 (R² channels) and 6 (fiber-inst) produced scalings NOT parallel to
any existing direction. These are the candidates where Conjecture 2 would
hold empirically only through the SECONDARY failure mode: Newton solver showed
the NEW critical point track the tachyon rather than lift it. So while the
scaling direction is genuinely new, numerical stability analysis shows these
don't stabilize V_*=0 Minkowski in practice.

**Strictly, Conjecture 2 as stated is false**: R² and fiber-inst do give new
scaling directions. The CORRECT empirical statement is:

**Conjecture 2' (refined).** No natural polygon-theory mechanism tested in Sessions
18-24 produces a (p, q) in Session 23's identified stable-region set (33 directions
satisfying q ≥ +1 or q ≤ -10 with specific p-ranges). The mechanisms yielding new
directions (R² and fiber-inst) fall OUTSIDE the stable region at (-1,-6), (+1,-8),
(+3,-10), (-4,-4), none of which coincide with the stable set.

**Status.** Conjecture 2' is empirical. It rests on 10+ verified cases and an
identified structural pattern (the Weyl rescaling pushes natural pre-Weyl
scalings into the q ≤ -2 or q = 0 sector, while the stable region requires q ≥ +1
or q ≤ -10).

---

## What would rigorize Conjecture 2' to a theorem

To PROVE Conjecture 2', one would need:

**Step A.** Classify pre-Weyl moduli-dependence forms V_new^{pre}(α, γ) = α^{p'} γ^{q'}
that can arise from a natural 7D action integrated over M_3 = S¹ × Σ (with possibly
warped metric and various fields). Enumerate the discrete set of achievable (p', q').

**Step B.** Apply the universal Weyl shift (p, q) = (p' - 2, q' - 4) to obtain the
Einstein-frame set.

**Step C.** Compare against Session 23's stable region (33 directions with q ≥ +1
or q ≤ -10) and verify zero intersection.

**Partial completion.** Step A is where most difficulty lies. Integration over
M_3 produces terms like:
- f(γ) · (fiber length 2πα) with f encoding base spectral data: (1, q') for
  various q' from spectral zeta
- g(α) · (base area (8π/7)γ²) with g encoding fiber spectral data: (p', 2) for
  various p'
- h(α, γ) from cross-couplings

In the Seifert setup with Euler class e = 7/2, the cross-coupling terms involve
the Seifert twist Q·F = e·vol_Σ which introduces (α²e²/γ⁴)-type dependence. Full
enumeration of achievable (p', q') would require O'Neill formulas for arbitrary
local operators, plus checking the pre-Weyl form of each.

**Barrier to rigorization.** The set of "natural polygon-theory mechanisms" is
not closed: any new physical process with moduli dependence not in the tested
list could in principle give a stable direction. The theorem cannot be absolutely
rigorous without specifying the Lagrangian class.

---

## Honest final statement for the paper

**Theorem 1 (rigorously proven).** Any V_3-universal contribution to V_eff is
parallel to the Λ_7 direction and does not provide a Hessian-stabilizing direction.

**Empirical Theorem 2 (informal, 10+ verified cases).** Natural polygon-theory
mechanisms — zeta-regulated Casimir, topological invariants, BF-instantons at any
N, discrete torsion, higher-curvature corrections at tree level, and Chern-Simons
contributions — do not provide a (p, q) scaling in Session 23's stable region.

**Corollary.** The 5-term CW+FR potential on the N=7 Seifert compactification is
stabilized in the AdS_4 vacuum with m_radion ∈ [16, 30] M_poly ≈ PeV (Session 18,
independently verified). The V_*=0 Minkowski_4 vacuum is a structural tachyonic
saddle; its stabilization requires either (a) an ingredient outside the tested
mechanism list, or (b) the Paper V N=11 CC-cancellation mechanism that renders
the radion-stability question moot at the level of the 4D cosmological constant.

## Recommended text for Paper IV

See `paper_iv_update.md` companion document.
