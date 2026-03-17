"""
Cauchy blob O(ε²) correction to the constrained Hessian eigenvalues.

The regularized Cauchy blob interaction:
    h_ε(d) = -½ ln(d² + 2ε²)
recovers -ln(d) as ε → 0 and introduces an O(ε²) Hessian correction.

Proposition (paper §6.4 / Proposition 4.2):
    λ_m(ε) = λ_m(0) + [-(N²-1)/12 + P_m] ε² + O(ε⁴)

where λ_m(0) is the Havelock eigenvalue and P_m is the projection of
the O(ε²) Hessian correction δ∇²H onto the critical radial Fourier mode.

The critical mode for each N is the radial amplitude modulation
    dz_k = z_k · cos(2π · floor(N/2) · k / N),
i.e., the "half-period" radial ripple around the ring.

Paper table (§6.4):
    N:   3      4     5    6     7     8
    P_m: -1/3  +1/4  +1   +4    +8   +65/4
    c_m: -1    -1    -1  +13/12  +4   +11

c_m < 0 for N ≤ 5 (blob destabilises), c_m > 0 for N ≥ 6 (blob stabilises).
"""
import numpy as np


def _ring_positions(N):
    return np.exp(2j * np.pi * np.arange(N) / N)


def _critical_mode(N):
    """Critical Fourier wavenumber: floor(N/2)."""
    return N // 2


def _radial_fourier_mode(N):
    """
    Critical radial Fourier mode: dz_k = z_k · cos(2π·m·k/N), m = floor(N/2).

    This is the radial amplitude modulation at the half-period frequency
    that gives the exact P_m values from the paper.

    Returns a normalized 2N real vector [dx₀,...,dx_{N-1}, dy₀,...,dy_{N-1}].
    """
    k = np.arange(N)
    m = _critical_mode(N)
    z_ring = np.exp(2j * np.pi * k / N)
    amp = np.cos(2 * np.pi * m * k / N)
    dz = z_ring * amp          # radial displacement with azimuthal modulation
    v = np.concatenate([dz.real, dz.imag])
    norm = np.linalg.norm(v)
    return v / norm if norm > 1e-14 else v


def _analytic_blob_hessian_correction(N):
    """
    O(ε²)/ε² Hessian correction matrix for the N-vortex ring.

    From d/d(ε²)|₀ of the Cauchy blob Hessian, per pair (j,k):
        δH_{jj,xx} += (2/d⁶)(dy² - 3dx²)
        δH_{jj,yy} += (2/d⁶)(dx² - 3dy²)
        δH_{jj,xy} += (-8dx·dy)/d⁶
    and the corresponding off-diagonal blocks (j,k) with opposite signs.

    This formula follows from differentiating the pair Hessian
    d²h_ε/dx_j² with respect to ε² and evaluating at ε=0.
    """
    z = _ring_positions(N)
    delta_H = np.zeros((2 * N, 2 * N))
    for j in range(N):
        for k in range(N):
            if j == k:
                continue
            dz = z[j] - z[k]
            dx, dy = dz.real, dz.imag
            d2 = dx ** 2 + dy ** 2
            d6 = d2 ** 3
            h_xx = (2.0 / d6) * (dy ** 2 - 3 * dx ** 2)
            h_yy = (2.0 / d6) * (dx ** 2 - 3 * dy ** 2)
            h_xy = -8.0 * dx * dy / d6
            # Diagonal block j-j
            delta_H[j, j]         += h_xx
            delta_H[j + N, j + N] += h_yy
            delta_H[j, j + N]     += h_xy
            delta_H[j + N, j]     += h_xy
            # Off-diagonal block j-k (opposite sign)
            delta_H[j, k]         -= h_xx
            delta_H[j + N, k + N] -= h_yy
            delta_H[j, k + N]     -= h_xy
            delta_H[j + N, k]     -= h_xy
    return delta_H


def compute_Pm(N):
    """
    P_m for the N-ring: projection of the O(ε²) blob Hessian correction
    onto the critical radial Fourier mode m = floor(N/2).

    Exact values from paper §6.4:
        N=3: -1/3,  N=4: 1/4,  N=5: 1,  N=6: 4,  N=7: 8,  N=8: 65/4.
    """
    delta_H = _analytic_blob_hessian_correction(N)
    v = _radial_fourier_mode(N)
    return float(v @ delta_H @ v)


def blob_correction_table(N_range=range(3, 9)):
    """
    Full correction table for N in N_range.

    Returns dict:
        N → {'shift': -(N²-1)/12, 'Pm': P_m, 'cm': -(N²-1)/12 + P_m}

    c_m < 0: blob destabilises (N ≤ 5)
    c_m > 0: blob stabilises  (N ≥ 6)
    """
    result = {}
    for N in N_range:
        shift = -(N ** 2 - 1) / 12.0
        Pm = compute_Pm(N)
        cm = shift + Pm
        result[N] = {'shift': shift, 'Pm': Pm, 'cm': cm}
    return result


def stabilization_threshold(N):
    """
    Minimum blob width ε to stabilise the N-ring.

    For N ≥ 6 (c_m > 0): ε_stab = 1 / sqrt(c_m).
    For N ≤ 5 (c_m ≤ 0): returns float('inf') — cannot be stabilised by blobs.
    """
    table = blob_correction_table(range(N, N + 1))
    cm = table[N]['cm']
    if cm <= 0:
        return float('inf')
    return 1.0 / np.sqrt(cm)


if __name__ == "__main__":
    table = blob_correction_table()
    print(f"{'N':>3}  {'shift':>8}  {'P_m':>8}  {'c_m':>8}")
    for N, d in table.items():
        print(f"{N:>3}  {d['shift']:>8.4f}  {d['Pm']:>8.4f}  {d['cm']:>8.4f}")
