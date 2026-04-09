# Paper I: Bernoulli Backbone Mathematics — Spec 3A of 4

## Goal

Add a new section to Paper I (the mathematics paper) containing the Bernoulli-Havelock backbone identities: 3 theorems, 3 corollaries, 2 propositions, 1 remark. Pure mathematics, no physics. ~120-150 lines of LaTeX.

## Location

New section after the existing stability analysis and growth law sections in `latex/paper-1-mathematics/main.tex`. The section title: "The Bernoulli backbone."

## Content (in order)

### Theorem: Bernoulli-Havelock identity [FULL PROOF]
The Havelock Casimir f(m,N) = m(N-m)/2 is an affine evaluation of the second Bernoulli polynomial:

  f(m,N) = (N^2/12)(1 - 6 B_2(m/N))

where B_2(x) = x^2 - x + 1/6.

Proof: Direct expansion of B_2(m/N) = (m/N)^2 - (m/N) + 1/6 = (m^2 - mN + N^2/6)/N^2. Then 1 - 6B_2 = 1 - 6(m^2-mN+N^2/6)/N^2 = (6mN - 6m^2)/N^2 = 6m(N-m)/N^2. Multiply by N^2/12: (N^2/12)(6m(N-m)/N^2) = m(N-m)/2 = f(m,N). QED.

### Corollary: Parabola form [ONE LINE]
1 - 6B_2(x) = 6x(1-x). (Expand B_2 directly.)

### Theorem: Closed-form moment tower [FULL PROOF]
M_k = integral_0^1 [6x(1-x)]^k dx = 6^k (k!)^2 / (2k+1)!

Proof: By the parabola form, M_k = 6^k integral_0^1 x^k(1-x)^k dx = 6^k B(k+1, k+1) where B is the Euler Beta function. By the Beta-Gamma identity: B(k+1,k+1) = Gamma(k+1)^2/Gamma(2k+2) = (k!)^2/(2k+1)!. QED.

### Corollary: Bernoulli-zeta bridge [PROOF SKETCH]
M_2 = 6/5 = 3 zeta(4)/zeta(2)^2.

Sketch: M_2 = 36*B(3,3) = 36*(4/120) = 6/5. And zeta(4)/zeta(2)^2 = (pi^4/90)/(pi^4/36) = 2/5. So 3*(2/5) = 6/5. QED.

### Corollary: Universal trigonometric identity [ONE LINE]
sin^2(arctan(sqrt(N))) = N/(N+1) for all N. (From tan(theta) = sqrt(N) and the Pythagorean identity.)

### Theorem: Von Staudt-Clausen characterization [FULL PROOF]
For odd N >= 3 with N-1 even: N divides denom(B_{N-1}) if and only if N is prime.

Proof: By the von Staudt-Clausen theorem, denom(B_{2k}) = product of primes p with (p-1)|2k. For B_{N-1} with N an odd prime: (N-1)|(N-1) is trivially true, so N appears in the product. For N composite: N is not prime and therefore cannot appear in the von Staudt-Clausen product. QED.

Application: At N=7, denom(B_6) = 2*3*7 = 42, so 7 | 42. Combined with the Havelock stability bound (lambda_min(7) = 0, lambda_min(8) < 0), this gives an independent number-theoretic characterization of the critical polygon.

### Proposition: Unified conformal dimension [PROOF SKETCH]
c_m = 1/2 + lambda_m/N where lambda_m = (N-1) - m(N-m)/2.

At the marginal mode (lambda=0): c = 1/2 (the Breitenlohner-Freedman threshold). For stable modes (lambda > 0): c > 1/2.

Sketch: lambda_m is the complement of the Casimir: f + lambda = N-1. The conformal dimension c = 1/2 + lambda/N places each mode relative to the BF threshold, with the most stable mode furthest above it.

### Proposition: Magri tower confirmation [PROOF SKETCH + REFERENCE]
The Magri coupling ratio at level 4 satisfies c_4/c_3 = 2/7 = 12 B_6.

Sketch: The hexic coefficient beta_0/(N f^3) = 4/45, and the predicted octic coefficient gamma_0/(N f^4) = 8/315. The ratio gamma_0/(beta_0 * f) = (8/315)/(4/45) = 2/7 = 12 * (1/42) = 12 B_6. This confirms that B_6 enters the Magri hierarchy at level 4, as predicted by the Bernoulli tower conjecture. Verified numerically (see bernoulli_havelock.py, 118 tests).

### Remark: The unified quantity
lambda_m encodes both the representation theory (through the Casimir f = (N-1) - lambda) and the geometry (through the conformal dimension c = 1/2 + lambda/N). The identities of this section are applied in Papers IV-VI.

## What we're NOT adding
- Any physics (CKM, PMNS, masses, baryogenesis)
- Forward pointers beyond the closing remark
- Changes to existing sections

## Files to modify
- `latex/paper-1-mathematics/main.tex` — add new section

## Label conventions
Following Paper I's existing pattern:
- Theorems: `thm:bernoulli-havelock`, `thm:moment-tower`, `thm:von-staudt-N`
- Corollaries: `cor:parabola`, `cor:zeta-bridge`, `cor:sin2-arctan`
- Propositions: `prop:unified-conformal`, `prop:magri-b6`
- Remark: `rmk:unified-quantity`

## Success criteria
1. Paper I compiles without errors
2. No duplicate labels
3. No physics content in the new section
4. All 3 theorems have complete proofs
5. The 2 propositions have proof sketches
6. The 3 corollaries have one-line or sketch proofs
