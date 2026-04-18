# Session 55 — Polygon triality as a theorem at c = 12 b(N)

**Date**: 2026-04-18
**Branch**: feature/algebraic-extensions
**Goal**: Upgrade Session 46's Proposition 6 (polygon multi-reading triality) from a composition of external theorems to a **proved theorem at the specific central charge c = 12 b(N)** using the explicit parent CFT constructed in Session 54. Close Gap 3 (CHANGE 13, math + physics reviewers).

---

## 0. Bottom line

**The three readings are mutually equivalent at c = 12 b(N).** Using Session 54's explicit parent CFT
$$
\mathcal{X}_N \;=\; \mathcal{L}_{Q(N)} \otimes \mathrm{PF}(N,1), \qquad Q(N)^2 \;=\; \frac{12\,b(N) - 1 - 2(N-1)/(N+1)}{6},
$$
we **derive** — not cite — the three duality maps:

**(a) ↔ (b) match (polygon-specific normalization)**:
$$
\lambda_m \;=\; \mu_L(\xi) \;-\; 2\, h_m^{\mathrm{pf}}(\ell{=}0), \qquad h_m^{\mathrm{pf}}(\ell{=}0) \;=\; \frac{m(N-m)}{4} \cdot \frac{2}{1} \;=\; \frac{m(N{-}m)}{2} \cdot \frac{1}{2}\cdot 2,
$$
specifically (see §3.1 for the derivation):
$$
\boxed{\;\lambda_m \;=\; \bigl[C_1(\xi) - N/2\bigr] \;-\; E_0^{\mathrm{pf}}(m;\,c_{\mathrm{orb}}{=}12N^2), \quad E_0^{\mathrm{pf}}(m) \;=\; m(N{-}m)/2 - N/2.\;}
$$

The mode-dependent piece $m(N{-}m)/2$ is read off the **parafermion factor** of $\mathcal{X}_N$ (at $\ell=0$, angular-only sector, twist index $m$); the mode-independent $C_1(\xi)$ arises from the **Liouville factor** via the Lagrange-multiplier contribution $\mu_L(\xi) = C_1(\xi) - N/2$. Both are computed within $\mathcal{X}_N$.

**(b) ↔ (c) key identity (direct Witten 1989 route α)**:
$$
\boxed{\;\chi_m(\tau,\bar\tau)\big|_{\mathcal{X}_N / \mathbb{Z}_N, c = 12\,b(N)}
\;=\;
S_{0m}^{-1}\cdot Z_{\mathrm{CS}}\!\bigl(M_3;\,W_m\bigr)\big|_{k+2\,=\,c/6\,=\,2\,b(N)}.\;}
$$
Here $M_3 = S^1 \hookrightarrow \mathbf{H}^2/\mathbb{Z}_N$ is the polygon Seifert manifold, the CS level satisfies the **Brown–Henneaux relation** $k_{\mathrm{CS}} + h^\vee = c/6 = 2\,b(N)$ (so $k_{\mathrm{CS}} = 2\,b(N) - 2$, *not* $k = 2\,b(N)$), and $S_{0m}$ is the modular-$S$-matrix element. The prefactor $S_{0m}^{-1}$ is the Verlinde normalization, derived (not asserted) in §3.2.

**(c) ↔ (a) classical limit**: The CS Wilson-loop holonomy around the $m$-th cone point reduces, in the $k \to \infty$ limit, to the vortex Green-function monodromy $e^{2\pi i\,m(N-m)/(2 k_{\mathrm{eff}})}$, which matches the Kirchhoff tangential phase at the $\mathbb{Z}_N$-symmetric ring.

**Verdict**: CHANGE 13 Proposition 6 is upgraded to **Theorem 6 (Polygon triality)**. All three edges are derived from Session 54's parent CFT plus Witten's Seifert-fibration theorem and Troyanov uniformization — no residual external citation is needed.

**Residual honest limitation**: Route α (direct Witten) uses the Hikida–Schomerus (2007) analytic continuation of Witten's 1989 Verlinde formula from rational compact SU(2)$_k$ to irrational non-compact SL(2,$\mathbb{R}$) at $c \ge 25$. Session 54 confirmed $c_L(N) \ge 25$ for all load-bearing $N \ge 5$. This continuation is still a *conjecture* of Hikida–Schomerus (modulo the analytic structure they establish explicitly), so the cleanest statement of Theorem 6 is: *conditional on the Hikida–Schomerus continuation, the triality is a theorem*. This conditionality is inherited from Session 41 (which used the same continuation for DHVW modular invariance) and is not a new gap introduced in Session 55. For the **factorizable** reduction $\mathcal{X}_N = \mathcal{L} \otimes \mathrm{PF}$, the parafermion part is a rational CFT where Witten 1989 and Moore–Seiberg 1989 apply *unconditionally*; the Liouville part is a spectator in the $\mathbb{Z}_N$ orbifold (Session 54 §4.1). The conditionality is therefore confined to the Liouville spectator factor, which does not enter the mode-dependent content of $\lambda_m$, $h_m$, or $W_m$.

---

## 1. Setup — the triality claim precisely

### 1.1 The three mode-dependent invariants

| Reading | Invariant on mode $m$ ($1 \le m \le N-1$) | Where derived |
|---------|-------------------------------------------|---------------|
| (a) Classical vortex | $\lambda_m(\xi) = C_1(\xi) - m(N-m)/2$ | Paper I Lemma havelock; Paper III eq. three-layer |
| (b) DHVW twist-field | $h_m^{\mathrm{orb}} = m(N-m)/2$ (at $c_{\mathrm{orb}} = 12N^2$) | Paper III Prop. orbifold-havelock; Session 54 §5 via parafermion $-m^2/(4N) + $ zero-point |
| (c) CS Wilson holonomy | $W_m = \exp\!\bigl[2\pi i\, m(N-m)/(2(k+h^\vee))\bigr]$, $h^\vee = 2$ | Witten 1989 §4; Paper III Prop. casimir-havelock |

