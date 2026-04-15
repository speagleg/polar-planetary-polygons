# Paper I — Structural Rigor Rewrites (Pickup Spec)

## Status — COMPLETE (2026-04-15)

All Paper I structural rewrites and applicable minor fixes are done.
Canonical file: `latex/paper-1-mathematics/main.tex`.

| Item | Status | Score |
|------|--------|-------|
| #1 Constrained-min derivation | DONE | 9.3/10 |
| #6 C₁(S²) bugfix + Pell unification | DONE | 9.2/10 |
| #2 Riemannian Havelock universality | DONE (already in canonical) | — |
| #4, #5, #3 | Paper II scope | — |
| Minor #2 (curvature dichotomy) | DONE | — |
| Minor #5 (duplicate Verification) | DONE | — |
| Minor #1 (Morse index) | Already correct in canonical | — |
| Minor #3, #4, #6, #7 | Paper II scope | — |

Items #3, #4, #5 (prop:center-ring, cor:inertia-N7, prop:inertia) and
minor fixes #3, #4, #6, #7 (Onsager, WKB, inertia threshold, quartic)
belong to Paper II and will be addressed in a separate spec.

Workflow template: `docs/rigor-sandbox/WORKFLOW_TEMPLATE.md`
4447 tests pass. All series papers updated.

---

## Original spec (for reference)

## Working files

- `latex/paper/main.tex` — main paper (5,200 lines)
- `latex/paper-A-appendices/main.tex` — appendix (440 lines, mostly C₁ derivations)
- `latex/supplement-proofs/main.tex` — supplement (1,500 lines, Morse-Bott + extras)
- `tests/` — all numerical claims have backing tests

## Reference baseline

- **Last fresh review score**: 7.6/10 (8th pass)
- **Best score achieved**: 8.6/10 (4th pass)
- **Target**: 9.5+/10 (Annals standard)
- **Total addressable deductions remaining**: ~2.4 across 6 structural items

---

## Structural Rewrite #1: Theorem `thm:constrained-min` — full Lagrangian eigenvalue derivation

**Current state**: Paper cites Havelock 1931 for λ_m^± = (N-1) − m(N-m)/2, m(N-m)/2 + numerical verification. Reviewers consistently flag this as "key step omitted".

**What's missing**: A self-contained algebraic derivation of the radial-radial and tangential-tangential block eigenvalues at each Z_N Fourier mode m.

**Difficulty**: Multi-page algebra. I tried 3 times and made errors each time. Needs careful, slow, page-by-page derivation.

**Plan**:
1. Set up the 2×2 block at mode m in (radial, tangential) basis with explicit Fourier amplitudes
2. Compute d²H/dr_j dr_k (radial-radial pair Hessian) explicitly:
   - Use z_k = e^{iθ_k}, perturbation z_k → (1 + a cos(2πmk/N))e^{iθ_k}
   - Expand |z_j(a) − z_k(a)|² to second order in a
   - Take −(1/2) d²/da² log of this
3. Sum over pairs using Fourier orthogonality:
   - Σ_k cos(2πmk/N)cos(2πm'k/N) = (N/2)δ_{m,m'} for m,m' ∈ {1,...,N-1}, m ≠ N/2
   - Reduces to Havelock identity T_m = m(N-m)/2 (Lemma already proved)
4. Apply Lagrange shift −2μ_L = (N-1)/2
5. Convert from amplitude to unit-eigenvector normalization
6. Verify trace identity λ^+ + λ^- = N-1 from the derivation (not as a separate claim)

**Key correctness checks** (numerically verified, must match):
- For N=5, m=2: λ^+ = 1, λ^- = 3
- For N=7, m=3: λ^+ = 0, λ^- = 6
- For N=11, m=5: λ^+ = -5, λ^- = 15

**Files to produce**:
- A clean ~3-page derivation in §6.2 of paper/main.tex
- Add to `tests/test_angular_hessian.py` if not there: assertion that paper formulas match diagonalization

**Estimated effort**: 1-2 focused days. Verify each step numerically before writing.

---

