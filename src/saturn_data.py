"""
Saturn observational parameters and three-epoch hexagon data.

Sources
-------
Godfrey 1988        (Voyager 1 & 2, 1980-81)
Sanchez-Lavega et al. 1993, 1997  (1990-91)
Sanchez-Lavega et al. 2014        (Cassini 2008-14)
Barbosa Aguiar et al. 2010        (Lab experiments)

All angular velocities in degrees/day; periods in seconds.
"""

import numpy as np
from dataclasses import dataclass, field


@dataclass
class SaturnParameters:
    """Fundamental Saturn physical parameters."""

    # Planet
    rotation_rate: float = 1.638e-4      # rad/s, sidereal
    equatorial_radius: float = 6.0268e7  # m
    polar_radius: float = 5.4364e7       # m

    # Hexagon location
    hexagon_latitude: float = 76.0       # degrees North
    hexagon_radius: float = 5.1e7        # m (physical radius at 76 deg N)

    # Jet parameters
    jet_speed_peak: float = 120.0        # m/s (Cassini 2008-14)
    jet_halfwidth: float = 2.5e6         # m

    # Equivalent depth for barotropic mode
    equivalent_depth: float = 1.0e4      # m (order of magnitude estimate)
    gravity: float = 10.44               # m/s^2, Saturn surface gravity

    @property
    def beta(self) -> float:
        """beta = 2*Omega*cos(phi) / R at hexagon latitude."""
        phi = np.radians(self.hexagon_latitude)
        return 2 * self.rotation_rate * np.cos(phi) / self.polar_radius

    @property
    def coriolis_f(self) -> float:
        """f = 2*Omega*sin(phi) at hexagon latitude."""
        phi = np.radians(self.hexagon_latitude)
        return 2 * self.rotation_rate * np.sin(phi)

    @property
    def rossby_radius(self) -> float:
        """L_R = sqrt(gH) / f where f = 2*Omega*sin(phi)."""
        return np.sqrt(self.gravity * self.equivalent_depth) / self.coriolis_f

    @property
    def jet_sigma_logpolar(self) -> float:
        """Jet half-width in log-polar units: sigma = L_jet / R_hex."""
        return self.jet_halfwidth / self.hexagon_radius


@dataclass
class EpochData:
    """Observational data for one observation epoch."""
    name: str
    years: str
    hexagon_omega: float         # deg/day, negative = westward
    hexagon_omega_err: float
    hexagon_period: float        # seconds
    hexagon_period_err: float
    nps_omega: float | None      # None if NPS absent
    nps_omega_err: float | None
    nps_period: float | None
    nps_present: bool
    source: str


# -- Three observation epochs --------------------------------------------------

EPOCH_1980_81 = EpochData(
    name="Voyager 1980-81",
    years="1980-1981",
    hexagon_omega=-0.0602,
    hexagon_omega_err=0.014,
    hexagon_period=10*3600 + 39*60 + 19.6,  # 10h 39m 19.6s in seconds
    hexagon_period_err=0.7,
    nps_omega=-0.0444,
    nps_omega_err=0.010,
    nps_period=10*3600 + 39*60 + 20.3,
    nps_present=True,
    source="Godfrey 1988; Sanchez-Lavega et al. 1997, 1993"
)

EPOCH_1990_91 = EpochData(
    name="Ground-based 1990-91",
    years="1990-1991",
    hexagon_omega=-0.0010,
    hexagon_omega_err=0.007,
    hexagon_period=10*3600 + 39*60 + 23.5,  # approximate, verify from paper
    hexagon_period_err=2.0,                  # larger uncertainty, fewer data
    nps_omega=None,                          # NPS weaker, less well measured
    nps_omega_err=None,
    nps_period=None,
    nps_present=True,   # Present but weaker
    source="Sanchez-Lavega et al. 1993"
)

EPOCH_2008_14 = EpochData(
    name="Cassini 2008-14",
    years="2008-2014",
    hexagon_omega=-0.0361,                   # From Sanchez-Lavega et al. 2014 Table 1
    hexagon_omega_err=0.01,                  # Approximate -- verify from paper
    hexagon_period=10*3600 + 39*60 + 23.01,
    hexagon_period_err=0.01,
    nps_omega=None,
    nps_omega_err=None,
    nps_period=None,
    nps_present=False,
    source="Sanchez-Lavega et al. 2014"
)

ALL_EPOCHS = [EPOCH_1980_81, EPOCH_1990_91, EPOCH_2008_14]


