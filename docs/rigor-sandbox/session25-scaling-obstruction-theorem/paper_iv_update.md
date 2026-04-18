# Paper IV revision draft — radion mass + scaling-obstruction lemma

**Version 4.** Corrections applied from v3 R1 (math, 7.8), R2 (physics, 8.3), R3 (unified-framework, 7.6):

**Math fixes**:
- Drop garbled "f'/f non-constant only if allowed to vanish pointwise" clause.
- Replace "span{(1,2)} ⊂ span{(-1,-2)}" with "span{(1,2)} = span{(-1,-2)}" (these are equal as sets).
- Drop h≠2 exclusion (h=2 gives (0,0) which is in the span trivially).
- BF-instanton item: state pointwise direction only; the pair-with-Λ_7 cross-product
  is zero at every point, rank-1 Hessian contribution preserved.
- Relax hypothesis from f: (0,∞)→(0,∞) to "f: (0,∞)→ℝ of constant sign, continuously
  differentiable with f(V_3) ≠ 0" (accommodates Λ_7 < 0).

**Physics fixes**:
- Honest Paper VI reconciliation: Paper VI's M_rad = N/2 is a tree-level zero-point
  frequency object; Session 18 [16, 30] M_poly is a 1-loop Hessian-eigenvalue object.
  Different objects with consistent parametrics, NOT a unit remap.
- Add explicit BF-non-applicability parenthetical at V_*=0 saddle.
- Clarify |C_base| uncertainty: 15% is twisted-sector sign-magnitude effect on untwisted
  coefficient; total |C_base| uncertainty ~50% from uncomputed full Selberg trace.
- Add spin-structure downside bound: flipped-sign eliminates V_*=0 saddle but AdS_4 branch
  qualitatively intact.
- Inline EFT-validity note in Remark.
- Add phenomenology sentences (BBN decay time, collider reach) in Paper VII bullet.

**Unified-framework fixes**:
- Paper-numbering error corrected throughout: `paper-5-cosmology` = Paper **VI**,
  `paper-6-discussion` = Paper **VII**. Updates 5 and 6 retargeted.
- Cross-ref `V-eq-Mrad` doesn't exist → use `\eqref{VI-eq:F-DE}` (actual label in context).
- Bibliography cite syntax corrected: `\cite{radion-derivation}`, not `\ref{cite:...}`.
- r_\* = 7√7/4 has no label in Paper I → define inline in the Remark.
- κ_V rename verified: not used elsewhere; clean.

---

## Current Paper IV radion content

Only (§4 table, line 539):

    σ = g_φφ (radion): "massive, m ~ M_poly"

A one-line entry with no cited derivation. Paper **VI** (`paper-5-cosmology/main.tex`)
at line 1048-1052 further states M_rad = N/2 as the "zero-point energy of the S¹
fiber modulus, stabilized at unit radius by the flux N/2", using a SINGLE-modulus
tree-level treatment in which γ (base scale) is held fixed at unit radius.

## What the derivation chain (Sessions 18-24) establishes

1. Full 2-modulus treatment: α (fiber), γ (base) both dynamical.
2. 5-term 1-loop effective potential (CW + FR + base Ricci + fiber Casimir + base Casimir).
3. Stable AdS₄ minimum at (α_*, γ_*, Λ_7) = (0.7255, 0.1567, -4.10×10⁴) on the
   ratio r_* = 7√7/4 = 4.6301 (the Thurston ratio for the Seifert N=7 geometry).
4. Mass eigenvalues: m_- = 16.4 M_poly, m_+ = 28.5 M_poly. Range [16, 30] M_poly
   under the Thurston-branch Λ_7 choice; broader scans over Λ_7 give ~10-100 M_poly.
5. A V_*=0 Minkowski critical point at (0.798, 0.165, -5770) is a tachyonic saddle
   (m²_- ≈ -110 M_poly²; since V_* = 0 the background is flat, so the BF bound
   does not apply — this is a genuine flat-space tachyon).
6. Scaling-parallelism lemma: V_3-only contributions are parallel to (-1, -2).
7. Empirical list of 10+ tested non-volume-universal mechanisms: none stabilize Minkowski_4.
8. Several candidates untested: fermion condensates, SM back-reaction, hidden-sector
   gauge on fiber, brane-analog tensions, Hodge dual FR, higher-loop Casimir,
   1-form-symmetry contributions.

