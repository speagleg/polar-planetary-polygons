"""
Matched asymptotic solution — inner loxodromic flow to outer Rossby wave.
"""
import numpy as np


class LoxodromicFlow:
    """Complex potential w(z) = A z^s, s = sigma + i*alpha."""

    def __init__(self, A: complex, s: complex):
        self.A = A
        self.s = s

    @classmethod
    def from_velocity_ratio(cls, ratio: float, U_max: float,
                             A: complex = 1.0) -> 'LoxodromicFlow':
        """Construct from radial/total velocity ratio at jet boundary.
        sigma ≈ ratio - 1 (Theorem 3 identification)."""
        sigma = ratio - 1.0
        alpha = np.pi / 3  # n=6 hexagonal mode
        return cls(A=A, s=complex(sigma, alpha))

    def stream_function(self, rho, theta):
        """psi = Im(A * exp(s*(rho + i*theta)))"""
        z = rho + 1j * theta
        return np.imag(self.A * np.exp(self.s * z))


def hexagon_amplitude_analytic(delta_U: float, U_star: float,
                                rho_star: float, n: int = 6) -> float:
    """
    Theorem 5 amplitude: epsilon = C * (delta_U/U_star) * exp(-n*|rho_star|)
    """
    C = 1.0
    return C * (delta_U / U_star) * np.exp(-n * abs(rho_star))


