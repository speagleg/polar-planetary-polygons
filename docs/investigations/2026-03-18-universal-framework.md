# Universal Constraint-Intersection Framework

**Date**: 2026-03-18
**Status**: Implemented and verified

## Problem

The paper explains three planetary polygon configurations through three separate
mechanisms:
- Saturn N=6: Rossby stationarity
- Jupiter north N=8: Thomson stability + Onsager energy monotonicity
- Jupiter south N=5: previously unexplained ("packing constraint outside our framework")

All share the logarithmic Green's function but use it differently. The question:
is there a deeper unifying principle?

## Key Insight

The mechanisms are not competing alternatives but a **constraint intersection**.
Each planet activates a different subset of constraints derived from the same
Green's function. The selected N satisfies ALL applicable constraints simultaneously:

```
N_selected = max { N : N <= N_Thomson(kappa_0/kappa)     [stability]
                       AND sin(pi/N) >= r_excl/R_ring    [packing]
                       AND n is Rossby-stationary          [wave quantization] }
```

## Results

| System | N_obs | N_Thomson | N_Rossby | N_Pack | Binding | Match |
|--------|-------|-----------|----------|--------|---------|-------|
| Saturn (76 deg N) | 6 | 7 | 6 | -- | rossby | YES |
| Jupiter north | 8 | 8 | -- | >8 | thomson | YES |
| Jupiter south | 5 | 8 | -- | 5 | packing | YES |

## Jupiter South N=5 Explanation

The south-pole cyclones are ~2x larger than north-pole cyclones (r ~ 3500 km
vs ~2500 km, Adriani+ 2018). The effective exclusion radius includes a
beta-drift buffer zone (Gavriel & Kaspi 2021):

    r_excl ~ 1.3 * r_cyclone ~ 4.55e6 m

Inverting the packing constraint sin(pi/N) >= r_excl/R with R = 8.0e6 m:
- sin(pi/5) = 0.588 >= 0.569 (OK, N=5 fits)
- sin(pi/6) = 0.500 < 0.569 (N=6 doesn't fit)

The ~30% excess (r_excl/r_cyclone ~ 1.3 vs 1.0) is the beta-drift exclusion
zone: cyclones repel each other through vorticity gradient effects, creating
an effective "personal space" larger than their physical size.

## What is PROVEN vs OBSERVATIONAL

| Claim | Status |
|-------|--------|
| Thomson bound N <= N_Thomson | PROVEN (Theorem 3 + Prop 4) |
| Energy monotonicity H_{N+1} > H_N | PROVEN (Proposition 9) |
| Packing geometry sin(pi/N) >= r_excl/R | PROVEN (elementary) |
| r_excl for Jupiter south ~ 1.3 * r_cyclone | OBSERVATIONAL (Juno + beta-drift) |
| Constraint intersection selects observed N | VERIFIED for 3 cases |
| Spectral gap as robustness indicator | CONJECTURE |

## Ice Giant Predictions

- **Uranus**: North polar cyclone confirmed (Akins+ 2023, VLA microwave).
  Single cyclone observed — no ring/crystal yet. If satellite cyclones
  form a ring, Thomson bound gives N <= 7 (no central vortex) or N <= 8
  (if central cyclone has kappa_0/kappa >= 0.5). Packing may further
  limit N depending on cyclone size vs ring radius.

- **Neptune**: No polar vortex crystal observed. If one forms, expect
  N <= 7 (same Thomson ceiling).

## Implementation

- `src/planetary_polygons/core/universal_selection.py` — core module
- `src/planetary_polygons/extensions/packing_analysis.py` — packing details
- `tests/test_universal_selection.py` — 30 tests (all pass)
- `tests/test_packing_analysis.py` — 11 tests (all pass)
- `notebooks/08_Universal_Framework.ipynb` — verification notebook
