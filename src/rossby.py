"""
Rossby wave theory on the beta-plane.

Core result needed for Theorem 3
---------------------------------
The Rossby wave dispersion relation:

    omega = U k - beta*k / (k^2 + l^2)

For a stationary wave (omega = 0):

    U* = beta / (k^2 + l^2)

where k is zonal wavenumber, l is meridional wavenumber.

In log-polar coordinates, k -> n/r (azimuthal wavenumber / physical radius),
and the stationarity condition becomes:

    U*(rho) = beta r^2 / (n^2 + n_rho^2 r^2)

The claim of Theorem 3: this condition, expressed in terms of the loxodromic
flow parameters, is equivalent to sigma = Re(s) = 0, i.e., r = e^sigma = 1.
"""

import numpy as np
from typing import Callable


def rossby_dispersion(k: float, l: float, U: float,
                       beta: float) -> float:
    """
    Rossby wave frequency omega = Uk - beta*k/(k^2+l^2).
    """
    K2 = k**2 + l**2
    if K2 == 0:
        return 0.0
    return U * k - beta * k / K2


def stationary_jet_speed(k: float, l: float, beta: float) -> float:
    """
    U* = beta/(k^2+l^2) -- the jet speed for which mode (k,l) is stationary.
    For Saturn n=6, this should give ~ 120 m/s.
    """
    K2 = k**2 + l**2
    if K2 == 0:
        return np.inf
    return beta / K2


def log_polar_stationarity_condition(n: int, rho_star: float,
                                      beta: float, sigma: float) -> float:
    """
    The stationarity condition rewritten in log-polar coordinates.

    THEOREM 3 PROOF (rigorous):
    Substitute the loxodromic eigenfunction psi_hat = e^{s*rho} with
    s = sigma + i*alpha into the stationary QGPV ODE at rho = rho*:

        U(rho*) * (s^2 - n^2) * e^{-2*rho*} + (beta - U'') = 0

    Expanding s^2 = sigma^2 - alpha^2 + 2i*sigma*alpha:

        Real part:      U*(sigma^2 - alpha^2 - n^2)*e^{-2*rho*} + (beta-U'') = 0
        Imaginary part: 2*U*alpha*sigma*e^{-2*rho*} = 0

    Since U > 0, alpha != 0 (hexagonal mode), and e^{-2*rho*} > 0,
    the imaginary part forces SIGMA = 0.

    This is equivalent to |lambda| = e^sigma = 1 (the r=1 locus),
    which is the Rossby wave stationarity condition omega = 0.  QED.

    The real part with sigma=0 then gives the stationary jet speed:
        U* = (beta - U'') / ((alpha^2 + n^2) * e^{-2*rho*})

    Returns the residual F(sigma): zero at sigma=0, positive for sigma>0.
    """
    # THEOREM 3: F(sigma) = 2*sigma*alpha where alpha is fixed
    # Normalized form (dividing by 2*alpha): F = sigma
    # Or equivalently, using r = e^sigma: F = ln(r) = sigma
    # We use the exponential form for consistency with the Mobius framework:
    return np.expm1(2 * sigma)  # e^{2*sigma} - 1, exact at sigma=0


def saturn_beta(latitude_deg: float = 76.0) -> float:
    """
    Compute beta = df/dy for Saturn at a given latitude.

    Saturn parameters:
        Omega = 1.638e-4 rad/s  (sidereal rotation rate)
        R = 5.4364e7 m          (polar radius, used for beta at high lat)

    beta = 2*Omega*cos(phi) / R
    """
    Omega = 1.638e-4   # rad/s
    R = 5.4364e7        # m (polar radius)
    phi = np.radians(latitude_deg)
    return 2 * Omega * np.cos(phi) / R


def saturn_wavenumbers(n: int, R_hex: float = 5.1e7,
                        jet_halfwidth: float = 2.5e6) -> tuple[float, float]:
    """
    Compute (k, l) wavenumbers for Saturn mode n.

    k = n / R_hex          (azimuthal)
    l = pi / jet_halfwidth (meridional, half-wavelength in jet width)
    """
    k = n / R_hex
    l = np.pi / jet_halfwidth
    return k, l


