# Legacy Code Cleanup — Spec 2 of 3

## Goal

Add informative deprecation notices to 3 source modules and mark old CKM test classes with `@pytest.mark.deprecated`. No functional changes. Code-only (no LaTeX).

## Context

Spec 1 built the new backbone modules (orbit_ckm.py, etc.) alongside the old code. The old code has known issues:
- ckm_mixing.py: uses RIGHT rotation (Y†Y) instead of LEFT (YY†)
- ckm_toeplitz.py: uses Plancherel formula delta=2*theta_CS*tanh(pi)=68.63 deg
- fermion_derivation.py: contains the old 70.2 deg formula (calculus error)

This spec marks them as deprecated with informative notices directing readers to the new modules. Old tests still pass but are filterable via pytest markers.

## Files to modify

| File | Change |
|------|--------|
| src/planetary_polygons/extensions/ckm_mixing.py | Module-level + per-function deprecation docstrings |
| src/planetary_polygons/extensions/ckm_toeplitz.py | Module-level + per-function deprecation docstrings |
| src/planetary_polygons/proofs/fermion_derivation.py | Section-level deprecation for lines 329-382 |
| tests/test_ckm_mixing.py | @pytest.mark.deprecated on test classes |
| tests/test_ckm_toeplitz.py | @pytest.mark.deprecated on test classes |
| tests/test_fermion_derivation.py | @pytest.mark.deprecated on CKM test classes |
| pyproject.toml | Register deprecated marker |

## Deprecation notice content

### ckm_mixing.py (module-level)

```
DEPRECATED: This module uses the Plancherel formula (delta=68.63 deg) and
the RIGHT rotation (Y†Y instead of YY†). Both are superseded by orbit_ckm.py
which uses the Gauss sum derivation (delta=arctan(sqrt(7))), LEFT rotation,
and instanton K^(N-1) correction.
See docs/investigations/2026-04-09-bernoulli-havelock-backbone.md.
```

Per-function notices on: ckm_matrix(), build_yukawa_complex(), eta_invariant_phase()

### ckm_toeplitz.py (module-level)

```
DEPRECATED: The theta_CS * tanh(pi) formula is superseded by the Gauss sum
derivation in orbit_ckm.py. The tanh(pi) Plancherel factor was based on the
scalar spectral function, not the Dirac operator.
See orbit_ckm.py for the corrected CKM.
```

Per-function notices on: yukawa_amplitude()

### fermion_derivation.py (section-level only)

```
DEPRECATED (CKM section, lines 329-382): The formula
delta = (1/2) log cosh(pi) = 70.2 deg contains a calculus error
(d/ds arg Gamma = Re psi, not Im psi).
Superseded by orbit_ckm.py.
```

## Test markers

Register in pyproject.toml:
```toml
[tool.pytest.ini_options]
markers = ["deprecated: tests for deprecated modules (deselect with -m 'not deprecated')"]
```

Apply @pytest.mark.deprecated to all test classes in:
- test_ckm_mixing.py
- test_ckm_toeplitz.py  
- test_fermion_derivation.py (CKM-related classes only)

## Success criteria

1. All existing tests still pass (0 failures)
2. pytest -m deprecated runs only old CKM tests
3. pytest -m "not deprecated" excludes them
4. No functional code changes (only docstrings and decorators)
5. 171 backbone tests unaffected
