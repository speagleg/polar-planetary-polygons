# Task 7: Z/3-extensions of SU(3) — systematic investigation

**Date**: 2026-04-16
**Scope**: classify extensions G of SU(3) by Z/3 and check which matches the polygon theory's matter content. Could this yield SU(4) indirectly?

## Lie group Z/3-extensions of SU(3): classification

**Short exact sequence**: `1 → Z/3 → G → SU(3) → 1`

For SU(3) (a simply-connected Lie group), finite central extensions are classified by `H²(SU(3), Z/3)` with trivial action:

`H²(SU(3), Z/3) = 0` (since SU(3) is simply connected and Z/3 is abelian).

Therefore the ONLY central extension is the direct product `G = SU(3) × Z/3`.

For non-central extensions: Z/3 acts on itself by `Aut(Z/3) = Z/2`. The action factors through a homomorphism `SU(3) → Z/2`. Since SU(3) is simple and has no non-trivial Z/2 quotient, this homomorphism must be trivial. Hence all extensions are central — i.e., direct products.

**Conclusion**: as Lie groups, the only Z/3-extension of SU(3) is `SU(3) × Z/3`.

This does NOT produce SU(4). Dead end via Lie group extensions.

## Finite-group approach: S_4 ⊂ PSL(2, F_7) ⊂ SU(4)?

### S_4 subgroup of PSL(2, F_7)

PSL(2, F_7) has order 168 = 2³ · 3 · 7, with maximal subgroups:
- `F_{21} = Z/7 ⋊ Z/3` (order 21, index 8)
- `S_4` (order 24, index 7) — 7 conjugate copies, fixing 7 points of some underlying 7-set

So S_4 IS a maximal subgroup of PSL(2, F_7). This is the polygon theory's "other" natural subgroup.

### S_4 ⊂ SU(4) naturally

S_4 acts on 4 elements (= coordinates of SU(4) 4-rep). The S_4 action by permutation matrices embeds S_4 into SU(4) (with appropriate sign twists for SU vs U). This is the Weyl group of SU(4).

Under S_4:
- 4-rep of SU(4) decomposes as S_4-rep: `4 = 1 + 3_{std}` where `1` is trivial (fixed coordinate) and `3_{std}` is the standard rep of S_4.

### χ_3 of PSL(2, F_7) restricted to S_4

PSL(2, F_7) has irreps (1, 3, 3̄, 6, 7, 8).

The 3-dim χ_3 restricted to the S_4 subgroup: since S_4 has a unique 3-dim irrep (the standard rep), `χ_3|_{S_4} = 3_{std}` of S_4.

So the SAME 3-dim object that gives SU(3)_c color via McKay (from Z/3 ⊂ PSL(2, F_7) ⊂ SU(3) embedding) ALSO transforms as the standard 3_{std} rep of the S_4 subgroup.

### The natural 4-rep extension

S_4 acts on `1 + 3_{std} = 4`. This is the S_4 4-rep (permutation of 4 elements).

Extending the S_4 action to a Lie group: S_4 ⊂ SU(4) via permutation matrices. The 4-rep of S_4 extends to the 4-rep of SU(4).

**Observation**: the polygon theory's PSL(2, F_7) structure naturally contains S_4, which has a natural 4-rep. Augmenting the χ_3 (3-dim) with a singlet gives the S_4 4-rep, which extends to SU(4) 4.

## Is this an SU(4) derivation?

### What we have

- Polygon theory gauge group at UV (from paper derivations): SU(3)_c × SU(2)_L × SU(2)_R × U(1)_Y (15 gauge bosons)
- Matter content fits Pati-Salam 16-rep per generation (4, 2, 1) + (4̄, 1, 2)
- PSL(2, F_7) automorphism group of X(7) contains S_4 ⊂ SU(4) naturally

### What we DON'T have

For full SU(4)_c gauge symmetry, we'd need:
- 15 gauge bosons of SU(4) adjoint (instead of 8 of SU(3)_c + 1 of U(1)_{B-L})
- 6 additional "leptoquark" gauge bosons that rotate quark into lepton color

The paper's derivation gives 8 SU(3)_c bosons + 1 U(1) boson = 9 gauge bosons (minus the gapped SU(2)_R sector). No source for 6 additional leptoquark bosons.

### Conclusion on SU(4) derivation

