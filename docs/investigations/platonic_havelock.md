# ADE Complementarity: Platonic Vortices and Curvature Phase Transitions

## Overview

The Havelock eigenvalue decomposition extends from regular N-gons (Z_N symmetry, A-type McKay) to Platonic solid configurations on S² (non-abelian symmetry, E-type McKay). The curvature sign determines which classification applies, giving a first-order phase transition at K=0 that simultaneously changes the ground state geometry and the gauge group.

The full picture:

    K > 0 (de Sitter):     Icosahedron on S²  →  E_8   (Onsager selection)
    K = 0 (Minkowski):      Heptagon on R²     →  SM    (Onsager selection)
    K < 0 (anti-de Sitter): Heptagon on H²     →  SM    (Onsager + Lax conservation)

---

## Proved Results

### 1. Generalized Havelock Formula (Theorem)

For a Platonic solid with N vertices on S², symmetry group G, and csc² interaction kernel K(d) = 1/(4 sin²(d/2)), the eigenvalue of the zero-sum interaction matrix in the G-irrep rho (restriction of D^j) is:

    T_rho = Sigma_{k!=0} K(d_{0k}) [1 - P_j(cos d_{0k})]

**Proof**: Schur's lemma (G-invariance of K) + zonal spherical function on S² is the Legendre polynomial P_j. The Legendre polynomial IS the eigenvector of the interaction matrix — verified to residuals ~10^{-16}.

**Verified**: Tetrahedron (j<=1), Octahedron (j<=2), Icosahedron (j<=3), Cube (j<=2).

**Limitation**: Requires D^j|_G to be irreducible. When D^j splits (cube j>=3, dodecahedron j>=3), the formula gives the dimension-weighted average, not individual eigenvalues.

**Code**: `proofs/platonic_havelock.py` (31 tests)

### 2. Stability Pattern on S²

| Solid | N | Group | |G| | Binary | McKay | Stable? | Index |
|-------|---|-------|-----|--------|-------|---------|-------|
| Tetrahedron | 4 | A_4 | 12 | T* | E_6 | YES | 0 |
| Octahedron | 6 | S_4 | 24 | O* | E_7 | YES | 0 |
| Cube | 8 | S_4 | 24 | O* | E_7 | NO | 2 |
| Icosahedron | 12 | A_5 | 60 | I* | E_8 | YES | 0 |
| Dodecahedron | 20 | A_5 | 60 | I* | E_8 | NO | 8 |

Every eigenvalue degeneracy matches an irrep dimension of G (verified for all 5 solids). The cube is the Platonic analogue of N=8 for polygons.

### 3. Universal Casimir

T = (N-1)/2 appears as a Casimir for every Platonic solid, matching the polygon fundamental mode f(1,N) = (N-1)/2.

### 4. GL(2,F_3) = O* (Bolza automorphism group)

The Bolza surface (genus 2) has Aut = GL(2,F_3), which is isomorphic to the binary octahedral group O*. Verified by conjugacy class structure: both have 8 classes of sizes [1, 1, 6, 6, 6, 8, 8, 12].

The McKay graph of O* is the extended E_7 Dynkin diagram.

### 5. First-Order Phase Transition at K=0

The energy ordering on S²(R) is R-independent: the R-dependent term -N(N-1)/2 × ln(R) is universal across all N-vertex configurations. Therefore:
- Platonic solids are the ground state for ALL K > 0 (any sphere)
- Polygon rings are the ground state at K = 0 (flat plane)

The transition is discontinuous:
- Octahedron (N=6): antipodal vertices project to infinity at K=0 (topological obstruction)
- Icosahedron (N=12): no antipodal vertices, but 12-gon wins by energy gap +58.7 on R²

### 6. Icosahedron is the Onsager Ground State on S²

Among stable Platonic solids (tetrahedron, octahedron, icosahedron), the Onsager principle (maximize N subject to stability) selects the icosahedron (N=12, A_5 -> E_8) — the largest stable Platonic solid. This parallels the heptagon (N=7) as the largest stable polygon.

### 7. E_8 -> SM is Single-Step at K=0

