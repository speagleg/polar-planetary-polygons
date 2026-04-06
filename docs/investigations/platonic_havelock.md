# Platonic Havelock Exploration — Session 2026-04-06

## Summary

The Havelock eigenvalue decomposition generalizes from regular N-gons (Z_N symmetry) to Platonic solid vortex configurations on S² (A_4, S_4, A_5 symmetry). This exploration discovered three new results.

## Result 1: Generalized Havelock Formula

For a Platonic solid with N vertices on S² and symmetry group G, the Hessian of the vortex energy decomposes into G-irreps:

    Hess = ⊕_ρ  λ_ρ · Id

with λ_ρ = C₁ - T_ρ, where T_ρ is the eigenvalue of the csc² kernel in the ρ-isotypic sector.

When the SO(3) representation D^j restricts to a single G-irrep ρ:

    T_ρ = Σ_{k≠0} [1/(4 sin²(d_{0k}/2))] × [1 - P_j(cos d_{0k})]

Verified exactly for tetrahedron, octahedron, icosahedron.

## Result 2: Stability Pattern

| Solid | N | Group | Stable on S²? | Unstable irrep |
|-------|---|-------|---------------|----------------|
| Tetrahedron | 4 | A_4 | YES | — |
| Octahedron | 6 | S_4 | YES | — |
| Cube | 8 | S_4 | NO (index 2) | dim-2 of S_4 |
| Icosahedron | 12 | A_5 | YES | — |
| Dodecahedron | 20 | A_5 | NO (index 8) | multiple |

The cube is the Platonic analogue of N=8 for polygons.

## Result 3: ADE-Surface Duality Conjecture

Platonic groups cannot embed in Isom(H²) = PSL(2,R). But compact quotients Γ\H² have automorphism groups matching binary Platonic orders:

| Surface | g | |Aut| | Binary group | McKay |
|---------|---|-------|-------------|-------|
| Bolza | 2 | 48 | O* (octahedral) | E_7 |
| Bring | 4 | 120 | I* (icosahedral) | E_8 |

**Conjecture**: The Havelock spectrum on Γ\H² is controlled by the ADE Dynkin diagram corresponding to Aut(Γ\H²) via the McKay correspondence.

This would unify:
- Problem 9 (Bolza stability) ↔ E_7 representation theory
- Problem 10 (Platonic solids) ↔ ADE classification

## Key finding: Universal Casimir

T = (N-1)/2 appears as a Casimir eigenvalue for every Platonic solid, matching the polygon mode m=1 Casimir f(1,N) = (N-1)/2.

## Open questions

1. Closed-form T(ρ) for all G-irreps (not just when D^j is irreducible)
2. Is the ADE-surface conjecture true? Test on the Bring surface.
3. Does the Bolza τ(P₋) = 0.644 relate to E_7 representation data?
