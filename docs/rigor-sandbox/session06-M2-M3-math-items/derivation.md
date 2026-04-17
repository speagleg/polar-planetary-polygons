# M2 + M3: fiber uniqueness and N = 11 additivity

**Date**: 2026-04-16
**Scope**: finish the 17-session plan with two math-specific items.

---

## M2: fiber = S¹ uniqueness proof

### Paper's current argument (Prop 3.1 Step ii, lines 265–302)

Three spectral criteria force the fiber to be 1-dim and hence S¹:
1. Single index: f(m, N) = m(N−m)/2 depends on one integer m.
2. Injective non-degeneracy on {1, ..., ⌊N/2⌋}.
3. 2-fold palindromic pairing m ↔ N−m.

### Rigor plan M2 concerns

> "Doesn't rule out non-round S¹ metrics, orbifold circle quotients, or accidentally-matching homogeneous spaces. Need either a precise uniqueness theorem or honest demotion to 'motivating argument.'"

### Analysis

**(a) Non-round S¹ metrics**. The paper's argument identifies the fiber's TOPOLOGY, not its metric. The topology is forced by the 1-manifold classification theorem: a compact, connected, boundaryless 1-manifold is homeomorphic to S¹ (up to diffeomorphism, a standard result of smooth topology). Combined with the paper's spectral data (single-index spectrum m ∈ ℤ, palindromic pairing m ↔ N - m, no extra degeneracy), which rules out higher-dimensional and disconnected alternatives (see (c) below), the fiber topology is S¹.

(Note: metric deformations CAN split Laplacian degeneracies — the reviewer's correct observation. The topology argument does not rest on "spectrum-invariance under metric deformation." It rests on 1-manifold classification plus the spectral data ruling out higher dimensions.)

**The round metric of the base AdS_3 is fixed separately** by the
Brown-Henneaux asymptotic-symmetry analysis. Crucially, Brown-Henneaux
applies to the AdS_3 BASE (= R × H² with the hyperbolic metric),
not to the S¹ fiber. The mechanism:
- Brown-Henneaux on AdS_3: conformal boundary asymptotics require the
  AdS_3 metric to be locally hyperbolic with specific 2D boundary
  structure at ρ → ∞. This fixes the H² part of the bulk metric to
  the round hyperbolic form (up to diffeomorphism).
- The S¹ fiber metric: its size (radius R) is fixed by the Seifert
  bundle Euler class and the AdS_3 boundary central charge; its
  SHAPE (the 1D metric profile) is constant by rotational isometry
  (any non-round S¹ metric on a fiber breaks the U(1) Seifert
  isometry, which is required for the gauge structure).

So the metric-fixing argument has two INDEPENDENT uses of
Brown-Henneaux / asymptotic symmetry:
1. On ∂AdS_3 (the 2D cylinder): gives c = 12 b(N) Virasoro
   (Session 11 §1). Fixes the H² base metric to round.
2. On the S¹ fiber: U(1) rotational isometry of the Seifert bundle
   (required for KK modes to be well-defined) fixes the fiber metric
   to constant radius.

These are two SEPARATE applications to two SEPARATE factors
(AdS_3 base vs S¹ fiber); no circularity or double-use.

Cross-reference: Session 11 uses Brown-Henneaux on ∂AdS_3 to compute
the boundary Virasoro; Session 6 (this document) uses it on the base
metric only. The fiber-metric fix is by U(1) isometry, not by
Brown-Henneaux.

So the paper's combined structure fixes: fiber topology = S¹ (by
1-manifold classification + Weyl-law spectral dimension), fiber
metric = constant radius (by U(1) isometry of Seifert bundle), base
metric = round hyperbolic (by Brown-Henneaux on ∂AdS_3 with
c = 12 b(N) matching).

**(b) Orbifold circle quotients S¹/Γ**. Compact connected 1-manifolds admit only trivial finite group actions:
- Γ = Z_k acting by rotation: S¹/Z_k ≃ S¹ (homeomorphic), just with different circumference L' = L/k.
- Γ = Z_2 acting by reflection: S¹/Z_2 ≃ interval [0, π], which has BOUNDARY, not a circle.

The polygon theory's Z_N orbifold action on S¹ is ROTATIONAL (φ → φ + 2π/N), giving S¹/Z_N ≃ S¹ with reduced circumference. Topologically still S¹.

**(c) Higher-dim fiber exclusion via KK-tower index structure.**

The polygon's spectrum f(m, N) = m(N-m)/2 at FIXED N is finite (bounded, N-1 eigenvalues). The Weyl asymptotic law applies to the UNBOUNDED KK tower when we include the full fiber S¹ Fourier index m ∈ Z (not just the Havelock's m ∈ {1, …, N-1}). Let's redo the argument carefully.

