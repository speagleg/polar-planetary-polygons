# GAP A: Vortex Dynamics on S³ — Design Spec

## Goal

Derive the S³ Green's function from first principles, construct the vortex Hamiltonian, compute the energy and stability of the 600-cell (120 I* quaternion vertices), and build the S³ Havelock decomposition using Gegenbauer polynomials.

## Mathematical Framework

### S³ Laplacian and Green's function (first principles)

On the unit S³, the scalar Laplacian eigenvalues are -Δf = l(l+2)f for l=0,1,2,..., with degeneracy (l+1)². The zonal eigenfunctions (depending only on geodesic distance χ) are Gegenbauer polynomials C_l^1(cos χ), normalized so C_l^1(1) = l+1.

The Green's function G(χ) satisfying ΔG = -δ + 1/Vol(S³) is constructed from the eigenfunction expansion:

    G(χ) = -(1/4π²) Σ_{l≥1} [(2l+2)/(l(l+2))] C_l^1(cos χ) / (l+1)

which sums to the closed form:

    G(χ) = -(1/4π²)(π - χ)/sin(χ)

This must be verified numerically.

### Vortex Hamiltonian on S³

    H = -Σ_{j<k} κ_j κ_k G(χ_{jk})

where χ_{jk} = arccos(q_j · q_k) is the geodesic distance on S³ between unit quaternions q_j, q_k (4D dot product). Equal circulations κ=1 throughout.

### 600-cell vertices = I* quaternions

The 120 elements of I* as unit quaternions (already constructed in GAP D) are the 120 vertices of the 600-cell on S³. This is a regular polytope with I* symmetry under left quaternion multiplication.

### S³ Havelock decomposition

Analog of the S² Platonic Havelock formula, using Gegenbauer C_l^1 instead of Legendre P_j:

    T_l = Σ_{k≠0} w(χ_{0k}) [1 - C_l^1(cos χ_{0k})/(l+1)]

where w(χ) is the interaction weight derived from G(χ). The normalization C_l^1(1) = l+1 ensures the zonal spherical function equals 1 at χ=0.

## Code Architecture

### File: `src/planetary_polygons/proofs/s3_vortex_dynamics.py`

1. `s3_green_function(chi)` — Closed form G(χ) = -(1/4π²)(π-χ)/sin(χ)
2. `s3_laplacian_eigenvalue(l)` — Returns l(l+2)
3. `gegenbauer_C1(l, x)` — Gegenbauer polynomial C_l^1(x) via recurrence
4. `s3_green_eigenfunction_expansion(chi, l_max)` — Partial sum for verification
5. `s3_geodesic_distance(q1, q2)` — arccos(q1·q2) for unit quaternions
6. `build_600cell_vertices()` — 120 I* quaternions (reuse GAP D construction)
7. `s3_vortex_energy(quats)` — Hamiltonian H = -Σ G(χ_{jk})
8. `s3_interaction_matrix(quats)` — N×N zero-sum matrix
9. `s3_havelock_casimir(quats, l)` — T_l via Gegenbauer zonal spherical function
10. `verify_s3_green_function(l_max)` — Eigenfunction expansion vs closed form

### File: `tests/test_s3_vortex_dynamics.py`

- Green's function correctness (special values, symmetry, singularity)
- Eigenfunction expansion convergence
- Geodesic distance properties
- 600-cell I* symmetry
- Interaction matrix zero-sum
- Havelock T₀ = 0

### Dependencies

numpy only. Reuses I* quaternion construction pattern from GAP D.

## Scope

This module establishes S³ vortex dynamics. GAPs B (Onsager on S³) and C (N=12→N=7 transition) build on top of it.
