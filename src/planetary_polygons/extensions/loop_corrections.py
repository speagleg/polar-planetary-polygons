r"""
One-loop corrections in the Havelock Field Theory.

The theory is 3D Chern-Simons + matter on R × (H² ×_N S¹).
Three exact results from CS non-renormalization:

1. CS LEVEL SHIFT (Coleman-Hill / Pisarski-Rao / Redlich):
   k_eff = k_bare + (1/2) × (n_boson - n_fermion)
   where n counts Majorana fermion equivalents with sign.
   For N_D Dirac fermions: shift = -N_D/2 (each Dirac = 2 Majorana, sign from parity anomaly).
   Beyond one loop: NO further renormalization (k must be integer → beta = 0 exactly).

2. ONE-LOOP COSMOLOGICAL CONSTANT (Coleman-Weinberg):
   ΔΛ = (1/2) Σ_bosons ln(μ_m²/Λ_UV²) - Σ_fermions ln(μ_m^f²/Λ_UV²)
   In 3D this is a finite sum (super-renormalizable), no UV divergence for Λ.

3. GAUGE COUPLING RUNNING:
   CS coupling: discrete shift only (no continuous running).
   U(1) Maxwell coupling: runs via standard β-function from charged matter loops.

References:
  - Coleman-Hill (1985): Phys. Lett. B159, 184
  - Pisarski-Rao (1985): Phys. Rev. D32, 2081
  - Redlich (1984): Phys. Rev. Lett. 52, 18
  - Dunne, "Aspects of Chern-Simons Theory" (Les Houches lectures)
"""

from math import pi, sqrt, log, log2, factorial
from fractions import Fraction


def casimir(m, N):
    """Havelock Casimir f(m,N) = m(N-m)/2."""
    return m * (N - m) / 2.0


def b_exact(N):
    """Havelock central charge coefficient."""
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


def central_charge(N):
    """c = 12b(N)."""
    return 12 * b_exact(N)


# =====================================================================
# 1. CHERN-SIMONS LEVEL SHIFT
# =====================================================================

def cs_level_shift(N):
    r"""Compute the one-loop CS level shift from matter loops.

    The CS level receives a one-loop exact correction from fermions
    (parity anomaly / Redlich 1984):

      k_eff = k_bare - (1/2) × Σ_f sign(m_f)

    For N Dirac fermions with POSITIVE masses (all KK modes):
      Each Dirac fermion contributes -1/2 × sign(m_f) = -1/2.
      Total shift: Δk = -N/2.

    But MASSLESS fermions contribute -1/2 × sign(0) = 0 (ambiguous).
    For odd N: all fermion masses |m - (N-1)/2| are half-integer → nonzero.
    For even N: m = (N-1)/2 is not integer, so no massless fermion.
    Actually: μ_m^f = |m - (N-1)/2|. For integer m:
      - N even: (N-1)/2 is half-integer, so μ_m^f > 0 for all m. N massive fermions.
      - N odd: (N-1)/2 is integer, so m = (N-1)/2 has μ = 0. (N-1) massive + 1 massless.

    The massless fermion (odd N) requires regularization (Pauli-Villars).
    With PV regularization: the massless fermion contributes -1/2 × sign(M_PV) = -1/2.
    So: Δk = -N/2 for all N (with PV reg for the massless case).

    The PHYSICAL level:
      k_phys = k_bare + Δk = c/6 - N/2 = 2b(N) - N/2
    """
    k_bare = central_charge(N) / 6  # = 2b(N)

    # Count fermions by mass
    fermion_masses = [abs(m - (N - 1) / 2) for m in range(N)]
    n_massive = sum(1 for mu in fermion_masses if mu > 1e-10)
    n_massless = sum(1 for mu in fermion_masses if mu < 1e-10)

    # Level shift: -1/2 per Dirac fermion (including massless with PV reg)
    delta_k = -N / 2.0

    k_phys = k_bare + delta_k

    # Check: is k_phys integer or half-integer?
    # For CS quantization: k must be integer (for SU(2)) or half-integer
    # (if there's a gravitational CS term).
    k_phys_mod1 = k_phys % 1
    is_integer = abs(k_phys_mod1) < 1e-10 or abs(k_phys_mod1 - 1) < 1e-10
    is_half_integer = abs(k_phys_mod1 - 0.5) < 1e-10

    # Exact computation using fractions for small N
    # b(N) = N(N+1)/12 - ln2 + ln(N)/(N-1)
    # k_bare = 2b(N) = N(N+1)/6 - 2ln2 + 2ln(N)/(N-1)
    # k_phys = N(N+1)/6 - N/2 - 2ln2 + 2ln(N)/(N-1)
    #        = N(N+1-3)/6 - 2ln2 + 2ln(N)/(N-1)
    #        = N(N-2)/6 - 2ln2 + 2ln(N)/(N-1)
    rational_part = Fraction(N * (N - 2), 6)
    irrational_part = -2 * log(2) + 2 * log(N) / (N - 1)

    return {
        'N': N,
        'k_bare': k_bare,
        'delta_k': delta_k,
        'k_phys': k_phys,
        'k_phys_rational_part': float(rational_part),
        'k_phys_irrational_part': irrational_part,
        'n_massive_fermions': n_massive,
        'n_massless_fermions': n_massless,
        'is_integer': is_integer,
        'is_half_integer': is_half_integer,
        'fermion_masses': fermion_masses,
        'formula': f'k_phys = N(N-2)/6 - 2ln2 + 2lnN/(N-1) = {k_phys:.6f}',
    }


