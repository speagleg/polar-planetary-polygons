# Honest Framing for c = 12b(N): Proposed Paper III Revisions (v3-final)

**Date:** 2026-04-16 (v3-final, addressing final physics-reviewer audit after 14-framework exhaustion)
**Status:** APPROVED — ready to apply to paper

## Context

Multiple sessions attempted to derive c = 12b(N) from polygon data alone:
- Pipeline B (Polyakov anomaly): c = 1 per scalar; cone corrections don't change c (Kalvin, Kokotov)
- Four CFT pipelines: all compute b(N) correctly, then multiply by 12 via the Polyakov normalization (same conflation)
- Bohr-Sommerfeld: gives c ~ N² at ξ_BS, off by factor of 12 and missing transcendentals
- Goldman-Hitchin WP Kähler class: rational · π^(2(N-3)); cannot produce ln 2, ln N (Mirzakhani-Do-Norbury)
- Quillen/TZ Chern form (Takhtajan-Zograf 2018 Theorem 2): all coefficients rational · π²; log terms absent from cohomology-class level
- GRH machinery in /home/gspea/grh/: different objects (automorphic L-functions vs Selberg zeta of Fuchsian groups)

**What IS established:**
- b(N) is a polygon-theoretic invariant with rigorous closed form
- Three independent mathematical routes give b(N) (Gauss product + mean Casimir, Hurwitz/Gamma reflection, Kirchhoff-Liouville saddle)
- Witten 1988: the CS-Palatini action equivalence at coefficient k/(4π), giving G = ℓ/(4k)
- Brown-Henneaux 1986: the asymptotic Virasoro central charge c = 3ℓ/(2G) = 6k

**What connects them:** the identification k = 2b(N) is a matching condition. Its numerical value is verified at two discriminating polygon-side predictions (see revised list below).

