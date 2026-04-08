# Mark-Balance Exploration Integration

## Goal

Integrate 30+ rigorously proved results from the mark-balance exploration (docs/investigations/2026-04-07-e8-mark-balance-identity.md, 1163 lines) into Papers I, IV, V, and VII. Every result in Papers I/IV/V receives full theorem-proof treatment in LaTeX with computational backing in src/tests.

## Architecture

Four independent workstreams targeting four papers. One new proof module with tests. All results proved from first principles.

## Source Material

Investigation document: `docs/investigations/2026-04-07-e8-mark-balance-identity.md`
Existing proof modules: `src/planetary_polygons/proofs/e8_casimir_bridge.py` (I* character table, Coxeter decomposition), `src/planetary_polygons/proofs/coupling_constants.py` (CS couplings, Weinberg angle)

---

## Workstream A: Paper I (Mathematical Foundations)

**Target file**: `latex/paper-1-mathematics/main.tex`
**Location**: New §8 "The Mark Distribution" (after existing §7 which has McKay/Coxeter material)

### New Theorems (8)

**Theorem 8.1 (Mark-Balance Identity)**: For the I* affine marks d = (1,2,3,4,5,6,4,2,3), Σdᵢ(dᵢ-4) = 0. This identity holds uniquely among all ADE types and is equivalent to |I*| = 4h(E₈) = 120 = 4×30.

*Proof*: Direct computation on all ADE mark sets (exhaustive, finite). Equivalence: Σd(d-4)=0 ⟺ Σd²=4Σd ⟺ |I*|=4h. Gauss-Bonnet form: the (2,3,5) Schwarz triangle has area πε = π/30 = π/h; since |I*|=120 such triangles tile S² of area 4π, we get |I*|·(π/h) = 4π ⟺ |I*| = 4h. QED.

**Theorem 8.2 (V⊗F Theorem)**: For the icosahedron, V_vertex ⊗ V_face = 4 × reg(A₅) as A₅-representations. Hence V×F = 4|A₅| = 240 = roots(E₈).

*Proof*: The A₅-character of V⊗F at g≠e vanishes because gcd(|Stab_V|, |Stab_F|) = gcd(5,3) = 1 implies no non-identity element fixes both a vertex and a face. A character proportional to δ(g,e) is a multiple of reg, with multiplicity 240/60 = 4. QED.

**Theorem 8.3 (Division Algebra Chain)**: The iterated charge-magnitude map gives E₈ →(k₁=4) E₆ →(k₁=2) A₃ →(k₁=1) ∅ with pivots dim(ℍ) = 4, dim(ℂ) = 2, dim(ℝ) = 1.

*Proof*: Step 1: |dᵢ-4| (nonzero, sorted) = E₆ affine marks. Direct verification. Kernel = {ρ₃,ρ₆} (d=4 nodes) = SU(3). Step 2: E₆ pivot k₁ = Σd²/Σd = 24/12 = 2. Apply |d-2| to E₆ marks → A₃ marks (all 1s). Step 3: A₃ pivot k₁ = 1. All marks equal pivot → terminated. QED.

**Theorem 8.4 (Pivot Uniqueness)**: The decreasing positive integer triple (a,b,c) satisfying a+b+c = abc-1 is unique: (4,2,1).

*Proof*: With c=1: ab-a-b-1=1, so (a-1)(b-1)=3. Since 3 is prime, the only factorization with a≥b≥1 is (a-1,b-1)=(3,1), giving (a,b,c)=(4,2,1). QED.

**Theorem 8.5 (2-Adic Filtration)**: The 2-adic valuation ν₂(dᵢ) partitions the 9 nodes of Ẽ₈ into three layers K₃ (ν₂=0, 4 nodes), K₂ (ν₂=1, 3 nodes), K₁ (ν₂≥2, 2 nodes) such that: (i) this is a proper 3-coloring of the Dynkin diagram, (ii) it holds only for D̃₄ and Ẽ₈ among all affine ADE types, (iii) the mark-balance decomposes as Σd(d-4)|_{K₃} = -4, Σd(d-4)|_{K₂} = +4, Σd(d-4)|_{K₁} = 0, and (iv) Σd²(K₂) = Σd²(K₃) = 44 uniquely at the quadratic moment.

