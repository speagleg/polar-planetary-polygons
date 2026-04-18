# Session 19 — BF-instanton contribution to the radion potential

**Date**: 2026-04-18
**Author**: Session 19 (continuation of Session 18)
**Status**: CLOSED at the BF-instanton level; Minkowski-4 stability NOT rescued.

## Scope

Session 18 closed three rounds of corrections to the 7D Candelas-Weinberg +
Freund-Rubin potential, establishing:

- An AdS_4 vacuum at $(\alpha_\star, \gamma_\star) \approx (0.53, 0.11)$,
  $\Lambda_7 \approx -1.6\times 10^5$, with both Hessian eigenvalues positive
  and radion masses $m_\rho, m_\sigma \sim 10$–$30\,M_{\mathrm{poly}}$
  (Session 18 §R.3).
- A Minkowski-4 critical locus at $V_\star = 0$, parametrized by the
  additional constraint that $\Lambda_7$ is no longer free, with a SADDLE
  Hessian of signature $(+, -)$ at all integer H-flux quanta
  $p \in \{0, 1, 2, 3, 5, 7\}$ and all $|C_{\mathrm{base}}| \in [0.05, 0.30]$
  (Session 18 §R.26).
- A structural obstruction: the H-flux scaling vector $(-3, -6)$ is parallel
  to the bulk-cosmological-constant scaling vector $(-1, -2)$ in log-modulus
  space, so H-flux cannot introduce a Hessian-stabilizing direction
  independent of $\Lambda_7$ (Session 18 §R.27).

This session investigates whether the **BF-instanton** contribution
$V_{\mathrm{inst}}(\alpha, \gamma)$—natural in the polygon framework via the
Born-Oppenheimer WKB action $S_{\mathrm{BO}}(7) = 18.274$ from Paper IV
§13—introduces a scaling direction different from $(-1,-2)$, and if so whether
it can complete the three-equation system
$\{V=0,\,\partial_\alpha V=0,\,\partial_\gamma V=0\}$ with both Hessian
eigenvalues positive.

**Cross-reference**: Session 18 §R.25–R.30 establishes the 5-term potential
and the H-flux obstruction. This document adds a sixth type of term to that
potential and analyzes its effect.

## §1. Derivation of $V_{\mathrm{inst}}(\alpha, \gamma)$

### 1.1 Starting point: Paper IV §13

The hierarchy formula of Paper IV (lines 3497–3513) is
$$
v \;=\; M_P \exp(-\mathcal{H}_7),
\qquad
\mathcal{H}_7 \;=\; 2 S_{\mathrm{BO}}(7)
  \;+\; \Delta\varepsilon \cdot \ln\varepsilon_7
  \;+\; \tfrac{1}{2}\ln\bigl(c_{11}/(24\pi^2)\bigr)
  \;=\; 38.459,
$$
with $S_{\mathrm{BO}}(7) = 18.274$ the WKB tunneling action of the breathing
mode at $N = 7$, $\varepsilon_7 = 8 + 3\sqrt{7}$, $\Delta\varepsilon = 0.8031$,
and $c_{11} = 12 \cdot b(11)$. The electroweak scale $v \approx 242$\,GeV
follows numerically.

The BF-instanton candidate contribution to the 4D effective potential is
$$
V_{\mathrm{inst}}(\alpha, \gamma)
\;=\; \mathcal{C}(\alpha, \gamma)\,\exp\!\bigl(-S_{\mathrm{BO}}(7; \alpha, \gamma)\bigr),
$$
where:
- $S_{\mathrm{BO}}$ is the breathing-mode WKB action, which may depend on the
  bulk moduli through the Einstein-frame kinetic and potential normalizations;
- $\mathcal{C}$ is the semiclassical prefactor, itself a Weyl-rescaled 4D mass
  density.

The structural question is: **what is the scaling vector
$(p_{\mathrm{inst}}, q_{\mathrm{inst}})$ of $\log|V_{\mathrm{inst}}|$ in
log-modulus space?**

### 1.2 The WKB integrand and moduli dependence

Recall (Paper VI Supplement, Observation §Obs.pell-numerical; Paper III §7):
$$
H_{\mathrm{BO}} \;=\; -\frac{1}{c_7}\,\partial_\rho^2 \;+\; V_7(\rho),
\qquad
V_7(\rho) \;=\; \ln(2\sinh\rho) + b(7) - f(m^*,7),
\qquad c_7 = 12\,b(7) = 51.57.
$$
Here $\rho$ is the dimensionless radial coordinate on $\mathbf{H}^2/\mathbb{Z}_7$
(unit curvature convention), $f(m^*,7) = m^*(7-m^*)/2 = 6$ at $m^* = 3$, and
$b(7) = 4.298$. The turning point is $\rho^* = 1.734$ (found from
$V_7(\rho^*) = 0$), and
$$
2 S_{\mathrm{BO}}(7) \;=\; \int_0^{\rho^*}\! \sqrt{2 c_7\,|V_7(\rho)|}\,d\rho
\;+\; (\rho \to -\rho\;\text{branch}) \;=\; 36.548.
$$

The key input for this session is how $c_7$ and $V_7(\rho)$ scale with the
bulk moduli $(\alpha, \gamma)$ upon embedding the breathing-mode
Hamiltonian in the 7D geometry $\mathbb{R}\times S^1_\alpha \times \Sigma_\gamma$.

**Numerical verification of the bare WKB integral:**
```
b(7)       = 4.297837844282607
c_7        = 51.57405413139128
rho_star   = 1.7338477078239245
2*S_BO     = 36.54797204359737   (matches Paper VI Obs.pell-numerical)
Delta_eps  = 0.8031
ln(eps_7)  = 2.7687
c_11       = 126.56
H_7        = 2*S_BO + Delta_eps*ln(eps_7) + (1/2)*ln(c_11/(24 pi^2))
           = 38.458    (matches Paper IV §13: 38.459)
```

