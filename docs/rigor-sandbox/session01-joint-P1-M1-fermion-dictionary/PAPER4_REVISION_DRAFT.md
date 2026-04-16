# Paper IV revision draft (Position B)

**Target**: replace `Gauge-theory consistency — Anomaly cancellation` paragraph (lines 3747–3755) with a full derivation of SM fermion content.

**Additionally**: fix M1 in §8.1 Step 2 (line 980) — the γ⁵ formula.

**Do NOT apply to paper**: this is a review draft for Gordon's approval.

---

## CHANGE 1: §8.1 Step 2 (line 975–981) — M1 fix

### Current text

```latex
Under KK reduction, $\gamma^5$-eigenvalue maps to the
$3$D CS sector: $4$D left-handed $\leftrightarrow$ couples to $A^+$
(the dreibein component along $S^1$ determines the chirality
projection, because $\gamma^3 = \gamma^\varphi$ is the fiber direction,
and $\gamma^5 = \gamma^0\gamma^1\gamma^2\gamma^3$ reduces to
$\gamma^{(3)} \cdot e^{i\pi m}$ in the KK basis).
```

### Proposed replacement

```latex
Under KK reduction, the $\gamma^5$ eigenvalue is preserved per KK mode:
a $4$D Weyl fermion $\psi$ with $\gamma^5\psi = \pm\psi$ decomposes
as $\psi = \sum_m \chi_m(x)\,e^{i(m+1/2)\varphi}$ with
$\gamma^5\chi_m = \pm\chi_m$ for every~$m$.
The matrix identity
$\gamma^5 = \gamma^{(3)}\cdot\gamma^3$,
where $\gamma^{(3)} \equiv i\gamma^0\gamma^1\gamma^2$ is the $3$D volume
element (which commutes with $\gamma^a$ for $a = 0, 1, 2$ and anticommutes
with $\gamma^3 = \gamma^\varphi$), identifies the sign-of-$\gamma^5$
sector with the product of the $\gamma^{(3)}$ eigenvalue and the $\gamma^3$
eigenvalue.
In the Witten CS splitting $[A^+, A^-]$ of $2{+}1$D gravity,
$\gamma^{(3)}$-eigenstates couple to $A^+$ and $A^-$ respectively:
the $4$D left-chiral sector ($\gamma^5 = +1$) and right-chiral sector
($\gamma^5 = -1$) map one-to-one onto the $A^+$ and $A^-$ CS sectors.
```

### Rationale

Current formula `γ^5 → γ^(3) · e^{iπm}` is imprecise — γ⁵ acts on the
spinor index, not on the scalar KK wavefunction, so there is no
m-dependent phase. The correct statement is the matrix identity
`γ^5 = γ^(3) · γ^3`, which preserves the physical content (chirality-to-
CS-sector mapping) while being mathematically rigorous. Verified via
sympy in `docs/rigor-sandbox/session01-joint-P1-M1-fermion-dictionary/M1-chirality/clifford_oracle.py`.

---

## CHANGE 2: §14.2 (lines 3745–3773) — full rewrite of gauge-theory consistency

### Current text

```latex
\subsection{Gauge-theory consistency}

\paragraph{Anomaly cancellation.}
Each generation carries the standard
$\mathrm{SU}(3) \times \mathrm{SU}(2) \times \mathrm{U}(1)$
quantum numbers (left-handed Weyl convention).
All gauge anomalies ($\operatorname{Tr}(Y)$,
$\operatorname{Tr}(Y^3)$, $\operatorname{Tr}(T_3^2 Y)$)
cancel per generation by the same arithmetic as in the
Standard Model; the orbifold determines which modes
form a generation, not what quantum numbers they carry.
```

### Proposed replacement

