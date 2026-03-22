# The Lorentzian Continuation: sinh/cosh and the BTZ Horizon

**Date:** 2026-03-22
**Status:** COMPUTED — five concrete results from the JT gravity hint

## The Hint

The JT gravity test found:
- C₁ = log(2sinh ρ) — our system, EXACT
- C₁^{JT} = log(cosh ρ) — JT gravity, FAILS

Same IR (both → ρ + const), different UV.

## Result 1: sinh = exterior, cosh = interior

The complex shift ρ → ρ + iπ/2 converts between them:

    sinh(ρ + iπ/2) = i·cosh(ρ)
    log(2sinh(ρ + iπ/2)) = log(2cosh(ρ)) + iπ/2

In the BTZ geometry:
- ρ real: the EXTERIOR (spatial geodesic distance from horizon)
- ρ + iπ/2: the INTERIOR (behind the horizon, Kruskal extension)

Our vortex system lives in the BTZ exterior. JT gravity probes
the interior. They are connected by the Kruskal analytic continuation.

Verified: the shift log(coth ρ) = log(2cosh) - log(2sinh) vanishes
exponentially for large ρ (same IR) and diverges logarithmically
at ρ → 0 (different UV).

## Result 2: Wick rotation recovers flat-space theory

Under ρ → it:

    sinh(ρ) → i·sin(t)
    C₁ = log(2sinh ρ) → log(2sin t) + iπ/2

The real part log(2sin t) IS the flat-space Havelock kernel.
The imaginary part π/2 is a constant Berry phase.

The three geometries sit at different imaginary parts:

| Im(ρ) | Geometry | Kernel | Curvature |
|-------|----------|--------|-----------|
| 0 | H² | log(2sinh ρ) | K = -1 |
| π/2 | Flat R² | log(2sin t) | K = 0 |
| π | Sphere S² | log(2cos t) | K = +1 |

This connects the analytic continuation to the developing map
analysis (which parameterizes the same three geometries via β).

## Result 3: Universal resonance width Γ = π

Each palindromic threshold at real ρ* becomes a complex resonance
at ρ* + iπ/2 with:

    Re(λ) = 0 (the threshold condition)
    Im(λ) = π/2 (UNIVERSAL, independent of N and m)

The quasi-bound polygon state has lifetime τ = 1/π.

The threshold curve in the complex ρ-plane:
- For N = 6: x*(JT) - ρ* = -0.14 (significant shift)
- For N = 8: shift = -0.017 (small)
- For N ≥ 12: shift < 10⁻⁴ (exterior/interior nearly coincide)

The exterior/interior distinction sharpens with N because
sinh ρ ≈ cosh ρ for large ρ (the threshold moves outward with N).

## Result 4: Time-space exchange at the threshold

For the critical mode m* at geodesic radius ρ:

| ρ vs ρ* | λ_{m*} | Physical interpretation |
|---------|--------|----------------------|
| ρ > ρ* | λ > 0 | EXTERIOR: mode oscillates in time (freq √λ) |
| ρ = ρ* | λ = 0 | HORIZON: frozen mode (Killing vector null) |
| ρ < ρ* | λ < 0 | INTERIOR: mode grows spatially (rate √|λ|) |

Verified for N = 8 (rho* = 2.40):

    ρ = 0.40: λ = -2.58, spatial growth rate 1.61
    ρ = 2.40: λ =  0.00, HORIZON
    ρ = 4.40: λ = +2.01, oscillation freq 1.42

The polygon-BTZ transition IS the exchange of time and space.
This resolves the problem of time at the threshold: the frozen
formalism (λ = 0) is the horizon, where the Killing vector
degenerates from timelike to spacelike.

## Result 5: The spectral flow clock

The palindromic staircase as a sequence of horizon crossings:

    ρ < ρ*(7): all polygons stable (AdS vacuum)
    ρ = ρ*(7): heptagon crosses horizon (first transition)
    ρ = ρ*(8): octagon crosses horizon
    ...
    ρ = ρ*(N): N-gon crosses horizon

Each crossing has:
- Critical exponent ν = 1/2 (universal, from single zero mode)
- Amplitude A(N) = 2^{3(N-2)/4}/(N-3)!! (frozen determinant)
- Resonance width Γ = π (universal, from Lorentzian continuation)
- Lifetime τ = 1/π (universal)

## The Lorentzian partition function

The Euclidean partition function near threshold:

    Z_E(ρ) ~ A(N) · |ρ - ρ*|^{-1/2}

Under Lorentzian continuation (ρ → ρ + iε):

    Z_L(ρ) ~ A(N) · (ρ - ρ* + iε)^{-1/2}

This has:
- Branch cut at ρ = ρ* (the horizon)
- Spectral function: Im[Z_L] ~ A(N)/√2 · |ρ - ρ*|^{-1/2}
- Van Hove singularity at the polygon-BTZ transition

## What's missing: the dynamics of ρ

The framework is complete as a STATIC theory: given (N, ρ, surface),
it computes the full partition function and stability spectrum.

The Lorentzian continuation adds the resonance structure and the
time-space exchange. But it does NOT determine the dynamics of ρ
itself. The spectral flow clock tells us "if ρ evolves, here's what
happens" — not "here's why ρ evolves."

The missing piece: a second equation relating ρ to physical
parameters (Rossby number, deformation radius, planetary radius).
The QG-PV equation provides this — it determines the equilibrium ρ
as a function of the jet stream. Coupling QG-PV to the partition
function would close the system.

## Physical predictions

1. The polygon-BTZ transition temperature: T_H = coth(ρ*)/(2π)
   → 1/(2π) for large ρ*. Measurable from infrared data.

2. Quasi-normal mode spectrum: frequencies √λ_m with universal
   damping Γ = π. The ratio of consecutive frequencies is set by
   the Casimir gaps (N-2m)²/8.

3. N_crit interpolation: from 7 (H²) to 4 (S²) through the
   developing map. Constrains the effective curvature at each planet.

## Code

`lorentzian_continuation.py`: 7-part analysis (complex shift,
Wick rotation, three geometries, resonances, Lorentzian partition
function, spectral flow, BTZ connection).