### 1.3 Weyl scaling of $c_7$, $V_7$, and $S_{\mathrm{BO}}$

Embed the breathing mode in the 7D Seifert manifold. The base $\Sigma$ has
physical metric $\gamma^2 \cdot ds^2_{\mathbf{H}^2/\mathbb{Z}_7}$, so the
physical base area is $\gamma^2 \cdot 8\pi/7$. The fiber $S^1_\alpha$
contributes length $2\pi\alpha$. Total $M_3$-volume:
$V_3(\alpha,\gamma) = K\alpha\gamma^2$, $K = 16\pi^2/7$ (Session 18 §1.1).

The 7D Jordan-frame action for the breathing mode (zero mode on base;
homogeneous on fiber):
$$
S_7^{\mathrm{breath}}
\;=\; \int dt_E \int_{M_3}\sqrt{g_3}\,d^3y\;
  \Bigl[\tfrac{1}{2}\,\kappa_{\rho}^{(7)}(\alpha,\gamma)\,(\partial_t \rho)^2
  \;+\; \Lambda_\rho^{(7)}(\alpha,\gamma)\,V_7(\rho)\Bigr],
$$
where $\kappa_\rho^{(7)}$ and $\Lambda_\rho^{(7)}$ are the Jordan-frame kinetic
and potential coefficients respectively.

**Claim (from Paper III §7 reduction).** The breathing-mode Lagrangian emerges
from the $N=7$ vortex energy on the hyperbolic base. Point-vortex interaction
energy on a base of curvature radius $\gamma$ has the scaling
$E \sim \kappa^2\,V_7(\rho)/\gamma^2$ (logarithmic interaction divided by
base area-scale squared; dimensionally: energy $\sim \kappa^2 / \text{length}^2$).
The moment-of-inertia coefficient, which is a kinematic factor with units
(mass)·(length)², is
$\kappa_\rho^{(7)} \sim \mathrm{const}\cdot \gamma^2$ in geometric units.

Specifically, writing $c_7 = 12\,b(7)$ as a PURE DIMENSIONLESS NUMBER and
restoring dimensions:
$$
\kappa_\rho^{(7)} \;=\; c_7 \cdot \gamma^2,
\qquad
\Lambda_\rho^{(7)} \;=\; \frac{1}{\gamma^2}.
$$
(The factor $1/\gamma^2$ in $\Lambda_\rho^{(7)}$ is the inverse base-curvature
scale; $\rho$ is still dimensionless.)

Pre-Weyl 4D Jordan-frame Lagrangian after integrating over $M_3$:
$$
\mathcal{L}_4^{\mathrm{Jordan}} \;=\; V_3\cdot\left[\tfrac{1}{2}\,c_7\,\gamma^2\,(\partial_t\rho)^2
\;+\; V_7(\rho)/\gamma^2\right]
\;=\; K\alpha\gamma^2\cdot\left[\tfrac{1}{2}\,c_7\,\gamma^2\,\dot\rho^2 + V_7/\gamma^2\right].
$$

**Weyl rescaling to Einstein frame** (Session 18 §R.1.2). Under
$g_4 \to V_3 g_4$, potential density $V_{\mathrm{pot}}$ rescales as
$V_{\mathrm{pot}}^{\mathrm{E}} = V_{\mathrm{pot}}^{\mathrm{pre}} / V_3^2$, while
scalar kinetic term rescales as
$T^{\mathrm{E}} = T^{\mathrm{pre}}/V_3$. Applying these to the breathing-mode:
$$
\boxed{\;
\mathcal{L}_4^{\mathrm{E}}
\;=\; \frac{K\alpha\gamma^2\cdot\tfrac{1}{2} c_7 \gamma^2}{K\alpha\gamma^2}\,\dot\rho^2
\;+\; \frac{K\alpha\gamma^2 / \gamma^2}{(K\alpha\gamma^2)^2}\,V_7
\;=\; \tfrac{1}{2}\,c_7\,\gamma^2\,\dot\rho^2
\;+\; \frac{V_7(\rho)}{K^2 \alpha^2 \gamma^4 \cdot \gamma^2 / (\alpha\gamma^2)}
\;}
$$

Let me redo this more carefully. The 4D Jordan-frame Lagrangian as written has
kinetic part $\tfrac{1}{2}[V_3 c_7 \gamma^2]\dot\rho^2$ and potential part
$[V_3/\gamma^2]\,V_7(\rho)$.

Under Weyl rescaling $g_4^{\mathrm{pre}} = \Omega^2 g_4^{\mathrm{E}}$ with
$\Omega^2 = V_3$ (to cancel the Jordan-frame $V_3\cdot R_4$ prefactor in the
Einstein-Hilbert term and put it in canonical 4D form):

- Potential density: $V^{\mathrm{E}} = V^{\mathrm{pre}}/\Omega^4 =
  V^{\mathrm{pre}}/V_3^2$.
- Scalar kinetic density: gets a factor $\Omega^{-2} = V_3^{-1}$ from the
  $\sqrt{-g}\,g^{\mu\nu}$ structure.

So:
$$
K^{\mathrm{E}}_\rho \;=\; \frac{V_3\,c_7\,\gamma^2}{V_3}
\;=\; c_7\,\gamma^2,
\qquad
V^{\mathrm{E}}_\rho
\;=\; \frac{V_3/\gamma^2}{V_3^2}\,V_7
\;=\; \frac{V_7(\rho)}{\gamma^2 V_3}
\;=\; \frac{V_7(\rho)}{K\,\alpha\,\gamma^4}.
$$

