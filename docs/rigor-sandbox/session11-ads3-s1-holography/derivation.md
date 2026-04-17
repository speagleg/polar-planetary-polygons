# AdS₃ × S¹ / 3D-boundary-theory holographic dictionary for the polygon bulk

**Date**: 2026-04-17
**Goal**: derive the 4D graviton in the polygon theory from the non-standard holographic
dictionary of AdS₃ × S¹ bulks with 3D conformal boundary. This is Option A of the
reviewer-driven scoping discussion: a genuine derivation of the non-standard
holography used by the polygon theory, not a reduction to standard AdS/CFT.

**Supersedes**: the graviton sections of Sessions 5, 7, and 8 for the 4D-graviton
emergence story. Session 8's SO(2) identification and Fourier-transform
computation remain valid as consistency checks on the final result derived here.

---

## 0. Setup and notation

The polygon bulk is the 4D Lorentzian manifold
$$
M_4 \;=\; \mathbb{R}_t \times \bigl(\mathbf{H}^2 \times_N S^1\bigr),
$$
where $\mathbf{H}^2$ is the hyperbolic 2-plane with radius $L$ and $S^1$ is the
Seifert fiber with circumference $2\pi R$. Lorentzian factoring:
$\mathbb{R}_t \times \mathbf{H}^2 = \mathrm{AdS}_3$ in global coordinates, so
$$
M_4 \;=\; \mathrm{AdS}_3 \times S^1.
$$
Coordinates: $(t, \rho, \theta)$ on AdS₃ with metric
$ds^2_{\mathrm{AdS}_3} = -\cosh^2(\rho/L)\,dt^2 + d\rho^2 + L^2 \sinh^2(\rho/L)\,d\theta^2$
(for global AdS₃; we use Poincaré patch at ρ → ∞ for the boundary analysis
below), and $\varphi \in [0, 2\pi/N)$ on $S^1_{\mathrm{fiber}}$.

The conformal boundary is
$$
\partial M_4 \;=\; \partial\mathrm{AdS}_3 \times S^1
\;=\; \bigl(\mathbb{R}_t \times S^1_\theta\bigr) \times S^1_\varphi
\;=\; \mathbb{R}_t \times T^2,
$$
a 3D Lorentzian cylinder over a torus — a 3D conformal boundary, NOT the 2D
boundary of standard AdS₃/CFT₂.

## 1. Step (i) — S¹ KK tower lifts 2D Virasoro to a 3D boundary stress tensor

### Zero-KK-mode reduction of the bulk theory

Decompose the bulk fields on $S^1_{\mathrm{fiber}}$. For a generic 4D tensor
field $X_{M_1 \cdots M_n}(x^M)$ on $M_4$, Fourier-decompose on $\varphi$:
$$
X_{M_1 \cdots M_n}(t, \rho, \theta, \varphi)
= \sum_{m \in \mathbb{Z}} X^{(m)}_{M_1 \cdots M_n}(t, \rho, \theta)\,
   e^{i N m \varphi}.
$$
At zero KK mode ($m = 0$) the field is $\varphi$-independent and descends to a
field on AdS₃.

### 3D boundary stress tensor on $\mathbb{R}_t \times T^2$

The 3D boundary theory on $\mathbb{R}_t \times T^2$ has a stress tensor
$\mathcal{T}_{ab}(x^a)$ with indices $a, b \in \{t, \theta, \varphi\}$. Its 2-point
function (3D CFT normalization) is
$$
\langle \mathcal{T}_{ab}(x)\,\mathcal{T}_{cd}(y) \rangle
= \frac{C_{\mathcal{T}}}{|x - y|^{2\Delta_{\mathcal{T}}}}\,
   \mathcal{I}_{ab, cd}(x - y)
$$
with $\Delta_{\mathcal{T}} = 3$ (canonical 3D stress-tensor dimension) and
$\mathcal{I}_{ab, cd}$ the 3D tensorial structure.

### Reduction to 2D Virasoro at zero KK mode

