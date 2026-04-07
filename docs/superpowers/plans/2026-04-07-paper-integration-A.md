# Paper Integration Plan A: Paper I Extensions + Paper IV Strengthening

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate the Platonic Havelock results (GAP D) into Paper I and strengthen Paper IV's Weinberg angle and coupling constant derivations.

**Architecture:** Paper I gets a new §5 ("Platonic extensions") inserted between current §5 (stability thresholds) and §6 (algebraic structure). The current §6 (algebraic structure) gets extended with I*/McKay/Coxeter results. Paper IV's existing §7-9 get derivation improvements. All changes are LaTeX text with theorem/proof environments following the existing paper style.

**Tech Stack:** LaTeX, existing shared preamble, cross-references via \externaldocument.

---

### Task 1: Paper I — New §5a: Generalized Havelock formula for Platonic solids

**Files:**
- Modify: `latex/paper-1-mathematics/main.tex` (insert after line ~1400, end of current §5)

- [ ] **Step 1: Insert new subsection after §5.2 (hyperbolic plane)**

Insert after the closing of the hyperbolic plane subsection (around line 1400), before §6 begins:

```latex
\subsection{Platonic extensions: the generalized Havelock formula}
\label{sec:platonic-havelock}

The Havelock identity extends from regular $N$-gons ($\mathbb{Z}_N$
symmetry) to Platonic solid configurations on~$\mathbf{S}^2$ with
non-abelian symmetry group $G \subset \mathrm{SO}(3)$.

\begin{theorem}[Generalized Havelock formula]\label{thm:platonic-havelock}
Let $G \subset \mathrm{SO}(3)$ act transitively on $N$ vertices
$\{v_0, \ldots, v_{N-1}\} \subset \mathbf{S}^2$, and let
$K(d) = 1/(4\sin^2(d/2))$ be the $\mathbf{S}^2$ interaction kernel.
For each $G$-irrep $\rho$ that is the restriction of the $\mathrm{SO}(3)$
representation $D^j$ to~$G$ (with $D^j|_G$ irreducible), the eigenvalue
of the zero-sum interaction matrix in the $\rho$-isotypic sector is
$-T_\rho$, where
\begin{equation}\label{eq:platonic-havelock}
  T_\rho = \sum_{k \neq 0} K(d_{0k})\bigl[1 - P_j(\cos d_{0k})\bigr],
\end{equation}
and $P_j$ is the Legendre polynomial of degree~$j$.
\end{theorem}

\begin{proof}
By Schur's lemma, $K$ is $G$-invariant and hence acts as a scalar
on each $G$-irrep.  The zonal spherical function of $D^j$ on
$\mathbf{S}^2 = \mathrm{SO}(3)/\mathrm{SO}(2)$ is the Legendre
polynomial $P_j$.  When $D^j|_G = \rho$ is irreducible,
$P_j(\cos d_{0k})$ restricted to the orbit is the eigenvector.
Evaluating $K \cdot P_j$ at vertex~$0$ and using the zero-sum property
$K_{00} = -C_1$ gives the eigenvalue $-T_\rho$.
\end{proof}

Verified numerically for the tetrahedron ($j \le 1$, $A_4$),
octahedron ($j \le 2$, $S_4$), icosahedron ($j \le 3$, $A_5$),
and cube ($j \le 2$, $S_4$); residuals $< 10^{-16}$ in all cases
(77~computational tests).
```

- [ ] **Step 2: Compile Paper I and check for errors**

Run: `cd latex/paper-1-mathematics && pdflatex main.tex`
Expected: Compiles without errors. Check the new subsection renders correctly.

- [ ] **Step 3: Commit**

```bash
git add latex/paper-1-mathematics/main.tex
git commit -m "paper I: add generalized Havelock formula for Platonic solids (Thm 5.x)"
```

---

### Task 2: Paper I — New §5b: Tangent Hessian eigenvalue pairing

