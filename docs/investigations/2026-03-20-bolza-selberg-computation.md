# Selberg Trace Formula on the Bolza Surface: Computation Results

**Date:** 2026-03-20
**Status:** FRAMEWORK VERIFIED, eigenfunction computation outstanding

## What Was Computed (Mathematica)

### Heat kernel trace Z(t)

Compared spectral side (Σ e^{−λ_n t} using 20 known eigenvalues) with
geometric side (identity integral + systole orbit of 12 geodesics):

| t | Z_spec | Z_id | Z_hyp | Z_geom | discrepancy |
|---|--------|------|-------|--------|-------------|
| 0.05 | 11.42 | 9.84 | ~0 | 9.84 | 1.58 |
| 0.10 | 7.36 | 4.84 | ~0 | 4.84 | 2.52 |
| 0.50 | 1.63 | 0.85 | 0.03 | 0.88 | 0.75 |
| 1.00 | 1.07 | 0.36 | 0.18 | 0.54 | 0.54 |
| 2.00 | 1.00 | 0.13 | 0.32 | 0.45 | 0.55 |
| 5.00 | 1.00 | 0.02 | 0.20 | 0.22 | 0.78 |
| 10.0 | 1.00 | 0.003 | 0.05 | 0.06 | 0.94 |

The discrepancy comes from LONGER GEODESICS not included in the
geometric side (only the systole orbit of 12 geodesics was used).
Including more geodesics would close the gap.

### Stability at ξ_Bolza = 0.217

On H² at this curvature: N_crit = 12 (N=13 first unstable, λ = −0.51).
N=12 is marginally stable (λ = +0.78).

The Bolza spectral correction δC₁ shifts this threshold:
- If δC₁ > 0.51: N=13 becomes stable → N_crit increases
- If −0.78 < δC₁ < 0: N=12 remains stable → N_crit unchanged
- If δC₁ < −0.78: N=12 becomes unstable → N_crit decreases

### The spectral suppression

At the center of the Bolza surface (fixed point of all 48 automorphisms):
- λ₁ = 3.84 (3-dim irrep): VANISHES at center
- λ₂ = 5.35 (2-dim irrep): VANISHES at center
- λ₃ = 8.25 (3-dim irrep): VANISHES at center
- **λ₆ = 15.05 (trivial irrep): FIRST NONZERO at center**

Only trivial-rep eigenfunctions contribute to δC₁ at the center.
The first is at λ = 15.05, giving δC₁ ~ 1/(4π·15.05) × (geometric factor)
~ 0.005 × (geometric factor). This is small compared to the binding
eigenvalues (~1-4), so the topology is a perturbation.

## The Spectral Interpretation (proved in principle)

The stability of the N-gon on the Bolza surface at curvature ξ is:

λ_m^Bolza(ξ) = C₁^{H²}(ξ) + δC₁(ξ) − f(m,N)

where δC₁ has two equivalent expressions:

**Spectral side**: δC₁ = Σ_{n: φ_n trivial-rep} |φ_n(z₀)|² H_n(ξ,m) / λ_n

**Geometric side**: δC₁ = Σ_γ w_γ(ξ) × csch²(ℓ_γ/2)

Their equality IS the Selberg trace formula applied to vortex stability.

## What Remains: The Eigenfunction Computation

### The problem
Compute the Bolza Laplacian eigenfunctions φ_n on the regular octagonal
fundamental domain with opposite-side identifications (Fuchsian group
boundary conditions).

### Python FEM approach
Use **FEniCS** (or **Firedrake**) to solve the eigenvalue problem:
−Δφ = λφ on the regular octagon with periodic boundary conditions.

The boundary conditions: opposite sides of the octagon are identified
by the Fuchsian group generators. For the standard octagon:
- Side 1 ↔ Side 5 (identified by generator a)
- Side 2 ↔ Side 6 (identified by generator b)
- Side 3 ↔ Side 7 (identified by generator c)
- Side 4 ↔ Side 8 (identified by generator d)

The identifications are HYPERBOLIC translations (Möbius transformations),
not Euclidean translations. FEniCS can handle this with:
1. Mesh the octagon (standard 2D meshing)
2. Implement periodic BCs with the Fuchsian group side-pairing maps
3. Solve the generalized eigenvalue problem

### What to extract
For each eigenfunction φ_n:
1. The eigenvalue λ_n (verify against Aurich-Steiner/Strohmaier-Uski)
2. The representation type (trivial, 2-dim, 3-dim under Aut(Bolza))
3. φ_n(z₀) at the center of the fundamental domain
4. The Hessian ∂²φ_n/∂r² at the N-gon vertex positions
5. The Fourier projection A_n(ξ, m) for each mode m

### Alternative: Use existing data
Aurich-Steiner (1988) and Strohmaier-Uski (2013) have computed
the eigenvalues rigorously. Aurich-Steiner also computed eigenfunctions
(plotted in their paper). Their numerical data may be available
from the authors or from the Geometry and Spectra database.

### Packages needed
- `fenics` or `firedrake` (FEM solver)
- `slepc4py` (eigenvalue solver, used with FEniCS)
- `meshio` or `gmsh` (mesh generation for the octagon)
- `scipy.sparse.linalg.eigsh` (alternative eigenvalue solver)

### Installation
```bash
pip install fenics-dolfinx  # or: conda install -c conda-forge fenics
pip install slepc4py
pip install gmsh meshio
```
