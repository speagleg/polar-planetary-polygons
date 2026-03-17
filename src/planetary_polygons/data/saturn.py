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
"""
Cassini-era Saturn zonal wind profile at high northern latitudes.

Sources
-------
Sanchez-Lavega et al. 2014, GRL 41, 1425-1431 (hexagon drift, jet structure)
Antunano et al. 2015, JGR-Planets 120, 155-176 (Cassini/ISS wind profiles)
Garcia-Melendo & Sanchez-Lavega 2001, Icarus 152, 316-330 (pre-Cassini)
Read et al. 2009, PSS 57, 1682-1698 (hexagonal jet dynamics)

Data below are digitized from published figures (primarily Antunano et al.
2015 Fig. 7 and Sanchez-Lavega et al. 2014 Fig. 1). Planetographic latitudes.
Wind speeds are zonal (eastward positive), relative to System III rotation.

NOTE: For publication, obtain digital data directly from authors or
use the Cassini PDS archive. These values are approximate digitizations.
"""

import numpy as np
from dataclasses import dataclass
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize_scalar


# Zonal wind profile near the hexagonal jet (70-82 deg N)
# Digitized from Antunano et al. 2015 Fig. 7 (Cassini/ISS 2008-2014)
# Format: (planetographic_latitude_deg, zonal_wind_ms)
CASSINI_WIND_PROFILE_RAW = np.array([
    # lat (deg N),  U (m/s)
    [70.0,   15.0],
    [71.0,   25.0],
    [72.0,   40.0],
    [73.0,   55.0],
    [74.0,   75.0],
    [75.0,   95.0],
    [75.5,  105.0],
    [76.0,  115.0],
    [76.5,  120.0],  # Peak of hexagonal jet
    [77.0,  118.0],
    [77.5,  110.0],
    [78.0,   95.0],
    [78.5,   80.0],
    [79.0,   60.0],
    [80.0,   30.0],
    [81.0,   10.0],
    [82.0,   -5.0],
])


@dataclass
class CassiniWindProfile:
    """
    Interpolated Cassini zonal wind profile near Saturn's hexagonal jet.

    The profile is a cubic spline fit to digitized data from
    Antunano et al. 2015. For the hexagonal jet region (70-82 deg N).
    """
    latitudes: np.ndarray  # planetographic degrees N
    winds: np.ndarray      # zonal wind, m/s
    _spline: CubicSpline = None

    def __post_init__(self):
        self._spline = CubicSpline(self.latitudes, self.winds)

    def __call__(self, lat: float | np.ndarray) -> float | np.ndarray:
        """Evaluate wind speed at latitude(s)."""
        return self._spline(lat)

    @property
    def peak_latitude(self) -> float:
        """Latitude of jet peak (degrees N)."""
        result = minimize_scalar(lambda x: -self._spline(x),
                                  bounds=(74, 80), method='bounded')
        return result.x

    @property
    def peak_speed(self) -> float:
        """Peak zonal wind speed (m/s)."""
        return float(self._spline(self.peak_latitude))

    @property
    def jet_halfwidth_deg(self) -> float:
        """Jet half-width at half-maximum (degrees latitude)."""
        half_max = self.peak_speed / 2
        lat_peak = self.peak_latitude

        # Find where wind drops to half-max on each side
        from scipy.optimize import brentq
        try:
            lat_south = brentq(lambda x: self._spline(x) - half_max,
                               70.0, lat_peak)
            lat_north = brentq(lambda x: self._spline(x) - half_max,
                               lat_peak, 82.0)
            return (lat_north - lat_south) / 2
        except ValueError:
            return 2.5  # fallback estimate

    @property
    def jet_halfwidth_m(self) -> float:
        """Jet half-width converted to meters."""
        # 1 degree of latitude on Saturn ~ pi * R_polar / 180
        R_polar = 5.4364e7  # m
        deg_to_m = np.pi * R_polar / 180
        return self.jet_halfwidth_deg * deg_to_m

    def second_derivative_at_peak(self) -> float:
        """U''(lat_peak) in m/s per degree^2."""
        lat = self.peak_latitude
        return float(self._spline(lat, 2))

    def to_logpolar(self, rho_center: float = 0.0) -> tuple[np.ndarray, np.ndarray]:
        """
        Convert wind profile to log-polar coordinates centered on the jet.

        Returns (rho, U) where rho = 0 is the jet peak.
        The conversion uses: rho = (lat - lat_peak) * (pi*R_polar/180) / R_hex
        where R_hex is the hexagonal jet radius.
        """
        R_polar = 5.4364e7
        R_hex = 5.1e7
        deg_to_rho = np.pi * R_polar / (180 * R_hex)

        lat_peak = self.peak_latitude
        rho = (self.latitudes - lat_peak) * deg_to_rho + rho_center
        return rho, self.winds


