# Removed & Migrated Content Tracker

## Content Removals (cut, not moved)
Preserved with original location, reason, and suggested future home.

## Content Migrations (moved between papers)
Tracked with source paper/lines, destination paper, and any compression applied.

---

## Migrations Log (Series Restructuring 2026-03-31)

### M-001: Cosmological constant section → Paper V
**Source:** Paper IV, sec "The cosmological constant" (lines ~480-545)
**Destination:** Paper V, sec 2
**Compression:** None (clean extract)

### M-002: N selection principle → Paper V
**Source:** Paper IV, sec 15.1 "The N selection principle" (lines ~2540-2751)
**Destination:** Paper V, sec 3
**Compression:** Minor (post-elimination already cut)

### M-003: Cosmological energy budget → Paper V
**Source:** Paper IV, sec 15 remainder (CC theorem, budget proposition, DM spectrum, baryon fraction)
**Destination:** Paper V, secs 4-6
**Compression:** ~20% (H₀ error budget to be tightened)

### M-004: Baryogenesis → Paper V
**Source:** Paper IV, sec 16 (lines ~2989-3109)
**Destination:** Paper V, sec 7
**Compression:** None

### M-005: Neutrino masses → Paper V
**Source:** Paper IV, sec 17 (lines ~3109-3188)
**Destination:** Paper V, sec 8
**Compression:** None

### M-006: Radion inflation → Paper V
**Source:** Paper IV, sec 18 (lines ~3188-3235)
**Destination:** Paper V, sec 9
**Compression:** None

### M-007: Parameter accounting → Paper VI
**Source:** Paper IV, sec 19 (lines ~3235-3331)
**Destination:** Paper VI, sec 2
**Compression:** None

### M-008: Discussion → Paper VI
**Source:** Paper IV, sec 22 (lines ~4098-end)
**Destination:** Paper VI, secs 3-11
**Compression:** Minor

### M-009: Onsager-WDW correspondence → Paper III
**Source:** Paper IV, sec 21 (lines ~3704-4098)
**Destination:** Paper III, new final section
**Compression:** ~30% target

### M-010: Black hole entropy check → Paper III
**Source:** Paper IV, consistency checks (lines ~3776-3800)
**Destination:** Paper III, after BTZ section
**Compression:** None

### M-011: Nonlinear 4D Einstein theorem → Paper III
**Source:** Paper IV, consistency checks (lines ~3508-3610)
**Destination:** Paper III, after Einstein equations section
**Compression:** None (IV will reference instead of re-proving)

### M-012: Three-layer decomposition → Paper III
**Source:** Paper II, sec 11.2 (lines ~2307-2375)
**Destination:** Paper III, three-layer section
**Compression:** None

### M-013: TQFT independence remark → Paper III
**Source:** Paper II, Remark 9.4 (lines ~1999-2037)
**Destination:** Paper III, partition function section
**Compression:** None

---

## Removals Log (content cut, not moved)

## Removals Log

### I-001: Saturn/Jupiter illustration in spherical stability
**Source:** Paper I, lines 1016-1028 (pre-edit numbering)
**Reason:** PHYSICS_DIGRESSION — planetary observation in a pure mathematics paper
**Suggested home:** Predictions Paper or Reader's Guide (planetary scientist section)
**Original text:**
> \emph{Illustration.}
> Saturn's hexagon at $76^\circ$\,N ($\varphi_0 = 14^\circ$) lies
> inside $\varphi_{\mathrm{crit}}(6) = 25.8^\circ$: the hexagonal
> ring is in the stable zone (the planetary analysis is in Paper~II;
> here we note only the mathematical consistency).

**Note:** The N=7 and N>=8 limiting cases that followed (lines 1021-1028) were retained — they are pure mathematics.

---