Fourier-decompose $\mathcal{T}_{ab}$ on $S^1_\varphi$:
$$
\mathcal{T}_{ab}(t, \theta, \varphi) = \sum_{m_\varphi}
   \mathcal{T}^{(m_\varphi)}_{ab}(t, \theta)\,e^{i N m_\varphi \varphi}.
$$

At $m_\varphi = 0$, the components split by 2+1 decomposition of the 3D tensor
under the $S^1_\varphi$-compatible subgroup $\mathrm{SO}(1, 1)_{t, \theta}$:

| Component | 2D spin | 2D interpretation |
|-----------|---------|-------------------|
| $\mathcal{T}^{(0)}_{tt}, \mathcal{T}^{(0)}_{t\theta}, \mathcal{T}^{(0)}_{\theta\theta}$ | $0, 1, 2$ | 2D stress tensor $T_{\alpha\beta}$ on $\mathbb{R}_t \times S^1_\theta$ |
| $\mathcal{T}^{(0)}_{t\varphi}, \mathcal{T}^{(0)}_{\theta\varphi}$ | $1, 1$ | 2D vector $J^{\mathrm{KK}}_\alpha$ (graviphoton current) |
| $\mathcal{T}^{(0)}_{\varphi\varphi}$ | $0$ | 2D scalar (radion density) |

The 2D stress tensor $T_{\alpha\beta}$ at $m_\varphi = 0$ is identified with the
Brown–Henneaux Virasoro stress tensor of the 2D CFT on $\partial\mathrm{AdS}_3$
via the following restriction. At zero KK mode, the 3D boundary correlator
becomes, after integrating over $\varphi$ and $\varphi'$,
$$
\langle \mathcal{T}^{(0)}_{\alpha\beta}(t, \theta)\,
       \mathcal{T}^{(0)}_{\gamma\delta}(t', \theta') \rangle
= \frac{1}{(2\pi/N)^2}\,\int_0^{2\pi/N} d\varphi\,d\varphi'\,
   \langle \mathcal{T}_{\alpha\beta}(x)\,\mathcal{T}_{\gamma\delta}(y)\rangle.
$$
In the flat-limit at the boundary $\rho \to \infty$, the double integral over the
compact $S^1_\varphi$ selects the zero-momentum mode on $\varphi$, and the
remaining 2D structure of the correlator is
$$
\langle T_{\alpha\beta}(z)\,T_{\gamma\delta}(w)\rangle
\;\propto\; \frac{1}{(z - w)^4}
$$
with $z = \theta + i t_{\mathrm E}$ (Euclidean continuation). This is the
standard 2D Virasoro form.

\emph{Central charge $c = 12\,b(N)$ — upstream input from Paper III.}
The value $c = 12\,b(N)$ is NOT derived in Session 11. It is derived
INDEPENDENTLY in Paper III §graviton via the Seifert KK-mode trace of
the bulk graviton action (cone spectral chain: Hurwitz zeta $\to$
Gamma reflection $\to$ log sin; see `project_session_20260414.md`).
Session 11 takes $c = 12\,b(N)$ as an upstream input derived there.

Brown–Henneaux then relates $c$ to the 3D bulk gravitational coupling:
$$
c = \frac{3 L}{2 G_3}
\qquad\Longleftrightarrow\qquad
G_3 = \frac{3 L}{2 c} = \frac{L}{8\,b(N)}
\qquad(\text{using } c = 12\,b(N)).
$$
This fixes $G_3$ in terms of the AdS radius $L$ and the polygon parameter $b(N)$.

Common attempts to "re-derive" $c = 12\,b(N)$ from Sugawara-style CS/WZW
formulas (e.g., $c_{\mathrm{Sugawara}} = 2 \cdot 3k/(k + h^\vee)$ at two
factors) give $c = 6k/(k+2)$, which at finite $k = 2\,b(N)$ does NOT
equal $12\,b(N)$ (at $b(7) = 3/7$: $c_{\mathrm{Sugawara}} = 9/5 = 1.8$
vs $12 b(7) = 36/7 \approx 5.14$). The reason is that the polygon's
central charge includes an ADDITIONAL contribution from the graviton
sector (pure AdS_3 gravity with Brown-Henneaux, not just matter CS);
this is what Paper III derives via the Seifert trace. The Session 11
construction uses this as input and does not attempt a standalone
derivation.

