# E₈ Casimir = Platonic Havelock Casimir (GAP D)

## Goal

Prove and numerically verify the bridge identity: the E₈ quadratic Casimirs restricted to I* (binary icosahedral group) equal the Platonic Havelock Casimirs T_ρ computed from icosahedral vortex interactions on S².

This closes GAP D from the session 10 pickup document and is the central bridge between the polygon framework (A-type, Z_N, K ≤ 0) and the Platonic framework (E-type, I*, K > 0).

## Mathematical Framework

### Two levels of the bridge

**Level 1 — Integer spin (A₅ irreps: dims 1, 3, 3', 4, 5)**

The existing `platonic_havelock.py` computes T_ρ = Σ K(d)[1 - P_j(cos d)] for A₅ irreps where D^j|_{A₅} is irreducible. The symmetric space theorem on S² = SU(2)/U(1) identifies Casimir = Laplacian, giving T_j = j(j+1) × C₁_norm where C₁_norm is a universal geometric factor of the icosahedron.

**Level 2 — Half-integer spin (I*-only irreps: dims 2, 2, 4, 6)**

These don't appear in the tangent space of the icosahedron (which has A₅ = I*/Z₂ symmetry). The Frobenius character formula extends the Platonic Havelock Casimir to the full I* representation ring: T_ρ = (|H|/dim ρ) Σ K(d) [1 - χ_ρ(g_k)/dim ρ], using I* characters on the 12 icosahedron vertices.

### The E₈ connection

I* ⊂ SU(2) embeds in E₈ via the principal embedding (unique for E₈). The E₈ adjoint (248-dim) decomposes under the principal SU(2) into representations with spins equal to the E₈ exponents:

    248 = V₃ ⊕ V₁₅ ⊕ V₂₃ ⊕ V₂₇ ⊕ V₃₅ ⊕ V₃₉ ⊕ V₄₇ ⊕ V₅₉
    spins j = 1, 7, 11, 13, 17, 19, 23, 29

Restricting further to I* gives 248|_{I*} = ⊕ n_ρ · ρ. The bridge theorem identifies these multiplicities and Casimirs with the Platonic Havelock data.

### I* conjugacy classes

| Class | Size | θ (SU(2) angle) | Order | Description |
|-------|------|------------------|-------|-------------|
| C₁ | 1 | 0 | 1 | identity |
| C₂ | 1 | π | 2 | -I (center) |
| C₃ | 12 | 2π/5 | 5 | order-5 type A |
| C₄ | 12 | 4π/5 | 5 | order-5 type B |
| C₅ | 12 | π/5 | 10 | order-10 type A |
| C₆ | 12 | 3π/5 | 10 | order-10 type B |
| C₇ | 20 | 2π/3 | 3 | order-3 |
| C₈ | 20 | π/3 | 6 | order-6 |
| C₉ | 30 | π/2 | 4 | order-4 |

Sum = 120. I* irrep dims in McKay (affine E₈ Dynkin) order: {1, 2, 3, 4, 5, 6, 4, 2, 3}. Sum of squares = 120.

### Prior data (from session 10, to verify)

E₈ adjoint character on I* classes: {248, -8, 2, 2, -4, 0, -2, -2, 4}

Partial decomposition (integer-spin only): mult(ρ₁) = 2, mult(ρ₃) = 8, mult(ρ₅) = 12

## Code Architecture

### File: `src/planetary_polygons/proofs/e8_casimir_bridge.py`

Six components building bottom-up:

1. **`i_star_character_table()`** — Full 9×9 character table of I* (order 120). Character values from SU(2) restriction: χ_j(θ) = sin((2j+1)θ)/sin(θ). Returns table, class_sizes, irrep_dims, irrep_names, class_angles. Verifies row and column orthogonality.

2. **`e8_adjoint_character_on_i_star()`** — Computes χ₂₄₈(g) for each I* class using principal SU(2) branching (spins = E₈ exponents {1,7,11,13,17,19,23,29}). Returns 9-element array.

3. **`decompose_e8_adjoint()`** — Character inner product: mult(ρᵢ) = (1/120) Σ_C |C| χ₂₄₈(C) χ̄_ρᵢ(C). Verifies Σ nᵢ dᵢ = 248 and all multiplicities are non-negative integers.

4. **`platonic_havelock_casimirs_i_star()`** — T_ρ for all 9 I* irreps. Integer-spin: delegates to `generalized_casimir()` from platonic_havelock.py. Half-integer-spin: Frobenius character formula using I* characters evaluated at the 12 icosahedron vertex group elements.

5. **`su2_casimirs_on_i_star()`** — For each I* irrep, the SU(2) Casimir j(j+1) from the embedding spin. First 6 irreps (dims 1–6): j = 0, 1/2, 1, 3/2, 2, 5/2 (direct restriction). Remaining 3 (split pieces): determined by first SU(2) spin in which they appear.

6. **`verify_bridge_identity()`** — Main theorem assembly. Compares T_ρ, j(j+1), and E₈ multiplicities for all 9 irreps. Determines the normalization C₁_norm and verifies T_ρ = j(j+1) × C₁_norm universally.

### File: `tests/test_e8_casimir_bridge.py`

Test categories:
- I* character table: orthogonality (rows and columns), Σ dᵢ² = 120
- E₈ adjoint: character values match session 10 data, Σ nᵢ dᵢ = 248, all multiplicities ≥ 0
- Platonic Havelock: T₀ = 0 (trivial irrep), T_ρ > 0 for non-trivial
- Bridge identity: T_ρ / j(j+1) = constant for all non-trivial irreps
- Cross-check: integer-spin T_ρ matches existing platonic_havelock.py values

### Dependencies

numpy only (no scipy). Imports from existing modules:
- `planetary_polygons.proofs.platonic_havelock` (generalized_casimir, interaction_matrix)
- `planetary_polygons.explorations.platonic_vortices` (icosahedron_vertices)

## Scope

This module proves the bridge for the **icosahedron (E₈)** only. The analogous bridges for tetrahedron (E₆ via T*) and octahedron (E₇ via O*) are structurally identical and can be added as corollaries in a follow-up.

## Approach

Bottom-up numerical discovery (Approach A): build infrastructure, compute everything numerically, find the exact relationship, then prove analytically using the symmetric space theorem.
