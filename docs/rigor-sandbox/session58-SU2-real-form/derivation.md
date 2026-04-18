# Session 58 — Compact SU(2) real form from polygon spin bundle

**Date**: 2026-04-18
**Branch**: feature/algebraic-extensions
**Closes**: Gap 7 (math reviewer) on CHANGE 2 §para:m4-isospin lines
  376–390 of PAPER4_REVISION_DRAFT.md: the "Euclidean continuation
  makes SL(2,ℝ) → SU(2)" argument is real-form confusion (Witten 1988,
  Witten 2007). Compact SU(2) must instead be derived from intrinsic
  polygon physics.

---

## 0. Bottom line

**The compact SU(2) real form is forced by global existence of the
polygon spinor bundle, not by analytic continuation.**

Primary argument (spin-bundle existence) is (1); it is logically
reinforced by (2) finite-dim fundamental rep and (3) unitarity on KK
sectors. Anomaly/level argument (4) is consistency; boundary-dual
argument (5) is irrelevant for bulk gauge and is rejected.

The compact real form is the unique choice for which:

  (a) the associated spin-1/2 bundle on M_3 = H²/Z_N ×_N S¹_iso is
      globally well-defined (Session 30: w_2(M_3) = 0, unique spin
      structure);
  (b) the Z/4 CP-orbit isospin doublet of Session 57 is a finite-
      dimensional **pseudoreal** representation of dimension 2, which
      exists on the compact SU(2) but not on non-compact SL(2,ℝ);
  (c) the chiral KK spectrum is unitary with positive-definite inner
      product (required for the 16 χ = L mode count).

Analytic continuation of Chern–Simons observables is NOT invoked. SL(2,ℝ)
and SU(2) are distinct real forms of sl(2,ℂ); they are not interchanged
by Wick rotation. The gauge group of the 3D polygon theory is fixed to
be compact SU(2) at the level of bundle data.

---

## 1. Problem statement

CHANGE 2 §para:m4-isospin (lines 376–390) argues: "In Lorentzian
signature the gauge group of each factor is SL(2,ℝ); under Euclidean
continuation the CS path integral is convergent only for the compact
real form, and both factors become SU(2)."

Math reviewer (verbatim): "SL(2,ℝ) and SU(2) are distinct real forms
of SL(2,ℂ), and analytic continuation does not swap them. The Witten
2+1D gravity path integral in Lorentzian signature with SL(2,ℝ) is
related to SL(2,ℝ) WZW, which is a well-studied object (Maldacena–
Ooguri), not compact SU(2)."

The reviewer is correct. We must derive compact SU(2) from an
intrinsic property of the polygon framework that does not rely on
continuation between real forms.

---

## 2. Setup: the polygon 3-manifold and its spin bundle

### 2.1 Geometry (from Sessions 29, 30, 57)

The polygon spacetime factor is the Seifert-fibered 3-manifold

    M_3 :  S¹_α  →  M_3  →  B = H²/Z_7,   Seifert Euler e = 7/2,

with base B the Hurwitz surface H²/Z_7 (three Z_7 cone points,
χ_orb = −4/7). The half-integer Euler class e = N/2 with N = 7 odd is
the key arithmetic input.

An auxiliary Z/4 isospin fiber S¹_iso (Session 57) commutes with the
S¹_α Seifert fiber and carries the m_4 KK index.

### 2.2 Spin bundle (from Session 30)

Session 30 proved: on M_3 at N = 7,

  - w_2(M_3) = 0 (orientable 3-manifold; Milnor–Stasheff 12.2);
  - H^1(M_3; Z/2) = 0 (Gysin with c̄_1 = 1 mod 2);
  - hence the spin bundle **exists and is unique**;
  - spinor holonomy around S¹_α is exp(2πi · 7/2) = −1
    (antiperiodic fermion BC).

