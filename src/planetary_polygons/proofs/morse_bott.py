"""
Morse-Bott structure of the N-gon critical point.

THEOREM (new, this paper):
    For N != 7, the regular N-gon is a Morse-Bott critical point of the
    Thomson energy H = -sum_{j<k} ln|z_j - z_k| restricted to the
    constraint surface M = {P = 0, L = R^2}, modulo the SO(2) rotation.

    The normal Hessian is diagonalised by the Fourier modes m = 2, ..., N-1,
    with eigenvalues lambda_m = (N-1) - m(N-m)/2, each of complex
    multiplicity 1 (real multiplicity 2).

    Morse-Bott index:
        N <= 6:  index 0  (non-degenerate minimum)
        N = 7:   NOT Morse-Bott (4-dim kernel; quartic alpha_0 = 45/14 resolves)
        N >= 8:  complex index N-5 (real index 2(N-5))

PROOF STRUCTURE:
    1. Fourier decomposition of tangent space T_p M
    2. Constraint P=0 removes c_0 (center of mass)
    3. Constraint L=const removes Re(c_1) (radial breathing of m=1 mode)
    4. SO(2) orbit direction is Im(c_1) (rotation)
    5. Normal space is spanned by {c_m : m = 2, ..., N-1}, dimension 2(N-2)
    6. Havelock eigenvalue lambda_m on each mode is (N-1) - m(N-m)/2
    7. Non-degeneracy: lambda_m = 0  iff  m(N-m) = 2(N-1)
       Solutions: m = (N +/- sqrt(N^2 - 8(N-1))) / 2 = (N +/- sqrt((N-4)^2 - 8)) / 2
       Integer solutions in {2,...,N-2} exist only at N=7 (m=3,4).
"""

from fractions import Fraction
from typing import List, Tuple, NamedTuple
import math


class MorseBottResult(NamedTuple):
    """Result of Morse-Bott analysis for the N-gon."""
    N: int
    is_morse_bott: bool
    complex_morse_index: int     # number of negative lambda_m, m=2..N-1
    real_morse_index: int        # = 2 * complex_morse_index
    kernel_dimension: int        # number of zero lambda_m (0 if Morse-Bott)
    normal_eigenvalues: list     # lambda_m as Fraction for m=2..N-1
    reason: str                  # human-readable summary


def havelock_eigenvalue(m: int, N: int) -> Fraction:
    """Exact Havelock eigenvalue lambda_m = (N-1) - m(N-m)/2."""
    return Fraction(N - 1) - Fraction(m * (N - m), 2)


def normal_eigenvalues(N: int) -> List[Fraction]:
    """
    Eigenvalues of the normal Hessian at the N-gon on the constraint
    surface M/SO(2).

    The m=0 mode is removed by P=0 (c_0 = 0).
    The m=1 mode is removed by L=const (Re(c_1)=0) and SO(2) (Im(c_1)).
    Modes m=2,...,N-1 are free, each with eigenvalue lambda_m.
    """
    return [havelock_eigenvalue(m, N) for m in range(2, N)]


def morse_bott_analysis(N: int) -> MorseBottResult:
    """
    Determine the Morse-Bott structure of the N-gon critical point.

    Returns a MorseBottResult with:
    - is_morse_bott: True if the normal Hessian is non-degenerate
    - complex_morse_index: number of negative eigenvalues
    - kernel_dimension: dimension of the kernel (0 if Morse-Bott)
    """
    if N < 3:
        raise ValueError(f"N must be >= 3, got {N}")

    evals = normal_eigenvalues(N)

    n_neg = sum(1 for lam in evals if lam < 0)
    n_zero = sum(1 for lam in evals if lam == 0)
    n_pos = sum(1 for lam in evals if lam > 0)

    is_mb = (n_zero == 0)

    if is_mb and n_neg == 0:
        reason = f"Morse-Bott, index 0 (non-degenerate minimum)"
    elif not is_mb:
        zero_modes = [m for m in range(2, N) if havelock_eigenvalue(m, N) == 0]
        reason = (f"NOT Morse-Bott: {2 * n_zero}-real-dim kernel "
                  f"from modes {zero_modes}")
    else:
        neg_modes = [m for m in range(2, N) if havelock_eigenvalue(m, N) < 0]
        reason = (f"Morse-Bott, complex index {n_neg} "
                  f"(real index {2 * n_neg}), negative modes {neg_modes}")

    return MorseBottResult(
        N=N,
        is_morse_bott=is_mb,
        complex_morse_index=n_neg,
        real_morse_index=2 * n_neg,
        kernel_dimension=2 * n_zero,
        normal_eigenvalues=evals,
        reason=reason,
    )