# =====================================================================
# 2. ONE-LOOP COSMOLOGICAL CONSTANT
# =====================================================================

def one_loop_cosmological_constant(N):
    r"""One-loop correction to the cosmological constant.

    The Coleman-Weinberg effective potential in 3D:
      V_1-loop = (1/(4π)) Σ_bosons μ_m³/3 - (1/(4π)) Σ_fermions |μ_m^f|³/3

    In 3D, the one-loop vacuum energy density goes as μ³ (not μ⁴ as in 4D).
    This is UV-finite (no divergence in the sum over KK modes).

    Tree-level: Λ_tree = (N² - 16) / 16
    One-loop: ΔΛ = V_1-loop (finite sum)

    We also compute the ratio ΔΛ/Λ_tree to assess the size of quantum corrections.
    """
    # Boson masses: μ_m = |m - N/2| for m = 0, ..., N-1
    boson_masses = [abs(m - N / 2.0) for m in range(N)]

    # Fermion masses: μ_m^f = |m - (N-1)/2| for m = 0, ..., N-1
    fermion_masses = [abs(m - (N - 1) / 2.0) for m in range(N)]

    # 3D Coleman-Weinberg: V = ±(1/(12π)) Σ |μ|³
    # Sign: + for bosons, - for fermions (opposite to 4D convention in 3D)
    # Actually in 3D: V_eff = -(1/(12π)) [Σ_b μ_b³ - Σ_f |μ_f|³]
    # The sign gives: positive boson contribution LOWERS Λ,
    # positive fermion contribution RAISES Λ.

    sum_boson_cubed = sum(mu**3 for mu in boson_masses)
    sum_fermion_cubed = sum(abs(mu)**3 for mu in fermion_masses)

    # V_1-loop = -(1/(12π)) × (boson - fermion)
    delta_lambda = -(1 / (12 * pi)) * (sum_boson_cubed - sum_fermion_cubed)

    # Tree level
    lambda_tree = (N**2 - 16) / 16.0

    # Also compute the log form (used in the dark sector budget)
    # This is the "Casimir energy" form: (1/2) Σ ln μ²
    sum_boson_log = sum(log(mu**2) for mu in boson_masses if mu > 1e-10)
    sum_fermion_log = sum(log(mu**2) for mu in fermion_masses if mu > 1e-10)
    delta_lambda_log = 0.5 * (sum_boson_log - sum_fermion_log)

    return {
        'N': N,
        'lambda_tree': lambda_tree,
        'delta_lambda_cubic': delta_lambda,
        'delta_lambda_log': delta_lambda_log,
        'ratio_cubic': delta_lambda / lambda_tree if lambda_tree != 0 else float('inf'),
        'ratio_log': delta_lambda_log / lambda_tree if lambda_tree != 0 else float('inf'),
        'sum_boson_cubed': sum_boson_cubed,
        'sum_fermion_cubed': sum_fermion_cubed,
        'boson_minus_fermion': sum_boson_cubed - sum_fermion_cubed,
        'n_bosons': N,
        'n_fermions': N,
        'boson_masses': boson_masses,
        'fermion_masses': fermion_masses,
    }


# =====================================================================
# 3. WEINBERG ANGLE RUNNING
# =====================================================================

