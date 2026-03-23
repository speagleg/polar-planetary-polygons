r"""
Dark matter and dark energy from the Havelock Field Theory.

The cosmological energy budget at N=11:
  Dark Energy = b(N) + N/4 (vacuum + radion zero-point)
  Dark Matter = (1/2) Σ ln|λ_m| (frozen mode one-loop)
  Baryonic Matter = ΔE (WDW mass gap)

At N=11 with the radion correction:
  DE = 68.9% (Planck: 68.5 ± 0.7%)  — 0.6σ
  DM = 26.9% (Planck: 26.6 ± 0.7%)  — 0.4σ
  M  = 4.2%  (Planck:  4.9 ± 0.06%) — tension remains

Dark matter candidates: frozen Havelock modes
  - Massive (Casimir gaps: 1, 3, 6, 10 = triangular numbers)
  - Stable (Z_N protected)
  - Non-luminous (different KK charge from Higgs)
  - Cold (zero kinetic energy at threshold)
  - Mass ratios: 1 : √3 : √6 : √10

N=11 is special:
  - [K₁₁:Q] = 5 = rank(SU(5)) — the GUT group
  - Sits at the quantum regime boundary (N ≥ 11)
  - 5 palindromic pairs → 5 fundamental reps of SU(5)
"""

import math


def casimir(m, N):
    return m * (N - m) / 2.0


def b_exact(N):
    return N * (N + 1) / 12 - math.log(2) + math.log(N) / (N - 1)


def dark_sector_budget(N=11, delta_E=0.81, include_radion=True):
    """Compute the cosmological energy budget.

    F_DE = b(N) + N/4 (vacuum + radion zero-point)
    F_DM = (1/2) Σ ln|λ_m| (frozen mode one-loop free energy)
    F_M  = ΔE (mass gap = baryonic matter)

    Returns dict with fractions and tensions.
    """
    b = b_exact(N)
    mc = N // 2
    fc = casimir(mc, N)

    F_vac = b
    if include_radion:
        F_vac += N / 4.0  # radion zero-point = (1/2) × M_radion = N/4

    F_loop = 0.5 * sum(
        math.log(abs(fc - casimir(m, N)))
        for m in range(1, N)
        if abs(fc - casimir(m, N)) > 0.01
    )

    F_matter = delta_E
    F_total = F_vac + F_loop + F_matter

    de_pct = F_vac / F_total * 100
    dm_pct = F_loop / F_total * 100
    m_pct = F_matter / F_total * 100

    return {
        'N': N,
        'F_vac': F_vac,
        'F_loop': F_loop,
        'F_matter': F_matter,
        'F_total': F_total,
        'DE_pct': de_pct,
        'DM_pct': dm_pct,
        'M_pct': m_pct,
        'DE_DM_ratio': F_vac / F_loop if F_loop > 0 else float('inf'),
        'sigma_DE': abs(de_pct - 68.47) / 0.73,
        'sigma_DM': abs(dm_pct - 26.60) / 0.73,
        'sigma_M': abs(m_pct - 4.93) / 0.06,
    }


def dark_matter_spectrum(N=11):
    """The dark matter particle spectrum at polygon number N.

    Returns list of (pair, casimir, mass_gap, mass) for each frozen pair.
    """
    mc = N // 2
    fc = casimir(mc, N)

    spectrum = []
    for m in range(1, (N + 1) // 2):
        f = casimir(m, N)
        lam = fc - f
        M = math.sqrt(2 * lam) if lam > 0.01 else 0
        is_critical = lam < 0.01
        spectrum.append({
            'pair': (m, N - m),
            'casimir': f,
            'eigenvalue_gap': lam,
            'mass': M,
            'is_critical': is_critical,
            'degeneracy': 2,
        })
    return spectrum


def required_mass_gap(N=11, include_radion=True):
    """The mass gap required to match the observed baryon fraction.

    Ω_b / (Ω_b + Ω_DM) = F_matter / (F_loop + F_matter) = 0.1564
    """
    b = b_exact(N)
    mc = N // 2
    fc = casimir(mc, N)

    F_loop = 0.5 * sum(
        math.log(abs(fc - casimir(m, N)))
        for m in range(1, N)
        if abs(fc - casimir(m, N)) > 0.01
    )

    baryon_frac = 0.0493 / (0.0493 + 0.2660)  # Planck 2018
    # F_matter / (F_loop + F_matter) = baryon_frac
    # F_matter = baryon_frac × F_loop / (1 - baryon_frac)
    F_matter = baryon_frac / (1 - baryon_frac) * F_loop

    return F_matter