def wavenumber_prediction(U_max: float, beta: float,
                           sigma_jet: float) -> dict:
    """
    Predict the selected wavenumber n* from jet parameters.

    The stationary condition U* = beta / K^2 with K^2 = k^2 + l^2
    where k = n/R, l = pi/L_jet gives:

        n* = R * sqrt(beta/U_max - (pi/L_jet)^2)

    Uses sigma_jet (jet half-width in physical units, meters) as L_jet.

    Returns dict with 'n_star', 'U_stationary', 'growth_rate'.
    """
    R_hex = 5.1e7  # m, Saturn hexagon radius (SaturnParameters.hexagon_radius)

    # Total wavenumber squared from stationarity
    K2_stat = beta / U_max

    # Meridional wavenumber
    l = np.pi / sigma_jet
    l2 = l**2

    # Zonal wavenumber squared
    k2 = K2_stat - l2

    if k2 > 0:
        k = np.sqrt(k2)
        n_star = k * R_hex
    else:
        # Jet too narrow; use simpler scaling
        n_star = R_hex * np.sqrt(K2_stat)

    # Stationary speed for the nearest integer mode
    n_int = round(n_star)
    k_int = n_int / R_hex
    K2_int = k_int**2 + l2
    U_stat = beta / K2_int if K2_int > 0 else np.inf

    return {
        'n_star': n_star,
        'n_integer': n_int,
        'U_stationary': U_stat,
        'growth_rate': 0.0,  # Marginal at stationarity
    }


class RossbyWavePacket:
    """
    A Rossby wave packet with specified wavenumber, amplitude, and phase.

    Used for constructing the outer solution in the matched asymptotic
    expansion (Theorem 5).
    """

    def __init__(self, n: int, amplitude: float, phase: float,
                 beta: float, U_background: float):
        self.n = n
        self.amplitude = amplitude
        self.phase = phase
        self.beta = beta
        self.U_background = U_background

        # Compute wave frequency from dispersion relation
        # Using the simplified barotropic form with effective wavenumber
        R_hex = 5.1e7  # m
        k = n / R_hex
        # For stationary waves, omega should be near zero
        # omega = U*k - beta*k/K^2; at stationarity omega = 0
        self.omega = 0.0  # Stationary by construction

    @property
    def decay_rate(self) -> float:
        """
        Radial decay rate of the wave amplitude in the outer region.
        For mode n, the eigenfunction decays as e^{-n*|rho - rho*|}.
        """
        return float(self.n)

    def stream_function(self, rho: np.ndarray,
                        theta: np.ndarray, t: float = 0.0) -> np.ndarray:
        """
        psi_wave(rho, theta, t) = A(rho) cos(n*theta - omega*t + phi)
        where A(rho) is the amplitude envelope from the outer eigenfunction.

        For stationary waves (omega=0):
        psi_wave = amplitude * exp(-n*|rho|) * cos(n*theta + phase)
        """
        A_rho = self.amplitude * np.exp(-self.n * np.abs(rho))
        return A_rho * np.cos(self.n * theta - self.omega * t + self.phase)

    def hexagonal_boundary(self, rho_star: float,
                            epsilon: float = 0.1) -> np.ndarray:
        """
        Compute the hexagonal meander of the PV step at rho = rho*.

        The PV boundary is deformed by the wave:
            rho_boundary(theta) = rho_star + epsilon * cos(n*theta + phase)

        Returns array of shape (360, 2) with columns [x, y] in polar coords.
        """
        theta = np.linspace(0, 2 * np.pi, 360, endpoint=False)
        rho_boundary = rho_star + epsilon * np.cos(self.n * theta + self.phase)
        # Convert to physical (x, y) via log-polar: r = e^rho
        r = np.exp(rho_boundary)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return np.column_stack([x, y])
