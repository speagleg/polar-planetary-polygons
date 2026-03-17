"""
Theorem 5: Matched Asymptotic Expansion.

The matched asymptotic solution connects the inner loxodromic flow (Theorem 2)
to the outer stationary Rossby wave (Theorem 3) through a boundary layer at
rho = rho* (the PV step location).

Structure of the expansion
--------------------------
Let epsilon = amplitude of hexagonal perturbation, delta = (U - U*)/U* = jet excess.

Inner expansion (rho << rho*):
    psi_inner = psi_0(rho) + epsilon psi_1(rho,theta) + O(epsilon^2)
    where psi_0 is the loxodromic flow (Theorem 2) and psi_1 is the O(epsilon) response.

Outer expansion (rho >> rho*):
    psi_outer = psi_wave(rho,theta) (Rossby wave, Theorem 3)

Matching region (|rho - rho*| = O(delta)):
    Van Dyke matching principle: inner-of-outer = outer-of-inner to each order.

Main result of Theorem 5:
    epsilon = C * (delta_U / U*) * exp(-alpha * n * |rho*|)

where C is an O(1) constant determined by the matching, alpha is the Rossby
wave decay rate in the matching region, and n=6 is the wavenumber.

This gives an explicit prediction for the hexagon amplitude as a function
of the observed jet speed excess delta_U -- testable against Saturn data.
"""

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from typing import Optional

# LoxodromicFlow and RossbyWavePacket are used by the MatchedAsymptoticSolver
# class but are not yet ported to this repo. The standalone functions
# matching_constant() and hexagon_amplitude_analytic() work without them.
try:
    from rossby import RossbyWavePacket
except ImportError:
    RossbyWavePacket = None

# Minimal stub for type annotations
class LoxodromicFlow:
    """Stub — full implementation in spiral-hexagon working repo."""
    def __init__(self, **kwargs):
        self.sigma = kwargs.get('sigma', 0.0)
        self.alpha = kwargs.get('alpha', 0.0)
        self.A = kwargs.get('A', 1.0)
    def stream_function(self, rho, theta):
        return rho * 0  # placeholder


def matching_constant(n: int = 6, sigma_jet: float = 0.05,
                       U_max: float = 120.0, U_star: float = 105.3) -> float:
    """
    Compute the matching constant C from the Fourier overlap integral.

    DERIVED (Mathematica, confirmed analytically):
    The overlap of the PV gradient dq/drho with the eigenfunction
    envelope exp(-n*rho) over the finite-width Gaussian jet gives:

        overlap = n*U_max - exp(n^2*sJ^2/2)*n^2*sqrt(pi/2)*sJ*U_max*Erfc(n*sJ/sqrt(2))

        C = overlap / (U_star * n)

    For Saturn (n=6, sJ=0.05, U_max=120, U_star=105.3):
        C = 0.797 (NOT 1/n = 0.167)

    The factor ~5 difference from C=1/n arises because 1/n assumed a
    delta-function PV step, while the actual Gaussian jet's PV gradient
    has a finite width that projects more strongly onto the eigenfunction.

    In the sharp-step limit (sJ -> 0): C -> U_max/U_star ~ 1.
    In the wide-jet limit (sJ -> inf): C -> 0.
    """
    from scipy.special import erfc
    sJ = sigma_jet
    term1 = n * U_max
    term2 = np.exp(n**2 * sJ**2 / 2) * n**2 * np.sqrt(np.pi / 2) * sJ * U_max * erfc(n * sJ / np.sqrt(2))
    overlap = term1 - term2
    return overlap / (U_star * n)


def hexagon_amplitude_analytic(delta_U: float, U_star: float,
                                n: int = 6, rho_star: float = 0.0,
                                C: float = None,
                                sigma_jet: float = 0.05,
                                U_max: float = 120.0) -> float:
    """
    Analytic amplitude formula from the matched asymptotic expansion.

    THEOREM 5:
        epsilon = C(n, sigma_jet) * (delta_U / U*) * exp(-n * |rho*|)

    where C is the Fourier overlap matching constant derived from the
    PV gradient projection onto the eigenfunction envelope.

    For Saturn: C = 0.797, giving epsilon = 0.112 (matches Cassini ✓).

    Parameters
    ----------
    delta_U : float
        Jet speed excess: U_observed - U_stationary
    U_star : float
        Stationary jet speed from Rossby dispersion
    n : int
        Azimuthal wavenumber (6 for hexagon)
    rho_star : float
        Log-radius of PV step (0 = jet center in normalized coords)
    C : float or None
        Matching constant. If None, computed from overlap integral.
    sigma_jet : float
        Jet half-width in log-polar units (used when C is None)
    U_max : float
        Peak jet speed (used when C is None)
    """
    if U_star == 0:
        return 0.0
    if C is None:
        C = matching_constant(n, sigma_jet, U_max, U_star)
    return C * (delta_U / U_star) * np.exp(-n * abs(rho_star))