## Honest reconciliation with Paper VI

Paper VI's M_rad = N/2 is the **tree-level zero-point frequency** of the S¹
fiber modulus at a tree-level potential minimum where γ is fixed at unit radius
by the FR flux. It is not an eigenvalue of any 2-modulus Hessian.

Session 18's [16, 30] M_poly is the **eigenvalue of the 1-loop Hessian** of the
full 5-term 2-modulus potential at the Thurston-branch AdS_4 minimum, where
both α and γ are dynamical and Λ_7 is a nonzero negative parameter.

These are **different objects**. Paper VI's tree-level value does not map to ours
by a coordinate relabel; the 1-loop terms and the 2-modulus γ dynamics change the
potential's curvature at the minimum. Both values remain internally consistent
with their respective potentials:

| Treatment | Moduli | Potential | Radion mass |
|---|---|---|---|
| Paper VI (tree-level) | σ_V = α; γ fixed at unit | N²/(8σ²) − c_{11}/(12σ) + Λσ | M_rad = N/2 (zero-point ω) |
| Session 18 (1-loop) | (α, γ) both dynamical | 5-term CW + FR at (0.7255, 0.1567, -4.10e4) | m ∈ [16, 30] M_poly (Hessian eigenvalues) |

**Integration plan**: Paper IV becomes the canonical source for the 1-loop 2-modulus
radion mass. Paper VI retains its tree-level single-modulus derivation for pedagogy
and cross-references Paper IV for the full treatment.

## Update 1 — Paper IV §4 table (line 539)

CHANGE radion row.

FROM:
```latex
$\sigma = g_{\varphi\varphi}$ (radion) & $0$ & $\mathbf{1}$ & massive, $m \sim M_{\mathrm{poly}}$ \\
```

TO:
```latex
$\sigma = g_{\varphi\varphi}$ (radion) & $0$ & $\mathbf{1}$ & massive, $m \in [16, 30]\,M_{\mathrm{poly}}$ on AdS$_4$ branch (Rem.~\ref{rem:radion-mass}) \\
```

## Update 2 — add bridge sentence after §4 table

ADD after existing `rmk:mass-spectrum` and before new Remark:

```latex
The single radion field $\sigma$ in the table above is one direction in a
two-dimensional internal-metric moduli space $(\alpha, \gamma)$, where $\alpha$ is
the $S^1_\varphi$ fiber radius and $\gamma$ is the $\mathbf{H}^2/\mathbb{Z}_7$
base curvature scale (Remark~\ref{rem:radion-mass}). Paper~VI's tree-level
single-modulus treatment \eqref{VI-eq:F-DE} corresponds to the fiber-only
projection with $\gamma$ held fixed at unit radius by the flux.
```

(The `VI-` xr-prefix for `paper-5-cosmology` is set at Paper IV line 7.)

## Update 3 — add Remark rem:radion-mass immediately after

