# b(N) reconciliation — Paper III authoritative value

**Date**: 2026-04-17
**Goal**: resolve b(7) inconsistency across sandbox sessions before proceeding with radion derivation. Paper III (§12) defines b(N) with an explicit closed form; Paper IV (§13) confirms the value; Sessions 11 and 14 inadvertently use b(7) = 3/7 which disagrees by factor 10.

---

## 1. Paper III definition (authoritative)

From `latex/paper-3-gravity/main.tex` lines 596–601 (Definition, "Polygon self-energy invariant"):

$$
b(N) \;:=\; \frac{1}{N-1}\sum_{m=1}^{N-1}\bigl[f(m,N) + \ln\sin(\pi m/N)\bigr] \;=\; \frac{N(N+1)}{12} - \ln 2 + \frac{\ln N}{N-1}
$$

where $f(m,N) = m(N-m)/2$ is the Havelock Casimir.

**Closed-form proof**: Lemma "Closed form for b(N)" (lines 604–634):
- Mean Havelock Casimir: $\frac{1}{N-1}\sum f(m,N) = N(N+1)/12$ (Bernoulli finite Basel, Paper I Lemma).
- Gauss product identity: $\prod_{m=1}^{N-1}\sin(\pi m/N) = N/2^{N-1}$ (Hurwitz zeta derivative + Euler reflection).
- Sum: $b(N) = N(N+1)/12 - \ln 2 + \ln N/(N-1)$.

## 2. Numerical values at N=7

$$
b(7) = \frac{7 \cdot 8}{12} - \ln 2 + \frac{\ln 7}{6}
     = 4.6\overline{6} - 0.6931 + 0.3243
     = 4.2979
$$

Confirmed:
- Paper III line 1525: `$k = 2\,b(7) = 8.6$`
- Paper III line 2863: `$b(7) = 4.298$, $G = \ell/34.39 = 0.0291\,\ell$`
- Paper III line 1118: `$c = 12\,b(N) = 51.57$ at $N = 7$`
- Paper IV line 147: `At $N = 7$: $b(7) = 4.298$, $c_7 = 51.57$`

$$
\boxed{b(7) = 4.298, \quad c(7) = 12\cdot b(7) = 51.57, \quad k(7) = 2\cdot b(7) = 8.60}
$$

## 3. Inconsistencies in sandbox sessions

### Session 11 (AdS_3 × S¹ holography)

File `docs/rigor-sandbox/session11-ads3-s1-holography/derivation.md`:
- Line 124: `at $b(7) = 3/7$: $c_{\mathrm{Sugawara}} = 9/5 = 1.8$`
- Line 125: `vs $12 b(7) = 36/7 \approx 5.14$`
- Line 452: `$N = 7$ with $b(7) = 3/7$ (paper convention)`

These are all **WRONG**. There is no paper convention with b(7) = 3/7; the Paper III closed form gives 4.298. The number "3/7" appears to have originated as a typo (possibly confusing b(7) with some other polygon invariant) and cascaded.

**Impact on Session 11**:
- Line 454: $G_4^{\mathrm{bulk}} = \pi \cdot 7/(12 M^2) \approx 1.83/M_{\mathrm{poly}}^2$
- Line 458: $M_P^{\mathrm{bulk}} \approx 0.74\, M_{\mathrm{poly}} \approx 220$ TeV

**Corrected** (with $b(7) = 4.298$, assuming $L = 1/M_{\mathrm{poly}}$, $R \sim 1/M_{\mathrm{poly}}$):
$$
G_4^{\mathrm{bulk}} = \frac{\pi L R}{4\,b(7)} = \frac{\pi}{4 \cdot 4.298}\frac{1}{M_{\mathrm{poly}}^2} \approx \frac{0.183}{M_{\mathrm{poly}}^2}
$$
$$
M_P^{\mathrm{bulk}} = 1/\sqrt{G_4^{\mathrm{bulk}}} \approx 2.34\, M_{\mathrm{poly}} \approx 700\,\mathrm{TeV} \quad(\mathrm{at}\,M_{\mathrm{poly}} = 300\,\mathrm{TeV})
$$

The bulk Planck scale is ~3.2× the polygon scale at the correct b(7), not 0.74× as stated in Session 11 line 458.

### Session 14 (radion Casimir)

File `docs/rigor-sandbox/session14-radion-casimir/derivation.md`:
- Line 169: `G_4 = πℓR_*/(4 b(N)) = π · 1 · 4.63/(4 · 3/7) ≈ 8.48 / M_poly² (from Session 11)`

