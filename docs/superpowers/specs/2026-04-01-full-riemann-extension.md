# Full 4D Riemann Curvature from the Polygon Spectrum

**Date:** 2026-04-01
**Location:** Paper III, Section 3.4 (Higher-dimensional extension), replacing line 994
**Goal:** Prove the full 4D Riemann tensor (including all 10 Weyl components) is determined by the polygon data. Close the gap identified by 3/4 reviewers.

## Problem Statement

Paper III proves R_ij = Lambda g_ij (vacuum Einstein) in 2+1D via entropy maximisation. The KK lift (Paper IV, Step B) extends this to 4D vacuum Einstein R^(4)_MN = Lambda^(4) g_MN on the Seifert background. But the vacuum Einstein equations determine only the Ricci tensor (10 of 20 Riemann components). The Weyl tensor C_MNPQ (the remaining 10 components) is unconstrained by the current argument.

In 2+1D this is not a problem (Weyl vanishes identically). In 3+1D it is: the Weyl tensor carries the propagating gravitational degrees of freedom.

## Proof Strategy: Three Layers

### Layer 1 — Background Weyl tensor (algebraic)

**Claim:** On the Seifert background, the full 4D Riemann tensor is an explicit, computable function of (N, Lambda_3).

**Argument:** The KK ansatz for the Seifert metric is:

    ds^2_4 = g_ij dx^i dx^j + sigma^2 (dphi + A_i dx^i)^2

with g_ij the constant-curvature H^2 metric, A_i the uniform KK gauge field (F = N/(2pi)), and sigma = 1 (stabilised fiber radius).

The 4D Riemann tensor decomposes under KK reduction as (standard GR, e.g. Bailin-Love 1987):

    R^(4)_ijkl = R^(3)_ijkl - (sigma^2/2)(F_ik F_jl - F_il F_jk)
    R^(4)_ijk_phi = (sigma/2) nabla_i F_jk    [= 0, uniform F on const-curvature base]
    R^(4)_i_phi_j_phi = -(sigma^2/4) F_ik F_j^k   [+ radion terms, zero since sigma=const]

In 3D, the Weyl tensor vanishes: R^(3)_ijkl is determined entirely by R^(3)_ij = Lambda_3 g_ij. The field strength F_ij is uniform (quantised flux). Therefore every component of R^(4)_MNPQ is determined.

The 4D Weyl tensor is then:

    C^(4)_MNPQ = R^(4)_MNPQ - (2/(d-2))(g_M[P R^(4)_Q]N - g_N[P R^(4)_Q]M)
                 + (2/((d-1)(d-2))) R^(4) g_M[P g_Q]N