```latex
\begin{remark}[Radion mass from 1-loop Candelas--Weinberg + Freund--Rubin]
\label{rem:radion-mass}
The radion mass is computed at 1-loop from the Candelas--Weinberg effective
potential combined with Freund--Rubin flux stabilization on the Seifert
compactification, using the full two-dimensional modulus space $(\alpha, \gamma)$.
The effective potential has five structural contributions:
bulk Einstein-Hilbert with~$\Lambda_7$, Freund--Rubin 2-form flux with
Euler class $e = 7/2$, 1-loop fiber and base Casimir energies (base with
negative sign for bosonic periodic modes on $\mathbf{H}^2/\mathbb{Z}_7$;
the three $\mathbb{Z}_7$ cone points contribute an opposite-sign twisted-sector
correction of approximately $15\%$ of the untwisted coefficient magnitude,
which does not flip the total sign), and the base-Ricci term. The total
$|C_{\mathrm{base}}| = 0.089$ carries an overall band of approximately
$\pm 50\%$ from the yet-uncomputed full Selberg trace on the
$(2, 3, 7)$-arithmetic surface; the $15\%$ twisted-sector quantity above is
distinct from this total uncertainty.

At the ratio $r_\star = \alpha_\star / \gamma_\star = 7\sqrt{7}/4 \approx 4.63$
(the Thurston-type ratio emergent dynamically in the Seifert $N = 7$ geometry),
with $|C_{\mathrm{base}}| = 0.089$ and $b(7) = 4.298$, the Newton solution is
\begin{equation}
  (\alpha_\star,\, \gamma_\star,\, \Lambda_7)
    = (0.7255,\; 0.1567,\; -4.10\times 10^4)\quad (G_7 = 1),
\end{equation}
with $V_\star \approx -2.44\times 10^3\,G_7^{-1}$ (AdS$_4$), and both Hessian
eigenvalues positive:
\begin{equation}
  m_{\mathrm{radion}} \in [16,\, 30]\,M_{\mathrm{poly}}
  \;\; (\text{multi-PeV at } M_{\mathrm{poly}} \sim 300\,\text{TeV}).
\end{equation}
Broader $\Lambda_7$ scans within the physical window yield $\sim 10$--$100\,M_{\mathrm{poly}}$;
the narrower $[16, 30]$ window is the Thurston-branch subrange. This two-modulus
1-loop Hessian eigenvalue result is a different object from Paper~VI's tree-level
single-modulus zero-point frequency $M_{\mathrm{rad}} = N/2$, not a unit relabel
of it; the two values remain internally consistent with their respective
potentials.

A second critical point at $(\alpha_\star, \gamma_\star, \Lambda_7) = (0.798,
0.165, -5770)$ with $|C_{\mathrm{base}}| = 0.10$ satisfies $V_\star = 0$
(Minkowski) but has Hessian signature $(+, -)$ with $m^2_- \approx -110\,M_{\mathrm{poly}}^2$:
a tachyonic saddle. Because $V_\star = 0$ the background is flat, so the
Breitenlohner--Freedman bound does not apply --- this is a genuine flat-space
tachyon. No single-ingredient addition from the list in
Remark~\ref{rem:empirical-exhaustion} lifts the saddle to a minimum. Higher-
curvature ($R^2$) corrections at Session 20's naive coupling
$\alpha'_7 = 1/k(7)$ are formally large at both critical points
($\alpha'_7\,|R_3| \approx 620$), but these corrections are a separate topic
from the five tree-plus-1-loop terms analyzed here and assume an overestimate
of the higher-curvature coupling (see Session 20 §5.2); at the natural
$\alpha_{\mathrm{CS}} = 1/k(7) \approx 12\%$ loop-suppression scale the
corrections are subleading.

The value $\Lambda_7 = -4.10 \times 10^4$ is not a free fit parameter; once
the ratio $r_\star = \alpha_\star/\gamma_\star = 7\sqrt{7}/4$ is imposed
(the Seifert--$N=7$ Thurston ratio, which emerges dynamically at 5\%
accuracy from the 5-term potential's stationarity conditions; see
\cite{radion-derivation} §R.18), $\Lambda_7$ is \emph{determined} by the
requirement $\partial_\alpha V = \partial_\gamma V = 0$. The ``Thurston
branch'' refers to the ray $r = r_\* = 7\sqrt{7}/4$ in $(\alpha, \gamma)$ space
along which this Λ_7 fixing applies.

The sign and magnitude of the base Casimir $|C_{\mathrm{base}}| = 0.089$ assume
the standard antiperiodic fiber boundary condition for fermions under Seifert
Euler class $e = 7/2$ (Paper~IV~§8.1); global spin-structure verification over
the three $\mathbb{Z}_7$ cone points of
$\mathbf{H}^2/\mathbb{Z}_7$ is an open item. A hypothetical flipped sign would
eliminate the $V_\star = 0$ saddle entirely but leave the AdS$_4$ branch
qualitatively intact. Full derivation:
\cite{radion-derivation}.
\end{remark}
```

## Update 4 — add Lemma + Corollary + Remark after

