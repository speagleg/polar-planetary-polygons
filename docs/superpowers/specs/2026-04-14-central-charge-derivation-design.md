# Design: first-principles derivation of `c = 12 b(N)`

**Date:** 2026-04-14
**Status:** approved by Gordon, awaiting spec review
**Target gap:** Paper III Gap A (R7 reviewer flagged `c = 12 b(N)` as a definition rather than a derivation)

## 1. Goal

Prove that the central charge of the polygon boundary CFT equals
```
c = 12 b(N),   b(N) = N(N+1)/12 − log 2 + log(N)/(N−1).
```
"First-principles" here means: extract `c` as the coefficient of the conformal anomaly of a well-defined 2D operator (not as a defined coefficient in a mode-independent offset), and show this coefficient equals `12 b(N)` by computation — ideally via three independent routes that must agree.

## 2. Object of study

Let `D` be the Poincaré disk with hyperbolic metric `g_hyp`. Place `N` punctures at the regular `N`-gon vertices `z_k = e^{2πik/N}`. The punctured surface `Σ_N = D \ {z_1,...,z_N}` carries a scalar Laplacian `Δ_Σ` with **cone-angle boundary conditions** `2π/N` at each puncture (vortex monodromy `e^{2πi/N}`).

The physical identification: 2D point vortices with unit circulation on `H²` are Coulomb-gas charges with Green's function `G(z,w) = −(1/2π) log|ρ(z,w)|`, and the Kirchhoff Hamiltonian at the `N`-gon is precisely the regularized Liouville action at the classical saddle with these `N` conical sources.

## 3. Three-pipeline derivation

All three produce `c`, but via different layers: (A) classical saddle action via TZ, (B) one-loop quantum anomaly via spectral zeta, (C) physical Kirchhoff-Liouville identification. `c` is a single scalar invariant of the CFT; agreement across the three layers (classical / quantum / physical) is what makes the result a derivation rather than a definition.

### Pipeline A — Classical Liouville action (Takhtajan–Zograf)

**Input:** saddle-point field `φ_*` solving the Liouville PDE
```
Δφ = e^{2φ} − (π/N) Σ_k δ(z − z_k)
```
with cone-angle `2π/N` at each puncture.

**Output:** regularized Liouville action `S_L[φ_*]`, evaluated at the `N`-gon saddle.