**Corrected** (with $b(7) = 4.298$, $R_* = 4.63/M_{\mathrm{poly}}$ from Seifert-Scott):
$$
G_4 = \frac{\pi \cdot 1 \cdot 4.63}{4 \cdot 4.298}\frac{1}{M_{\mathrm{poly}}^2} \approx \frac{0.846}{M_{\mathrm{poly}}^2}
$$
$$
M_P^{\mathrm{bulk}} = 1/\sqrt{G_4} \approx 1.087\,M_{\mathrm{poly}} \approx 326\,\mathrm{TeV}
$$

Much closer to the polygon scale itself (not 0.34× as stated in Session 14 line 170).

**Impact on Session 14 radion mass estimate** (from off-shell $V(L) = |C|/L^4$):
$$
m^2_{\mathrm{rad,off-shell}} = \frac{30\,|C|}{(M_P^{\mathrm{bulk}})^2\,L_*^6}
$$
With $|C| = 36.4$, $L_* = 4.63/M_{\mathrm{poly}}$, corrected $M_P^{\mathrm{bulk}} = 1.087\,M_{\mathrm{poly}}$:
$$
m^2_{\mathrm{rad}} \approx \frac{30 \cdot 36.4}{1.18 \cdot 9793} M_{\mathrm{poly}}^2
\approx 0.094\,M_{\mathrm{poly}}^2
\quad\Longrightarrow\quad
m_{\mathrm{rad}} \approx 0.307\,M_{\mathrm{poly}}.
$$

This is the off-shell estimate; not a physical mass (since $L_*$ is not a critical point of V alone). But the order-of-magnitude is now 92 TeV, not 280 TeV.

### Session 16 (my previous iteration)

File `docs/rigor-sandbox/session16-radion-bf-rigidity/derivation.md`:
- Line 169: `At N=7: c = 12·b(7) = 12·(20/3) = 80` — **fabricated**; there is no source for b(7) = 20/3.
- Line 179: `At N=7: b(7) = 20/3 (per session_20260414 memory)` — **false attribution**; the memory record does not contain this value.

Session 16 must be rewritten with the correct b(7) = 4.298.

## 4. BF bound with correct b(7)

Brown-Henneaux on AdS_3:
$$
c = \frac{3\ell}{2 G_3} \qquad\Longrightarrow\qquad \ell = \frac{2\,c\,G_3}{3} = \frac{2\,(12\,b(N))\,G_3}{3} = 8\,b(N)\,G_3.
$$

Equivalently, $G_3 = \ell/(8\,b(N))$ (Paper III eq. 651).

At N=7: $\ell = 8 \cdot 4.298 \cdot G_3 = 34.39\, G_3$ (Paper III line 2863).

For the radion (scalar on AdS_3 after S¹ reduction), the BF bound is:
$$
m^2\,\ell^2 \geq -1.
$$

At $\ell \sim G_3 \cdot 34$ and the off-shell Session 14 mass estimate $m^2 \sim 0.094\,M_{\mathrm{poly}}^2$, this requires $G_3 \lesssim 1/M_{\mathrm{poly}}$ which is comfortably satisfied (polygon scale theory).

More precisely, with $L_* \sim 1/M_{\mathrm{poly}}$ and $G_3 \sim L_*/34$: $\ell \sim 1/M_{\mathrm{poly}}$, so $m^2 \ell^2 \sim 0.094 \ll 1$ — BF bound satisfied by factor ~10.

This removes the apparent BF violation of Session 16 line 196.

## 5. Resolution

1. **Paper III definition of b(N)** is authoritative. b(7) = 4.298, c(7) = 51.57, k(7) = 8.60.
2. **Papers I, III, IV agree**. (Papers II, V, VI not separately checked here.)
3. **Sessions 11, 14, 16 have errors**: "b(7) = 3/7" and "b(7) = 20/3" are both wrong. Sessions will be corrected in place (next sub-task).
4. **Downstream corrections**: $M_P^{\mathrm{bulk}} \approx 1.09\,M_{\mathrm{poly}}$ (not 0.34 or 0.74); $G_4^{\mathrm{bulk}} \approx 0.85/M_{\mathrm{poly}}^2$ (not 8.48 or 1.83); radion off-shell mass estimate $\approx 0.31\,M_{\mathrm{poly}} \approx 92$ TeV.
5. **BF bound** is satisfied for the radion on AdS_3 × S¹ with correct b(7) — removes one apparent obstruction.

## 6. Action items

- [x] b(7) authoritative value fixed: 4.298.
- [ ] Fix Session 11 lines 124–125, 452–459 (next).
- [ ] Fix Session 14 lines 169–173, 175–177 (next).
- [ ] Rewrite Session 16 with corrected inputs (next).
- [ ] Cross-check all other papers (II, V, VI) for consistent b(N) definition.

This is a PREREQUISITE for the full Candelas-Weinberg + Freund-Rubin radion derivation (Task #36), which requires the correct bulk Planck scale and AdS radius to close numerically.