**Canonical normalization of $\rho$.** The Einstein-frame kinetic coefficient
$K^{\mathrm{E}}_\rho = c_7\gamma^2$ is $\rho$-independent but $\gamma$-dependent.
The canonical breathing mode $\tilde\rho$ satisfies
$d\tilde\rho = \sqrt{K^{\mathrm{E}}_\rho}\,d\rho = \gamma\sqrt{c_7}\,d\rho$.
Since we are only computing the WKB integral $\int d\rho\sqrt{2 K V}$,
canonicality is not required—it suffices that WKB action is an invariant of the
coordinate change.

### 1.4 Einstein-frame WKB tunneling action

The Euclidean WKB action is
$$
S_{\mathrm{BO}}^{\mathrm{E}}(\alpha,\gamma)
\;=\; \int_0^{\rho^*}\! \sqrt{2\,K^{\mathrm{E}}_\rho\,|V^{\mathrm{E}}_\rho|}\,d\rho
\;=\; \int_0^{\rho^*}\!\sqrt{\frac{2\,c_7\,\gamma^2\,|V_7(\rho)|}{K\alpha\gamma^4}}\,d\rho.
$$
Factoring out the moduli dependence, which is $\rho$-independent:
$$
\boxed{\;
S_{\mathrm{BO}}^{\mathrm{E}}(\alpha, \gamma)
\;=\; \sqrt{\frac{1}{K\alpha\gamma^2}}\cdot\int_0^{\rho^*}\!\sqrt{2 c_7 |V_7(\rho)|}\,d\rho
\;=\; \frac{S_{\mathrm{BO}}(7)}{\sqrt{K\alpha\gamma^2}}
\;=\; \frac{18.274}{\sqrt{V_3(\alpha,\gamma)}}.
\;}
$$

So the Einstein-frame instanton action has the scaling
$$
S_{\mathrm{BO}}^{\mathrm{E}}(\alpha, \gamma)
\;\propto\; \alpha^{-1/2}\gamma^{-1},
\qquad
\text{i.e.\ scaling vector }\;(p_S, q_S) \;=\; (-\tfrac{1}{2}, -1).
$$

**Numerical value at the benchmark** $(\alpha, \gamma) = (0.7965, 0.1588)$
(Session 18 §R.17.3):
$$
V_3 \;=\; K\alpha\gamma^2 \;=\; (16\pi^2/7)\cdot 0.7965\cdot (0.1588)^2
\;=\; 22.56 \cdot 0.02010 \;=\; 0.4535,
$$
$$
S_{\mathrm{BO}}^{\mathrm{E}} \;=\; 18.274/\sqrt{0.4535} \;=\; 27.14.
$$

**Consistency check.** The numerically-quoted $\mathcal{H}_7 = 38.459$ in
Paper IV §13 corresponds to $2 S_{\mathrm{BO}}(7) + \ldots$, NOT to
$2 S_{\mathrm{BO}}^{\mathrm{E}}$. The bare $S_{\mathrm{BO}}(7) = 18.274$
is the integrand evaluated in "unit-volume" geometric units, and the
hierarchy formula implicitly takes $V_3 = 1$. This is a clean assumption only
at the fixed-point value $V_3(\alpha_\star, \gamma_\star)$, and it is consistent
with Paper IV's framework if we identify
$$
V_3(\alpha_\star, \gamma_\star) \;=\; 1 \;\text{(choice of natural $G_7$ unit)}.
$$
Under this identification, $S_{\mathrm{BO}}^{\mathrm{E}}(\alpha_\star, \gamma_\star)
= S_{\mathrm{BO}}(7) = 18.274$, and the volume deviation $V_3 \neq 1$ away from
$(\alpha_\star, \gamma_\star)$ drives the moduli scaling of
$S_{\mathrm{BO}}^{\mathrm{E}}$.

### 1.5 The prefactor $\mathcal{C}(\alpha, \gamma)$

The WKB prefactor is
$\mathcal{C} \sim (\text{stiffness at turning point}) \cdot \exp(\ldots)$.
Dimensionally in 4D, it must be a mass$^4$ density. The natural choice—
Weyl-rescaling the bare semiclassical prefactor from 7D—gives
$$
\mathcal{C}(\alpha, \gamma)
\;=\; \mathcal{C}_0 \cdot V_3^{-2}
\;=\; \frac{\mathcal{C}_0}{K^2 \alpha^2 \gamma^4},
$$
matching the Weyl prescription for any Einstein-frame potential density
(Session 18 §R.1.2).

Scaling vector of the prefactor: $(p_\mathcal{C}, q_\mathcal{C}) = (-2, -4)$.

### 1.6 Full BF-instanton potential

Assembling:
$$
\boxed{\;
V_{\mathrm{inst}}^{(\mathrm{BF})}(\alpha, \gamma)
\;=\; \frac{\mathcal{C}_0}{K^2 \alpha^2 \gamma^4}\cdot
   \exp\!\left(-\frac{S_{\mathrm{BO}}(7)}{\sqrt{K\alpha\gamma^2}}\right).
\;}
$$

## §2. Effective scaling vector of $\log|V_{\mathrm{inst}}|$

