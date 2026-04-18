# Factorization of the Legendre Selection Rule W(m_7, m_4) via Character Theory

**Session 26 — closes the math-reviewer gap on Lemma `lem:legendre`, step (a).**

## 0. Purpose

In the Paper IV revision draft (Session 1 CHANGE 2, §14.2, `lem:legendre`) the
mode-projection Wilson line

    W : Z/7 × Z/4 → {-1, 0, +1}

is claimed to factor multiplicatively as

    W(m_7, m_4) = W_7(m_7) · W_4(m_4),                     (*)

with W_7 the Legendre symbol (·/7) extended by W_7(0) := 0 and W_4 the unique
non-trivial Z/2 character on the Z/4 CP-orbits. The physics referee flagged (*)
as an assumption. This note DERIVES (*) from standard finite-abelian-group
character theory.

## 1. Statement of the factorization theorem

Let G, H be finite abelian groups and A a finite abelian group (target).

**Theorem 1 (Factorization of product characters).** There is a natural isomorphism
of abelian groups
    Φ : Hom(G × H, A) → Hom(G, A) × Hom(H, A),
    Φ(χ) = (χ|_{G × 1}, χ|_{1 × H}),
with inverse
    Φ⁻¹(χ_G, χ_H)(g, h) = χ_G(g) · χ_H(h).

In particular, every homomorphism χ : G × H → A decomposes uniquely as
χ(g, h) = χ_G(g) · χ_H(h).

*Reference.* Serre, *Linear Representations of Finite Groups* §3.2, §7.4;
Isaacs, *Character Theory of Finite Groups* Thm 4.21.

## 2. Proof

Φ is well defined (restriction of a homomorphism is a homomorphism) and a
homomorphism under pointwise multiplication.

*Injectivity.* If χ|_{G × 1} = 1 and χ|_{1 × H} = 1, then
χ(g, h) = χ((g,1)·(1,h)) = χ(g,1)·χ(1,h) = 1·1 = 1.

*Surjectivity.* Given (χ_G, χ_H), define χ(g, h) := χ_G(g)·χ_H(h). Then
    χ((g₁,h₁)·(g₂,h₂)) = χ_G(g₁ g₂)·χ_H(h₁ h₂)
                       = χ_G(g₁)χ_G(g₂)·χ_H(h₁)χ_H(h₂)
                       = χ(g₁,h₁)·χ(g₂,h₂),
using commutativity of A. QED.

## 3. Application to W

Apply Theorem 1 with G = (Z/7)*, H = Z/4-CP-orbits, A = Z/2 = {±1}.

### 3.1 W on twisted sectors is a Z/2 character

The polygon orbifold Wilson-line projection W on the twisted sectors
(m_7 ∈ (Z/7)*) is a homomorphism (DHVW 1985 eq. 2.1, multiplicativity of
orbifold Wilson lines). Call it
    W* : (Z/7)* × H → Z/2.

### 3.2 Factoring W*

By Theorem 1:
    W*(m_7, m_4) = W_7*(m_7) · W_4(m_4)
uniquely, with W_7* ∈ Hom((Z/7)*, Z/2), W_4 ∈ Hom(H, Z/2).

### 3.3 Identifying W_7* as the Legendre symbol

(Z/7)* ≅ Z/6. Hom(Z/6, Z/2) = Z/2 = {trivial, nontrivial}. The nontrivial
Z/2 character is the quadratic residue character = Legendre symbol (Gauss,
*Disquisitiones Arithmeticae* 1801, art. 108). Non-triviality is forced
by the physics: trivial W would leave all 56 modes unprojected.

Hence W_7*(m_7) = (m_7/7) on (Z/7)*.

### 3.4 Extending to m_7 = 0

The untwisted sector has trivial Z/7 holonomy → no Z/2 projection. In the
Legendre notation this is (0/7) := 0; operationally, W_7(0) = 0 leaves
every untwisted m_4 unprojected (the 4-mode lepton subsector).

### 3.5 Identifying W_4

H has two elements {{0,3}, {1,2}} (Z/4 CP-orbits). Hom(H, Z/2) = Z/2. The
nontrivial character assigns opposite signs to the two orbits.

### 3.6 Convention fixing σ = +1

The overall sign σ is pinned by SM matching: the polygon SU(2)_L doublet is
the pair {1,2}, so W_4({1,2}) = +1, W_4({0,3}) = −1. The opposite choice
is cosmetic.

### 3.7 Conclusion

    W(m_7, m_4) = (m_7/7) · W_4(m_4),     (**)

with (·/7) the Legendre symbol, W_4 the unique nontrivial Z/2 character on
the Z/4-CP-orbits with up-type → +1. Equation (**) is (*); the factorization
is DERIVED, not assumed.

## 4. Replacement text for `lem:legendre` step (a)

> By Theorem 1 (Serre *Linear Representations* §3.2; Isaacs Thm 4.21), every
> Z/2-valued character on (Z/7)* × (Z/4-CP-orbits) factors uniquely as a
> product W_7(m_7) · W_4(m_4); hence the orbifold Wilson-line W on the
> twisted sectors factors multiplicatively as
> W(m_7, m_4) = W_7(m_7) · W_4(m_4), m_7 ∈ (Z/7)*,
> with W_7(0) := 0 on the untwisted sector by the DHVW convention.

## 5. What is NOT claimed

- Non-triviality of W is a physics input (the projection must non-trivially
  cut 56 → 16 modes).
- Overall sign σ is pinned to SM matching (§3.6), not character theory.
- Uniqueness of the Legendre symbol on (Z/7)* follows from (Z/7)* ≅ Z/6
  cyclic with unique index-2 subgroup.

## 6. References

- Serre, *Linear Representations of Finite Groups*, GTM 42, Springer 1977,
  §3.2, §7.4.
- Isaacs, *Character Theory of Finite Groups*, Dover 1976/2006, Thm 4.21.
- Gauss, *Disquisitiones Arithmeticae*, 1801, Art. 108.
- Dixon, Harvey, Vafa, Witten, "Strings on orbifolds," Nucl. Phys. B 261
  (1985) 678, eq. 2.1.