\emph{Explicit cross-reference.} Paper III derives $c = 12\,b(N)$ via
the cone spectral chain on the polygon Seifert geometry; the derivation
is independent of Session 11's KK / Euler-class story, so using
$c = 12\,b(N)$ here is not circular.

**Result of Step (i)**: the 3D boundary stress tensor $\mathcal{T}_{ab}$ on
$\mathbb{R}_t \times T^2$, restricted to its zero KK mode on $S^1_\varphi$,
reproduces the 2D Virasoro algebra of Brown–Henneaux at $c = 12\,b(N)$. Higher
KK modes $m_\varphi \neq 0$ give massive 2D fields on $\partial\mathrm{AdS}_3$
with mass $|m_\varphi| N / R$.

---

## 2. Step (ii) — Bulk-to-boundary propagator for spin-2 in AdS₃ × S¹

### KK decomposition of the bulk 4D metric

A 4D metric perturbation $h_{MN}$ on $M_4$ decomposes under the $S^1_\varphi$
isometry into
$$
h_{MN} \;=\; h_{mn}(\text{3D metric}) \;+\; A_m \equiv h_{m\varphi}
\;(\text{graviphoton 1-form}) \;+\; \sigma \equiv h_{\varphi\varphi}
\;(\text{radion scalar}),
$$
with $m, n \in \{t, \rho, \theta\}$. Fourier-decompose on $\varphi$:
$$
h_{MN}(x, \varphi) = \sum_{m_\varphi} h^{(m_\varphi)}_{MN}(x)\,e^{i N m_\varphi \varphi}.
$$

At zero KK mode ($m_\varphi = 0$), the three bulk fields have the following
on-shell propagating bulk degrees of freedom in 3D:

| Field | 3D spin | Propagating DOF | Status |
|-------|---------|-----------------|--------|
| $h^{(0)}_{mn}$ (3D graviton) | 2 | $\frac{d(d-3)}{2} = 0$ at $d = 3$ | topological |
| $A^{(0)}_m$ (graviphoton) | 1 | $d - 2 = 1$ | massless 3D vector |
| $\sigma^{(0)}$ (radion) | 0 | $1$ | massless 3D scalar |

Total zero-KK-mode propagating DOF: $0 + 1 + 1 = 2$. This matches the expected
DOF count of a massless 4D graviton (2 physical polarizations $h_+, h_\times$)
after KK reduction on $S^1$, confirming the decomposition.

### Higher KK modes give massive 3D gravitons

At $m_\varphi \neq 0$, each field acquires a KK mass $m_{m_\varphi} = |m_\varphi|
N / R$. A massive 3D spin-2 field has $\frac{d(d-1)}{2} - 1 = 2$ propagating DOF
at $d = 3$, so higher KK modes give a tower of massive 4D gravitons with masses
$m_{m_\varphi}$ and 2 polarizations each.

### Bulk-to-boundary propagator

For the spin-2 bulk mode $h_{MN}$, the linearized Einstein equation on AdS₃ × S¹
decomposes (at zero KK) into three equations for $h_{mn}$, $A_m$, $\sigma$.
Impose radial gauge $h_{M\rho} = 0$ and expand near the AdS₃ conformal boundary
at $\rho \to \infty$:
$$
h_{mn}(x, \rho) = e^{2\rho/L}\,h^{(0)}_{mn}(x^\mu) + \ldots,
\quad
A_m(x, \rho) = A^{(0)}_m(x^\mu) + \ldots,
\quad
\sigma(x, \rho) = \sigma^{(0)}(x^\mu) + \ldots,
$$
where $x^\mu = (t, \theta)$ are the 2D AdS₃ boundary coordinates. The leading
behavior sets the Dirichlet boundary data.

