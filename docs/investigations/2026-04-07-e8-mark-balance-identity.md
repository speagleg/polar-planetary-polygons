# The E₈ Mark-Balance Identity

## Discovery Date: 2026-04-07

## The Identity

The marks of the affine E₈ Dynkin diagram (= I* irrep dimensions) satisfy:

    Σ dᵢ(dᵢ - 4) = 0

where dᵢ = (1, 2, 3, 4, 5, 6, 4, 2, 3).

This is **unique to E₈** among all ADE types (E₆ and E₇ both give -24).

## Equivalent Forms

- Σ dᵢ² = 4 Σ dᵢ (second moment = 4 × first moment)
- |I*| = 4h(E₈) (group order = 4 × Coxeter number: 120 = 4 × 30)
- ⟨d²⟩/⟨d⟩ = 4 (ratio of moments = 4)
- The marks are "balanced around 4": contributions from d < 4 (total -17) cancel d > 4 (total +17)

## The Derived Chain

| Step | Identity | Proof |
|------|----------|-------|
| (1) | marks = I* irrep dims | McKay correspondence |
| (2) | h = Σdᵢ = 30, \|I*\| = Σdᵢ² = 120 | Standard rep theory |
| (3) | Σdᵢ(dᵢ-4) = 0 | Direct check on Ẽ₈ |
| (4) | \|I*\| = 4h | Equivalent to (3) |
| (5) | E(icosahedron) = \|I*\|/4 = h = 30 | Orbit-stabilizer + (4) |
| (6) | V×F = 4\|A₅\| = 8h = rank×h = roots(E₈) = 240 | gcd(5,3)=1 + (5) |
| (7) | V⊗F = 4×reg(A₅) = 2×(Coxeter integer sector) | Character theory |

## The V⊗F Theorem

**Theorem**: V_vertex ⊗ V_face = 4 × reg(A₅) for the icosahedron.

**Proof**: The A₅-character of V⊗F vanishes at all g ≠ e because gcd(|Stab_V|, |Stab_F|) = gcd(5,3) = 1 implies no non-identity element fixes both a vertex and a face. A character proportional to δ(g,e) is a multiple of the regular representation, with multiplicity 240/60 = 4. QED.

**Generalization**: V⊗F = k × reg(G) whenever gcd(|Stab_V|, |Stab_F|) = 1:
- Octahedron: V⊗F = 2 × reg(S₄) (48 = 2 × 24)
- Cube: V⊗F = 2 × reg(S₄) (48 = 2 × 24)
- Icosahedron: V⊗F = 4 × reg(A₅) (240 = 4 × 60)
- Tetrahedron: gcd(3,3) = 3 ≠ 1, so V⊗F is NOT a multiple of reg

## Why V×F = roots(E₈) is Unique

V×F = h × rank (= root count) iff |I*| = 4h iff Σdᵢ(dᵢ-4) = 0.

This holds ONLY for E₈:
- E₆: |T*| = 24 ≠ 4×12 = 48
- E₇: |O*| = 48 ≠ 4×18 = 72
- E₈: |I*| = 120 = 4×30 = 4h ✓

## Connection to the Framework

The 240 = 12 × 20 decomposition of the E₈ root count is representation-theoretic, not numerical. It follows from the mark-balance identity Σdᵢ(dᵢ-4) = 0 through the chain above.

In the vortex framework: the icosahedron's vertices (12 vortex positions) tensor with its faces (20 dual cells) to produce the full E₈ root system structure. The vertex-face duality of the Platonic solid encodes the root-Cartan decomposition of the Lie algebra.

## Open Questions

1. Is there a conceptual explanation for WHY the E₈ marks balance around 4?
2. Does the identity generalize to other quantities (e.g., higher moments)?
3. What is the geometric meaning of the "pivot value" 4 (the dim of ρ₃ and ρ₆)?
4. Does the octahedron identity V⊗F = 2×reg(S₄) have consequences for E₇?