## Structural Rewrite #2: Riemannian Havelock universality (`λ_m^- = m(N-m)/2` on curved surfaces)

**Current state**: Trace identity proven (λ^+ + λ^- = mode-independent constant), individual eigenvalues cited from Boatto-Cabral 2003. Reviewer: "the actual claim λ_m^- = m(N-m)/2 requires more — specifically, either anti-symmetry of the radial-tangential difference or an additional algebraic step — which is then attributed to BC: 'We cite this result rather than rederive it.'"

**What's missing**: An explicit algebraic argument that on constant-curvature surfaces, the tangential block eigenvalue is exactly m(N-m)/2 (not just that the trace is constant).

**Difficulty**: Medium-hard. Requires direct computation of the second variation under a tangential perturbation on H² and S² separately, using geodesic distances.

**Plan**:
1. **Tangential perturbation on S²**: at colatitude φ₀, perturb angles θ_k → θ_k + b cos(2πmk/N)
2. Compute geodesic distance second variation: cos(d_jk) = cos²φ₀ + sin²φ₀ cos(θ_j − θ_k)
3. Expand to O(b²), apply Z_N Fourier orthogonality
4. Show coefficient at mode m is exactly m(N-m)/2 × (universal factor) + φ₀-dependent C_1
5. Repeat for H² with cosh replacing cos
6. **Key insight**: the m-dependence factors out because the angular variable enters through the SO(2) symmetry of the ring's azimuthal angle, which has the same Z_N representation on any rotationally-symmetric surface

**Verification**:
- Numerical: tests/test_curved_surfaces.py already verifies for N ∈ {3,...,12} at colatitudes (15°, 30°, ..., 75°)

**Files to produce**:
- ~2-page derivation in §3.2 of paper/main.tex (Riemannian Havelock section)
- Possibly extract S² and H² cases as separate lemmas

**Estimated effort**: 2-3 days.

---

## Structural Rewrite #3: Proposition `prop:center-ring` Case 1 — uniform proof for all (N, M) with N ≥ 8

**Current state**: Numerical computation for (N, M) ∈ {8,...,50} × {2,...,99}. Statement restricted to {8,...,20} × {2,...,20}. Open problem acknowledged: "uniform analytical closure for all (N, M) is an open problem."

**What's missing**: An analytical proof that for N ≥ 8 and any M ≥ 2, the two-ring Lagrangian Hessian has a negative eigenvalue.

**Difficulty**: Hard. May genuinely require novel mathematical work.

**Plan options** (in order of likelihood of success):

**Option A: Eigenvector localization argument**
1. Show the critical negative eigenvector at λ=0 (no inner-outer coupling) is localized on the outer ring at mode m = ⌊N/2⌋
2. Use perturbation theory to show coupling to inner-ring modes is suppressed by gcd(N, M) constraints
3. Show the "bad case" (where coupling could push the eigenvalue positive) requires gcd(N, 2M) | NM in a specific way that excludes generic (N, M)

**Option B: Variational argument**
1. Construct an explicit trial vector that gives negative quadratic form for all (N, M) with N ≥ 8
2. Use min-max principle to conclude λ_min < 0

**Option C: Concede and reframe**
1. Accept that a fully uniform proof is genuinely open
2. State the proposition more carefully: rigorous for finite range, conjecture for general (N, M)
3. Move to "Open Problem" section with explicit conjecture

**Verification**:
- Existing: 4,312 cases checked numerically
- For Option A/B: would need additional tests for the analytical bounds

**Files to produce**:
- New §6.x analytical argument in paper/main.tex
- Possibly a new Lemma about the Z_N × Z_M cross-coupling structure
- If Option C: clean honest statement + open-problem callout

**Estimated effort**: 3-7 days (could be much longer if Option A/B pursued and fails).

---

## Structural Rewrite #4: Corollary `cor:inertia-N7` — true computer-assisted proof

**Current state**: Lipschitz constant L ≤ 202 + grid evaluation min_i λ(ε_i) ≥ 0.36 + Lipschitz-bound interpolation. Reviewers correctly flag: "no validated interval arithmetic" and "the certificate is not exhibited in the paper."