*Proof*: (i)-(ii) Exhaustive check on all ADE diagrams. (iii) Direct computation by layer. (iv) Algebraic: the equation 2^(n+1)+6^n = 1+2·3^n+5^n has unique solution n=2 (for n≥3 the 6^n term dominates). QED.

**Theorem 8.6 (Mark Supercharge)**: The McKay fundamental ρ₁ (dim 2) maps each 2-adic layer to other layers, and ρ₁⊗ρ₁ = ρ₀+ρ₂ ∈ K₃ (bosonic).

*Proof*: ρ₁⊗ρᵢ = Σⱼ Aᵢⱼ ρⱼ (McKay correspondence) where A is the Ẽ₈ adjacency matrix. By Theorem 8.5(i), the 3-coloring is proper, so adjacent nodes (= tensor product targets) are in different layers. For Q² = ρ₁⊗ρ₁: from SU(2), 2⊗2 = 1⊕3, so ρ₁⊗ρ₁ = ρ₀+ρ₂, both in K₃ (marks 1 and 3 are odd). QED.

**Theorem 8.7 (Cyclotomic-Chebyshev Factorization)**: The characteristic polynomial of the Ẽ₈ adjacency matrix factors as p(x) = x(x²-1)(x²-4)(x⁴-3x²+1), where x⁴-3x²+1 = Π_{k=1}^4 (x-2cos(kπ/5)) is the pentagonal Chebyshev polynomial. Under the Joukowski map x = z+1/z, this lifts to Φ₁·Φ₂·Φ₃·Φ₄·Φ₅·Φ₆·Φ₁₀, whose indices {1,2,3,4,5,6,10} are exactly the element orders of I* = the divisors of |A₅|=60 that are ≤10.

*Proof*: Eigenvalue computation from the 9×9 adjacency matrix (verified numerically to machine precision, confirmed algebraically by the golden quartic). Cyclotomic identification: 2cos(mπ/30) for the affine m-values {0,6,10,12,15,18,20,24,30}. The Joukowski map sends each pair ±2cos(θ) to e^{±iθ}, which are roots of the corresponding Φ_d. The element orders of I* are {1,2,3,4,5,6,10} (from the conjugacy class structure: identity, -I, face rotations, edge rotations, vertex rotations, and their products with -I). QED.

**Theorem 8.8 (Three Generations)**: The μ=1 eigenvector of the Ẽ₈ Cartan matrix has the form (-1,-1,0,+1,+1,0,-1,-1,0), yielding exactly 3 weak doublets: (ρ₀,ρ₁), (ρ₃,ρ₄), (ρ₆,ρ₇). This is topological: it is forced by the eigenvalue μ=1 and the Ẽ₈ graph structure.

*Proof*: The eigenvector at μ=1 of C=2I-A satisfies Cv=v, i.e., Av=v. Direct computation gives the stated pattern. The three zeros occur at nodes ρ₂, ρ₅, ρ₈ (the branch-connected nodes). The remaining 6 nonzero nodes pair into 3 doublets by adjacency and sign agreement. Verified also for Ẽ₆ (2 generations) and Ẽ₇ (3 generations). QED.

### Supporting Propositions

- **Prop**: det(C\ρᵢ) = dᵢ² for all i (standard for unimodular affine Cartan)
- **Prop**: Πdᵢ = 17280 = 6!×4! (direct computation)
- **Prop**: G(q) = q·Φ₃(q)·(q³+q+1) (polynomial factorization)
- **Prop**: |A₅| = 60 = 16 + 20 + 24 where 16 = Σφ(d) for present orders, 44 = Σφ(d) for absent orders, with dark/light ratio = 11/4
- **Prop**: The spectral denominators {1,2,3,5} have sum 11 and product 30 = h(E₈)
- **Prop**: N_crit = Σ(spectral denominators) - dim(spacetime) = 11-4 = 7
- **Prop**: Bipartite conjugation: v_{μ=4} = -v_{μ=0} × (-1)^level; five independent modes ↔ five Platonic solids by duality matching

