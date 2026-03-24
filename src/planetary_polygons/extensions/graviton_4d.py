r"""
The 4D graviton from Kaluza-Klein decomposition on the Seifert manifold.

The critical gap in the QM-to-gravity unification: 2+1D gravity is
topological (zero propagating DOF), so where is the graviton?

ANSWER: The 4D graviton has 2 propagating DOF. After KK reduction on S¹:
  - 3D metric g_ij: 0 DOF (topological, Witten 1988)
  - Graviphoton A_i = g_{i,φ}: 1 DOF (propagating)
  - Radion σ = g_{φφ}: 1 DOF (propagating)

  Total: 0 + 1 + 1 = 2 = the 4D graviton.

The graviphoton and radion ARE the two polarizations of the 4D graviton,
decomposed by KK reduction. The "topological" nature of 3D gravity
is compensated by these KK fields.

The graviton mass spectrum:
  - Even N: massless zero mode at m = N/2 (exact 4D massless graviton)
  - Odd N: lightest mode has mass μ = 1/2 (massive, but at the KK scale)
  - Full tower: μ_m = |m - N/2| for m = 0, ..., N-1
"""

from math import pi, sqrt, log


def dof_counting(d=4):
    """Degree-of-freedom counting for the graviton.

    In d dimensions:
      Metric components: d(d+1)/2
      Diffeomorphisms: d
      Physical DOF: d(d+1)/2 - 2d = d(d-3)/2

    For d=4: 2 DOF (the graviton).
    For d=3: 0 DOF (topological).
    """
    n_metric = d * (d + 1) // 2
    n_diffeo = d
    n_physical = d * (d - 3) // 2

    return {
        'd': d,
        'metric_components': n_metric,
        'diffeomorphisms': n_diffeo,
        'physical_dof': n_physical,
    }


def kk_decomposition():
    """KK decomposition of the 4D graviton.

    4D metric g_MN decomposes as:
      g_ij (3D metric):     6 components → 0 DOF (topological)
      A_i = g_{i,φ}:        3 components → 1 DOF (graviphoton)
      σ = g_{φφ}:           1 component  → 1 DOF (radion)

    Total: 0 + 1 + 1 = 2 = 4D graviton DOF.
    """
    # 3D metric sector
    metric_3d = {
        'field': 'g_ij (3D metric)',
        'components': 6,
        'gauge': 3,       # 3D diffeomorphisms
        'constraints': 3,  # 3D Einstein equations
        'dof': 0,
        'nature': 'topological (Witten 1988)',
    }

    # Graviphoton sector
    graviphoton = {
        'field': 'A_i = g_{i,φ} (graviphoton)',
        'components': 3,
        'gauge': 1,       # U(1) gauge
        'constraints': 1,  # Gauss law
        'dof': 1,
        'nature': 'propagating',
    }

    # Radion sector
    radion = {
        'field': 'σ = g_{φφ} (radion)',
        'components': 1,
        'gauge': 0,
        'constraints': 0,
        'dof': 1,
        'nature': 'propagating',
    }

    total = metric_3d['dof'] + graviphoton['dof'] + radion['dof']

    return {
        'sectors': [metric_3d, graviphoton, radion],
        'total_dof': total,
        'matches_4d_graviton': total == 2,
        'identification': '4D graviton (2 pol.) = graviphoton (1) + radion (1)',
    }


def graviton_mass_spectrum(N):
    """The graviton KK mass spectrum at polygon number N.

    Each KK mode m has mass μ_m = |m - N/2|.
    Even N: massless zero mode at m = N/2.
    Odd N: lightest mass = 1/2 (no massless mode).

    Returns list of (m, mass, casimir, is_massless, is_critical) tuples.
    """
    m_crit = N // 2
    f_crit = m_crit * (N - m_crit) / 2.0

    spectrum = []
    for m in range(N):
        mu = abs(m - N / 2.0)
        f = m * (N - m) / 2.0
        is_massless = abs(mu) < 1e-10
        is_critical = abs(f - f_crit) < 1e-10 and m != 0

        spectrum.append({
            'm': m,
            'mass': mu,
            'casimir': f,
            'is_massless': is_massless,
            'is_critical': is_critical,
        })

    has_massless = any(s['is_massless'] for s in spectrum)
    lightest_mass = min(s['mass'] for s in spectrum if s['m'] > 0)

    return {
        'N': N,
        'spectrum': spectrum,
        'has_massless_graviton': has_massless,
        'lightest_massive': lightest_mass,
        'n_modes': N,
        'even_N': N % 2 == 0,
    }