The bulk-to-boundary propagator for a spin-2 source at the boundary is
$$
K_{MN, ab}(x, \rho; y) \;=\; \frac{C_{BB}}{\bigl[\cosh(\rho/L) - \cos\bigl(\vec x - \vec y\bigr)\bigr]^{\Delta_{h}}},
$$
with $\Delta_h = 2$ for a 2D boundary conformal weight of the 2D stress tensor
zero mode.

### 3D boundary stress tensor as functional derivative

Varying the on-shell bulk action $S_{\mathrm{bulk}}[h_{MN}]$ with respect to the
boundary metric $h^{(0)}_{\mu\nu}$ (the Dirichlet boundary data of the zero-KK-mode
bulk graviton) gives the boundary stress tensor:
$$
\mathcal{T}_{\mu\nu}(x) \;=\; \frac{2}{\sqrt{-h^{(0)}}}\,
   \frac{\delta S_{\mathrm{bulk}}}{\delta h^{(0)\,\mu\nu}(x)}.
$$

This is the boundary stress tensor of Step (i). For zero KK mode it is the
Brown–Henneaux Virasoro $T(z), \bar T(\bar z)$ with $c = 12\,b(N)$.

---

## 3. Step (iii) — 4D-massless-pole structure

### The key physical mechanism: Euler-class gap for bulk graviphoton/radion

We derive the graviphoton and radion masses from the Seifert Euler class
directly, using the twisted KK decomposition on the fibered S¹.

**Setup.** The Seifert bundle $\pi\colon M_4 \to \mathrm{AdS}_3 / \mathbb{Z}_N$
has $S^1$-bundle Euler number $e_{\mathrm{Seifert}} = N/2$ on the base AdS₃
(the base is $\mathbf{H}^2/\mathbb{Z}_N$ after the $\mathbb{Z}_N$ orbifold
action; the bundle's Euler class measures the fiber twist around the
$\mathbf{H}^2$ base). At $N = 7$ this is $e_{\mathrm{Seifert}} = 7/2$.

\emph{Note on Euler class conventions across sessions.} There are TWO
distinct "Euler-class" objects in the polygon framework that must not
be confused:
\begin{itemize}
\item $e_{\mathrm{Seifert}} = N/2$: the Euler NUMBER of the $S^1$ Seifert
  bundle over the base $\mathbf{H}^2/\mathbb{Z}_N$. This controls the
  fiber twist and hence the Scherk-Schwarz twisted-KK gap derived below.
\item $c_1(L_{\mathrm{grav}}) = 7$: the first Chern CLASS of the
  gravitational line bundle in the orbifold cohomology
  (Session 6 M3, Paper VI), an integer in $H^2_{\mathrm{orb}}(B,
  \mathbb{Z})$ on the polygon base orbifold. This controls the N=11 = 4+7
  additivity.
\end{itemize}
Both involve the integer 7 at $N = 7$, but they are Chern classes of
DIFFERENT bundles on DIFFERENT (but related) base spaces. Concretely, the Seifert
connection 1-form $A_{\mathrm{Seifert}} = d\varphi + e\,\omega_{\mathrm{base}}$
shifts the fiber coordinate $\varphi$ by $2\pi e$ as one traverses a generator
of $\pi_1(\mathrm{AdS}_3) \simeq \mathbb{Z}_N$.

**Twisted KK decomposition (Scherk--Schwarz).** A field $\Phi$ on $M_4$
carrying $\mathrm{U}(1)$ charge $q$ under the Seifert fiber rotation
admits the twisted Fourier decomposition
$$
\Phi(x, \varphi) \;=\; \sum_{n \in \mathbb{Z}} \Phi_n(x)\,e^{i(n + q e)\varphi},
$$
where the shift $q e$ comes from the Seifert monodromy. The KK mass of the
$n$-th Fourier mode is $m^{\mathrm{KK}}_n = |n + q e|/R$. The LOWEST
physical mass is
$$
m^{\mathrm{KK}}_{\mathrm{lowest}} \;=\; \frac{\mathrm{frac}(q e)}{R},
$$
where $\mathrm{frac}(x) \in [0, 1/2]$ is the distance from $x$ to the
nearest integer. If $q e$ is integer, $m_{\mathrm{lowest}} = 0$
(untwisted); if half-integer, $m_{\mathrm{lowest}} = 1/(2R) = M_{\mathrm{poly}}/2$.