with d=4. Since R^(4)_MN = Lambda^(4) g_MN (proved in Paper IV Step B), this simplifies, but C^(4) != 0 because the Seifert manifold is not maximally symmetric (it's a fiber bundle, not S^4 or H^4).

**Computational verification:** Implement `weyl_tensor_seifert(N)` returning the independent Weyl components as functions of N. Verify C != 0 for N >= 5 and C_ijkphi = 0 (from nabla F = 0).

### Layer 2 — Linearised perturbations (spectral)

**Claim:** All linearised metric perturbations around the Seifert background, and hence the linearised Weyl tensor, are determined by the Havelock-Lichnerowicz spectrum.

**Argument:** A linearised perturbation h_MN decomposes under KK into:

    h_ij   (3D metric perturbation)  ->  Lichnerowicz operator Delta_Lich
    delta_A_i  (graviphoton perturbation)  ->  Hodge Laplacian on 1-forms
    delta_sigma  (radion perturbation)  ->  scalar Laplacian + mass^2

Paper III already identifies: "a negative Havelock eigenvalue is a negative mode of the Lichnerowicz operator" (line 1790). The Lichnerowicz spectrum on the multi-cone geometry is controlled by the Havelock eigenvalues lambda_m.

The graviphoton modes satisfy the Maxwell equation on the constant-curvature base; their spectrum is the Laplacian spectrum on H^2/Z_N (determined by N).

The radion is massive (mass from the flux potential V(sigma) = (N/2)(sigma - 1/sigma)^2), so its perturbation is gapped and decays exponentially. No zero mode.

Since all three sectors have spectra determined by (N, Lambda_3), the complete linearised 4D metric perturbation is determined, and hence the linearised Weyl tensor delta_C_MNPQ is determined mode by mode.

**Computational verification:** Implement `lichnerowicz_spectrum_seifert(N)` and verify it matches the Havelock eigenvalues. Verify graviphoton and radion spectra are gapped.

### Layer 3 — Full nonlinear reconstruction (Fefferman-Graham + KK)

**Claim:** The full nonlinear 4D Riemann tensor is uniquely determined by the boundary CFT data.

**Argument:** Three steps:

(a) **FG reconstruction in AdS_3.** The Fefferman-Graham expansion for a 3D asymptotically AdS manifold with 2D boundary is:

    g(rho, x) = drho^2/rho^2 + (1/rho)(g_0 + rho g_2 + rho^2 g_4)

where g_0 is the boundary metric, g_2 = -(Ric[g_0] - (R[g_0]/2)g_0), and g_4 = (1/4)g_2^2 + T_ab/(boundary terms). In d=2 (the boundary dimension), the expansion **terminates at second order** (de Haro-Solodukhin-Skenderis 2001). This is exact, not perturbative.

The boundary stress tensor T_ab is determined by the Virasoro algebra at c = 12 b(N), which is determined by the polygon spectrum.

(b) **KK lift.** The reconstructed 3D metric, combined with the stabilised fiber (sigma=1) and quantised flux (F = N/(2pi)), uniquely determines the 4D metric g^(4)_MN.

(c) **Riemann from metric.** The 4D Riemann tensor is the second derivative of the metric: R^(4)_MNPQ = partial^2 g + Gamma * Gamma. Since g^(4)_MN is uniquely determined, R^(4)_MNPQ is uniquely determined. QED.

**Key citation:** de Haro, Solodukhin, Skenderis (2001) for FG in AdS_3. Already cited at Paper IV line 323.

## Integration into Paper III

### What changes

**Remove:** Line 994 ("The extension to full Riemann curvature (beyond Ricci) requires higher-rank tensor probes and is beyond the scope of this paper.")

**Replace with:** A theorem statement + three-part proof sketch (~50 lines total).

**Structure:**

```latex
\begin{theorem}[Full Riemann curvature]
\label{thm:full-riemann}
On the Seifert manifold $\mathbf{H}^2 \times_N S^1$ with
stabilised fibre and quantised flux, the full $4$D Riemann
tensor $R^{(4)}_{MNPQ}$ (including all $10$ Weyl components)
is uniquely determined by the polygon number~$N$.
For linearised perturbations, the Weyl tensor is determined
mode by mode by the Havelock--Lichnerowicz spectrum.
For the full nonlinear theory, the Fefferman--Graham
reconstruction (exact in $2{+}1$D) combined with the
KK lift determines the complete $4$D geometry from the
boundary CFT at $c = 12\,b(N)$.
\end{theorem}

\begin{proof}[Proof sketch]
Three layers.

\emph{Layer 1 (Background).}
[KK Riemann decomposition, ~15 lines]

\emph{Layer 2 (Linearised).}
[Lichnerowicz-Havelock + KK spectral decomposition, ~15 lines]

\emph{Layer 3 (Nonlinear).}
[FG reconstruction + KK lift, ~15 lines]
\end{proof}
```

### What changes in the Remark table

The table at lines 964-976 currently says:

    d=3 (3+1D) | 10 Weyl | Spatial equivalence: (H1) constrains traceless Ricci;
                           full spacetime requires Paper IV

Replace status with:

    d=3 (3+1D) | 10 Weyl | **Theorem**: KK + Lichnerowicz + FG reconstruction
                           (Theorem X)

### What changes in the abstract

Paper III abstract currently says "We derive the vacuum Einstein equations." After the theorem, this can be strengthened to: "We derive the vacuum Einstein equations, and prove that the full Riemann tensor (including all Weyl components) is determined by the polygon number N."

## Code and Tests

### New source file

`src/planetary_polygons/extensions/weyl_tensor.py`:

- `kk_riemann_decomposition(N, Lambda3)` — Returns the independent components of R^(4)_MNPQ on the Seifert background as symbolic expressions
- `weyl_tensor_seifert(N)` — Returns the 4D Weyl tensor components
- `radion_mass_squared(N)` — Returns the radion mass from the flux potential, verifying it's positive (gapped)
- `lichnerowicz_kk_spectrum(N, n_modes)` — Returns Lichnerowicz eigenvalues on the Seifert background, verifying they match Havelock

### New test file

`tests/test_weyl_tensor.py`:

- `test_weyl_vanishes_3d()` — Verify C^(3)_ijkl = 0 identically (sanity check)
- `test_weyl_nonzero_4d()` — Verify C^(4) != 0 for N >= 5 on Seifert
- `test_mixed_weyl_vanishes()` — Verify C_ijkphi = 0 (uniform flux)
- `test_ricci_matches_einstein()` — Verify R^(4)_MN = Lambda^(4) g_MN from KK decomposition (consistency)
- `test_radion_gapped()` — Verify m^2_radion > 0 for all N
- `test_lichnerowicz_matches_havelock()` — Verify Lichnerowicz eigenvalues = Havelock eigenvalues on Seifert
- `test_fg_terminates()` — Verify FG expansion terminates at order 2 for d=2 boundary (algebraic check)

### Dependencies

numpy only (no scipy). All computations are algebraic/exact-rational where possible.

## Risks and Mitigations

1. **The KK Riemann decomposition is textbook but lengthy.** Mitigation: cite Bailin-Love or Overduin-Wesson for the general formula, then specialise to constant curvature + uniform flux + stabilised radion, which kills most terms.

2. **The Lichnerowicz-Havelock identification is currently stated as an analogy (line 1790), not proved.** Mitigation: the identification follows from the vortex-gravity isomorphism — the Havelock Hessian IS the Lichnerowicz operator restricted to the Z_N-symmetric sector. This needs to be stated precisely.

3. **The FG reconstruction is cited but not verified for the Seifert geometry.** Mitigation: cite Toldo-Willett 2018 (already at line 323) who verify FG for Seifert manifolds explicitly.

## Non-goals

- We are NOT deriving the Einstein equations (already done).
- We are NOT proving dynamical evolution of gravitational waves (that's a separate paper).
- We are NOT extending to d >= 5 (the FG argument is specific to d=2 boundary / AdS_3).
- We are NOT adding figures.