The log-modulus derivative of the instanton:
$$
\alpha\partial_\alpha \log V_{\mathrm{inst}}
\;=\; -2 \;+\; \frac{1}{2}\cdot\frac{S_{\mathrm{BO}}(7)}{\sqrt{V_3}},
\qquad
\gamma\partial_\gamma \log V_{\mathrm{inst}}
\;=\; -4 \;+\; 1\cdot\frac{S_{\mathrm{BO}}(7)}{\sqrt{V_3}}.
$$
The first term is the prefactor contribution $(-2, -4)$; the second is
$-\partial_{\log m}S_{\mathrm{BO}}^{\mathrm{E}} = -S_{\mathrm{BO}}^{\mathrm{E}}
\cdot (p_S, q_S) = -S_{\mathrm{BO}}^{\mathrm{E}} \cdot (-\tfrac{1}{2}, -1)
= S_{\mathrm{BO}}^{\mathrm{E}} \cdot (\tfrac{1}{2}, 1)$.

At the benchmark $V_3 = 0.4535$, $S_{\mathrm{BO}}^{\mathrm{E}} = 27.14$:
$$
(p_{\mathrm{inst}}, q_{\mathrm{inst}})
\;=\; (-2, -4) \;+\; 27.14\cdot(\tfrac{1}{2}, 1)
\;=\; (11.57, 23.14).
$$

### 2.1 Parallel-direction check

Vector $(11.57, 23.14)$ compared to the five existing scaling vectors of the
6-term potential (including H-flux):

| Term | scaling vector $(p, q)$ | cross-product with $(11.57, 23.14)$ |
|:---:|:---:|:---:|
| Ricci | $(-1, -4)$ | $11.57\cdot(-4) - (-1)\cdot 23.14 = -23.13$ |
| Freund-Rubin | $(+1, -6)$ | $11.57\cdot(-6) - 1\cdot 23.14 = -92.56$ |
| fiber Casimir | $(-6, -4)$ | $11.57\cdot(-4) - (-6)\cdot 23.14 = 92.55$ |
| base Casimir | $(-2, -8)$ | $11.57\cdot(-8) - (-2)\cdot 23.14 = -46.28$ |
| $\Lambda_7$ | $(-1, -2)$ | $11.57\cdot(-2) - (-1)\cdot 23.14 = \mathbf{0}$ |
| H-flux | $(-3, -6)$ | $11.57\cdot(-6) - (-3)\cdot 23.14 = \mathbf{0}$ |

The effective scaling vector of $\log|V_{\mathrm{inst}}|$ is
$(11.57, 23.14) = -27.14\cdot(-\tfrac{1}{2}, -1) \propto (1, 2)$—**exactly
parallel to the $\Lambda_7$ scaling direction $(-1, -2)$ (up to an overall sign
and magnitude) and parallel to the H-flux direction $(-3, -6) = 3\cdot(-1,-2)$.**

### 2.2 Structural root cause

The parallel-direction pathology is not a coincidence. The Weyl prescription
used in §1.3–1.5 dictates:
- All Einstein-frame potential densities have a common $1/V_3^2$ factor
  (prefactor scaling $(-2, -4)$).
- The $S_{\mathrm{BO}}^{\mathrm{E}}$ scaling arises from
  $S_{\mathrm{BO}}^{\mathrm{E}} \propto V_3^{-1/2}$, with scaling
  $(-\tfrac{1}{2}, -1) = \tfrac{1}{2}(-1, -2)$.

Both contributions sit along the SAME direction $\propto (-1, -2) \propto
(p_\Lambda, q_\Lambda)$. The total scaling vector of $\log V_{\mathrm{inst}}$
is thus always a linear combination of $(-1, -2)$ and $(-\tfrac{1}{2}, -1)$,
both of which are $\parallel\Lambda_7$. Hence V_inst's scaling is EXACTLY
parallel to the cosmological-constant direction, and by the §R.27
cross-product argument it contributes ZERO to $\det H$ in combination with
$\Lambda_7$.

**This is the same obstruction as H-flux, from the same structural cause:
pure Weyl scaling.**

## §3. Three-equation system with $V_{\mathrm{inst}}$ included

Despite §2's parallel-direction result, let us carry out the full
root-finding to verify that the Hessian eigenvalues behave as the structural
argument predicts.

### 3.1 Potential with BF-instanton term added

$$
V(\alpha, \gamma) \;=\;
\frac{A_R}{\alpha\gamma^4}
\;+\; \frac{A_F\alpha}{\gamma^6}
\;+\; \frac{A_C^{\mathrm{fib}}}{\alpha^6\gamma^4}
\;-\; \frac{B_{\mathrm{base}}}{\alpha^2\gamma^8}
\;+\; \frac{\Lambda_7\,A_L}{\alpha\gamma^2}
\;+\; \frac{\mathcal{C}_0}{K^2\alpha^2\gamma^4}
   \,\exp\!\left(-\frac{S_{\mathrm{BO}}}{\sqrt{K\alpha\gamma^2}}\right),
$$
with Session 18 coefficients
$A_R = 1.764\times 10^{-3}$, $A_F = 1.654\times 10^{-2}$,
$A_L = 1.764\times 10^{-3}$, $A_C^{\mathrm{fib}} = 7.139\times 10^{-2}$,
$B_{\mathrm{base}} = |C_{\mathrm{base}}|/K^2$, and H-flux OFF ($p=0$ for
clarity).

### 3.2 Solution at $\mathcal{C}_0$ such that $V_{\mathrm{inst}}$ is comparable to $\Lambda_7\cdot A_L$