def load_cassini_profile() -> CassiniWindProfile:
    """Load the standard Cassini wind profile."""
    data = CASSINI_WIND_PROFILE_RAW
    return CassiniWindProfile(latitudes=data[:, 0], winds=data[:, 1])


def measure_delta_U(profile: CassiniWindProfile = None) -> dict:
    """
    Measure delta_U / U* from the Cassini wind profile.

    This is the KEY OBSERVATIONAL MEASUREMENT for the paper.

    U_observed = peak jet speed from Cassini
    U* = stationary jet speed from Rossby dispersion (beta / k^2)
    delta_U = U_observed - U*
    """
    if profile is None:
        profile = load_cassini_profile()

    from planetary_polygons.core.rossby import stationary_jet_speed

    saturn = SaturnParameters()

    # Measured values from Cassini
    U_obs = profile.peak_speed
    lat_peak = profile.peak_latitude
    hw_deg = profile.jet_halfwidth_deg
    hw_m = profile.jet_halfwidth_m

    # Compute U* from Rossby stationarity
    k = 6 / saturn.hexagon_radius  # n=6 zonal wavenumber
    beta = saturn.beta
    U_star = stationary_jet_speed(k, 0, beta)

    # The key ratio
    delta_U = U_obs - U_star
    ratio = delta_U / U_star

    # Compare Gaussian fit with actual profile
    from planetary_polygons.core.rossby import gaussian_jet_profile
    sigma_logpolar = hw_m / saturn.hexagon_radius
    rho_grid = np.linspace(-0.2, 0.2, 100)
    U_gaussian = gaussian_jet_profile(rho_grid, U_obs, 0.0, sigma_logpolar)

    rho_cassini, U_cassini = profile.to_logpolar()
    # Interpolate Cassini to same grid for comparison
    U_cassini_interp = np.interp(rho_grid, rho_cassini, U_cassini,
                                  left=0, right=0)

    rms_error = np.sqrt(np.mean((U_gaussian - U_cassini_interp)**2))
    relative_rms = rms_error / U_obs

    return {
        'U_observed': U_obs,
        'U_star': U_star,
        'delta_U': delta_U,
        'delta_U_over_Ustar': ratio,
        'peak_latitude': lat_peak,
        'jet_halfwidth_deg': hw_deg,
        'jet_halfwidth_m': hw_m,
        'gaussian_rms_error_ms': rms_error,
        'gaussian_relative_rms': relative_rms,
    }


def measure_hexagon_epsilon() -> dict:
    """
    Measure the hexagon meander amplitude epsilon from geometry.

    The hexagon vertices deviate from a circle by an amount that
    defines epsilon = (max_radius - min_radius) / (2 * mean_radius).

    From Cassini images (Sanchez-Lavega et al. 2014):
    - Hexagon mean latitude: ~76.5 deg N
    - Hexagon vertices span roughly 75-78 deg N
    - This is a ~3 degree meander in latitude
    """
    R_polar = 5.4364e7  # m
    deg_to_m = np.pi * R_polar / 180

    # From Cassini observations
    lat_mean = 76.5  # degrees N
    lat_inner = 75.0  # approximate inner vertex latitude
    lat_outer = 78.0  # approximate outer vertex latitude

    # Physical distances
    r_mean = R_polar * np.cos(np.radians(lat_mean))  # ~ 12,700 km
    delta_lat = (lat_outer - lat_inner) / 2  # ~ 1.5 degrees
    delta_r = delta_lat * deg_to_m  # ~ 1,420 km

    epsilon = delta_r / r_mean

    # Also compute from the hexagonal shape directly
    # A regular hexagon inscribed in a circle of radius R has
    # vertices at distance R from center, edges at R*cos(30) = R*sqrt(3)/2
    # So epsilon_regular = 1 - sqrt(3)/2 = 0.134
    epsilon_regular_hexagon = 1 - np.sqrt(3) / 2

    return {
        'lat_mean': lat_mean,
        'lat_inner': lat_inner,
        'lat_outer': lat_outer,
        'meander_deg': delta_lat,
        'meander_m': delta_r,
        'r_mean_m': r_mean,
        'epsilon_observed': epsilon,
        'epsilon_regular_hexagon': epsilon_regular_hexagon,
    }