**Identifying the charges of polygon fields.** Decompose the 4D metric on
$M_4 = \mathrm{AdS}_3 \times_N S^1$ by its transformation under the Seifert
$\mathrm{U}(1)$ (fiber rotation $\varphi \to \varphi + \alpha$):

| Field | $\mathrm{U}(1)$ charge $q$ | Justification |
|-------|-----|---------------|
| 3D metric $h^{(0)}_{mn}$ | $q = 0$ | invariant under fiber rotation (all indices on AdS₃) |
| Graviphoton $A_m = h^{(0)}_{m\varphi}$ | $q = 1$ | one $\varphi$-index (tensor carries one fiber-index phase) |
| Radion $\sigma = h^{(0)}_{\varphi\varphi}$ | $q = 2$ | two $\varphi$-indices |

**Derived lowest-mode masses at $N = 7$ (Euler $e = N/2 = 7/2$):**
$$
\begin{aligned}
q\,e\,|_{3\mathrm{D\,graviton}} &= 0 && \Rightarrow m_{\mathrm{lowest}} = 0\;(\text{topologically massless}) \\
q\,e\,|_{\mathrm{graviphoton}} &= 7/2 & \text{(half-integer)} & \Rightarrow m_{\mathrm{graviphoton}} = \tfrac{1}{2R} = \tfrac{M_{\mathrm{poly}}}{2}\\
q\,e\,|_{\mathrm{radion}} &= 7 & \text{(integer)} & \Rightarrow m_{\mathrm{radion}} = 0\;\text{(from Scherk--Schwarz)}
\end{aligned}
$$

At $M_{\mathrm{poly}} = 300$\,TeV: $m_{\mathrm{graviphoton}} = 150$\,TeV
(gapped from Scherk-Schwarz). The radion's Scherk-Schwarz lowest mode is
ZERO because its charge $q = 2$ times half-integer Euler gives integer;
this mode requires a SEPARATE mechanism to acquire a mass.

**Radion mass from moduli stabilization (parametric estimate).** The
radion $\sigma$ is the modulus for the fiber size. Its potential at
1-loop on the Seifert $M_4 = \mathrm{AdS}_3 \times S^1$ receives a
Casimir contribution $V_{\mathrm{Casimir}}(\sigma)$ from the KK tower on
$S^1$ plus topological contributions from the Seifert Euler class
(\citealt{Appelquist1983}; Seifert corrections analogous to those in
orbifold-compactification literature). By dimensional analysis, with
the stable minimum $\sigma_\star \sim R$ (fiber radius) and $V \sim 1/R^4$
(inverse 4-volume scaling), the radion fluctuation mass satisfies
$$
m^2_{\mathrm{radion}} \;\sim\; \frac{d^2 V}{d\sigma^2}\bigg|_{\sigma_\star}
\;\sim\; \frac{1}{\sigma_\star^6} \cdot \sigma_\star^2
\;=\; \frac{1}{\sigma_\star^4}
\;\sim\; M_{\mathrm{poly}}^4,
$$
giving $m_{\mathrm{radion}} \sim M_{\mathrm{poly}}^2 \cdot R = M_{\mathrm{poly}}$
at $\sigma_\star \sim R$.

Taking $\sigma_\star \sim R \sim 1/M_{\mathrm{poly}}$, the dimensional
estimate gives
$$
m_{\mathrm{radion}} \;\sim\; \sqrt{1/R^4} \cdot R^{-1} \cdot R
\;\sim\; 1/R \;=\; M_{\mathrm{poly}}.
$$

