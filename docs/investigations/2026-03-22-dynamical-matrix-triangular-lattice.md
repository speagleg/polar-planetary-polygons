# Dynamical Matrix: The Triangular Lattice is Always Stable

**Date:** 2026-03-22
**Status:** COMPUTED (dynamical matrix with convergence study)
**CORRECTION:** Supersedes the supercell result "Δ_tri ≈ 0.8" from earlier in this session.

## The Correction

The earlier supercell computation (periodic Hessian on small torus cells)
reported the triangular lattice as unstable for Δ < 0.8. This was WRONG:

1. Dirichlet BC broke translational symmetry → non-equilibrium point
2. Periodic BC with small supercells had insufficient lattice image shells
3. The lattice sum for 2Δ+2 < 3 converges very slowly (~R^{-(2Δ+0.6)})

The correct computation uses the **dynamical matrix** D(k) — the standard
phonon approach — which gives the exact infinite-lattice result through
a k-dependent lattice sum at each Brillouin zone point.

## The Dynamical Matrix

For V = r^{-2Δ} on the triangular lattice:

$$D_{\alpha\beta}(\mathbf{k}) = 2\Delta \sum_{\mathbf{R}\neq 0}
  R^{-2\Delta-2} \left[(2\Delta+2)\hat{R}_\alpha\hat{R}_\beta - \delta_{\alpha\beta}\right]
  (1 - \cos\mathbf{k}\cdot\mathbf{R})$$

Stability requires min_k min_eigenvalue D(k) ≥ 0.

## Results

### Triangular lattice: ALWAYS STABLE

| Δ | ω²(K) | ω²(M) | Converged? |
|---|--------|--------|:---:|
| 0.3 | +0.49 (extrap) | +0.35 | ✓ (Richardson) |
| 0.5 | +1.06 (extrap) | +1.39 | ✓ (Richardson) |
| 1.0 | +3.65 | +4.88 | ✓ (direct) |
| 2.0 | +15.47 | +20.65 | ✓ (direct) |
| 5.0 | +120.65 | +160.88 | ✓ (direct) |

The minimum eigenvalue is at the **K-point** (1/3, 1/3) for all Δ.
It is ALWAYS positive: no instability exists.

**Δ_tri does not exist.** The triangular lattice has no phase transition.

### Square lattice: ALWAYS UNSTABLE

| Δ | ω²(X) | ω²(M) |
|---|--------|--------|
| 0.5 | **−0.60** | +5.81 |
| 1.0 | **−1.87** | +18.08 |
| 2.0 | **−6.84** | +65.22 |
| 5.0 | **−33.71** | +400.05 |

The instability is at the **X-point** (π, 0): a stripe deformation where
alternating columns displace in opposite directions. Well-converged
(stable across shell counts). The square lattice has no stable regime.

### Summary

| Lattice | Coordination | Stable? | Instability point |
|---------|:-----------:|:-------:|:--:|
| Triangular {3,6} | 6 | **ALWAYS** | — |
| Square {4,4} | 4 | **NEVER** | X-point (stripe) |
| Hexagonal {6,3} | 3 | **NEVER** | K-point (honeycomb) |

## Why the Triangular Lattice is Special

The triangular lattice has coordination number 6 — the maximum for a 2D
Bravais lattice. Each vertex has 6 equidistant nearest neighbors arranged
symmetrically at 60° intervals. This provides enough restoring force in
every direction to stabilize all phonon modes.

The square lattice has coordination 4 and a "soft direction" along the
diagonal (the (1,1) direction has no nearest-neighbor bond). The X-point
instability exploits this: the stripe mode displaces rows perpendicular
to the soft direction.

This is the lattice analogue of the single-polygon result: the triangle
(N=3) is stable because all chord distances are equal (single distance
→ no mode competition). The triangular lattice (coordination 6) is
stable because all nearest-neighbor directions are equivalent (uniform
angular distribution → no soft direction).

## Impact on Paper II

The tessellation subsection (§10.11) must be corrected:
- The claim "triangular lattice stabilizes at Δ ≈ 0.8" is WRONG
- The correct statement: "the triangular lattice is always stable"
- The table of "Δ_tri transitions" should be removed
- The theorem and CDT remark STRENGTHEN: triangulation is stable at
  ALL interaction ranges, not just Δ ≥ 1

The corrected result is actually STRONGER than what we claimed:
the triangular lattice doesn't just stabilize first — it's the ONLY
regular lattice that is ever stable, at any Δ.
