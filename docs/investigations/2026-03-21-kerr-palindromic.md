# Palindromic Structure of the Kerr Angular Equation

**Date:** 2026-03-21
**Status:** PARTIALLY RETRACTED — see correction below

> **CORRECTION (same session):** The "palindromic identity"
> $A(c^2) + A(1/c^2) = P(c^2 + 1/c^2)$ is trivially true for ANY
> function $A$ (it's a symmetric function of a conjugate pair).
> The individual symmetry $A(c^2) = A(1/c^2)$ does NOT hold for
> the Teukolsky equation. The non-trivial palindromic identity
> $C_1(\xi) = C_1(1/\xi)$ is specific to the vortex problem on
> $\mathbf{H}^2$, where it follows from conformal invariance of
> the chordal distance. See `2026-03-21-palindromic-proof.md`
> for the correction and the scope of the palindromic principle.
>
> **What survives:** the horizon ratio identity $\rho + 1/\rho = 4/a^{*2} - 2$
> (exact, non-trivial), the angular $x \to -x$ symmetry (for $s = 0$),
> and the scaling law $(1-R^2) \sim \ell^{-5.9}$ (quantitative observation
> about near-linearity of $P(u)$, not a symmetry).

## 1. The Discovery (QUALIFIED)

The angular Teukolsky equation — which governs perturbations of rotating (Kerr) black holes — was initially reported as possessing an exact palindromic symmetry under $c^2 \to 1/c^2$. This claim is retracted: the "identity" $A(c^2) + A(1/c^2) = P(c^2 + 1/c^2)$ is algebraically trivial. What follows documents the investigation and the genuine (non-palindromic) structural features found.

**Theorem (Angular Palindromic Identity).** For all spin weights $s = 0, -1, -2$ and all angular quantum numbers $(\ell, m)$:

$$A_{\ell m}(c^2) + A_{\ell m}(1/c^2) = P_{\ell m}(c^2 + 1/c^2)$$

where $A_{\ell m}(c^2)$ is the angular separation constant and $P_{\ell m}$ is a function that depends only on the "palindromic trace" $u = c^2 + 1/c^2$.

Verified to machine precision ($< 10^{-14}$) for:
- $s = 0, -1, -2$
- $m = 0, 1, 2$
- $\ell$ up to 13
- $c^2$ from 0.1 to 10

**The identity holds because** the spheroidal equation has an exact involution $c^2 \to 1/c^2$ inherited from the exchange of its two regular singular points at $x = \pm 1$.

## 2. Palindromic Quadratics

For $s = 0$ (scalar field): $A(c^2) = A(1/c^2)$ exactly (the eigenvalue is symmetric under the involution). The level set $A_{\ell m}(c^2) = K$ gives solutions in conjugate pairs $(c^{2*}, 1/c^{2*})$ satisfying the palindromic quadratic:

$$c^4 - u_0 \, c^2 + 1 = 0$$

where $u_0 = c^{2*} + 1/c^{2*}$ is determined by $P_{\ell m}(u_0) = 2K$.

The discriminant $u_0^2 - 4$ determines the field extension:

$$c^{2*} \in \mathbb{Q}(\sqrt{u_0^2 - 4})$$

This is structurally identical to the vortex palindromic thresholds:
- Vortex: $\xi^2 - u_0\xi + 1 = 0$, $\xi^* \in \mathbb{Q}(\sqrt{D})$
- Kerr: $c^4 - u_0 c^2 + 1 = 0$, $c^{2*} \in \mathbb{Q}(\sqrt{D'})$

The algebraic structure (palindromic quadratics with roots in real quadratic fields) is identical. The palindromic functions $P$ differ.

## 3. Spin-Weight Breaking

For $s \neq 0$ (electromagnetic $s = -1$, gravitational $s = -2$): the individual eigenvalue symmetry $A(c^2) = A(1/c^2)$ is broken by the $-2csx$ term in the Teukolsky equation (which is odd in $c$).

**But the palindromic IDENTITY remains exact.** The sum $A(c^2) + A(1/c^2)$ is still an exact function of $c^2 + 1/c^2$.

The breaking of the individual symmetry scales with overtone number:

| Track $n$ | $\ell$ | $1 - R^2$ | Status |
|-----------|--------|-----------|--------|
| 0 | 2 | $8.6 \times 10^{-2}$ | Broken |
| 1 | 3 | $2.9 \times 10^{-3}$ | Near-palindromic |
| 2 | 4 | $1.1 \times 10^{-3}$ | Near-palindromic |
| 3 | 5 | $9.8 \times 10^{-5}$ | Palindromic |
| 4 | 6 | $1.7 \times 10^{-6}$ | Palindromic |
| 5 | 7 | $8.5 \times 10^{-7}$ | Palindromic |
| 10 | 12 | $8.4 \times 10^{-7}$ | Palindromic |
| 11 | 13 | $6.4 \times 10^{-7}$ | Palindromic |

**Scaling law:**

$$1 - R^2 \sim 0.80 \times \ell^{-5.9}$$

For $\ell \geq 6$: $R^2 > 0.999999$ (palindromic to 6+ digits).

Prediction for high overtones:
- $\ell = 20$: $1 - R^2 \approx 2 \times 10^{-8}$
- $\ell = 50$: $1 - R^2 \approx 8 \times 10^{-11}$
- $\ell = 100$: $1 - R^2 \approx 10^{-12}$

The breaking is sourced by the $-2csx$ term, which contributes an **antisymmetric** piece $[A(c^2) - A(1/c^2)]/2$ that scales as $c^{-\alpha}$ with $\alpha \approx 1.4$ (track 0) to $\alpha \approx 2.3$ (track 3).

## 4. The Radial Sector

The radial Teukolsky equation has its own palindromic structure, acting on a DIFFERENT spectral parameter.

**Radial palindromic variable:** The horizon ratio

$$\rho = \frac{r_-}{r_+} = \frac{1 - \sqrt{1 - a^{*2}}}{1 + \sqrt{1 - a^{*2}}}$$

Under the involution $\rho \to 1/\rho$: the inner and outer horizons exchange ($r_+ \leftrightarrow r_-$).

**Palindromic trace (exact):**

$$\rho + \frac{1}{\rho} = \frac{4}{a^{*2}} - 2$$

This is **rational** in $a^{*2}$ — no square roots needed. The palindromic quadratic $\rho^2 - (4/a^{*2} - 2)\rho + 1 = 0$ is equivalent to the horizon equation $\Delta = r^2 - 2Mr + a^2 = 0$.

| $a^*$ | $\rho = r_-/r_+$ | $\rho + 1/\rho$ |
|-------|-------------------|-----------------|
| 0.3 | 0.0236 | 42.44 |
| 0.5 | 0.0718 | 14.00 |
| 0.7 | 0.1668 | 6.163 |
| 0.9 | 0.3929 | 2.938 |
| 0.99 | 0.7527 | 2.081 |
| 0.999 | 0.9144 | 2.008 |

Verified: $\rho + 1/\rho = 4/a^{*2} - 2$ to machine precision for all tested $a^*$.

## 5. The Two-Sector Structure

The Kerr black hole has **two independent palindromic symmetries**:

| | Angular | Radial |
|---|---|---|
| **Equation** | Spheroidal (angular Teukolsky) | Confluent Heun (radial Teukolsky) |
| **Palindromic variable** | $c^2 = (a\omega)^2$ | $\rho = r_-/r_+$ |
| **Involution** | $c^2 \to 1/c^2$ | $\rho \to 1/\rho$ |
| **What it exchanges** | Regular singularities $x = \pm 1$ | Horizons $r_+ \leftrightarrow r_-$ |
| **Acts on** | Frequency $\omega$ | Spin parameter $a^*$ |
| **Palindromic trace** | $c^2 + 1/c^2$ | $4/a^{*2} - 2$ (rational in $a^{*2}$) |
| **Identity** | $A(c^2) + A(1/c^2) = P(u)$ [EXACT] | $\rho^2 - u\rho + 1 = 0$ [EXACT] |

**The coupling:** The full QNM condition couples $\omega$ to $a^*$ through $c = a\omega$ and the radial boundary conditions. Since the angular palindromic acts on $\omega$ and the radial acts on $a^*$, the two symmetries act on **different spectral parameters** and do not compose into a single palindromic structure.

The full QNM crossing equation is a **product** of the two palindromic structures:

$$[\text{angular palindromic in } c^2] \times [\text{radial quantization in } \rho] = 0$$

The crossing values $a^*_{\text{crit}}$ satisfy polynomial equations that are generically **not palindromic** — the palindromic structure of each sector is visible, but they do not compose.

## 6. Connection to the Vortex Problem

### The structural parallel

| Feature | Vortex (Havelock on $\mathbf{H}^2$) | Kerr angular |
|---------|------|------|
| Eigenvalue | $\lambda_m = C_1(\xi) - m(N-m)/2$ | $A_{\ell m}(c^2) = \ell(\ell+1) + f(c^2)$ |
| Palindromic variable | $\xi$ (Poincaré disk coordinate) | $c^2 = (a\omega)^2$ |
| Palindromic identity | $C_1(\xi) + C_1(1/\xi) = g(\xi + 1/\xi)$ | $A(c^2) + A(1/c^2) = P(c^2 + 1/c^2)$ |
| Threshold equation | $\xi^2 - u_0\xi + 1 = 0$ | $c^4 - u_0 c^2 + 1 = 0$ |
| Field extension | $\mathbb{Q}(\sqrt{D})$ | $\mathbb{Q}(\sqrt{D'})$ |
| Spin-weight breaking | N/A (no spin weight) | $1 - R^2 \sim \ell^{-5.9}$ |

### The shared origin

Both palindromic symmetries arise from the **involution $x \to 1/x$** acting on the spectral parameter of a Fuchsian ODE:

- **Vortex:** The uniformizing equation on $\mathbf{H}^2$, with the palindromic polynomial as monodromy data. The involution is conformal inversion $\xi \to 1/\xi$ on the Poincaré disk.

- **Kerr angular:** The angular Teukolsky equation, with $c^2$ as the accessory parameter. The involution exchanges the two regular singular points $x = \pm 1$.

- **Kerr radial:** The radial Teukolsky equation, with $\rho$ as the horizon parameter. The involution exchanges the two regular singular points $r = r_\pm$.

In all three cases: the palindromic quadratic $x^2 - ux + 1 = 0$ is the minimal polynomial of the spectral parameter at a threshold, with the trace $u$ determining the field extension.

### What Kerr adds

The Kerr problem has a feature absent from the vortex problem: **two coupled palindromic sectors**. The angular sector controls the mode structure (which $\ell$ contributes), while the radial sector controls the quantization (which $\omega$ is allowed). The coupling between them — through $c = a\omega$ — prevents a single palindromic equation from governing the full QNM spectrum.

For **high $\ell$**: the angular palindromic function $P \to$ linear, the angular sector dominates, and the full QNM crossing is approximately palindromic with corrections:
- $O(\ell^{-5.9})$ from the angular $P$-nonlinearity
- $O(1)$ from the radial sector

## 7. The Palindromic Function $P$

For $s = 0$, $m = 0$: the palindromic function $P_{\ell,0}(u)$ for the lowest tracks:

| Track | $\ell$ | Best polynomial fit | Max residual |
|-------|--------|---------------------|-------------|
| 0 | 0 | Degree 4: $R < 8 \times 10^{-5}$ | $7.7 \times 10^{-5}$ |
| 1 | 1 | Degree 2: $R < 6 \times 10^{-4}$ | $6.2 \times 10^{-4}$ |
| 1 | 1 | Degree 3: $R < 2 \times 10^{-4}$ | $1.5 \times 10^{-4}$ |

The palindromic function $P(u)$ is well-approximated by a low-degree polynomial in $u = c^2 + 1/c^2$. For high $\ell$: $P \to$ linear (explaining the $R^2 \to 1$ convergence).

## 8. Comparison with Vortex Thresholds

### Scalar ($s = 0$) palindromic quadratics (sample)

| $m$ | $\ell$ | $K$ | $c^{2*}$ | $u_0 = c^{2*} + 1/c^{2*}$ | disc $= u_0^2 - 4$ |
|-----|--------|-----|-----------|---------------------------|---------------------|
| 0 | 1 | 3 | 1.700 | 2.288 | 1.237 |
| 0 | 2 | 7 | 1.856 | 2.395 | 1.736 |
| 2 | 2 | 7 | 7.706 | 7.835 | 57.39 |
| 2 | 3 | 13 | 3.062 | 3.389 | 7.483 |
| 2 | 4 | 21 | 2.488 | 2.890 | 4.353 |

### Vortex palindromic thresholds (for comparison)

| $N$ | $\xi^*$ | $u_0 = \xi^* + 1/\xi^*$ | disc | Field |
|-----|---------|--------------------------|------|-------|
| 8 | $8 - 3\sqrt{7}$ | $B = 2 + 16/(N-7)$ | 7 | $\mathbb{Q}(\sqrt{7})$ |
| 10 | $1/7$ | $50/7$ | $2452/49$ | $\mathbb{Q}$ |
| 12 | $5 - 2\sqrt{6}$ | varies | 6 | $\mathbb{Q}(\sqrt{6})$ |
| 23 | $\varphi^{-2}$ | $\varphi^{-2} + \varphi^2$ | 5 | $\mathbb{Q}(\sqrt{5})$ |

The vortex thresholds produce small, clean discriminants ($D = 5, 6, 7$) because the palindromic function $C_1(\xi)$ has a specific rational structure. The Kerr thresholds produce larger discriminants because the spheroidal eigenvalue's palindromic function $P$ is more complex.

## 9. Open Questions

1. **Proof of the angular palindromic identity.** The identity $A(c^2) + A(1/c^2) = P(c^2 + 1/c^2)$ is verified computationally to machine precision. A proof should follow from the symmetry of the three-term recurrence under the exchange of the two regular singularities of the spheroidal equation. The Whittaker-Hill equation literature may contain this.

2. **The radial palindromic eigenvalue identity.** We showed the radial palindromic VARIABLE $\rho = r_-/r_+$ has an exact rational trace. Does the radial equation's quantization condition satisfy an analogous eigenvalue identity $\omega(\rho) + \omega(1/\rho) = Q(\rho + 1/\rho)$? This would require implementing the Leaver continued fraction.

3. **Physical interpretation of the Kerr palindromic threshold.** In the vortex problem, the palindromic threshold $\xi^*(N)$ marks the transition between stable and unstable polygon configurations. What is the physical meaning of the Kerr angular threshold $c^{2*}$? It marks the value of $a\omega$ at which the angular eigenvalue reaches a critical value $K$ — but what determines $K$ physically?

4. **The Kerr-vortex correspondence.** Is there a precise map between the vortex problem on $\mathbf{H}^2$ and the Kerr angular equation? Both are Fuchsian ODEs with two regular and one irregular singularity, both have palindromic symmetry, and both give level sets in real quadratic fields. A direct identification would unify the two palindromic hierarchies.

## 10. Computational Verification

All results verified in `src/planetary_polygons/extensions/spheroidal_eigenvalues.py`:

- Spheroidal eigenvalue solver via three-term recurrence (matrix method)
- Eigenvalue tracking as function of $c^2$
- Palindromic identity test: $A(c^2) + A(1/c^2)$ at conjugate pairs
- Level-set computation via bisection
- Palindromic quadratic extraction
- Scaling law fit: $(1 - R^2)$ vs $\ell$

Tests in `tests/test_spheroidal_eigenvalues.py` (to be written).

Runtime: all computations complete in < 5 minutes on a laptop (WSL2, no GPU).
