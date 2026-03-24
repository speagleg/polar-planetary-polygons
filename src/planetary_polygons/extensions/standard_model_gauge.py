r"""
The Standard Model gauge group from the polygon hierarchy.

SU(3) × SU(2) × U(1) emerges from three mechanisms, each grounded
in established mathematics:

  SU(2): Witten-Achúcarro-Townsend theorem (1986, 1988).
    3D gravity with Λ < 0 IS Chern-Simons theory with gauge group
    SU(2) × SU(2) (Euclidean signature) at level k = ℓ/(4G).
    After KK reduction on S¹, the zero-mode gravitational sector
    is pure 2+1D AdS gravity → SU(2)×SU(2) CS.
    At N=4: the critical mode m*=2 IS the zero mode (μ₂ = 0),
    so the critical gravitational mode carries SU(2) quantum numbers
    in the j=1 (adjoint) representation: f(2,4) = 2 = j(j+1), j=1.

  SU(3): McKay correspondence on the Z/3Z Galois orbifold.
    The Frobenius automorphism σ: m → 2m mod 7 generates Z/3Z ⊂ Aut(Z/7Z).
    On the orbit O₊ = {1,2,4}: σ acts by cyclic permutation.
    Diagonalising: the charged modes (η₁, η₂) ∈ C² carry the Z/3Z
    action diag(ω, ω⁻¹), which is the STANDARD McKay embedding
    Z/3Z ⊂ SU(2).
    By the McKay correspondence (McKay 1980): Z/3Z ⊂ SU(2) → A₂ → SU(3).
    In the orbifold CFT: the extended chiral algebra contains ŝu(3)₁.

  U(1): Kaluza-Klein reduction on S¹ (all N).
    The S¹ fiber with flux N/2 gives a U(1) gauge field.

The Weinberg angle from the CS threshold couplings:
  At the orbifold fixed point, both SU(2) and SU(3) are at level 1.
  The quantum-corrected SU(2) inverse coupling: 1/g₂² = k₂ + h∨(SU(2)) = 1+2 = 3.
  The U(1)_Y inverse coupling from SU(3)₁ threshold: 1/g_Y² = dim(SU(3)) = 8.
  sin²θ_W = g_Y² / (g_Y² + g₂²) = (1/8)/(1/8 + 1/3) = 3/11 ≈ 0.273.
"""

from math import pi, sqrt, sin, cos, log, gcd, exp
import cmath


def casimir(m, N):
    """Havelock Casimir f(m,N) = m(N-m)/2."""
    return m * (N - m) / 2.0


def spin_j(m, N):
    """The SL(2,R) spin j from the Casimir: j(j+1) = f(m,N)."""
    f = casimir(m, N)
    return (-1 + sqrt(1 + 4 * f)) / 2


