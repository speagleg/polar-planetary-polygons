# Session Transfer Manifest: 2026-03-21

**Purpose:** Catalog all work from the C_FB / twin prime / quantum Havelock
session for transfer to the main paper repository (planetary-polygons-unified).

## Summary of Results

### 1. C_FB Closed-Form Investigation
- **Hypothesis C_FB = -π⁴/512:** consistent but unresolvable at current precision
- **Character sum κ = 0.991674 ± 0.000001** (6 digits, Mellin integral)
- **Corrected L(1, f) = 0.849** (not 0.816; verified via LMFDB L(1/2) = 0.5828)
- **S_eff ≈ R(2)·R(5)·129/128** to 0.03% (at precision limit)
- **PSLQ:** no closed form found for κ in any tested basis

### 2. GPY Sieve with Hecke Weights
- **Anti-correlation:** 14,770/14,770 verified, zero violations
- **GPY ratio 1.92** for p ≡ 17 mod 40 (highest known for gap-2 in a natural class)
- **Hecke weight amplifies errors** (variance ratio 8.2×)
- **Anti-correlation as constraint:** 34% density boost, 9% lower BDH error
- **No Chebotarev advantage** beyond mod-8 congruence

### 3. Gap Analysis
- Character sums κ_g for gaps 2, 4, 6, 8, 10, 12
- Gap 8 bilateral correlator: 14,639 doubly-active pairs, sign bias 0.002
- Gap 2 remains highest GPY among "hard" gaps (1.91 vs 1.90 for gap 8)
- κ_g depends ONLY on g mod 5 (confirmed)

### 4. Chebyshev Bias
- Rubinstein-Sarnak parameter b = 0.003 (nearly zero — exceptionally fair race)
- No significant bias at 10⁸ for either unrestricted or twin-restricted race
- The sign of a_p is noise; the residue class is the signal

### 5. Palindromic Form Comparison
- Five forms compared: Bolza, Golden, D=7, Gaussian, Eisenstein
- Bolza wins for twins (GPY 1.918) but NOT optimal among all congruence classes
- p ≡ 11 mod 15 achieves GPY 3.84 (from Hardy-Littlewood local factors)

### 6. Quantum Havelock Eigenvalues
- **Four theorems** on f_q(m,N) at prime roots of unity q = e^{2πi/p}
- **Number field matching:** N=8↔k=7 (Q(cos(π/7))), N=10↔k=12 (Q(√3)), N=23↔k=5 (Q(√5))
- **Bolza anomaly:** N=11 at k=8 degenerates (D₄ obstructs scalar q-deformation)
- **Fusion identities:** (1+β)² = α(α-1) at k=7 generalises φ² = φ+1 at k=5
- **Galois sectors:** (p-1)/2 stability phases, most unstable carries fundamental unit
- **Composite discriminant obstruction:** Q(√6) projects to Q(√3)
- **Promotion breaks Galois:** σ₃ trivial, σ₅ sign-flips (stable ↔ unstable)

### 7. Torus / Entanglement Bridge
- **Havelock identity FAILS on the torus** for N ≥ 4 (C₁ is mode-dependent)
- **Palindromic symmetry δ_m = δ_{N-m} holds perfectly**
- **q-expansion correction verified** but only captures ~1% of delta_m
- **Galois sector test (N=23):** NO clustering — within-sector variance = 95% of total
- **Honest conclusion:** TQFT and entanglement corrections are independent

---

## Files Created

### Source Code: `src/spiral_hexagon/number_theory/`

