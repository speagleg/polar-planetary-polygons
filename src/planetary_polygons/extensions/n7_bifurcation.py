"""
N=7 bifurcation: quartic coefficient on the neutral subspace.

The N=7 ring has two marginal (zero-eigenvalue) modes: the angular Fourier
modes at m=3 and m=4.  By Z_7 symmetry, the unconstrained quartic
d^4H/dt^4 = 153/7 is constant on the entire 2D neutral sphere (paper eq. 13).

The constrained quartic uses Newton projection onto {L = N}: for the angular
m=3 mode u with Re(Σ z_k·conj(u_k)) = 0 and |u|^2 = 1, the projected path is
    z(ε) = (z + ε·u) · sqrt(N / (N + ε²))
The constrained quartic is extracted by the paper's two-point stencil with
Richardson extrapolation (§6.3), giving ≈ 19.29.

Paper §6.3: unconstrained = 153/7 ≈ 21.86, constrained ≈ 19.28,
            correction Δ ≈ 2.58, α₀ ≈ 3.2.
"""
import numpy as np
from fractions import Fraction


def _ring_positions(N):
    return np.exp(2j * np.pi * np.arange(N) / N)


def _angular_fourier_mode(N, m, imag_part=False):
    """
    Angular (tangential) Fourier mode of the N-vortex ring, as a normalized
    2N real vector [dx₀,...,dx_{N-1}, dy₀,...,dy_{N-1}].

    For ring z_k = exp(2πik/N), the pure-angular perturbation is:
        dz_k = i · z_k · ε_k,   ε_k = cos(2πmk/N)  or  sin(2πmk/N)

    This is orthogonal to the angular impulse gradient (v · ∇L = 0) since
    Re(Σ z_k · conj(dz_k)) = Re(Σ i|z_k|²·ε_k) = 0.
    """
    k = np.arange(N)
    eps = np.sin(2 * np.pi * m * k / N) if imag_part else np.cos(2 * np.pi * m * k / N)
    z_ring = np.exp(2j * np.pi * k / N)
    dz = 1j * z_ring * eps          # tangential displacement
    v = np.concatenate([dz.real, dz.imag])
    norm = np.linalg.norm(v)
    return v / norm if norm > 1e-14 else v


def _analytic_pair_quartic(z, v):
    """
    Exact quartic Σ_{j<k} d^4/dt^4 [-ln|z_j+t·v_j - z_k-t·v_k|] |_{t=0}

    Per-pair formula (paper §6.3):
        6C²/A² - 12C·B²/A³ + 3B⁴/A⁴
    where  A = |Δz|², B = 2Re(Δz · conj(Δu)), C = |Δu|²
    and Δz = z_j-z_k, Δu = v_cj - v_ck  (complex perturbation).
    """
    N = len(z)
    v_c = v[:N] + 1j * v[N:]
    total = 0.0
    for j in range(N):
        for k in range(j + 1, N):
            dz = z[j] - z[k]
            du = v_c[j] - v_c[k]
            A = abs(dz) ** 2
            B = 2.0 * np.real(dz * np.conj(du))
            C = abs(du) ** 2
            total += 6.0 * C ** 2 / A ** 2 - 12.0 * C * B ** 2 / A ** 3 + 3.0 * B ** 4 / A ** 4
    return total


def unconstrained_quartic(N, m):
    """
    d^4H/dt^4 for the angular Fourier mode m of the N-ring,
    computed with the exact analytic per-pair formula.

    For N=7, m=3 and m=4 both give 153/7 ≈ 21.857 by Z_7 symmetry.
    """
    z = _ring_positions(N)
    v = _angular_fourier_mode(N, m)
    return _analytic_pair_quartic(z, v)


def quartic_exact_n7():
    """Exact unconstrained quartic for N=7: 153/7."""
    return Fraction(153, 7)


def _constrained_quartic_at_h(z, u, h):
    """
    Paper's two-point stencil for the constrained quartic at step size h.

    Newton-projected path: z(ε) = (z + ε·u) · sqrt(N / (N + ε²))
    where L(ε) = N + ε² exactly (since Re(Σ z_k·conj(u_k)) = 0, |u|^2 = 1).

    Stencil: [2·δH(2h) - 8·δH(h)] / h^4 → 24c₄ = d^4H/dε^4
    (eliminates h^2 leading error; see paper §6.3).
    """
    N = len(z)

    def H(z_pts):
        total = 0.0
        for j in range(N):
            for k in range(j + 1, N):
                d = abs(z_pts[j] - z_pts[k])
                if d > 1e-14:
                    total -= np.log(d)
        return total

    def z_proj(eps):
        return (z + eps * u) * np.sqrt(N / (N + eps ** 2))

    H0 = H(z)
    dH_h  = H(z_proj(h))   - H0
    dH_2h = H(z_proj(2 * h)) - H0
    return (2.0 * dH_2h - 8.0 * dH_h) / h ** 4


def constrained_quartic_n7():
    """
    Constrained quartic on the Newton-projected constraint surface for N=7.

    Uses the angular m=3 mode, the paper's two-point stencil, and
    Richardson extrapolation in h² to eliminate leading truncation error.

    Returns ≈ 19.29 (paper gives 19.28).
    """
    N = 7
    z = _ring_positions(N)
    u = _angular_fourier_mode(N, 3)
    u_c = u[:N] + 1j * u[N:]

    # Richardson extrapolation: two step sizes that agree to 4 decimal places
    h1, h2 = 0.04, 0.03
    q1 = _constrained_quartic_at_h(z, u_c, h1)
    q2 = _constrained_quartic_at_h(z, u_c, h2)
    # Exact leading error is O(h²): q(h) ≈ q_exact + c·h²
    # Richardson: q_exact ≈ (q2·h1² - q1·h2²) / (h1² - h2²)
    r = h2 ** 2 / h1 ** 2
    return float((q2 - r * q1) / (1.0 - r))


def constraint_correction_n7():
    """153/7 minus constrained quartic ≈ 2.57."""
    return float(Fraction(153, 7)) - constrained_quartic_n7()


def alpha_0_n7():
    """Leading amplitude coefficient α₀ = constrained_quartic / 6 ≈ 3.21."""
    return constrained_quartic_n7() / 6.0


if __name__ == "__main__":
    print(f"Unconstrained (m=3): {unconstrained_quartic(7, 3):.6f}")
    print(f"Unconstrained (m=4): {unconstrained_quartic(7, 4):.6f}")
    print(f"Exact 153/7 = {float(Fraction(153, 7)):.6f}")
    print(f"Constrained (Richardson): {constrained_quartic_n7():.4f}")
    print(f"Correction: {constraint_correction_n7():.4f}")
    print(f"alpha_0: {alpha_0_n7():.4f}")