def polygon_scale_from_weinberg(sin2_poly=3/11):
    r"""Find the polygon scale M_poly where SM RG running gives sin²θ_W(M_Z) = 0.2312.

    The Weinberg angle runs from sin²(M_poly) = 3/11 at the polygon scale
    down to sin²(M_Z) = 0.2312 via standard SM one-loop RG.

    The SM running uses:
      b_1^SM = (3/5) × 41/10 = 123/50  (U(1)_Y in SM normalization)
      b_2 = -19/6  (SU(2)_L)

    Result: M_poly ≈ 10^7.5 GeV (tree level) or 10^4.7 GeV (with 1-loop CS shift).
    The latter is ~50 TeV — just above LHC reach.
    """
    from math import exp

    alpha_mz = 1 / 128.9
    M_Z = 91.2
    sin2_exp = 0.23122
    b1_SM = (3 / 5) * 41 / 10
    b2 = -19 / 6
    b_em = -80 / 9

    def run_to_MZ(sin2_M, M):
        t = log(M / M_Z)
        if t <= 0:
            return sin2_M
        inv_alpha_M = 1 / alpha_mz - b_em / (2 * pi) * t
        if inv_alpha_M <= 0:
            return None
        alpha_M = 1 / inv_alpha_M
        inv_a1 = (1 - sin2_M) / alpha_M
        inv_a2 = sin2_M / alpha_M
        inv_a1_mz = inv_a1 + b1_SM / (2 * pi) * t
        inv_a2_mz = inv_a2 + b2 / (2 * pi) * t
        if inv_a2_mz <= 0:
            return None
        return inv_a2_mz / (inv_a1_mz + inv_a2_mz)

    # Binary search for M_poly
    lo, hi = M_Z * 1.01, 1e16
    for _ in range(200):
        mid = exp((log(lo) + log(hi)) / 2)
        s = run_to_MZ(sin2_poly, mid)
        if s is None or s < sin2_exp:
            hi = mid
        else:
            lo = mid

    M_poly = exp((log(lo) + log(hi)) / 2)
    sin2_check = run_to_MZ(sin2_poly, M_poly)

    return {
        'sin2_polygon': sin2_poly,
        'M_poly_GeV': M_poly,
        'log10_M': log(M_poly) / log(10),
        'sin2_at_MZ': sin2_check,
        'experimental': sin2_exp,
        'match': abs(sin2_check - sin2_exp) < 1e-4 if sin2_check else False,
    }


def weinberg_angle_running(N_ew=4, N_cosmo=11, ln_ratio=None):
    r"""RG running of sin²θ_W from the polygon scale to low energy.

    Key asymmetry:
      - SU(2) coupling: CS level shifts discretely (k → k - N/2).
        NO continuous running. The shifted conformal dim:
        h̄_SU(2) = j(j+1) / [2(k_eff + h∨)]

      - U(1) coupling: Maxwell kinetic term runs continuously.
        Standard 3D β-function from charged matter loops.

    In the Havelock theory, the β-function for the U(1) coupling α is:
      β_α = (1/(6π)) Σ_m q_m² × μ_m  [3D one-loop]
    where q_m = m (KK charge) and μ_m = |m - N/2| (KK mass).

    The running is POWER-LAW in 3D (not logarithmic as in 4D):
      1/α(μ) = 1/α(Λ) - (1/(6π)) Σ_m q_m² × (Λ - max(μ, μ_m))

    For the Weinberg angle: we need to track how h_U(1) evolves
    relative to h̄_SU(2) as we flow from the polygon scale to the IR.
    """
    from planetary_polygons.extensions.standard_model_gauge import (
        weinberg_angle_cs_threshold, central_charge as cc
    )

    # Tree level at the orbifold point
    tree = weinberg_angle_cs_threshold()
    sin2_tree = tree['sin2_theta_W']  # = 3/11

    # CS level shift at the electroweak polygon N=4
    cs = cs_level_shift(N_ew)
    k_bare = cs['k_bare']
    k_phys = cs['k_phys']

    # Shifted SU(2) conformal dimension
    h_dual_su2 = 2
    j = 1
    h_SU2_shifted = j * (j + 1) / (k_phys + h_dual_su2) / 2  # physical = WZW/2

    # U(1) conformal dimension (unchanged at tree level)
    Q = 0.5
    K = 1
    h_U1 = Q**2 / (2 * K)

    # Weinberg angle with CS-shifted SU(2) level
    sin2_shifted = h_U1 / (h_U1 + h_SU2_shifted)

    # U(1) running: in 3D, the U(1) coupling runs as power law.
    # The one-loop correction to 1/α from integrating out KK mode m:
    # Δ(1/α) = q_m² × μ_m / (6π)
    # At the electroweak scale, heavy KK modes (μ >> M_W) are integrated out.
    boson_masses = [abs(m - N_ew / 2.0) for m in range(N_ew)]
    delta_inv_alpha = sum(
        m**2 * mu / (6 * pi)
        for m, mu in enumerate(boson_masses)
        if mu > 0.01
    )

    c = cc(N_ew)
    alpha_tree = 6 / (pi * c)
    inv_alpha_tree = 1 / alpha_tree
    inv_alpha_shifted = inv_alpha_tree + delta_inv_alpha

    # Effective h_U1 with running
    # h_U1_eff = Q² / (2 K_eff) where K_eff accounts for the running
    K_eff = K * (inv_alpha_shifted / inv_alpha_tree)
    h_U1_eff = Q**2 / (2 * K_eff)

    sin2_running = h_U1_eff / (h_U1_eff + h_SU2_shifted)

    return {
        'sin2_tree': sin2_tree,
        'sin2_cs_shifted': sin2_shifted,
        'sin2_running': sin2_running,
        'k_bare': k_bare,
        'k_phys': k_phys,
        'h_SU2_shifted': h_SU2_shifted,
        'h_U1': h_U1,
        'h_U1_eff': h_U1_eff,
        'K_eff': K_eff,
        'delta_inv_alpha': delta_inv_alpha,
        'experimental': 0.23122,
    }