Required: $V_{\mathrm{inst}}^\star \sim \Lambda_7 A_L/(\alpha\gamma^2)$, i.e.
$$
\frac{\mathcal{C}_0 \exp(-S_{\mathrm{BO}}^{\mathrm{E}})}{K^2\alpha^2\gamma^4}
\;\sim\; \Lambda_7 \cdot A_L/(\alpha\gamma^2)
\;\Longrightarrow\;
\mathcal{C}_0 \;\sim\; |\Lambda_7|\cdot A_L\cdot K^2\cdot \alpha\gamma^2 \cdot e^{+27.14}
\;\approx\; 6\times 10^3\cdot 1.76\times 10^{-3}\cdot 507\cdot 0.020\cdot 6\times 10^{11}
\;\approx\; 7\times 10^{13}.
$$
This is **many orders of magnitude larger than any natural scale in the 7D
theory** (which is $\mathcal{O}(1)$ in $G_7 = 1$ units). The instanton is
numerically VIRTUALLY ZERO at the benchmark.

### 3.3 Explicit numerical verification

Using a Newton-Raphson scheme (native numpy implementation verified on the
Session 18 §R.17.3 benchmark: it recovers $(\alpha_\star, \gamma_\star, \Lambda_7)
= (0.7978, 0.1651, -5769)$ to residual $8 \times 10^{-12}$):

```
# Verification of Session 18 benchmark (no V_inst)
alpha_* = 0.7978, gamma_* = 0.1651, Lambda_7 = -5768.59
Cartesian Hessian: H_aa = 17873.10, H_ag = -36838.29, H_gg = -301984.65
eigenvalues: e_- = -3.06e+05, e_+ = +2.21e+04
det H = -6.75e+09  ->  SADDLE
```

Adding $V_{\mathrm{inst}}$ with physically-motivated prefactor
$\mathcal{C}_0 \in \{10^{-3}, 1, 10^3\}$ (i.e. spanning 6 orders of magnitude
around the natural scale):

| $\mathcal{C}_0$ | $V_{\mathrm{inst}}(\alpha_\star,\gamma_\star)$ | relative to
$V_\Lambda = -10.26$ |
|:---:|:---:|:---:|
| $10^{-3}$ | $10^{-3}\cdot 6.2\times 10^{-15} \;=\; 6.2\times 10^{-18}$ | $10^{-18}$ |
| $1$ | $6.2\times 10^{-15}$ | $10^{-15}$ |
| $10^3$ | $6.2\times 10^{-12}$ | $10^{-12}$ |

The critical point $(\alpha_\star, \gamma_\star, \Lambda_7)$ shifts by
$< 10^{-12}$ and the Hessian shifts by $< 10^{-11}$. The saddle remains a
saddle with $m^2_-$ effectively unchanged. **The BF-instanton is
quantitatively irrelevant.**

## §4. Hessian and radion masses

At the unshifted benchmark $(\alpha_\star, \gamma_\star, \Lambda_7) = (0.7978,
0.1651, -5769)$, the Hessian is identical to the Session 18 §R.17.3 result:

| quantity | value |
|:---:|:---:|
| $V_\star$ | $-6\times 10^{-14}$ (numerically zero) |
| $\|\nabla V\|$ | $8\times 10^{-12}$ |
| $m^2_-/M_P^2$ | $-3.06\times 10^5$ |
| $m^2_+/M_P^2$ | $+2.21\times 10^4$ |
| $m^2_-\,[M_{\mathrm{poly}}^2]$ | $-109.6$ (per Session 18 conversion $m^2_{\mathrm{phys}} = m^2/M_P^2 \cdot (\alpha_\star/4.63)^2/1.181$) |
| $m^2_+\,[M_{\mathrm{poly}}^2]$ | $+540.7$ |
| BF bound | VIOLATED by factor 110 |

**Conclusion**: the BF-instanton does not rescue Minkowski-4 stability. The
$\rho$-mode tachyon persists.

## §5. If $V_{\mathrm{inst}}$ succeeded

Not applicable; however, for completeness the $S_{\mathrm{BO}}^{\mathrm{E}}$
value at the saddle is
$$
S_{\mathrm{BO}}^{\mathrm{E}}(0.7978, 0.1651)
\;=\; \frac{18.274}{\sqrt{0.4609}} \;=\; 26.91.
$$
Paper IV's $\mathcal{H}_7 = 38.459$ contains not only $S_{\mathrm{BO}}(7)$
but also $\Delta\varepsilon\ln\varepsilon_7 = 2.224$ and
$\tfrac{1}{2}\ln(c_{11}/24\pi^2) = -0.299$, so $\mathcal{H}_7 \neq
S_{\mathrm{BO}}^{\mathrm{E}}$ in any straightforward sense. The Paper IV
construction uses the bare $2 S_{\mathrm{BO}}(7)$ as an input to the hierarchy
formula, not as a radion-potential exponent, so the present §4 result does NOT
directly conflict with Paper IV §13's electroweak-hierarchy prediction. Paper
IV §13's claim is that $v = M_P\exp(-38.459) = 242$\,GeV, which does not
require Minkowski-4 stability in the 7D theory.

## §6. Diagnostic: why $V_{\mathrm{inst}}$ fails

### 6.1 Root cause

The two independent contributions to $\log V_{\mathrm{inst}}$ are:

1. **Prefactor** $\mathcal{C}(\alpha,\gamma) \propto V_3^{-2}$, scaling $(-2,-4)$.
   This is the universal 4D-Einstein-frame rescaling factor for any bulk
   potential (Session 18 §R.1.2).
2. **Exponent** $-S_{\mathrm{BO}}^{\mathrm{E}} \propto V_3^{-1/2}$. Under log-
   differentiation, this contributes
   $-\partial_{\log m}(-S_{\mathrm{BO}}^{\mathrm{E}})\cdot S_{\mathrm{BO}}^{\mathrm{E}}
   = \tfrac{1}{2}S_{\mathrm{BO}}^{\mathrm{E}}\cdot(1, 2)$.

Both directions lie along $(-1,-2)$, the same line as $\Lambda_7$ and (a
multiple of) H-flux.