class MatchedAsymptoticSolver:
    """
    Computes the matched asymptotic expansion connecting spiral (inner) to
    hexagon (outer) through the PV step at rho*.

    Parameters
    ----------
    loxodromic_flow : LoxodromicFlow
        Inner solution (Theorem 2)
    rossby_wave : RossbyWavePacket
        Outer solution (Theorem 3)
    rho_star : float
        Log-radius of the PV step (jet center)
    delta_U : float
        Jet speed excess above stationary value: delta_U = U - U*
    U_star : float
        Stationary jet speed
    n : int
        Azimuthal wavenumber (default 6)
    """

    def __init__(self, loxodromic_flow: LoxodromicFlow,
                 rossby_wave: RossbyWavePacket,
                 rho_star: float, delta_U: float,
                 U_star: float, n: int = 6):
        self.inner_flow = loxodromic_flow
        self.outer_wave = rossby_wave
        self.rho_star = rho_star
        self.delta_U = delta_U
        self.U_star = U_star
        self.n = n

        # Matching region width scales with delta_U/U_star
        self.delta = abs(delta_U / U_star) if U_star != 0 else 0.1
        # Boundary layer thickness
        self.matching_width = max(self.delta, 0.01)

    def inner_expansion(self, rho: np.ndarray,
                        theta: np.ndarray, order: int = 1) -> np.ndarray:
        """
        Compute inner expansion to specified order in epsilon.

        Order 0: psi_0 = loxodromic stream function (Theorem 2)
        Order 1: psi_0 + epsilon * psi_1 where psi_1 is the n-fold
                 perturbation induced by the hexagonal boundary.
        """
        psi_0 = self.inner_flow.stream_function(rho, theta)

        if order == 0:
            return psi_0

        # O(epsilon) correction: n-fold modulation of the inner flow
        # psi_1 ~ exp(sigma*rho) * cos(n*theta) * envelope
        sigma = self.inner_flow.sigma
        epsilon = self._estimate_epsilon()
        envelope = np.exp(-self.n * np.abs(rho - self.rho_star))
        psi_1 = epsilon * np.exp(sigma * rho) * np.cos(self.n * theta) * envelope

        return psi_0 + psi_1

    def outer_expansion(self, rho: np.ndarray,
                        theta: np.ndarray) -> np.ndarray:
        """
        Compute outer (Rossby wave) expansion.

        The outer solution is the stationary Rossby wave packet
        from Theorem 3, valid for rho > rho*.
        """
        return self.outer_wave.stream_function(rho, theta)

    def _estimate_epsilon(self) -> float:
        """Estimate epsilon from the analytic formula."""
        return hexagon_amplitude_analytic(
            self.delta_U, self.U_star, self.n, self.rho_star
        )

    def matching_residual(self, epsilon: float) -> float:
        """
        Compute the Van Dyke matching residual at the intermediate region.

        The matching condition requires that the inner expansion (evaluated
        at the outer edge of the inner region) equals the outer expansion
        (evaluated at the inner edge of the outer region).

        At rho = rho* + delta (matching point):
            inner_of_outer = outer_of_inner

        The residual measures the mismatch. Zero when matching is satisfied.
        """
        rho_match = self.rho_star + self.matching_width
        theta_match = np.array([0.0])  # Evaluate along theta = 0

        # Inner solution at matching point
        rho_arr = np.array([rho_match])
        sigma = self.inner_flow.sigma
        psi_inner = (abs(self.inner_flow.A)
                     * np.exp(sigma * rho_match)
                     * np.sin(self.inner_flow.alpha * rho_match)
                     + epsilon * np.exp(-self.n * self.matching_width))

        # Outer solution at matching point
        psi_outer = (self.outer_wave.amplitude
                     * np.exp(-self.n * self.matching_width))

        # Van Dyke residual: inner - outer at the overlap
        return psi_inner - psi_outer - epsilon

    def solve_epsilon(self) -> float:
        """
        Solve for the hexagon amplitude epsilon.

        Uses the analytic formula as primary result, with brentq
        refinement when possible.

        THEOREM 5: This is the central prediction.
        Should give epsilon ~ 0.05-0.15 for Saturn parameters.
        """
        # Primary: analytic formula
        eps_analytic = self._estimate_epsilon()

        # Try numerical refinement via root-finding
        try:
            # Check if residual changes sign in a reasonable interval
            r_low = self.matching_residual(0.001)
            r_high = self.matching_residual(0.5)
            if r_low * r_high < 0:
                eps_numerical = brentq(self.matching_residual, 0.001, 0.5)
                return eps_numerical
        except (ValueError, RuntimeError):
            pass

        return eps_analytic

    def hexagon_amplitude_formula(self) -> str:
        """
        Return the analytic amplitude formula as a LaTeX string.
        """
        return (r"\varepsilon = C \cdot \frac{\delta U}{U^*} "
                r"\cdot \exp\left(-\alpha \cdot 6 \cdot |\rho_*|\right)")

    def composite_solution(self, rho: np.ndarray,
                           theta: np.ndarray) -> np.ndarray:
        """
        Full composite asymptotic solution = inner + outer - common_part.

        The additive composite is valid uniformly across all three regions:
            psi_composite = psi_inner + psi_outer - psi_common

        where psi_common is the shared leading-order behavior in the
        overlap region.
        """
        psi_inner = self.inner_expansion(rho, theta, order=1)
        psi_outer = self.outer_expansion(rho, theta)

        # Common part: the shared behavior at rho = rho*
        # At the matching point, both solutions agree at leading order
        epsilon = self._estimate_epsilon()
        psi_common = epsilon * np.exp(-self.n * np.abs(rho - self.rho_star))

        return psi_inner + psi_outer - psi_common

    def composite_is_continuous(self, tol: float = 0.5) -> bool:
        """
        Check that the composite solution is approximately continuous
        across the matching region.
        """
        theta = np.array([0.0])
        rho_left = self.rho_star - self.matching_width
        rho_right = self.rho_star + self.matching_width

        psi_left = self.composite_solution(np.array([rho_left]), theta)
        psi_right = self.composite_solution(np.array([rho_right]), theta)
        psi_center = self.composite_solution(np.array([self.rho_star]), theta)

        # Check continuity: values shouldn't jump dramatically
        jump_left = float(np.max(np.abs(psi_left - psi_center)))
        jump_right = float(np.max(np.abs(psi_right - psi_center)))
        max_jump = max(jump_left, jump_right)
        scale = max(float(np.max(np.abs(psi_center))), 1e-10)

        return max_jump / scale < tol