def graviton_propagator_structure(N):
    """Structure of the 4D graviton propagator.

    G_4D(x, x') = Σ_m G^(m)_3D(x_3D, x'_3D) e^{im(φ-φ')}

    where G^(m) is the 3D propagator at mass μ_m:
      m = N/2 (even N): massless → 1/r (Newtonian, 3D)
      m ≠ N/2: massive → e^{-μ_m r}/r (Yukawa corrections)

    At long distances (r >> R = 1/N): dominated by zero mode → 3D Newton
    At short distances (r << R): full KK tower → 4D Newton (1/r²)
    """
    spec = graviton_mass_spectrum(N)
    kk_scale = N  # 1/R in polygon units

    return {
        'N': N,
        'kk_scale': kk_scale,
        'zero_mode': 'massless (Newtonian)' if spec['has_massless_graviton']
                     else f'lightest mass = {spec["lightest_massive"]:.1f}',
        'long_distance': 'log(r) potential (3D Newton, from CS topological mode)',
        'short_distance': '1/r² potential (4D Newton, from KK tower)',
        'transition_scale': f'r ~ 1/{N} (S¹ radius)',
        'n_massive_modes': sum(1 for s in spec['spectrum'] if not s['is_massless']),
    }


def spin2_dof_check(j=2):
    """Verify the spin-2 DOF counting.

    A spin-j field in 4D has (2j+1) magnetic substates.
    After transversality (-2) and tracelessness (-1):
      Physical DOF = 2j + 1 - 2 - 1 = 2(j - 1)

    For j=2: 5 - 2 - 1 = 2 DOF.
    """
    magnetic = 2 * j + 1
    transversality = 2
    tracelessness = 1 if j >= 2 else 0
    physical = magnetic - transversality - tracelessness

    return {
        'j': j,
        'magnetic_substates': magnetic,
        'transversality_constraints': transversality,
        'tracelessness_constraints': tracelessness,
        'physical_dof': physical,
        'is_graviton': j == 2 and physical == 2,
    }


def graviton_theorem():
    """The complete graviton theorem.

    Combines:
    1. 4D DOF counting: 2 physical graviton polarizations
    2. KK decomposition: graviphoton (1) + radion (1) = 2
    3. j=2 at N=7: spin-2 Casimir gives 2 physical DOF
    4. Mass spectrum: even N has massless graviton, odd N has gap 1/2
    """
    dof_4d = dof_counting(4)
    dof_3d = dof_counting(3)
    kk = kk_decomposition()
    spin2 = spin2_dof_check(2)

    return {
        '4D_dof': dof_4d,
        '3D_dof': dof_3d,
        'kk_decomposition': kk,
        'spin2_check': spin2,
        'theorem': (
            'The 4D graviton on R × (H² ×_N S¹) has 2 propagating '
            'polarizations, identified with the graviphoton A_i = g_{i,φ} '
            '(1 DOF) and the radion σ = g_{φφ} (1 DOF) from KK reduction. '
            'The 3D gravitational sector is topological (0 DOF), but the '
            'full 4D theory recovers the 2 physical DOF of general relativity.'
        ),
        'proof_steps': [
            '1. In 4D: d(d-3)/2 = 4×1/2 = 2 physical graviton DOF.',
            '2. KK on S¹: 3D metric (0 DOF, topological) + graviphoton (1) + radion (1) = 2.',
            '3. At N=7: j=2 gives 2j+1-3 = 2 physical DOF (spin-2 graviton).',
            '4. The graviphoton + radion ARE the graviton polarizations.',
        ],
    }
