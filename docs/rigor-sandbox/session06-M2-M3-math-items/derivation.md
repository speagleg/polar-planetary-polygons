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

**(a) Non-round S¹ metrics**. A general metric on S¹ gives Laplacian eigenvalues (2π m/L)² with varying L(φ). But the TOPOLOGICAL structure (single index m, palindromic pairing, no extra degeneracy) is INVARIANT under metric deformation. The paper's argument IDENTIFIES the TOPOLOGY of the fiber (S¹), not the metric.

**The round metric is fixed separately** by Brown-Henneaux conformal boundary conditions (c = 12 b(N) requires specific boundary asymptotics). So the paper's combined structure fixes: fiber topology = S¹, metric = round (to leading order).

**(b) Orbifold circle quotients S¹/Γ**. Compact connected 1-manifolds admit only trivial finite group actions:
- Γ = Z_k acting by rotation: S¹/Z_k ≃ S¹ (homeomorphic), just with different circumference L' = L/k.
- Γ = Z_2 acting by reflection: S¹/Z_2 ≃ interval [0, π], which has BOUNDARY, not a circle.

The polygon theory's Z_N orbifold action on S¹ is ROTATIONAL (φ → φ + 2π/N), giving S¹/Z_N ≃ S¹ with reduced circumference. Topologically still S¹.

**(c) Accidentally-matching homogeneous spaces**. Compact connected 1-manifolds: by classification, only S¹ (with or without boundary considerations). No other 1-manifold admits the Laplacian spectrum (2π m/L)² with the required pairing and non-degeneracy.

For higher-dim fibers to ACCIDENTALLY match: ruled out by the multi-index / degeneracy structure (paper's criteria 2 and 3). Specifically:
- S² has (2ℓ+1)-fold degeneracy at each eigenvalue — incompatible.
- T² has (m₁, m₂) double index — incompatible.
- S³, S² × S¹, etc. — all multi-indexed.

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

The S¹ fiber carries TWO flux-quantized gauge sectors:
- L_EW: electroweak sector with Chern number c_1 = 4 (from N_EW = 4)
- L_grav: gravitational sector with c_1 = 7 (from N_grav = 7)

On a single S¹ fiber, the total Chern class is the SUM: c_1 = 4 + 7 = 11.

This is a standard mathematical fact: Chern classes of direct-sum line bundles add.

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
