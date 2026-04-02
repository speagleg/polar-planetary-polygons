# Cosmological Structure Integration Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate uniqueness-of-initial-conditions and entropy-bridge results into Papers III, V, and VI, with mathematical proofs where needed.

**Architecture:** Six targeted LaTeX insertions across three papers. Paper III gets the technical results (uniqueness remark, entropy bridge remark). Paper V gets the cosmological consequences (new §9). Paper VI gets predictions and framing (binary test, null predictions, discussion paragraph).

**Tech Stack:** LaTeX, existing paper cross-reference infrastructure

---

### Task 1: Paper III — Uniqueness of the WDW wave function (Remark after line 2341)

**Files:**
- Modify: `latex/paper-3-gravity/main.tex:2341` (after algebraic field remark, before §three-layer)

- [ ] **Step 1: Insert uniqueness remark with Weyl classification proof**

Insert after line 2341 (after "...not a perturbative artefact)."), before the paragraph starting "The palindromic threshold...":

```latex
\begin{remark}[Uniqueness of the WDW wave function]
\label{rmk:wdw-uniqueness}
The WDW equation~\eqref{eq:wdw} on $\rho \in (0,\infty)$ has two
singular endpoints.  Their Weyl classification determines whether
boundary conditions are needed:
\begin{enumerate}
\item \emph{At $\rho = 0$: limit-circle.}
  The potential $V(\rho) = \log(2\sinh\rho) + b(N) - f(m^*,N) \to
  \log(2\rho) + \mathrm{const}$ as $\rho \to 0$.
  Weyl's criterion (integral test): $\int_0^\varepsilon \rho\,|2c\,V(\rho)|\,d\rho
  < \infty$ because $\rho\,|\!\log\rho|$ is integrable.
  Both linearly independent solutions are $L^2$ near the origin;
  a boundary condition is required.
\item \emph{At $\rho \to \infty$: limit-point.}
  $V(\rho) \to \rho + \mathrm{const}$ (linear growth), so
  $\int^\infty \rho\cdot 2c\rho\,d\rho = \infty$.
  Only the Airy-decaying solution is $L^2$;
  no boundary condition is needed.
\end{enumerate}
The operator therefore requires exactly one boundary condition
(at $\rho = 0$).  The Born--Oppenheimer structure supplies it:
the CMS integrability of the angular sector
(Proposition~\ref{prop:orbifold-havelock}) makes the adiabatic
separation \emph{exact}, and the angular modes in their ground
state at each~$\rho$ select the ground state of the effective
Hamiltonian.  This ground state is non-degenerate: numerically,
the spectral gap $\Delta E \approx 0.84$ is stable across
$N = 7$--$15$ (see Code Availability).
The wave function is therefore unique without imposing
Hartle--Hawking or Vilenkin boundary conditions---the
microscopic (Havelock) structure determines the
cosmological state.
\end{remark}
```

- [ ] **Step 2: Verify LaTeX compiles** (visual check for balanced environments)

- [ ] **Step 3: Commit**

---

### Task 2: Paper III — Entropy bridge remark (after line 3205)

**Files:**
- Modify: `latex/paper-3-gravity/main.tex:3205` (after "Summary of the bridge" paragraph, before Code availability)

- [ ] **Step 1: Insert entropy bridge remark**

Insert after line 3206 (after "...the Schrödinger equation)."), before the Code availability paragraph:

```latex
\begin{remark}[Entropy bridge: Onsager coarse-graining to Bekenstein--Hawking]
\label{rmk:entropy-bridge}
The central charge $c = 12\,b(N)$ that appears as the Fisher--Rao
information metric on the angular-mode Boltzmann distributions
(eq.~\eqref{eq:wdw}, Step~2 above) is the \emph{same}~$c$ that
enters the Cardy formula via Brown--Henneaux
($c = 3\ell/(2G_3)$, \S\ref{sec:holographic}).
The Bekenstein--Hawking entropy at the palindromic threshold is
\begin{equation}\label{eq:entropy-bridge}
  S_{\mathrm{BH}} = \frac{\pi c}{3}\,\cosh\rho^*
  = \frac{\pi c}{3}\,T_{\mathrm{GH}}\,L,
\end{equation}
where $T_{\mathrm{GH}} = \coth(\rho^*)/(2\pi)$ is the
Gibbons--Hawking temperature and $L = 2\pi\sinh\rho^*$ is the
horizon circumference.
Three entropy levels illuminate the structure:
\begin{center}\small
\begin{tabular}{lccc}
\toprule
Level & Formula & $N\!=\!7$ & Scaling \\
\midrule
CL squeezing
  & $\sum_m[(r_m{+}1)\ln(r_m{+}1) - r_m\ln r_m]$
  & $1.6$ & $O(1)$ \\
One-loop (frozen det.)
  & $\tfrac{1}{2}\sum_{m \ne m^*}\ln|\lambda_m(\rho^*)|$
  & $1.1$ & $O(N)$ \\
Cardy (BH)
  & $(\pi c/3)\cosh\rho^*$
  & $158$ & $O(e^{\rho^*})$ \\
\bottomrule
\end{tabular}
\end{center}
The Gaussian (Caldeira--Leggett) entanglement captures the same~$c$
but accounts for $O(1/c)$ of the total: the gap
$S_{\mathrm{BH}}/S_{\mathrm{1\text{-}loop}} \approx 144$
(at $N = 7$, growing to $5.5 \times 10^4$ at $N = 15$)
reflects the exponential density of Virasoro descendants
inaccessible to the Gaussian approximation.
The Onsager coarse-graining determines~$c$;
the Cardy formula completes~$c$ to the full entropy.
\end{remark}
```