**The polygon theory does NOT have full SU(4)_c gauge symmetry.** The matter content happens to fit SU(4) rep structure (via the {0} ∪ O± = 4-rep identification), but the gauge group lacks the 6 leptoquark bosons needed for SU(4).

The theory is best described as:
- **UV gauge group**: SU(3)_c × SU(2)_L × SU(2)_R × U(1)_Y (15 bosons)
- **IR gauge group** (below m_R): SM = SU(3)_c × SU(2)_L × U(1)_Y (12 bosons after SU(2)_R gapping)
- **Matter content**: 16 Weyl per generation in (4, 2, 1) + (4̄, 1, 2) PS embedding (structural, not gauged)

This is "SM + SU(2)_R" (NOT full Pati-Salam or full LR-symmetric).

## Refinement of sin²θ_W = 3/11 interpretation

Previously claimed: "sin²θ_W = 3/11 matches PS at g_R²/g_{B-L}² = 8/5."

Refined: the ratio ρ = 8/5 ≠ 1 means the coupling ratio is NOT at PS unification (where all couplings equal). So 3/11 is NOT a standard PS signature.

The paper's derivation of sin²θ_W = 3/11 uses a POLYGON-SPECIFIC formula:
```
sin²θ_W = h_Y / (h_Y + h_W)
        = (Q²/k_Y) / ((Q²/k_Y) + f(m*, N)/(k + h∨))
        = (1/4) / (1/4 + 2/3)
        = 3/11
```

This is NOT a generic PS or GUT formula. It's an intrinsic polygon-theory calculation.

The "match with PS at ρ² = 8/5" is a post-hoc reorganization that doesn't derive PS from the polygon. Our framework's value 3/11 arises INDEPENDENTLY of any PS unification claim.

## Updated framework: polygon theory is SM + SU(2)_R, not PS

With this refined understanding:

| Scale | Gauge group | Matter content |
|-------|-------------|----------------|
| UV (above m_R ≈ 107 TeV) | SU(3)_c × SU(2)_L × SU(2)_R × U(1)_Y | 16 Weyl/gen (PS-embedded) |
| IR (below m_R) | SU(3)_c × SU(2)_L × U(1)_Y = SM | 15 Weyl/gen + ν_R Dirac mass from KK |

The polygon theory is MORE THAN SM (has SU(2)_R at UV, broken via Redlich) but LESS THAN Pati-Salam (no leptoquark gauge bosons).

The matter content happens to fit PS rep structure due to the Frobenius orbit {0} ∪ O± = 4-rep embedding. This is a STRUCTURAL COINCIDENCE (or a hint of a deeper UV unification beyond the polygon theory).

## What does this tell us?

1. **Position B is confirmed** as the correct framing. The polygon theory is "SM + SU(2)_R" with PS-embedded matter content.

2. **SU(4) is unreachable** from polygon theory alone. The matter content has SU(4) structure, but the gauge group doesn't. A further unification beyond polygon (e.g., at even higher scales via additional structure) would be needed for full SU(4)/PS.

3. **sin²θ_W = 3/11** is an intrinsic polygon-theory prediction, NOT a PS signature (despite appearing to match PS at specific coupling ratio).

## Status update

Task 7 resolves negatively for SU(4) derivation: Z/3-extensions of SU(3) (Lie group sense) don't give SU(4), and even the S_4 ⊂ PSL(2, F_7) embedding into SU(4) gives only the Weyl group, not the full Lie algebra.

**Updated framework description**:
- UV gauge group: SU(3)_c × SU(2)_L × SU(2)_R × U(1)_Y (15 bosons, rigorous)
- Matter content: PS-embedded 16-Weyl per generation × 3 generations = 48 Weyl
- Pati-Salam is a STRUCTURAL LABEL for the matter embedding, NOT the UV gauge group
- All 11 verifications still valid

## Implications for Paper IV revision

The revision draft should be updated to remove the "Pati-Salam UV" motif and instead frame:

> "The SM fermion content is derived from the polygon theory via the Pati-Salam rep embedding of matter, though the UV gauge group is SU(3)_c × SU(2)_L × SU(2)_R × U(1)_Y (the polygon theory's derived gauge group), not full Pati-Salam. Whether the theory has a further unification at a higher scale (beyond the polygon structure) is an open question."

This is honest and avoids over-claiming Pati-Salam.