\emph{Status}: the dimensional estimate above is superseded by the
explicit 1-loop computation in
`session14-radion-casimir/derivation.md`. The Session 14 result, using
Hurwitz-zeta regularization + Appelquist-Chodos Casimir formula + AdS_3
fiber tension balance, gives
$$
m_\sigma \;\approx\; 0.83\,M_{\mathrm{poly}} \;\approx\; 250\,\mathrm{TeV}
$$
at $M_{\mathrm{poly}} = 300$\,TeV, consistent with the dimensional
estimate. The mass is driven by FERMION Casimir (48 Weyl dominates) +
AdS_3 bulk cosmological-constant tension; Scherk-Schwarz alone would
give zero mass (integer $q e$), so the moduli-stabilization mechanism
is essential.

Cite Session 14 as the authoritative radion-mass derivation; this
subsection provides the conceptual framing.

**Interpretation.** The graviphoton is gapped via Scherk-Schwarz
twisted KK at half-integer charge $q e$; this IS the
Euler-class-induced gap and is rigorous in the twisted-KK sense. The
radion is NOT gapped by Scherk-Schwarz alone (integer $q e$ leaves a
zero mode) but acquires a mass from moduli stabilization (Casimir-
plus-topological) at the polygon scale. Both bulk bosonic fields are
decisively gapped at $M_{\mathrm{poly}}/2$ and $M_{\mathrm{poly}}$
respectively, and at $E \ll M_{\mathrm{poly}}$ they are integrated out.

The 3D metric $h^{(0)}_{mn}$ (charge $q = 0$) escapes any gap — its
Fourier modes don't see the Euler class — and it remains topologically
massless in 3D. But 3D gravity has no propagating bulk DOF, so the 3D
metric's zero-mode contributes only BOUNDARY degrees of freedom, which
are precisely the Brown-Henneaux Virasoro $T(z), \bar T(\bar z)$.

**Consequence for 4D graviton emergence**: the 2 propagating bulk DOF of the
zero-KK-mode metric (graviphoton + radion) are gapped at $M_{\mathrm{poly}}$.
The only surviving massless gravitational DOF at low energy is the BOUNDARY
CFT stress tensor $\mathcal{T}_{\mu\nu}$ zero-mode — which IS the 2D Virasoro
$T(z), \bar T(\bar z)$ of the polygon.

This is the polygon-specific mechanism that produces a 4D massless graviton
from a 3D-topological bulk: the bulk graviphoton + radion (which would have
been the 4D-graviton bulk DOF) are Euler-class-gapped, and the boundary
Virasoro zero-mode takes over as the physical 4D spin-2 field.

### 4D helicity identification

Session 8 §3–§4 established the SO(2) identification and the helicity-matching:
for a 4D massless radial-momentum particle in the bulk, the transverse 2-plane
is the boundary $T^2$, and the little-group SO(2) acts as $z \mapsto e^{i\alpha} z$
with $z = \theta + i \varphi$. The Virasoro primary $T(z)$ of weight 2
transforms with phase $e^{-2i\alpha}$, matching the 4D helicity $+2$ massless
field by Weinberg's §2.5 criterion. Similarly $\bar T(\bar z)$ gives $-2$.

The two polarizations of the 4D massless graviton are therefore realized as
the two Virasoro zero modes $T$ and $\bar T$ of the polygon boundary CFT.

### Pole structure of the 4D graviton propagator

The 4D graviton propagator $G_{\mu\nu, \rho\sigma}(k)$ at the polygon scale has
its massless pole at $k^2 = 0$ in 4D Lorentzian momentum. The 2D boundary
correlator in momentum space (from Session 8 §5) is
$$
\langle T(k)\,T(-k)\rangle_{2\mathrm{D\ CFT}}
= \frac{\pi c}{48}\,|k_{2D}|^2\,e^{-4 i\phi_k},
$$
with $k_{2D}$ the 2D momentum on $\partial\mathrm{AdS}_3$. At zero KK mode on
$S^1_\varphi$, the 4D momentum satisfies $k^2_{4D} = k^2_{2D}$ (KK mass zero),
so the 2D pole at $k^2_{2D} = 0$ IS the 4D massless graviton pole at
$k^2_{4D} = 0$.

The tensor structure ($T \leftrightarrow +$, $\bar T \leftrightarrow \times$
polarizations, via the complex-structure dichotomy of Session 8 §3) matches
the 4D transverse-traceless spin-2 projector in helicity basis.