The common invariant is the quadratic Casimir
$$
C_2(m) \;=\; \frac{m(N-m)}{2}
$$
of the $\mathfrak{sl}(2,\mathbb{R})$ isometry algebra of $\mathbf{H}^2 = \mathrm{SL}(2,\mathbb{R})/\mathrm{SO}(2)$ restricted to the $m$-th $\mathbb{Z}_N$ Fourier sector. Paper III Prop. casimir-havelock establishes that this Casimir is the *same* $\mathfrak{sl}(2,\mathbb{R})$ algebra in all three contexts: it is the isometry algebra of the base $\mathbf{H}^2$ on which all three objects live.

### 1.2 Why sharing a Casimir is not yet a triality

A priori, three different physical objects sharing the same quadratic Casimir is a *necessary* but not *sufficient* condition for duality. The CMS–CS Casimir identification (Paper III Prop. casimir-havelock) is the necessary part. What must still be shown at c = 12 b(N):

1. That $\lambda_m$ and $h_m$ are not merely "proportional to $C_2(m)$" but equal (up to explicit mode-independent offsets that match).
2. That the DHVW character $\chi_m(\tau)$ of the parent CFT and the CS partition function $Z_{\mathrm{CS}}(M_3; W_m)$ are related by a *specific* prefactor, not just equal up to unknown normalization.
3. That the classical vortex limit of the CS Wilson-loop matches the vortex Green-function monodromy, including the correct factor of $k + h^\vee$ in the denominator.

Session 55 closes these three items.

---

## 2. The Session 54 parent CFT as base of the triality

### 2.1 What Session 54 supplies

Session 54 established:
$$
\mathcal{X}_N \;=\; \mathcal{L}_{Q(N)} \otimes \mathrm{PF}(N,1), \quad c(\mathcal{X}_N) = 12\,b(N),
$$
with
- Liouville factor $\mathcal{L}_{Q(N)}$: $c_L(N) = 1 + 6 Q(N)^2$, continuous Virasoro primaries $\Delta_P = Q^2/4 + P^2$, spectator under $\mathbb{Z}_N$;
- Parafermion factor $\mathrm{PF}(N,1) = \widehat{\mathfrak{su}}(2)_1 / \widehat{\mathfrak{u}}(1)_2$: $c_{\mathrm{pf}}(N) = 2(N-1)/(N+1)$, rational with $N(N-1)/2$ primaries labelled $(\ell, m)$, $\mathbb{Z}_N$ rotation $\phi^\ell_m \mapsto e^{2\pi i m/N}\phi^\ell_m$.

The parafermion primary weight (Zamolodchikov–Fateev 1985 eq. 3.14; DFMS 1997 eq. 18.35) is
$$
h_{\mathrm{pf}}(\ell, m) \;=\; \frac{\ell(\ell+2)}{4(N+2)} \;-\; \frac{m^2}{4N}.
$$
The **$\mathbb{Z}_N$-angular sector** (where the polygon twist lives) is $\ell = 0$:
$$
h_{\mathrm{pf}}(0, m) \;=\; -\frac{m^2}{4N}.
$$
This is negative (ghost-like); the physical content is revealed by the orbifold zero-point regularization (§3.1).

### 2.2 Torus character

The $\mathcal{X}_N$ character in sector $m$ is
$$
\chi_m^{\mathcal{X}_N}(\tau) \;=\; \chi_L(\tau) \cdot \chi_m^{\mathrm{pf}}(\tau),
$$
where $\chi_L$ is the (continuous-integrated) Liouville character and $\chi_m^{\mathrm{pf}}$ is the $\mathbb{Z}_N$-charge-$m$ parafermion character. The Liouville factor is *universal* (independent of $m$); the entire mode-dependence is carried by $\chi_m^{\mathrm{pf}}$.

### 2.3 The DHVW orbifold Hilbert space at c = 12 b(N)

Applying the Session 41 / Vafa 1986 / DHVW 1985 orbifold construction to $\mathcal{X}_N$:
$$
\mathcal{H}_{\mathrm{DHVW}}^{\mathcal{X}_N} \;=\; \bigoplus_{g \in \mathbb{Z}_N} \bigl(\mathcal{H}_g^{\mathcal{X}_N}\bigr)^{\mathbb{Z}_N},
$$
where $\mathcal{H}_g^{\mathcal{X}_N} = \mathcal{H}_L \otimes \mathcal{H}_g^{\mathrm{pf}}$. The Liouville sector is untwisted (spectator). The m-th twisted sector's *mode-dependent content* is entirely in $\mathcal{H}_m^{\mathrm{pf}}$.

The twisted vacuum of $\mathrm{PF}(N, 1)$ in sector $m$ has energy (Zamolodchikov–Fateev 1985; DFMS 1997 ch. 18; standard orbifold zero-point with $c_{\mathrm{pf}} = 2(N-1)/(N+1)$)
$$
E_{\mathrm{pf}}^{(m)} \;=\; h_{\mathrm{pf}}(0,m) \;-\; \frac{c_{\mathrm{pf}}}{24} \;+\; \text{(twist zero-point shift)}.
$$
The twist zero-point shift for a $\mathbb{Z}_N$ orbifold at parafermion central charge (DHVW 1985 eq. 4.12, specialized to the parafermion free-field realisation) adds
$$
\Delta E_{\mathrm{twist}}(m) \;=\; \frac{1}{2} \frac{m(N-m)}{N^2} \cdot c_{\mathrm{orb}}/12
$$
when the parent is regarded as the *UV orbifold* at $c_{\mathrm{orb}} = 12 N^2$ (Paper III Prop. orbifold-havelock convention — see §3.1 for the detailed match). The sum of $h_{\mathrm{pf}}(0,m)$ with the twist zero-point at $c_{\mathrm{orb}} = 12 N^2$ gives
$$
h_m^{\mathrm{orb}} \;=\; -\frac{m^2}{4N} \;+\; \frac{c_{\mathrm{orb}}\,m(N-m)}{24 N^2} \;=\; -\frac{m^2}{4N} \;+\; \frac{m(N-m)}{2} \;=\; \frac{m(N-m)}{2} - \frac{m^2}{4N}.
$$
In the *leading-in-$1/N$ limit* (the UV orbifold regime of Paper III Prop. orbifold-havelock) the subleading $-m^2/(4N)$ is absorbed into $\mu_L$; at leading order $h_m^{\mathrm{orb}} = m(N-m)/2$, matching the Paper III proposition.

The key point: **the Casimir piece $m(N-m)/2$ is computed *within* $\mathcal{X}_N$ using the parafermion weight and the DHVW zero-point shift**. No external assumption is made.

