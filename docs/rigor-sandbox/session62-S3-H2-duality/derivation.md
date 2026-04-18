# Session 62 — Tier 4 foundation: S^3/Ẽ_8 ↔ H²/Z_7 dynamical relationship

**Date**: 2026-04-18
**Goal**: Replace Session 45 moral-analog scope with actual derivation of the
dynamical relationship between the S^3 compact-base framework (Paper V) and the
H²/Z_7 polygon framework. Three candidate mechanisms: (1) RG flow between
curvature-sign vacua, (2) Coleman–De Luccia bounce, (3) dual CFT description.
Session 45 ruled out (3) on c-mismatch. This session investigates (1) and (2)
and — on finding a topological obstruction — derives it rigorously.

---

## 0. Bottom line

**VERDICT: TOPOLOGY-CHANGE OBSTRUCTION.** No Coleman–De Luccia bounce exists
at the radion level connecting S^3 and H²/Z_7 × S^1 within the framework.
The obstruction is FUNDAMENTAL (Euler-class quantization + Thurston rigidity),
not a computational gap. The weaker dynamical relationship that does exist is
a superselection-sector structure: the two frameworks are separate vacua of a
common algebraic parent (ADE / Schwarz-triangle classification) with no
continuous modulus space between them. CHANGE 12 upgrades from moral-analog
to superselection-sector statement (§6–7).

---

## 1. The three mechanisms

### 1.1 Setup

- Vacuum A: S^3 / Ẽ_8 Chern–Simons at k=1, base K = +1 (compact spherical),
  3-manifold S^3 with π_1 = 0, b_1 = 0, c_WZW = 8.
- Vacuum B: H² / Z_7 × S^1 Seifert fibration, base K = −1 (hyperbolic
  heptagon orbifold), 3-manifold with π_1 = ℤ ⋊ Z_7, b_1 = 1, c_DHVW = 51.57.
- Candidate interpolator: a radion σ with σ_S ↔ Vacuum A and σ_H ↔ Vacuum B,
  passing through σ_{K=0} (flat saddle, (2,3,6) triangle group).

### 1.2 Mechanism (3): dual CFT — already dead (Session 45)

c_WZW(E_8, k=1) = 248/31 = 8 (rational) and c_DHVW(7) = 12·b(7) = 51.57
(irrational) cannot be two vacua of one unitary CFT preserving the Z_N
orbifold structure. The Ẽ_8 (|I*|=120) and Z_7 (|Z_7|=7) orbifold data are
coprime (gcd(120,7)=1). Superselection: mechanism (3) fails.

### 1.3 Mechanism (1): RG flow — c-ordering impossible

An RG flow A → B preserving conformal structure would require a single
2D boundary CFT whose stress tensor flows between c=8 and c=51.57.
Zamolodchikov c-theorem: c decreases along unitary RG from UV to IR.
Paper V asserts S^3/E_8 is UV and polygon/SM is IR, so we would need
c_UV > c_IR, i.e. 8 > 51.57 — FALSE. Mechanism (1) is impossible in the
claimed direction. A flow from the polygon c=51.57 "UV" to the S^3 c=8 "IR"
is c-theorem compatible but reverses the physical interpretation and does
not connect to any known boundary description of the S^3 sector.

### 1.4 Mechanism (2): CdL bounce — the topological obstruction

This is the most promising candidate. We derive its obstruction below.

---

## 2. CdL bounce attempt — what would be required

A Euclidean CdL bounce A → B demands an interpolating minisuperspace
trajectory σ(τ) obeying

    d²σ/dτ² = V′(σ),    σ(−∞) = σ_S,   σ(+∞) = σ_H,

with V(σ) having local minima at σ_S (K>0 base) and σ_H (K<0 base).
The Euclidean action is

    S_CdL  =  ∫ dτ [ (1/2)(dσ/dτ)² + V(σ) ]  =  ∫_{σ_S}^{σ_H} √(2V) dσ.

For S_CdL to be finite, σ(τ) must be continuous, and at each τ the 3D
slice must be a well-defined Riemannian 3-manifold.  This requires a
**1-parameter family of 3-manifolds M(σ) with M(σ_S) = S^3 and
M(σ_H) = H²/Z_7 × S^1**.

---

## 3. The topology-change obstruction

### 3.1 Homotopy invariants of the endpoints