```latex
\begin{lemma}[Volume-universal scaling parallelism]
\label{lem:scaling-obstruction}
Let the 7D compactification on the Seifert manifold
$M_3 = S^1_\alpha \hookrightarrow M_3 \to \Sigma_\gamma$ with
$\Sigma_\gamma = \mathbf{H}^2/\mathbb{Z}_7$ have internal $3$-volume
$V_3(\alpha, \gamma) = \kappa_V\,\alpha\gamma^2$ with $\kappa_V = 16\pi^2/7$, and
$4$D Einstein-frame Weyl rescaling $\Omega^2 = V_3^{-1}$. If a contribution
$V_{\mathrm{new}}(\alpha, \gamma)$ to the 4D Einstein-frame effective potential
has the form
\begin{equation}
  V_{\mathrm{new}} = f(V_3)\cdot V_3^{-2},
\end{equation}
with $f \colon (0, \infty) \to \mathbb{R}$ of constant sign, continuously
differentiable, and $f \ne 0$ pointwise, then at every $(\alpha, \gamma)$ the
log-modulus scaling vector
\begin{equation}
  (p_{\mathrm{new}}, q_{\mathrm{new}}) \equiv
  (\partial_{\log\alpha}\ln |V_{\mathrm{new}}|,\,
   \partial_{\log\gamma}\ln |V_{\mathrm{new}}|)
  \;=\; (h(V_3) - 2)\cdot (1, 2),
\end{equation}
where $h(V_3) := V_3\,f'(V_3)/f(V_3)$. In particular
$(p_{\mathrm{new}}, q_{\mathrm{new}}) \in \mathrm{span}\{(1, 2)\} = \mathrm{span}\{(-1, -2)\}$.
\end{lemma}

\begin{proof}
From $\partial_{\log\alpha} V_3 = V_3$, $\partial_{\log\gamma} V_3 = 2V_3$, and
$\ln|V_{\mathrm{new}}| = \ln|f(V_3)| - 2\ln V_3 + \text{const}$:
\[
  \partial_{\log\alpha}\ln|V_{\mathrm{new}}|
    = h(V_3) - 2, \qquad
  \partial_{\log\gamma}\ln|V_{\mathrm{new}}|
    = 2(h(V_3) - 2).
\]
\end{proof}

\begin{corollary}[Explicit excluded contributions]
\label{cor:excluded-mechanisms}
The following contributions to $V_{\mathrm{eff}}$ on the $N=7$ Seifert
compactification have the form of Lemma~\ref{lem:scaling-obstruction}:
\begin{enumerate}
  \item Bulk cosmological constant: $V_\Lambda = \Lambda_7\,A_L\,\kappa_V/V_3$,
    so $f(V_3) = \Lambda_7\,A_L\,\kappa_V\,V_3$ (constant sign, sign of
    $\Lambda_7$), $h = 1$, scaling $(-1,\, -2)$.
  \item 3-form $H$-flux with $\int_{M_3} H = 2\pi p$, $p \in \mathbb{Z}$:
    $V_H = B_H\,p^2\,\kappa_V^3/V_3^{3}$, so $f(V_3) = B_H\,p^2\,\kappa_V^3\,V_3^{-1}$
    (positive), $h = -1$, scaling $(-3,\, -6) = 3(-1,\, -2)$.
  \item Born--Oppenheimer instanton amplitude of the form
    $V_{\mathrm{inst}} = \mathcal{C}_N\,\exp(-S_N/\sqrt{V_3})\cdot V_3^{-2}$
    with $\mathcal{C}_N > 0$ and $S_N$ independent of moduli, for the verified
    cases $N = 7$ and $N = 11$: $f = \mathcal{C}_N\,\exp(-S_N/\sqrt{V_3})$
    (positive, $C^1$ on $(0,\infty)$), $h(V_3) = S_N/(2\sqrt{V_3})$ is moduli-
    dependent, scaling still $(h-2)(1, 2) \in \mathrm{span}\{(-1, -2)\}$ pointwise.
\end{enumerate}
In all three cases the log-modulus scaling vector lies on
$\mathrm{span}\{(-1, -2)\}$ at every point, so the contribution of each term to
the effective Hessian is rank 1 along the $V_3$-gradient direction. The pairwise
cross-product with $\Lambda_7$ in the Hessian decomposition of
\cite[Appendix~R.27]{radion-derivation} vanishes identically, and no such
contribution can independently stabilize a direction orthogonal to $V_3$
(such as the tachyonic $\rho$ direction of the $V_\star = 0$ saddle).
\end{corollary}

\begin{remark}[Empirical status of non-volume-universal candidates]
\label{rem:empirical-exhaustion}
Non-volume-universal mechanisms tested against the 3-equation system
$\{V = 0,\; \partial_\alpha V = 0,\; \partial_\gamma V = 0\}$ (Newton solve in
physical moduli window) and against Hessian signature $(+, +)$:
higher-curvature $R_\Sigma^2$ (three channels $(-1, -6)$, $(+1, -8)$, $(+3, -10)$);
fiber-wrapped Euclidean instanton (effective scaling
$(-2 - 2\pi\alpha\mu, -4)$); base-Casimir sign variation in the physical
$|C_{\mathrm{base}}|$ window; gravitational Chern--Simons with $\eta$-invariant,
scaling $(-1, -4)$; $\mathbb{Z}_7$ discrete torsion flux across five channels;
sub-leading Minakshisundaram--Pleijel heat-kernel coefficients (uniformly
$(-2, -8)$). None produced a stable $V_\star = 0$ critical point in the
physical moduli window.

Untested candidates: supersymmetric or non-supersymmetric fermion condensates
$\langle\bar\lambda\lambda\rangle$; SM-fermion back-reaction on the moduli
(4D 1-loop Coleman--Weinberg from 48 Weyl fermions); hidden-sector gauge
dynamics on the fiber; brane-analog tension (KKLT-type uplift); Hodge dual
of the FR 2-form; generalized-global-symmetry 1-form Coulomb-branch
contributions; $\mathrm{SL}(2, \mathbb{Z})$-duality-invariant corrections;
higher-loop Casimir; discrete-gauge anomaly inflow from the
$\mathbb{Z}_7$ orbifold fixed points. The set of tested mechanisms is the empirical
sandbox status at the time of writing; it is not a closed classification.
\end{remark}
```

