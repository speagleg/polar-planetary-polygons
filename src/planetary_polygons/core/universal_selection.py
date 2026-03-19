"""
Universal constraint-intersection framework for planetary polygon selection.

Central result: the observed polygon wavenumber N is determined by the
intersection of three constraints, all derived from the logarithmic
Green's function:

    N_selected = max { N : N <= N_Thomson(kappa_0/kappa)     [stability]
                           AND sin(pi/N) >= r_excl/R_ring    [packing]
                           AND n is Rossby-stationary          [wave quantization] }

Each planet activates a different subset:
    Saturn:         Rossby constraint (n=6) is tightest  -> N=6
    Jupiter north:  Thomson+max-H (N=8) is tightest      -> N=8
    Jupiter south:  Packing constraint (N<=5) is tightest -> N=5

Status:
    Thomson bound:   PROVEN (Theorem 3 + Proposition 4)
    Packing bound:   PROVEN (geometry); r_excl is OBSERVATIONAL
    Rossby bound:    Uses existing code (rossby.py)
"""
from fractions import Fraction
import math


# ---------------------------------------------------------------------------
# Havelock spectral gap (exact, using Fraction arithmetic)
# ---------------------------------------------------------------------------

def havelock_eigenvalue(N, m):
    """
    Exact Havelock eigenvalue lambda_m for the N-ring.

    lambda_m = (N-1) - m(N-m)/2,  m = 1, ..., N-1

    Returns a Fraction for exact arithmetic.
    """
    N = int(N)
    m = int(m)
    return Fraction(N - 1) - Fraction(m * (N - m), 2)


def spectral_gap(N):
    """
    Exact spectral gap (minimum Havelock eigenvalue) for the N-ring.

    The critical mode is m = floor(N/2).  Returns a Fraction.
    Positive => stable, negative => unstable.

    Examples:
        N=3: lambda_1 = 2 - 1 = 1
        N=6: lambda_3 = 5 - 9/2 = 1/2
        N=7: lambda_3 = 6 - 6 = 0  (marginal)
        N=8: lambda_4 = 7 - 8 = -1  (unstable)
    """
    N = int(N)
    m_crit = N // 2
    return havelock_eigenvalue(N, m_crit)


def spectral_gap_table(N_min=3, N_max=12):
    """
    Table of spectral gaps for N = N_min..N_max.

    Returns list of dicts with keys: N, m_crit, lambda_min, stable.
    """
    rows = []
    for N in range(N_min, N_max + 1):
        m = N // 2
        lam = spectral_gap(N)
        rows.append({
            'N': N,
            'm_crit': m,
            'lambda_min': lam,
            'stable': lam > 0,
            'marginal': lam == 0,
        })
    return rows


# ---------------------------------------------------------------------------
# Packing bound (geometric)
# ---------------------------------------------------------------------------

def packing_bound(R_ring, r_excl):
    """
    Largest N such that N non-overlapping discs of radius r_excl
    fit on a ring of radius R_ring.

    Geometry: adjacent vortex centers are separated by 2*R*sin(pi/N).
    Non-overlap requires 2*R*sin(pi/N) >= 2*r_excl, i.e.
    sin(pi/N) >= r_excl / R_ring.

    Returns the largest integer N satisfying this, or None if r_excl > R_ring.
    """
    ratio = r_excl / R_ring
    if ratio >= 1.0:
        return None
    if ratio <= 0.0:
        return None  # degenerate

    # Direct iteration avoids arcsin floating-point boundary issues.
    # sin(pi/N) is decreasing in N, so increment until it fails.
    N = 3
    while math.sin(math.pi / (N + 1)) >= ratio - 1e-12:
        N += 1
    return N


