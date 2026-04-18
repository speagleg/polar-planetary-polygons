# Session 63 — Polygon-internal inflaton search beyond Session 47

**Date**: 2026-04-18
**Goal**: Using Session 54's explicit parent CFT construction
$\mathcal{X}_N = \mathcal{L}_{Q(N)}\otimes\mathrm{PF}(N,1)$, identify a
polygon-internal inflaton candidate beyond the four ruled out in
Session 47 (breathing, large-$\xi$ Higgs, Starobinsky, Anber–Sorbo).
Four new candidates (C7 Liouville scalar; C8 parafermion mode;
C9 radion+breathing composite; C10 chaotic-Liouville inflation) are
surveyed. The load-bearing case is C7/C10 (they coincide in bulk).

---

## 0. Bottom line

**NONE of C7–C10 gives viable inflation at load-bearing $N\in\{5,6,7,11\}$.**

The Liouville-sector inflaton (C7 $\equiv$ C10 in bulk) produces a
*pure exponential* 4D potential whose slow-roll parameters are fixed
by the Liouville coupling $\beta_-(N)$, which in turn is fixed by the
central charge $c_L(N)=12\,b(N)-2(N-1)/(N+1)$. At $N=11$ (the
cosmologically load-bearing case, Paper VI §CC-instanton) the
prediction is

$$
n_s(11) = 0.785, \qquad r(11) = 1.72,
$$

versus Planck 2018 $n_s=0.9665\pm 0.0038$ and BICEP/Keck 2021 $r<0.036$:
$n_s$ is off by $-47.8\,\sigma$, $r$ is $48\times$ the upper bound.

**Candidates C8 and C9 fail trivially** (parafermion gives a finite
massive Klein–Gordon tower, no exponential slope; off-diagonal
Ferrara–Kounnas kinetic mixing cannot create new critical points of
$V$). Details in §5–6.

The Liouville slope $\lambda(N)=2\beta_-(N)$ is a *monotone-decreasing*
function of $N$; the Planck tilt $n_s=0.9665$ would require
$\lambda\approx 0.183$, i.e.\ $N\approx 26$, which lies outside the
load-bearing polygon set. Even at $N=26$ the tensor ratio $r\approx 0.28$
still exceeds the BICEP/Keck bound by $\sim 8\times$. **No load-bearing
polygon value produces observed inflation**.

Session 47's conclusion (companion sector required) is re-confirmed
under the Session 54 parent CFT. Gap 1 (parent CFT) does not open
a new inflation channel. **The framework remains agnostic to the
inflation sector.** No paper edits are required beyond those already
identified in Session 47 §9.

---

## 1. Candidate C7: Liouville-sector inflaton

### 1.1 2D boundary action

From Session 54 §2.1, the Liouville factor in the parent CFT has
worldsheet action

$$
S_L[\varphi]=\frac{1}{4\pi}\int_\Sigma d^2z\,\sqrt{\hat g}\,
\bigl(\hat g^{ab}\partial_a\varphi\,\partial_b\varphi
      + Q(N)\,\hat R\,\varphi + 4\pi\mu\, e^{2\beta\varphi}\bigr),
$$

with $Q(N)=\beta+1/\beta$ and $c_L=1+6Q(N)^2=12b(N)-2(N-1)/(N+1)$.
Two roots of $\beta^2-Q\beta+1=0$: the small root $\beta_-(N)$
(semiclassical / weak-coupling) and the large dual $\beta_+=1/\beta_-$.
Session 54 §8 (verified numerically):

| $N$ | $c_L(N)$ | $Q(N)$ | $\beta_-(N)$ |
|-----|----------|--------|-----|
| 5   | 25.177   | 2.007  | 0.918 |
| 6   | 36.554   | 2.434  | 0.523 |
| 7   | 50.074   | 2.860  | 0.408 |
| 11  | 124.893  | 4.544  | 0.232 |

### 1.2 Bulk uplift via dS/CFT (Strominger 2001)

Under the dS$_3$/CFT$_2$ dictionary (Strominger, *JHEP* 0110:034,
2001; also applied by Silverstein et al.\ 2007–2012 in Liouville
inflation), a 2D Liouville field with coupling $\beta$ maps to a
4D bulk scalar $\phi_I$ with canonically normalized kinetic term
and potential

$$
V(\phi_I)\;=\;V_0\,e^{-\lambda\,\phi_I/M_P},
\qquad \lambda = 2\beta_-(N),
$$

(taking the semiclassical root; the large root gives an equivalent
rolling tachyon by FZZ duality). The prefactor $V_0$ is fixed by the
3D cosmological constant lift; it sets the inflationary energy scale
but not $n_s$ or $r$. The exponential slope $\lambda$ is the unique
dimensionless coupling inherited from the Liouville background
charge; it is invariant under the bulk canonical-normalization rescale
(exponential slopes are scale-invariant).

