# Session 4 Pickup — 2026-04-01

## What this session accomplished

### Physics fixes (3)
- **Einstein circularity**: Remark at line 753 — Regge identification = single finite-dimensional optimization, not iteration between metric and vortex configuration
- **WDW CL coefficient**: Gaussian truncation loses exact mode-by-mode factorisation; b(N) uniqueness from mode-independent offset in eigenvalue formula
- **Lashkari domain**: 3D matter coupling lifts to 4D by same KK reduction as Step B

### Full 4D Riemann theorem (Paper III, Theorem thm:full-riemann)
- Replaces disclaimer "beyond the scope of this paper" with three-layer proof
- Layer 1: Explicit R^(3)_{ijkl} = (Λ₃/2)(gg−gg) via O'Neill/Besse submersion formula
- Layer 2: Lichnerowicz-Havelock + gapped perturbations (radion m²=N²/4, graviphoton gap ≥1)
- Layer 3: FG reconstruction exact for d_boundary=2, KK lift gives unique 4D metric
- Code: weyl_tensor.py (23 tests, all passing)
- Sign convention resolved: work at 3D Riemannian level, cite O'Neill for submersion

### Paper I error corrected
- Theorem 3.2(b) claimed constrained threshold N≤10 — double-count of Lagrange shift
- The Havelock eigenvalue (N−1)−m(N−m)/2 IS the constrained eigenvalue (σ_m + shift)
- Removed part (b); threshold is N≤7 (consistent with Paper II)

### QFT fixes (2)
- **Weinberg angle**: Formula rewritten as g²C₂ ratio (gauge coupling × Casimir), not conformal weight h_R. The denominator (k+h∨) enters through the gauge coupling (CS-level property), the numerator C₂=j(j+1) enters through the Casimir (representation property). Integrable bound constrains TQFT states, not matter coupling.
- **Cosmological constant**: Coleman false-vacuum citation removed. Physical mechanism is WDW tunneling (WKB suppression between turning points), not Coleman's decay rate.

### Technical fixes (7)
- Paper V one-loop: scattering-theory → spectral zeta for discrete spectra
- Paper IV CKM: "(amplitude, not probability)" → standard S=e^{2iδ}
- Paper V N=11: elimination table distinguishes mathematical vs structural constraints
- Paper II multi-ring: N=3,4 cases computed and added (all unstable), count 12→15
- Paper III Hadamard: Seeley-DeWitt a₁=R/6 cited
- Paper IV H²×R: "no compact fiber" → "Euler class e=0"
- Supplement Pell: explicit residue calculation added

### Redundancy elimination (−87 lines)
- Boilerplate endings: identical 6-line blocks in 5 papers → 3-line with repo URL
- Paper II: 85-line re-proof of constrained minimum → 25-line Proposition citing Paper I
- "1 >> 0.61" → "1 > 0.61"

### Writing fixes (from earlier in session)
- Paper VI master table legend
- Paper IV Z/3Z redundancy trimmed
- Paper II K₀ paragraph headers
- Paper III palindromic headers promoted

---

## Reviewer panel scores

### Round 1 (pre-fixes)
| Reviewer | Score |
|----------|-------|
| Mathematician | 8.25 |
| GR specialist | 6.85 |
| QFT physicist | 4.00 |
| Skeptic | 4.00 |
| **Average** | **5.78** |

### Round 2 (post-fixes)
| Reviewer | Score |
|----------|-------|
| Mathematician | 7.15 |
| GR specialist | 7.90 |
| QFT physicist | 3.75 |
| Skeptic | 4.00 |
| Tech writer | 5.50 |
| **Average** | **5.66** |

GR specialist improved +1.05 (Riemann theorem). QFT and Skeptic unchanged (structural objections). Mathematician stricter but found fewer new issues.

---

## Current state
- **Branch:** `feature/algebraic-extensions`
- **Tests:** 1667 passing
- **Commits this session:** 6
- **Total lines:** ~12,720 (main papers) + 579 (supplement)

## Line counts
```
paper-1-mathematics:  2,839
paper-2-physics:      1,979
paper-3-gravity:      3,007
paper-4-field-theory: 2,313
paper-5-cosmology:    1,150
paper-6-discussion:     471
supplement-proofs:      579
```

---

## Remaining work (next session)

### Technical writer items
- **Notation collision on `c`**: central charge vs geodesic trace vs curvature constant in Paper I. Rename geodesic trace to τ or tr.
- **Paper III 230-line proof block** (lines 619-848): should split into separately numbered lemmas
- **Paper IV Section 12 (550 lines)**: fermion masses need 3+ subsections reflecting the three-tier structure (exact/one-parameter/non-perturbative)
- **Paper III intro** (lines 40-98): reads as table of contents, should state the argument
- **"typical parameter values"** (Paper III line 2340): specify the range

### Mathematician items
- **Hadamard 1/6 → 1/4 angular averaging**: Seeley-DeWitt a₁=R/6 cited but the conversion to R/4 via polygon-ring averaging not derived (~5 lines)
- **YM₂ + time → YM₃₊₁** (Paper IV Step B5): breathing mode as time direction is assertion, not derivation
- **Parity breaking → mass gap** (Paper IV): different CS levels don't automatically gap a gauge field

### Structural (philosophical, not fixable by editing)
- Vortex-gravity isomorphism (QFT −1.5, Skeptic −1.5)
- DHVW at irrational c (QFT −0.75, Skeptic −1.0)
- Frobenius as gauge-group selector (Skeptic −1.0)
- KK flux additivity for N=11 (QFT −0.75, Skeptic −0.5)
- Cosmological energy budget labeling (Skeptic −0.5)
- Dark matter unfalsifiable (Skeptic −0.25)

### Deferred
- Figures (every reviewer flagged zero figures)
- Merge/PR decision

## Protocol
- Language edits: present options to Gordon, get approval before editing
- Structural edits: can proceed directly
- Physics arguments: discuss before implementing

## Key commits
```
cf019d6 Physics fixes, writing cleanup, and full 4D Riemann theorem
87be390 Fix constrained threshold error (N≤10→N≤7) and one-loop proof
6bcc538 Close remaining technical issues from reviewer panel
93a2c8d Address QFT reviewer's two key objections
b3cb4af Eliminate redundancy: boilerplate, duplicate proof, precision fix
```