By definition, a spin-1/2 bundle on an oriented Riemannian 3-manifold
is a principal Spin(3) = SU(2) bundle P_Spin → M_3 whose associated
frame bundle is the orthonormal frame bundle SO(M_3). **The structure
group of the spin bundle is, by definition of spin, the compact group
SU(2).** There is no SL(2,ℝ) spin bundle on a Riemannian (or
Lorentzian with timelike Killing direction) 3-manifold: the signature
(3,0) local model forces Spin(3) = SU(2).

This is already enough to fix the gauge group of the spinor sector to
compact SU(2). We now explain why the same compact real form propagates
to the Chern–Simons gauge connection that the spinors couple to.

---

## 3. Primary derivation (spin-bundle consistency)

### 3.1 Gauge–spin coupling requires matched structure group

The polygon isospin gauge field A^± is a connection on a principal
G-bundle P_G → M_3 that acts on fermions via the associated rank-2
bundle

    E  =  P_G ×_G  V_fund   (where V_fund is the fundamental rep).

Coupled Dirac operator on M_3:

    D\!\!\!\!/ _A  =  γ^μ (∇^{LC}_μ + A_μ)   acting on  P_Spin ⊗ E.

For the tensor product P_Spin ⊗ E to be a well-defined smooth bundle,
the transition functions of P_G must be compatible with those of
P_Spin. Both bundles transform under local rotations/gauge
transformations of the spinor frame, so the structure group G must act
on V_fund as a **subgroup of GL(2,ℂ) compatible with the Spin(3) = SU(2)
metric** on the spinor fiber.

Equivalently: the fundamental representation V_fund = C² carries a
positive-definite hermitian inner product ⟨·, ·⟩_spin induced from the
Riemannian metric on M_3 (via the spinor metric on P_Spin). For the
gauge connection A to preserve this inner product — a requirement of
unitarity of the coupled Dirac equation — G must act by unitary 2 × 2
matrices.

The real forms of sl(2,ℂ) ↪ gl(2,ℂ) are:

  - compact real form **su(2)**  (preserves positive-definite hermitian
    form on ℂ²);
  - non-compact **sl(2,ℝ)**       (preserves real bilinear form on ℝ²;
                                   no positive-definite hermitian
                                   invariant);
  - non-compact **su(1,1) ≅ sl(2,ℝ)** (preserves indefinite hermitian
    form of signature (1,1)).

Only su(2) preserves the positive-definite spinor inner product.
**Hence G = SU(2) is the unique real form of SL(2,ℂ) consistent with
the polygon spin-bundle data.**

### 3.2 Global obstruction from the half-integer Euler class

The Seifert Euler class e = 7/2 is HALF-integer. Spin-1/2 fields carry
holonomy exp(2πi · e) = −1 around S¹_α; this works because the
universal cover Spin(3) → SO(3) has kernel Z/2, so the half-integer
holonomy lifts uniquely to a sign on the spin bundle.

For a gauge group G acting on spin-1/2 fibers, the analogous lift
requires the gauge group to have a double cover compatible with Spin(3).
Concretely:

  - **SU(2)**: the gauge bundle P_G has π_1(SU(2)) = 0, so no additional
    global obstruction. The Seifert Euler class e = 7/2 is absorbed
    entirely into the spin structure. ✓
  - **SL(2,ℝ)**: π_1(SL(2,ℝ)) = ℤ, so gauge bundles on M_3 are
    classified by H^1(M_3; ℤ) ⊕ higher data. Sessions 30 gave
    H^1(M_3; Z/2) = 0, but H^1(M_3; ℤ) = H_1(M_3; ℤ) = Z_7 ⊕ Z_7 is
    non-trivial torsion. A non-compact gauge bundle would acquire
    additional Z_7 ⊕ Z_7 holonomy moduli, **not** matched by the
    polygon's intrinsic geometric data (which fixes the Seifert Euler
    class to the specific value 7/2 and nothing else in that sector).
    The extra moduli would overdetermine the theory.

Hence on the specific polygon M_3, the compact SU(2) bundle is uniquely
consistent with the Seifert geometric data; a non-compact SL(2,ℝ)
bundle would carry spurious torsion moduli and fail the rigidity
property that Paper IV uses throughout.