| File | Lines | Purpose |
|------|-------|---------|
| `__init__.py` | 1 | Package init |
| `arithmetic.py` | ~130 | Legendre, Tonelli-Shanks, √2 mod p, α(p), a_p |
| `sieve.py` | ~20 | Sieve of Eratosthenes |
| `bolza_form.py` | ~100 | η(8z)η(16z) q-expansion, Hecke multiplicativity |
| `l_functions.py` | ~260 | Abel-smoothed L(s, f⊗χ), characters mod 5 |
| `singular_series.py` | ~50 | C₂, S_{40,17} = (10/3)C₂ |
| `level1_test.py` | ~160 | Level 1 test: C_FB = -π⁴/512? |
| `euler_product.py` | ~350 | L'/L via Euler product + Richardson |
| `mellin_lfunc.py` | ~330 | **Mellin integral** L-values (exponential convergence) |
| `gpy_hecke.py` | ~480 | GPY sieve with Hecke weighting |
| `gpy_constrained.py` | ~440 | GPY with anti-correlation constraint |
| `gap_analysis.py` | ~320 | All gaps 2-12: character sums, bilateral correlator |
| `chebyshev_bias.py` | ~280 | Silver ratio Chebyshev race + Rubinstein-Sarnak |
| `palindromic_comparison.py` | ~410 | Five palindromic forms comparison |
| `consecutive_correlation.py` | ~300 | C(x) = Σ a_p·a_{p'} + explicit formula |

**Total: ~3,630 lines of computation code**

### Tests: `tests/`

| File | Tests | Purpose |
|------|-------|---------|
| `test_arithmetic.py` | 22 | Legendre, Tonelli-Shanks, α(p), a_p |
| `test_bolza_form.py` | 15 | η product, Hecke multiplicativity, cross-checks |
| `test_l_functions.py` | 11 | Characters, L-values, convergence |
| `test_singular_series.py` | 5 | C₂, S_{40,17} |

**Total: 53 tests, all passing**

### Investigation Documents: `docs/investigations/`

| File | Sections | Purpose |
|------|----------|---------|
| `2026-03-21-cfb-computation-and-gpy.md` | 8 | **Main paper integration doc** |
| `2026-03-21-gpy-hecke-ratio.md` | 6 | GPY ratio 1.92 result |
| `2026-03-21-quantum-havelock.md` | 10 | Quantum eigenvalue number field matching |
| `2026-03-21-quantum-havelock-theorems.md` | 4 | Four theorems (formal statements) |
| `2026-03-21-session-transfer-manifest.md` | — | This file |

### Design/Planning (historical, not for transfer):

| File | Purpose |
|------|---------|
| `docs/superpowers/specs/2026-03-20-cfb-closed-form-computation-design.md` | Original design spec |
| `docs/superpowers/plans/2026-03-20-cfb-closed-form-pipeline.md` | 10-task implementation plan |

---

## Transfer Instructions

### To planetary-polygons-unified:

1. **Copy the number_theory package:**
   ```bash
   cp -r src/spiral_hexagon/number_theory/ \
     ../planetary-polygons-unified/src/planetary_polygons/extensions/number_theory/
   ```

2. **Copy the tests:**
   ```bash
   cp tests/test_arithmetic.py tests/test_bolza_form.py \
     tests/test_l_functions.py tests/test_singular_series.py \
     ../planetary-polygons-unified/tests/
   ```

3. **Copy the investigation docs:**
   ```bash
   cp docs/investigations/2026-03-21-*.md \
     ../planetary-polygons-unified/docs/investigations/
   ```

4. **Update imports:** Change `spiral_hexagon.number_theory` →
   `planetary_polygons.extensions.number_theory` throughout.

5. **Add dependency:** Ensure `mpmath>=1.3` is in the target pyproject.toml.

### Key values to update in the paper:

- **L(1, f) = 0.849** (was 0.816 — the Dirichlet series hadn't converged)
- **κ = 0.991674** (the character sum, 6 digits)
- **GPY ratio 1.92** for p ≡ 17 mod 40

### Computations that ran locally (no GPU):

| Computation | Runtime | Limit |
|------------|---------|-------|
| Sieve + α(p) to 10⁸ | 62s | 36,885 qualifying twins |
| Sieve to 10⁹ | 197s | 286,203 qualifying twins |
| Mellin L-values (all 4 chars) | ~60s | 15+ digit L(1), 5+ digit L'/L |
| GPY analysis | ~30s | 58,978 twin primes to 10⁷ |
| Chebyshev bias | ~120s | 665,000+ Hecke-active primes to 10⁸ |
| Consecutive correlation | ~120s | 5.7M primes to 10⁸ |
| All tests | 20s | 53 tests |

---

## Git History (this session, 17 commits)

```
0d9547b Four theorems on quantum Havelock eigenvalues
75bfdd3 N=8 at k=7: full algebraic eigenvalue structure
4f88e68 Quantum Havelock: three computations resolve open questions
7023f56 Quantum Havelock eigenvalues: number field matching + session catalog
d7dcb14 feat(number_theory): consecutive prime correlation
4270e20 feat(number_theory): Chebyshev bias analysis
838eabb feat(number_theory): palindromic form comparison
f4b6d81 feat(number_theory): complete prime gap analysis
fd2fc0e Comprehensive investigation: C_FB computation and GPY
eb3fa58 RESULT: GPY ratio 1.92 for twin primes via Bolza form
198d61f feat(number_theory): constrained GPY analysis
2f7fca6 feat(number_theory): GPY sieve with Hecke weighting
42498a8 feat(number_theory): Mellin integral L-values
5c69ff8 feat(number_theory): Euler product L'/L
39a9b22 feat(number_theory): L-functions + Level 1 test
23d6b23 feat(number_theory): arithmetic + sieve + Bolza form
bda5ab7 Add design spec for C_FB pipeline
```