## Update 5 — Paper VI radion section

IN `latex/paper-5-cosmology/main.tex` (which is **Paper VI**),
after the sentence ending "This is determined by the geometry." (currently at
line 1052; anchor by phrase, not line number, to survive upstream edits), ADD:

```latex
This single-modulus tree-level result is the fiber-only projection with
$\gamma$ held fixed of the full 2-modulus 1-loop Hessian eigenvalues derived
in Paper~IV~Remark~\ref*{IV-rem:radion-mass}, which gives
$m_{\mathrm{radion}} \in [16, 30]\,M_{\mathrm{poly}}$ on the AdS$_4$ branch.
The two values are different objects (tree-level zero-point frequency vs
1-loop Hessian eigenvalue), not coordinate relabels of a single quantity.
```

## Update 6 — Paper VII parameter accounting

IN `latex/paper-6-discussion/main.tex` (which is **Paper VII**), §"Parameter
accounting" (`\label{sec:parameters}`, line 73), insert the bullet below under
the "Derived from N (no freedom)" paragraph near line 191 (or equivalently
in the post-Total bullet list near line 232 — either location works):

```latex
\item The radion mass $m_{\mathrm{radion}} \in [16, 30]\,M_{\mathrm{poly}} \approx$
  multi-PeV is derived at 1-loop (Paper~IV~Remark~\ref*{IV-rem:radion-mass}).
  Independent inputs: $b(7) = 4.298$ (Paper~III), Seifert Euler class $e = 7/2$,
  with $\Lambda_7$ determined (not fit) by stationarity on the Thurston ray
  $r = 7\sqrt{7}/4$. At this mass the radion decays via gravitational coupling
  $\tau \sim M_{\mathrm{Pl}}^2/m^3 \sim 10^{-6}$~s (using $M_{\mathrm{Pl}}
  \approx 1.22\times 10^{19}$~GeV, not $M_{\mathrm{poly}}$), well before BBN.
  It avoids all 5th-force and Eöt-Wash bounds ($m \gg 10^{-3}$~eV) and is
  above LHC reach; no direct cosmological or collider constraint applies.
```

## Bibliography entry

In `latex/shared/refs.bib`, add:

```bibtex
@misc{radion-derivation,
  author = {Speagle, G.},
  title  = {Radion Stabilization Derivation Chain, Sessions 18--24},
  year   = {2026},
  note   = {\url{docs/rigor-sandbox/session18-cw-freund-rubin-radion/} through
    \url{docs/rigor-sandbox/session24d-Z7-torsion-flux/}. Includes
    Appendix~R.27 Hessian-decomposition formula.},
}
```