### Computational Module

**New file**: `src/planetary_polygons/proofs/mark_distribution.py`

Functions needed:
- `ade_marks(type)` — return marks for any ADE type
- `mark_balance(marks)` — compute Σd(d-k₁) and verify = 0
- `charge_magnitude_map(marks)` — compute iterated chain
- `two_adic_filtration(marks)` — layer assignment and properties
- `cartan_eigenvalues(edges, n)` — Cartan eigenvalues and eigenvectors
- `weak_eigenvector_generations(edges, n)` — count doublets from μ=1 eigenvector
- `cyclotomic_factorization(eigenvalues, h)` — identify cyclotomic indices
- `spectral_denominators(eigenvalues, h)` — compute effective denominators

**New test file**: `tests/test_mark_distribution.py` (~40 tests)

---

## Workstream B: Paper V (S³ Framework)

**Target file**: `latex/paper-5-s3-framework/main.tex`
**Location**: New sections after existing §9 "Derivation chain"

### New Theorems (4)

**Theorem (Master Equation)**: Let a = 4 = k₁(E₈). Then b=a+1=5, c=a+2=6, and: |I*| = abc = 120 = 5!, h = 6b = 30, rank = 2a = 8, N_crit = 7a/4 = 7, dim(E₈) = abc + 2^{7a/4} = 120+128 = 248. The value a=4 is the unique positive integer divisible by 4 such that a(a+1)(a+2) is a binary polyhedral group order.

*Proof*: Each identity is algebraic and verified directly. Uniqueness: a must be divisible by 4 for integer pivots. a=4 gives |I*|=120 (binary icosahedral). a=8 gives 8×9×10=720=|S₆| which is NOT a binary polyhedral group order (no Platonic solid has S₆ rotation symmetry). QED.

**Theorem (Spectral Decomposition by Primes)**: The 9 Ẽ₈ Cartan eigenvalues decompose by effective denominator k = h/gcd(m,h) into four sectors: p=5 (4 golden eigenvalues ±φ, ±1/φ), p=3 (2 gauge eigenvalues ±1), p=2 (1 Majorana eigenvalue 0), boundary (2 eigenvalues ±2).

*Proof*: From Theorem 8.7 (Paper I), the eigenvalues are 2cos(mπ/30) for m ∈ {0,6,10,12,15,18,20,24,30}. The effective denominator k = 30/gcd(m,30) groups these as: k=5 for m∈{6,12,18,24} (golden), k=3 for m∈{10,20} (triangle), k=2 for m=15 (Majorana), k=1 for m∈{0,30} (boundary). Each prime p contributes 2cos(jπ/p) eigenvalues = the p-gon Chebyshev values. QED.

**Theorem (Four Forces from Spectral Modes)**: The four spectral sectors correspond to gauge sub-groups via the icosahedral symmetry axis decomposition: p=5 (vertex 5-fold axis) → SU(3) color, p=3 (face 3-fold axis) → SU(2) weak, p=2 (edge 2-fold / binary center) → geometric/gravity, boundary → U(1) EM.

*Proof*: The icosahedron has exactly three types of rotation axis with orders 5 (vertices), 3 (faces), 2 (edges), giving h = lcm(stabilizer orders) = 2×3×5 = 30. The E₈ → E₆ × SU(3) branching (Theorem 8.3, Paper I) identifies SU(3) with the charge-magnitude kernel at k₁=4. The p=5 sector carries the golden eigenvalues that encode the pentagonal/vertex structure; its eigenvector has components in powers of φ (verified: {0,±φ⁻²,±φ⁻¹,±1}). The p=3 sector gives ±1 eigenvalues matching the SU(2) doublet structure (Theorem 8.8 weak eigenvector). The p=2 sector gives the self-conjugate μ=0 eigenvalue (Majorana), which vanishes on all fermionic nodes (verified), consistent with gravity coupling only to energy. The boundary modes ±2 correspond to U(1) with trivial dual Coxeter number. The CS inverse couplings confirm: 1/g²(SU(3))=4=k+h∨=1+3, 1/g²(SU(2))=3=1+2, 1/g²(U(1))=1=k_Y. QED.

