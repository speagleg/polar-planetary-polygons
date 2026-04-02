# Non-Technical Companion Paper Design

**Date**: 2026-04-02
**Author**: Gordon Speagle (voice), Claude (drafting)
**Status**: Approved design, ready for implementation

## Purpose

A single document that explains the entire six-paper Havelock Field Theory series in language accessible to a curious reader with no science background, while including translated equations for science-adjacent professionals. It mirrors the technical papers section by section so a reader can cross-reference.

## Audience

Three layers, served simultaneously:
1. **Curious layperson** — no science background, reads for the story and ideas
2. **Science-adjacent professional** — can follow an equation if every symbol is named
3. **Skimmer** — reads only the italicized bottom-line sentences and the scorecard

## Voice and Style

First person. Gordon explaining his own work. Discovery narrative.

**Voice rules (non-negotiable):**
- Short declarative sentences. "The series is six papers." Not "The series comprises six papers."
- State what IS, not what isn't. "The polygon sits at the bottom of an energy valley" not "The polygon is not at the top of an energy hill."
- No hedging filler: no "it turns out that," "interestingly," "remarkably," "it is worth noting that," "delve," "tapestry," "landscape" (as metaphor), "elegant," "beautiful," "shed light on," "paving the way."
- Dashes for asides — like this — not parenthetical hedges.
- Active voice throughout. "I proved X" not "X was shown to hold."
- Technical precision even in plain language. Don't say "tiny" when you mean "10⁻¹⁶."
- Analogies must be physically accurate, not just evocative. If the analogy breaks, say where.
- No AI shibboleths: no "crucial," "utilize," "facilitate," "leverage," "robust," "comprehensive," "cutting-edge," "novel approach," "paradigm shift," "groundbreaking."
- Match the cadence of the technical papers: short paragraphs, clear topic sentences, no throat-clearing.

## Format

LaTeX document at `latex/companion/main.tex`, using the shared preamble.

## Structure

### Prologue: "The Polygon Number" (3-5 pages)

No equations. Punchline-first.

1. **Opening hook**: Saturn's hexagon and Jupiter's octagon. Not accidents — signatures of a formula.
2. **The one idea**: Stability of a polygon splits into surface + geometry. Threshold is N=7. This N=7 determines the graviton, the gauge group, and the cosmological constant.
3. **The scorecard**: Plain-English table of all 17 predictions vs. observations. What the theory says, what we measure, how close.
4. **The honest disclaimer**: Three tiers — Theorem (proved), Derivation (chain with controlled approximations), Conjecture. Translated from Paper VI's classification.
5. **The map**: One paragraph per paper.

### Part I: "The Mathematics of Polygons" (8-12 pages)

Mirrors Paper I (7 sections → 6 companion sections).

| Companion section | Technical section | Core idea |
|---|---|---|
| Why logarithms are special | §1-2 | Only interaction where polygon stability is scale-independent |
| The sign rule: bowls, not hilltops | §3 | Regular polygon is energy minimum, not maximum |
| The Havelock formula: one equation, two parts | §4 | λ_m = C₁ - m(N-m)/2 — presented, every symbol named |
| Why seven is the magic number | §4-5 | On flat surface, C₁ = N-1; at N=7 they balance exactly |
| Curved surfaces and algebraic number theory | §5-6 | Thresholds on H² live in quadratic number fields; ξ*=8-3√7 |
| The stability phase diagram | §7 | Sharp boundaries between stability zones (K-theory, translated) |

### Part II: "The Physics of Vortex Rings" (8-12 pages)

Mirrors Paper II (12 sections → 4 blocks).

| Block | Technical sections | Core idea |
|---|---|---|
| How vortices actually move | §1-3 | No inertia; pushed by neighbors; constrained equilibrium |
| Stabilizing the unstable | §4-5 | Central vortex threshold; N=7 quartic bifurcation |
| From perfect to realistic | §6-9 | Blob correction (profile-independent); Rossby bridge (Saturn N=6) |
| Vortices meet gravity | §10-12 | Deficit angle = circulation; same Green's function; isomorphism |

### Part III: "How Gravity Emerges" (10-14 pages)

Mirrors Paper III (13 sections → 5 blocks).