### 3.3 Z/4 isospin representation is pseudoreal of dimension 2

Session 57 derived the Z/4 CP-orbit structure:

    O_up = {1, 2}   (2-dim, doublet one),
    O_dn = {0, 3}   (2-dim, doublet two).

Each CP-orbit is 2-dimensional and supports a **pseudoreal
representation** — a representation with invariant antisymmetric
bilinear form ε_{ab} (the Pauli σ² form). The only compact simple Lie
group whose fundamental 2-dim representation is pseudoreal is
**SU(2)**: its fundamental rep admits the quaternionic structure
j : C² → C², j(z₁, z₂) = (−z̄₂, z̄₁), with j² = −1.

- SL(2,ℝ): fundamental rep on ℝ² is **real** (not pseudoreal); j² = +1.
- SU(1,1): fundamental rep on ℂ² is pseudoreal but preserves an
  **indefinite** hermitian form, incompatible with positive-definite
  spinor inner product (§3.1).

Hence the compact SU(2) is uniquely singled out: it is the only real
form of sl(2,ℂ) whose fundamental representation is both (i) 2-dim,
(ii) pseudoreal, and (iii) unitary with respect to a positive-definite
hermitian inner product — the three properties simultaneously
realized by the polygon's Z/4 CP-orbit isospin doublet.

---

## 4. Reinforcing arguments

### 4.1 Unitarity of finite-dim KK spectrum (from Session 57)

The KK mode space at each (m_7, m_4, χ) has dimension 1 per cusp, and
the polygon's 56 Weyl components per cusp must carry a unitary, finite-
dim representation of the gauge group to define a finite-dim
Hilbert-space inner product that descends to the 16 χ = L matter
modes.

- Compact SU(2): all unitary irreps are finite-dim (classical; Peter–
  Weyl). ✓
- SL(2,ℝ): non-trivial unitary irreps are infinite-dim (principal
  series, discrete series); the only finite-dim representations are
  non-unitary (Bargmann 1947). ✗

A finite-dim 2-component isospin doublet per KK mode therefore requires
compact SU(2).

### 4.2 Chern–Simons level quantization (from Session 42)

The polygon CS level k ∈ ℤ (Session 42) is quantized by π_3(SU(2)) = ℤ.
For non-compact SL(2,ℝ), π_3(SL(2,ℝ)) = 0, so the CS level is
unquantized — no integrality constraint — incompatible with the
polygon's discrete level structure derived in Sessions 24c, 42.
Compact SU(2) is necessary for CS level quantization.

### 4.3 Fermion chirality via Redlich

The Redlich mechanism (Paper IV §sec:chiral-su2) gaps χ = R fermions
via an induced topological mass term ∝ k_CS sign(m). This requires a
compact gauge group so that k_CS is integer-quantized (Redlich 1984);
non-compact SL(2,ℝ) has no analogous mechanism and would not yield a
chiral spectrum.

---

## 5. Why the "Euclidean continuation" argument is wrong

The discarded argument (CHANGE 2 lines 376–390) invoked the
continuation prescription

    Z_CS^Lorentz [SL(2,ℝ)]  ⟶  Z_CS^Eucl [SU(2)]

