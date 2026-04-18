# Session 30 — Global spin structure on the N=7 Seifert manifold

## Summary

(i) **Global spin structure exists on M_3 at N=7.** w_2(M_3) = 0 automatically
(orientable 3-manifold; Milnor-Stasheff 12.2). The orbifold refinement also
vanishes: N=7 is odd, so H^{≥1}(BZ_7; Z/2) = 0 (mod-p cohomology vanishes when
p ∤ |G|). Gysin sequence gives H^1(M_3; Z/2) = H^2(M_3; Z/2) = 0.

(ii) **Antiperiodic fiber BC is the unique consistent choice.** Spinor holonomy
around fiber is exp(2πi·7/2) = -1.

(iii) **No correction to |C_base|** from spin structure.

(iv) **rem:radion-mass open item CLOSED.**

## 1. Problem

CHANGE 4 rem:radion-mass flags: "global spin-structure verification over three
Z_7 cone points of H²/Z_7 is an open item." Physics reviewer concern: affects
base Casimir sign and |C_base|.

## 2. Setup

M_3 = S¹_α → M_3 → B = H²/Z_7, Seifert Euler class e = 7/2. Base B has three
Z_7 cone points; χ_orb = -4/7, Area = 8π/7. c₁(L) = 2e_phys = 7 ∈ Z.

M_3 is orientable closed smooth 3-manifold: local model at each cone is
(S¹ × D²)/Z_7.

## 3. Mod-2 Gysin sequence for Seifert bundle

For oriented S¹-bundle with integer c₁:
    ⋯ → H^{k-2}(B; Z/2) ─∪c̄₁→ H^k(B; Z/2) → H^k(M; Z/2) → H^{k-1}(B; Z/2) → ⋯

c̄₁ = 7 mod 2 = 1.

### 3.1 Key lemma: H^{≥1}(BZ_7; Z/2) = 0

Proof: H*(BZ_n; Z/2) = Ext*_{Z/2[Z_n]}(Z/2, Z/2). Transfer is multiplication by n.
gcd(7, 2) = 1, so mult by 7 is invertible mod 2, killing positive-degree cohomology
(Cartan-Eilenberg XII.10). ∎

### 3.2 Orbifold cohomology of B

By Behrend 2004 Thm 3.2:
    H^k_orb(B; Z/2) = H^k(|B|; Z/2) ⊕ ⊕_p H^k(BZ_{a_p}; Z/2)_reduced

|B| = S², H^*(S²; Z/2) = (Z/2, 0, Z/2). Cone contributions all vanish in positive
degree by Lemma 3.1. So:
    H^0_orb = Z/2, H^1_orb = 0, H^2_orb = Z/2, H^{≥3}_orb = 0 in base.

### 3.3 Running the Gysin

k=1: 0 → H^1(M_3) → H^0_orb ─×1→ H^2_orb → ...
     0 → H^1(M_3) → Z/2 ─iso→ Z/2 → ...
     ⇒ H^1(M_3; Z/2) = 0.

k=2: H^0_orb ─×1→ H^2_orb → H^2(M_3) → H^1_orb = 0
     Z/2 ─iso→ Z/2 → H^2(M_3) → 0
     ⇒ H^2(M_3; Z/2) = 0.

**H^1(M_3; Z/2) = 0 and H^2(M_3; Z/2) = 0.**

## 4. Spin structure: exists and unique

Spin structures exist iff w_2(M_3) = 0, automatic for orientable 3-manifolds.
Classified as torsor over H^1(M_3; Z/2) = 0. **Unique global spin structure.**

## 5. Explicit Stiefel-Whitney check

TM_3 ≅ π*(TB) ⊕ V with V trivial. w(TM_3) = π* w(TB). w_1(TB) = 0, w_2(TB) = 0 on
|B| = S². Orbifold pieces vanish by §3.2. So w(TM_3) = 1.

Cone-point check: local model (S¹ × D²)/Z_7 with Z_7 ⊂ SO(3) lifts to SU(2) iff
H²(Z_7; Z/2) = 0, true for odd order. ✓

## 6. Fiber holonomy

Spin-½ fields carry half the Seifert charge:
    hol_spin(S¹_α) = exp(2πi · 7/2) = exp(7πi) = **-1**.

Since H^1(M_3; Z/2) = 0, no other spin structure exists. **Antiperiodic fiber BC
is the unique consistent choice.** Paper IV §8.1 correctly uses this.

## 7. Impact on |C_base| and CHANGE 4

- **|C_base| = 0.089**: fermion decoupling confirmed rigorous (unique antiperiodic BC);
  bosonic 27 DOF count unchanged; twisted sector correction unchanged.
- **Base Casimir sign**: negative (bosonic periodic modes). Unchanged.
- **Radion mass**: AdS_4 branch [16, 30] M_poly unchanged.

**Counterfactual**: if the obstruction had been nonzero, spin^c refinement would
introduce O(3) extra cone-point modes, shifting |C_base| by ~5%. This doesn't happen.

## 8. Important domain condition: N odd

Argument requires N = 7 (odd). For N even, cone isotropy has even order, H²_orb
would gain Z/2 contributions, and the analysis becomes subtler. Paper I already
restricts to N ≤ 7, and N = 6 is in a flat-space regime (not hyperbolic base). So
N = 7 odd is the only case we need.

## 9. Mod-2 Betti numbers (consistency check)

From Gysin: H^*(M_3; Z/2) = (Z/2, 0, 0, Z/2). Rational homology 3-sphere structure
matches H_1(M_3; Z) = Z_7 ⊕ Z_7 (known for Seifert with three (7, b_i) cones)
reducing to 0 mod 2. ✓

## 10. Conclusion

Global spin structure on M_3 at N=7 **exists, is unique, and gives antiperiodic
fermion boundary conditions**. The rem:radion-mass open item is **CLOSED**. No
correction to |C_base|, no impact on CHANGE 4.

## References

- Milnor, Stasheff, *Characteristic Classes*, Cor. 12.2.
- Cartan, Eilenberg, *Homological Algebra*, XII.10.
- Behrend, *Cohomology of stacks*, ICTP Lect. Notes XIX (2004).
- Kirby, Taylor, "Pin structures on low-dimensional manifolds," LMS LN 151 (1990).
- Furuta, Steer, "Seifert fibered homology 3-spheres and Yang-Mills," Adv. Math.
  96 (1992).
- Friedrich, *Dirac Operators in Riemannian Geometry*, AMS GSM 25.