**What's missing**: Either (a) validated interval arithmetic with explicit bounds on rounding errors, or (b) a Kantorovich-style a priori spectral bound.

**Difficulty**: Medium. Standard computer-assisted proof techniques apply.

**Plan**:
1. **Implement validated interval arithmetic** in `tests/test_blob_correction.py`:
   - Use `mpmath` with explicit interval bounds on each operation
   - Track rounding error through the entire eigenvalue computation
   - Output: a certified interval [λ_min^lower, λ_min^upper] for each grid point
2. **Verify**: λ_min^lower − L·Δε > 0 on every subinterval
3. **Provide**: a separate "certificate file" listing the interval bounds
4. **In paper**: either inline the certificate (if compact) or reference it precisely with hash + reproducible script

**Alternative**: Use a Kantorovich-Newton method to prove the eigenvalue is bounded away from zero on all of Region 2 with a priori bounds — but this is harder.

**Files to produce**:
- Updated `tests/test_blob_correction.py` with validated interval arithmetic
- Certificate file (e.g., `docs/certificates/cor_inertia_N7_certificate.json`)
- Updated text in paper/main.tex referencing the certificate by hash

**Estimated effort**: 2-3 days.

---

## Structural Rewrite #5: Proposition `prop:inertia` — clean infinite-dimensional inertia argument

**Current state**: Mixed-norm (L² on center, $\dot H^{-1}$ on shape) Schur complement. Reviewer: "inertia is preserved by congruence; the congruence transformation between these two different metric spaces should be explicitly stated."

**What's missing**: Clear statement of which inertia is preserved and how the cross-norm Schur reduction respects it.

**Difficulty**: Medium. Functional-analytic care required.

**Plan**:
1. **Choose a single inner product** for the entire problem (e.g., L² on the full perturbation space, with appropriate weight to handle the H^{-1} divergence at small scales)
2. **Show the H_ss block is bounded below in this norm** with explicit constant (using Sobolev embedding or other standard inequality with cited constant)
3. **Apply standard finite-dimensional Schur complement** after spectral truncation, with explicit bounds on truncation error
4. **Take limit**: show the inertia is independent of the truncation scale

**Alternative cleaner approach**: 
- Reformulate the perturbation space as a Hilbert space with the energy inner product
- In this inner product, H_ss is exactly the identity (by construction of the energy norm)
- Standard Schur complement applies
- Convert back to physical L² norms only at the end

**Verification**: 
- Already verified numerically for the prescribed-blob case
- For general patches, need additional numerical tests

**Files to produce**:
- Rewritten §10 of paper/main.tex with single-norm formulation
- Possibly extract the analytic preliminaries as a separate appendix

**Estimated effort**: 2-3 days.

---

## Structural Rewrite #6: Appendix C₁(S²) derivation

**Current state**: Appendix derives the Euclidean stereographic formula C_1^eucl = (N-1)(1+ξ²)/(1+ξ)², then cites Boatto-Cabral 2003 for the geodesic-metric formula C_1(S²) = (N-1)(1-ξ)/(1+ξ). Reviewer: "the boxed C_1(S²) formula — on which the entire §4.2 table of exact rational thresholds depends — is not actually derived in the paper."

**What's missing**: A self-contained derivation of the geodesic-metric C_1(S², ξ) formula, OR a clean argument showing the Euclidean-frame formula and the geodesic-frame formula give the SAME stability conclusions (so the table thresholds are valid).

**Difficulty**: Medium. The Boatto-Cabral derivation is in their paper; we need to either reproduce it or argue equivalence.

**Plan options**:

**Option A: Reproduce BC2003 derivation**
1. Set up the geodesic Green's function on S² in stereographic coordinates: 
   h_S²(z_j, z_k) = -log|z_j - z_k| + (1/2)log[(1+|z_j|²)(1+|z_k|²)] - log 2
2. Compute the constrained Hessian at the polygon equilibrium
3. The single-site correction (1/2)log(1+|z_k|²) modifies the Lagrange multiplier and the radial Hessian
4. Reduce to (N-1)(1-ξ)/(1+ξ) via direct algebra
5. ~2-3 pages of careful work