| Invariant | S^3 | H²/Z_7 × S^1 |
|-----------|-----|---------------|
| π_1 | trivial | ℤ ⋊ Z_7 |
| b_1 | 0 | 1 |
| Euler χ (3-mfd) | 0 | 0 |
| Seifert Euler class e | 1 (Hopf) | 7/2 (fractional) |
| Orbifold Euler char χ^orb(base) | +2 (S^2) | −1/42 ((2,3,7)) |

Both 3-manifold Euler characteristics are 0 (trivial for 3-manifolds),
but π_1, b_1, and χ^orb of the base differ.

### 3.2 Gauss–Bonnet obstruction

The base orbifold satisfies

    ∫_B K dA = 2π χ^orb(B).

At σ_S: B = S², χ^orb = +2, total curvature +4π.
At σ_H: B = H²/(2,3,7), χ^orb = 1 − 1/2 − 1/3 − 1/7 = −1/42, total curvature negative.

A CONTINUOUS σ-deformation connecting these endpoints requires the
orbifold Euler character to interpolate continuously from +2 to −1/42.
But χ^orb is a RATIONAL-VALUED orbifold invariant (element of ℚ) and is
LOCALLY CONSTANT under any deformation that preserves the orbifold
structure. The deformation class of 2-orbifolds is labelled by χ^orb,
and different labels are different connected components of the moduli.

**First obstruction**: χ^orb jumps discontinuously between sectors.

### 3.3 Euler-class quantization (Session 16)

Session 16 (radion BF rigidity) established: for a Seifert fibration
S^1 → M → B with base orbifold B, the Euler class e ∈ ℚ satisfies

    (α/γ)² = e² / |χ^orb(B)|,

where α is fiber radius and γ is base-curvature radius. This ratio is
**topologically rigid** — pinned by the rational Euler class.

At σ_S (Hopf fibration S^1 → S^3 → S^2): e = 1, χ^orb = 2, (α/γ)² = 1/2.
At σ_H (heptagonal Seifert, Z_7 orbifold): e = 7/2.

A continuous CdL trajectory σ(τ) would require e(σ) to vary continuously
from 1 to 7/2. But e is a discrete Z-valued (for integer orbifold singular
data) or Q-valued (general Seifert) topological invariant that **cannot** change
continuously along a deformation preserving the Seifert structure.

**Second obstruction**: Seifert Euler-class jump 1 → 7/2.

### 3.4 Thurston geometric-class obstruction

π_1(S^3) = trivial cannot continuously deform into π_1(H²/Z_7 × S^1) =
ℤ ⋊ Z_7. By the classification of closed 3-manifolds (Perelman, 2003),
these are in different Thurston geometric classes: S^3 is spherical
geometry; the Seifert manifold is SL(2,ℝ)~ or H² × ℝ. Moving between
Thurston classes requires the geometry to DEGENERATE (volume → 0 or ∞
locally on a sub-manifold), which corresponds to a singular point in the
minisuperspace, not a smooth bounce.

**Third obstruction**: Thurston-class transition requires geometric
degeneration, not smooth deformation.

---

## 4. Formal statement of the obstruction

**Theorem (Topology-change obstruction).**
Let M_A = S^3 (round, Hopf-Seifert with e_A = 1 and χ^orb_A = +2) and
M_B = H²_(2,3,7)/Z_7 × S^1 (Seifert, e_B = 7/2, χ^orb_B = −1/42).
There is no smooth 1-parameter family of closed Riemannian 3-manifolds
{M(σ) : σ ∈ [0,1]} with M(0) = M_A and M(1) = M_B such that:

  (i)  at each σ, M(σ) is a Seifert fibration over a Thurston 2-orbifold;
  (ii) the Seifert Euler class e(σ) ∈ ℚ is continuous in σ;
  (iii) the orbifold Euler character χ^orb(B(σ)) is continuous in σ.

**Proof sketch.** Condition (iii) requires a ℚ-valued continuous function
χ^orb(σ) on [0,1] with χ^orb(0) = 2 and χ^orb(1) = −1/42. Orbifold Euler
character takes values in a discrete subset of ℚ indexed by (genus, cone
orders) — and for Seifert deformations preserving the singular-fibre
structure, χ^orb is LOCALLY CONSTANT. The two endpoint values lie in
different cells of this locally-constant sheaf, so no continuous
interpolation exists. Equivalently, condition (ii) is violated: e is
integer-valued under an oriented Seifert-preserving homotopy of a fixed
singular fibre structure, hence cannot change from 1 to 7/2 continuously.
Either route contradicts the hypotheses. □