| Block | Technical sections | Core idea |
|---|---|---|
| The graviton is a wobble of seven | §1-2 | Marginal mode at N=7 carries spin 2; Pell equation uniqueness |
| Why the universe has constant curvature | §3-4 | Jensen + Onsager → R=const → Einstein's equation |
| The cosmological constant and the breathing mode | §5-7 | WDW on breathing mode; c=12b(N) from Fisher-Rao; Λ from ground state |
| Black holes, holograms, and the full Riemann tensor | §8-11 | BTZ phase transition; holography; 3-layer → all 10 Weyl components |
| From statistics to quantum mechanics | §12-13 | Feynman-Kac: thermodynamics IS quantum gravity; self-decoherence |

### Part IV: "The Particles Inside the Polygon" (10-14 pages)

Mirrors Paper IV (13 sections → 5 blocks).

| Block | Technical sections | Core idea |
|---|---|---|
| The shape of spacetime is forced | §1-2 | N=4+7=11; Thurston eliminates all but Seifert; 4D graviton emerges |
| One number sets every coupling | §3-5 | c=12b(N) determines α_s, G, Weinberg angle; coupling lock |
| Where the Standard Model gauge group comes from | §6-8 | Klein quartic → Frobenius → McKay → SU(3); SU(2) from N=4; confinement |
| The Weinberg angle and the CKM phase | §9-10 | sin²θ_W = 3/11 (arithmetic shown); δ = 70.2° from scattering integral |
| Fermion masses, the Higgs, and consistency | §11-13 | Mass hierarchy from WKB; Higgs 122-128 GeV; σ/Λ²=5.97; proton stability |

### Part V: "The Numbers of the Universe" (8-12 pages)

Mirrors Paper V (12 sections → 4 blocks).

| Block | Technical sections | Core idea |
|---|---|---|
| Why N=11, and the cosmological constant | §1-4 | Flux additivity; elimination table; Λ₃=(N²-16)/16 |
| The hierarchy problem solved by tunneling | §5-6 | S_BO(7)=18.274; three-component decomposition; 0.04% match |
| The cosmic energy budget | §7-9 | Tree=DE, one-loop=DM, tunneling=baryons; instanton resummation |
| Neutrinos, inflation, and the beginning | §10-12 | Seesaw; radion inflation; Penrose past hypothesis resolved |

### Part VI: "The Scorecard" (4-6 pages)

Mirrors Paper VI (4 sections).

| Section | Technical section | Core idea |
|---|---|---|
| What goes in, what comes out | §1 | One integer, one scale, three identifications → 17 outputs |
| How confident should you be? | §2-3 | Algebraic tier (exact) vs geometric tier (~5%); cumulative uncertainty |
| How to prove this wrong | §3 | Six binary pass/fail tests |
| What remains open | §4 | DM production, η_B factor-3, light quark masses |

### Epilogue: "One Formula" (1-2 pages)

Returns to Saturn's hexagon. One sentence per paper. Closes with what confirmation or refutation looks like.

## Equation Policy

- The central formula λ_m = C₁ - m(N-m)/2 is presented once (Part I §3) with every symbol translated.
- Key derived equations (sin²θ_W = 3/11, Λ₃ = (N²-16)/16, hierarchy decomposition) are shown with full symbol translation.
- All other equations are described in words only.
- Every equation that appears gets a plain-English sentence immediately after: "In words: ..."

## Status Tags

Every factual claim gets one of:
- **(Proved)** — mathematical theorem, no physical assumptions beyond the identification
- **(Derived)** — follows from the structural identifications with controlled approximations
- **(Conjectured)** — numerically verified but not proved from first principles

These match Paper VI's classification exactly.

## Cross-References

Each section header includes: `[Technical reference: Paper X, §Y]`

## Estimated Length

55-75 pages. Comparable to a short book or long review article.

## Implementation Notes

- Single LaTeX file `latex/companion/main.tex`
- Uses `\input{../shared/preamble}` for font/style consistency
- No `\externaldocument` (the companion is self-contained)
- Minimal bibliography (only references the series itself and a few textbook sources for analogies)
- No figures in v1 (text only); figures can be added later