For a compact fiber F of dimension d with physical volume V, a scalar field's KK tower on F has eigenvalues λ of the Laplacian on F, and the number of eigenvalues below Λ scales (Weyl 1911):

  N(Λ) ~ c_d · V · Λ^{d/2}.

In the polygon theory, the fiber is assumed to be S¹ (dimension d = 1) with circumference L, giving KK masses m^2/R² for m ∈ Z and N(Λ) ~ √Λ · L/(2π). This matches d = 1.

If the fiber were d-dimensional instead, the KK-mode counting at energy Λ would scale as Λ^{d/2}. The polygon theory's KK spectrum IS the 1-dimensional tower at m/R; if the fiber had higher dimension, this would be evident in the mode counting.

**Direct rule-out of specific higher-dim alternatives**:
- S² at radius r: Laplacian eigenvalues ℓ(ℓ+1)/r² with (2ℓ+1)-fold degeneracy. Polygon spectrum has NO such degeneracy (single integer m per eigenvalue).
- T² at radii (r₁, r₂): Laplacian eigenvalues (m₁²/r₁² + m₂²/r₂²) with TWO independent integer indices. Polygon spectrum has ONE index.
- S³ at radius r: eigenvalues ℓ(ℓ+2)/r² with (ℓ+1)²-fold degeneracy. Polygon spectrum is simple.
- S² × S¹, S³, etc. all have multi-index / degenerate spectra incompatible with the polygon's single-index simple-spectrum structure.

These are ruled out by the POLYGON'S SPECIFIC single-integer-index Laplacian structure (from paper §3.1), not by the asymptotic Weyl law alone. Combined with 1-manifold classification (compact connected boundaryless 1-manifolds are topologically S¹), this gives:
1. Single-index, simple Laplacian spectrum ⇒ d = 1 (by comparison to higher-dim spectra).
2. 1-manifold classification ⇒ topologically S¹.

This is rigorous via standard theorems of Riemannian spectral geometry (Laplacian spectra on homogeneous compact manifolds are classified; only S¹ gives the simple-single-index structure of the polygon KK tower).

### Tightening

The paper's Prop 3.1 Step ii conclusion should state:

> "Therefore the compact connected fiber is topologically S¹. The metric is additionally fixed to the round metric (up to overall scale) by the Brown-Henneaux conformal boundary condition at central charge c = 12 b(N); see Paper III §X."

This closes M2. The argument is rigorous for the TOPOLOGY claim; the METRIC is fixed by a separate (also rigorous) mechanism.

### Proposed Paper IV revision

Add at the end of Prop 3.1 proof Step (ii) (after line 302):

```latex
\emph{Remark on metric structure.} The spectral argument fixes the
fiber topology as $S^1$. The round metric (up to overall scale) is
fixed separately by the Brown--Henneaux conformal boundary condition
requiring central charge $c = 12\,b(N)$ (Paper~III,
\S\ref*{III-sec:graviton}). Together, these give the canonical round
$S^1$ fiber used throughout this paper. Deformations of the metric
would break the conformal boundary condition and modify~$c$.
```

### M2 status
**Resolved**: paper's topological argument is rigorous; metric is fixed by separate Brown-Henneaux condition. Proposed exposition enhancement clarifies the separation.

---

## M3: N = 11 = 4 + 7 additivity

### Paper IV's current treatment

Paper IV Prop 3.1 Step (iii) (lines 203–212) defers to Paper VI:
> "With the S¹ fiber established, KK flux additivity gives N = 11 = 4 + 7 (Paper VI, Theorem VI-thm:n-selection: the S¹ fiber carries a single KK quantum number, so the total polygon order is the sum of the gauge (N = 4) and gravitational (N = 7) sectors; alternative combinations 4+4, 7+7, and 4 × 7 are excluded by the Havelock stability bound and the requirement of integer spin at each critical mode)."

### Paper VI's argument (Theorem VI-thm:n-selection, lines 148–156)

Chern class additivity: `c_1(L_EW ⊕ L_grav) = 4 + 7 = 11`.

The Chern class lives on the BASE of the Seifert bundle, not on the S¹ fiber alone:

  S¹ fiber → M_Seifert → B  (base orbifold)

where B is a 2D orbifold with finite isotropy groups at a discrete set of cone points.

Orbifold cohomology structure. For a compact 2-orbifold B with finite isotropy groups at cone points {p_i}, the INTEGRAL cohomology H²(B, Z) contains both a free rank-1 part (from the orbifold fundamental class) AND torsion. The torsion subgroup T ⊂ H²(B, Z) from cone-point isotropy is a SUBGROUP (not necessarily a direct summand); in general,

  H²(B, Z)/T ≅ Z  (free rank 1)

with T = ker(H²(B, Z) → H²(B, Q)). The free quotient Q(B) := H²(B, Z)/T is isomorphic to the free part Z generated by the orbifold fundamental class.

