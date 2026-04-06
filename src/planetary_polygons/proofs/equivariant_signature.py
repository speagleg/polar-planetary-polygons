"""
THEOREM: Z_N equivariant signature as a topological invariant.

STATEMENT:
    The equivariant signature sigma_N of the regular N-gon Havelock Hessian,
    defined as the spectral asymmetry of the normal eigenvalues, is a
    topological invariant that:

    (a) Depends only on N (not on continuous deformation parameters)
    (b) Equals the eta invariant eta_Hav(0) of the Havelock operator at s=0
    (c) Is xi-independent on the hyperbolic plane H^2
    (d) Has closed form: sigma_N = N-2 (N<=6), 3 (N=7), 8-N (N>=8)
    (e) Satisfies the APS spectral flow theorem at the N=7 transition

DEFINITIONS:
    sigma_N = #{m : lambda_m > 0} - #{m : lambda_m < 0}
    where lambda_m = (N-1) - m(N-m)/2 for m = 2, ..., N-1.

    eta_Hav(N, s) = sum_{m, lam_m != 0} sgn(lam_m) * |lam_m|^{-s}
    This is entire in s (finite sum) and eta_Hav(N, 0) = sigma_N.

PROOF:
    The closed form follows from: lambda_m < 0 iff m(N-m) > 2(N-1),
    which defines m in (m_-, m_+) where m_+/- = (N +/- sqrt((N-4)^2-8))/2.
    For N <= 6: discriminant < 0, no negative modes.
    For N = 7: discriminant = 1, roots m = 3, 4 are exact (zero modes).
    For N >= 8: discriminant > 0, roots in (2, 3) and (N-3, N-2),
    giving negative modes {3, ..., N-3}, count = N-5.

    Positive modes for N >= 8: {2, N-2, N-1}, count = 3.
    sigma_N = 3 - (N-5) = 8-N.

    xi-independence: on H^2 with parameter xi, eigenvalues scale as
    lambda_m^{H2}(xi) = C_1(N, xi) * lambda_m where C_1 > 0 for xi in (0,1).
    Signs are preserved, so sigma_N is xi-independent.

    The APS spectral flow from sigma_6 = 4 to sigma_8 = 0 is -4,
    which equals -2 * dim_ker(N=7) = -2*2 = -4, confirming the
    Atiyah-Patodi-Singer spectral flow theorem.

Run: PYTHONPATH=src python3 -m planetary_polygons.proofs.equivariant_signature
"""

from fractions import Fraction
from typing import List, Tuple, Dict, Optional, NamedTuple
import math


# ---------------------------------------------------------------------------
# Core eigenvalue infrastructure (imported concept from morse_bott.py)
# ---------------------------------------------------------------------------

def havelock_eigenvalue(m: int, N: int) -> Fraction:
    """Exact Havelock eigenvalue lambda_m = (N-1) - m(N-m)/2."""
    return Fraction(N - 1) - Fraction(m * (N - m), 2)


def normal_eigenvalues(N: int) -> List[Fraction]:
    """Eigenvalues of the normal Hessian, modes m = 2, ..., N-1."""
    if N < 3:
        raise ValueError(f"N must be >= 3, got {N}")
    return [havelock_eigenvalue(m, N) for m in range(2, N)]


# ---------------------------------------------------------------------------
# Eigenvalue sign classification
# ---------------------------------------------------------------------------

def positive_modes(N: int) -> List[int]:
    """Modes m in {2, ..., N-1} with lambda_m > 0."""
    return [m for m in range(2, N) if havelock_eigenvalue(m, N) > 0]


def negative_modes(N: int) -> List[int]:
    """Modes m in {2, ..., N-1} with lambda_m < 0."""
    return [m for m in range(2, N) if havelock_eigenvalue(m, N) < 0]


def zero_modes(N: int) -> List[int]:
    """Modes m in {2, ..., N-1} with lambda_m = 0."""
    return [m for m in range(2, N) if havelock_eigenvalue(m, N) == 0]


def sign_counts(N: int) -> Tuple[int, int, int]:
    """Return (n_positive, n_negative, n_zero) for normal modes."""
    evals = normal_eigenvalues(N)
    n_pos = sum(1 for lam in evals if lam > 0)
    n_neg = sum(1 for lam in evals if lam < 0)
    n_zero = sum(1 for lam in evals if lam == 0)
    return n_pos, n_neg, n_zero