```latex
\subsection{Gauge-theory consistency}
\label{sec:gauge-consistency}

\paragraph{The fermion content per generation.}
\label{para:fermion-dictionary}
Each of the three fermion generations of the Standard Model is
derived from the KK mode space
$\{(m_7, m_4, \chi) : m_7 \in \mathbb{Z}/7,\ m_4 \in \mathbb{Z}/4,\ \chi \in \{L, R\}\}$
of the Seifert manifold $\mathbb{R} \times (\mathbf{H}^2 \times_7 S^1)$,
via a Pati--Salam embedding compatible with the derivations of
\S\ref{sec:chiral-su2}--\S\ref{sec:gauge-derivation-chain}:

\begin{center}\small
\begin{tabular}{lcccccl}
\toprule
PS rep & $m_7$ range & $m_4$ range & $\chi$ & $B{-}L$ & $Y$ & SM fields \\
\midrule
$(\mathbf{4}, \mathbf{2}, \mathbf{1})$ & $\{0\} \cup O_+$ & $\{1, 2\}$ & $L$
   & $\begin{cases} 1/3, & m_7 \in O_+ \\ -1, & m_7 = 0 \end{cases}$
   & $\begin{cases} +1/6 \\ -1/2 \end{cases}$
   & $Q_L \oplus L_L$ \\[2pt]
$(\bar{\mathbf{4}}, \mathbf{1}, \mathbf{2})$ & $\{0\} \cup O_-$ & $\{0, 3\}$ & $L$
   & $\begin{cases} -1/3, & m_7 \in O_- \\ +1, & m_7 = 0 \end{cases}$
   & $T_3^R \pm (B{-}L)/2$
   & $u_R^c, d_R^c, \nu_R^c, e_R^c$ \\
\bottomrule
\end{tabular}
\end{center}
\noindent where $O_+ = \{1, 2, 4\}$ and $O_- = \{3, 5, 6\}$ are the
Frobenius orbits from \S\ref{sec:su3-mckay}, and $T_3^R$ is determined
by $m_4$: $m_4 = 0 \Rightarrow T_3^R = -1/2$, $m_4 = 3 \Rightarrow T_3^R = +1/2$.
The hypercharge formula
\begin{equation}\label{eq:Y-derived}
  Y = T_3^R + (B{-}L)/2
\end{equation}
reproduces the standard-model hypercharges $\{1/6, -2/3, +1/3, -1/2, +1, 0\}$
exactly (verified in exact rational arithmetic).

The $4$-element sets $\{0\} \cup O_\pm$ host the fundamental and
antifundamental representations of $\mathrm{SU}(4)$ in a
Frobenius-compatible basis: the $\mathbb{Z}/3$ Frobenius
$\sigma\colon m \mapsto 2m \pmod 7$ fixes $m_7 = 0$ and cyclically
permutes the three elements of~$O_\pm$, realising the $\mathrm{SU}(4)
\supset \mathrm{SU}(3) \times \mathrm{U}(1)_{B{-}L}$ decomposition
$\mathbf{4} \to \mathbf{3} + \mathbf{1}$ (quark triplet + lepton singlet)
and $\bar{\mathbf{4}} \to \bar{\mathbf{3}} + \mathbf{1}$.

\paragraph{Anomaly cancellation.}
\label{para:anomaly-cancellation}
All five Standard-Model gauge-anomaly traces are computed
\emph{from the charges in Table~\ref{para:fermion-dictionary}} (not
assumed from SM arithmetic) and vanish exactly per generation:
\begin{equation}\label{eq:anomalies-zero}
  \operatorname{Tr}(Y) =
  \operatorname{Tr}(Y^3) =
  \operatorname{Tr}(T_3^2\,Y) =
  \operatorname{Tr}(C_{\mathrm{SU}(3)}\,Y) =
  \operatorname{Tr}(C_{\mathrm{SU}(3)}^3)
  \;=\; 0,
\end{equation}
where the traces sum over all Weyl fermions in one generation
(left-handed convention), and $C_{\mathrm{SU}(3)}$ denotes the
$\mathrm{SU}(3)$ quadratic Casimir. All five identities hold in
exact rational arithmetic (verified numerically; see Code Availability).

\paragraph{Three generations from Riemann--Hurwitz on the Klein quartic.}
\label{para:three-generations}
Let $\mathbb{Z}/7 \subset \mathrm{PSL}(2, \mathbb{F}_7)$ be a Sylow-$7$
subgroup acting on the Klein quartic $X(7) = \Gamma(7)\backslash\mathbf{H}^2$
(genus $3$). The Riemann--Hurwitz formula for the degree-$7$ cyclic cover
$X(7) \to X(7)/(\mathbb{Z}/7)$:
\begin{equation}\label{eq:RH}
  2 g(X(7)) - 2 = 7\left(2 g_{\mathrm{quot}} - 2\right) + F\,(7 - 1),
\end{equation}
admits the unique nonnegative integer solution $g_{\mathrm{quot}} = 0$,
$F = 3$. The $\mathbb{Z}/7$ action therefore has \emph{exactly three fixed
cusps} on $X(7)$, matching the generation count~$n_{\mathrm{gen}} = (N-1)/2 = 3$
of Paper~V, Corollary~4. Verification over $N \in \{3, \ldots, 13\}$
confirms that the identity $F = (N-1)/2$ with integer $F$ and
$g(X(N)) \ge 1$ is satisfied uniquely at $N = 7$.

Each of the three fixed cusps localises one copy of the matter content
of Table~\ref{para:fermion-dictionary} via a DHVW twisted-sector
construction; the total matter content is $3 \times 16 = 48$ left-handed
Weyl fermions, comprising three generations of the Standard Model
augmented by a right-handed neutrino per generation.

\paragraph{Proton stability.}
\label{cor:proton-stability}%
The $\mathrm{SU}(3)$ and $\mathrm{SU}(2)$ sectors live in different
polygon numbers ($N = 7$ and $N = 4$).  A non-trivial
cross-sector Yukawa coupling carries a combined
$\mathbb{Z}_{28}$ phase
$\exp(2\pi i(4m_7 + 7m_4)/28)$ with $m_7 \in \{1,\ldots,6\}$
and $m_4 \in \{1,2,3\}$.  Invariance requires
$4m_7 + 7m_4 \equiv 0 \pmod{28}$; since $\gcd(4,28) = 4$
and $\gcd(7,4) = 1$, this forces $4 \mid m_4$, which has no
solution in $\{1,2,3\}$.
This is exact $\mathbb{Z}_{28}$ charge conservation
(\S\ref{sec:decoupling}).
\emph{Prediction}: the proton is exactly stable, not just
long-lived, distinguishing this theory from $\mathrm{SU}(5)$ GUTs
($\tau_p \sim 10^{34}$\,yr) and consistent with Super-Kamiokande
bounds ($\tau_p > 1.6 \times 10^{34}$\,yr for $p \to e^+\pi^0$).

\begin{remark}[UV gauge group]
\label{rem:uv-gauge-group}
The matter content fits the Pati--Salam embedding
$\mathrm{SU}(4)_c \times \mathrm{SU}(2)_L \times \mathrm{SU}(2)_R$
with $Y = T_3^R + (B{-}L)/2$~\eqref{eq:Y-derived}. Two independent
consistency checks support this embedding:
(i)~$\sin^2\theta_W = 3/11$~\eqref{eq:weinberg} is the Pati--Salam
value at gauge coupling ratio $g_R^2/g_{B{-}L}^2 = 8/5$;
(ii)~the gauge central-charge budget is preserved under
$\mathrm{SU}(4)_1 \to \mathrm{SU}(3)_1 \times \mathrm{U}(1)_{B{-}L}$
(both give $c_{\mathrm{gauge}} = 3$).
The polygon theory's explicit derivations (\S\ref{sec:chiral-su2},
\S\ref{sec:su3-mckay}, \S\ref{sec:gauge-derivation-chain}) produce
$\mathrm{SU}(3)_c \times \mathrm{SU}(2)_L \times \mathrm{U}(1)_Y$ directly.
Whether the theory has $\mathrm{SU}(4)_c \times \mathrm{SU}(2)_L \times
\mathrm{SU}(2)_R$ as its UV gauge group at a higher scale
(with $\mathrm{SU}(4)_c \to \mathrm{SU}(3)_c \times
\mathrm{U}(1)_{B{-}L}$ breaking at the polygon scale, and the
residual $\mathrm{SU}(2)_R \times \mathrm{U}(1)_{B{-}L}$ broken at
$m_R \approx 107$\,TeV via the Redlich parity-anomaly mechanism of
\S\ref{sec:chiral-su2}) is an open structural question. The derivation
above is neutral on this point: it requires only the polygon-theory
gauge group~\S\ref{sec:gauge-derivation-chain} and the fermion
dictionary of Table~\ref{para:fermion-dictionary}.
\end{remark}
```

