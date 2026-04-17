# Session 7 — LOW priority rigor items

**⚠ PARTIALLY SUPERSEDED**: the 4D-graviton SO(2) identification
(Item 2 below) is superseded by:
- `session08-graviton-rigor/derivation.md` (full SO(2) + Fourier derivation)
- `session11-ads3-s1-holography/derivation.md` (authoritative holographic dictionary)

The $\sin^2\theta_W$ running discussion (Item 1) remains current.

**Date**: 2026-04-17
**Scope**: finish the two LOW-priority reviewer items from
`session01-joint-P1-M1-fermion-dictionary/REVIEWER_FEEDBACK.md`:
  1. Honest $\sin^2\theta_W$ running language (current)
  2. 4D graviton KK lift — explicit boundary-SO(2) ↔ 4D transverse-SO(2)
     construction (SUPERSEDED by 08/11)

---

## Item 1: $\sin^2\theta_W$ running language

### Status

**Already honest in Paper IV.** The reviewer's concern
> "sin²θ_W at M_Z is 3.9% off (0.240 predicted vs 0.231 observed) —
> not a 'confirmed prediction' as might be claimed"

is addressed by the paper as written. Two relevant passages:

**Paper IV §13 (`sec:electroweak-couplings`), lines 2236-2248:**
> "Below the polygon scale the theory flows to the 4D SM, and 3/11
> becomes the boundary condition for the standard RG running (one-loop,
> $b_1 = 41/10$, $b_2 = -19/6$), which brings it to
> $\sin^2\theta_W(M_Z) = 0.231$, matching the measured value 0.2312 to
> 0.1%. This determines $M_{\mathrm{poly}} \approx 300\,\mathrm{TeV}$:
> a consistency check (the running must land in the 50–500 TeV window)."

**Paper IV Proposition (sensitivity table), lines 2640-2650:**
> "The tree-level prediction $\sin^2\theta_W = 3/11$ matches the
> experimental 0.2312 at $M_Z$ via standard SM running for
> $M_{\mathrm{poly}} \approx 300\,\mathrm{TeV}$... At $M_{\mathrm{poly}}
> = 50$ TeV the prediction is $\sin^2\theta_W(M_Z) = 0.240$ (3.9% above
> experiment); $O(1)$ threshold corrections at the polygon scale
> accommodate the 50–500 TeV range."

### Assessment

The paper states: (a) 3/11 is the \emph{tree-level} polygon prediction
at the polygon scale, not at $M_Z$; (b) standard SM 1-loop running
brings it to 0.231 \emph{if} $M_{\mathrm{poly}} \approx 300$ TeV; (c)
the 3.9% discrepancy at $M_{\mathrm{poly}} = 50$ TeV is explicitly
noted. This is honest by the reviewer's standard.

**Action**: no paper change required. If anything needs strengthening,
it is a single phrase elsewhere in the paper; we flag no specific edit.

---

## Item 2: 4D graviton KK lift — explicit SO(2) identification

### Reviewer concern

> 4D graviton KK lift: "boundary SO(2) = 4D transverse SO(2)" is
> asserted, not constructed. Standard AdS$_3$/CFT$_2$ gives 3D
> graviton; 4D uplift via $S^1$ fiber is non-standard and
> under-developed.

### Paper IV §5 current state

Lines 461–525 (Derivation~\ref{thm:graviton-4d}) carry the four-step
derivation. The helicity identification appears at lines 486–498:
> "$T(z)$ has conformal weight $(2, 0)$, so under the SO(2) rotation
> $z \to e^{i\alpha}z$ it transforms as $T(z) \to e^{2i\alpha}\,T(z)$.
> The eigenvalue $e^{2i\alpha}$ under SO(2) is the definition of
> helicity $+2$ for the massless little group in four dimensions."

The missing step is making explicit \emph{which} SO(2) at the boundary
equals \emph{which} SO(2) in the 4D Lorentz little group. The
construction follows.

### Explicit construction

**Setup.** The bulk 4D spacetime is
$M_4 = \mathbb{R}_t \times (\mathbf{H}^2 \times_N S^1)$
with coordinates $(t, \rho, \theta, \varphi)$ where $\rho$ is the
$\mathbf{H}^2$ radial coordinate, $\theta$ its angular coordinate, and
$\varphi$ the $S^1$ fiber coordinate of period $2\pi/N$. The conformal
boundary is $\partial M_4 = \mathbb{R}_t \times \partial\mathbf{H}^2
\times_N S^1 \cong \mathbb{R}_t \times T^2$, with boundary torus
coordinates $(\theta, \varphi)$.

**Step A (4D massless little group).** A massless quantum in 4D has
momentum $p^\mu = (E, 0, 0, E)$ in a suitable frame (say the momentum
aligned with bulk radial direction $\partial_\rho$ at large $\rho$).
Its little group is SO(2), acting on the 2-plane transverse to~$p$:
$\mathrm{span}\{\partial_\theta, \partial_\varphi\}$ at the boundary,
with rotation
\begin{equation*}
  R_\alpha\colon\;
  \begin{pmatrix}\theta\\\varphi\end{pmatrix}
  \mapsto
  \begin{pmatrix}\cos\alpha & -\sin\alpha \\ \sin\alpha & \cos\alpha\end{pmatrix}
  \begin{pmatrix}\theta\\\varphi\end{pmatrix}.