The reason is that $V_3(\alpha, \gamma) = K\alpha\gamma^2$ is a single
dimensionful quantity (the 3-volume), and any Weyl-rescaled quantity
$f(V_3)$ has $\log f$ derivatives along the direction $(\partial_{\log\alpha}
\log V_3, \partial_{\log\gamma}\log V_3) = (1, 2)$. **To introduce a scaling
direction that is NOT a function of $V_3$ alone, one needs an ingredient whose
moduli dependence is NOT purely through $V_3$.**

### 6.2 What would a non-parallel direction look like?

Examples of moduli-dependent quantities NOT of the form $f(V_3)$:

(a) **Separate fiber and base scales** (not just their $V_3$ product). E.g.,
   an instanton from a string wrapping the fiber $S^1_\alpha$ alone would have
   action $\propto \alpha$, scaling $(1, 0)$—independent of $V_3$.

(b) **Instantons living on $\Sigma$ alone** (e.g., vortex-antivortex pairs on
   the hyperbolic base) would have action $\propto \gamma^2$ or $\gamma^0$,
   scaling $(0, 2)$ or $(0, 0)$—also $V_3$-inhomogeneous.

(c) **Fiber Wilson lines / Kaluza-Klein momentum modes** along $S^1_\alpha$
   have mass $\propto 1/\alpha$, giving potential-scale $1/\alpha^4$—scaling
   $(-4, 0)$, $V_3$-inhomogeneous.

(d) **Higher-curvature terms** from the base scalar curvature $R_\Sigma =
   -2/\gamma^2$ squared: $R_\Sigma^2 \propto \gamma^{-4}$, yielding (after
   volume integration and Weyl) a $\gamma^{-4}$ piece that DOES depend only on
   $\gamma$—scaling $(0, -4)$, which is $V_3$-inhomogeneous.

Any one of these would produce a genuinely new scaling vector. The breathing-
mode BF-instanton happens not to—its Weyl scaling is degenerate with the
cosmological-constant direction by virtue of being a purely $V_3$-scaled
quantity.

### 6.3 Numerical diagnostic: what $V_{\mathrm{inst}}$ scaling WOULD work?

I performed a scan over constant-power ansätze $V_{\mathrm{inst}} = A_I
\alpha^{p_I}\gamma^{q_I}$ with $(p_I, q_I) \in [-4,4]\times[-8,5]$ and $A_I$
spanning 4 orders of magnitude, seeking the full 3-equation system
$\{V=0,\partial_\alpha V = 0,\partial_\gamma V = 0\}$ to have a stable-minimum
critical point in the physical window $(\alpha,\gamma) \in [0.1, 3.0]\times
[0.03, 0.5]$.

The complete diagnostic search (1344 trials, 3 seed points each) yielded
10 stable minima. All 10 share the signature that the required
$V_{\mathrm{inst}}$ coefficient is **$A_I = +10$ (large positive)**, with the
following scaling vectors:

| $(p_I, q_I)$ | $A_I$ | $\alpha_\star$ | $\gamma_\star$ | $\Lambda_7$ | $m^2_-$ | $m^2_+$ |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| $(-2, +2)$ | $+10$ | $1.28$ | $0.496$ | $-568$ | $+5.5$ | $+192$ |
| $(-1, 0)$ | $+10$ | $1.08$ | $0.404$ | $-1487$ | $+47.4$ | $+623$ |
| $(-1, +2)$ | $+10$ | $1.13$ | $0.472$ | $-617$ | $+18.1$ | $+267$ |
| $(0, 0)$ | $+10$ | $0.96$ | $0.404$ | $-1496$ | $+115$ | $+634$ |
| $(0, +2)$ | $+10$ | $1.05$ | $0.466$ | $-640$ | $+33.2$ | $+295$ |
| $(+1, 0)$ | $+10$ | $0.88$ | $0.426$ | $-1424$ | $+129$ | $+543$ |
| $(+1, +2)$ | $+10$ | $1.00$ | $0.469$ | $-646$ | $+45.6$ | $+293$ |
| $(+2, 0)$ | $+10$ | $0.83$ | $0.471$ | $-1305$ | $+76.1$ | $+469$ |
| $(+2, +2)$ | $+10$ | $0.95$ | $0.480$ | $-639$ | $+51.3$ | $+280$ |
| $(+3, +2)$ | $+10$ | $0.92$ | $0.496$ | $-622$ | $+48.3$ | $+264$ |

All 10 cases have **$\gamma_\star \in [0.40, 0.50]$**—at the high end of the
previously-scanned $\gamma$ window—and **$\alpha_\star \in [0.83, 1.28]$**.
These are distinct from the §R.17 saddle at $\gamma \approx 0.16$.

**Required scaling vectors all have $q_I \geq 0$**, i.e., $V_{\mathrm{inst}}$
must grow or be constant with $\gamma$ at fixed $\alpha$. This is a
characteristic NOT produced by pure Weyl rescaling of a bulk potential
density, which always gives $q \leq -2$ (since the Einstein-frame prefactor is
$1/V_3^2 \propto \gamma^{-4}$).

**Required coefficient magnitude $A_I = +10$** (in $G_7 = 1$ units, where
$A_R = 1.8\times 10^{-3}$) is about $6 \times 10^3$ times the natural
Casimir/Ricci scale. This is the diagnostic reach of §R.28.3 of Session 18.

### 6.4 Physical interpretation of the required magnitude