**Option B: Argue equivalence**
1. Show that for the stability question (is min eigenvalue ≥ 0 or < 0?), both formulas give identical conclusions on the same parameter range
2. Formula difference is a global rescaling that doesn't change sign of eigenvalues
3. Therefore the §4.2 table of rational thresholds is valid

**Verification**:
- tests/test_curved_surfaces.py already verifies the geodesic-metric formula numerically to 10⁻¹⁴ for N ∈ {3,...,12}
- Numerical evidence is overwhelming; the issue is purely about derivation cleanliness

**Files to produce**:
- Replace appendix derivation with Option A or Option B (ideally A for completeness)
- Possibly extract as separate appendix section

**Estimated effort**: 2-3 days for Option A; 1 day for Option B.

---

## Minor Issues to Fix Along the Way

These are smaller items that should be addressed during the structural rewrites:

1. **Morse index dimension counting** (§5, lines ~1695-1717): Specify real vs complex dimension explicitly. Each unstable Fourier mode m gives a 2-real-dim eigenspace; palindromic pair (m, N-m) doubles it for m ≠ N/2.

2. **Curvature dichotomy quantifiers** (§5, lines 1664-1684): Specify ξ ∈ (0, ξ*(N)) range; clarify that "any nonzero radius" excludes the equator on S².

3. **Onsager hypothesis bundling** (§9, prop:onsager-n-select): Separate the r > 1/2 case from r = 1/2 case to avoid mixing strict/non-strict inequalities.

4. **WKB branch disconnection** (lines 4498-4513): Either tighten the structural-stability claim or remove the "WKB" framing — currently it's an obvious continuity argument dressed up.

5. **Duplicate "Verification" paragraphs** in Thm 6.2: Editorial pass to remove duplication.

6. **Inertia preservation threshold in proposition statement** (§10, prop:inertia): Move the explicit ε₀(N) threshold from proof into proposition statement.

7. **N=7 quartic 153/7 derivation** (§7): The explicit symbolic reduction is in `scripts/n7_quartic_proof.py` (fully working, all 21 pairs reduce in Q(ω)). Consider inlining the most essential steps in the paper as a proof sketch (currently delegated to script).

---

## Suggested Order of Attack

1. **Start with #1** (constrained-min derivation): foundational, unblocks others, well-defined scope
2. **Then #6** (C₁(S²)): fixes the appendix issue cascading to the threshold table
3. **Then #4** (computer-assisted proof for cor:inertia-N7): standard technique, likely solvable
4. **Then #5** (prop:inertia clean formulation): builds on #4 understanding
5. **Then #2** (Riemannian λ_m^- universality): nicer to do after #1 establishes the flat-plane derivation pattern
6. **Last #3** (uniform two-ring): hardest, may be genuinely open; fall back to "Option C: concede" if needed

After each structural rewrite: dispatch a focused fresh-eyes mathematics reviewer on JUST that proof+statement (not the whole paper). Iterate the rewrite until that focused review gives 9.5+/10. Then move to the next item.

## Expected Score Trajectory

- Current: ~8.0
- After #1, #6: ~8.5
- After #1, #6, #4: ~8.8
- After #1, #6, #4, #5: ~9.0
- After all 6: ~9.5+

## Reproducibility

All numerical results have backing tests in `tests/`. Before each rewrite session:
```bash
cd /mnt/c/Users/gspea/source/repos/planetary-polygons-unified
python3 -m pytest tests/ -v
```

Should pass cleanly. If any test fails, fix that first before working on the proof — it likely indicates a real mathematical issue.

## Key Constraints During Rewrites

- **No retreat language**: Every claim must either be proved or explicitly stated as open
- **No hand-waving**: "Standard result" requires precise citation; "by symmetry" requires the symmetry to be explicit
- **Numerical verification ≠ proof**: Code agreement is necessary but not sufficient
- **Honest scoping**: If a claim only holds for restricted range, state that range in the proposition statement (not buried in proof)
- **Cite Havelock 1931 / Boatto-Cabral 2003 freely** for classical results — they're proved, just elsewhere
