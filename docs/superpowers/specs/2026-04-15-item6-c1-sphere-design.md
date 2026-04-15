# Item #6 — C₁(S²) Geodesic Derivation Design

**Date:** 2026-04-15
**Input:** `docs/PAPER1_RIGOR_REWRITE_SPEC.md`, Structural Rewrite #6
**Problem:** The boxed C₁(S²,ξ) = (N-1)(1-ξ)/(1+ξ) formula — on which the entire §4.2 threshold table depends — is cited from Boatto-Cabral 2003 but not derived in the paper. Reviewer: "not actually derived in the paper."
**Goal:** Full first-principles derivation from the geodesic Green's function on S², following the same sandbox workflow as Item #1.

## Sandbox structure

```
docs/rigor-sandbox/item6-c1-sphere/
├── derivation.tex       # standalone LaTeX (~3-4 pages)
├── numerical_check.py   # symbolic + numerical verification
├── review-notes.md      # math-reviewer feedback rounds
└── replacement-proof.tex # approved appendix replacement
```

## Derivation strategy

The appendix (`latex/paper-A-appendices/main.tex`, lines 178-336) already contains:

- The S² Hamiltonian in stereographic coordinates: H_sph = -Σ log|z_j - z_k| + (N-1)/2 Σ log(1+|z_k|²) (eq:H_sph)
- The equilibrium rotation rate Ω = (N-1)(1-ξ²)/(8ξ) (eq:Omega_S2)
- Three Euclidean-frame second-variation terms yielding C₁^eucl = (N-1)(1+ξ²)/(1+ξ)² (eq:C1-eucl-frame)
- A "Limitation" paragraph correctly noting that C₁^eucl is NOT the geodesic-frame result
- A citation of BC2003 for C₁(S²) = (N-1)(1-ξ)/(1+ξ) (eq:C1_S2, the boxed formula)

**What's missing:** The derivation that converts the Euclidean-frame computation to the geodesic-frame result, or equivalently a direct computation using the geodesic pair interaction.

### Key mathematical content

The geodesic Green's function on S² in stereographic coordinates is:
```
h_geo(z_j, z_k) = -log|z_j - z_k| + (1/2)log(1+|z_j|²) + (1/2)log(1+|z_k|²) - log 2
```

The derivation will:
1. Start from h_geo and compute the mode-m radial second variation directly
2. The pairwise correction terms `(1/2)log(1+|z_j|²) + (1/2)log(1+|z_k|²)` contribute additional second-variation terms beyond those in the Euclidean computation
3. The constraint on S² is angular momentum J = Σ cos θ_k (not Euclidean L = Σ|z_k|²), which changes the Lagrange multiplier structure
4. Geodesic-frame normalization: at the ring with |z| = r_E, the stereographic conformal factor σ = 2/(1+ξ) rescales perturbation distances
5. Combining all corrections yields C₁(S²) = (N-1)(1-ξ)/(1+ξ)

### Numerical verification

`numerical_check.py` will verify:
- C₁(S²,ξ) = (N-1)(1-ξ)/(1+ξ) matches `riemannian_havelock.C1_sphere(N, ξ)` for N ∈ [3,10], ξ ∈ {0.1, 0.2, ..., 0.9}
- C₁(S²,ξ) matches `curved_surfaces.sphere_constrained_eigenvalues()` oracle for sampled (N, colatitude) pairs
- Each intermediate algebraic step verified symbolically (sympy) to 30 digits
- Boundary cases: ξ→0 gives N-1 (flat limit), ξ=1 gives 0 (equator)

## Gates (same as Item #1)

1. **Numerical gate:** `numerical_check.py` exits 0
2. **math-reviewer gate:** Score ≥ 9.0 AND zero structural deductions on sandbox only
3. **Diff approval gate:** User approves the exact appendix replacement before it lands
4. **Regression gate:** Paper builds cleanly, full test suite passes (4447+ tests)

## Scope

- Replace appendix §2 (lines 178-336 of `latex/paper-A-appendices/main.tex`) with the full geodesic derivation
- Preserve: `eq:C1_S2` label, `app:c1_s2` section label, "Properties" items
- The existing Euclidean-frame derivation (terms 1-3) may be kept as intermediate steps if useful, or replaced if cleaner
- No changes to any other paper section or any other appendix section

## Non-goals

- No changes to `latex/paper/main.tex`
- No changes to §4.2 threshold table (it's already correct, just needs the appendix formula derived)
- No physics-reviewer pass (pure math)

## References

- Existing tests: `tests/test_curved_surfaces.py`
- Source of truth: `src/planetary_polygons/extensions/riemannian_havelock.py:C1_sphere()`
- Spec: `docs/PAPER1_RIGOR_REWRITE_SPEC.md`, Item #6
- Item #1 workflow: `docs/superpowers/specs/2026-04-14-paper1-rigor-sandbox-design.md`