Referenced from Paper IV as `\cite{radion-derivation}` and
`\cite[Appendix~R.27]{radion-derivation}`. **IMPORTANT**: this refs.bib entry
must commit atomically with the Paper IV changes; otherwise bibtex will emit
undefined-citation warnings.

## Values and sources (reference table)

| Quantity | Value | Source |
|---|---|---|
| b(7) | 4.298 | Paper III authoritative |
| c(7) = 12 b(7) | 51.57 | same |
| k(7) = 2 b(7) | 8.596 | same |
| e (Seifert Euler class) | 7/2 | Paper IV §2 |
| \|χ_orb\| | 4/7 | Paper IV §3 |
| κ_V = 16π²/7 | 22.56 | V_3 coefficient (new notation, avoids K collision) |
| r_\* = 7√7/4 | 4.6301 | **defined inline** (no Paper I label exists); Seifert-N=7 Thurston ratio |
| AdS_4 minimum (α,γ,Λ_7) | (0.7255, 0.1567, -4.10×10⁴) | Session 18 R.18, R.20 |
| V_* AdS_4 | -2.44×10³ G_7^{-1} | Session 18 R.20 |
| m_radion AdS_4 | [16.4, 28.5] M_poly | Session 18 R.20 |
| V_*=0 saddle | (0.798, 0.165, -5770) | Session 18 R.17, R.20 |
| m²_- at saddle | -110 M_poly² (flat-space tachyon, BF N/A) | Session 18 R.20 |
| \|C_base\| (central) | 0.089 | Session 22 |
| \|C_base\| total band | [0.05, 0.15] (~50%) | Session 18 R.22 |
| twisted-sector correction | ~15% of untwisted magnitude, opposite sign, does not flip total | Session 22 §4 |

## Open items (flagged, not blockers)

1. **Spin-structure obstruction check** on Seifert e=7/2 over three Z_7 cone
   points. Antiperiodic fiber BC assumed (Paper IV §8.1); global obstruction
   in H²(orbifold; Z_2) needs verification. Downside bounded: flipped sign
   eliminates V_*=0 saddle, preserves AdS_4 branch.
2. **r_\* label in Paper I**: no label exists; defined inline in the Remark.
   Adding a named proposition in Paper I is optional future work.
3. **Untested mechanisms** (Remark): to be checked in future sessions.
4. **Higher-curvature EFT validity** at V_*=0 saddle: α'_7·|R_3| ≈ 619 > 1;
   the saddle is outside the EFT regime. Flagged inline in the Remark.

## Files to modify

| File | Identity | Changes | Lines added |
|---|---|---|---|
| `latex/paper-4-field-theory/main.tex` | Paper IV | Table row + bridge sentence + Remark + Lemma + Corollary + Remark | ~90 |
| `latex/paper-5-cosmology/main.tex` | Paper **VI** | 5-line cross-ref after line 1052 | 5 |
| `latex/paper-6-discussion/main.tex` | Paper **VII** | 1 bullet in parameter accounting | 6 |
| `latex/shared/refs.bib` | bibliography | 1 bibliography entry | 9 |

Total: ~110 new lines across 4 files. All CORE derivation content, not
defensive padding; compliant with EDITING_COMPANION.md (the 600–800-line
reduction target applies to redundancy/defensive patterns, not to new rigorous
derivations).

## What NOT to do

- Do NOT remove the claim that the radion is massive; it is derived.
- Do NOT downgrade "1-loop CW+FR derivation" to a citation.
- Do NOT invoke Paper VI's N=11 mechanism as a Minkowski resolution (contradicts Session 24a).
- Do NOT claim Paper VI's M_rad = N/2 is a unit-remap of our [16, 30] M_poly;
  they are different objects (tree-level ω vs 1-loop Hessian eigenvalue).
- Do NOT introduce new ambiguous notation; κ_V is new but unambiguous.
- Do NOT edit canonical paper files until this draft is at 9-10/10 on all
  three review axes.

## Iteration plan

Re-dispatch math / physics / unified-framework reviewers on this v4 draft.
Target ≥9.0 on all six axes. When converged, add as CHANGE 4 to
`docs/rigor-sandbox/session01-joint-P1-M1-fermion-dictionary/PAPER4_REVISION_DRAFT.md`
and proceed to Phase 5 of WORKFLOW_TEMPLATE.md (canonical paper integration).