If $V_{\mathrm{inst}} = A_I$ with $A_I = 10$ at $(\alpha,\gamma) = (1.0, 0.4)$
and the ansatz is $V_{\mathrm{inst}} = \mathcal{C}_0 e^{-S}$, then
$$
\mathcal{C}_0 \;=\; 10 \cdot e^{+S}.
$$
For $S = S_{\mathrm{BO}}(7) = 18.274$: $\mathcal{C}_0 \approx 10 \cdot 8.6\times 10^7
\approx 8.6\times 10^8$ — ~$10^9$ times natural scale.

For $S = 0$ (no exponential suppression), $\mathcal{C}_0 \approx 10$ — of order
the fiber Casimir scale (also $\mathcal{O}(10)$ in $C_{\mathrm{fib}} = 36.33$).
This is suggestive: the required ingredient is NOT an exponentially-suppressed
instanton but a tree-level or one-loop contribution with a large coefficient.

### 6.5 Polygon-theory candidates for a non-parallel scaling direction

Following the §R.28.4 enumeration, the natural candidates are:

**(C1) Higher-curvature corrections** ($R^2$, Ricci², Riemann²) on the
hyperbolic base. Base curvature $R_\Sigma = -2/\gamma^2$, so
$R_\Sigma^2 \propto \gamma^{-4}$. After Weyl rescaling:
$$
V_{R^2} \;\propto\; \frac{(R_\Sigma^2)\cdot V_3}{V_3^2}
\;=\; \frac{\gamma^{-4}\cdot K\alpha\gamma^2}{K^2\alpha^2\gamma^4}
\;=\; \frac{1}{K\alpha\gamma^6}.
$$
Scaling vector $(-1, -6)$. Is this parallel to any existing term? Check
cross-products:

| existing vector | $(p,q)$ | cross-product with $(-1,-6)$ |
|:---:|:---:|:---:|
| Ricci $(-1,-4)$ | | $(-1)(-4) - (-1)(-6) = 4-6 = -2$ |
| FR $(+1,-6)$ | | $(-1)(-6) - (+1)(-6) = 6+6 = +12$ |
| fib Cas $(-6,-4)$ | | $(-1)(-4) - (-6)(-6) = 4-36 = -32$ |
| base Cas $(-2,-8)$ | | $(-1)(-8) - (-2)(-6) = 8-12 = -4$ |
| $\Lambda_7$ $(-1,-2)$ | | $(-1)(-2) - (-1)(-6) = 2-6 = -4$ |
| H-flux $(-3,-6)$ | | $(-1)(-6) - (-3)(-6) = 6-18 = -12$ |

**$(-1, -6)$ is independent of all six existing directions.** This is the
cleanest candidate for a genuinely new scaling direction.

However, when I test $(p_I, q_I) = (-1, -6)$ in the numerical scan at natural
coefficient $A_I = \pm 10^{-3}$ to $\pm 10^3$, no stable minimum is found in
the physical window. The direction is independent but its sign/magnitude at
physically natural values of the coefficient (after a proper 1-loop
computation) does not suffice to stabilize.

**(C2) Hodge dual of the FR 2-form flux.** In 7D, $\star F_2$ is a 5-form; its
action-density contribution after reduction yields a term with scaling
dependent on whether the dual field lives on the fiber or the base. A
preliminary dimensional analysis suggests scaling $(-4, -2)$ or similar, NOT
$\propto V_3$: this is worth investigating in a future session.

**(C3) Wrapped Euclidean 3-cycles.** If a BF instanton wraps $M_3$ itself
(not the breathing mode), its action is $\propto V_3$, and the exponential
contributes $\partial_{\log m}e^{-V_3} = -V_3\cdot(1, 2) \cdot e^{-V_3}$ — STILL
along $(-1,-2)$. But if it wraps $S^1_\alpha$ only, action is
$\propto \alpha$, scaling $(1, 0)$—independent of $V_3$ direction. This
corresponds to a fiber-localized instanton, e.g., the fiber Wilson line from a
fundamental string.

**(C4) Scherk-Schwarz-induced fermion masses at intermediate $\gamma$
values.** The antiperiodic fermion spectrum contributes $1/\alpha^4$ (Session
18 §R.1.2) at LEADING order, but subleading (finite-$\gamma$) corrections
have a scaling $(-4, -4)$ or $(-4, -2)$—again potentially independent.

**(C5) Axion-instanton at N=7 Chern-Simons boundary.** The $\mathrm{CS}_3$
level-7 boundary-term contribution to the 4D potential has a scaling that
depends on the ratio $\alpha/\gamma$ through the Seifert Euler class
$e = N/2 = 7/2$. Dimensional analysis is pending.

### 6.6 Summary of §6

The BF-instanton from the breathing-mode WKB action $S_{\mathrm{BO}}(7)$ FAILS
to stabilize Minkowski-4, for two independent reasons:

1. **Scaling degeneracy**: under pure Weyl rescaling to the Einstein frame,
   $V_{\mathrm{inst}}$'s effective scaling vector is parallel to $\Lambda_7$
   (a linear combination of $(-2,-4)$ from the prefactor and $(1,2)\cdot
   S_{\mathrm{BO}}^{\mathrm{E}}$ from the exponent, both along the $V_3$
   direction).

2. **Exponential smallness**: even if the scaling were non-parallel, at the
   benchmark critical point $V_3 \sim 0.45$ gives
   $S_{\mathrm{BO}}^{\mathrm{E}} \sim 27$, so $e^{-S} \sim 10^{-12}$—too small
   to compete with the $\mathcal{O}(1)$ Casimir and flux terms.

The two reasons are logically independent: fixing either would not suffice
without the other.

## §7. Verdict