The intermediate Platonic solids (E_7, E_6) do not appear as separate phases. On S² at any K > 0, all stable Platonic solids coexist, and the Onsager principle selects the icosahedron. The breaking E_8 -> SM happens in a single step at K = 0.

E_8 contains SM via: E_8 -> E_6 x SU(3) -> SO(10) x U(1) x SU(3) -> SU(5) x U(1)^2 x SU(3) -> SM x [massive].

---

## Suggestive but Unconfirmed

### Bolza tau and E_7

At word length L=3 (336 = 7 x 48 elements), the Bolza tau(P_-) = 217/336 = 31/48, and 31 = 48 - 17 = |O*| - max(E_7 exponent). This is suggestive but NOT confirmed as the converged value — tau drifts to 0.642 (L=4) and 0.636 (L=5). Higher word lengths needed.

Prediction for Bring surface (g=4, |Aut|=120, McKay E_8, h=30): tau = 91/120 = 0.7583. Testable once the Bring surface Fuchsian group is implemented.

---

## Open Questions (Investigation Programme)

### Mathematical (provable with existing machinery)

1. **Full character formula**: Compute T_rho for all G-irreps when D^j splits, using the Frobenius character formula. Needed for cube (j>=3) and dodecahedron (j>=3).

2. **Converged Bolza tau**: Push Fuchsian group enumeration to L>=8 to determine whether tau = 31/48 or some other rational value. Need ~10^5 group elements.

3. **Bring surface tau**: Implement the Bring surface (g=4, |Aut|=S_5) Fuchsian group and compute tau to test the E_8 prediction 91/120.

4. **Platonic Havelock on compact quotients**: Compute the generalized Havelock eigenvalues for vortex configurations on the Bolza surface using the O* irrep decomposition.

### Structural (requires new ideas)

5. **E_8 -> SM breaking mechanism**: How does the geometric transition (icosahedron -> heptagon at K=0) realize the standard GUT breaking chain? Is there a geometric interpolation?

6. **The 3+1D formulation**: The Platonic framework on S² naturally lives in 3D (S² subset R³). Does this give a direct 3+1D theory without the KK compactification needed in the polygon framework?

7. **Dihedral intermediates**: The dihedral groups D_n (binary dihedral D*_n -> D_{n+2} -> SO(2n+4)) lie between cyclic and Platonic in the ADE classification. Do dihedral vortex configurations on S² interpolate between the polygon and Platonic ground states?

8. **Curvature quantization**: If the gauge group is determined by the curvature sign (E-type for K>0, A-type for K<=0), is there a selection principle that determines the MAGNITUDE of K? This would connect to the cosmological constant problem.

9. **248 = ?**: Does dim(E_8) = 248 have a Havelock interpretation in terms of the icosahedron? The icosahedron has N(N-1)/2 = 66 pairs; not 248. The Havelock modes (2N-3 = 21 physical DOF) don't match either. What does 248 count in the vortex picture?

10. **Three generations**: dim(E_8)/(N_icosa x N_heptagon) = 248/84 = 2.95 ≈ 3. Is this a coincidence or does it explain three fermion generations?

---

## Code Index

| File | Content | Tests |
|------|---------|-------|
| `explorations/platonic_vortices.py` | Vertex coordinates, S² energy, Hessian | — |
| `explorations/platonic_irreps.py` | Character tables, irrep decomposition, Casimir analysis | — |
| `explorations/ade_phase_transition.py` | Energy comparison, phase transition scanning | — |
| `proofs/platonic_havelock.py` | Generalized Havelock formula proof | 31 |
| `tests/test_platonic_havelock.py` | Full verification suite | 31 |

---

## Relationship to Main Papers

When ready for integration:
- **Paper I** (Math): Generalized Havelock theorem as new section after S²/H² stability
- **Paper IV** (Field Theory): E_8 UV completion remark in §10
- **Paper V** (Cosmology): ADE phase transition at reheating in §9/§11
- **New Paper?**: If the investigation programme yields enough results, this could be a standalone paper on "ADE vortex classification and curvature phase transitions"