### 1.3 4D effective action

At $N=11$ (load-bearing, Paper VI §CC-instanton):

$$
S_{\mathrm{eff}}^{(N=11)}
=\int d^4x\sqrt{-g}\,\Bigl[\tfrac{M_P^2}{2}R
   - \tfrac{1}{2}(\partial\phi_I)^2 - V_0\,e^{-0.464\,\phi_I/M_P}\Bigr].
$$

### 1.4 Slow-roll parameters (exponential / power-law inflation)

For $V=V_0\exp(-\lambda\phi_I/M_P)$, standard results:

$$
\epsilon = \frac{M_P^2}{2}\Bigl(\frac{V'}{V}\Bigr)^2 = \frac{\lambda^2}{2},
\quad
\eta = M_P^2\,\frac{V''}{V} = \lambda^2.
$$

Both constants; slow-roll does not terminate unless $\lambda^2>1$
(graceful-exit problem in pure exponentials). Scale-invariant scalar
tilt and tensor-to-scalar ratio:

$$
n_s = 1+2\eta-6\epsilon = 1-\lambda^2,
\qquad
r = 16\epsilon = 8\lambda^2.
$$

### 1.5 Numerical predictions

For each load-bearing $N$:

| $N$ | $\beta_-$ | $\lambda=2\beta_-$ | $n_s=1-\lambda^2$ | $r=8\lambda^2$ | $(n_s-0.9665)/0.0038$ | $r/0.036$ |
|-----|-----------|------|------|------|---------|------|
| 5   | 0.918     | 1.836 | $-2.37$ | 26.95 | $-878\,\sigma$ | $749\times$ |
| 6   | 0.523     | 1.047 | $-0.10$ | 8.76  | $-279\,\sigma$ | $244\times$ |
| 7   | 0.408     | 0.816 | $+0.33$ | 5.32  | $-166\,\sigma$ | $148\times$ |
| 11  | 0.232     | 0.464 | $+0.78$ | 1.72  | $-47.8\,\sigma$ | $48\times$ |

**All load-bearing $N$ miss Planck 2018 by tens to hundreds of
sigma on $n_s$, and exceed the BICEP/Keck 2021 bound $r<0.036$ by
factors of $48$ to $749$.**

Asymptotic limit: $\beta_-\sim 1/Q$ as $N\to\infty$, hence
$\lambda\sim 2/Q$, $n_s\to 1^-$ and $r\to 0^+$. The *right* tilt
would need $\lambda\approx 0.183$, i.e.\ $Q\approx 10.9$, i.e.\
$c_L\approx 727$, i.e.\ $b(N)\approx 60.6$, i.e.\ $N\approx 26$.
**This $N$ is not in the load-bearing polygon spectrum.**

Even at hypothetical $N=26$, the tensor ratio $r=0.28$ still
violates BICEP/Keck by $\sim 8\times$. The exponential inflation
$r=8(1-n_s)$ scaling predicts $r=0.27$ for $n_s=0.9665$, which was
decisively ruled out by BICEP/Keck 2014–2018 (Planck Collab.\
2018 §4.4; see also the "power-law inflation excluded" contour in
Planck 2018 X §5.5).

### 1.6 Verdict on C7/C10

**FAIL (quantitatively, at all load-bearing $N$).** Polygon-driven
Liouville inflation produces power-law $a(t)\propto t^p$ with
$p=2/\lambda^2(N)$, and the scaling $r=8(1-n_s)$ is categorically
excluded by the joint $(n_s,r)$ constraint. No accessible parameter
reaches the Planck/BICEP region.

---

## 2. Candidate C8: Parafermion-sector inflaton

### 2.1 Parafermion primary spectrum

From Session 54 §2.2, $\mathrm{PF}(N,1)$ has primaries $\phi^{\ell}_m$
with conformal weight

$$
h(\ell,m) = \frac{\ell(\ell+2)}{4(N+2)} - \frac{m^2}{4N},
\qquad \ell\in\{0,\dots,N-1\},\ |m|\le\ell,\ \ell+m\in 2\mathbb{Z}.
$$

This is a **finite set** of Virasoro primaries — $\tfrac{1}{2}N(N-1)$
states — with discrete weights.

### 2.2 Bulk dual

Via standard AdS$_3$/CFT$_2$ + KK on $S^1_\varphi$ (Session 53 §§2–3),
each boundary primary of weight $(h,\bar h)$ with $\Delta=h+\bar h$
lifts to a bulk scalar with mass

$$
m^2_\Delta L^2 = \Delta(\Delta-2).
$$

Crucially, the bulk dual of a parafermion primary is a **Klein–Gordon
field with quadratic potential** $V=\tfrac12 m^2\phi^2$ — it is
*not* an exponential. The potential arises from the mass term alone
because parafermion primaries have no exponential dressing (unlike
Liouville's $e^{2\beta\varphi}$).

### 2.3 Verdict

**FAIL (structurally).** A finite tower of massive Klein–Gordon
scalars has at most quadratic potentials. The only candidate slow-roll
regime of $V=\tfrac12 m^2\phi^2$ is chaotic inflation at $\phi\gg M_P$,
which is itself ruled out by Planck/BICEP ($r\approx 0.13$ at
$n_s=0.967$; cf.\ Planck 2018 Inflation Fig.\ 8). Furthermore, there
is no mechanism in the polygon framework to boost a specific
parafermion field above $M_P$. Candidate C8 offers no new slow-roll
region not already excluded.

---

## 3. Candidate C9: Radion + breathing composite

### 3.1 Field-space geometry

Two-field inflation with $(\sigma,\rho)$ can in principle exhibit
slow-roll along a non-gradient trajectory if the Ferrara–Kounnas
kinetic matrix has off-diagonal components. However:

(i) The **critical-point structure of $V(\sigma,\rho)$ is invariant
under any field redefinition**, including the switch from
canonical to off-diagonal kinetic terms. $V$ still has its minimum
at the AdS$_4$ locus (Session 51) and its saddle at
$V_\star=0$ (Session 18); no new plateaus are created.

(ii) Slow-roll along a **valley** requires $V$ itself to be nearly
flat somewhere. The polygon $V(\sigma,\rho)$ has no such
near-flat region: the radion sector is locked at FR scale, and
the breathing mode is strictly concave (Session 47 §2.2).

(iii) The off-diagonal Ferrara–Kounnas coefficient, computed in
Session 39 for the $N=11$ two-modulus model, is $|g_{\sigma\rho}|
\lesssim 0.1$; too small to substantially redirect the inflationary
trajectory.

### 3.2 Verdict

**FAIL.** No new inflationary phase emerges from radion–breathing
coupling; the critical structure of $V$ is topologically fixed.

---

## 4. Candidate C10: Chaotic Liouville inflation

Silverstein–Westphal 2008 ("Monodromy in the CMB") and related
"chaotic Liouville" constructions use a 4D scalar with
*monodromy-extended* linear potential $V=\mu^3\phi$. This is NOT
the polygon Liouville: the polygon's Liouville is a 2D worldsheet
CFT uplifted to a 4D bulk *exponential* potential (C7 above).
Chaotic Liouville inflation assumes an *axion-monodromy* origin
for the linear potential, which requires a large-$f$ axion — absent
from the polygon spectrum (Paper IV line 1734, cf.\ Session 47 §5.3).

C10 collapses onto C7 in the polygon context and is not an independent
candidate. **FAIL by the same argument as C7.**

---

## 5. Summary table

| Candidate | Potential | Failure mode | Section |
|-----------|-----------|--------------|---------|
| C7 Liouville (bulk dual) | $V_0\,e^{-\lambda\phi/M_P},\ \lambda=2\beta_-(N)$ | $n_s,r$ fail by tens of $\sigma$; power-law inflation ruled out by joint Planck+BICEP | §1 |
| C8 Parafermion primary | $\tfrac12 m^2\phi^2$ (Klein–Gordon) | Only chaotic $m^2\phi^2$ regime, already excluded | §2 |
| C9 Radion+breathing | AdS$_4$-locked with concave ridge | No flat direction; topological | §3 |
| C10 Chaotic Liouville | Same $V_0 e^{-\lambda\phi/M_P}$ as C7 | Collapses to C7; no axion-monodromy in framework | §4 |

---

## 6. Conclusion

Session 54's explicit parent CFT does **not** supply a polygon-internal
inflaton. The Liouville factor $\mathcal{L}_{Q(N)}$, although
concrete and modular-invariant, inherits a fixed exponential slope
$\lambda(N)=2\beta_-(N)$ whose value at all load-bearing $N$ places
the resulting 4D cosmology deep in the power-law-inflation region
excluded by Planck 2018 + BICEP/Keck 2021 jointly. The parafermion
factor $\mathrm{PF}(N,1)$ supplies only a finite Klein–Gordon tower,
contributing no exponential or plateau structure. The radion-breathing
composite field space is topologically rigid.

This session therefore **confirms and sharpens Session 47's C6
conclusion**: the polygon framework requires an external
companion inflation sector. The new input from Session 54 is that
the obstruction is now *explicitly* quantified: not just "no
identified candidate" (Session 47 §7), but rather "the unique
candidate enabled by the parent-CFT construction misses Planck/BICEP
by an order of magnitude in the power-law plane at every
load-bearing $N$".

**Quantitative wall**: Liouville slope $\lambda(11)=0.464$ vs
required $\lambda\approx 0.183$; the required $N\approx 26$ lies
outside the load-bearing polygon set $\{5,6,7,11\}$, and even at
$N=26$ the tensor ratio $r\approx 0.28$ fails BICEP/Keck by $\sim 8\times$.

**No paper edits** beyond those already in Session 47 §9 are required.
The Paper VI correction continues to read "companion inflation sector
required"; Session 63 adds a footnote reference to the explicit
Liouville-inflaton exclusion.

---

## 7. Code verification

```python
import math

def bN(N):
    return N*(N+1)/12 - math.log(2) + math.log(N)/(N-1)

def liouville_inflation(N):
    b = bN(N)
    c_total = 12*b
    c_pf = 2*(N-1)/(N+1)
    c_L = c_total - c_pf
    Q = math.sqrt((c_L - 1)/6)
    beta_minus = (Q - math.sqrt(Q*Q - 4))/2
    lam = 2*beta_minus
    n_s = 1 - lam**2
    r = 8*lam**2
    return dict(N=N, c_L=c_L, Q=Q, beta=beta_minus, lam=lam,
                n_s=n_s, r=r,
                sigma_ns=(n_s - 0.9665)/0.0038,
                r_ratio=r/0.036)

for N in [5, 6, 7, 11]:
    d = liouville_inflation(N)
    print(f"N={d['N']:2d}: lam={d['lam']:.4f}  n_s={d['n_s']:+.4f}  "
          f"r={d['r']:.3f}  {d['sigma_ns']:+7.1f} sigma  "
          f"r/r_max={d['r_ratio']:.1f}x")

# Output:
#   N= 5: lam=1.8355  n_s=-2.3691  r=26.953   -877.8 sigma  r/r_max=748.7x
#   N= 6: lam=1.0466  n_s=-0.0953  r=8.763    -279.4 sigma  r/r_max=243.4x
#   N= 7: lam=0.8156  n_s=+0.3347  r=5.322    -166.3 sigma  r/r_max=147.8x
#   N=11: lam=0.4638  n_s=+0.7849  r=1.721     -47.8 sigma  r/r_max= 47.8x
```

Verified: all four load-bearing $N$ values fail both Planck and
BICEP/Keck bounds catastrophically.

---

## 8. References

- Silverstein, E.; Westphal, A. (2008). "Monodromy in the CMB."
  *Phys. Rev. D* 78, 106003.
- Silverstein, E. (2013). "Les Houches lectures on inflationary
  observables and string theory." arXiv:1311.2312.
- Strominger, A. (2001). "The dS/CFT correspondence."
  *JHEP* 0110:034.
- McAllister, L.; Silverstein, E.; Westphal, A. (2010). "Gravity
  waves and linear inflation from axion monodromy."
  *Phys. Rev. D* 82, 046003.
- Planck Collaboration (2018). "Planck 2018 X. Constraints on
  inflation." *Astron. Astrophys.* 641, A10.
- BICEP/Keck Collaboration (2021). "Improved constraints on
  primordial gravitational waves using Planck, WMAP, and BICEP/Keck
  observations through the 2018 observing season." *Phys. Rev.
  Lett.* 127, 151301.
- Session 47 (this project): inflaton sector identification
  (C1–C6 ruled out).
- Session 54 (this project): parent CFT
  $\mathcal{L}_{Q(N)}\otimes\mathrm{PF}(N,1)$ construction.
- Session 53: 4D graviton on AdS$_3\times S^1$ (bulk dictionary
  conventions).

---

## 9. Status table

| Claim | Status | Where |
|-------|--------|-------|
| C7 Liouville inflaton $n_s, r$ at $N=11$ | COMPUTED: $(0.785, 1.72)$ | §1.5 |
| C7 fails Planck $n_s$ by $-47.8\sigma$ | DERIVED | §1.5 |
| C7 fails BICEP/Keck $r$ by $48\times$ | DERIVED | §1.5 |
| C7 power-law $r=8(1-n_s)$ scaling excluded | DERIVED (cf. Planck 2018 §5.5) | §1.6 |
| C8 parafermion gives Klein–Gordon tower only | STRUCTURAL | §2 |
| C9 composite has no flat direction | STRUCTURAL (topological) | §3 |
| C10 = C7 in bulk | IDENTIFIED | §4 |
| Required $N\approx 26$ outside load-bearing set | DERIVED | §1.5 |
| Session 47 companion-sector conclusion | RE-CONFIRMED, sharpened | §6 |
| Paper edits required | NONE beyond Session 47 §9 | §6 |
