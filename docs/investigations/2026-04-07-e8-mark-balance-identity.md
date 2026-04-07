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

## Further Discoveries (continued exploration)

### The E₈ Balance Pivot Sequence

The E₈ marks (1,2,3,4,5,6,4,2,3) generate a sequence of balance pivots k_n = Σd^{n+1}/Σd:

| n | k_n | Value | Interpretation |
|---|-----|-------|----------------|
| 0 | Σd/Σ1 = 30/9 | 10/3 | average dim |
| 1 | Σd²/Σd | **4 = rank(E₈)/2** | THE mark-balance identity |
| 2 | Σd³/Σd | **18 = h(E₇)** | cross-references E₇! |
| 3 | Σd⁴/Σd | 438/5 | (not clean) |
| 4 | Σd⁵/Σd | **450 = h(E₈)²/2** | squares the Coxeter number |

### Cross-Type Pivot Table

The k₂ = Σd³/Σd pivot cross-references between types:

| Marks of | k₂ = Σd³/Σd | Interpretation |
|----------|-------------|----------------|
| E₆ | 9/2 | — |
| E₇ | **8 = rank(E₈)** | E₇ marks know about E₈ rank |
| E₈ | **18 = h(E₇)** | E₈ marks know about E₇ Coxeter number |

The exceptional Lie algebras cross-reference each other through the moments of their McKay marks.

### The V⊗F Theorem Generalization

V⊗F = k × reg(G) whenever gcd(|Stab_V|, |Stab_F|) = 1:

| Solid | V⊗F | k | Matches roots? |
|-------|-----|---|----------------|
| Tetrahedron | NOT k×reg | — | — (gcd=3) |
| Octahedron | 2×reg(S₄) | 2 | No (48 ≠ 126) |
| Icosahedron | 4×reg(A₅) | 4 | **YES (240 = 240)** |

### Second Balance Identity

Σ dᵢ(dᵢ² - 18) = 0 for the E₈ marks. The pivot 18 = h(E₇).

### Open: Why Do the E-Types Cross-Reference?

The moments of the I* marks encode data about E₇ and E₈:
- k₁ = 4 = rank(E₈)/2
- k₂ = 18 = h(E₇)
- k₄ = 450 = h(E₈)²/2

This suggests the mark distribution encodes the ENTIRE exceptional hierarchy, not just E₈. The mechanism connecting the moment structure to the Lie algebraic data is unknown.

## The Dynkin Inclusion Mechanism (deepest layer)

### How E₈ "knows about" E₇

Removing node 1 (mark 2) from the affine Ẽ₈ diagram gives **A₁ + E₇**. This is the Dynkin inclusion E₇ ⊂ E₈, corresponding to the branching E₈ ⊃ E₇ × SU(2): 248 = (133,1) + (1,3) + (56,2).

The mechanism: the McKay correspondence converts this DIAGRAM operation into a MOMENT relationship. The k₂ pivot of the E₈ marks (= 18 = h(E₇)) is the Dynkin inclusion E₇ ⊂ E₈ expressed in the moment language.

### The Asymmetry: Terminal vs Non-Terminal

- k₂(Ẽ₇) = 8 = rank(E₈) — looks UP to E₈
- k₂(Ẽ₈) = 18 = h(E₇) — looks DOWN to E₇ (E₈ is terminal, no E₉)

E₈ is the largest exceptional algebra. Its k₂ moment cannot reference a higher algebra, so it references the Coxeter number of the next-lower algebra. The moment sequence encodes the hierarchy in both directions.

### Node Removal and Subalgebras

Removing different nodes from Ẽ₈ gives different maximal subalgebras:

| Removed node | Mark | Remaining diagram | Subalgebra |
|---|---|---|---|
| 0 (affine) | 1 | E₈ | (the finite algebra itself) |
| 1 | 2 | A₁ + E₇ | E₈ ⊃ SU(2) × E₇ |
| 7 (far end) | 2 | D₈ | E₈ ⊃ SO(16): 248 = 120 + 128 |
| 8 (branch) | 3 | A₈ | E₈ ⊃ SU(9): 248 = 80 + 84 + 84̄ |

The 120/128 split (from GAP D) corresponds to removing node 7 (the D₈/SO(16) branching).

### The Holographic Encoding

The McKay marks of E₈ form a 9-element distribution whose moments encode:
- Order 1: h(E₈) = 30 (first moment = Coxeter number)
- Order 2: |I*| = 120, with k₁ = 4 = rank(E₈)/2 (the mark-balance identity)
- Order 3: k₂ = 18 = h(E₇) (Dynkin inclusion downward)
- Order 5: k₄ = 450 = h(E₈)²/2 (self-reference squared)

The I* dimension distribution is a generating function for the exceptional hierarchy.

### E₈/E₆ Exponential Relation

For the T* ⊂ I* subgroup inclusion (A₄ ⊂ A₅):

Σd^n(E₈) / Σd^n(E₆) = (h₈/h₆) × 2^{n-1} = (5/2) × 2^{n-1}

Exact for n = 1, 2, 3. Breaks at n = 4 (ratio 219/11 ≈ 19.91 vs predicted 20).
