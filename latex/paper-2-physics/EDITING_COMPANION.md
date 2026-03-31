# Paper II Editing Companion -- Content Index & Assessment

**Paper**: "Why Rotating Fluids Make Polygons -- Paper II: Classical and Quantum Physics"
**File**: `latex/paper-2-physics/main.tex`
**Total lines**: 2380
**Sections**: 10 (including subsections)

---

## Summary

Paper II is the physics core. Proves the N-gon is a constrained energy minimum for N <= 7, resolves N=7 with exact quartic, extends through five bridges (central vortex, multi-ring, blob, Rossby, deformation radius), then applies to BEC and 2+1D gravity.

**Strengths:** Argument arc is clear. Builds from simplest case through increasing complexity. Theorem statements precise. Central-vortex/multi-ring dichotomy is a clean narrative unit.

**Main concern:** Front-loaded with tight material (Secs 1-7) but becomes discursive in Secs 8-10. Section 10 (2+1D gravity) is arguably Paper III material. Remarks on quantum Hall, TQFT, orbifold-Havelock belong elsewhere.

---

## SECTION-BY-SECTION INDEX

### Abstract (lines 15--28) -- CORE
Clean and accurate.

### Section 1: Introduction (lines 30--37) -- CORE
Two paragraphs. Lines 33 (53 words) and 36 (56 words) both too long.

### Section 2: Point vortex dynamics (lines 42--112)

| Lines | Content | Assessment | Notes |
|-------|---------|------------|-------|
| 45--69 | QGPV, Thomson energy, conserved quantities | CORE | |
| 71--112 | Centered spiral deformation + Mobius | CORE/SUPPLEMENTAL | 27 lines of Mobius material flagged as "not entering proofs" |

Label `sec:results` on line 72 is misleading for spiral deformation subsection.

### Section 3: Constrained energy landscape (lines 115--293) -- CORE
The strongest section.

| Lines | Content | Assessment | Notes |
|-------|---------|------------|-------|
| 118--145 | Theorem 3.1: H''(0) < 0 along spiral | CORE | |
| 157--250 | Theorem 3.2: N-gon minimizes H on constraint surface iff N<=7 | CORE | Central result |
| 252--293 | Corollary 3.1: constrained min vs unconstrained saddle | CORE | Lines 262--266 slightly redundant with statement |

### Section 4: Central vortex stabilization (lines 297--417)

| Lines | Content | Assessment | Notes |
|-------|---------|------------|-------|
| 305--378 | Lagrange shift + Prop 4.1 + kappa_crit table | CORE | |
| 385--413 | N=6 worked example | SUPPLEMENTAL | 29 lines, could be 15 |

### Section 5: N=7 bifurcation (lines 420--563)

| Lines | Content | Assessment | Notes |
|-------|---------|------------|-------|
| 424--563 | Landau normal form, quartic, alpha_0=45/14 | CORE | |
| 460--485 | Galois rationality argument | REDUNDANT | Stated 3 times (lines 460, 471, 481) |
| 520--532 | Richardson extrapolation | SUPPLEMENTAL | 12-line parenthetical, move to remark |

### Section 6: Multi-ring (lines 568--719) -- CORE
Well-structured. 12-case table is effective.

### Section 7: Blob bridge (lines 729--1222)

| Lines | Content | Assessment | Notes |
|-------|---------|------------|-------|
| 740--883 | Blob regularization, Prop 7.1, corrections table | CORE | |
| 885--1077 | Full infinite-dim convergence, Prop 7.2 | CORE | |
| 1078--1222 | Rossby bridge | CORE | |
| 1135--1215 | Cat's-eye Remark | SUPPLEMENTAL | 80 lines, very long for a remark |

**Issues:** Line 1199 incomplete sentence (trails off with comma). Line 1193 stray comma on own line.

### Section 8: Deformation radius (lines 1225--1531) -- CORE
Solid. Line 1493 missing sentence subject.

### Section 9: Circulation disorder (lines 1537--1708) -- CORE
Line 1651 refs "Paper V" which doesn't exist.

### Section 10: BEC predictions (lines 1712--2037)

| Lines | Content | Assessment | Notes |
|-------|---------|------------|-------|
| 1718--1842 | BEC predictions, hard-wall disk, palindromic thresholds | CORE | |
| 1860--1907 | Healing length, hyperbolic lattices | SUPPLEMENTAL | |
| 1909--1997 | Remarks on mesoscopic disks, Laughlin, non-abelian | SUPPLEMENTAL | |
| 1999--2037 | Remark 9.4: TQFT independence | RELOCATE | Belongs in Paper III/IV |

### Section 11: Gravitational polygon stability (lines 2040--2375)