def intrinsic_drift_rate() -> tuple[float, float]:
    """
    Estimate the intrinsic hexagon drift (absent NPS perturbation).

    Uses the 2008-14 epoch as the best estimate of unperturbed drift.
    Returns (omega_intrinsic, uncertainty).

    The near-zero 1990-91 value suggests partial NPS cancellation of
    the intrinsic drift -- interesting dynamical constraint.
    """
    return EPOCH_2008_14.hexagon_omega, EPOCH_2008_14.hexagon_omega_err


def nps_coupling_coefficient() -> tuple[float, float]:
    """
    Estimate gamma from the linear perturbation model:

        omega_hex = omega_intrinsic + gamma * omega_NPS

    Using 1980-81 data (NPS present, strong coupling) and 2008-14
    (NPS absent, intrinsic drift only).

    Returns (gamma, uncertainty).
    This is the empirical test of Theorem 3's perturbation prediction.
    """
    omega_0, omega_0_err = intrinsic_drift_rate()

    # From 1980-81: omega_hex = omega_0 + gamma * omega_NPS
    # gamma = (omega_hex - omega_0) / omega_NPS
    omega_hex_80 = EPOCH_1980_81.hexagon_omega
    omega_nps_80 = EPOCH_1980_81.nps_omega

    gamma = (omega_hex_80 - omega_0) / omega_nps_80

    # Propagate uncertainty
    sigma_num = np.sqrt(EPOCH_1980_81.hexagon_omega_err**2 + omega_0_err**2)
    gamma_err = abs(gamma) * np.sqrt(
        (sigma_num / (omega_hex_80 - omega_0))**2
        + (EPOCH_1980_81.nps_omega_err / omega_nps_80)**2
    )

    return gamma, gamma_err


def near_resonance_period() -> float:
    """
    Compute the period of relative motion between hexagon and NPS in 1980-81.

    T_rel = 360 / |omega_hex - omega_NPS| days

    This should give ~62 years -- the near-resonance identified in the analysis.
    """
    omega_hex = EPOCH_1980_81.hexagon_omega
    omega_nps = EPOCH_1980_81.nps_omega
    return 360.0 / abs(omega_hex - omega_nps) / 365.25  # in years


def rossby_number_at_jet() -> float:
    """
    Ro = U / (f * L) where f = 2*Omega*sin(phi), L is jet halfwidth.

    Note: Ro ~ 0.15 for Saturn, meaning the flow is strongly geostrophic.
    The Mobius parameter sigma is NOT directly derived from Ro; instead
    it comes from the jet excess delta_U/U* (see mobius_sigma_from_jet).
    """
    saturn = SaturnParameters()
    return saturn.jet_speed_peak / (saturn.coriolis_f * saturn.jet_halfwidth)


def mobius_sigma_kinematic(epsilon_hex: float = 0.05) -> dict:
    """
    Compute the Mobius parameter sigma from the KINEMATIC identification.

    THEOREM 2 identification:
    The loxodromic stream function psi = |A| e^{sigma*rho} sin(alpha*rho + sigma*theta)
    produces a velocity field with radial-to-azimuthal ratio |u_r/u_theta| = |sigma/alpha|.

    For the hexagonal jet boundary r(theta) = R(1 + epsilon*cos(n*theta)):
        |u_r/u_theta|_rms = n*epsilon / sqrt(2)

    Therefore:
        sigma = alpha * n * epsilon / sqrt(2)

    This is OBSERVATIONAL: sigma is determined by the measured hexagon
    meander amplitude epsilon, not assumed from dynamical arguments.

    Parameters
    ----------
    epsilon_hex : float
        Hexagon meander amplitude (ratio of deviation to mean radius).
        Observed range: 0.03-0.10. Default 0.05 (conservative).

    Returns dict with sigma, r, and supporting quantities.
    """
    n = 6
    alpha = np.pi / 3  # 2*pi/n for n=6

    # Velocity ratio from hexagonal boundary geometry
    velocity_ratio_rms = n * epsilon_hex / np.sqrt(2)

    # Kinematic identification
    sigma = alpha * velocity_ratio_rms
    r = np.exp(sigma)

    # Also compute the jet excess for comparison
    saturn = SaturnParameters()
    k = n / saturn.hexagon_radius
    beta = saturn.beta
    U_star = beta / k**2
    delta_U = saturn.jet_speed_peak - U_star

    return {
        'sigma': sigma,
        'r': r,
        'epsilon_hex': epsilon_hex,
        'velocity_ratio_rms': velocity_ratio_rms,
        'alpha': alpha,
        'U_star': U_star,
        'delta_U': delta_U,
        'sigma_jet_excess': delta_U / U_star,
    }