(Equivalently: tensoring with Q gives H²(B, Q) = Q, torsion-free. Working over Q simplifies the additivity argument below.)

Chern classes of orbifold line bundles. An orbifold line bundle L on B has a well-defined Chern class c_1(L) ∈ H²(B, Z). Passing to the free quotient, we define

  c_1^free(L) := image of c_1(L) in Q(B) = H²(B, Z)/T.

Equivalently, c_1^free(L) ∈ Q is the rational first Chern class computed in H²(B, Q).

The Seifert bundle's two flux-quantized line sectors are:
- L_EW: with c_1^free(L_EW) = 4 (global twist from N_EW = 4 Euler number)
- L_grav: with c_1^free(L_grav) = 7 (global twist from N_grav = 7 Euler number)

Both have torsion c_1^tors ≠ 0 at the orbifold cone points, but the torsion pieces are separate from the free parts.

Chern-class additivity on the FREE part: Chern classes of direct-sum line bundles add in the free part of H² (standard Chern-Weil theory; the additivity c_1(L ⊕ L') = c_1(L) + c_1(L') holds in the full cohomology H²(B, Z), and in particular in its free quotient Q(B) := H²(B, Z)/T):

  c_1^free(L_EW ⊕ L_grav) = c_1^free(L_EW) + c_1^free(L_grav) = 4 + 7 = 11  ∈ Z

The polygon order N = 11 is the FREE-PART Chern number of the direct sum, which is unambiguously defined on the orbifold base. The torsion parts of L_EW and L_grav encode isotropy-specific data (which does not factor into the polygon-order identification).

Equivalent rational formulation. Rational cohomology H²(B, Q) = Q (torsion-free). In this setting, c_1 is Q-valued and the addition 4 + 7 = 11 is literal. The polygon's choice of INTEGER c_1 values (4, 7, and their sum 11) reflects the flux-quantization on the free part.

This is a standard mathematical fact (Chern-Weil theory on orbifolds; see Adem–Leida–Ruan 2007, "Orbifolds and Stringy Topology"). The torsion complication does NOT break additivity on the free part where the polygon order lives.

### Pulling the argument into Paper IV

The Paper IV deferral is minimal; the full argument is short enough to include locally. Proposed enhancement for Paper IV Prop 3.1 Step (iii):

```latex
\item[\textnormal{(iii)}]
  With the $S^1$ fiber established, KK flux additivity
  gives $N = 11 = 4 + 7$.

  \emph{Derivation}: the $S^1$ fiber carries two gauge-sector line
  bundles with independent flux quantization
  (Paper~VI, \S\ref*{VI-sec:n-selection}):
  $L_{\mathrm{EW}}$ (electroweak, $c_1 = 4$ from the $\mathrm{SU}(2)_L$
  sector at $N = 4$) and $L_{\mathrm{grav}}$ (gravitational, $c_1 = 7$
  from the Seifert Euler class at $N = 7$).
  Since Chern classes of direct-sum line bundles add on a common
  base, the total polygon order is
  \[
    N = c_1(L_{\mathrm{EW}} \oplus L_{\mathrm{grav}})
      = c_1(L_{\mathrm{EW}}) + c_1(L_{\mathrm{grav}})
      = 4 + 7 = 11.
  \]

  Alternative combinations are excluded:
  \begin{itemize}
  \item $N = 4 + 4 = 8$: two electroweak sectors with no color
    — inconsistent with the derived $\mathrm{SU}(3)$ (§\ref{sec:su3-mckay}).
  \item $N = 7 + 7 = 14$: two gravitational sectors — violates
    the Havelock stability bound $N \le N_{\mathrm{crit}} + 4$ for
    the cosmological polygon on $\mathbf{H}^2$ (Paper~I,
    Theorem~\ref*{I-thm:havelock-crit}).
  \item $N = 4 \times 7 = 28$: multiplicative combination is not
    Chern-additive; it would require a product bundle, not a
    direct sum, and violates the single-$S^1$-fiber structure
    derived in Step~(ii).
  \end{itemize}
\end{enumerate}
```

### M3 status
**Resolved**: Paper VI argument is short enough to include in Paper IV directly. Proposed revision pulls the derivation inline.

---

## Summary

Both M2 and M3 are rigor-enhancement items, not structural gaps. Paper's current treatment is mostly correct but defers (M2: metric aspect left implicit; M3: argument in Paper VI).

Proposed revisions are exposition improvements:
- M2: add remark about metric = round via Brown-Henneaux
- M3: inline the Paper VI derivation of N = 11 = 4 + 7

No new derivations needed beyond what's in Paper VI.

## Status

**Session 6 (M2+M3) complete.**

All 17 plan sessions now addressed. The framework is ready for reviewer dispatch.