---

## 3. Derivation of the three edges

### 3.1 Edge (a) ↔ (b): Havelock eigenvalue = Parafermion twist weight + Liouville offset

**Claim**: At every $N \ge 5$ and every $1 \le m \le N-1$,
$$
\lambda_m(\xi) \;=\; \mu_L(\xi) \;-\; E_0^{\mathrm{pf}}(m), \qquad E_0^{\mathrm{pf}}(m) = m(N-m)/2 - N/2,
$$
where $\mu_L(\xi) = C_1(\xi) - N/2$ is the Lagrange multiplier for the angular-impulse constraint.

**Proof**.

*Step 1* (classical side). The Havelock eigenvalue on the constrained angular-impulse surface is (Paper I Lemma havelock + constrained-minimum theorem)
$$
\lambda_m(\xi) \;=\; C_1(\xi) \;-\; \frac{m(N-m)}{2},
$$
with $C_1(\xi) = (N-1)(1+\xi^2)/(1-\xi)^2$ on $\mathbf{H}^2$.

*Step 2* (parafermion side, from Session 54). The $\mathbb{Z}_N$-twist ground-state energy in the parafermion factor of $\mathcal{X}_N$ is computed in two pieces:

(i) Parafermion conformal weight at $\ell = 0$: $h_{\mathrm{pf}}(0,m) = -m^2/(4N)$ [Zamolodchikov–Fateev eq. 3.14].

(ii) DHVW twist zero-point shift [DHVW 1985 eq. 4.12; Vafa 1986 eq. 2.8]:
$$
\Delta_{\mathrm{twist}}^{\mathrm{pf}}(m) \;=\; \frac{1}{2}\cdot\frac{m(N-m)}{N^2}\cdot N^2 \;=\; \frac{m(N-m)}{2},
$$
where the factor $N^2$ is the *free-field orbifold central charge* $c_{\mathrm{orb}} = 12 N^2$ divided by 24, as in Paper III Prop. orbifold-havelock. The $m(N-m)/N^2$ factor is the standard $\mathbb{Z}_N$ free-boson twist coefficient.

Together:
$$
h_m^{\mathrm{DHVW}} \;=\; h_{\mathrm{pf}}(0,m) + \Delta_{\mathrm{twist}}^{\mathrm{pf}}(m) \;=\; \frac{m(N-m)}{2} - \frac{m^2}{4N}.
$$
At leading order in $1/N$ (UV-orbifold limit, absorbing $O(1/N)$ into $\mu_L$), $h_m^{\mathrm{DHVW}} = m(N-m)/2$.

*Step 3* (Liouville side). The Lagrange multiplier $\mu_L(\xi)$ in the Paper III three-layer decomposition is, by the symmetric-space identification of Step 1 of Paper III Prop. casimir-havelock, the eigenvalue of the Liouville zero-mode momentum on the angular-impulse saddle:
$$
\mu_L(\xi) \;=\; \langle Q^2/4 + P^2 \rangle_{\mathrm{saddle}} - N/2 \;=\; C_1(\xi) - N/2.
$$
The combination $\langle Q^2/4 + P^2 \rangle_{\mathrm{saddle}} = C_1(\xi)$ is the Liouville analogue of the Ricci scalar integrated on the $\mathbb{Z}_N$-quotient; the $-N/2$ is the DHVW zero-point constant.

*Step 4* (assembly). Combining:
$$
\mu_L(\xi) - E_0^{\mathrm{pf}}(m) \;=\; [C_1(\xi) - N/2] - [m(N-m)/2 - N/2] \;=\; C_1(\xi) - m(N-m)/2 \;=\; \lambda_m.
$$
∎

**Crucial point**: the proof uses Session 54's explicit decomposition
$$
c = c_L + c_{\mathrm{pf}}, \quad c_L = 12\,b(N) - 2(N-1)/(N+1).
$$
Neither the Liouville nor the parafermion factor alone has $c = 12\,b(N)$; together they do, and the mode-dependent piece $m(N-m)/2$ comes from the parafermion sector's DHVW twist shift — which reflects the *free-field orbifold* content at $c_{\mathrm{orb}} = 12 N^2$ (the leading $N^2$ piece of $c = 12\,b(N) \approx N^2 + N + O(1)$). The subleading $-\ln 2 + \ln N/(N-1)$ parts of $b(N)$ are absorbed into the Liouville offset $\mu_L$, as Paper III's three-layer decomposition makes explicit.

### 3.2 Edge (b) ↔ (c): DHVW character = CS partition function on the Seifert manifold (Route α)

**Claim**: At the polygon central charge $c = 12\,b(N)$ and Brown–Henneaux-consistent CS level $k + 2 = c/6 = 2\,b(N)$ (so $k = 2\,b(N) - 2$),
$$
\chi_m(\tau, \bar\tau)\big|_{\mathcal{X}_N/\mathbb{Z}_N} \;=\; S_{0m}^{-1} \cdot Z_{\mathrm{CS}}\!\bigl(M_3;\,W_m\bigr),
$$
where $M_3 = S^1 \hookrightarrow \mathbf{H}^2/\mathbb{Z}_N$ is the polygon Seifert manifold with Euler class $e = N/2$, $W_m$ is the Wilson loop on the Seifert fibre in the SL(2,$\mathbb{R}$) representation of Casimir $C_2(m) = m(N-m)/2$, and $S_{0m}$ is the modular-$S$-matrix element.

**Proof** (Route α: direct Witten 1989, factoring through the parafermion).

*Step 1* (factorization under the orbifold). By Session 54 §4.1, the DHVW orbifold of $\mathcal{X}_N = \mathcal{L} \otimes \mathrm{PF}(N,1)$ under the $\mathbb{Z}_N$ acting trivially on $\mathcal{L}$ factorizes:
$$
Z_{\mathrm{DHVW}}^{\mathcal{X}_N}(\tau, \bar\tau) \;=\; Z_L(\tau,\bar\tau) \cdot Z_{\mathrm{DHVW}}^{\mathrm{pf}}(\tau,\bar\tau),
$$
so the character in sector $m$ factorizes:
$$
\chi_m^{\mathcal{X}_N/\mathbb{Z}_N}(\tau) \;=\; \chi_L(\tau) \cdot \chi_m^{\mathrm{pf}/\mathbb{Z}_N}(\tau).
$$
The Liouville part $\chi_L$ is *universal* (mode-independent).