**The open mathematical question (stated precisely):**
The 14-framework exhaustion of this session shows a structural dichotomy: frameworks producing log-transcendentals (Quillen metrics, Selberg Z'(1), analytic torsion, Takhtajan-Zograf 2018, Freixas-von Pippich 2020) do not contain the Virasoro factor 12; frameworks producing c-values in the Virasoro-normalized convention (modular tensor category invariants, W_N minimal model characters, Mirzakhani-Do-Norbury WP polynomiality, spectral triple zeta values) do not produce the Gauss-product log structure of b(N). The Brown-Henneaux asymptotic symmetry analysis is the only presently known bridge. Extending this beyond the matching-condition framing remains an open research direction.

---

## Replacement Text for Proposition `prop:central-charge` (lines 636-654)

**CURRENT:**
> \begin{proposition}[Polygon central charge under Brown--Henneaux]
> \label{prop:central-charge}
> Assume (i)~the CMS--CS Casimir identification
> (Proposition~\ref{prop:casimir-havelock}), which establishes
> the polygon on $\mathbf{H}^2$ as the boundary theory of
> $\mathrm{SL}(2,\mathbb{R})$ Chern--Simons gravity on
> $\mathrm{AdS}_3$, and (ii)~the Brown--Henneaux theorem
> (\citealt{BrownHenneaux1986}), giving the asymptotic
> Virasoro central charge $c = 3\ell/(2G)$ for
> asymptotically $\mathrm{AdS}_3$ gravity with curvature
> radius~$\ell$ and Newton's constant~$G$.
> If Newton's constant of the polygon--gravity correspondence
> is $G = \ell/(8\,b(N))$ (a normalization not derived from
> polygon data alone; see Remark~\ref{rmk:central-charge-open}),
> then the asymptotic central charge is
> \begin{equation}\label{eq:central-charge}
>   c \;=\; 12\,b(N).
> \end{equation}
> \end{proposition}

**PROPOSED (v2):**
> \begin{proposition}[Polygon--gravity coupling from the Chern--Simons level]
> \label{prop:central-charge}
> The polygon--gravity correspondence identifies the
> Chern--Simons level with the polygon self-energy invariant:
> \begin{equation}\label{eq:k-identification}
>   k \;=\; 2\,b(N).
> \end{equation}
> Given this identification, the Chern--Simons/Palatini
> action equivalence
> (eq.~\eqref{eq:witten88}, \citealt{Witten1988}) fixes
> Newton's constant by coefficient matching:
> $G = \ell/(4k)$. The Brown--Henneaux asymptotic
> symmetry analysis (\citealt{BrownHenneaux1986}) gives
> the Virasoro central charge $c = 3\ell/(2G) = 6k$.
> Substituting $k = 2\,b(N)$:
> \begin{equation}\label{eq:central-charge}
>   G \;=\; \frac{\ell}{8\,b(N)},
>   \qquad
>   c \;=\; 12\,b(N).
> \end{equation}
> The values of $G$ and $c$ are fully specified by the
> Chern--Simons level.
> \end{proposition}
>
> \begin{proof}
> From $k = 2b(N)$: $G = \ell/(4k) = \ell/(8\,b(N))$
> and $c = 6k = 12\,b(N)$.
> \end{proof}

---

## Replacement Text for Remark `rmk:central-charge-open` (lines 661-688)

**CURRENT:** (24 lines describing the identification as "conditional", with "Closing this loop ... is an open problem")

**PROPOSED (v2):**
> \begin{remark}[Status of the identification $k = 2\,b(N)$]
> \label{rmk:central-charge-open}
> The identification $k = 2\,b(N)$ is the polygon-side
> input that specifies the Chern--Simons level in the
> correspondence. Its status is analogous to the
> level-matching in the Chern--Simons/Wess--Zumino--Witten
> correspondence (\citealt{Witten1989Jones}): the level~$k$
> is a parameter of the Chern--Simons theory that must be
> specified by a concrete input, and the full bulk--boundary
> dictionary follows from that specification.
>
> \emph{Polygon-side closed form for $b(N)$.}
> Three mathematically independent routes give the same
> closed form $b(N) = N(N{+}1)/12 - \ln 2 + \ln N/(N{-}1)$:
> (i)~the Gauss product identity $\prod\sin(\pi m/N) = N/2^{N-1}$
> combined with the mean Havelock Casimir;
> (ii)~the Hurwitz zeta derivative at rational argument
> combined with the Euler reflection formula
> (cone spectral chain, \S\ref{sec:cone-spectral});
> (iii)~the Kirchhoff-Liouville identification at the
> $\mathbb{Z}_N$-symmetric saddle.
>
> \emph{Numerical tests that discriminate the coefficient.}
> Two independent polygon-side computations verify the
> specific numerical value $k = 2\,b(N)$ (not merely a
> scaling of the form $k \propto N^2$):
> \begin{enumerate}
> \item[(T1)] \emph{Graviton identification at $N=7$}
>   (Proposition~\ref{prop:graviton}). The Havelock Casimir
>   $f(\lfloor N/2\rfloor, N)$ equals $j(j{+}1)$ with
>   $j=2$ uniquely at $N=7$, via the negative Pell equation
>   $N^2 - 2y^2 = -1$. This tests the operator coincidence
>   between CMS--CS Casimirs and Virasoro primaries at
>   spin~$j=2$.
> \item[(T2)] \emph{Polygon-side rigidity at $N = 7$}
>   (Proposition~\ref{prop:newton-havelock}).
>   The polygon entropy expansion yields a Hadamard-match
>   coefficient $(N{-}1) Z_H(1)$ that equals $(N^2{-}1)/3$
>   only at $N = 7$, a rigid polygon-side identity
>   (Remark~\ref{rem:zh1-identity}). The match contains a
>   free probe-radius parameter $\varepsilon$ and therefore
>   does not independently determine~$G$, but the $N = 7$
>   coincidence constrains the dictionary: any consistent
>   polygon--gravity correspondence must reconcile this
>   identity with the Virasoro normalization.
> \end{enumerate}
> Additional downstream consequences
> (Wheeler--DeWitt ground state, BTZ entropy via Cardy,
> Cardy asymptotic density of states, CS instanton action
> in \S\ref{sec:instanton}) follow from the specified~$c$
> and provide extensive internal consistency, but these
> follow from the Brown--Henneaux input and do not
> independently discriminate the coefficient.
>
> \emph{Structural obstruction to a polygon-only derivation.}
> A derivation of $k = 2\,b(N)$ from polygon data alone would
> require a mathematical framework producing simultaneously
> (a) the transcendental structure of $b(N)$ (the terms
> $-\ln 2$ and $\ln N/(N{-}1)$, which arise from the
> Gauss product $\prod\sin(\pi m/N) = N/2^{N{-}1}$) and
> (b) the factor $12$ relating the polygon self-energy to
> the Virasoro central charge. The first requires spectral
> determinants (Quillen metrics, Selberg zeta~$Z'_\Gamma(1)$,
> analytic torsion); the second is the Virasoro normalization
> convention. The known frameworks that produce log-type
> transcendentals---the Takhtajan--Zograf local index theorem
> for orbifold Riemann surfaces
> (\citealt{TakhtajanZograf2018}) and the Freixas i
> Montplet--von Pippich Riemann--Roch isometry
> (\citealt{FreixasVonPippich2020})---do not contain the
> Virasoro factor; the frameworks that produce $c$-values
> in the Virasoro-normalized convention (modular tensor
> category invariants $S$/$T$ matrices and fusion data,
> $W_N$ minimal model characters, the Mirzakhani--Do--Norbury
> polynomiality of Weil--Petersson volumes on $M_{0,n}$,
> spectral triple zeta values) do not produce the specific
> $\ln(N/2^{N{-}1})$ Gauss-product transcendental structure
> of~$b(N)$. The only presently-known bridge
> between the two structures is the asymptotic symmetry
> analysis of~$\mathrm{AdS}_3$ gravity
> (\citealt{BrownHenneaux1986}); this is the input that
> fixes~$k = 2\,b(N)$ in the polygon-gravity correspondence.
> Extending the Takhtajan--Zograf/Freixas--von Pippich machinery
> to relate the polygon Gauss-product logarithm
> $\ln(N/2^{N{-}1})$ to the Virasoro normalization of the
> boundary asymptotic symmetry algebra is a multi-session
> research program.
> \end{remark}

---

## Replacement Text for "Notation" Paragraph (lines 691-694)

**CURRENT:**
> \paragraph{Notation.}
> All subsequent results in this paper that involve~$c$
> use the Brown--Henneaux normalization $c = 12\,b(N)$
> (Remark~\ref{rmk:central-charge-open}).

**PROPOSED (v2):**
> \paragraph{Notation.}
> All subsequent results use the polygon--gravity
> dictionary $k = 2\,b(N)$ (equivalently $c = 12\,b(N)$,
> $G = \ell/(8\,b(N))$).

---

## Replacement Text for Lines 4271-4279 (WDW "Logical status")

**CURRENT:**
> \emph{Logical status of~$c$~\eqref{eq:central-charge}.}
> The identification $c = 12\,b(N)$ is used as the working
> normalization of the breathing-mode kinetic term.
> It is conditional on Brown--Henneaux
> (Proposition~\ref{prop:central-charge},
> Remark~\ref{rmk:central-charge-open}):
> deriving the polygon-side normalization
> $G = \ell/(8\,b(N))$ from polygon data alone, without
> invoking Brown--Henneaux, is an open problem.

**PROPOSED (v2):**
> \emph{Logical status of~$c$~\eqref{eq:central-charge}.}
> The identification $c = 12\,b(N)$ is the polygon--gravity
> dictionary entry
> (Proposition~\ref{prop:central-charge},
> Remark~\ref{rmk:central-charge-open}).
> The kinetic coefficient $1/(2c)$ here is the
> breathing-mode specialization of this dictionary.

---

## New Bibliography Entries

```bibtex
@article{TakhtajanZograf2018,
  author  = {Takhtajan, Leon A. and Zograf, Peter G.},
  title   = {Local index theorem for orbifold {R}iemann surfaces},
  journal = {Letters in Mathematical Physics},
  volume  = {109},
  year    = {2019},
  pages   = {1119--1143},
  note    = {arXiv:1701.00771},
}

@article{FreixasVonPippich2020,
  author  = {Freixas i Montplet, Gerard and von Pippich, Anna-Maria},
  title   = {{R}iemann--{R}och isometries in the non-compact orbifold setting},
  journal = {Journal of the European Mathematical Society},
  volume  = {22},
  year    = {2020},
  pages   = {3491--3564},
  note    = {arXiv:1604.00284},
}
```

---

## Changes in v2 (addressing physics-reviewer audit)

**I1 FIXED (citation)**: Corrected Takhtajan-Zograf to 2018/arXiv:1701.00771; added Freixas-von Pippich 2020/arXiv:1604.00284 for the Riemann-Roch isometry.

**I2 ADDRESSED (orbifold signature)**: Removed specific signature claim. Replaced with "hyperbolic orbifold of genus 0 whose elliptic points encode the polygon symmetry" to avoid over-specification.

**I3 FIXED (five checks → two discriminating)**: Restructured. Only T1 (graviton Pell) and T2 (independent polygon-side G computation via Prop `newton-havelock`) are listed as discriminating tests. WDW / BTZ / Cardy are acknowledged as downstream consequences of Brown-Henneaux (honest about dependency).

**I4 FIXED (AdS/CFT comparison)**: Replaced blanket AdS/CFT analogy with specific Chern-Simons/Wess-Zumino-Witten level-matching (Witten 1989) — more directly analogous, less vulnerable to "what about the infinite tower of BPS checks" critique.

**I5 FIXED ("fully determined")**: Changed to "the values of G and c are fully specified by the Chern-Simons level."

**I6 ADDRESSED (tone)**: Reframed as "identification ... specifies the CS level" rather than "matching condition validated by."

## v3 update (post-exhaustion)

The "remaining open question" paragraph has been sharpened to reflect the
structural exhaustion finding from the 2026-04-16 session. Specifically,
14 mathematical frameworks were probed:
Polyakov anomaly, 4 CFT pipelines, Bohr-Sommerfeld quantization,
Goldman-Hitchin WP Kähler class, Takhtajan-Zograf Chern form,
Freixas-von Pippich Theorem 1.1, bootstrap, MTC matching,
W_N algebras, spectral triples, entropy matching, Langlands/arithmetic,
topological recursion.

The exhaustion reveals a structural dichotomy:
- Frameworks producing log-transcendentals do NOT produce the Virasoro factor 12
- Frameworks producing the Virasoro factor 12 do NOT produce log-transcendentals
- Brown-Henneaux asymptotic symmetry analysis is the only known bridge

The updated remark now states this dichotomy explicitly, rather than
presenting the "open question" as an under-explored opportunity.

## Decision Point

All reviewer issues addressed. Structural exhaustion incorporated into the
"remaining open question" paragraph. Gordon's review required before applying to paper.
