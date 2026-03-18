"""
N=7 bifurcation: quartic coefficient on the neutral subspace.

The N=7 ring has a 2D neutral subspace: the radial cos and sin Fourier modes
at m=3. These are dz_k = z_k·cos(2πmk/N) and dz_k = z_k·sin(2πmk/N) (radial
displacements along the equilibrium positions). Note: the tangential m=3 mode
(dz_k = i·z_k·cos(2πmk/N)) has Lagrangian eigenvalue +6 and is NOT marginal.

By Z_7 symmetry, the unconstrained quartic d^4H/dt^4 = 153/7 is constant on
the entire 2D neutral subspace (paper eq. 13).

The constrained quartic uses Newton projection onto {L = N}: for the radial
m=3 mode u with Re(Σ z_k·conj(u_k)) = 0 and |u|^2 = 1, the projected path is
    z(ε) = (z + ε·u) · sqrt(N / (N + ε²))
The constrained quartic is extracted via the log-ratio delta-H method with
Richardson extrapolation (§6.3), giving ≈ 19.29.

Paper §6.3: unconstrained = 153/7 ≈ 21.86, constrained ≈ 19.29,
            correction Δ ≈ 2.57, α₀ ≈ 3.21.
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


def _radial_fourier_mode(N, m, imag_part=False):
    """
    Radial Fourier mode of the N-vortex ring, as a normalized 2N real vector.

    For ring z_k = exp(2πik/N), the radial perturbation is:
        dz_k = z_k · ε_k,   ε_k = cos(2πmk/N)  or  sin(2πmk/N)

    This is the correct neutral subspace mode for N=7, m=3.
    The tangential mode (dz_k = i·z_k·ε_k) has eigenvalue +6, not 0.
    """
    k = np.arange(N)
    eps = np.sin(2 * np.pi * m * k / N) if imag_part else np.cos(2 * np.pi * m * k / N)
    z_ring = np.exp(2j * np.pi * k / N)
    dz = z_ring * eps          # radial displacement (NOT 1j * z_ring * eps)
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


def _delta_H_constrained(z, u, h):
    """
    H_constrained(h) - H(0) computed as sum of log-ratios (numerically stable).

    Projected path: z_proj = (z + h*u) * sqrt(N / (N + h²))
    """
    import math
    N = len(z)
    zp = z + h * u
    L = np.sum(np.abs(zp)**2)
    scale = np.sqrt(N / L)
    zproj = zp * scale
    dH = 0.0
    for j in range(N):
        for l in range(j + 1, N):
            d_eq = abs(z[j] - z[l])
            d_pr = abs(zproj[j] - zproj[l])
            dH -= math.log(d_pr / d_eq)
    return dH


def _fourth_diff_delta(z, u, h):
    """[2·dH(2h) - 8·dH(h)] / h^4 → 24·c₄ (the constrained quartic)."""
    dH1 = _delta_H_constrained(z, u, h)
    dH2 = _delta_H_constrained(z, u, 2 * h)
    return (2 * dH2 - 8 * dH1) / h**4


def constrained_quartic_n7():
    """
    Constrained quartic on the Newton-projected constraint surface for N=7.

    Uses the radial m=3 mode, log-ratio delta-H method, and Richardson
    extrapolation in h² to eliminate leading truncation error.

    Returns ≈ 19.29 (paper §6.3).
    """
    N = 7
    z = _ring_positions(N)
    v = _radial_fourier_mode(N, 3)
    u_c = v[:N] + 1j * v[N:]

    h1, h2 = 0.04, 0.03
    q1 = _fourth_diff_delta(z, u_c, h1)
    q2 = _fourth_diff_delta(z, u_c, h2)
    # Richardson: q_exact ≈ (q2·h1² - q1·h2²) / (h1² - h2²)
    r = h2**2 / h1**2
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