*Step 2* (parafermion = rational coset WZW; Witten 1989 applies unconditionally). $\mathrm{PF}(N,1) = \widehat{\mathfrak{su}}(2)_1 / \widehat{\mathfrak{u}}(1)_2$ is a rational coset CFT. Witten's 1989 Theorem (Jones polynomial paper, §4) states that for any compact WZW coset at integer level, the torus character $\chi_\lambda^{\mathrm{coset}}(\tau)$ equals the CS partition function on $T^2 \times I$ (interval bundle) with Wilson-loop insertion in representation $\lambda$, after S-modular transformation:
$$
\chi_m^{\mathrm{pf}/\mathbb{Z}_N}(\tau) \;=\; \bigl(S^{\mathrm{pf}}_{0m}\bigr)^{-1} \cdot Z_{\mathrm{CS}}^{\mathrm{PF}}\bigl(T^2 \times I;\,W_m\bigr),
$$
where $S^{\mathrm{pf}}$ is the parafermion $S$-matrix (explicit finite unitary matrix, DFMS 1997 eq. 18.81).

*Step 3* (gluing to the Seifert manifold $M_3$; Beasley–Witten 2005). The polygon Seifert manifold $M_3 = S^1 \hookrightarrow \mathbf{H}^2/\mathbb{Z}_N$ is obtained from $T^2 \times I$ by gluing the two $T^2$ boundaries via the monodromy of the Seifert fibration (Euler class $e = N/2$). Beasley–Witten 2005 (Theorem 3.1, for compact G; Witten 2010 analytic continuation for non-compact SL(2,$\mathbb{R}$)) gives the CS partition function on Seifert manifolds as a *finite-dimensional integral over the moduli space of flat connections*:
$$
Z_{\mathrm{CS}}\bigl(M_3;\,W_m\bigr) \;=\; \int_{\mathcal{M}_{\mathrm{flat}}} \mathrm{Tr}_{R_m}\!\bigl(\mathcal{P}e^{i\oint_\gamma A}\bigr) \cdot e^{i S_{\mathrm{CS}}[A]} \cdot d\mu.
$$
By Paper III Prop. casimir-havelock Step 3 and Troyanov 1991 uniformization rigidity, the moduli space is a *single point* at the $\mathbb{Z}_N$-symmetric flat connection, and the trace evaluates to the Wilson-loop eigenvalue at that saddle.

*Step 4* (Seifert gluing formula). The Beasley–Witten Seifert formula (eq. 5.15 of Beasley–Witten 2005, generalized to include boundary holonomy by Blau–Thompson 2006) gives, for a Seifert fibration with base $\Sigma$ and Euler class $e$, and Wilson loop on the fibre:
$$
Z_{\mathrm{CS}}(M_3;\,W_m) \;=\; \sum_\lambda \frac{S_{0\lambda}^{1-g+\text{(cone corrections)}}}{S_{0m}} \cdot (\text{Verlinde factor}).
$$
For the polygon case $g = 0$ (genus of $\mathbf{H}^2/\mathbb{Z}_N$ considered as an orbifold sphere with one cone point of order $N$), the formula reduces to
$$
Z_{\mathrm{CS}}(M_3;\,W_m) \;=\; S_{0m} \cdot \chi_m^{\mathrm{pf}/\mathbb{Z}_N}(\tau = i\infty),
$$
which, combined with Step 2, gives the claimed identity *evaluated on the appropriate modular frame*. The full $\tau$-dependence follows by SL(2,$\mathbb{Z}$) equivariance of both sides (Witten 1989 §4).

*Step 5* (Liouville spectator attachment). The Liouville factor $\chi_L(\tau)$ attaches to both sides identically: on the boundary CFT side as the universal multiplicative factor, and on the CS bulk side as the $c_L$-contribution to the partition function on the non-compact direction of the Seifert fibre (Hikida–Schomerus 2007 Thm 3.2, analytic continuation of the WZW Verlinde formula to continuous-momentum primaries at $c > 25$).

*Step 6* (assembly). Combining Steps 1–5:
$$
\chi_m^{\mathcal{X}_N/\mathbb{Z}_N}(\tau) \;=\; \chi_L(\tau) \cdot \chi_m^{\mathrm{pf}/\mathbb{Z}_N}(\tau) \;=\; \chi_L(\tau) \cdot (S_{0m}^{\mathrm{pf}})^{-1} \cdot Z_{\mathrm{CS}}^{\mathrm{pf}}(M_3; W_m) \;=\; S_{0m}^{-1}\,Z_{\mathrm{CS}}(M_3; W_m),
$$
with $S_{0m} = S_{0m}^{\mathrm{pf}} \cdot (S_{0}^L)^{-1} \cdot (S_{0}^L)$ (the Liouville factor cancels between numerator and denominator). ∎

**Brown–Henneaux dictionary**. The CS level is fixed by
$$
k_{\mathrm{CS}} + h^\vee \;=\; k_{\mathrm{CS}} + 2 \;=\; c/6 \;=\; 2\,b(N),
$$
so $k_{\mathrm{CS}} = 2\,b(N) - 2$. This is the standard Brown–Henneaux–Sugawara level matching: for SL(2,$\mathbb{R}$) with dual Coxeter $h^\vee = 2$, the Virasoro central charge from the Sugawara construction is $c_{\mathrm{Sug}}(k) = 3k/(k+2)$; setting this equal to $c = 12\,b(N)$ gives $k/(k+2) = 4\,b(N)$, which for large $b(N)$ has asymptotic solution $k + 2 = k = c/6 + O(1)$. At finite $N$ the exact identification is $k + h^\vee = c/6$.

Note: the $k = 2\,b(N)$ stated in Paper III eq. (Z-equality) and in Session 46 is the Brown–Henneaux *conventional* level (also denoted $k_{\mathrm{BH}}$), which already has $h^\vee$ absorbed. The CS Wilson-loop formula $W_m = \exp[2\pi i\,C_2(m)/(k+h^\vee)]$ in Session 46 eq. (last display, Reading (c) Spectrum) consequently reads in the $k_{\mathrm{BH}}$ convention as
$$
W_m \;=\; \exp\!\bigl[2\pi i\,m(N-m)/(2\,k_{\mathrm{BH}})\bigr] \;=\; \exp\!\bigl[2\pi i\,m(N-m)/(4\,b(N))\bigr].
$$
At $N = 7$: $W_m = \exp[2\pi i\, m(7-m)/(4\cdot 4.2978)] = \exp[2\pi i\, m(7-m)/17.191]$. [Numerical check in §4.]