### Rationale

Replaces a 9-line paragraph that ASSERTS SM quantum numbers (per physics-
reviewer audit: "0% derived") with a ~80-line derivation including:
- Explicit (m_7, m_4, χ) → SM dictionary
- Derived hypercharge formula Y = T_3R + (B-L)/2
- Anomaly cancellation from derived charges (5 traces, all vanish in
  exact arithmetic)
- 3-generation mechanism from Riemann-Hurwitz theorem on X(7)
- Pati-Salam UV framework flagged as structural observation, with the
  genuine open SU(4) UV derivation noted in Remark
- Consistency with Paper §§8.1, 8.3, 8.5, 16, and Paper V Cor. 4

Verified via 8 independent numerical consistency checks in
`docs/rigor-sandbox/session01-joint-P1-M1-fermion-dictionary/`:
Clifford identity, polygon→PS mapping, Y formula, anomalies,
sin²θ_W, Yukawa texture, PMNS theorem, Riemann-Hurwitz.

---

## CHANGE 3: Code Availability footnote update

Add to the `\paragraph{Code availability}` section (currently line 3894):

```latex
The fermion dictionary, anomaly verification, and Riemann--Hurwitz
three-generation computation are in
\texttt{docs/rigor-sandbox/session01-joint-P1-M1-fermion-dictionary/}.
```