- [ ] **Step 2: Commit**

---

### Task 3: Paper V — New §9 "Spatial geometry and the initial state" (after line 1217)

**Files:**
- Modify: `latex/paper-5-cosmology/main.tex:1218` (between Dark matter detection and Conclusion)

- [ ] **Step 1: Insert new section**

Insert after line 1217 (after "...structure formation, CMB spectral distortions)."), before the %% separator:

```latex


%% ====================================================================
\section{Spatial geometry and the initial state}
\label{sec:geometry-initial}

Three structural consequences of the Seifert geometry
$\mathbf{H}^2 \times_N S^1$.

\paragraph{Spatial flatness.}
The Kaluza--Klein reduction absorbs the $\mathbf{H}^2$ curvature
($K = -1$) into the three-dimensional cosmological constant
$\Lambda_3 = (N^2 - 16)/16$ (eq.~\eqref{eq:lambda3}).
The $3{+}1$-dimensional spatial sections are flat:
$\Omega_k = 0$ exactly, not as a fine-tuning but as a consequence
of the KK mechanism---the negative internal curvature and the
positive $S^1$ flux energy are absorbed into~$\Lambda_3$, leaving
no residual spatial curvature.
Current constraints ($|\Omega_k| < 0.002$, Planck 2018) are
consistent; next-generation surveys (CMB-S4, Euclid) will reach
$|\Omega_k| < 10^{-4}$.
The framework predicts exactly zero, distinguishable in principle
from inflationary predictions $\Omega_k \sim e^{-2N_e}$.

\paragraph{No initial singularity.}
The WDW wave function (Paper~III, eq.~\eqref{III-eq:wdw}) is
evanescent in the interior ($V < 0$, $\rho < \rho^*$) and
oscillatory in the exterior ($V > 0$, $\rho > \rho^*$).
As $\rho \to 0$, $V(\rho) \to \log(2\rho) + \mathrm{const} \to -\infty$
and $\Psi \to 0$ exponentially.  The WKB action
\begin{equation}\label{eq:wkb-convergence}
  S_{\mathrm{WKB}} = \int_0^{\rho^*}\!\sqrt{2c\,|V(\rho)|}\;d\rho
  \;<\; \infty
\end{equation}
converges (numerically: $5.8$ oscillations for $N = 7$,
$32.7$ for $N = 11$; see Code Availability).
Classical spacetime begins at the turning point
$\rho = \rho^*$, where the $S^1$ fibre becomes a physical
spatial dimension and Lorentzian time emerges from the
WKB phase.
The Born--Oppenheimer tunnelling action $2S = 36.548$
(eq.~\eqref{eq:tunnelling-action}) determines the amplitude.
The wave function is unique
(Remark~\ref{III-rmk:wdw-uniqueness}): the CMS integrability
of the angular sector selects the ground state of the
effective Hamiltonian, bypassing the Hartle--Hawking vs.\
Vilenkin boundary-condition ambiguity.

\paragraph{Thermodynamic closure.}
The Onsager mechanism requires three prerequisites
(Lemma~\ref{III-lem:onsager-prerequisites}): compact phase
space, fixed total energy, and fixed vortex number~$N$.
All three require a closed system---the negative-temperature
states that drive polygon formation do not exist in open systems
where energy can leak out.
The WDW constraint $H\Psi = 0$ is the quantum version of total
energy conservation.
The universe expands eternally ($w = -1$, $\Lambda > 0$) but
exchanges no energy with an environment.
Local spacetime curvature ($R_{\mu\nu\sigma\tau} \ne 0$) is
present through the full Einstein equations
(Paper~III, Theorem~\ref{III-thm:polygon-einstein}
and Paper~IV, Theorem~\ref{IV-thm:nonlinear-einstein});
the spatial flatness is a statement about the global FLRW
average, not about local geometry.
```

- [ ] **Step 2: Commit**

---

### Task 4: Paper V Conclusion — Extend with new results (modify line 1239-1241)