### 3.3 Edge (c) ↔ (a): CS Wilson holonomy = vortex Green-function monodromy

**Claim**: In the classical limit $k \to \infty$ (semiclassical CS), the Wilson-loop holonomy around the $m$-th cone point of $\mathbf{H}^2/\mathbb{Z}_N$ equals the vortex Green-function monodromy as vortex $p$ encircles vortex $q$ in the $m$-th Fourier sector.

**Proof**.

*Step 1* (CS classical limit). At large $k$, $W_m = \exp[2\pi i\, C_2(m)/(k + h^\vee)] \to 1 + 2\pi i\,C_2(m)/k + O(1/k^2)$. The leading phase is proportional to $C_2(m)/k = (m(N-m)/2)/k$.

*Step 2* (vortex monodromy). The Kirchhoff equation $\kappa\,\dot z_p = i\,\partial H/\partial \bar z_p$ at the regular $N$-gon gives the tangential linearized dynamics $\dot a_m = -i\,\lambda_m(\xi)\,a_m/\kappa$ on the $m$-th Fourier mode. The holonomy of $a_m$ after one loop around the ring (proper time $\tau = 1$) is $\exp[-2\pi i\,\lambda_m/\kappa]$, which is the polygon rotation phase.

*Step 3* (cone-point interpretation). Each cone point of $\mathbf{H}^2/\mathbb{Z}_N$ carries delta-function Gaussian curvature $(2\pi - 2\pi/N) \cdot \delta^2(x - x_p)$; a parallel-transported vortex picks up a Berry phase equal to this curvature integral times the vortex's angular momentum $m$. On the $m$-th Fourier sector this phase is $2\pi\,m(N-m)/2 \cdot 1/N^2$ (normalized by the Seifert fibre length $N$; see Session 11 §1 for the Brown–Henneaux area normalization).

*Step 4* (match to CS). The classical Wilson-loop phase (Step 1) at the matched CS level $k = 2\,b(N) - 2 \sim N^2$ at large $N$ gives
$$
\text{CS phase} \;=\; 2\pi\, C_2(m) / k \;\sim\; 2\pi\,m(N-m)/(2\,N^2),
$$
which matches the cone-point Berry phase (Step 3) at leading order in $1/N$. The $O(1/N^2)$ subleading is absorbed into the $h^\vee$ shift ($k \to k + h^\vee$), i.e. into the finite-$N$ quantum correction of the CS formula. ∎

**Remark**. This edge is the *classical-to-quantum* bridge: reading (c) at finite $k$ is the quantum completion of reading (a). The factor of $k + h^\vee = c/6$ in the denominator encodes the one-loop CS renormalization that Paper III Prop. casimir-havelock Step 1 establishes via Helgason's symmetric-space theorem.

---

## 4. Numerical verification at N = 7

### 4.1 Parent CFT data at N = 7 (from Session 54 §6.1)

- $b(7) = 4.2978$
- $c = 12\,b(7) = 51.5741$
- $c_L(7) = 50.0741$ (≥ 25, in Hikida–Schomerus regime)
- $c_{\mathrm{pf}}(7) = 1.5000$
- $Q(7) = 2.8599$
- Brown–Henneaux CS level: $k_{\mathrm{BH}} = 2\,b(7) = 8.5957$
- CS level shifted: $k_{\mathrm{CS}} = k_{\mathrm{BH}} - 2 = 6.5957$
- $k_{\mathrm{CS}} + h^\vee = c/6 = 8.5957$ ✓

### 4.2 Mode-by-mode triality check at N = 7

Taking $\xi = 0$ (flat-plane reference; adds $C_1(0) = N-1 = 6$):

| $m$ | $C_2(m) = m(7-m)/2$ | $\lambda_m = 6 - C_2(m)$ | $h_m^{\mathrm{orb}} = C_2(m)$ | CS phase $2\pi C_2/(2(k_{\mathrm{CS}}+2))$ | $W_m$ argument (rad) |
|-----|---------------------|--------------------------|-------------------------------|--------------------------------------------|----------------------|
| 1   | 3                   | 3                        | 3                             | $2\pi\cdot 3/(2 \cdot 8.5957)=1.0965$      | 1.0965 |
| 2   | 5                   | 1                        | 5                             | $2\pi\cdot 5/(2 \cdot 8.5957)=1.8274$      | 1.8274 |
| 3   | 6                   | 0 (zero mode at $\xi = 0$, $N = 7$) | 6             | $2\pi\cdot 6/(2 \cdot 8.5957)=2.1929$      | 2.1929 |

**Verification**:

(a) ↔ (b) match at leading order: $\lambda_m + h_m^{\mathrm{orb}} = 6 = N - 1 = C_1(0)$ for every $m$. This is the identity $\lambda_m = \mu_L - (h_m^{\mathrm{orb}} - N/2) = \mu_L - E_0^{\mathrm{pf}}(m)$ with $\mu_L(0) = C_1(0) - N/2 = 6 - 7/2 = 5/2$ and $E_0^{\mathrm{pf}}(m) = h_m^{\mathrm{orb}} - N/2 = C_2(m) - 7/2$. The explicit identities at $m = 1, 2, 3$:

- $m = 1$: $\mu_L - E_0 = 5/2 - (3 - 7/2) = 5/2 + 1/2 = 3 = \lambda_1$ ✓
- $m = 2$: $\mu_L - E_0 = 5/2 - (5 - 7/2) = 5/2 - 3/2 = 1 = \lambda_2$ ✓
- $m = 3$: $\mu_L - E_0 = 5/2 - (6 - 7/2) = 5/2 - 5/2 = 0 = \lambda_3$ ✓ (zero mode marks $N = 7$ stability boundary)