\end{equation*}
This is the standard massless helicity little group
(Weinberg QFT Vol.~1, §2.5).

**Step B (boundary SO(2)).** At low energies $E \ll M_{\mathrm{poly}}$
the boundary torus $T^2 = S^1_\theta \times S^1_\varphi$ is
approximated by the Euclidean plane $\mathbb{R}^2$ (paper lines
475–485): both circles have wavelength $\gg 1/E$, so local metric
corrections vanish to $O(E^2/M_{\mathrm{poly}}^2)$. Introduce the
complex boundary coordinate $z = \theta + i\varphi$ (flat limit). The
2D Euclidean rotation $z \to e^{i\alpha} z$ is precisely the boundary
SO(2) rotation of $T^2$ acting in the flat-limit.

**Step C (identification).** The rotation in Step~B is the SAME SO(2)
as the little-group rotation in Step~A:
\[
  R_\alpha(\theta, \varphi) = (\theta \cos\alpha - \varphi \sin\alpha,
  \theta \sin\alpha + \varphi \cos\alpha)
  \;\Longleftrightarrow\; z \mapsto e^{i\alpha} z.
\]
This identity is algebraic: the boundary torus is the transverse
2-plane of the radial momentum $p \propto \partial_\rho$, and its
rotation group in the flat limit is the unique SO(2) acting on that
plane, which is the 4D little group by definition. No independent
"uplift" is needed — at zero momentum the boundary SO(2) \emph{is} the
4D transverse SO(2) up to the controlled $O(E^2/M_{\mathrm{poly}}^2)$
correction quoted in the paper.

**Step D (helicity matching).** The stress tensor $T(z)$ has conformal
weight $(2, 0)$: by the defining property of conformal primaries,
$T(e^{i\alpha}z) (e^{i\alpha})^2 = T(z)$, i.e., $T$ transforms by the
phase $e^{2i\alpha}$ under $z \to e^{i\alpha}z$. Combined with
Step~C, this is the Weinberg helicity eigenvalue $e^{ih\alpha}$ with
$h = +2$. Likewise $\bar{T}(\bar z)$ transforms by $e^{-2i\alpha}$,
helicity $-2$.

**DOF count.** Two independent boundary operators ($T, \bar{T}$) give
two 4D helicity states ($+2, -2$), matching the $d(d-3)/2 = 2$ physical
polarizations of a massless spin-2 field in 4D.

### Weinberg--Witten evasion

Weinberg--Witten (1980) forbids a massless spin $> 1$ particle with a
local Lorentz-covariant stress tensor in 4D QFT. In the polygon
theory:
1. The UV bulk is a 3D Chern--Simons topological theory; there is no
   local $T^{\mu\nu}$ in the bulk (the CS action is metric-independent).
2. The 4D effective $T^{\mu\nu}$ is defined by the holographic
   dictionary (Maldacena 1997, de~Haro--Solodukhin--Skenderis 2001),
   which is \emph{non-local} in the 4D sense.
Both Weinberg--Witten assumptions (locality and Lorentz-covariance in
the 4D bulk) fail, so the theorem does not apply. This is the
standard AdS/CFT resolution, adapted to the polygon setting by one
dimension.

### Status

**Resolved.** Steps A–D make the boundary-SO(2) ↔ 4D-transverse-SO(2)
identification explicit. The construction is rigorous in the
effective-field-theory sense with controlled
$O(E^2/M_{\mathrm{poly}}^2)$ corrections; the Weinberg--Witten evasion
is justified.

### Proposed paper enhancement (optional)

Add a short paragraph after line 495 of `paper-4-field-theory/main.tex`,
inside the proof of Derivation~\ref{thm:graviton-4d}:

```latex
\emph{Explicit SO(2) identification.}
In the frame where the massless graviton has $4$D momentum
$p^\mu \propto \partial_\rho$ (radial from the bulk), the little-group
transverse $2$-plane is $\mathrm{span}\{\partial_\theta,
\partial_\varphi\}$. At low energies $E \ll M_{\mathrm{poly}}$ this
coincides with the boundary $T^2$ up to $O(E^2/M_{\mathrm{poly}}^2)$
(as shown above), and the boundary complex coordinate $z = \theta + i\varphi$
parametrizes the flat-limit plane. The rotation $z \mapsto e^{i\alpha}z$
is simultaneously the boundary torus $\mathrm{SO}(2)$ and the $4$D
transverse $\mathrm{SO}(2)$ little-group element; the identification is
algebraic, not an extra postulate.
```

No structural change to the paper; this is an exposition strengthening.

---

## Summary

| Item | Resolution |
|------|-----------|
| Honest $\sin^2\theta_W$ running | Paper IV already honest (lines 2236-2248, 2640-2650); no change. |
| 4D graviton boundary SO(2) ↔ 4D transverse SO(2) | Explicit construction above; optional paper-text strengthening in proof of `thm:graviton-4d`. |

Both LOW items resolved. Rigor pass complete across HIGH + MEDIUM + LOW.