**Files:**
- Modify: `latex/paper-1-mathematics/main.tex` (insert after Task 1's subsection)

- [ ] **Step 1: Insert new subsection**

```latex
\subsection{Tangent Hessian eigenvalue pairing}
\label{sec:hessian-pairing}

\begin{theorem}[Eigenvalue pairing]\label{thm:hessian-pairing}
For a $G$-symmetric configuration of $N$ vertices on~$\mathbf{S}^2$,
the tangent-space Hessian eigenvalues come in pairs
$(\lambda_-(\rho),\, \lambda_+(\rho))$ summing to a universal constant:
\begin{equation}\label{eq:hessian-pairing}
  \lambda_+(\rho) + \lambda_-(\rho) = \frac{N-1}{2}
  \qquad \text{for all $G$-irreps $\rho$}.
\end{equation}
\end{theorem}

\begin{proof}
\emph{Step 1 (Laplacian identity).}
For $f(d) = -\ln\sin(d/2)$ on~$\mathbf{S}^2$,
$f' = -\tfrac{1}{2}\cot(d/2)$ and $f'' = 1/(4\sin^2(d/2))$.
The radial Laplacian $\Delta f = f'' + \cot(d)\,f'$
equals $(1 - \cos d)/(4\sin^2(d/2)) = 1/2$,
a \emph{constant independent of~$d$}.

\emph{Step 2 (Per-vertex trace).}
The diagonal block $H_{kk}$ of the $2N \times 2N$ tangent Hessian
has trace $\operatorname{Tr}(H_{kk}) = \sum_{j \neq k} \tfrac{1}{2}
= (N-1)/2$.

\emph{Step 3 (Schur decomposition).}
$H$ is $G$-equivariant.  On the isotypic component of~$\rho$
(multiplicity~$2$ from $\operatorname{Ind}(\omega) \oplus
\operatorname{Ind}(\bar\omega)$), Schur's lemma gives
$H|_\rho = A_\rho \otimes \mathrm{Id}_{d_\rho}$ where $A_\rho$
is a $2 \times 2$ matrix with eigenvalues $\lambda_\pm(\rho)$.

\emph{Step 4 (Stabiliser isotropy).}
The vertex stabiliser $H_v \supset \mathbb{Z}_n$ ($n \ge 3$ for all
Platonic solids) acts on $T_{v_k}\mathbf{S}^2$ by rotation, forcing
$H_{kk} = \tfrac{N-1}{4}\,I_2$.  By $G$-transitivity, the per-vertex
trace distributes uniformly across all irreps:
$\operatorname{Tr}(A_\rho) = \lambda_+ + \lambda_- = (N{-}1)/2$.
\end{proof}

\begin{corollary}
$\operatorname{Tr}(H) = N(N-1)/2$.
\end{corollary}

Verified for the tetrahedron ($N = 4$, pairs $(0, 3/2)$ and
$(3/4, 3/4)$), the octahedron ($N = 6$, pairs $(0, 5/2)$ and
$(1/2, 2)$), and the icosahedron ($N = 12$, pairs $(0, 11/2)$,
$(1/2, 5)$, and $(5/4, 17/4)$).
```

- [ ] **Step 2: Compile and verify**

- [ ] **Step 3: Commit**

```bash
git add latex/paper-1-mathematics/main.tex
git commit -m "paper I: add tangent Hessian pairing theorem (Thm 5.x)"
```

---

### Task 3: Paper I — New §5c: The icosahedral bridge identity

**Files:**
- Modify: `latex/paper-1-mathematics/main.tex`

- [ ] **Step 1: Insert new subsection**

```latex
\subsection{The icosahedral bridge identity}
\label{sec:bridge-identity}

The icosahedron has three classes of inter-vertex distances on the
unit~$\mathbf{S}^2$: five nearest neighbours at $d_1 = \cos^{-1}(1/\sqrt{5})$,
five far neighbours at $d_2 = \cos^{-1}(-1/\sqrt{5})$, and one
antipodal vertex at~$d_3 = \pi$.

\begin{theorem}[Bridge identity]\label{thm:bridge}
The Havelock eigenvalue for $\mathrm{SO}(3)$ spin~$j$ on the icosahedron is
\begin{equation}\label{eq:bridge}
  \lambda_j = 5K_1\, P_j\!\bigl(\tfrac{1}{\sqrt{5}}\bigr)
            + 5K_2\, P_j\!\bigl(-\tfrac{1}{\sqrt{5}}\bigr)
            + \tfrac{1}{4}(-1)^j,
\end{equation}
where $K_1 = (5+\sqrt{5})/8$, $K_2 = (5-\sqrt{5})/8$, and
$P_j$ is the Legendre polynomial.
\end{theorem}

The three terms correspond to the three distance classes.
The golden ratio enters structurally:
$K_1 - K_2 = \sqrt{5}/4$ controls the odd-$j$ splitting,
$K_1 + K_2 = 5/4$ sets the even-$j$ level, and
$c = 1/\sqrt{5} = 1/(2\varphi - 1)$ is the icosahedral
golden angle.

For $j = 0, 1, 2, 3$, the formula gives the exact half-integers
$\lambda = 13/2,\; 1,\; -1,\; -3/2$, with $C_1 = 13/2$.
This is the icosahedral analogue of the polygon formula
$\lambda_m = (N{-}1) - m(N{-}m)/2$.
```

- [ ] **Step 2: Compile and verify**

- [ ] **Step 3: Commit**

```bash
git add latex/paper-1-mathematics/main.tex
git commit -m "paper I: add icosahedral bridge identity (Thm 5.x)"
```

---

### Task 4: Paper I — §6 extension: I* character table and McKay correspondence

**Files:**
- Modify: `latex/paper-1-mathematics/main.tex` (insert in §6, algebraic structure)

- [ ] **Step 1: Insert new subsection in §6**

Insert after the existing algebraic structure material (around line 1900), before the geodesics subsection or as a new subsection:

```latex
\subsection{The binary icosahedral group and the McKay correspondence}
\label{sec:i-star-mckay}

The Platonic framework connects to $E_8$ through the binary
icosahedral group $I^* \subset \mathrm{SU}(2)$, the double cover
of the icosahedral rotation group~$A_5$.

$I^*$ has order~$120$ and nine conjugacy classes.  Its nine
irreducible representations have dimensions
$\{1, 2, 3, 4, 5, 6, 4, 2, 3\}$ (in McKay ordering).  The first
six are restrictions of $\mathrm{SU}(2)$ representations
$V_{2j+1}$ for $j = 0, \tfrac{1}{2}, 1, \tfrac{3}{2}, 2, \tfrac{5}{2}$;
the remaining three arise from the McKay recursion when $V_7$, $V_8$,
$V_9$ split upon restriction to~$I^*$.

\begin{theorem}[McKay correspondence for $I^*$]\label{thm:mckay-i-star}
The tensor product $\rho_1 \otimes \rho_i = \bigoplus_j a_{ij}\,\rho_j$
has adjacency matrix $(a_{ij})$ equal to the adjacency matrix of the
extended $E_8$ Dynkin diagram $\tilde{E}_8$.
\end{theorem}

The marks of $\tilde{E}_8$ (null root coefficients) are the
dimensions of the $I^*$ irreps: $1, 2, 3, 4, 5, 6, 4, 2, 3$
(sum~$30 = h(E_8)$, the Coxeter number).

The McKay adjacency matrix has eigenvalues
$\{-2, -\varphi, -1, -1/\varphi, 0, 1/\varphi, 1, \varphi, 2\}$,
where $\varphi = (1+\sqrt{5})/2$ is the golden ratio.
The same $\varphi$ governs the icosahedral interaction kernel
(Theorem~\ref{thm:bridge}), connecting $E_8$ graph theory to
icosahedral geometry.
```

- [ ] **Step 2: Compile and verify**

- [ ] **Step 3: Commit**

```bash
git add latex/paper-1-mathematics/main.tex
git commit -m "paper I: add I* character table and McKay correspondence (§6)"
```

---

### Task 5: Paper I — §6 extension: Coxeter decomposition of E₈ adjoint

**Files:**
- Modify: `latex/paper-1-mathematics/main.tex`

- [ ] **Step 1: Insert after Task 4's subsection**

```latex
\subsection{Coxeter decomposition of the $E_8$ adjoint}
\label{sec:coxeter-decomposition}

\begin{theorem}[Coxeter decomposition]\label{thm:coxeter}
The $E_8$ adjoint representation restricted to $I^*$ (via the
Coxeter element of $W(E_8)$) decomposes as
\begin{equation}\label{eq:coxeter}
  248 = 2\,\mathrm{reg}(I^*) + 2(\rho_1 + \rho_7),
\end{equation}
with multiplicities $\{2, 6, 6, 8, 10, 12, 8, 6, 6\}$
equalling $2 d_i$ for all irreps except $\rho_1$ and $\rho_7$
(both of dimension~$2$), which receive an extra~$2$.
\end{theorem}

The integer-spin irreps ($\rho_0, \rho_2, \rho_4, \rho_6, \rho_8$)
contribute $120$~dimensions; the half-integer irreps
($\rho_1, \rho_3, \rho_5, \rho_7$) contribute~$128$.
This matches the branching $E_8 \supset \mathrm{SO}(16)$:
$248 = 120_{\mathrm{adj}} \oplus 128_{\mathrm{spinor}}$.

The $120/128$ split is physically significant: the integer-spin
sector is the classical vortex physics visible on~$\mathbf{S}^2$
(Paper~II), while the half-integer sector (the spinor) is invisible
classically but revealed on~$S^3$ (Paper~V, \S\ref{sec:600cell}).
```

- [ ] **Step 2: Compile and verify**

- [ ] **Step 3: Commit**

```bash
git add latex/paper-1-mathematics/main.tex
git commit -m "paper I: add Coxeter decomposition 248=2reg+2(ρ₁+ρ₇) (§6)"
```

---

### Task 6: Paper IV — Strengthen Weinberg angle derivation

**Files:**
- Modify: `latex/paper-4-field-theory/main.tex` (§7, Weinberg angle section)

- [ ] **Step 1: Find and strengthen the Weinberg angle section**

Locate the Weinberg angle section (grep for `Weinberg` or `sin.*theta`). Replace or augment the derivation with:

```latex
The Weinberg angle follows from the WZW conformal weights at
level $k = 1$.  The $\mathrm{SU}(2)_1$ adjoint ($j = 1$) has
conformal weight
\[
  h_W = \frac{j(j+1)}{k + h^\vee} = \frac{2}{1 + 2} = \frac{2}{3}.
\]
The $\mathrm{U}(1)_Y$ sector inherits the Kaluza--Klein level
$K_Y = e/2 = 1/2$ from the Euler class $e = 1$ of the Hopf
fibration and the DHVW twist-field normalisation.  The conformal
weight of the hypercharge current with fundamental charge
$Q = 1/2$ is
\[
  h_Y = \frac{Q^2}{2K_Y} = \frac{1/4}{1} = \frac{1}{4}.
\]
The Weinberg angle at the orbifold scale is therefore
\begin{equation}\label{eq:weinberg}
  \sin^2\theta_W = \frac{h_Y}{h_Y + h_W}
  = \frac{1/4}{1/4 + 2/3} = \frac{1/4}{11/12} = \frac{3}{11}
  \approx 0.2727.
\end{equation}
No normalisation ambiguity arises: $K_Y$, $Q$, $k$, and $h^\vee$
are all topologically determined.
```

- [ ] **Step 2: Find and strengthen the CS level derivation**

In the UV completion section (§9), add or strengthen:

```latex
The Chern--Simons level $k = 1$ is fixed by the Euler class of
the Hopf fibration $S^1 \to S^3 \to S^2$: $e = c_1(\mathcal{O}(1)) = 1$.
The DHVW orbifold construction fixes the base level at~$1$, giving
$k = e \times 1 = 1$.  This is topological: the Euler class $e \in \mathbb{Z}$
classifies principal $\mathrm{U}(1)$-bundles over~$S^2$, and $k = 1$
is the unique minimal nontrivial case.

For $E_8$ at $k = 1$: $1/g^2 = k + h^\vee = 31$ and the WZW
central charge $c = 248/31 = 8$ (exactly).
```

- [ ] **Step 3: Compile Paper IV and verify**

- [ ] **Step 4: Commit**

```bash
git add latex/paper-4-field-theory/main.tex
git commit -m "paper IV: strengthen Weinberg angle (conformal weights) and CS level (Euler class)"
```

---

### Task 7: Final consistency check

- [ ] **Step 1: Compile all modified papers**

```bash
cd latex/paper-1-mathematics && pdflatex main.tex && pdflatex main.tex
cd ../paper-4-field-theory && pdflatex main.tex && pdflatex main.tex
```

- [ ] **Step 2: Check cross-references resolve**

Grep for undefined references:
```bash
grep -i 'undefined' latex/paper-1-mathematics/main.log
grep -i 'undefined' latex/paper-4-field-theory/main.log
```

- [ ] **Step 3: Commit final state**

```bash
git add latex/
git commit -m "paper integration plan A complete: Paper I extensions + Paper IV strengthening"
```