**Files:**
- Modify: `latex/paper-5-cosmology/main.tex:1239-1241`

- [ ] **Step 1: Extend the prediction sentence**

Replace lines 1239-1241:
```
Three falsifiable predictions --- normal neutrino hierarchy,
$w = -1$ exactly, and no $0\nu\beta\beta$ decay --- are
tested by JUNO, Euclid, and nEXO respectively.
```

With:
```latex
Five falsifiable predictions --- normal neutrino hierarchy,
$w = -1$ exactly, no $0\nu\beta\beta$ decay,
$\Omega_k = 0$ exactly, and no initial singularity
(replaced by quantum tunnelling at $\rho = \rho^*$) --- are
tested by JUNO, Euclid, nEXO, CMB-S4, and future
quantum-gravity phenomenology respectively.
```

- [ ] **Step 2: Commit**

---

### Task 5: Paper VI — Add Ω_k and null predictions to falsifiable tests (after line 471)

**Files:**
- Modify: `latex/paper-6-discussion/main.tex:471` (after EWPT item, before correlated observables)

- [ ] **Step 1: Insert new binary test and null predictions**

Insert after line 471 (`\end{itemize}`), before `\emph{(ii)~Correlated observables.}`:

```latex
\item $\Omega_k = 0$ exactly
  (the KK reduction absorbs all spatial curvature into
  $\Lambda_3 = (N^2{-}16)/16$;
  CMB-S4 and Euclid will reach $|\Omega_k| < 10^{-4}$,
  where the framework predicts exactly zero,
  distinguishable from inflationary
  $\Omega_k \sim e^{-2N_e}$).
\end{itemize}
\emph{(i\hspace{0.5pt}b)~Null predictions}
(the absence of each is a falsifiable consequence):
no cosmic strings,
no magnetic monopoles,
no isocurvature perturbations (single breathing mode
$\rho$ provides a single clock),
$N_{\mathrm{eff}} = 3.00$ (no additional light relics),
no cosmic birefringence,
no dark matter annihilation signals
(gravitational-strength coupling,
$\sigma_{\mathrm{SI}} \sim 10^{-103}\;\mathrm{cm^2}$),
NANOGrav signal is astrophysical
(supermassive black hole binaries, not cosmological),
and $r \sim 10^{-6}$ (undetectable primordial gravitational
waves from inflation; \S\ref{V-sec:inflation}).
```

Note: this replaces the `\end{itemize}` on line 471 — the new item goes inside the list, and a new `\end{itemize}` follows.

- [ ] **Step 2: Commit**

---

### Task 6: Paper VI — Cosmological framing paragraph (before Conclusion, after line 499)

**Files:**
- Modify: `latex/paper-6-discussion/main.tex:499` (after CKM paragraph, before Conclusion)

- [ ] **Step 1: Insert framing paragraph**

Insert after line 499 (after "...all entries computed from $N = 7$."), before `\section{Conclusion}`:

```latex

\paragraph{Cosmological structure.}
The framework determines the large-scale structure of the
universe without free cosmological parameters beyond~$M_P$.
Spatial sections are flat
($\Omega_k = 0$, \S\ref{V-sec:geometry-initial}),
the equation of state is $w = -1$ at all redshifts
(\S\ref{V-sec:cc-instanton}),
and the initial state is uniquely determined by the
Born--Oppenheimer structure of the polygon breathing mode
(Remark~\ref{III-rmk:wdw-uniqueness}).
The classical big-bang singularity is replaced by quantum
tunnelling at the palindromic threshold $\rho^*$, where
the 2D vortex system on $\mathbf{H}^2$ gives rise to
$3{+}1$-dimensional Lorentzian spacetime through the
Wick rotation $\rho \to \rho + i\pi/2$.
The Bekenstein--Hawking entropy at the threshold
is determined by the same central charge
$c = 12\,b(N)$ that governs the WDW kinetic term
(Remark~\ref{III-rmk:entropy-bridge}):
$S_{\mathrm{BH}} = (\pi c/3)\cosh\rho^*$, counting the
non-perturbative Virasoro descendants of the angular modes
coarse-grained by the Onsager mechanism.
```

- [ ] **Step 2: Commit**

---

### Task 7: Update cross-references and verify

- [ ] **Step 1: Check that all \label and \ref pairs resolve**

Search for the new labels: `rmk:wdw-uniqueness`, `rmk:entropy-bridge`, `sec:geometry-initial`, `eq:entropy-bridge`, `eq:wkb-convergence`.

Cross-refs from Paper V and VI to Paper III use the `III-` prefix convention. Verify these match.

- [ ] **Step 2: Run full test suite to confirm code still passes**

```bash
python3 -m pytest tests/test_wdw_initial_conditions.py tests/test_entropy_bridge.py -q
```

- [ ] **Step 3: Final commit**