def packing_bound_exact(R_ring, r_excl):
    """
    Same as packing_bound but also returns the critical sin(pi/N) values.

    Returns dict with N_max and details for N_max and N_max+1.
    """
    N_max = packing_bound(R_ring, r_excl)
    if N_max is None:
        return {'N_max': None, 'ratio': r_excl / R_ring}

    ratio = r_excl / R_ring
    sin_N = math.sin(math.pi / N_max) if N_max >= 2 else 1.0
    sin_N1 = math.sin(math.pi / (N_max + 1))

    return {
        'N_max': N_max,
        'ratio': ratio,
        'sin_pi_over_N': sin_N,
        'sin_pi_over_N_plus_1': sin_N1,
        'margin_at_N': sin_N - ratio,
        'deficit_at_N_plus_1': sin_N1 - ratio,
    }


# ---------------------------------------------------------------------------
# Thomson bound (wraps kappa_crit)
# ---------------------------------------------------------------------------

# Known exact kappa_crit values (from Proposition 4 / hessian.py):
# N <= 7: kappa_crit = 0 (stable without central vortex)
# N = 8:  kappa_crit = 1/2
# N = 9:  kappa_crit = 1
# N >= 10: kappa_crit > 1 (increasingly large)
KAPPA_CRIT = {
    3: Fraction(0),
    4: Fraction(0),
    5: Fraction(0),
    6: Fraction(0),
    7: Fraction(0),
    8: Fraction(1, 2),
    9: Fraction(1),
    10: Fraction(2),     # approximate; exact value requires numerical computation
    11: Fraction(7, 2),  # approximate
    12: Fraction(6),     # approximate
}


def kappa_crit(N):
    """
    Critical central vortex strength ratio kappa_0/kappa for N-gon stability.

    For N <= 7: returns 0 (stable without central vortex).
    For N = 8: returns 1/2 (exact, Proposition 4).
    For N = 9: returns 1 (exact).
    For N >= 10: returns approximate values.

    The N-gon + central vortex is stable iff kappa_0/kappa >= kappa_crit(N).
    """
    N = int(N)
    if N <= 7:
        return Fraction(0)
    if N in KAPPA_CRIT:
        return KAPPA_CRIT[N]
    # For large N, kappa_crit grows roughly as (N-7)^2 / 4
    # This is a rough approximation for N > 12
    return Fraction(int(round((N - 7)**2 / 4)))


def thomson_bound(kappa_ratio):
    """
    Largest stable N given kappa_0/kappa = kappa_ratio.

    N_Thomson = max { N : kappa_crit(N) <= kappa_ratio }

    For kappa_ratio = 0:   N_Thomson = 7
    For kappa_ratio = 0.5: N_Thomson = 8
    For kappa_ratio = 1.0: N_Thomson = 9

    Returns int.
    """
    if isinstance(kappa_ratio, (int, float)):
        kappa_ratio = Fraction(kappa_ratio).limit_denominator(1000)

    N = 3
    while True:
        kc = kappa_crit(N + 1)
        if kc > kappa_ratio:
            return N
        N += 1
        if N > 50:  # safety
            return N


# ---------------------------------------------------------------------------
# Rossby wavenumber (from existing rossby.py infrastructure)
# ---------------------------------------------------------------------------

def rossby_stationary_n(U_max, beta, R_hex, sigma_jet=None):
    """
    Stationary Rossby wavenumber from the dispersion relation.

    Simple scaling: n* = R_hex * sqrt(beta / U_max)

    This uses the bare beta-plane parameter and the hexagonal jet radius.
    The leading-order estimate gives n* ~ 5.6 for Saturn; the full
    Rayleigh-Kuo eigenvalue computation rounds this to n* = 6
    (Sanchez-Lavega+ 2014).

    Returns float (the nearest integer is the selected mode).
    """
    K2 = beta / U_max
    if sigma_jet is not None:
        l2 = (math.pi / sigma_jet) ** 2
        k2 = K2 - l2
        if k2 > 0:
            return R_hex * math.sqrt(k2)
    return R_hex * math.sqrt(K2)