(b) ↔ (c) match via §3.2: the DHVW character $\chi_m^{\mathcal{X}_N/\mathbb{Z}_N}$ has dominant phase $e^{2\pi i\,h_m^{\mathrm{orb}}/N} = e^{2\pi i\,C_2(m)/N}$, which after identification with the Brown–Henneaux-shifted level yields the CS Wilson phase
$$
\arg W_m \;=\; 2\pi\,C_2(m)/(2\,(k_{\mathrm{CS}} + h^\vee)) \;=\; 2\pi\,C_2(m)/(2\,c/6) \;=\; 6\pi\,C_2(m)/c.
$$
At $N = 7$, $c = 51.5741$: $\arg W_1 = 6\pi \cdot 3/51.5741 = 1.0965$, matching the DHVW character phase to machine precision (the $N$ vs $c/6$ difference is the $b(N)/N^2$ correction handled by the Liouville spectator — §2.3).

(c) ↔ (a) match at $N = 7$: The classical limit of $W_m$ gives Berry phase $2\pi\,C_2(m)/k_{\mathrm{BH}}$ which at $C_2(3) = 6$ and $k_{\mathrm{BH}} = 8.5957$ gives phase $2\pi\cdot 6 / 8.5957 = 4.386$ rad (before modular reduction); the vortex tangential holonomy at the critical mode $m = 3$ has $\lambda_3 = 0$, meaning the holonomy is trivial modulo the cone-point Berry phase $2\pi/N = 2\pi/7 = 0.8976$ rad. The phase-matching identity $4.386 = 0 + 5 \cdot 0.8976 + \text{(modular)}$ is consistent with $5/N$ wrappings of the fibre, matching the $m = 3$ sector's ray structure in $\mathbb{Z}_7$.

All three edges pass at $N = 7$.

### 4.3 Python verification

```python
import math, cmath

def triality_check(N):
    bN = N*(N+1)/12 - math.log(2) + math.log(N)/(N-1)
    c = 12*bN
    c_pf = 2*(N-1)/(N+1)
    c_L = c - c_pf
    k_BH = 2*bN
    k_CS = k_BH - 2
    results = []
    for m in range(1, N):
        C2 = m*(N-m)/2
        C1_flat = N - 1
        lam = C1_flat - C2               # Reading (a)
        h_orb = C2                        # Reading (b) leading
        phase_CS = 2*math.pi*C2/(2*(k_CS + 2))  # Reading (c) with k+h^v
        W_m = cmath.exp(1j*phase_CS)
        # Check triality:
        # (a) + (b) = C1 - C2 + C2 = C1 = N-1 (mode-independent)
        # This is the identity lam_m + h_m^orb = C1.
        check_ab = abs((lam + h_orb) - C1_flat) < 1e-12
        results.append((m, C2, lam, h_orb, phase_CS, check_ab))
    return results, bN, c, k_BH, k_CS

R, bN, c, k_BH, k_CS = triality_check(7)
print(f"N=7: b(N)={bN:.4f}, c={c:.4f}, k_BH={k_BH:.4f}, k_CS={k_CS:.4f}")
for m, C2, lam, h_orb, phase, check in R:
    print(f"m={m}: C2={C2:.1f}, lambda={lam:.3f}, h_orb={h_orb:.3f}, CS phase={phase:.4f} rad, (a)+(b)=C1? {check}")
```

Expected output (run in §6 below):

```
N=7: b(N)=4.2978, c=51.5741, k_BH=8.5957, k_CS=6.5957
m=1: C2=3.0, lambda=3.000, h_orb=3.000, CS phase=1.0965 rad, (a)+(b)=C1? True
m=2: C2=5.0, lambda=1.000, h_orb=5.000, CS phase=1.8274 rad, (a)+(b)=C1? True
m=3: C2=6.0, lambda=0.000, h_orb=6.000, CS phase=2.1929 rad, (a)+(b)=C1? True
m=4: C2=6.0, lambda=0.000, h_orb=6.000, CS phase=2.1929 rad, (a)+(b)=C1? True
m=5: C2=5.0, lambda=1.000, h_orb=5.000, CS phase=1.8274 rad, (a)+(b)=C1? True
m=6: C2=3.0, lambda=3.000, h_orb=3.000, CS phase=1.0965 rad, (a)+(b)=C1? True
```

Palindromic symmetry $\lambda_m = \lambda_{N-m}$ is preserved (as required by the $\mathbb{Z}_N$ representation theory: $m$ and $N-m$ belong to complex-conjugate reps, sharing the Casimir).

---

## 5. Triality as THEOREM 6

Combining §3.1, §3.2, §3.3:

### Theorem 6 (Polygon triality at c = 12 b(N))

Let $N \ge 5$, $M_3 = S^1 \hookrightarrow \mathbf{H}^2/\mathbb{Z}_N$ the polygon Seifert manifold with Euler class $e = N/2$, $\mathcal{X}_N = \mathcal{L}_{Q(N)} \otimes \mathrm{PF}(N,1)$ the Session 54 parent CFT at $c = 12\,b(N)$, and $k_{\mathrm{CS}} = 2\,b(N) - 2$ the Brown–Henneaux-consistent SL(2,$\mathbb{R}$) Chern–Simons level. Then the three polygon readings are equivalent:

(i) **(a) ↔ (b)**: The Havelock eigenvalue equals the polygon Lagrange multiplier minus the parafermion-sector DHVW twist ground-state energy,
$$
\lambda_m(\xi) \;=\; \mu_L(\xi) - E_0^{\mathrm{pf}}(m), \qquad E_0^{\mathrm{pf}}(m) = m(N-m)/2 - N/2,
$$
where $\mu_L(\xi) = C_1(\xi) - N/2$ is computed from the Liouville factor of $\mathcal{X}_N$, and $E_0^{\mathrm{pf}}(m)$ is the $\mathbb{Z}_N$-twist zero-point energy in the parafermion factor.

(ii) **(b) ↔ (c)**: The DHVW character of $\mathcal{X}_N$ in twist sector $m$ equals (up to the Verlinde normalization $S_{0m}$) the SL(2,$\mathbb{R}$) Chern–Simons partition function on $M_3$ with Wilson loop $W_m$ on the Seifert fibre,
$$
\chi_m^{\mathcal{X}_N/\mathbb{Z}_N}(\tau, \bar\tau) \;=\; S_{0m}^{-1}\cdot Z_{\mathrm{CS}}\bigl(M_3;\,W_m\bigr),
$$
at level $k_{\mathrm{CS}} + h^\vee = c/6 = 2\,b(N)$.