**Central charge extraction:** by Takhtajan–Zograf (punctured sphere, 2003), `−S_L[φ_*]/π` is a Kähler potential for the Weil–Petersson metric on `M_{0,N}`. In the semiclassical quantization,
```
Z_Liouville[g] = exp(−(c/6π) · S_L[φ_*] + (one-loop) + ...)
```
so the coefficient of `S_L[φ_*]` in `log Z` equals `−c/(6π)`. We extract `c` by evaluating `S_L[φ_*]` at the regular `N`-gon saddle (symmetric configuration, closed form via TZ's explicit formula on punctured disk) and identifying with the semiclassical partition function.

**Reused modules (spiral-hexagon):**
- `one_loop_determinant.py` — regularized partition function structure
- `gravity_partition.py` — `(c/12) × geometry` factor machinery
- `equivariant_rr.py` — equivariant Riemann–Roch with cones (the TZ anomaly coefficient)
- `conformal_block_zn.py` — Z_N twist dimensions `h_m = m(N−m)/2`

**New module:** `src/planetary_polygons/extensions/cft_liouville_action.py`
**Tests:** `N = 3, 5, 7, 11` numerical evaluation, check coefficient of `K_WP` equals `12 b(N)/6 = 2 b(N)`.

### Pipeline B — Spectral zeta / heat kernel

**Input:** heat kernel `e^{−t Δ_Σ}` on the conical punctured disk.

**Output:** `log det'(−Δ_Σ)` via Mellin transform of `Tr(e^{−tΔ_Σ}) − (asymptotics)`.

**Central charge extraction:** the Polyakov–Alvarez anomaly formula on a surface with conical singularities of angle `2πα_k` gives
```
log det'(−Δ_{e^{2φ}g}) − log det'(−Δ_g)
   = (c/12π) S_L[φ] + Σ_k (α_k + 1/α_k − 2) · R_k(φ)
```
(Kokotov–Korotkin / Klevtsov–Ma–Marinescu–Wiegmann for the hyperbolic case). With `α_k = 1/N` for all `k`, the conical correction per puncture is `(1/N + N − 2) · R_k`. Extract `c` from the coefficient of `S_L[φ]`.

**Reused modules (spiral-hexagon):**
- `spectral_machinery.py` — Selberg transform, trace formula
- `bolza_heat_kernel.py` — heat kernel `K_{H²}` with lattice sums, Havelock kernel `−log(2 sinh(d/2))`
- `spectral_zeta_verify.py` — analytic continuation of `Z_E(s)`
- `bolza_spectral.py` — `Z'_Γ(1)` machinery (reference case at `N=6` Bolza analog)

**New module:** `src/planetary_polygons/extensions/cft_spectral_zeta.py`
**Tests:** convergence of heat-kernel expansion truncated at order `t^0`; `c`-extraction for `N = 3, 5, 7, 11` matches `12 b(N)` to ≥ 4 digits.

### Pipeline C — Kirchhoff Hamiltonian = regularized Liouville action

**Input:** Kirchhoff Hamiltonian `H_N = Σ_{i<j} κᵢκⱼ G(zᵢ,zⱼ)` at the `N`-gon, with standard `log ε` self-energy subtraction.

**Output:** `H_N^{reg}` as a closed form in `N` (already known — this is the Gauss-product structure proved in `bernoulli_havelock.py`).

**Central charge extraction:** on physical grounds, the regularized Kirchhoff Hamiltonian at a vortex configuration equals `(c/12) × (WP area)` at the saddle. Verify
```
H_N^{reg}(N-gon) / (WP_area_at_N-gon) = b(N).
```

**Reused modules (spiral-hexagon):**
- `weyl_anomaly_cancellation.py` — three-layer decomposition `λ_m = C_1 − f(m,N) + δ_m` with δ_m = 0 theorem
- `zamolodchikov_finite_c.py` — Kac degenerate dimensions at finite `c`
- Local: `bernoulli_havelock.py` — Gauss product `Π 2 sin(πm/N) = N`

**New module:** `src/planetary_polygons/extensions/cft_kirchhoff_anomaly.py`
**Tests:** analytical equality `H_N^{reg} / WP_area = b(N)` for `N = 3, 5, 7, 11, 12`.

### Agreement test (the derivation itself)

**Orchestrator:** upgrade existing `cft_central_charge.py` to a three-way comparison.

For each `N ∈ {3, 5, 7, 11}`:
```
c_A = 12 · (A-pipeline coefficient of K_WP)
c_B = 12 · (B-pipeline anomaly coefficient)
c_C = 12 · (C-pipeline Kirchhoff-over-area)
assert c_A ≈ c_B ≈ c_C ≈ 12 b(N)   to > 4 digits
```

If the three agree and equal `12 b(N)`, the derivation is complete: `c` is defined by the anomaly (Pipeline B, first-principles CFT definition), reproduced by the classical saddle (Pipeline A, TZ), and identified with the physical Kirchhoff energy (Pipeline C).

## 4. Implementation order and scope

1. **Pipeline C** (~1 session). Reframes `bernoulli_havelock.py` content as an anomaly coefficient. Cheapest, fixes the physical bridge first.
2. **Pipeline A** (~2 sessions). Takhtajan–Zograf explicit formula on punctured disk with equal cone angles. Adapt `equivariant_rr.py` + `conformal_block_zn.py`.
3. **Pipeline B** (~2–3 sessions). Heat kernel on conical punctured `H²` via Selberg + method-of-images on the universal cover. Adapt `spectral_machinery.py` + `bolza_heat_kernel.py`.
4. **Orchestrator** (~0.5 session). Three-way agreement test + report.

**Total:** ~5–6 sessions if no route hits a wall. If any route hits an unreducible wall, document the wall concretely (which theorem is missing) per `feedback_first_principles_proofs.md`.

## 5. Paper integration

Once three-way agreement is numerically verified, rewrite Paper III §591–647 ("The central charge") to:
- Present Pipeline B as the **definition** (`c` is the Polyakov anomaly coefficient).
- Present Pipeline A as the **classical-saddle derivation** (Takhtajan–Zograf theorem cited).
- Present Pipeline C as the **physical identification** (Kirchhoff = regularized Liouville).
- Remove the "c is defined by the Havelock spectral data" framing — it was the reviewer's principal objection.

## 6. Out of scope

- Liouville/DOZZ identification (Route 2 from pickup memory) — deferred unless Pipeline A hits a wall.
- Selberg zeta on `H²/Γ_N` congruence quotient (Route 1) — deferred; the punctured disk is more direct for the `N`-gon.
- Gap B (Langer log-singular), Gap C (Galois 1071/4), Gap D (subsumed by A).

## 7. Cross-repo dependency

Reuse spiral-hexagon modules via `sys.path.insert(0, "/mnt/c/Users/gspea/source/repos/spiral-hexagon")`
at the top of each new module. Document the dependency in each file header. Do **not** copy code — stays DRY.

## 8. Test-driven discipline

Each pipeline module gets a test file first (per TDD skill and `feedback_first_principles_proofs.md`):
- Test asserts the predicted value (`12 b(N)`) for `N = 3, 5, 7, 11` before implementation.
- Implementation proceeds until tests pass.
- Paper text is updated only after tests pass.
