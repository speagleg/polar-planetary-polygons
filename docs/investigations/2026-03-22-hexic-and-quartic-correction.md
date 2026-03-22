# The Quartic and Hexic at the Critical Mode: Correction and Scaling

**Date:** 2026-03-22
**Status:** CORRECTED — the quartic is nonzero; exact scaling under investigation

## Correction: ∂⁴H/∂a⁴ ≠ 0 at the Self-Paired Mode

The earlier computation showing ∂⁴H/∂a⁴ = 0 at m = N/2 was an
artifact of the MULTI-MODE perturbation used. When perturbing
ONLY the single mode m = N/2 (the correct computation for the
stability resolution), the fourth derivative is:

| N | m = N/2 | ∂⁴H/∂a⁴ |
|---|---------|----------|
| 6 | 3 | 486 |
| 8 | 4 | 2,049 |
| 10 | 5 | 6,255 |
| 12 | 6 | 15,571 |
| 14 | 7 | 33,669 |
| 16 | 8 | 65,676 |

**All positive.** The quartic DOES resolve the marginal stability
at the self-paired critical mode, confirming N_crit = 7 is stable
at quartic order for ALL even N.

## The Two Quartic Quantities

The confusion arose from two different quartic objects:

1. **Q_{m,-m,m,-m}** = the MODE-ISOLATED quartic coupling coefficient,
   computed from the transfer matrix product. This satisfies
   Q/f² = N/48 exactly. It measures the coupling between mode m
   and its palindromic partner N-m in the INTERACTION basis.

2. **∂⁴H/∂a_m⁴** = the FULL fourth derivative of the Hamiltonian
   with respect to a single-mode amplitude. This includes
   contributions from ALL modes (through the nonlinear interaction)
   and is much larger than Q alone.

The relation: ∂⁴H/∂a⁴ = Q_{m,-m,m,-m} + (cross-mode contributions)
The cross-mode contributions are LARGE and POSITIVE, overwhelming
the diagonal Q. The previous "zero" result was from a computation
that mistakenly measured the cross-mode CANCELLATION (where two modes
are perturbed simultaneously and their quartic contributions cancel),
not the single-mode fourth derivative.

## The Q/f² = N/48 Identity Stands

The identity Q/f² = N/48 at the critical mode (even N) remains
EXACT (verified to 10⁻¹⁵). It describes the DIAGONAL quartic
coupling in the mode-interaction basis. The FULL quartic at the
critical mode is larger because it includes off-diagonal contributions.

## The Fourth Derivative Scaling

∂⁴H/∂a_{N/2}⁴ grows rapidly with N. Approximate scaling:

$$\frac{\partial^4 H}{\partial a_{N/2}^4} \propto N^a \cdot f_{\text{crit}}^b$$

Under investigation (see next computation).

## The Sixth Derivative

The sixth derivative ∂⁶H/∂a⁶ is also nonzero and positive:

| N | β₀ = ∂⁶H/(6!·∂a⁶) |
|---|---------------------|
| 6 | 48.8 |
| 8 | 365 |
| 10 | 1,737 |
| 12 | 6,224 |
| 16 | 46,665 |
| 20 | 222,580 |

The scaling: β₀ ∝ f^{3.5} (between f³ and f⁴). The non-integer
exponent suggests the hexic involves a more complex combination
of the Casimir and N than the clean N/48 of the quartic.

## For the Paper

1. The quartic resolves stability at m = N/2 for ALL even N (∂⁴H > 0).
2. Q/f² = N/48 is exact for the DIAGONAL coupling.
3. The FULL ∂⁴H includes large cross-mode contributions.
4. The distinction between Q (mode-interaction) and ∂⁴H (full derivative)
   must be stated clearly.