# =====================================================================
# 4. FERMION MASS CORRECTIONS
# =====================================================================

def fermion_self_energy_cs(N=7):
    r"""One-loop fermion self-energy from CS gauge exchange in 3D.

    In 3D CS + fermion theory, the one-loop self-energy is:
      Σ(p) = (1/k) × (finite integral)

    The CS propagator in Landau gauge:
      D_μν(q) = (1/k) ε_μνρ q^ρ / q²

    The one-loop fermion self-energy:
      Σ(p) = ∫ d³q/(2π)³ γ^μ S(p-q) γ^ν D_μν(q)

    For a fermion of mass m at external momentum p = 0:
      Σ(0) = -m/(4πk) × [parity-even mass shift]
            + 1/(4πk) × [parity-odd anomalous magnetic moment]

    The MASS SHIFT at one loop:
      δm/m = -1/(4πk) = -1/(4π × 2b(N))

    This is the leading quantum correction to the fermion masses.
    """
    k = central_charge(N) / 6  # CS level

    # Fermion KK masses at N=7
    fermion_masses = [abs(m - (N - 1) / 2) for m in range(N)]
    pairs = [(m, N - m) for m in range(1, (N + 1) // 2)]

    results = []
    for m1, m2 in pairs:
        mu = fermion_masses[m1]
        # One-loop mass correction: δμ/μ = -1/(4πk)
        delta_mu_over_mu = -1 / (4 * pi * k)
        mu_corrected = mu * (1 + delta_mu_over_mu)

        results.append({
            'pair': (m1, m2),
            'mu_tree': mu,
            'delta_mu_over_mu': delta_mu_over_mu,
            'mu_corrected': mu_corrected,
        })

    # Tree-level mass ratio
    tree_ratio = results[0]['mu_tree'] / results[1]['mu_tree'] if len(results) > 1 and results[1]['mu_tree'] > 0 else float('inf')
    corrected_ratio = results[0]['mu_corrected'] / results[1]['mu_corrected'] if len(results) > 1 and results[1]['mu_corrected'] > 0 else float('inf')

    return {
        'N': N,
        'k': k,
        'delta_m_over_m': -1 / (4 * pi * k),
        'pairs': results,
        'tree_ratio_12': tree_ratio,
        'corrected_ratio_12': corrected_ratio,
        'ratio_shift_pct': abs(corrected_ratio - tree_ratio) / tree_ratio * 100 if tree_ratio > 0 else 0,
        'comment': 'One-loop mass shift is universal (-1/(4πk)), so ratios are unchanged at this order.',
    }


# =====================================================================
# SUMMARY: ALL LOOP CORRECTIONS
# =====================================================================

def all_loop_corrections(N=7):
    """Compute all one-loop corrections at polygon number N."""
    cs = cs_level_shift(N)
    cc = one_loop_cosmological_constant(N)
    ferm = fermion_self_energy_cs(N)

    return {
        'N': N,
        'cs_level_shift': cs,
        'cosmological_constant': cc,
        'fermion_masses': ferm,
    }