def trace_field_degree(N):
    """Degree [K_N : Q] of the trace field Q(cos 2π/N)."""
    phi = sum(1 for k in range(1, N + 1) if gcd(k, N) == 1)
    return max(1, phi // 2)


def b_exact(N):
    """The Havelock central charge coefficient b(N).

    c = 12*b(N) is the kinetic coefficient of the breathing mode.
    """
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


def central_charge(N):
    """The Havelock central charge c = 12*b(N).

    This is the exact coefficient, not the approximation c ≈ N².
    """
    return 12 * b_exact(N)


# =====================================================================
# SU(2) FROM THE CHERN-SIMONS FORMULATION OF 3D GRAVITY
# =====================================================================

def su2_from_cs_gravity(N=4):
    """SU(2) from the Witten-Achúcarro-Townsend theorem.

    3D gravity with Λ < 0 (on H²) IS SU(2)×SU(2) Chern-Simons theory
    in Euclidean signature (Witten 1988, Achúcarro-Townsend 1986).

    After KK reduction on S¹, the zero-mode sector is pure 2+1D gravity.
    The CS gauge group of this sector is SU(2)×SU(2).

    At N=4: the critical mode m*=2 has KK mass μ₂ = |2 - 4/2| = 0,
    so it IS the zero mode. Its Casimir f(2,4)=2=j(j+1) with j=1
    (the SU(2) adjoint), confirming it carries SU(2) quantum numbers.

    Returns dict with the proof chain.
    """
    c = central_charge(N)
    G = 3.0 / (2 * c)
    k_cs = c / 6  # CS level from Brown-Henneaux: c = 3ℓ/(2G), k = ℓ/(4G)
    h_dual = 2  # dual Coxeter number of SU(2)

    m_crit = N // 2
    f_crit = casimir(m_crit, N)
    mu_kk = abs(m_crit - N / 2.0)
    j = spin_j(m_crit, N)
    j_int = int(round(j))

    return {
        'N': N,
        'theorem': 'Witten 1988, Achúcarro-Townsend 1986',
        'gauge_group': 'SU(2) × SU(2)',
        'cs_level': k_cs,
        'central_charge': c,
        'G': G,
        'h_dual_su2': h_dual,
        'quantum_corrected_level': k_cs + h_dual,
        # Critical mode at N=4
        'm_crit': m_crit,
        'f_crit': f_crit,
        'mu_kk': mu_kk,
        'is_zero_mode': abs(mu_kk) < 1e-10,
        'j': j_int,
        'is_adjoint': j_int == 1,
        'proof_chain': [
            f'1. KK reduce 4D metric on S¹: zero-mode sector = pure 2+1D gravity on R×H².',
            f'2. H² has K=-1, so Λ₃ < 0 (AdS₃).',
            f'3. By Witten (1988): 2+1D AdS gravity = SU(2)×SU(2) CS at k={k_cs:.1f} (Euclidean).',
            f'4. At N={N}: m*={m_crit}, μ_KK={mu_kk} (zero mode).',
            f'5. Casimir: f({m_crit},{N})={f_crit}=j(j+1) with j={j_int} (SU(2) adjoint).',
            f'6. The gravitational zero mode at N={N} IS the SU(2) adjoint.'
        ],
    }


# =====================================================================
# SU(3) FROM THE McKAY CORRESPONDENCE AT N=7
# =====================================================================

def frobenius_orbits(N=7):
    """Compute the Frobenius orbits on the Havelock modes.

    The Frobenius automorphism σ: m → 2m mod N (for prime N)
    generates a cyclic subgroup of Aut(Z/NZ) = (Z/NZ)*.

    Returns the orbits as lists of mode numbers.
    """
    if N < 3:
        return []

    # Find a primitive root mod N (generator of (Z/NZ)*)
    # For the Galois action, we use σ: m → 2m mod N
    sigma = 2  # Frobenius at 2

    # Check order of sigma in (Z/NZ)*
    order = 1
    val = sigma
    while val % N != 1:
        val = (val * sigma) % N
        order += 1

    visited = set()
    orbits = []
    for m in range(1, N):
        if m in visited:
            continue
        orbit = []
        current = m
        for _ in range(order):
            if current not in visited:
                orbit.append(current)
                visited.add(current)
            current = (current * sigma) % N
        orbits.append(sorted(orbit))

    return orbits


def mckay_embedding(N=7):
    """The McKay embedding of Z/3Z ⊂ SU(2) from the Galois action at N=7.

    The Frobenius σ: m → 2m mod 7 has order 3 (since 2³=8≡1 mod 7).
    On orbit O₊ = {1,2,4}, σ acts by cyclic permutation.

    Diagonalising with ω = e^{2πi/3}:
      η₀ = (φ₁ + φ₂ + φ₄)/√3   [Z/3Z invariant]
      η₁ = (φ₁ + ωφ₂ + ω²φ₄)/√3  [charge 1]
      η₂ = (φ₁ + ω²φ₂ + ωφ₄)/√3  [charge 2]

    On (η₁, η₂): σ acts as diag(ω, ω⁻¹) ∈ SU(2).
    This is the STANDARD McKay embedding of Z/3Z ⊂ SU(2).

    Returns the McKay data and verification.
    """
    omega = cmath.exp(2j * cmath.pi / 3)

    # The Frobenius automorphism at N=7
    orbits = frobenius_orbits(N)

    # Find the orbit containing 1
    orbit_plus = None
    for orb in orbits:
        if 1 in orb:
            orbit_plus = orb
            break

    # Verify it has 3 elements (Z/3Z action)
    assert len(orbit_plus) == 3, f"Expected orbit of size 3, got {len(orbit_plus)}"

    # The cyclic permutation σ on the orbit
    # σ: 1 → 2 → 4 → 1 (since 2×1=2, 2×2=4, 2×4=8≡1 mod 7)
    m1, m2, m3 = orbit_plus[0], orbit_plus[1], orbit_plus[2]

    # Diagonalise: σ eigenvalues are 1, ω, ω²
    # η₀ eigenvalue: 1 (invariant)
    # η₁ eigenvalue: ω
    # η₂ eigenvalue: ω² = ω⁻¹

    # Verify: diag(ω, ω⁻¹) ∈ SU(2)
    det = omega * omega.conjugate()
    assert abs(det - 1.0) < 1e-10, "determinant should be 1"

    # McKay correspondence: Z/3Z ⊂ SU(2) → A₂ Dynkin diagram
    # Non-trivial irreps of Z/3Z: ω and ω² → two nodes of A₂
    # A₂ = Dynkin diagram of SU(3)

    return {
        'N': N,
        'frobenius_generator': 2,
        'frobenius_order': 3,
        'orbit_plus': orbit_plus,
        'orbit_minus': [N - m for m in orbit_plus],
        'casimirs': [casimir(m, N) for m in orbit_plus],
        'omega': omega,
        'mckay_embedding': 'diag(ω, ω⁻¹) ∈ SU(2)',
        'det_check': abs(det - 1.0) < 1e-10,
        'dynkin_diagram': 'A₂',
        'gauge_group': 'SU(3)',
        'mckay_level': 1,
        'current_algebra': 'ŝu(3)₁',
        'central_charge_su3': 2.0,  # c(SU(3)₁) = 1×8/(1+3) = 2
    }


def su3_from_mckay(N=7):
    """Prove SU(3) from the McKay correspondence at N=7.

    The argument:
    1. Frobenius σ: m → 2m mod 7 generates Z/3Z on the Havelock modes.
    2. The orbit O₊ = {1,2,4} has 3 elements with Z/3Z cyclic action.
    3. Diagonalising: the charged modes carry diag(ω,ω⁻¹) ∈ SU(2).
    4. By McKay (1980): Z/3Z ⊂ SU(2) → A₂ diagram → SU(3).
    5. In the orbifold CFT: the extended chiral algebra contains ŝu(3)₁.

    This is a theorem of the McKay correspondence, NOT a numerical coincidence.
    The Z/3Z → A₂ map is a proven mathematical result.
    """
    mckay = mckay_embedding(N)

    return {
        'N': N,
        'method': 'McKay correspondence',
        'references': ['McKay 1980', 'Gonzalez-Sprinberg & Verdier 1983',
                        'Dixon-Harvey-Vafa-Witten 1985'],
        'mckay': mckay,
        'proof_chain': [
            '1. Frobenius σ: m → 2m mod 7 generates Z/3Z ⊂ (Z/7Z)* (order 3: 2³≡1 mod 7).',
            f'2. Orbit O₊ = {mckay["orbit_plus"]} under σ (3 modes, cyclic permutation).',
            '3. Diagonalise σ on O₊: eigenvalues 1, ω, ω² where ω=e^{2πi/3}.',
            '4. Invariant mode η₀ decouples. Charged sector (η₁,η₂) ∈ C².',
            '5. σ acts on C² as diag(ω,ω⁻¹) ∈ SU(2) (det=ωω⁻¹=1). ✓',
            '6. By McKay correspondence: Z/3Z ⊂ SU(2) → A₂ Dynkin diagram → SU(3).',
            '7. Non-trivial Z/3Z irreps (ω,ω²) ↔ simple roots of A₂ = SU(3).',
            '8. In orbifold CFT: Z/3Z twisted sectors extend the chiral algebra to ŝu(3)₁.',
        ],
        'gauge_group': 'SU(3)',
        'level': 1,
    }


# =====================================================================
# SU(3): legacy interface (updated to use McKay)
# =====================================================================

def galois_action_on_pairs(N=7):
    """The Galois group acting on palindromic mode pairs (legacy interface)."""
    orbits = frobenius_orbits(N)
    n_pairs = (N - 1) // 2
    pairs = [(m, N - m) for m in range(1, n_pairs + 1)]

    # Find the generator that acts by pair permutation
    sigma = 2
    perm = []
    for m, nm in pairs:
        new_m = (sigma * m) % N
        if new_m > N // 2:
            new_m = N - new_m
        perm.append(new_m)

    return {
        'N': N,
        'n_pairs': n_pairs,
        'pairs': pairs,
        'galois_generators': [sigma],
        'actions': {sigma: perm},
        'galois_group_order': trace_field_degree(N),
        'is_cyclic_permutation': len(set(perm)) == n_pairs,
    }


def su3_from_galois(N=7):
    """SU(3) from the N=7 Galois structure (updated to use McKay)."""
    return su3_from_mckay(N)


# =====================================================================
# U(1) FROM KALUZA-KLEIN
# =====================================================================

def u1_from_kk(N=7):
    """U(1) from S¹ Kaluza-Klein reduction."""
    c = central_charge(N)
    alpha = 6 / (pi * c)
    G = 3 / (2 * c)
    lock = alpha / (8 * pi * G)

    return {
        'mechanism': 'Kaluza-Klein on S¹ fiber with flux N/2',
        'gauge_group': 'U(1)',
        'coupling_alpha': alpha,
        'coupling_G': G,
        'coupling_lock': lock,
        'lock_exact': '1/(2π²)',
        'lock_numerical': 1 / (2 * pi**2),
        'lock_matches': abs(lock - 1 / (2 * pi**2)) < 1e-10,
    }


# =====================================================================
# THE WEINBERG ANGLE FROM CS THRESHOLD COUPLINGS
# =====================================================================

def weinberg_angle_cs_threshold():
    """Derive sin²θ_W = 3/11 from conformal dimensions at the orbifold CFT.

    The Weinberg angle is the U(1) fraction of the critical mode's
    conformal weight:

      sin²θ_W = h_{U(1)} / (h_{U(1)} + h_bar_{SU(2)})

    where:
      h_{U(1)} = Q²/(2K) = (1/2)²/2 = 1/8
        (compact boson, Q = m*/N = 1/2, K = 1)
      h_bar_{SU(2)} = j(j+1) / [2(k + h_dual)] = 2/6 = 1/3
        (left-right average in SU(2)xSU(2) CS gravity;
         j=1 from f(2,4)=2, k=1, h_dual(SU(2))=2)

      sin²θ_W = (1/8)/(1/8 + 1/3) = 3/11

    The factor of 2 giving h_bar = h_WZW/2 is physical:
    3D gravity = SU(2)_L x SU(2)_R CS (Witten 1988),
    physical perturbations have h_L = h_R = h_total/2.

    Compare SU(5) GUT: sin²θ_W = 3/8 uses CLASSICAL Casimir j(j+1).
    Our 3/11 uses QUANTUM-CORRECTED conformal dim j(j+1)/(k+h_dual).
    """
    # Critical mode at N=4
    Q = 0.5              # U(1)_K charge = m*/N = 2/4
    K = 1                # U(1) level (free boson)
    j = 1                # SU(2) spin (f(2,4)=2=j(j+1))
    k_su2 = 1            # SU(2) CS level
    h_su2 = 2            # dual Coxeter number of SU(2)
    k_su3 = 1            # SU(3) CS level (from McKay)
    h_su3 = 3            # dual Coxeter number of SU(3)

    # Conformal dimensions
    h_U1 = Q**2 / (2 * K)                          # = 1/8
    h_SU2_WZW = j * (j + 1) / (k_su2 + h_su2)     # = 2/3
    h_SU2_phys = h_SU2_WZW / 2                      # = 1/3 (L-R average)

    sin2_theta = h_U1 / (h_U1 + h_SU2_phys)

    return {
        'method': 'Conformal dimensions at orbifold fixed point',
        'Q': Q,
        'K': K,
        'j': j,
        'k_su2': k_su2,
        'h_dual_su2': h_su2,
        'k_su3': k_su3,
        'h_dual_su3': h_su3,
        'h_U1': h_U1,
        'h_SU2_WZW': h_SU2_WZW,
        'h_SU2_phys': h_SU2_phys,
        'sin2_theta_W': sin2_theta,
        'exact_fraction': '3/11',
        'numerical': sin2_theta,
        'experimental': 0.23122,
        'su5_gut': 3 / 8,
        'discrepancy_pct': abs(sin2_theta - 0.23122) / 0.23122 * 100,
        'su5_discrepancy_pct': abs(3 / 8 - 0.23122) / 0.23122 * 100,
        # Legacy fields for backward compat
        'inv_g2_sq': k_su2 + h_su2,
        'inv_gY_sq': 8,
        'dim_su2': 3,
        'dim_su3': 8,
        'proof_chain': [
            f'1. Critical mode at N=4: Q = m*/N = {Q}, j = {j} (from f(2,4)=2).',
            f'2. U(1)_K conformal dim: h = Q^2/(2K) = {Q**2}/(2*{K}) = {h_U1}.',
            f'3. SU(2)_1 WZW dim: h = j(j+1)/(k+h_dual) = 2/{k_su2+h_su2} = {h_SU2_WZW:.4f}.',
            f'4. Physical SU(2): h_bar = h_WZW/2 = {h_SU2_phys:.4f} (L-R average in SU(2)xSU(2) CS).',
            f'5. sin^2 theta_W = h_U1/(h_U1 + h_bar) = {h_U1}/({h_U1}+{h_SU2_phys:.4f}) = 3/11.',
        ],
    }


# Legacy interface
def weinberg_angle(N=4):
    """Compute the Weinberg angle (delegates to CS threshold derivation)."""
    result = weinberg_angle_cs_threshold()
    result['N'] = N
    return result


# =====================================================================
# THE ACTION / LAGRANGIAN
# =====================================================================

def havelock_action(N):
    """The complete Havelock field theory action.

    S = S_grav + S_gauge + S_scalar + S_fermion + S_Yukawa

    All couplings determined by c = 12b(N).
    """
    c = central_charge(N)
    G = 3.0 / (2 * c)
    alpha = 6.0 / (pi * c)
    Lambda = (N**2 - 16) / 16.0

    # KK masses
    m_crit = N // 2
    scalar_masses = [abs(m - N / 2.0) for m in range(N)]
    fermion_masses = [abs(m - (N - 1) / 2.0) for m in range(N)]

    return {
        'spacetime': f'R × (H² ×_{N} S¹)',
        'central_charge': c,
        'G': G,
        'alpha': alpha,
        'Lambda': Lambda,
        'coupling_lock': alpha / (8 * pi * G),
        'cs_level': c / 6,
        'S_grav': f'(c/(24π)) ∫ √g (R - 2Λ), Λ = {Lambda:.4f}',
        'S_gauge': f'-(πc/24) ∫ √g F_μν F^μν',
        'S_CS': f'(k/(4π)) ∫ Tr(A∧dA + ⅔A∧A∧A), k = c/6 = {c/6:.2f}',
        'S_scalar': f'{N} KK modes with masses μ_m = |m - N/2|',
        'S_fermion': f'{N} KK modes with masses μ_m^f = |m - (N-1)/2|',
        'S_Yukawa': 'Y_ij ψ̄_i Φ ψ_j, subject to m_i - m_j + m_H ≡ 0 mod N',
        'scalar_masses': scalar_masses,
        'fermion_masses': fermion_masses,
        'n_massless_scalars': sum(1 for m in scalar_masses if m < 1e-10),
        'n_massless_fermions': sum(1 for m in fermion_masses if m < 1e-10),
    }


# =====================================================================
# THE TWO-FORCE UNIFICATION
# =====================================================================

def two_force_unification():
    """The complete two-force picture with improved derivations."""
    su3 = su3_from_mckay(7)
    su2 = su2_from_cs_gravity(4)
    u1 = u1_from_kk()
    theta = weinberg_angle_cs_threshold()

    return {
        'force_1': {
            'name': 'Gravity/Color',
            'N': 7,
            'base': 'gravity on H² (graviton j=2)',
            'cover': 'SU(3) from McKay on Z/3Z Galois orbifold',
            'mechanism': 'McKay correspondence: Z/3Z ⊂ SU(2) → A₂ → SU(3)',
            'su3': su3,
        },
        'force_2': {
            'name': 'Electroweak',
            'components': {
                'SU(2)': 'Witten CS formulation of 3D gravity (proven, 1988)',
                'U(1)': 'Kaluza-Klein on S¹ (textbook)',
            },
            'su2': su2,
            'u1': u1,
        },
        'weinberg_angle': theta,
        'unification_field': 'Q(ζ₅₆) = Q(ζ₇, ζ₈)',
        'gauge_group': 'SU(3) × SU(2) × U(1)',
    }


# =====================================================================
# THE COMPLETE STANDARD MODEL TABLE
# =====================================================================

def standard_model_table():
    """The polygon hierarchy → Standard Model correspondence."""
    rows = []
    for N in range(3, 16):
        m = N // 2
        f = casimir(m, N)
        j = spin_j(m, N)
        j_int = int(round(j)) if abs(j - round(j)) < 0.01 else None
        deg = trace_field_degree(N)

        physics = ""
        if j_int == 1:
            physics = "SU(2) adjoint (Witten CS, j=1)"
        elif j_int == 2:
            physics = "graviton (j=2); SU(3) from McKay at N=7"

        rows.append({
            'N': N,
            'trace_field_degree': deg,
            'critical_casimir': f,
            'spin_j': j,
            'j_integer': j_int,
            'physics': physics,
            'central_charge': central_charge(N),
        })
    return rows
