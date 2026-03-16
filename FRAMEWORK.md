# The Mechanistic Framework: Why Rotating Fluids Make Polygons

## The Answer (three tiers)

### Tier 1: Universal (any Hamiltonian on a symmetric domain)

**Result 1 (Spectral reality).** For any second-order self-adjoint operator with real coefficients ψ'' + V(ρ)ψ = 0, the WKB exponent satisfies s² ∈ ℝ. When V < 0 (oscillatory regime), s = ±iα_ρ, forcing σ = Re(s) = 0. This is not specific to the QGPV — it holds for any real eigenvalue problem.

**Result 2 (Equivariant critical point).** For any Hamiltonian H(z₁,...,z_N) with U(1) rotation symmetry and Z_N cyclic permutation symmetry, the regular N-gon is a critical point of H. This follows from the equivariant critical point theorem: symmetric functions have critical points at fixed points of the symmetry group.

**Result 3 (V < 0 is generic).** The condition V < 0 requires that the jet/vortex width is smaller than the polygon edge length. This is satisfied whenever the polygon is observationally resolved. If the jet is wider than the edge, the polygon is smeared out and not visible. Therefore: V < 0 is generic for any visible polygon on a rotating planet.

### Tier 2: Specific to attractive/vortex interactions

**Result 4 (Energy maximum from h' < 0).** For pairwise interactions h(|z_j - z_k|), the sign of H''(0) at the N-gon is determined by whether h is decreasing or increasing:

| h(r) | h'(r) | H''(0) | N-gon is |
|------|-------|--------|----------|
| -ln r (Thomson/vortex) | < 0 | < 0 | Energy MAX |
| -1/r (attractive Coulomb) | < 0 | < 0 | Energy MAX |
| -1/r² (attractive inv-sq) | < 0 | < 0 | Energy MAX |
| e^{-r} (Yukawa) | < 0 | < 0 | Energy MAX |
| +1/r (repulsive Coulomb) | > 0 | > 0 | Energy min |
| +r² (spring) | > 0 | > 0 | Energy min |

**The rule: h decreasing → N-gon is energy maximum. h increasing → N-gon is energy minimum.**

Vortex dynamics has h = -ln r (decreasing). Therefore the N-gon is always an energy maximum for vortex systems. This is proven analytically (H'' < 0 for all N ≥ 3) and verified numerically for 9 different interaction types.

**Result 5 (Onsager selection).** In 2D turbulence at negative temperature, systems are driven toward energy maxima (Onsager 1949). Since the N-gon is the energy maximum (Result 4), it is the most probable macrostate. The polygon is statistically selected.

### Tier 3: Planet-specific

**Result 6 (Mode selection).** Which N is selected depends on the specific dynamical mechanism:
- Saturn (N=6): Rossby dispersion n* = R√(β/U) = 5.62 → 6
- Jupiter north (N=8): Vortex self-organization + central cyclone stabilization
- Jupiter south (N=5): Vortex self-organization

**Result 7 (Thermostat).** Atmospheric turbulence provides the effective mixing that drives the large-scale structure toward the Onsager equilibrium. This is observed but not derived from first principles.

## What each tier requires

| Tier | Requires | Status |
|------|----------|--------|
| 1 (Universal) | Hamiltonian + symmetric domain + resolved polygon | **Proven** |
| 2 (Vortex) | Attractive/decreasing pairwise interaction | **Proven** (all N ≥ 3) |
| 3 (Planet) | Specific dynamics + atmospheric thermostat | **Observed** |

## The chain

```
Hamiltonian + rotational symmetry
    → real eigenvalue problem → s² ∈ ℝ → σ = 0 branch exists
    → equivariant critical point → N-gon is dH/dσ = 0

Attractive interaction (h' < 0)
    → H''(0) < 0 → N-gon is energy maximum
    → Onsager negative temperature → polygon is most probable

Mode selection (Rossby / Thomson / other)
    → picks specific N
    → Z_N converts circle to polygon

Atmospheric turbulence
    → thermostat → drives relaxation to Onsager equilibrium
```

## Open questions

1. **Can Tier 2 be made universal?** Is there a deeper reason why planetary vortex interactions are always attractive/decreasing? (The 2D Green's function is logarithmic — this may be forced by dimension.)

2. **Can Step 5 be derived?** The atmospheric thermostat is observed but not derived. What turbulent cascade process provides the effective mixing?

3. **Does this framework predict new polygons?** Uranus and Neptune polar observations would test the universality.

4. **What selects N for Jupiter?** The Rossby mechanism works for Saturn but fails for Jupiter. The Thomson critical ratio provides constraints but doesn't uniquely determine N.