| Lines | Content | Assessment | Notes |
|-------|---------|------------|-------|
| 2070--2232 | Props 11.1-11.2 (grav stability, conformal invariance) | CORE | Belong here |
| 2251--2304 | Prop 11.3 (max stable polygon) | CORE | |
| 2307--2375 | Three-layer decomposition, orbifold-Havelock, WDW | RELOCATE | Paper III material |

**Note:** Introduction (line 34) says paper "does not assume gravitational interpretation" but Section 11 is entirely gravitational.

---

## REDUNDANCY MAP

| ID | Content | Appearances | Recommendation |
|----|---------|-------------|----------------|
| R1 | Galois rationality of quartic | Lines 460, 471, 481 (3x) | Keep 460, cut 471 and 481 |
| R2 | H_rt vanishing by anti-symmetry | Lines 194--199, 319--331 | Back-reference at 319 |
| R3 | Profile independence of blob | Lines 787--801, 855--864 | One-sentence ref at 855 |

---

## CROSS-REFERENCE PROBLEMS

### Critical

| Line | Reference | Problem |
|------|-----------|---------|
| 1035 | `\ref{prop:blob-stability}` | **Label never defined.** Should be `prop:blob` or `prop:inertia` |
| 1651 | "Paper~V, S3" | **Paper V doesn't exist** |
| 6 | `\externaldocument[A-]{../paper-A-appendices/main}` | **Paper A doesn't exist** |

### Formatting errors

| Line | Problem |
|------|---------|
| 1193--1194 | Stray comma on its own line |
| 1197--1199 | Incomplete sentence (trails off with comma) |
| 1493--1494 | Missing sentence subject |

### Fragile text references (should be \ref labels)
12 instances of "Paper I, Proposition X.Y" in plain text at lines: 104, 111, 137, 204, 216, 426, 735, 1231, 1907, 1952, 2239, 2273.

### Duplicate/orphan labels
- Lines 38, 725: Orphan `\label{part:pvd}`, `\label{part:extensions}`
- Multiple sections have two labels (e.g., `sec:n7-bifurcation` + `sec:n7`)

---

## SENTENCE LENGTH VIOLATIONS (>40 words)

| Line | ~Words | Severity |
|------|--------|----------|
| 33 | 53 | REWRITE |
| 36 | 56 | REWRITE |
| 85--94 | 72 | REWRITE |
| 95--102 | 62 | REWRITE |
| 257--266 | 64 | IMPROVE |
| 520--532 | 72 | IMPROVE (parenthetical) |
| 534--544 | 57 | IMPROVE |
| 689--703 | 68 | IMPROVE |
| 959--978 | 80+ | REWRITE (Prop statement is single sentence) |
| 1267--1277 | 56 | IMPROVE |

---

## NOTATION ISSUES

| Symbol | Meanings | Severity |
|--------|----------|----------|
| eta | R/R_d (deformation), eta_k (disorder), Stuart vortex concentration | Medium -- different sections |
| epsilon | Blob width, N=7 perturbation amplitude, observed amplitude, healing/R | Medium |
| sigma | Deformation parameter, jet width sigma, disorder sigma_eta | Medium (line 1090 vs 1544) |
| m | Fourier mode, point mass (sec 11), filling denominator (Laughlin) | Low |

---

## RECOMMENDED ACTIONS (by priority)

### Must fix
1. **Line 1035**: Undefined reference `prop:blob-stability`
2. **Line 1651**: "Paper V" doesn't exist
3. **Line 6**: Dead `\externaldocument` for Paper A
4. **Lines 1193--1194**: Stray comma
5. **Lines 1197--1199**: Incomplete sentence
6. **Lines 1493--1494**: Missing sentence subject

### Should fix
7. **Galois rationality 3x** (lines 460--485): Consolidate to one statement
8. **H_rt proof repeated** (lines 319--331): Back-reference instead
9. **Mobius material** (lines 85--111): Condense 27 lines to one paragraph
10. **Section 11.2** (lines 2307--2375): Move to Paper III
11. **Remark 9.4** (lines 1999--2037): Move to Paper III/IV
12. **Label sec:results** (line 72): Rename to sec:spiral
13. **Convert 12 plain-text Paper I references** to \ref labels
14. **Line 1067**: Replace \textsc with \textit

### Consider
15. Split 10 worst long sentences (50+ words)
16. Cat's-eye Remark (1135--1215): Shorten from 80 lines or make subsection
17. Clean up duplicate labels
18. Remove orphan \label{part:...} tags
19. Add notation table in introduction
20. Amend introduction claim about "no gravitational interpretation" (contradicted by sec 11)
21. Richardson extrapolation (520--532): Move to footnote/remark
22. N=6 worked example (385--413): Shorten from 29 to ~15 lines