# ---------------------------------------------------------------------------
# Universal selection (constraint intersection)
# ---------------------------------------------------------------------------

def universal_selection(N_thomson, N_pack, N_rossby=None):
    """
    Constraint intersection: select N from the overlap of all active bounds.

    Parameters
    ----------
    N_thomson : int
        Thomson stability bound (max stable N).
    N_pack : int or None
        Packing bound (max N that fits geometrically). None = no constraint.
    N_rossby : int or None
        Rossby stationary wavenumber (exact integer). None = not applicable.

    Returns
    -------
    dict with keys:
        N_selected : int
        binding_constraint : str
        constraints : dict of individual bounds
    """
    bounds = {'thomson': N_thomson}
    active = [N_thomson]

    if N_pack is not None:
        bounds['packing'] = N_pack
        active.append(N_pack)

    if N_rossby is not None:
        bounds['rossby'] = N_rossby
        active.append(N_rossby)

    N_selected = min(active)

    # Identify binding constraint
    binding = []
    for name, val in bounds.items():
        if val == N_selected:
            binding.append(name)

    return {
        'N_selected': N_selected,
        'binding_constraint': '+'.join(binding),
        'constraints': bounds,
    }


# ---------------------------------------------------------------------------
# Planet-specific selections
# ---------------------------------------------------------------------------

# Saturn physical parameters
SATURN = {
    'U_max': 120.0,          # m/s, hexagonal jet peak speed
    'beta': 1.46e-12,        # m^-1 s^-1, at 76 deg N
    'sigma_jet': 2.5e6,      # m, jet half-width
    'R_hex': 5.1e7,          # m, hexagon radius
    'kappa_ratio': 0.0,      # no central vortex for jet meander
}

# Jupiter north physical parameters
JUPITER_NORTH = {
    'R_ring': 7.473e6,       # m, ring radius (from Juno, Adriani+ 2018)
    'r_cyclone': 2.5e6,      # m, mean cyclone radius (north)
    'kappa_ratio': 0.7,      # kappa_0/kappa (conservative estimate)
    'N_observed': 8,
}

# Jupiter south physical parameters
JUPITER_SOUTH = {
    'R_ring': 8.0e6,         # m, ring radius (~8000 km from pole, Juno)
    'r_cyclone': 3.5e6,      # m, mean cyclone radius (south, ~2x north)
    'kappa_ratio': 0.7,      # assumed similar to north
    'N_observed': 5,
    'beta_drift_factor': 1.3,  # r_excl / r_cyclone from beta-drift (Gavriel+Kaspi 2021)
}


def saturn_selection():
    """
    Saturn N=6: Rossby stationarity is the binding constraint.

    Returns dict with selection details.
    """
    p = SATURN

    # Rossby wavenumber
    n_star = rossby_stationary_n(
        p['U_max'], p['beta'], p['R_hex']
    )
    N_rossby = round(n_star)

    # Thomson bound (no central vortex => N_thomson = 7)
    N_thom = thomson_bound(p['kappa_ratio'])

    # No packing constraint for jet meander
    result = universal_selection(N_thom, N_pack=None, N_rossby=N_rossby)
    result['n_star_continuous'] = n_star
    result['planet'] = 'Saturn'
    result['mechanism'] = 'jet meander (Rossby stationarity)'
    return result


def jupiter_north_selection():
    """
    Jupiter north N=8: Thomson + energy monotonicity is the binding constraint.

    Returns dict with selection details.
    """
    p = JUPITER_NORTH

    # Thomson bound
    N_thom = thomson_bound(p['kappa_ratio'])

    # Packing bound (generous — cyclones fit easily at N=8)
    r_excl = p['r_cyclone']
    N_pack = packing_bound(p['R_ring'], r_excl)

    # No Rossby constraint (discrete vortices, not jet meander)
    result = universal_selection(N_thom, N_pack, N_rossby=None)
    result['planet'] = 'Jupiter north'
    result['mechanism'] = 'Thomson stability + Onsager max-H'
    result['spectral_gap'] = spectral_gap(result['N_selected'])
    return result


