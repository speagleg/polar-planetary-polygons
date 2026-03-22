# The Palindromic Theorem: Proof and Scope

**Date:** 2026-03-21
**Status:** PROVED (the vortex case); CORRECTED (the Kerr case)

## The Correction

The "Kerr palindromic identity" $A(c^2) + A(1/c^2) = P(c^2 + 1/c^2)$
reported earlier is **trivially true** for any function $A$. It is an
algebraic tautology, not a structural result. The individual symmetry
$A(c^2) = A(1/c^2)$ does NOT hold for the Teukolsky angular equation.

The **non-trivial** palindromic identity is $C_1(\xi) = C_1(1/\xi)$
for the Havelock confining potential on $\mathbf{H}^2$. This is specific
to the conformally invariant Green's function and does not generalise to
the spheroidal equation.

## The Theorem

**Theorem (Conformal Palindromic Identity).** Let $G(z,w) = -\log\sigma(z,w)$
be the Green's function on the Poincaré disk $\mathbb{D}$, where
$\sigma(z,w) = |z-w|/|1-\bar{z}w|$ is the chordal distance. For the
regular $N$-gon at radius $R = \sqrt{\xi}$:

$$C_1(\xi) = C_1(1/\xi)$$

where $C_1(\xi) = (N-1)(1+\xi^2)/(1-\xi)^2$ is the Havelock confining
potential. In particular, the stability threshold $C_1(\xi^*) = f_{\max}(N)$
gives $\xi^*$ satisfying a palindromic polynomial $Q(\xi) = \xi^d P(\xi + 1/\xi)$.

## Proof

**Step 1: Conformal invariance of $\sigma$.**

The chordal distance $\sigma(z,w) = |z-w|/|1-\bar{z}w|$ is invariant under
all Möbius automorphisms of $\mathbb{D}$. In particular, under the inversion
$\iota: z \mapsto 1/\bar{z}$ (which maps $\mathbb{D}$ to
$\mathbb{C} \setminus \bar{\mathbb{D}}$ and extends $\sigma$ continuously):

$$\sigma(\iota(z), \iota(w)) = \frac{|1/\bar{z} - 1/\bar{w}|}{|1 - (1/z)(1/\bar{w})|}
= \frac{|w - z|}{|\bar{z}\bar{w}|} \cdot \frac{|\bar{z}\bar{w}|}{|\bar{z}\bar{w} - 1|}
= \frac{|z - w|}{|1 - \bar{z}w|} = \sigma(z, w)$$

**Step 2: The N-gon maps to an N-gon.**

The ring $z_j = \sqrt{\xi} \cdot e^{2\pi ij/N}$ maps under $\iota$ to
$\iota(z_j) = (1/\sqrt{\xi}) \cdot e^{2\pi ij/N}$: a ring at radius
$1/\sqrt{\xi}$, i.e., at curvature parameter $1/\xi$.

**Step 3: The energy is invariant.**

The Havelock energy $H = -\sum_{j<k} \log\sigma(z_j, z_k)$ satisfies
$H(\xi) = H(1/\xi)$ by Steps 1 and 2. Since $C_1(\xi)$ is the radial
second derivative of $H$ at the equilibrium ring, and the inversion maps
radial perturbations at $\xi$ to radial perturbations at $1/\xi$:

$$C_1(\xi) = C_1(1/\xi) \qquad \square$$

**Step 4: The palindromic polynomial.**

The threshold $C_1(\xi^*) = f_{\max}(N)$ gives an algebraic equation in $\xi$.
Since $C_1$ is invariant under $\xi \to 1/\xi$, if $\xi^*$ is a root then
$1/\xi^*$ is also a root. The minimal polynomial of $\xi^*$ therefore satisfies
$Q(\xi) = \xi^d Q(1/\xi)$ (palindromic). Writing $u = \xi + 1/\xi$:
$Q(\xi) = \xi^d P(u)$ for a polynomial $P$ of degree $d$ in $u$.