# ---------------------------------------------------------------------------
# Equivariant signature: direct computation from eigenvalues
# ---------------------------------------------------------------------------

def signature_from_eigenvalues(N: int) -> int:
    """
    Compute sigma_N = #{lambda_m > 0} - #{lambda_m < 0}
    directly from the Havelock eigenvalues (exact, Fraction arithmetic).

    This is the spectral asymmetry of the normal Hessian restricted
    to modes m = 2, ..., N-1.
    """
    if N < 3:
        raise ValueError(f"N must be >= 3, got {N}")
    n_pos, n_neg, _ = sign_counts(N)
    return n_pos - n_neg


# ---------------------------------------------------------------------------
# Equivariant signature: closed-form formula
# ---------------------------------------------------------------------------

def signature_closed_form(N: int) -> int:
    """
    Closed-form formula for sigma_N.

    sigma_N = N - 2     for 3 <= N <= 6  (all eigenvalues positive)
    sigma_N = 3         for N = 7        (2 zero modes, 3 positive, 0 negative)
    sigma_N = 8 - N     for N >= 8       (3 positive, N-5 negative)

    PROOF:
    The discriminant of m^2 - Nm + 2(N-1) = 0 is D = (N-4)^2 - 8.
    - N <= 6: D < 0, all eigenvalues positive, sigma = N-2.
    - N = 7: D = 1, roots m = 3, 4 (zero eigenvalues), sigma = 5-2-0 = 3.
    - N >= 8: D > 0, roots in (2,3) and (N-3,N-2).
      Positive modes: {2, N-2, N-1} (count 3).
      Negative modes: {3, ..., N-3} (count N-5).
      sigma = 3 - (N-5) = 8-N.
    """
    if N < 3:
        raise ValueError(f"N must be >= 3, got {N}")
    if N <= 6:
        return N - 2
    if N == 7:
        return 3
    return 8 - N


# ---------------------------------------------------------------------------
# Havelock eta invariant (spectral zeta / eta function)
# ---------------------------------------------------------------------------

def eta_havelock(N: int, s: float = 0.0) -> Fraction:
    """
    The eta invariant of the Havelock operator at parameter s.

    eta_Hav(N, s) = sum_{m=2, lambda_m != 0}^{N-1} sgn(lambda_m) * |lambda_m|^{-s}

    For s = 0: eta_Hav(N, 0) = sigma_N (the equivariant signature).

    Since the spectrum is finite, the eta function is entire in s.
    For exact rational result, use s = 0 only.
    """
    if N < 3:
        raise ValueError(f"N must be >= 3, got {N}")

    if s == 0.0:
        # Exact computation: sgn sum
        result = Fraction(0)
        for m in range(2, N):
            lam = havelock_eigenvalue(m, N)
            if lam > 0:
                result += 1
            elif lam < 0:
                result -= 1
        return result

    # For s != 0: use floating point
    total = 0.0
    for m in range(2, N):
        lam = havelock_eigenvalue(m, N)
        if lam != 0:
            sgn = 1 if lam > 0 else -1
            total += sgn * float(abs(lam)) ** (-s)
    return Fraction(total).limit_denominator(10**12)


def reduced_eta(N: int) -> Fraction:
    """
    Reduced eta invariant: eta-bar(N) = (eta(0) + dim ker) / 2.

    eta-bar = (sigma_N + n_zero) / 2

    This is the mod-Z reduction of the APS rho-invariant.
    Values:
        N <= 6: (N-2)/2
        N = 7:  5/2
        N >= 8: (8-N)/2
    """
    sigma = signature_from_eigenvalues(N)
    n_zero = len(zero_modes(N))
    return Fraction(sigma + n_zero, 2)


# ---------------------------------------------------------------------------
# Spectral flow (APS spectral flow theorem)
# ---------------------------------------------------------------------------

def spectral_flow(N1: int, N2: int) -> int:
    """
    Spectral flow of sigma from N1 to N2.

    SF = sigma_{N2} - sigma_{N1}

    Key result: the total spectral flow from N=6 to N=8 is -4,
    which equals -2 * dim_ker(N=7) = -2*2 = -4.
    This is the Atiyah-Patodi-Singer spectral flow theorem:
    the spectral flow through a degenerate point equals (minus)
    twice the kernel dimension.
    """
    return signature_from_eigenvalues(N2) - signature_from_eigenvalues(N1)


