"""
Stability analysis with disordered vortex circulations on H².

For a ring of N vortices with unequal circulations κ_k = κ(1 + η_k),
η_k i.i.d. N(0, σ²), the H² Hamiltonian becomes:

    H_κ = −Σ_{j<k} κ_j κ_k ln|z_j − z_k|
          + ½ Σ_j κ_j (K_total − κ_j) ln(a² − |z_j|²)

where K_total = Σ_k κ_k.

The uniform-circulation H_hyp is recovered when κ_k = 1 for all k
(K_total = N, so ½ κ_j(K−κ_j) = (N-1)/2).

Eigenvalue computation: the ring positions are held at the uniform-
circulation equilibrium r_E = a·tanh(ρ/(2a)).  This is exact to O(η);
the O(η) equilibrium shift produces only an O(η²) eigenvalue correction.
The Fourier-mode FD eigenvalue is therefore correct to O(η²) for small σ.

Instability probability P(λ_min < 0) is computed by Monte Carlo.
"""
import numpy as np
from .h2_stability import get_Omega, J_hyp


def _H_hyp_kappa(z_re, z_im, a, kappa):
    """
    H² Hamiltonian with unequal vortex circulations.

    Parameters
    ----------
    z_re, z_im : array_like of shape (N,)
        Vortex positions inside the Poincaré disk |z| < a.
    a : float
        Curvature radius.
    kappa : array_like of shape (N,)
        Individual circulations κ_k.  K_total = sum(kappa).

    Returns
    -------
    float
    """
    z = z_re + 1j * z_im
    N = len(z)
    kappa = np.asarray(kappa, dtype=float)
    K_total = np.sum(kappa)
    H = 0.0
    for j in range(N):
        for k in range(j + 1, N):
            H -= kappa[j] * kappa[k] * np.log(abs(z[j] - z[k]))
        H += 0.5 * kappa[j] * (K_total - kappa[j]) * np.log(a ** 2 - abs(z[j]) ** 2)
    return H


def disorder_min_eigenvalue_h2(N, rho, eta, a=1.0, h_fd=1e-5):
    """
    Minimum Fourier-mode eigenvalue of the disordered H_κ Hamiltonian.

    Ring positions are held at the uniform equilibrium r_E = a·tanh(ρ/(2a)).
    The rotation rate Ω is also taken from the uniform-κ formula — the
    O(η) correction to Ω produces only an O(η²) error in the eigenvalue.

    Parameters
    ----------
    N : int
        Ring size.
    rho : float
        Geodesic ring radius ρ (r_E = a·tanh(ρ/(2a))).
    eta : array_like of shape (N,)
        Fractional disorders η_k so that κ_k = 1 + η_k.
    a : float
        Curvature radius.
    h_fd : float
        Finite-difference step size.

    Returns
    -------
    float
        Minimum eigenvalue over modes m = 1, ..., N//2.
    """
    r_E = a * np.tanh(rho / (2.0 * a))
    k_idx = np.arange(N)
    z = r_E * np.exp(2j * np.pi * k_idx / N)
    kappa = 1.0 + np.asarray(eta, dtype=float)

    Omega = get_Omega(N, r_E, a)   # uniform-κ rotation rate

    def F(q):
        return _H_hyp_kappa(q[0::2], q[1::2], a, kappa) - Omega * J_hyp(q[0::2], q[1::2], a)

    q0 = np.zeros(2 * N)
    q0[0::2] = z.real
    q0[1::2] = z.imag
    F0 = F(q0)

    lams = []
    for m in range(1, N // 2 + 1):
        theta_k = 2 * np.pi * k_idx / N
        amp = np.cos(2 * np.pi * m * k_idx / N)
        u = np.zeros(2 * N)
        u[0::2] = amp * np.cos(theta_k)
        u[1::2] = amp * np.sin(theta_k)
        norm_sq = np.dot(u, u)
        if norm_sq < 1e-10:
            continue
        u_hat = u / np.sqrt(norm_sq)
        lam = (F(q0 + h_fd * u_hat) - 2 * F0 + F(q0 - h_fd * u_hat)) / h_fd ** 2
        lams.append(lam)

    return min(lams)


def instability_probability(N, rho, eta_std, n_trials=1000, seed=0, a=1.0):
    """
    Monte Carlo estimate of P(λ_min < 0) for a disordered N-ring on H².

    For each trial, draws η_k ~ N(0, eta_std²) i.i.d. and computes the
    minimum Fourier-mode eigenvalue of H_κ at the nominal ring equilibrium.

    Parameters
    ----------
    N : int
        Ring size.
    rho : float
        Geodesic ring radius ρ.
    eta_std : float
        Standard deviation of the fractional circulation disorder.
    n_trials : int
        Number of Monte Carlo samples.
    seed : int
        RNG seed for reproducibility.
    a : float
        Curvature radius.

    Returns
    -------
    float
        Estimated P(λ_min < 0) ∈ [0, 1].
    """
    rng = np.random.default_rng(seed)
    count = 0
    for _ in range(n_trials):
        eta = rng.normal(0.0, eta_std, size=N)
        if disorder_min_eigenvalue_h2(N, rho, eta, a=a) < 0:
            count += 1
    return count / n_trials


if __name__ == '__main__':
    print('Instability probability vs eta_std for N=7, rho=0.3:')
    for eta_std in [0.0, 0.05, 0.10, 0.20, 0.40]:
        p = instability_probability(7, 0.3, eta_std, n_trials=500, seed=42)
        print(f'  eta_std={eta_std:.2f}  P(unstable)={p:.3f}')