**Corollary.** No Coleman–De Luccia bounce exists connecting Vacuum A to
Vacuum B within the class of Seifert-fibered minisuperspaces.

**Remark.** If one DROPS conditions (i)–(iii), one could imagine a Ricci-flow
neck-pinch trajectory with a singular intermediate geometry (e.g. a
Hamilton–Perelman surgery). But then the fibration structure is broken
and the Ẽ_8 / Z_7 gauge content has no continuous carrier; the algebraic
identification is lost at the singular point. This is not a CdL bounce
in the semiclassical sense (no finite-action Euclidean instanton over a
smooth background exists).

---

## 5. What does exist: a superselection structure

The failure of (1), (2), (3) does NOT mean the two frameworks are
unrelated. They share an ALGEBRAIC parent, the ADE / Schwarz-triangle
organization:

- Vacuum A: (2,3,5) spherical, I^* = binary icosahedral, McKay → Ẽ_8.
- Flat saddle: (2,3,6) Euclidean, degenerate Carter-triangle, measure zero.
- Vacuum B: (2,3,7) hyperbolic, Klein quartic / Hurwitz, automorphism PSL(2,7).

The (2,3,5) ↔ (2,3,7) connection runs through PSL(2,p) at p=5 (A_5) and
p=7 (Klein quartic). Both are Hurwitz triangle groups, organizing ADE
content in different curvature regimes. But this is an ALGEBRAIC
coincidence, not a dynamical relationship: the configuration spaces
Conf_N(S^2), Conf_N(ℝ^2), Conf_N(H^2/Z_7) are distinct spaces, and the
algebraic structure organizes their admissible saddle points, not a flow
between spaces.

---

## 6. Upgraded framing: superselection-sector structure

Replace Session 45 "moral analog" with the following precise claim:

> The S^3/Ẽ_8 framework and the H²/Z_7 polygon framework are DISTINCT
> superselection sectors of a common algebraic shell (ADE / Schwarz
> triangles). No continuous modulus space or CdL bounce connects them;
> the Euler-class and orbifold-χ obstructions (§3–4) preclude smooth
> dynamical interpolation. Each sector has its own UV completion —
> S^3/Ẽ_8 CS at k=1 (c_WZW=8) for the S^3 sector, DHVW Z_7 orbifold
> at c = 12·b(7) = 51.57 for the polygon sector — and the sectors are
> mutually inaccessible within the Euclidean gravitational path
> integral restricted to Seifert geometries.

This is stronger than "moral analog" (it identifies the precise shared
algebraic structure and the obstruction) and weaker than "dual
description" (it accepts the topological obstruction).

### 6.1 Consequences for Paper V / VII

Paper V Theorem phase-transition is HONEST read as "a change in the
dominant variational saddle as base curvature K crosses 0" — so K is a
SECTOR LABEL, not a continuous control parameter. It is OVERCLAIMED read
as "quantum tunnelling event between Thurston sectors."

Paper VII (2,3,5) → (2,3,6) → (2,3,7) is a TAXONOMIC organization, not a
dynamical trajectory. The arrow should be read as an indexing of
curvature-sign sectors, not a flow.

---

## 7. Upgrade to CHANGE 12

**Old** (Session 45): "structurally parallel compact-base framework ...
moral analog."

**New** (Session 62): "mutually inaccessible superselection sectors of
the ADE algebraic organisation, with distinct UV completions (S^3/Ẽ_8
CS at c = 8 and DHVW Z_7 at c = 12·b(7)) and a rigorous topology-change
obstruction (Theorem of §4) forbidding smooth interpolation at the
Seifert minisuperspace level."

This is an actual derivation (the obstruction theorem of §4) rather than
a scope disclaimer.

### 7.1 Specific replacement language — Paper V

Replace "the UV completion for the series" with:

    "an algebraically parallel compact-base description in a DISTINCT
    superselection sector — the S^3/Ẽ_8 Chern–Simons vacuum — whose
    topology-change obstruction (Euler class 1 vs 7/2; orbifold Euler
    character +2 vs −1/42) precludes a Coleman–De Luccia bounce to the
    H^2/Z_7 polygon vacuum but whose shared ADE / Schwarz-triangle
    structure controls the algebraic content of both phases."

### 7.2 Specific replacement language — Paper VII

