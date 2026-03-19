# Open Problems

Problems identified during this research that are not resolved in the paper.
Organized by difficulty and proximity to current results.

---

## Tractable (provable with existing tools, need time)

### OP1: Morse-Bott structure for all N
**Statement:** The Thomson energy H is a Morse-Bott function on the
constrained configuration space C_N^c for all N ≥ 3, with the N-gon
as the unique Z_N-symmetric critical orbit (up to rotation).
**Status:** Verified numerically for N ≤ 15. The Hessian and Goldstone
mode are computed. A proof would require showing non-degeneracy of
the Hessian on the Z_N-fixed locus for all N.
**Route:** Direct analysis of the Havelock eigenvalues — already
available but needs formal write-up as a general-N theorem.

### OP2: Complete critical point census on C_N^c
**Statement:** Enumerate all Z_N-symmetric critical points of H on
C_N^c = {L=const, P=0} \ Δ for each N.
**Status:** For N ≤ 7: the N-gon is the unique minimum (proven).
For N ≥ 8: other critical points (saddles) exist. Their Morse indices
are unknown.
**Route:** Numerical continuation (homotopy methods) starting from
the N-gon and tracking critical points as N varies.

### OP3: Equivariant Euler class sign change at N=7→8
**Statement:** The equivariant Euler class e^{Z_N}(ν) of the normal
bundle to the N-gon in C_N^c changes sign from +1 (N ≤ 7) to -1
(N = 8). This is a topological invariant.
**Status:** Computable for each N from the Havelock eigenvalue signs.
The sign change IS the stability transition. Need to show this is
the ONLY sign change (i.e., no further sign changes at larger N
that would create "re-entrant" stability).
**Route:** The formula μ(N) = N-5 (proven) shows μ is monotonically
increasing, so no sign-change reversal occurs.

---

## Hard (require new mathematical ideas)

### OP4: Geometric construction of the Dirac operator D_N
**Statement:** Construct D_N = d/dξ + H_N(ξ) from geometric data
(the surface, the Z_N action, the Green's function) WITHOUT reference
to the explicit eigenvalue family H_N(ξ).
**Why it matters:** If D_N has a geometric interpretation, then
ind(D_N) = μ(N) = N-5 becomes a geometric/topological theorem
rather than an algebraic computation.
**Status:** The APS identity ind(D_N) = SF = μ(N) is PROVEN, but
D_N is currently defined by the family, making it tautological.
**Route:** Identify H_N as a restriction of the Laplacian to the
Z_N-symmetric sector of the configuration space, and construct
D_N as the associated Dirac operator on this sector.

### OP5: ind(D_N) = N-5 via characteristic classes
**Statement:** Compute ind(D_N) using the Atiyah-Singer index formula
(Chern numbers, A-hat genus) on the configuration space C_N^c, and
show it equals N-5.
**Why it matters:** This would give a TOPOLOGICAL PROOF of N_crit = 7.
**Status:** Open. The naive equivariant index on R² gives ind = 1
for all N (the quotient R²/Z_N is a cone). The right space is the
configuration space C_N, whose topology (pure braid group π₁ = P_N,
Arnold-Cohen homology) depends on N.
**Route:** Equivariant index theory on configuration spaces.
Literature: F. Cohen (1976) on H*(C_N), V. Arnold (1970) on the
cohomology of braid groups.

### OP6: Is H a perfect Morse function on C_N^c?
**Statement:** Does the Morse polynomial of H on C_N^c equal the
Poincaré polynomial? (Equivalently: are all Morse inequalities
equalities?)
**Why it matters:** If yes, the Morse index μ(N) is determined
entirely by the topology of C_N^c, with no reference to the
specific energy function H.
**Status:** Unknown. Requires knowledge of both the complete critical
point set (OP2) and the homology of C_N^c.

### OP7: Equivariant signature as a topological invariant
**Statement:** Express the Z_N-equivariant signature
σ^{Z_N}(H) = Σ_m ω^m · sgn(λ_m) (where ω = e^{2πi/N})
in terms of topological invariants of the configuration space.
**Why it matters:** This encodes WHICH modes are unstable, not
just how many. It's a finer invariant than the Morse index.
**Status:** Computable for each N. Topological interpretation unknown.

---

## Frontier (require substantial new theory)

### OP8: Vortex stability on compact hyperbolic surfaces
**Statement:** Compute the stability thresholds for point vortices
on the Bolza surface (genus 2, {8,3} tiling) and other compact
hyperbolic surfaces.
**Why it matters:** Would combine the H² algebraic structure
(Pell equations, palindromic polynomials) with genus-dependent
corrections. Potential connection to Selberg zeta function.
**Status:** The flat torus was explored and found NOT to support
the ring stability problem (vortex row, not ring). Compact
hyperbolic surfaces are the natural next candidate.
**Route:** Compute the Green's function on the Bolza surface
(known in terms of automorphic forms), build the Hessian,
find the stability thresholds.

### OP9: Non-abelian symmetry groups
**Statement:** Generalize the Havelock analysis to vortex
configurations with non-abelian symmetry (dihedral D_N,
tetrahedral A_4, octahedral S_4, icosahedral A_5).
**Why it matters:** The Hessian would decompose into MULTI-
DIMENSIONAL irreps, giving a richer eigenvalue structure.
**Status:** The framework (Remark rep-theory) identifies the
structure but no computations have been done.
**Route:** Build the Hessian for Platonic-solid vortex configurations
on S², decompose into irreps, find stability conditions.

### OP10: Modular forms on compact hyperbolic surfaces
**Statement:** Do the stability thresholds on compact hyperbolic
surfaces involve modular forms (through the moduli space of
the surface)?
**Status:** The flat torus approach (j-invariant conjecture) was
shown to be inapplicable (the torus doesn't support ring stability).
The compact hyperbolic case is unexplored.
**Route:** Requires OP8 first, then analysis of how thresholds
depend on the moduli of the surface.
