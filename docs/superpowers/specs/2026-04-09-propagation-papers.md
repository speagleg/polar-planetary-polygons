# Propagation Papers — Spec 3D of 4

## Goal

Update all remaining papers that reference 68.63° or the old CKM formula. These are summaries and cross-references that consume results from Papers I, IV, V, VI. No new derivations.

## Files and changes

### latex/paper-0-overview/main.tex (2 occurrences)

- **Line 85**: `CKM phase $\delta = 68.63^\circ$` → `CKM phase $\delta = \arctan(\sqrt{7}) = 69.3^\circ$`
- **Line 243**: `$\delta = 68.63^\circ$ from BF-crossing` → `$\delta = \arctan(\sqrt{7})$ from the Z_7 quadratic Gauss sum`
- ADD: mention of PMNS predictions and baryon asymmetry in the overview list
- ADD: mention the Bernoulli backbone as the organizing principle

### latex/paper-3-gravity/main.tex (1 occurrence)

- **Line 3688**: Summary table entry `$\delta_{\mathrm{CKM}} = 68.63^\circ$ & BF-crossing Plancherel weight & $2\,\theta_{\mathrm{CS}}\tanh(\pi)$`
  → `$\delta_{\mathrm{CKM}} = \arctan(\sqrt{7}) = 69.3^\circ$ & Z_7 Gauss sum & Paper IV, Theorem~\ref{thm:ckm-phase}`

### latex/paper-A-appendices/main.tex (1 occurrence)

- **Line 314**: `CKM phase $\delta = 68.63^\circ$ & Theorem & Paper IV, §12`
  → `CKM phase $\delta = \arctan(\sqrt{7}) = 69.3^\circ$ & Theorem & Paper IV, §12`

### latex/readers-guide/main.tex (1 occurrence)

- **Line 139**: `CKM phase $\delta = 68.63^\circ$ from` → `CKM phase $\delta = \arctan(\sqrt{7})$ from`

### latex/companion/main.tex (5 occurrences)

- **Line 126**: `$68.63^\circ$` → `$69.3^\circ$` (or `$\arctan(\sqrt{7})$`)
- **Line 2644**: `polygon prediction: $\delta = 68.63^\circ$` → `$\delta = \arctan(\sqrt{7}) \approx 69.3^\circ$`
- **Lines 2656-2658**: Replace Plancherel density explanation with Gauss sum explanation (non-technical: "the sum over the quadratic residues mod 7 gives a complex number whose angle is the CP phase")
- **Lines 2665-2674**: Replace full theta_CS*tanh(pi) derivation with the Gauss sum chain (accessible version)
- **Lines 2677-2681**: Update "no parameter is adjusted" statement (still true, stronger now)
- ADD: brief mention of PMNS predictions, baryon asymmetry, strong CP

### latex/supplement-proofs/main.tex (~20 occurrences)

- **Lines 847-1046**: The ENTIRE expanded CKM proof section needs replacement
  - This is a detailed expansion of Paper IV's derivation
  - Replace the 6-step Plancherel proof with the Gauss sum derivation
  - Replace all intermediate numerical values
  - This is the LARGEST single change in Spec 3D

## What does NOT change

- latex/paper-1-mathematics/main.tex (handled in Spec 3A)
- latex/paper-2-physics/main.tex (no CKM references)
- latex/paper-4-field-theory/main.tex (handled in Spec 3B)
- latex/paper-5-cosmology/main.tex (handled in Spec 3C)
- latex/paper-6-discussion/main.tex (handled in Spec 3C)

## Execution order

1. supplement-proofs first (biggest change, mirrors Paper IV)
2. companion (non-technical rewrite of CKM explanation)
3. paper-0-overview (add backbone mention)
4. paper-3-gravity, paper-A-appendices, readers-guide (simple replacements)

## Success criteria

1. All files compile
2. Zero instances of "68.63" in the entire latex/ directory
3. Zero instances of "Plancherel" in CKM derivation context (supplement-proofs, companion)
4. The companion explanation is accessible to non-specialists
5. All cross-references to thm:ckm-phase still resolve
6. Paper 0 overview mentions the Bernoulli backbone, PMNS, and baryon asymmetry