## Why the Spheroidal Equation Lacks This

The spheroidal equation
$(1-x^2)S'' - 2xS' + [A + c^2x^2 - m^2/(1-x^2)]S = 0$
has the symmetry $x \to -x$ (exchange of the regular singularities at $x = \pm 1$).
This is a symmetry of the **independent variable**, giving even/odd eigenfunctions.

The involution $c^2 \to 1/c^2$ acts on the **parameter** (the coefficient of $x^2$).
This is NOT a symmetry of the equation: changing $c^2$ to $1/c^2$ changes the
potential, and $A_\ell(c^2) \neq A_\ell(1/c^2)$ in general.

The vortex palindromic $\xi \to 1/\xi$ also acts on a parameter (the ring position),
but it IS a symmetry because of conformal invariance: the Green's function
$-\log\sigma$ is Möbius-invariant, and the inversion $z \to 1/\bar{z}$ is a
Möbius transformation. The spheroidal equation has no analogous conformal
invariance.

**In summary:**
- Vortex: parameter involution $\xi \to 1/\xi$ IS a symmetry (conformal invariance) → palindromic
- Kerr angular: parameter involution $c^2 \to 1/c^2$ is NOT a symmetry → not palindromic
- Kerr angular: variable involution $x \to -x$ IS a symmetry → even/odd eigenfunctions (but not palindromic in $c^2$)

## What IS True About Kerr

### 1. The horizon ratio identity (exact, non-trivial)

$\rho = r_-/r_+$ satisfies $\rho + 1/\rho = 4/a^{*2} - 2$.

This is an algebraic consequence of $r_\pm = M \pm \sqrt{M^2 - a^2}$ and
$r_- r_+ = a^2$, $r_- + r_+ = 2M$. The palindromic quadratic
$\rho^2 - u\rho + 1 = 0$ with $u = 4/a^{*2} - 2$ encodes the
horizon structure. This is genuine palindromic algebra, but it describes
the **horizon equation** ($\Delta = 0$), not the **eigenvalue equation**.

### 2. The angular $x \to -x$ symmetry (exact, known)

For $s = 0$: eigenfunctions are even or odd, eigenvalues depend on parity.
For $s \neq 0$: the $-2csx$ term breaks the parity symmetry.

### 3. Near-linearity of $P(u)$ (approximate, quantitative)

The function $P(u) = A(c^2) + A(1/c^2)$ (trivially a function of $u$)
is approximately linear in $u$ for low-lying eigenvalues. The deviation
from linearity scales as $\ell^{-5.9}$ for $s = -2$. This is an
empirical observation about the spheroidal eigenvalue's dependence on $c^2$,
not a structural symmetry.

## The Scope of the Palindromic Principle

The palindromic hierarchy requires **conformal invariance** of the Green's function.
This holds for:

1. **The Poincaré disk** ($\mathbf{H}^2$): Möbius group $\text{PSL}(2,\mathbb{R})$ ✓
2. **The Riemann sphere** ($S^2$): Möbius group $\text{PSL}(2,\mathbb{C})$ ✓
3. **The flat plane** ($\mathbb{R}^2$): conformal group (infinite-dimensional) ✓
4. **Any Riemann surface** $\Gamma\backslash\mathbf{H}^2$: inherited from $\mathbf{H}^2$ ✓

It does NOT hold for:

5. **The spheroidal equation** (Kerr angular): no Möbius invariance ✗
6. **The radial Teukolsky equation** (Kerr radial): no conformal invariance ✗
7. **The torus** (rectangular lattice): conformal invariance is present but the
   fundamental domain breaks the Möbius group to a discrete subgroup, and
   $C_1$ becomes mode-dependent (the Havelock identity FAILS on the torus for $N \geq 4$)

The palindromic principle is a **2D conformal** phenomenon. It lives precisely
where the Möbius group acts transitively on the spectral parameter.