via Wick rotation. This is incorrect for two independent reasons
(Witten 1988 §2.4; Witten 2007 "Three-Dimensional Gravity
Reconsidered" §§2–3):

(W1) SL(2,ℝ) and SU(2) are distinct real forms of SL(2,ℂ). Real-form
     choice is topological data on the gauge bundle (π_1, π_3 differ),
     not kinematical data that Wick rotation can modify. The
     **complexified** algebras agree, but the integration contour in
     path integrals is independent per real form.

(W2) The Lorentzian SL(2,ℝ) Chern–Simons theory is a non-trivial
     well-studied object (Maldacena–Ooguri 2000, SL(2,ℝ) WZW and AdS_3
     strings); it is NOT formally the analytic continuation of
     compact-SU(2) CS. The two theories have different representation
     content, different partition functions, and different dual CFTs.

Hence the CHANGE 2 argument "the CS path integral is convergent only
for the compact real form, and both factors become SU(2)" misidentifies
convergence of a Euclidean Gaussian integral with a statement about
real-form choice. These are unrelated.

Our replacement argument (§3) never appeals to convergence of the CS
path integral. It derives compact SU(2) from:

  - global existence of the polygon spin bundle (forces Spin(3) = SU(2)
    structure group);
  - preservation of the positive-definite spinor hermitian form
    (forces unitary real form);
  - pseudoreal 2-dim Z/4 CP-orbit representation (forces SU(2)
    fundamental rep);
  - finite-dim unitary KK spectrum (excludes SL(2,ℝ));
  - π_3(SU(2)) = ℤ CS level quantization (excludes SL(2,ℝ)).

Each of these is a property of the polygon's intrinsic 3-manifold
geometry and representation content, not of a Wick rotation.

---

## 6. Proposed replacement text for CHANGE 2 lines 376–390

```latex
\emph{Step 1 (two sectors).}
The Witten Chern--Simons decomposition of $2{+}1$D gravity produces
two \emph{independent} CS connections $A^\pm = \omega \pm e/\ell$
(paper \S\ref{sec:gauge-derivation-chain} Step~2,
\citealt{Witten1988}). The gauge group of each factor is fixed to be
the \emph{compact real form} $\mathrm{SU}(2)$ of
$\mathrm{SL}(2,\mathbb{C})$ by the polygon's intrinsic spin-bundle
data, not by analytic continuation. Specifically (Session~58):
\begin{enumerate}
  \item \textbf{Spin-bundle structure group.} $M_3$ is Riemannian
    3-manifold with $w_2(M_3)=0$ and $H^1(M_3;\mathbb{Z}/2)=0$
    (Session~30). The unique global spin bundle is by definition a
    principal $\mathrm{Spin}(3)=\mathrm{SU}(2)$ bundle; its structure
    group is compact.
  \item \textbf{Positive-definite spinor norm.} Unitarity of the
    polygon Dirac operator requires the gauge group to preserve the
    positive-definite hermitian form on the spinor fundamental rep
    $\mathbb{C}^2$. Among real forms of $\mathfrak{sl}(2,\mathbb{C})$,
    only $\mathfrak{su}(2)$ does so; $\mathfrak{sl}(2,\mathbb{R})$
    preserves a real bilinear form (not hermitian) and
    $\mathfrak{su}(1,1)$ preserves an indefinite hermitian form.
  \item \textbf{Pseudoreal 2-dim Z/4 doublet.} The Z/4 CP-orbit
    isospin doublets of Lemma~\ref{lem:legendre} are 2-dimensional
    pseudoreal representations; the unique real form of
    $\mathrm{SL}(2,\mathbb{C})$ whose fundamental rep is 2-dim,
    pseudoreal, and unitary is compact $\mathrm{SU}(2)$.
  \item \textbf{Finite-dim unitary KK spectrum.} All non-trivial
    unitary irreps of $\mathrm{SL}(2,\mathbb{R})$ are infinite-
    dimensional (Bargmann 1947); the polygon's finite-dim KK modes
    per cusp force compact $\mathrm{SU}(2)$.
  \item \textbf{CS level quantization.} $\pi_3(\mathrm{SU}(2))=
    \mathbb{Z}$ quantizes the CS level, required for the discrete
    level structure of Sessions~24c,~42;
    $\pi_3(\mathrm{SL}(2,\mathbb{R}))=0$ gives no quantization.
\end{enumerate}
Hence both polygon CS sectors are compact $\mathrm{SU}(2)$ Chern--
Simons theories. Distinct real forms of $\mathfrak{sl}(2,\mathbb{C})$
are \emph{not} interchanged by Wick rotation
\citep{Witten2007GravityReconsidered}; the earlier draft's appeal to
``Euclidean continuation'' is withdrawn. The Standard Model gauge
groups $\mathrm{SU}(2)_L,\mathrm{SU}(2)_R$ are identified with the
two polygon $\mathrm{SU}(2)$ CS sectors (L/R assignment via parity
matching, Step~3); the two factors are distinct as gauge bundles but
have isomorphic structure groups.
```

---

## 7. Evidence table: why each candidate survives or fails

| Argument | Role | Necessary? | Sufficient? | Verdict |
|---|---|---|---|---|
| (1) Spin bundle = Spin(3) = SU(2) | Structure group | Yes | Yes (alone) | **Primary** |
| (2) Pseudoreal 2-dim fundamental | Rep content | Yes | Alone no, with (1) yes | **Supports** |
| (3) Finite-dim unitary KK | Unitarity | Yes | With (1), (2) yes | **Supports** |
| (4) CS level quantization | Consistency | Yes | No (only constrains k) | **Consistency** |
| (5) Boundary CFT SU(2)×SU(2) | Dual theory | No | No | **Rejected** (bulk≠boundary) |

Argument (1) alone suffices: the spin bundle on M_3 is by definition
an SU(2)-bundle, and the gauge field coupling to spinors inherits that
structure group. Arguments (2)–(4) independently exclude SL(2,ℝ) and
confirm consistency. Argument (5) is correctly identified as an AdS/CFT
dictionary move, not a real-form statement.

---

## 8. What is derived vs. input

**Derived from first principles**:
- Spin bundle structure group = SU(2) (Riemannian 3-manifold
  definition of Spin(3); Lawson–Michelsohn 1989).
- Unique real form preserving positive-definite hermitian form on ℂ²
  is su(2) (classification of real forms; Helgason 1978 Ch. X).
- Pseudoreal 2-dim irreps classified: only SU(2) fundamental is 2-dim
  pseudoreal unitary (Fulton–Harris 1991 §23).
- Finite-dim unitary irreps of SL(2,ℝ) do not exist non-trivially
  (Bargmann 1947).
- π_3(SU(2)) = ℤ vs π_3(SL(2,ℝ)) = 0 (standard; Bott periodicity).

**Physical input (not derived)**:
- Polygon 3-manifold M_3 = H²/Z_7 ×_N S¹ with e = 7/2 (Paper I).
- Gauge field A^± couples to fermion spinors via standard Dirac
  coupling.
- The isospin sector carries the Z/4 CP-orbit structure of Session 57.

---

## 9. References

- Witten, E., "Quantum field theory and the Jones polynomial,"
  Comm. Math. Phys. 121 (1989) 351, §2.4 (real-form choice in CS).
- Witten, E., "Three-Dimensional Gravity Revisited," arXiv:0706.3359
  (2007), §§2–3 (SL(2,ℝ) vs SU(2) in 3d gravity).
- Maldacena, J., Ooguri, H., "Strings in AdS_3 and SL(2,ℝ) WZW
  model," J. Math. Phys. 42 (2001) 2929, hep-th/0001053.
- Bargmann, V., "Irreducible unitary representations of the Lorentz
  group," Ann. Math. 48 (1947) 568 (SL(2,ℝ) reps infinite-dim).
- Helgason, S., *Differential Geometry, Lie Groups, and Symmetric
  Spaces*, Academic Press 1978, Ch. X (classification of real forms).
- Fulton, W., Harris, J., *Representation Theory: A First Course*,
  Springer GTM 129, 1991, §23 (pseudoreal representations).
- Lawson, H. B., Michelsohn, M.-L., *Spin Geometry*, Princeton 1989,
  Ch. II (Spin(n) = universal cover of SO(n), Spin(3) = SU(2)).
- Redlich, A. N., "Parity violation and gauge noninvariance of the
  effective gauge field action in three dimensions," Phys. Rev. D 29
  (1984) 2366.
- Session 30 (rigor-sandbox), "Global spin structure on N=7 Seifert
  manifold."
- Session 42 (rigor-sandbox), "Fractional CS level quantization."
- Session 57 (rigor-sandbox), "Native Z/7 × Z/4 derivation of W."

