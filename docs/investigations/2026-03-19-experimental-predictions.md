# Experimental Predictions for Hyperbolic Lattices

**Date:** 2026-03-19
**Status:** PREDICTIONS (falsifiable, parameter-free)

## Target Platforms

1. **Circuit QED** (Kollár-Fitzpatrick-Houck, Princeton, 2019):
   Microwave resonators on {p,q} hyperbolic tilings.
   Demonstrated: {6,4} and {8,3} lattices.

2. **Electric circuits** (Lenggenhager et al., 2022):
   Topoelectric circuits on {8,3} tiling, measured band structure.

3. **Photonic lattices** (future): Coupled waveguides on H² geometry.

## The Five Exact Thresholds

| Transition | ξ* | R*/a | Exact form | Field |
|-----------|-----|------|-----------|-------|
| 7→8 | 0.0627 | 0.251 | 8−3√7 | Q(√7) |
| 8→9 | 0.2087 | 0.457 | (5−√21)/2 | Q(√21) |
| 10→11 | 0.1716 | 0.414 | 3−2√2 | Q(√2) |
| 14→15 | 0.2680 | 0.518 | 2−√3 | Q(√3) |
| 22→23 | 0.3820 | 0.618 | (3−√5)/2 | Q(√5) |

These are EXACT algebraic numbers determined by the Z_N Casimir
and the conformal inversion symmetry of H². No fitting, no
free parameters.

## Four Testable Predictions

**Prediction 1 (qualitative — the cleanest test)**:
On a hyperbolic lattice, a ring of N > 7 vortex-like excitations
is stable WITHOUT a central defect. This is impossible on flat
geometry. Test: create N=12 ring at R/a ≈ 1 and verify stability.

**Prediction 2 (quantitative — exact thresholds)**:
Vary the ring radius R on a {8,3} lattice and find the critical
ξ = R²/a² where the 7→8 transition occurs. The predicted value
ξ* = 8−3√7 = 0.0627 is exact.

**Prediction 3 (number-theoretic — the algebraic structure)**:
The thresholds are Pell units satisfying ξ·(1/ξ) = 1 in
quadratic fields. The discriminants {7, 21, 2, 3, 5} are
predicted by the Z_N representation theory, not by the
lattice geometry.

**Prediction 4 (falsifiable bound)**:
N_crit ≤ 7 on ANY surface with K ≥ 0. Observing N ≥ 8 stable
ring without central defect on a flat or spherical surface
would falsify the entire framework.

## Experimental Protocol

1. **Lattice preparation**: Fabricate {8,3} lattice with ≥50 sites.
   Effective curvature radius a = L/0.727 where L is the physical
   edge length.

2. **Ring creation**: Place N excitations at sites forming a ring
   of radius R = a√ξ for controlled ξ values.

3. **Stability measurement**: Observe persistence vs breakup.
   Time-resolve the dynamics after initial preparation.

4. **Threshold extraction**: Scan ξ from 0 to 0.5 and identify
   N_crit(ξ). Compare with the exact threshold table.

## Practical Considerations

**Most practical first test**: N=12 ring at R/a ≈ 1.
On the flat plane: N=12 is strongly unstable (μ=7).
On H² at R/a ≈ 1: N=12 should be stable (N_crit ≈ 12).
This qualitative test requires no precise threshold measurement.

**For the {8,3} lattice**:
- 7→8 transition: ring ≈ 2.2 edge lengths from center (~18 sites around ring)
- 22→23 transition (golden ratio): ring ≈ 5.3 edges from center (~1600 total sites)

**Caveat**: The point vortex model assumes a continuum; the lattice
is discrete. The correspondence requires the lattice spacing to be
much smaller than the ring radius (many lattice sites per ring).
For the 7→8 transition with ~18 sites around the ring, discretization
effects may be significant. The 22→23 transition with ~123 sites
around the ring would be more reliable but requires a larger lattice.