def verify_mode_counting(N: int) -> dict:
    """
    Verify the Fourier mode counting on the constraint surface.

    Configuration space: C^N (dim 2N)
    Constraints: P=0 (2 eqs), L=const (1 eq) -> constraint surface dim 2N-3
    SO(2) orbit: dim 1 -> quotient dim 2N-4
    Normal modes: m=2,...,N-1 -> N-2 complex = 2(N-2) real dimensions

    Check: 2(N-2) = 2N-4  ✓
    """
    config_dim = 2 * N
    constraint_surface_dim = config_dim - 3  # P=0 (2) + L=const (1)
    quotient_dim = constraint_surface_dim - 1  # SO(2) orbit
    normal_dim = 2 * (N - 2)  # modes m=2,...,N-1

    return {
        'N': N,
        'config_dim': config_dim,
        'constraint_surface_dim': constraint_surface_dim,
        'quotient_dim': quotient_dim,
        'normal_mode_dim': normal_dim,
        'dimensions_match': quotient_dim == normal_dim,
    }


def zero_eigenvalue_classification() -> dict:
    """
    Classify all N for which the normal Hessian has zero eigenvalues.

    lambda_m = 0  iff  m(N-m) = 2(N-1)
    Rewriting: m^2 - Nm + 2(N-1) = 0
    Discriminant: D = N^2 - 8(N-1) = (N-4)^2 - 8

    Integer solutions exist iff D is a perfect square.
    D = k^2 => (N-4)^2 - k^2 = 8 => (N-4-k)(N-4+k) = 8

    Factor pairs of 8: (1,8), (2,4)
    Case (1,8): N-4-k=1, N-4+k=8 => N=8.5 (not integer)
    Case (2,4): N-4-k=2, N-4+k=4 => N=7, k=1 => m = (7±1)/2 = 3 or 4

    So N=7 is the UNIQUE value with zero normal eigenvalues.
    """
    results = {}
    for N in range(3, 31):
        evals = normal_eigenvalues(N)
        zeros = [m for m in range(2, N) if havelock_eigenvalue(m, N) == 0]
        if zeros:
            results[N] = zeros

    # Analytical verification
    # D = (N-4)^2 - 8 must be a non-negative perfect square
    # and m = (N ± sqrt(D))/2 must be integer in {2,...,N-2}
    analytical_check = {}
    for N in range(3, 100):
        D = (N - 4) ** 2 - 8
        if D >= 0:
            sqrtD = int(math.isqrt(D))
            if sqrtD * sqrtD == D:
                m1 = (N + sqrtD) // 2
                m2 = (N - sqrtD) // 2
                if (N + sqrtD) % 2 == 0 and 2 <= m2 and m1 <= N - 2:
                    analytical_check[N] = [m2, m1]

    return {
        'numerical_zeros': results,
        'analytical_zeros': analytical_check,
        'unique_N': 7,
        'proof': (
            "lambda_m = 0 iff m^2 - Nm + 2(N-1) = 0. "
            "Discriminant D = (N-4)^2 - 8. "
            "Factor pairs of 8: (2,4) gives N=7, m in {3,4}. "
            "No other factorisation gives integer N. QED."
        ),
    }


def morse_index_formula_value(N: int) -> int:
    """
    Complex Morse index formula.

    index = 0      for N <= 6  (all lambda_m > 0)
    index = N-5    for N >= 8  (modes m=3,...,N-3 are negative, plus palindromic)

    N=7 is not Morse-Bott (kernel, not counted).

    Proof that index = N-5 for N >= 8:
    The negative modes are {m in {2,...,N-1} : m(N-m) > 2(N-1)}.
    The boundary m(N-m) = 2(N-1) gives m = (N ± sqrt((N-4)^2 - 8))/2.
    For N >= 8: sqrt((N-4)^2 - 8) < N-4, so the roots are in (2, N-2).
    The negative modes form a contiguous block {m_-, m_-+1, ..., m_+}
    symmetric about N/2 (palindromic).
    For N=8: modes {3,4,5} -> count 3 = 8-5. ✓
    By induction on N: adding vortex N+1 adds exactly one new negative
    mode (m = N-2 becomes negative), so index(N+1) = index(N) + 1.
    """
    if N <= 6:
        return 0
    if N == 7:
        return 0  # not Morse-Bott, but kernel not negative
    return N - 5


def verify_morse_index_formula(N_max: int = 25) -> dict:
    """Verify the Morse index formula across a range of N."""
    results = {}
    for N in range(3, N_max):
        mb = morse_bott_analysis(N)
        formula = morse_index_formula_value(N)
        matches = (mb.complex_morse_index == formula)
        results[N] = {
            'computed_index': mb.complex_morse_index,
            'formula_index': formula,
            'matches': matches,
            'is_morse_bott': mb.is_morse_bott,
        }
    return results


def full_morse_bott_table(N_max: int = 15) -> list:
    """Generate the complete Morse-Bott classification table."""
    rows = []
    for N in range(3, N_max + 1):
        mb = morse_bott_analysis(N)
        vc = verify_mode_counting(N)
        rows.append({
            'N': N,
            'is_morse_bott': mb.is_morse_bott,
            'complex_index': mb.complex_morse_index,
            'real_index': mb.real_morse_index,
            'kernel_dim': mb.kernel_dimension,
            'dim_check': vc['dimensions_match'],
            'reason': mb.reason,
        })
    return rows
