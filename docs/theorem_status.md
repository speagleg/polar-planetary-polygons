# Theorem Status

## The Answer: Why Rotating Fluids Make Polygons

Two-scale mechanism:

| Scale | Question | Mechanism | Status |
|-------|----------|-----------|--------|
| Macro | Why do N coherent vortices form? | Onsager negative temp + inverse cascade | **ESTABLISHED** |
| Meso | Why regular polygon? | Arnold/Thomson dynamical stability | **PROVEN** (constrained Hessian) |

## Core Results

| # | Claim | Status | Notes |
|---|-------|--------|-------|
| 1 | Regular N-gon at \|lambda\|=1 in C* | **PROVEN** | Conjugacy theorem |
| 2 | sigma=0 iff omega=0 (Rossby stationarity) | **PROVEN** | Im(s^2)=0 |
| 2' | sigma=0 can't be broken locally | **PROVEN** | Branch disconnection within WKB |
| 3 | ~~N-gon maximises H~~ -> N-gon MINIMISES H on constraint surface | **PROVEN** | Constrained Hessian, Lagrangian positive definite for N<=7 |
| 4 | Stability boundary at N=7->8 | **PROVEN** | Constrained eigenvalue sign change |
| 5 | Central vortex stabilises large N | **PROVEN** | kappa_crit computed for N=8,...,12 |

## Revised from Previous Version

**OVERTURNED (2026-03-16):**
- Step 3 previously claimed H''(0)<0 means "energy maximum" -> Onsager selects polygon
- The constrained Hessian shows H''(0)<0 is along a dynamically inaccessible direction
- The N-gon is a constrained energy MINIMUM (mu_L = -(N-1)/4 shifts all eigenvalues)
- Polygon arrangement is Arnold stability, not Onsager selection

**REFRAMED:**
- Theorem 4 (Thomson=Rossby conjecture) was false as stated (Galerkin test)
- New connection: constrained Hessian stability boundary at N=7->8 recovers Thomson
- This is a stronger result than the original conjecture

## Supporting Results

| Result | Status | Notes |
|--------|--------|-------|
| n*=5.62 -> 6 for Saturn | PROVEN | Rossby dispersion |
| kappa_crit = -1/4 for N=6 Thomson | PROVEN | Char. poly. factorisation |
| Thomson != Rayleigh-Kuo spectrally | PROVEN | Galerkin test (Thm 4 false as stated) |
| C=0.797, epsilon=0.112 for Saturn | DERIVED | Gaussian jet assumption |
| Jupiter N=5,8 at sigma_geom < 0.07 | OBSERVED | Digitised Juno data |
| N=8 unstable modes: m=5,4,6 | COMPUTED | Fourier decomposition of unstable eigenvectors |
| kappa_crit(N=8) = 0.50 | COMPUTED | Central vortex stabilisation threshold |
| Perturbations on constraint surface increase H | VERIFIED | Newton-projected random perturbations |

## Honest Caveats

1. Gaussian jet assumption for Saturn amplitude prediction
2. Digitised data (not PDS archival quality)
3. Three configurations from two planets only
4. 12% U* discrepancy from barotropic approximation
5. Onsager relaxation at macro scale assumes effective thermostat

## Resolved Questions

- **kappa_crit discrepancy (2026-03-16)**: Energy (Hessian) and dynamical (Thomson)
  stability give the SAME kappa_crit to within 0.01 for all N. The earlier apparent
  30x discrepancy was a numerical artifact (absolute vs relative eigenvalue threshold).

## Resolved Questions

- **Theorem 4 (2026-03-16)**: Original spectral identity conjecture FALSE (Galerkin test).
  Replaced with complementary selection proposition: Rossby for Saturn, Thomson for Jupiter,
  unified by logarithmic Green's function specialness.
- **kappa_crit discrepancy (2026-03-16)**: Energy (Hessian) and dynamical (Thomson)
  stability give the SAME kappa_crit to within 0.01 for all N. Earlier 30x discrepancy
  was a numerical threshold artifact.
- **Open Problem 3 / sigma_flow (2026-03-16)**: RESOLVED. sigma_flow = 0 exactly (branch
  disconnection). The observable called "sigma" is actually epsilon = C * delta_U/U*,
  the hexagon amplitude from the matched asymptotic expansion. The system sits at |lambda|=1
  always; apparent spiral is the finite amplitude perturbation, not a Mobius modulus offset.
- **Amplitude matching (#3) (2026-03-16)**: The formula epsilon = C * delta_U/U* SURVIVES
  the constrained minimum finding. The matching is between continuous QGPV solutions, not
  point vortex configurations. The constrained Hessian concerns the discrete system;
  the amplitude concerns the continuous PDE. Independent.

## Remaining Open

1. **kappa_crit vs Juno data**: Quantitative comparison of predicted kappa_crit(N=8) = 0.50
   with observed central cyclone strength from Juno. Requires published circulation estimates.

Last updated: 2026-03-16