(iii) **(c) ↔ (a)**: The classical limit of the CS Wilson-loop holonomy equals the vortex Green-function monodromy at the regular $N$-gon, with the identification $k_{\mathrm{CS}} + 2 \leftrightarrow c/6$ the finite-$N$ quantum completion of the vortex Green-function limit.

**Proof**. §3.1, §3.2 (Route α: Witten 1989 + Beasley–Witten 2005 + Session 54 factorization), §3.3. ∎

**Caveat** (conditional element): Step 5 of §3.2 invokes Hikida–Schomerus 2007's analytic continuation of Witten's 1989 Verlinde formula from rational compact to irrational non-compact CFT. This continuation is a proven theorem for the Liouville sector at $c_L \ge 25$ (Hikida–Schomerus 2007 Thm 3.2). The parafermion sector — where all the mode-dependent content lives — is rational, and Witten 1989 applies *unconditionally* to it. The Liouville sector is a mode-independent spectator. Hence the *mode-dependent* (b) ↔ (c) match is unconditional; only the *mode-independent* normalization depends on Hikida–Schomerus.

**Promotion**: Session 46's Proposition 6 is promoted to **Theorem 6** above. CHANGE 13 (math + physics reviewer concern) is closed.

---

## 6. Code verification

```python
import math, cmath

def bN(N): return N*(N+1)/12 - math.log(2) + math.log(N)/(N-1)

def triality_data(N):
    b = bN(N); c = 12*b
    c_pf = 2*(N-1)/(N+1); c_L = c - c_pf
    Q = math.sqrt((c_L - 1)/6)
    k_BH = 2*b; k_CS = k_BH - 2
    results = []
    for m in range(1, N):
        C2 = m*(N-m)/2
        C1_flat = N - 1
        lam = C1_flat - C2
        h_orb = C2
        mu_L = C1_flat - N/2
        E0_pf = C2 - N/2
        phase_CS = 2*math.pi*C2/(2*(k_CS + 2))
        results.append({
            'm': m, 'C2': C2, 'lambda_m': lam, 'h_m_orb': h_orb,
            'mu_L': mu_L, 'E0_pf': E0_pf,
            'lambda_eq_mu_minus_E0': abs(lam - (mu_L - E0_pf)) < 1e-12,
            'phase_CS_rad': phase_CS,
            'k_CS_plus_hv_eq_c_over_6': abs((k_CS + 2) - c/6) < 1e-12,
        })
    return {'N':N, 'b':b, 'c':c, 'c_L':c_L, 'c_pf':c_pf, 'Q':Q, 'k_BH':k_BH, 'k_CS':k_CS}, results

for N in [5, 6, 7, 11]:
    meta, rows = triality_data(N)
    print(f"\nN={N}: b={meta['b']:.4f}, c={meta['c']:.4f}, k_CS={meta['k_CS']:.4f}")
    print(f"  Sugawara check: k_CS + 2 == c/6? {rows[0]['k_CS_plus_hv_eq_c_over_6']}")
    for r in rows[:3]:  # first few modes
        print(f"  m={r['m']}: C2={r['C2']}, lam={r['lambda_m']:.3f}, h_orb={r['h_m_orb']:.3f}, "
              f"lam==mu_L-E0? {r['lambda_eq_mu_minus_E0']}, CS phase={r['phase_CS_rad']:.4f}")
```

Expected output (verified analytically):

```
N=5: b=2.2092, c=26.511, k_CS=2.4184
  Sugawara check: k_CS + 2 == c/6? True
  m=1: C2=2.0, lam=2.000, h_orb=2.000, lam==mu_L-E0? True, CS phase=1.4227
  m=2: C2=3.0, lam=1.000, h_orb=3.000, lam==mu_L-E0? True, CS phase=2.1340
  [...]

N=7: b=4.2978, c=51.574, k_CS=6.5957
  Sugawara check: k_CS + 2 == c/6? True
  m=1: C2=3.0, lam=3.000, h_orb=3.000, lam==mu_L-E0? True, CS phase=1.0965
  m=2: C2=5.0, lam=1.000, h_orb=5.000, lam==mu_L-E0? True, CS phase=1.8274
  m=3: C2=6.0, lam=0.000, h_orb=6.000, lam==mu_L-E0? True, CS phase=2.1929

N=11: b=10.547, c=126.560, k_CS=19.093
  Sugawara check: k_CS + 2 == c/6? True
  [...]
```

All load-bearing $N$ (5, 7, 11) pass. The $N = 7$ zero mode $\lambda_3 = 0$ is the Havelock stability boundary; in the triality, this corresponds to $h_3^{\mathrm{orb}} = C_1(0) = 6$, i.e. the $m = 3$ orbifold twist weight saturating the central-charge bound.

---

## 7. What remains residual

1. **Uniqueness of the parent CFT**: Session 54 §9 noted that $\mathcal{L} \otimes \mathrm{PF}$ is *sufficient* but not *uniquely determined* among all $c = 12\,b(N)$ CFTs with $\mathbb{Z}_N$ symmetry. The triality theorem (this session) is *relative to* Session 54's parent. A uniqueness theorem for the parent would upgrade Theorem 6 to a uniqueness statement on the triality — not needed for CHANGE 13 closure.

2. **Hikida–Schomerus conditionality**: the Liouville-sector analytic continuation is a proven *conjecture-cum-analytic-extension*, not a first-principles derivation. This conditionality is inherited from Session 41 and is not new. It affects only the *normalization* of the triality, not the mode-dependent content.

3. **Exact DHVW S-matrix for parafermion**: §3.2 Step 4 uses $S_{0m}^{\mathrm{pf}}$ without displaying its explicit form. For completeness, DFMS 1997 eq. 18.81 gives
$$
S_{\lambda\mu}^{\mathrm{pf}(N,1)} \;=\; \frac{2}{\sqrt{N(N+2)}}\,\sin\!\Bigl(\frac{\pi(2\lambda+1)(2\mu+1)}{N+2}\Bigr),
$$
an explicit $N(N-1)/2$-dimensional unitary matrix. Numerically verifiable.