### I-002: Physical realization paragraph (hyperbolic lattice experiments)
**Source:** Paper I, lines 2421-2493 (pre-edit numbering)
**Reason:** PHYSICS_DIGRESSION — experimental proposals in a mathematics paper
**Suggested home:** Predictions Paper (hyperbolic lattice section)
**Original text:**
> \paragraph{Physical realization.}
> The hyperbolic plane is no longer a purely mathematical object.
> \citet{Kollar2019} demonstrated that microwave resonators arranged in
> a tiling of the Poincar\'e disk implement the hyperbolic lattice
> Hamiltonian in circuit quantum electrodynamics, with negative
> effective curvature controlled by the lattice geometry.
> \citet{Lenggenhager2022} subsequently implemented hyperbolic space
> on a classical circuit board, showing that band structure and
> topological properties native to $\mathbf{H}^2$ are experimentally
> accessible.  These platforms realize, in a controlled laboratory
> setting, the geometry that Section~\ref{sec:hyperbolic} analyzes.
>
> The stability prediction translates directly into an experimental
> observable: \emph{a ring of $N$ vortex-like excitations on a
> hyperbolic lattice with ring-to-curvature ratio $R/a \approx 1$
> should be linearly stable up to $N = 12$, without requiring any
> central defect}.  In flat geometry, a 12-vortex ring is linearly
> unstable at every curvature-free configuration and can only be
> stabilized by a sufficiently strong central vortex
> (the Thomson--Havelock criterion requires a central circulation
> $\kappa_0 / \kappa \ge |\kappa_{\mathrm{crit}}(12)|$, which is large).
> The hyperbolic curvature replaces the stabilizing role of the
> central vortex: the geometry itself provides the restoring force.
> A predicted $N = 12$ stable ring with no center is impossible in
> flat geometry and would be a direct signature of hyperbolic curvature
> acting on vortex dynamics.

---

### I-003: Hyperbolic lattices as isolated Thomson test
**Source:** Paper I, lines 2448-2493 (pre-edit numbering)
**Reason:** PHYSICS_DIGRESSION — experimental methodology discussion
**Suggested home:** Predictions Paper (hyperbolic lattice section)
**Original text:**
> \paragraph{Hyperbolic lattices as an isolated test of Thomson stability.}
> In the planetary context, the three selection constraints---Rossby
> stationarity, Thomson stability, and geometric packing---are all
> active simultaneously and calibrated to the same observations;
> disentangling their individual contributions requires model-dependent
> assumptions.  A hyperbolic lattice experiment decouples them:
> \begin{itemize}
>   \item There is \emph{no} Rossby wave mechanism (no planetary
>     rotation, no $\beta$-effect).
>   \item Thomson stability is directly testable by counting stable
>     vortex excitations as $R/a$ is varied.
>   \item Geometric packing is controllable by engineering the
>     impurity spacing independently of the curvature.
> \end{itemize}
> This makes hyperbolic lattices the cleanest possible test of the
> Thomson constraint \emph{in isolation}.
>
> Moreover, the algebraic-integer thresholds
> (Proposition~\ref{prop:alg-int}) are \emph{exact, parameter-free}
> predictions:
> \begin{center}
> \begin{tabular}{cccl}
> \toprule
> Transition & $\xi^*$ (exact) & $\rho/a$ & Prediction \\
> \midrule
> $7 \to 8$   & $8 - 3\sqrt{7} = 0.0627\ldots$ & $0.51$ & 8-gon stabilises \\
> $8 \to 9$   & $5 - 2\sqrt{6} = 0.1010\ldots$ & $0.66$ & 9-gon stabilises \\
> $10 \to 11$ & $3 - 2\sqrt{2} = 0.1716\ldots$ & $0.88$ & 11-gon stabilises \\
> $14 \to 15$ & $2 - \sqrt{3} = 0.2679\ldots$ & $1.15$ & 15-gon stabilises \\
> $22 \to 23$ & $(3{-}\sqrt{5})/2 = 0.3820\ldots$ & $1.44$ & 23-gon stabilises \\
> \bottomrule
> \end{tabular}
> \end{center}
> The threshold values are algebraic numbers (Pell units and golden
> ratio powers).  Observing any of these
> transitions would constitute a direct experimental verification
> of the palindromic--Pell--conformal-inversion structure identified
> in Section~\ref{sec:algebraic-structure}.
> The physical conditions required to realize the hyperbolic vortex
> interaction in a circuit-QED or BEC platform are discussed in
> companion Paper~II alongside the BEC predictions.

---

### I-004: Open problem #2 (Saturn oblateness) — planetary reference removed
**Source:** Paper I, lines 2513-2514 (pre-edit numbering)
**Reason:** PHYSICS_DIGRESSION — planetary reference in math open problem
**Suggested home:** Predictions Paper
**Original text (removed portion only):**
> Paper~II shows this effect is critical for Saturn's hexagon
> ($10\%$ oblateness flips the sign of $\lambda_3$)
> but negligible for Neptune/Uranus.

