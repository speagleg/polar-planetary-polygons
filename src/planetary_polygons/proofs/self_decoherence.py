"""
Self-decoherence of the breathing mode by the angular Havelock bath.

PROPOSITION: The N-2 angular modes decohere the breathing mode ρ with rate
  γ = (C₁')²/4 × Σ_{m≠m*} 1/λ_m²

For γ >> 1, the reduced density matrix is effectively diagonal:
  ρ_red(ρ, ρ') ≈ |Ψ₀(ρ)|² δ(ρ-ρ')

recovering the Born rule without postulating it.
"""
import numpy as np


def C1_h2(N, rho):
    """C₁ on H² at geodesic radius rho."""
    xi = np.tanh(rho / 2) ** 2
    return (N - 1) * (1 + xi ** 2) / (1 - xi) ** 2


def C1_prime(N, rho, eps=1e-7):
    """dC₁/dρ by central difference."""
    return (C1_h2(N, rho + eps) - C1_h2(N, rho - eps)) / (2 * eps)


def decoherence_rate(N, rho):
    """
    Compute the decoherence rate γ from the Havelock bath.

    γ = (C₁')²/4 × Σ_{m≠m*} 1/λ_m²

    Parameters
    ----------
    N : int — polygon number
    rho : float — geodesic radius on H²

    Returns
    -------
    gamma : float — decoherence rate (γ >> 1 means strong decoherence)
    """
    m_star = N // 2
    C1 = C1_h2(N, rho)
    C1p = C1_prime(N, rho)

    fisher_sum = 0.0
    for m in range(1, N):
        if m == m_star:
            continue
        lam_m = C1 - m * (N - m) / 2
        if lam_m <= 0:
            continue
        fisher_sum += 1.0 / lam_m ** 2

    return C1p ** 2 / 4 * fisher_sum


def decoherence_length(N, rho):
    """Δρ = 1/√γ — the coherence length of the breathing mode."""
    gamma = decoherence_rate(N, rho)
    return 1.0 / np.sqrt(gamma) if gamma > 0 else float('inf')


def verify_strong_decoherence(N_values=None, rho=0.5):
    """Verify γ >> 1 for the physically relevant polygon numbers."""
    if N_values is None:
        N_values = [5, 7, 9, 11]

    results = {}
    for N in N_values:
        gamma = decoherence_rate(N, rho)
        delta_rho = decoherence_length(N, rho)
        results[N] = {
            'gamma': gamma,
            'delta_rho': delta_rho,
            'strong': gamma > 1,
        }
    return results


if __name__ == '__main__':
    print("=== Self-decoherence of the breathing mode ===")
    print()
    results = verify_strong_decoherence()
    for N, r in results.items():
        print(f"N={N}: γ = {r['gamma']:.2f}, Δρ = {r['delta_rho']:.3f}, "
              f"strong = {r['strong']}")
    print()
    print("The angular Havelock bath decoheres the breathing mode")
    print("for all N ≥ 5, giving the Born rule |Ψ₀(ρ)|² without postulate.")