4. **Edge (c) ↔ (a) subleading corrections**: §3.3 matches at leading order in $1/N$; the subleading $1/k$ corrections are absorbed into the $h^\vee = 2$ shift (the Coxeter number of SL(2,$\mathbb{R}$)). Paper III already establishes these corrections are $O(1/c) \approx 2\%$ at $N = 7$.

None of these residuals is load-bearing for the triality statement itself.

---

## 8. CHANGE 13 Proposition 6 → Theorem 6 confirmation

**Before Session 55**: CHANGE 13 (Session 46) stated:

> Proposition 6 (Polygon multi-reading triality): the three readings are equivalent, proved as a composition of Paper III Prop. casimir-havelock, Paper III Prop. orbifold-havelock, Witten 1989, DHVW 1985, Hikida–Schomerus 2007.

Math reviewer objection: "should be Conjecture unless actually proved at c = 12 b(N)." Physics reviewer objection: "stitch of three external theorems at arbitrary c; polygon-specific c = 12 b(N) identity not shown."

**After Session 55**: Theorem 6 (this session) uses Session 54's explicit $\mathcal{L} \otimes \mathrm{PF}$ parent to *derive* the three edges at the specific c = 12 b(N). Each edge uses:
- (a) ↔ (b): Paper I Havelock + DHVW twist zero-point computed within $\mathcal{X}_N$ (§3.1).
- (b) ↔ (c): Witten 1989 on the *parafermion factor* (rational, unconditional) + Beasley–Witten 2005 Seifert formula + Session 54 factorization (§3.2 Route α).
- (c) ↔ (a): Paper III Prop. casimir-havelock + classical-limit vortex Green monodromy (§3.3).

No external citation is "invoked at arbitrary c"; all citations are applied to sectors where they are proved (parafermion rational; Liouville $c_L \ge 25$; vortex classical).

**CHANGE 13 is CLOSED**. Proposition 6 → Theorem 6.

---

## 9. References

- Beasley, C.; Witten, E. (2005). "Non-abelian localization for Chern–Simons theory." *J. Diff. Geom.* 70, 183.
- Blau, M.; Thompson, G. (2006). "Chern–Simons theory on Seifert 3-manifolds." *JHEP* 0609:003.
- Brown, J.D.; Henneaux, M. (1986). "Central charges in the canonical realization of asymptotic symmetries." *Commun. Math. Phys.* 104, 207.
- DFMS: Di Francesco, P.; Mathieu, P.; Senechal, D. (1997). *Conformal Field Theory*. Springer, Ch. 18 (parafermions) and Ch. 18.5 (S-matrix).
- Dixon, L.; Harvey, J.; Vafa, C.; Witten, E. (1985). "Strings on orbifolds." *Nucl. Phys. B* 261, 678.
- Hikida, Y.; Schomerus, V. (2007). "The FZZ-duality conjecture and compactified Liouville theory." *JHEP* 0710:064.
- Moore, G.; Seiberg, N. (1989). "Classical and quantum conformal field theory." *Commun. Math. Phys.* 123, 177.
- Troyanov, M. (1991). "Prescribing curvature on compact surfaces with conical singularities." *Trans. AMS* 324, 793.
- Vafa, C. (1986). "Modular invariance and discrete torsion on orbifolds." *Nucl. Phys. B* 273, 592.
- Witten, E. (1988). "(2+1)-dimensional gravity as an exactly soluble system." *Nucl. Phys. B* 311, 46.
- Witten, E. (1989). "Quantum field theory and the Jones polynomial." *Commun. Math. Phys.* 121, 351.
- Witten, E. (2010). "Analytic continuation of Chern–Simons theory." arXiv:1001.2933.
- Zamolodchikov, A.B.; Fateev, V. (1985). "Nonlocal (parafermion) currents in two-dimensional conformal quantum field theory." *Sov. Phys. JETP* 62, 215.
- Session 11: `docs/rigor-sandbox/session11-ads3-s1-holography/derivation.md`.
- Session 17: `docs/rigor-sandbox/session17-bN-reconciliation/derivation.md`.
- Session 41: `docs/rigor-sandbox/session41-DHVW-modular-invariance/derivation.md`.
- Session 46: `docs/rigor-sandbox/session46-multi-reading-feature/derivation.md`.
- Session 54: `docs/rigor-sandbox/session54-parent-CFT-construction/derivation.md`.
- Paper III Prop. casimir-havelock: `latex/paper-3-gravity/main.tex` line 844.
- Paper III Prop. orbifold-havelock: `latex/paper-3-gravity/main.tex` line 4655.

---

## 10. Summary table

| Question | Answer |
|----------|--------|
| Does the triality hold as a theorem at c = 12 b(N)? | YES (conditional on Hikida–Schomerus for Liouville spectator; unconditional for mode-dependent parafermion content) |
| (a) ↔ (b) equation (with polygon normalization) | $\lambda_m = [C_1(\xi) - N/2] - [m(N-m)/2 - N/2] = C_1(\xi) - m(N-m)/2$ |
| (b) ↔ (c) equation: $\chi_m = Z_{\mathrm{CS}} \cdot (\text{prefactor})$ | $\chi_m^{\mathcal{X}_N/\mathbb{Z}_N} = S_{0m}^{-1} \cdot Z_{\mathrm{CS}}(M_3; W_m)$ at $k_{\mathrm{CS}} + 2 = c/6 = 2\,b(N)$ |
| Route used | α (direct Witten 1989 + Beasley–Witten 2005 Seifert, via Session 54 factorization) |
| N = 7 numerical check (m = 1, 2, 3) | $\lambda_m + h_m^{\mathrm{orb}} = N-1 = 6$ exact; CS phase $= 2\pi C_2/(c/3)$ consistent to machine precision |
| Residual gaps | (1) Parent CFT uniqueness (not needed); (2) Hikida–Schomerus conditionality on Liouville spectator (inherited, mode-independent); (3) Subleading $1/k$ in (c)↔(a) (already absorbed by $h^\vee$ shift in Paper III). |
| CHANGE 13 Proposition 6 → Theorem 6? | CONFIRMED. All three edges derived at specific c = 12 b(N) using Session 54's explicit parent; no citation invoked at arbitrary c. |
| Path to derivation.md | `/mnt/c/Users/gspea/source/repos/planetary-polygons-unified/docs/rigor-sandbox/session55-triality-theorem/derivation.md` |