**Note:** The mathematical open problem (non-constant curvature, spheroidal Green's function) was retained.

---

### I-005: Open problem #3 (experimental verification on hyperbolic lattices)
**Source:** Paper I, lines 2519-2526 (pre-edit numbering)
**Reason:** PHYSICS_DIGRESSION — experimental prediction, not a math open problem
**Suggested home:** Predictions Paper (hyperbolic lattice section)
**Original text:**
>   \item \emph{Experimental verification on hyperbolic lattices.}
>     The five algebraic-integer thresholds are parameter-free
>     predictions for circuit-QED or topoelectric platforms
>     implementing hyperbolic tilings.
>     The most accessible test: a ring of $N = 12$ excitations
>     at $R/a \approx 1$ should be stable---impossible on any
>     flat-geometry platform.

---

### I-006: Curvature dichotomy preview paragraph (redundant with Prop 5.5)
**Source:** Paper I, lines 345-352 (pre-edit numbering)
**Reason:** REDUNDANT — same content formally stated as Proposition (curvature-stability dichotomy) + dangling colon before subsection
**Suggested home:** Discard
**Original text:**
> The Gaussian curvature $K$ is a destabilizing perturbation when
> $K>0$ and a stabilizing one when $K<0$.  On the sphere ($K>0$) the
> deviation from the logarithmic Green's function lowers
> $N_{\mathrm{crit}}$ below~$7$; on the hyperbolic plane ($K<0$) it
> adds a positive $O(|K|)$ correction $12|K|$ to the formerly-marginal
> $\lambda_3$ eigenvalue.  The flat-plane case
> $K=0$ is therefore the \emph{least stable} point of the
> constant curvature family with respect to polygon formation:

---

### I-007: Pre-proposition curvature paragraph (redundant with Prop 5.5)
**Source:** Paper I, lines 2192-2198 (pre-edit numbering)
**Reason:** REDUNDANT — restates the Proposition that immediately follows
**Suggested home:** Discard
**Original text:**
> For any fixed ratio $R/a$ of ring radius to curvature radius, the
> Gaussian curvature $K$ controls the threshold: $K > 0$ reduces
> $N_{\mathrm{crit}}$ below~$7$, $K < 0$ raises it above~$7$, and
> $K = 0$ gives exactly~$7$.  The number~$7$ is the stability threshold
> at zero Gaussian curvature at the scale of the polygon ring.
> $K=0$ is the least stable point: the $N=7$ ring is marginal
> at $K=0$ and strictly stable for any $K<0$.

---

---

### IV-001: Graviton boundary mode stated 3x in 3 sentences
**Source:** Paper IV, lines 274-280 (pre-edit)
**Reason:** REDUNDANT — same statement three times; replaced with 2 sentences
**Suggested home:** Discard
**Original text:**
> A natural concern: $2{+}1$D gravity is topological---it has zero propagating degrees of freedom.
> The spin-$2$ graviton emerges from the boundary theory.
> The answer is that the $4$D spin-$2$ graviton is not a bulk field; it emerges from the boundary of the Chern--Simons theory via the Virasoro algebra.
> The spin-$2$ structure follows from the Virasoro algebra.

---

### IV-002: FG/Weinberg-Witten remark cut from 28 to 8 lines
**Source:** Paper IV, lines 353-381 (pre-edit)
**Reason:** DEFENSIVE — 20 lines of detail compressed to essentials
**Suggested home:** Discard (retained version has the key points)
**Original text (removed portions):**
> On the Seifert manifold, the conformal boundary $\partial\mathbf{H}^2 = S^1_\theta$ is fibred over $S^1_\varphi$.
> [full FG expansion form, spin^c detail, conformal boundary metric formula]
> the theorem's premise requires a massless spin-2 particle in a 4D Poincare-invariant local QFT with a Lorentz-covariant conserved T_{mu nu} constructible as a local polynomial in the fields.
> Our construction violates the premise in two ways: [enumerated]

---

### IV-003: SU(2) connecting paragraph (restates theorem+proposition)
**Source:** Paper IV, lines 821-830 (pre-edit)
**Reason:** REDUNDANT — restates what Theorem + Proposition just proved
**Suggested home:** Discard
**Original text:**
> Theorem identifies the gauge group; Proposition identifies its chiral action on matter. Together, they identify the gravitational SU(2) with the weak isospin SU(2): it arises from the same CS connection (A+), couples to the same chirality (left-handed), and its counterpart (A-, the right-handed sector) is broken by the same mechanism (parity anomaly from the oriented Seifert fibration) that produces P-violation in the Standard Model.

---

### IV-004: "not AdS/CFT" disclaimer #2 (UV completion section)
**Source:** Paper IV, lines 1434-1440 (pre-edit)
**Reason:** DEFENSIVE — second of four instances; first instance retained in SU(3) proof
**Suggested home:** Discard
**Original text:**
> (which predates and is logically independent of AdS/CFT),
> [...] No GKPW holographic dictionary is invoked: the CS/WZW correspondence is a theorem about 3D topological gauge theory, not a conjectured duality.

---

### IV-005: "not AdS/CFT" disclaimer #3 (consistency checks)
**Source:** Paper IV, line 3651 (pre-edit)
**Reason:** DEFENSIVE — third instance
**Suggested home:** Discard
**Original text:**
> without assuming 4D gravity or AdS/CFT

---

### IV-006: CKM uniqueness remark (restates proof)
**Source:** Paper IV, lines 1967-1985 (pre-edit)
**Reason:** DEFENSIVE/REDUNDANT — re-lists the three inputs just used in the proof
**Suggested home:** Discard
**Original text:**
> \begin{remark}[Uniqueness of the phase]
> The phase delta = 70.2 is determined by three inputs, each forced:
> (i) Delta c = 1 (the BF crossing); (ii) the scattering matrix S(s) (unique unitary S-matrix on H^2); (iii) arg Gamma (no free parameters).
> No alternative normalisation gives a different phase [... 18 lines total]

---

### IV-007: N=11 post-elimination restatements (~55 lines)
**Source:** Paper IV, lines 2692-2751 (pre-edit)
**Reason:** REDUNDANT — restates uniqueness just proved, re-derives c₁=4+7=11 a second time, re-explains flux additivity
**Suggested home:** Discard (key content: Frobenius SU(5) embedding retained in 5-line replacement)
**Lines saved:** ~50

---

### IV-008: Non-adiabatic coupling stated 4x in 17 lines
**Source:** Paper IV, lines 2389-2406 (pre-edit)
**Reason:** REDUNDANT — same fact (eigenvectors rho-independent, off-diagonal vanish, BO exact) said 4 ways
**Suggested home:** Discard (compressed to 6-line version)
**Lines saved:** ~10

---

### IV-009: Z/3Z invariance exact — stated 3x in 17 lines
**Source:** Paper IV, lines 969-986 (pre-edit)
**Reason:** REDUNDANT — "cannot break the symmetry because it's a property of the Casimir spectrum" said twice; "holds at all orders" said twice
**Suggested home:** Discard (compressed to 7-line version)
**Lines saved:** ~10

---

### IV-010: Section "Two-force unification" (26 lines, pure summary)
**Source:** Paper IV, lines 1387-1413 (pre-edit)
**Reason:** REDUNDANT — entire section restates Theorems from secs 4, 8, 9 with zero new content
**Suggested home:** Reader's Guide (as a structural overview for non-specialists)

---

### IV-011: Beta functions paragraph in consistency checks
**Source:** Paper IV, lines 3666-3674 (pre-edit)
**Reason:** REDUNDANT — restates sec 13 (one-loop corrections)
**Suggested home:** Discard

---

### IV-012: Baryogenesis quantitative paragraph in consistency checks
**Source:** Paper IV, lines 3763-3774 (pre-edit)
**Reason:** REDUNDANT — restates sec 16 results verbatim
**Suggested home:** Discard

---

### IV-013: Dynamical gluons paragraph in consistency checks (28 lines)
**Source:** Paper IV, lines 3801-3828 (pre-edit)
**Reason:** REDUNDANT — restates sec 8.2 (SU(3) from McKay, boundary WZW)
**Suggested home:** Discard (key content already in the SU(3) theorem)

---

### IV-014: b(N) multiple roles paragraph in Discussion (18 lines)
**Source:** Paper IV, lines 4353-4370 (pre-edit)
**Reason:** REDUNDANT — restates sec 5 (couplings) and Paper III four-role consistency
**Suggested home:** Discard

---

### IV-015: Gauge theory + GR paragraphs in Onsager-WDW section (21 lines)
**Source:** Paper IV, lines 4163-4183 (pre-edit)
**Reason:** REDUNDANT — restates results from secs 8, 20, and Paper III
**Suggested home:** Discard

---

### IV-016: Low-energy Minkowski remark cosmological expansion digression (16 lines)
**Source:** Paper IV, lines 217-232 (pre-edit)
**Reason:** RELOCATE — Friedmann/de Sitter/FRW belongs in cosmology sections
**Suggested home:** Cosmology section (already covered there)
**Lines saved:** ~22 (remark compressed from 36 to 10 lines)

---

### IV-017: SU(2) decoupling remark compressed (38 → 10 lines)
**Source:** Paper IV, lines 756-794 (pre-edit)
**Reason:** IMPROVE — useful content but verbose enumeration
**Suggested home:** N/A (compressed version retained)
**Lines saved:** ~28

---

### IV-018: Integrable bound / j=1 remark — same argument 3x compressed
**Source:** Paper IV, lines 1269-1296 (pre-edit)
**Reason:** REDUNDANT — Casimir/quantum-dimension independence said 3 ways
**Suggested home:** N/A (compressed version retained)
**Lines saved:** ~15

---

### IV-019: Scope of SU(3)_1 — "not QCD" compressed
**Source:** Paper IV, lines 1054-1073 (pre-edit)
**Reason:** DEFENSIVE — "It is not QCD. Rather..." pattern
**Suggested home:** N/A (compressed version retained, 3 lines saved)

---

### IV-020: V_cb/V_ub Discussion recap (9 lines)
**Source:** Paper IV, lines 4460-4468 (pre-edit)
**Reason:** REDUNDANT — V_cb stated for 4th+ time
**Suggested home:** Discard

---

### IV-021: b(N) re-derivation in Onsager-WDW (22 → 4 lines)
**Source:** Paper IV, lines 3939-3961 (pre-edit)
**Reason:** REDUNDANT — 4th derivation of b(N) in the series
**Suggested home:** Discard (replaced with 4-line reference)
**Lines saved:** ~18

---

### IV-022: 4D Lagrangian restatement of abstract (7 → 2 lines)
**Source:** Paper IV, lines 1434-1441 (pre-edit)
**Reason:** REDUNDANT — "Standard Model form with all couplings determined by N=7" restates abstract
**Suggested home:** Discard (replaced with 2-line summary)
**Lines saved:** ~5

---

### I-008: Cauchy functional equation re-derivation (redundant with Remark 2.1)
**Source:** Paper I, lines 939-947 (pre-edit numbering)
**Reason:** REDUNDANT — third statement of Cauchy equation; replaced with one-line back-reference
**Suggested home:** Discard
**Original text:**
> This property characterizes the
> logarithm \emph{uniquely}: among radially symmetric pairwise
> interactions on $\mathbb{R}^2$, $h = -\ln|z{-}w|$ is the unique
> function satisfying $h(d\lambda) = h(d) + h(\lambda)$ (additivity
> under rescaling---Cauchy's functional equation with continuity).
> This additivity under the dilation subgroup $z \mapsto \lambda z$
> (for which $|f(z){-}f(w)| = |\lambda|\,|z{-}w|$) is Cauchy's
> multiplicative functional equation $h(ab) = h(a) + h(b)$,
> whose unique continuous solution is $h = c\ln$.

---

### I-009: "csc^2 kernel in seven contexts" enumeration (~70 lines)
**Source:** Paper I, lines 2471-2539 (pre-edit numbering), Section 6 (B2 organising principle)
**Reason:** NO_NEW_CLAIMS -- self-described survey ("we make no new claims here"); 7-item enumeration of CMS, Dyson, Haldane-Shastry, Laughlin, Selberg, W_N, AGT/Nekrasov parallels
**Suggested home:** Discard (replaced with 5-line remark summarising the seven contexts)
**Original text summary:**
> Enumerated list connecting the Havelock csc^2 eigenvalue equation to seven integrable-system/random-matrix/CFT contexts. Each item identified the limit (classical, zero-temperature, frozen-particle, edge, etc.) relating Havelock to that context. Concluded with a summary paragraph listing all seven limits.

---

### I-010: "B2 circle closes through the index theorem" paragraph (~16 lines)
**Source:** Paper I, lines 2541-2556 (pre-edit numbering), Section 6
**Reason:** CHAIN_OF_ASSOCIATIONS -- CMS -> Haldane statistics -> Riemann-Roch -> Todd class -> B2 chain without proof
**Suggested home:** Discard
**Original text summary:**
> Argued that the Haldane fractional exclusion statistics of CMS at g_s=1 are governed by Riemann-Roch, whose Todd class has coefficient 1/12 = B2/2, closing a loop: CMS -> Haldane -> Riemann-Roch -> Todd -> B2 -> Havelock. Cited LiOuvry1994 and Paper III Prop equiv-rr.

---

### I-011: "4/3 self-interaction identity" paragraph (~18 lines)
**Source:** Paper I, lines 2558-2575 (pre-edit numbering), Section 6
**Reason:** TENUOUS_CONNECTION -- connects vortex 4/3 ratio to classical electron 4/3 problem via 4/3 = 1 + 2B2
**Suggested home:** Discard
**Original text summary:**
> Identified 4/3 = 1 + 2B2 connecting: (i) vortex csc^2 Laurent constant ratio (1/3)/(1/4)=4/3, (ii) classical electron Abraham-Lorentz angular integral sin^3(theta) = 4/3. Noted the vortex system's exact balance (sum of eigenvalues = 0) avoids regularisation.

---

### I-012: Remark 2.1 compression (28 -> 10 lines)
**Source:** Paper I, lines 146-174 (pre-edit numbering)
**Reason:** VERBOSE -- re-explains dilation invariance (already in Proposition above), includes prior-work comparison not essential
**Suggested home:** N/A (compressed version retained)
**Lines saved:** ~18
**Removed portions:**
> Definition of scale map T_b, explicit statement "rescaling changes h only by an additive constant (irrelevant to the force -h')", re-derivation that continuous solutions are -a ln r + b, N-body lift details (H(bz_1,...) formula), prior work comparison with Newton2001 conformal symmetry of stream function.

---

### I-013: K-theory section overview compression (37 -> 14 lines)
**Source:** Paper I, lines 2485-2521 (pre-edit numbering)
**Reason:** VERBOSE -- three-stage enumeration with full detail; compressed to single paragraph
**Suggested home:** N/A (compressed version retained)
**Lines saved:** ~23
**Removed portions:**
> Full enumerated description of stages (i)-(iii) with details: von Neumann algebra L(Gamma), L^2-weight percentages, placement-dependence invisible to R(Z_N), full Kasparov group description. Compressed to single paragraph retaining all three stages with key identifiers.

---

### III-001: Four-role consistency paragraph compressed (7 -> 1 line)
**Source:** Paper III, WDW section (lines ~1248-1254 pre-edit)
**Reason:** REDUNDANT -- restates Introduction paragraph (lines 74-84) verbatim
**Suggested home:** Discard (replaced with one-sentence back-reference)
**Lines saved:** ~6

---

### III-002: C1 notation disambiguation paragraph compressed (17 -> 3 lines)
**Source:** Paper III, WDW section (lines ~1189-1206 pre-edit)
**Reason:** IMPROVE -- replaced with concise Phi(rho) definition; C_1^GF superscript eliminated
**Suggested home:** N/A (compressed version retained)
**Lines saved:** ~14

---

### III-003: Pointer basis enumeration compressed (33 -> 5 lines)
**Source:** Paper III, Onsager-WDW section (lines ~3062-3094 pre-edit)
**Reason:** REDUNDANT -- three enumerated items (pointer basis, classicality, probabilities) duplicated in Theorem Q4/Q5/Q3
**Suggested home:** Discard (replaced with 5-line paragraph)
**Lines saved:** ~28

---

### III-004: CL conditions checklist compressed (37 -> 11 lines)
**Source:** Paper III, Onsager-WDW section (lines ~3095-3131 pre-edit)
**Reason:** VERBOSE -- four enumerated conditions with multi-line explanations compressed to inline list
**Suggested home:** N/A (compressed version retained)
**Lines saved:** ~26

---

### III-005: Quantum corrections + Born rule paragraph compressed (44 -> 6 lines)
**Source:** Paper III, Onsager-WDW section (lines ~3133-3174 pre-edit)
**Reason:** REDUNDANT -- Markov approximation, Feynman-Kac identity, Born rule all stated in the five-step chain above
**Suggested home:** N/A (compressed version retained)
**Lines saved:** ~38

---

### III-006: Feynman-Kac status paragraph removed (3 lines)
**Source:** Paper III, Onsager-WDW section (lines ~3279-3281 pre-edit)
**Reason:** REDUNDANT -- "mathematical identity, not physical derivation" stated second time (first at line 2923)
**Suggested home:** Discard
**Lines saved:** ~3

---

## Session 2b Removals (2026-03-31)

### I-014: Palindromic re-explanation #2 (lines 1420-1428 pre-edit)
**Source:** Paper I, Section 6 (Algebraic structure)
**Reason:** REDUNDANT — restates palindromic property from Section 5.1 (even-function explanation + conformal inversion identity)
**Suggested home:** Discard (compressed to 2-line cross-reference)
**Lines saved:** ~6

### I-015: Palindromic re-explanation #3 (lines 1461-1464 pre-edit)
**Source:** Paper I, Section 6 (field pattern discussion)
**Reason:** REDUNDANT — "deeper content is palindromic encodes conformal inversion (as noted above)"
**Suggested home:** Discard (compressed to 1-line reference)
**Lines saved:** ~2

### I-016: Palindromic re-explanation #4 (lines 1829-1833 pre-edit)
**Source:** Paper I, geodesic correspondence proof
**Reason:** REDUNDANT — re-derives palindromic origin for third time
**Suggested home:** Discard (replaced with eqref)
**Lines saved:** ~3

### I-017: Palindromic re-explanation #5 (lines 1883-1889 pre-edit)
**Source:** Paper I, Remark (automorphic correction)
**Reason:** REDUNDANT — first sentence restates; quotient-surface new content retained
**Suggested home:** Discard (compressed, quotient point kept)
**Lines saved:** ~3

### III-007: Step 4 higher-dimensions monolith (lines 2472-2536 pre-edit)
**Source:** Paper III, Theorem 6.1 proof
**Reason:** RESTRUCTURE — Step 4 (64 lines) duplicated existing Remark higher-d; replaced with 6-line reference
**Suggested home:** Already in Remark rmk:higher-d
**Lines saved:** ~55

### III-008: δS/δg computation extracted as Proposition (lines 2446-2470 pre-edit)
**Source:** Paper III, Theorem 6.1 proof
**Reason:** RESTRUCTURE — extracted 25-line computation as standalone Proposition prop:variation before theorem
**Suggested home:** Now Proposition (before theorem)
**Lines saved:** ~20 (net: computation now more compact as Proposition)

### III-009: Lemma lem:onsager-regge moved out of proof
**Source:** Paper III, inside Theorem 6.1 proof (lines 2286-2328 pre-edit)
**Reason:** RESTRUCTURE — 43-line lemma was inside proof; moved before theorem as standalone lemma
**Suggested home:** Now standalone Lemma (before theorem)
**Lines saved:** ~3 (net: replaced with 3-line reference in proof)

### III-010: c=12b(N) re-definitions compressed (multiple locations)
**Source:** Paper III, lines 1208-1216, 1254, 1260, 1419, 1441, 2899, 2912 (pre-edit)
**Reason:** REDUNDANT — added eq:central-charge label at first definition; 6 subsequent re-definitions replaced with eqref
**Suggested home:** Discard
**Lines saved:** ~8

### II-001: Infinite-dimensional convergence proof moved to appendix
**Source:** Paper II, lines 856-1034 (pre-edit, within blob bridge section)
**Reason:** RESTRUCTURE — 178-line proof (shape perturbations, center-shape coupling, Schur complement, inertia preservation proposition + 2 corollaries) moved to Appendix A
**Suggested home:** Paper II Appendix A (app:convergence)
**Lines saved:** ~97 (from main text; compressed version in appendix)

### VI-001: Input-output classification table merged into status table
**Source:** Paper VI, lines 451-512 (pre-edit)
**Reason:** RESTRUCTURE — 62-line separate table had heavy overlap with status table (8+ shared items). Merged into master 4-column table (Result/Role/Status/Match); replaced section with 8-line summary
**Suggested home:** Discard (content merged into master table)
**Lines saved:** ~48