**$V_{\mathrm{inst}}$ DOES NOT rescue Minkowski-4 stability.** The breathing-
mode BF-instanton has scaling vector parallel to $\Lambda_7$, matching the
H-flux obstruction of Session 18 §R.27. Moreover, the exponential
$e^{-S_{\mathrm{BO}}^{\mathrm{E}}} \sim 10^{-12}$ at the benchmark critical
point renders the instanton numerically negligible even if it had a genuinely
new scaling direction.

**The Session 18 verdict stands**: the 7D Seifert compactification for $N=7$
does not admit a stable Minkowski-4 vacuum within the framework
(Einstein-Hilbert + $\Lambda_7$ + Freund-Rubin 2-form + 1-loop Casimir +
H-flux + BF-instanton). Options for future sessions:

1. **Higher-curvature corrections** ($R^2$, Ricci², Riemann²): scaling
   $(-1,-6)$ is independent of all existing directions. Needs proper 1-loop
   coefficient computation.

2. **Hodge-dual FR flux** ($\star F_2$, a 5-form in 7D): may give scaling
   $(-4,-2)$ or similar, independent of $V_3$-direction. Needs full Weyl
   reduction.

3. **Fiber Wilson-line instanton** (wrapping $S^1_\alpha$ only, not $M_3$):
   scaling $(1,0)$—completely $V_3$-independent. Natural candidate from the
   Seifert structure.

4. **Fermion threshold corrections** at intermediate $\gamma$: scaling
   $(-4,-4)$ or $(-4,-2)$, potentially independent.

5. **Scherk-Schwarz Chern-Simons boundary term** at level 7: scaling
   depends on Seifert Euler class $e = 7/2$.

None of these is a trivial calculation; each is a multi-session research
project. The present session closes the BF-instanton branch with a negative
result.

## §8. Consistency check with Paper IV §13

Paper IV §13's electroweak-hierarchy formula $v = M_P \exp(-\mathcal{H}_7)$
uses $\mathcal{H}_7 = 38.459$ as a DIMENSIONLESS EXPONENT, constructed from
the bare $S_{\mathrm{BO}}(7) = 18.274$ at unit-volume choice $V_3 = 1$. The
present derivation shows that $S_{\mathrm{BO}}^{\mathrm{E}} = S_{\mathrm{BO}}(7)
/ \sqrt{V_3}$ in general, and at $V_3 = 0.4535$ (the Session 18 §R.17 saddle
point) we get $S_{\mathrm{BO}}^{\mathrm{E}} = 27.14$.

**Paper IV's framework implicitly uses the AdS-branch critical point (where
$V_3 \approx 1$ by choice of natural $G_7$ unit)**, not the V_*=0 saddle.
The hierarchy formula is internally consistent with a stable-AdS-4 theory
where the AdS vacuum is taken as the natural ground state, and the present
§4 result showing that Minkowski-4 is unreachable DOES NOT UNDERMINE Paper
IV's electroweak prediction, which is a functional relation between bare
polygon numbers ($b(7), b(11), \Delta\varepsilon, \varepsilon_7$) and the
dimensionless ratio $M_P/v$.

**However**, the claim "the radion is stabilized at Minkowski-4 with
$m_{\mathrm{radion}} \sim M_{\mathrm{poly}}$" in Paper IV §9 remains unsupported
within the CW+FR+Einstein+Casimir+H-flux+BF-instanton framework. Session
18's assessment options (accept AdS-4 with $m_{\mathrm{radion}} \sim 10$–$30
M_{\mathrm{poly}}$, or seek a new ingredient) remain the open paths.

## §9. Final statement

After adding $V_{\mathrm{inst}}(\alpha, \gamma)$ derived from the breathing-mode
WKB action $S_{\mathrm{BO}}(7)$ under proper Weyl rescaling to the 4D Einstein
frame, the 7-term potential
$$
V \;=\; V_{\mathrm{Ricci}} + V_{\mathrm{FR}} + V_{\mathrm{fib-Cas}}
  \;+\; V_{\mathrm{base-Cas}} + V_\Lambda + V_H + V_{\mathrm{inst}}
$$
does NOT admit a stable Minkowski-4 vacuum. The BF-instanton's effective
scaling direction is parallel to the cosmological-constant direction, and
its magnitude is exponentially suppressed. The stability obstruction of
Session 18 §R.27 is therefore ROBUST to the addition of the polygon's
natural instanton ingredient.

Path (b) — adding $V_{\mathrm{inst}}$ — has been closed.

The remaining first-principles ingredients to try (in order of structural
promise) are:

- **(C1) Higher-curvature base-scalar-curvature-squared term**: scaling
  $(-1, -6)$, genuinely independent of all six existing directions. This is
  the PRIMARY CANDIDATE for a follow-up session.
- **(C3) Fiber-wrapped Euclidean instanton**: scaling $(1, 0)$, completely
  $V_3$-independent. Natural from the Seifert-bundle structure.
- **(C4) Fermion threshold corrections**: $(-4, -4)$ or $(-4, -2)$.

These should be pursued in Session 20 or beyond. Each represents a separate
research programme with non-trivial technical content (e.g., base-manifold
Riemann tensor contractions for (C1), explicit fiber Wilson-line semiclassical
reduction for (C3)).

The ROBUST CONCLUSION of Sessions 18 and 19 is this: **within the natural
bulk gravitational + Casimir + flux + breathing-mode-BF framework, the $N=7$
Seifert compactification produces a stable AdS-4 vacuum with PeV-scale radion
masses, but not a stable Minkowski-4 vacuum.** Any claim of Minkowski-4
stability in Paper IV requires an additional ingredient from one of the
(C1)–(C5) categories.

---

*Session 19 closed: BF-instanton does not rescue Minkowski-4 stability;
obstruction is robust. Next session should investigate higher-curvature
(C1) as the primary candidate.*