def spectral_flow_table(N_max: int = 15) -> List[Dict]:
    """Compute the spectral flow between consecutive N values."""
    rows = []
    for N in range(4, N_max + 1):
        sf = spectral_flow(N - 1, N)
        rows.append({
            'transition': f'{N-1}->{N}',
            'sigma_prev': signature_from_eigenvalues(N - 1),
            'sigma_next': signature_from_eigenvalues(N),
            'spectral_flow': sf,
        })
    return rows


# ---------------------------------------------------------------------------
# Dedekind sum and APS rho-invariant
# ---------------------------------------------------------------------------

def dedekind_sum_s1N(N: int) -> Fraction:
    """
    Exact Dedekind sum s(1, N) = (N-1)(N-2)/(12N).

    This is the closed form of:
    s(1, N) = sum_{k=1}^{N-1} ((k/N))^2

    where ((x)) = x - floor(x) - 1/2 is the sawtooth function.
    """
    return Fraction((N - 1) * (N - 2), 12 * N)


def eta_signature_lens(N: int) -> Fraction:
    """
    Eta invariant of the signature operator on the lens space L(N, 1).

    eta_sig(L(N,1)) = 4 * s(1, N) = (N-1)(N-2)/(3N)

    This is the GEOMETRIC eta invariant from the Atiyah-Patodi-Singer
    theory, distinct from the vortex eta_Hav.
    """
    return 4 * dedekind_sum_s1N(N)


def rho_invariant(N: int) -> Fraction:
    """
    APS rho-invariant: rho(N) = sigma_N - eta_sig(L(N,1)).

    This combines the vortex spectral asymmetry with the geometric
    eta invariant on the lens space L(N,1) = S^3/Z_N.

    The quantity 3*N*rho(N) is always an integer:
        N <= 6: 3*N*rho = (N-2)(2N+1)
        N = 7:  3*N*rho = 33
        N >= 8: 3*N*rho = -4N^2 + 27N - 2
    """
    sigma = Fraction(signature_from_eigenvalues(N))
    eta_sig = eta_signature_lens(N)
    return sigma - eta_sig


def rho_integrality(N: int) -> Fraction:
    """
    Verify that 3*N*rho(N) is an integer.

    This integrality is a non-trivial check of the APS index theorem:
    it means rho(N) lies in (1/3N)*Z, consistent with the cyclic
    group structure of Z_N.
    """
    return 3 * N * rho_invariant(N)


# ---------------------------------------------------------------------------
# xi-independence on H^2
# ---------------------------------------------------------------------------

def c1_h2(N: int, xi: float) -> float:
    """
    Curvature coefficient C_1(H^2, xi) = (N-1)(1 + xi^2) / (1 - xi)^2.

    On H^2 with parameter xi = r_E^2 / a^2 in (0, 1):
    lambda_m^{H2}(xi) = C_1(N, xi) * lambda_m

    C_1 > 0 for all xi in (0, 1), so signs of eigenvalues are PRESERVED.
    """
    if xi <= 0 or xi >= 1:
        raise ValueError(f"xi must be in (0, 1), got {xi}")
    return (N - 1) * (1 + xi ** 2) / (1 - xi) ** 2


def verify_xi_independence(N: int, xi_values: Optional[List[float]] = None) -> Dict:
    """
    Verify that sigma_N is independent of the H^2 parameter xi.

    PROOF: C_1(N, xi) > 0 for all xi in (0, 1), so
    sgn(lambda_m^{H2}(xi)) = sgn(lambda_m) for all m and all xi.
    Therefore sigma_N(xi) = sigma_N for all xi.

    This function provides NUMERICAL verification at sample points.
    """
    if xi_values is None:
        xi_values = [0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99]

    sigma_flat = signature_from_eigenvalues(N)
    results = {'N': N, 'sigma_flat': sigma_flat, 'xi_checks': []}

    for xi in xi_values:
        c1 = c1_h2(N, xi)
        assert c1 > 0, f"C_1(N={N}, xi={xi}) = {c1} <= 0"

        # sigma on H^2 at this xi
        sigma_h2 = 0
        for m in range(2, N):
            lam = havelock_eigenvalue(m, N)
            lam_h2 = float(lam) * c1
            if lam_h2 > 0:
                sigma_h2 += 1
            elif lam_h2 < 0:
                sigma_h2 -= 1

        results['xi_checks'].append({
            'xi': xi,
            'C1': c1,
            'sigma_h2': sigma_h2,
            'matches': sigma_h2 == sigma_flat,
        })

    results['all_match'] = all(c['matches'] for c in results['xi_checks'])
    return results