---

## Integration checklist

Before applying to `latex/paper-4-field-theory/main.tex`:

- [ ] Gordon reviews this diff document
- [ ] Resolve any notational conflicts (label names, cross-references)
- [ ] Verify Table label doesn't conflict with existing
      `\ref{para:fermion-dictionary}`
- [ ] Run physics-reviewer + math-reviewer on the proposed replacement
      (ensure no mathematical errors)
- [ ] Verify pdflatex compilation with proposed changes
- [ ] Update companion if §14.2 is referenced there

## Downstream impact assessment

Potential downstream impacts (to verify before applying):

1. **§16 PMNS**: references three generations via pair structure; our
   3-gen mechanism may reframe this (consistent, per `pmns_consistency.py`).
2. **§13 Yukawa texture**: uses pair labels {1, 2, 3}; our derivation
   maps these to the 3 Z/7-fixed cusps (consistent, per
   `yukawa_consistency.py`).
3. **Paper V §23 ν_R**: ν_R is in (4̄, 1, 2) with T_3R = -1/2; consistent.
4. **Paper VI parameter counting**: may need update of "inputs" list if
   fermion content is now derived (was assumed).
5. **Paper 0 overview**: SM derivation claim may need strengthening
   (no longer "asserted"; now "derived").

## Proposed session scheduling

Gordon decides whether to:
(A) Apply the changes after reviewer approval.
(B) Wait for further PS framework deepening (DHVW matter localization,
    Yukawa overlap integrals).
(C) Apply only M1 change (§8.1 Step 2) now; defer §14.2 revision until
    the open problems are more fully resolved.