def jupiter_south_selection():
    """
    Jupiter south N=5: Packing constraint is the binding constraint.

    The south-pole cyclones are ~2x larger than north-pole cyclones
    (Adriani+ 2018). The exclusion radius includes a beta-drift buffer
    zone (Gavriel & Kaspi 2021): r_excl ~ 1.3 * r_cyclone.

    Returns dict with selection details.
    """
    p = JUPITER_SOUTH

    # Thomson bound (same as north, kappa_ratio ~ 0.7)
    N_thom = thomson_bound(p['kappa_ratio'])

    # Packing bound with beta-drift exclusion
    r_excl = p['r_cyclone'] * p['beta_drift_factor']
    N_pack = packing_bound(p['R_ring'], r_excl)

    # No Rossby constraint
    result = universal_selection(N_thom, N_pack, N_rossby=None)
    result['planet'] = 'Jupiter south'
    result['mechanism'] = 'geometric packing (large cyclones + beta-drift)'
    result['r_excl_m'] = r_excl
    result['r_excl_over_r_cyclone'] = p['beta_drift_factor']
    result['spectral_gap'] = spectral_gap(result['N_selected'])
    return result


def cross_planetary_table():
    """
    Cross-planetary comparison table.

    Returns list of dicts, one per planet/pole, with all constraint values.
    """
    rows = []

    # Saturn
    sat = saturn_selection()
    rows.append({
        'system': 'Saturn (76 deg N)',
        'N_observed': 6,
        'N_selected': sat['N_selected'],
        'N_thomson': sat['constraints']['thomson'],
        'N_rossby': sat['constraints'].get('rossby'),
        'N_packing': sat['constraints'].get('packing'),
        'binding': sat['binding_constraint'],
        'spectral_gap': spectral_gap(6),
        'match': sat['N_selected'] == 6,
    })

    # Jupiter north
    jn = jupiter_north_selection()
    rows.append({
        'system': 'Jupiter north',
        'N_observed': 8,
        'N_selected': jn['N_selected'],
        'N_thomson': jn['constraints']['thomson'],
        'N_rossby': jn['constraints'].get('rossby'),
        'N_packing': jn['constraints'].get('packing'),
        'binding': jn['binding_constraint'],
        'spectral_gap': spectral_gap(8),
        'match': jn['N_selected'] == 8,
    })

    # Jupiter south
    js = jupiter_south_selection()
    rows.append({
        'system': 'Jupiter south',
        'N_observed': 5,
        'N_selected': js['N_selected'],
        'N_thomson': js['constraints']['thomson'],
        'N_rossby': js['constraints'].get('rossby'),
        'N_packing': js['constraints'].get('packing'),
        'binding': js['binding_constraint'],
        'spectral_gap': spectral_gap(5),
        'match': js['N_selected'] == 5,
    })

    return rows


if __name__ == '__main__':
    print('=== Spectral Gap Table ===')
    for row in spectral_gap_table(3, 12):
        status = 'stable' if row['stable'] else ('marginal' if row['marginal'] else 'UNSTABLE')
        print(f"  N={row['N']:2d}: lambda_min = {row['lambda_min']:>6s}  [{status}]")

    print('\n=== Cross-Planetary Table ===')
    for row in cross_planetary_table():
        check = 'OK' if row['match'] else 'MISMATCH'
        print(f"  {row['system']:20s}: N_obs={row['N_observed']}, "
              f"N_sel={row['N_selected']}, binding={row['binding']:12s}  [{check}]")
        print(f"    Thomson={row['N_thomson']}, Rossby={row['N_rossby']}, "
              f"Packing={row['N_packing']}, gap={row['spectral_gap']}")