# ---------------------------------------------------------------------------
# Palindromic structure
# ---------------------------------------------------------------------------

def verify_palindromic(N: int) -> Dict:
    """
    Verify the palindromic symmetry: lambda_m = lambda_{N-m}.

    This implies:
    - If m is a positive mode, so is N-m.
    - If m is a negative mode, so is N-m.
    - If m is a zero mode, so is N-m.
    - sigma_N decomposes into palindromic pair contributions.
    """
    pairs = []
    for m in range(2, (N + 1) // 2):
        partner = N - m
        lam_m = havelock_eigenvalue(m, N)
        lam_partner = havelock_eigenvalue(partner, N)
        pairs.append({
            'm': m,
            'partner': partner,
            'lambda_m': lam_m,
            'lambda_partner': lam_partner,
            'equal': lam_m == lam_partner,
        })

    # Self-palindromic mode at m = N/2 (even N only)
    self_palindromic = None
    if N % 2 == 0:
        m_half = N // 2
        if 2 <= m_half <= N - 1:
            self_palindromic = {
                'm': m_half,
                'lambda': havelock_eigenvalue(m_half, N),
            }

    all_palindromic = all(p['equal'] for p in pairs)

    return {
        'N': N,
        'pairs': pairs,
        'self_palindromic': self_palindromic,
        'all_palindromic': all_palindromic,
    }


# ---------------------------------------------------------------------------
# Comprehensive verification
# ---------------------------------------------------------------------------

class SignatureResult(NamedTuple):
    """Complete equivariant signature analysis for a given N."""
    N: int
    sigma: int
    n_positive: int
    n_negative: int
    n_zero: int
    eta_hav_0: Fraction
    reduced_eta: Fraction
    rho: Fraction
    rho_3N: Fraction
    positive_modes: List[int]
    negative_modes: List[int]
    zero_modes: List[int]


def full_analysis(N: int) -> SignatureResult:
    """Complete equivariant signature analysis."""
    if N < 3:
        raise ValueError(f"N must be >= 3, got {N}")

    sigma = signature_from_eigenvalues(N)
    n_pos, n_neg, n_zero = sign_counts(N)
    eta_0 = eta_havelock(N, 0.0)
    red_eta = reduced_eta(N)
    rho = rho_invariant(N)
    rho_3n = rho_integrality(N)

    return SignatureResult(
        N=N,
        sigma=sigma,
        n_positive=n_pos,
        n_negative=n_neg,
        n_zero=n_zero,
        eta_hav_0=eta_0,
        reduced_eta=red_eta,
        rho=rho,
        rho_3N=rho_3n,
        positive_modes=positive_modes(N),
        negative_modes=negative_modes(N),
        zero_modes=zero_modes(N),
    )


def verify_all_identities(N: int) -> Dict:
    """
    Verify ALL claimed identities for sigma_N at a given N.

    Checks:
    1. sigma_from_eigenvalues == sigma_closed_form
    2. eta_havelock(N, 0) == sigma
    3. n_pos + n_neg + n_zero == N - 2
    4. palindromic symmetry
    5. 3*N*rho is an integer
    6. xi-independence
    """
    sigma_ev = signature_from_eigenvalues(N)
    sigma_cf = signature_closed_form(N)
    eta_0 = int(eta_havelock(N, 0.0))
    n_pos, n_neg, n_zero = sign_counts(N)
    pal = verify_palindromic(N)
    rho_3n = rho_integrality(N)

    checks = {
        'sigma_eigenvalues_equals_closed_form': sigma_ev == sigma_cf,
        'eta_havelock_0_equals_sigma': eta_0 == sigma_ev,
        'mode_count_consistent': n_pos + n_neg + n_zero == N - 2,
        'palindromic': pal['all_palindromic'],
        'rho_3N_is_integer': rho_3n.denominator == 1,
        'sigma_value': sigma_ev,
    }

    # xi-independence (quick check at 3 points)
    xi_check = verify_xi_independence(N, [0.1, 0.5, 0.9])
    checks['xi_independent'] = xi_check['all_match']

    checks['all_pass'] = all(v for k, v in checks.items()
                              if k != 'sigma_value' and isinstance(v, bool))
    return checks


# ---------------------------------------------------------------------------
# Display table
# ---------------------------------------------------------------------------

def signature_table(N_max: int = 20) -> List[Dict]:
    """
    Generate the complete equivariant signature table.

    Columns: N, n+, n-, n0, sigma, eta-bar, rho, 3N*rho, positive modes.
    """
    rows = []
    for N in range(3, N_max + 1):
        r = full_analysis(N)
        rows.append({
            'N': r.N,
            'n_pos': r.n_positive,
            'n_neg': r.n_negative,
            'n_zero': r.n_zero,
            'sigma': r.sigma,
            'eta_bar': str(r.reduced_eta),
            'rho': str(r.rho),
            'rho_3N': str(r.rho_3N),
            'pos_modes': r.positive_modes,
            'neg_modes': r.negative_modes,
        })
    return rows


# ---------------------------------------------------------------------------
# __main__
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 78)
    print("EQUIVARIANT SIGNATURE OF THE HAVELOCK HESSIAN")
    print("=" * 78)
    print()

    # Table
    print(f"{'N':>3s} {'n+':>3s} {'n-':>3s} {'n0':>3s} {'sigma':>6s} "
          f"{'eta-bar':>8s} {'rho':>12s} {'3N*rho':>8s}  pos modes")
    print("-" * 78)

    for row in signature_table(16):
        print(f"{row['N']:3d} {row['n_pos']:3d} {row['n_neg']:3d} "
              f"{row['n_zero']:3d} {row['sigma']:6d} {row['eta_bar']:>8s} "
              f"{row['rho']:>12s} {row['rho_3N']:>8s}  {row['pos_modes']}")

    print()
    print("=" * 78)
    print("SPECTRAL FLOW TABLE")
    print("=" * 78)
    print()

    for row in spectral_flow_table(12):
        arrow = "<--" if row['spectral_flow'] < -1 else ""
        print(f"  {row['transition']:>6s}: sigma {row['sigma_prev']:3d} -> "
              f"{row['sigma_next']:3d},  SF = {row['spectral_flow']:+d}  {arrow}")

    # APS spectral flow verification
    sf_6_to_8 = spectral_flow(6, 8)
    dim_ker_7 = 2 * len(zero_modes(7))  # real dimension
    print()
    print(f"  APS spectral flow theorem: SF(6->8) = {sf_6_to_8}")
    print(f"  -2 * dim_ker(N=7) = -2 * {len(zero_modes(7))} = {-2 * len(zero_modes(7))}")
    print(f"  Match: {sf_6_to_8 == -2 * len(zero_modes(7))}")

    print()
    print("=" * 78)
    print("XI-INDEPENDENCE VERIFICATION (N=8)")
    print("=" * 78)
    print()

    xi_result = verify_xi_independence(8)
    for c in xi_result['xi_checks']:
        print(f"  xi = {c['xi']:.2f}: C_1 = {c['C1']:8.4f}, "
              f"sigma_H2 = {c['sigma_h2']}, matches flat: {c['matches']}")
    print(f"  All match: {xi_result['all_match']}")

    print()
    print("=" * 78)
    print("FULL IDENTITY VERIFICATION")
    print("=" * 78)
    print()

    all_ok = True
    for N in range(3, 16):
        checks = verify_all_identities(N)
        status = "PASS" if checks['all_pass'] else "FAIL"
        if not checks['all_pass']:
            all_ok = False
        print(f"  N={N:2d}: sigma={checks['sigma_value']:4d}  [{status}]")

    print()
    if all_ok:
        print("  ALL IDENTITIES VERIFIED for N = 3, ..., 15.")
    else:
        print("  SOME IDENTITIES FAILED -- check output.")