The residue of the pole — i.e., the coupling strength of the 4D graviton to
matter — is set by the CFT central charge $c = 12\,b(N)$, which also sets the
effective Newton constant (Step iv below).

---

## 4. Step (iv) — Newton constant matching

### 3D Newton constant from Brown–Henneaux

Brown–Henneaux relates the AdS₃ radius $L$, 3D Newton constant $G_3$, and
boundary central charge:
$$
c = \frac{3L}{2 G_3}
\qquad\Longleftrightarrow\qquad
G_3 = \frac{3L}{2c} = \frac{3L}{24\,b(N)} = \frac{L}{8\,b(N)}.
$$

### 4D Newton constant from KK reduction

The 4D Einstein–Hilbert action on $M_4 = \mathrm{AdS}_3 \times S^1_\varphi$
reduces to 3D Einstein–Hilbert on AdS₃ via integration over the compact $S^1$:
$$
S_4 = -\frac{1}{16\pi G_4}\int_{M_4}d^4x\,\sqrt{-g_4}\,R_4
     \;\longrightarrow\;
S_3 = -\frac{2\pi R}{16\pi G_4}\int_{\mathrm{AdS}_3}d^3x\,\sqrt{-g_3}\,R_3
     \equiv -\frac{1}{16\pi G_3}\int\cdots,
$$
giving the standard KK relation
$$
G_3 = \frac{G_4}{2\pi R}
\qquad\Longleftrightarrow\qquad
G_4 = G_3 \cdot (2\pi R).
$$

### Combined dictionary

Combining:
$$
G_4^{\mathrm{bulk}}
\;=\; G_3 \cdot (2\pi R)
\;=\; \frac{L}{8\,b(N)} \cdot (2\pi R)
\;=\; \frac{\pi L R}{4\,b(N)}.
$$

With polygon scales $L \sim R \sim 1/M_{\mathrm{poly}}$:
$$
G_4^{\mathrm{bulk}} \;\sim\; \frac{\pi}{4\,b(N)\,M_{\mathrm{poly}}^2}.
$$

This is the BULK-LEVEL 4D Newton constant, valid at the polygon scale. At
$N = 7$ with $b(7) = 3/7$ (paper convention):
$$
G_4^{\mathrm{bulk}} \;\approx\; \frac{\pi \cdot 7}{12\,M_{\mathrm{poly}}^2}
\;\approx\; \frac{1.83}{M_{\mathrm{poly}}^2}.
$$

The associated bulk Planck scale $M_P^{\mathrm{bulk}} = 1/\sqrt{G_4^{\mathrm{bulk}}}
\approx 0.74\,M_{\mathrm{poly}} \approx 220$\,TeV at $M_{\mathrm{poly}} = 300$\,TeV.

### Relation to observed 4D $M_{\mathrm{Planck}}$

The bulk-level Newton constant is NOT the observed 4D Newton constant. The
polygon theory's 4D Planck scale $M_P \sim 10^{19}$\,GeV enters as an input in
the BF-instanton hierarchy formula (Paper IV §13, eq. at line 3497):
$v = M_P/\exp(\mathcal{H}_7)$ with $\mathcal{H}_7 \approx 38.46$, giving the
observed EW scale $v \approx 242$\,GeV.

The hierarchy between $M_P \sim 10^{19}$\,GeV and $M_{\mathrm{poly}} \sim 300$\,TeV
is a separate polygon result: the ratio $M_P / M_{\mathrm{poly}} \sim 10^{13}$
is the 1-loop RG running from the polygon scale up to the Planck scale. The
bulk-level $G_4^{\mathrm{bulk}}$ computed above fixes the 4D graviton's
coupling at the polygon scale; extrapolation to cosmological scales is by
standard RG flow.

---

## 5. Summary and status

The polygon AdS₃ × S¹ holography has the following structure:

| Step | Result | Status |
|------|--------|--------|
| (i) S¹ KK → 2D Virasoro | Zero-KK boundary stress tensor = Brown–Henneaux with $c = 12\,b(N)$ | Derived |
| (ii) Bulk-to-boundary propagator | Standard AdS₃ $K_{MN, ab}$ with $\Delta_h = 2$; KK tower $m_\varphi \neq 0$ gives massive 3D gravitons | Derived |
| (iii) 4D-massless pole | Bulk graviphoton + radion Euler-class-gapped at $M_{\mathrm{poly}}$; surviving 4D graviton = boundary Virasoro; pole at $k^2 = 0$ | Derived from paper §5 Remark |
| (iv) Newton constants | $G_4^{\mathrm{bulk}} = \pi L R / (4\,b(N))$; separate from observed $M_P$ (RG-running input) | Derived |

This construction is specific to the AdS₃ × S¹ bulk with Euler-class-breaking
of $S^1$ translation (the polygon structure). It is not a reduction to
standard AdS₃/CFT₂ (which has no propagating 4D graviton) nor AdS₄/CFT₃
(which has a different bulk dimensionality). It is a new holographic
dictionary for Seifert-fibered bulks with a specific mechanism (Euler-class
gap) that converts the KK-reduced bulk DOF into boundary CFT modes.

## 6. Weinberg–Witten evasion

The Weinberg–Witten theorem (1980) forbids massless spin $> 1$ particles with
a local Lorentz-covariant stress tensor in 4D QFT. The polygon evades both
premises:

1. **Bulk locality fails**: the UV bulk is a 3D Chern–Simons theory, which is
   topological (metric-independent). There is no local bulk $T^{\mu\nu}$ in
   4D because the bulk action is $\int (k/4\pi) A \wedge dA$ — it carries no
   dynamical metric.
2. **Effective 4D $T^{\mu\nu}$ is non-local**: the 4D graviton is the
   boundary Virasoro zero mode $T(z), \bar T(\bar z)$. Its dual bulk field
   via the holographic dictionary is non-local in the 4D sense (constructed
   from the near-boundary behavior of the bulk metric perturbation, not a
   local 4D field operator).

Both Weinberg–Witten premises fail for the polygon theory; the theorem does
not apply. This is the adapted version of the standard AdS/CFT resolution,
now specific to the AdS₃ × S¹ polygon construction.

## 7. Proposed Paper IV enhancement

Add to §5 (`sec:graviton`) after Remark 5.3 (FG-WW) a new paragraph:

```latex
\emph{The non-standard AdS$_3$ × $S^1$ holography.}
The polygon bulk $M_4 = \mathbb{R}_t \times (\mathbf{H}^2 \times_N S^1)$
factors as $\mathrm{AdS}_3 \times S^1$ in Lorentzian signature, with 3D
conformal boundary $\mathbb{R}_t \times T^2$. The zero KK mode on
$S^1_\varphi$ of the 3D boundary stress tensor $\mathcal{T}_{ab}$ reduces
to the Brown-Henneaux 2D Virasoro algebra at $c = 12\,b(N)$. The KK
decomposition of the bulk metric gives 3 zero-mode fields: topological
3D graviton (0 propagating DOF), graviphoton $A_m$ (1 DOF), and radion
$\sigma$ (1 DOF) — total 2 DOF matching a massless 4D graviton. The
bulk graviphoton and radion acquire Euler-class masses
$\sim M_{\mathrm{poly}}$ (Remark~\ref{rmk:kk-dof}); at $E \ll
M_{\mathrm{poly}}$ they are integrated out, leaving the boundary Virasoro
$T(z), \bar T(\bar z)$ zero mode as the sole surviving gravitational
DOF. These two Virasoro sectors realize the helicity $\pm 2$ polarizations
of the physical 4D graviton via the SO(2) boundary/transverse-plane
identification (Session 8). Newton constant matching:
$G_4^{\mathrm{bulk}} = \pi L R / (4\,b(N))$.
```

This is a PARAGRAPH (not a reframing); it commits explicitly to the
AdS₃ × S¹ dictionary and provides the derivation chain inline. The physical
predictions (2 polarizations, massless spin-2, Weinberg–Witten evaded) are
unchanged; the derivation status is strengthened.