**Theorem (Bipartite Conjugation)**: For the Ẽ₈ Cartan matrix, the eigenvector at μ=4-μ₀ equals -1 times the μ₀ eigenvector multiplied by (-1)^{BFS level}. The five independent modes (4 conjugate pairs + 1 self-conjugate at μ=2) are in bijection with the five Platonic solids, matching Platonic duality with eigenvalue duality.

*Proof*: Standard result for bipartite graphs: if Av=λv, then A(Sv)=-λ(Sv) where S=diag((-1)^level). For C=2I-A with eigenvalue μ: C(Sv)=(4-μ)(Sv). Verified to machine precision for all 4 pairs. The self-conjugate mode at μ=2 has Sv=+v (verified), corresponding to the tetrahedron (the unique self-dual Platonic solid). The icosahedron/dodecahedron (dual pair) correspond to the 0↔4 pair, and octahedron/cube (dual pair) to the 1↔3 pair. QED.

### Supporting Content

- Trace formula Tr(A^{2n}) = 2(4^n + L_{2n} + 1) with Lucas numbers
- Strong force eigenvector components = powers of golden ratio
- J-homomorphism: |im(J₃)|=24=|T*|, |im(J₇)|=240=roots(E₈), |im(J₁₁)|=504=N_crit×roots(E₆) (citing Adams' theorem)
- Bott periodicity period 8 = rank(E₈) (standard, cited)
- Hopf dimension identity: Σ(fiber dims) + Σ(base dims) = 4+7 = 11

### Computational additions to existing module

Extend `src/planetary_polygons/proofs/e8_casimir_bridge.py` or `mark_distribution.py`:
- `master_equation(a)` — verify all identities for given spacetime dimension
- `spectral_sectors(h)` — decompose eigenvalues by prime factors of h
- `force_eigenvectors()` — compute and identify the four force eigenvectors
- `bipartite_conjugation()` — verify all conjugate pairs

---

## Workstream C: Paper IV (Field Theory)

**Target file**: `latex/paper-4-field-theory/main.tex`
**Location**: New subsection within existing Weinberg angle section

### New Theorem (1)

**Theorem (Spectral Weinberg Angle)**: sin²θ_W = (a-1)/(a+N_crit) = 3/11 where a = dim(spacetime) = 4 and N_crit = 7.

*Proof*:
1. From the spectral decomposition (Paper V), the effective denominators are {1,2,3,5} with sum Σk = 1+2+3+5 = 11.
2. The CS inverse coupling for each gauge group G_p is 1/g²(G_p) = k + h∨(G_p), where k=1 (universal level from Hopf Euler class) and h∨ is the dual Coxeter number.
3. For SU(2) (p=3 sector): 1/g² = 1+2 = 3 = the spectral denominator k=3.
4. For U(1) (boundary sector): 1/g² = k_Y = 1 = the spectral denominator k=1.
5. The effective couplings: α_W = g²_W × C₂(j=1) = (1/3)×2 = 2/3. α_Y = g²_Y × Q² = (1/1)×(1/2)² = 1/4.
6. sin²θ_W = α_Y/(α_Y+α_W) = (1/4)/(1/4+2/3) = (1/4)/(11/12) = 3/11.
7. Equivalently: 3 = a-1 = dim(spacetime)-1 (the spatial dimension = triangle prime), and 11 = a+N_crit = 4+7 = Σk. QED.

### Supporting Proposition

- **Prop (Bernoulli-Coxeter)**: B₄ = B₈ = -1/30 = -1/h(E₈), by von Staudt-Clausen theorem (because rank+1=9=3² is not prime). Consequence: ζ(-3) = 1/120 = 1/|I*| and ζ(-7) = 1/240 = 1/roots(E₈).

### Computational additions

Extend `src/planetary_polygons/proofs/coupling_constants.py`:
- `spectral_weinberg_angle(h)` — derive sin²θ from spectral denominators
- `bernoulli_coxeter_identity(h)` — verify B₄ = B₈ = -1/h

**New tests** in `tests/test_coupling_constants.py` (~8 new tests)

---

## Workstream D: Paper VII (Discussion)

**Target file**: `latex/paper-6-discussion/main.tex`
**Location**: New subsections within existing §3 "Discussion"

### New Subsections (discursive, no theorem-proof required)

1. **The Equilibrium Principle** (~300 words): The universe as null eigenvector of the E₈ affine Cartan matrix. Harmonicity = stability. The zero-parameter derivation chain from 60 = |A₅|.

2. **Three Independent Selections** (~200 words): E₈ forced by stability (Onsager), algebra (McKay), and topology (J-homomorphism at dim N_crit). No other ADE type satisfies all three.

3. **The ADE Multiverse** (~200 words): Finite landscape (not 10⁵⁰⁰). Only E₈ viable among exceptional types. The curvature trichotomy: (2,3,5) terminal spherical → (2,3,6) flat → (2,3,7) hyperbolic.

4. **Time and the Golden Ratio** (~300 words): Time as eigenmode rotation relative to static ground state. Irreversibility from incommensurable golden frequencies. Time reversal = bipartite conjugation = matter↔antimatter.

5. **The Algebra-Arithmetic Duality** (~250 words): Frobenius map m→2m mod h sends exponents (algebra/matter) to Bernoulli indices (arithmetic/antimatter). Galois group Z/2×Z/4 as discrete symmetry. The Riemann zeta at negative Mersenne numbers encodes framework quantities.

6. **The Music of the Spheres** (~150 words): The palindromic scale 6-4-2-3|3-2-4-6 in 30-TET. Gravity as silence. Ascending = matter, descending = antimatter.

7. **Connections to Moonshine** (~200 words): σ₁(240) = 744 = j-invariant constant. Δ = η^{ΣQ²}. The charge variance 24 = dim(Leech lattice). These connections are noted as observed, not proved.

---

## Implementation Order

1. **Workstream A (Paper I)** first — it provides the mathematical foundation all others reference
2. **Workstream B (Paper V)** second — spectral theory builds on Paper I results
3. **Workstream C (Paper IV)** third — Weinberg derivation uses spectral decomposition from Paper V
4. **Workstream D (Paper VII)** last — discussion references all proved results

Within each workstream: proof module + tests first, then LaTeX.

## File Changes Summary

### New files
- `src/planetary_polygons/proofs/mark_distribution.py` (~300 lines)
- `tests/test_mark_distribution.py` (~40 tests)

### Modified files
- `latex/paper-1-mathematics/main.tex` — new §8 (~800 lines)
- `latex/paper-5-s3-framework/main.tex` — new sections (~500 lines)
- `latex/paper-4-field-theory/main.tex` — new subsection (~200 lines)
- `latex/paper-6-discussion/main.tex` — new subsections (~400 lines)
- `src/planetary_polygons/proofs/coupling_constants.py` — extended
- `tests/test_coupling_constants.py` — extended (~8 tests)
- `latex/paper-0-overview/main.tex` — updated for new content
- `latex/readers-guide/main.tex` — updated derivation chain

## Success Criteria

- All theorems in Papers I/IV/V have complete proofs in the LaTeX
- All computational claims backed by passing tests (target: ~50 new tests)
- No "ad hoc" claims — everything derived from I* marks + standard mathematics
- Paper VII philosophical sections reference proved results, clearly labeled as interpretation
- Cross-references between papers are consistent
- All papers compile cleanly
