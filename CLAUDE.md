# CLAUDE.md — Planetary Polygons: Toward a Unifying Principle

## Project Overview

This project continues the work begun in `speagleg/planetary-polygons` (the spiral-hexagon repository) toward a **total unifying principle** explaining why rotating fluid systems produce persistent polygonal vortex structures.

The predecessor project established the **how**: five proven results connecting Mobius geometry, Rossby wave stationarity, topological protection, Thomson vortex stability, and Onsager negative-temperature statistics. It showed that Saturn's hexagon (N=6), Jupiter's octagonal (N=8) and pentagonal (N=5) cyclone rings all sit near |λ|=1 in the Mobius parameter space C*.

This project pursues the **why**: a single variational or algebraic principle that explains the convergence of independent mechanisms at the polygon locus.

## What We Know (from the predecessor)

### Proven Results
1. **Conjugacy theorem**: spiral-polygon family parameterized by σ in C*
2. **Stationarity**: σ=0 ⟺ Rossby ω=0 (from Im(s²)=0)
3. **Topological protection**: σ=0 preserved to all orders (branch disconnection)
4. **Thomson κ_crit = -1/4**: exact for N=6 (characteristic polynomial factorization)
5. **Thomson ≠ Rayleigh-Kuo spectrally**: proven via Galerkin projection
6. **Amplitude C=0.797**: from Fourier overlap integral (Gaussian jet)
7. **Energy-enstrophy sign structure**: H''<0, Z''>0, μ>0 for all N≥3

### Verified Against Data
- Saturn ε = 0.112 predicted vs 0.112 observed (Cassini, Gaussian jet assumption)
- Jupiter north σ_geom = 0.061, south σ_geom = 0.046 (Juno, digitized)
- Saturn wavenumber n* = 5.62 → 6
- NPS near-resonance period = 62.4 years

### What Remains Open
1. **The unifying principle**: Why do independent mechanisms (Rossby waves, vortex clustering, Onsager statistics) all converge at |λ|=1? Is there a single functional on C* that is extremized there?
2. **The Onsager connection formalized**: The sign structure (H''<0, Z''>0) is computed but the statistical mechanical argument needs to be made rigorous on C* (not just invoked by reference to Onsager 1949).
3. **The N-selection problem**: Why N=6 for Saturn, N=8 for Jupiter north, N=5 for Jupiter south? The Rossby mechanism works for Saturn but fails for Jupiter. What determines N when Rossby doesn't apply?
4. **Laboratory validation**: Barbosa Aguiar rotating tank experiments provide a controlled test where the thermostat (viscous dissipation) is known exactly.
5. **Ice giant test**: Uranus and Neptune polar observations would strengthen or falsify universality.

## Research Directions

### Direction 1: Onsager Partition Function on C*
Compute the partition function Z(β) = ∫ exp(-β H(σ)) dσ for the Thomson vortex system parameterized by the Mobius modulus σ. Show that for β < 0 (negative temperature), the distribution peaks at σ=0 (the polygon). This would formalize Step 4 of the five-step answer.

### Direction 2: Casimir Invariants and the Polygon
The QGPV is a Hamiltonian system with Casimir invariants (enstrophy, higher PV moments). The polygon may extremize a specific Casimir on C*. Investigate which Casimir functional has σ=0 as its extremum, and whether this is the same across different dynamical mechanisms.

### Direction 3: Representation Theory of Z_N in C*
The cyclic group Z_N acts on both the Thomson ring (permuting vortices) and the Fourier decomposition (selecting mode n). The |λ|=1 locus is where Z_N embeds as a subgroup of the elliptic Mobius transformations. Investigate whether the polygon is algebraically distinguished within C* through representation theory.

### Direction 4: Information-Theoretic Approach
Maximum entropy principles in 2D turbulence (Robert-Sommeria-Miller theory) predict that the equilibrium state maximizes a mixing entropy subject to conservation of energy and Casimirs. The polygon at σ=0 may be the maximum-entropy state on C*. This would connect the geometric framework to information theory.

### Direction 5: The N-Selection Mechanism
For Saturn: N=6 from Rossby dispersion (proven). For Jupiter: N is determined by vortex dynamics (observed, not derived). Investigate whether N is selected by a condition on the Thomson characteristic polynomial — specifically, whether the planet's central vortex strength κ₀ determines N through the hierarchy of critical ratios:
- N=3,4,5: κ_crit = -1/2
- N=6: κ_crit = -1/4
- N≥8: unstable without center

The observed κ₀/κ ratio at each pole would then predict N.

## Technical Foundation

### From the predecessor repo
- All Python code: `speagleg/planetary-polygons` on GitHub
- Mathematica derivations: 11 .wl files in `mathematica/derivations/`
- LaTeX paper: 15 pages, "Why Rotating Fluids Make Polygons"
- Test suite: 159 tests covering all proven results

### For this project
- **Language**: Python (numerics), Mathematica (symbolic), LaTeX (paper)
- **Key libraries**: NumPy, SciPy, SymPy, matplotlib
- **Data**: Cassini (Saturn), Juno (Jupiter), Barbosa Aguiar (lab)
- **Approach**: theory-first, validated against data, honest about caveats

## Preferences

- Be direct, skip boilerplate
- Propose concrete computations over abstract discussion
- Every claim must be either proven, computed, or labeled as conjecture
- When a result depends on an assumption (Gaussian jet, digitized data), say so
- The goal is elegance but not at the cost of honesty
- This work ventures into natural philosophy — that's intentional, not a bug

## Key References

- Onsager, L. (1949). Statistical hydrodynamics. Il Nuovo Cimento, 6, 279-287.
- Robert, R. & Sommeria, J. (1991). Statistical equilibrium states for two-dimensional flows. JFM, 229, 291-310.
- Bouchet, F. & Venaille, A. (2012). Statistical mechanics of two-dimensional and geophysical flows. Physics Reports, 515, 227-295.
- Adriani, A. et al. (2018). Clusters of cyclones encircling Jupiter's poles. Nature, 555, 216-219.
- Gavriel, N. & Kaspi, Y. (2021). The number and location of Jupiter's circumpolar cyclones explained by vorticity dynamics. Nature Geoscience, 14, 559-563.

## Directory Structure (to be built)

```
planetary-polygons-unified/
├── CLAUDE.md                    # This file
├── README.md
├── src/
│   ├── partition_function/      # Direction 1: Onsager on C*
│   ├── casimir_analysis/        # Direction 2: Casimir invariants
│   ├── representation_theory/   # Direction 3: Z_N in C*
│   ├── max_entropy/             # Direction 4: information theory
│   └── n_selection/             # Direction 5: what determines N
├── mathematica/
├── latex/
├── tests/
└── data/                        # Inherited from predecessor
```