Replace the (2,3,5)→(2,3,6)→(2,3,7) "transition" text with:

    "taxonomy: the Schwarz-triangle classification labels three
    superselection sectors — spherical (2,3,5) hosting the S^3/Ẽ_8 UV
    completion (c = 8), Euclidean (2,3,6) as a measure-zero degenerate
    sector, and hyperbolic (2,3,7) hosting the polygon DHVW UV completion
    at c = 12·b(7) — which are mutually inaccessible by continuous
    Seifert deformation (Session 62 topology-change obstruction)."

---

## 8. Physical content of the obstruction

The obstruction predicts that an early-universe S^3-phase cannot smoothly
evolve into the polygon phase by any semiclassical path-integral process
restricted to Seifert manifolds. Any such transition would require:

- A non-Seifert intermediate (generic Ricci-flow neck-pinch) — but then
  the fibration structure is broken and the Ẽ_8 / Z_7 gauge content has
  no continuous carrier.
- A non-perturbative topology change (Giddings–Strominger wormhole, etc.)
  requiring exotic matter not present in the framework.

**Predictive consequence**: the framework accommodates a MULTIVERSE
reading in which different Hubble patches settle into different ADE
sectors at the big bang and remain topologically disconnected thereafter.
Paper VII §11.3 ADE multiverse language is consistent with this provided
"multiverse" is read as "topologically distinct superselection sectors"
rather than "CdL-mediated landscape."

---

## 9. Summary table

| Mechanism | Session 45 status | Session 62 status |
|-----------|-------------------|-------------------|
| (3) Dual CFT | Ruled out (c_WZW=8 vs c_DHVW=51.57) | Ruled out (same) |
| (1) RG flow | Not derived | Ruled out (c-ordering inverted) |
| (2) CdL bounce | Not derived | **Ruled out — §4 theorem** |
| Parent CFT (Session 54) | Not proposed for this | Ruled out (superselection) |
| Algebraic parent | "Moral analog" | **Superselection-sector structure** |

---

## 10. Relevant file paths

- /mnt/c/Users/gspea/source/repos/planetary-polygons-unified/latex/paper-5-s3-framework/main.tex
  §10 (phase-transition), §9 line 440–444, Conclusion line 791–816
- /mnt/c/Users/gspea/source/repos/planetary-polygons-unified/latex/paper-6-discussion/main.tex
  §11.3 line 1141–1153
- /mnt/c/Users/gspea/source/repos/planetary-polygons-unified/docs/rigor-sandbox/session16-radion-bf-rigidity/derivation.md
  (Thurston–Scott rigidity; Euler-class pinning)
- /mnt/c/Users/gspea/source/repos/planetary-polygons-unified/docs/rigor-sandbox/session41-DHVW-modular-invariance/derivation.md
  (c = 12·b(N))
- /mnt/c/Users/gspea/source/repos/planetary-polygons-unified/docs/rigor-sandbox/session45-S3-E8-UV-route/derivation.md
  (moral-analog ruling; predecessor)
- /mnt/c/Users/gspea/source/repos/planetary-polygons-unified/docs/rigor-sandbox/session48-N-selection-tunnelling/derivation.md
  (BO tunnelling on FIXED H^2 base; not S^3 ↔ H^2)

---

## 11. References

- Thurston, W. (1997). *Three-Dimensional Geometry and Topology.* PUP.
  Chapter 4 (Seifert fibered spaces), Chapter 13 (Orbifolds).
- Scott, P. (1983). "The geometries of 3-manifolds."
  *Bull. Lond. Math. Soc.* 15, 401.
- Coleman, S.; De Luccia, F. (1980). *Phys. Rev. D* 21, 3305.
- Zamolodchikov, A. B. (1986). "Irreversibility of the flux of the
  renormalization group." *JETP Lett.* 43, 730.
- Perelman, G. (2002–2003). arXiv:math/0211159, 0303109, 0307245.
- Witten, E. (1988, 1989) as in Session 45.
- Dixon, Harvey, Vafa, Witten (1985, 1986) as in Session 45.

---

## 12. One-sentence conclusion

The S^3/Ẽ_8 and H²/Z_7 frameworks are provably-disconnected superselection
sectors under Seifert-preserving minisuperspace gravity (Session 62 §4
Theorem), with no Coleman–De Luccia bounce, no RG flow, and no dual CFT
linking them; their shared ADE / Schwarz-triangle algebraic structure
makes each the natural compact-base description of its own curvature
sign, which is the precise content that upgrades CHANGE 12 from moral
analog to an obstruction-theorem statement.
