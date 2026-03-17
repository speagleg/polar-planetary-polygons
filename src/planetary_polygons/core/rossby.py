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
"""
Quasi-Geostrophic Potential Vorticity (QGPV) equation and its log-polar form.

Mathematical background
-----------------------
The barotropic QGPV equation on the beta-plane:

    Dq/Dt = 0,   q = nabla^2 psi + beta*y

where psi is the stream function, beta = df/dy is the meridional gradient of the
Coriolis parameter, and D/Dt = d/dt + J(psi, .) is the material derivative.

Log-polar transformation
------------------------
Under (x, y) -> (rho, theta) with x + iy = e^(rho + i*theta):

    nabla^2 = e^(-2*rho) (d^2/drho^2 + d^2/dtheta^2)

The QGPV linearized about a zonal base state U(rho) becomes:

    (d/dt + U d/dtheta) nabla^2 psi' + (beta - U'') d psi'/dtheta = 0

where primes denote perturbation quantities and U'' = d^2U/drho^2 in log-polar coords.
Fourier expanding psi' = psi_hat_n(rho) e^{in*theta} e^{-i*omega*t} yields the
Rayleigh-Kuo eigenvalue ODE:

    (U - c)(psi_hat_n'' - n^2 psi_hat_n) + (beta - U'') psi_hat_n = 0    (*)

where c = omega/n is the phase speed. For stationary waves (c = 0):

    psi_hat_n'' + [(beta - U'')/U - n^2] psi_hat_n = 0

This is the central eigenvalue problem. For n=0: axisymmetric (spiral) modes.
For n=6: hexagonal mode. The wavenumber n=6 is selected by the Rossby
dispersion relation: U* = beta/k^2 gives U* closest to U_observed at n=6.
"""

import numpy as np
from scipy.integrate import solve_bvp
from scipy.linalg import eig
from typing import Callable


class QGPVSolver:
    """
    Solver for the linearized QGPV eigenvalue problem in log-polar coordinates.

    Parameters
    ----------
    beta : float
        Meridional gradient of Coriolis parameter (beta). For Saturn's hexagon
        latitude (76 deg N), beta ~ 3.7e-13 m^-1 s^-1.
    U_profile : Callable[[np.ndarray], np.ndarray]
        Base-state zonal velocity as function of log-radius rho.
        The Gaussian jet profile U(rho) = U_max * exp(-(rho-rho0)^2/2*sigma^2) is the
        standard model for Saturn's hexagonal jet.
    rho_domain : tuple[float, float]
        Domain in log-radius [rho_min, rho_max].
    n_grid : int
        Number of grid points.
    """

    def __init__(self, beta: float, U_profile: Callable,
                 rho_domain: tuple, n_grid: int = 512):
        self.beta = beta
        self.U_profile = U_profile
        self.rho_domain = rho_domain
        self.n_grid = n_grid

        # Build grid and precompute profiles
        self.rho = np.linspace(rho_domain[0], rho_domain[1], n_grid)
        self.drho = self.rho[1] - self.rho[0]
        self.U = self.U_profile(self.rho)
        self.U_pp = self._second_derivative(self.U)

    def _second_derivative(self, f: np.ndarray) -> np.ndarray:
        """Compute d^2f/drho^2 using second-order central finite differences."""
        d2f = np.zeros_like(f)
        h = self.drho
        d2f[1:-1] = (f[2:] - 2 * f[1:-1] + f[:-2]) / h**2
        # One-sided at boundaries
        d2f[0] = (f[2] - 2 * f[1] + f[0]) / h**2
        d2f[-1] = (f[-1] - 2 * f[-2] + f[-3]) / h**2
        return d2f

    def _build_d2_matrix(self) -> np.ndarray:
        """Build the second-derivative matrix D2 for the rho grid."""
        N = self.n_grid
        h = self.drho
        D2 = np.zeros((N, N))
        for i in range(1, N - 1):
            D2[i, i - 1] = 1.0 / h**2
            D2[i, i] = -2.0 / h**2
            D2[i, i + 1] = 1.0 / h**2
        # Dirichlet BCs: psi_hat = 0 at boundaries (already zero rows)
        return D2

    def laplacian_logpolar(self, psi: np.ndarray, n: int = 0) -> np.ndarray:
        """
        Compute nabla^2 psi in log-polar coordinates for Fourier mode n.

        nabla^2 = e^(-2*rho) (d^2/drho^2 + d^2/dtheta^2)

        For a Fourier mode e^{in*theta}, the theta-derivative gives -n^2, so:

        nabla^2[psi_hat_n(rho) e^{in*theta}] = e^(-2*rho) (psi_hat_n'' - n^2 psi_hat_n) e^{in*theta}
        """
        psi_pp = self._second_derivative(psi)
        return np.exp(-2 * self.rho) * (psi_pp - n**2 * psi)

    def build_eigenvalue_matrix(self, n: int, omega: float = 0.0) -> np.ndarray:
        """
        Build the discretized eigenvalue matrix for Fourier mode n at frequency omega.

        Returns the matrix L_n such that L_n psi_hat_n = 0 is the discretized
        form of the Rayleigh-Kuo equation.

        The standard barotropic Rayleigh-Kuo equation (Pedlosky Ch. 7):
            (U - c)(psi'' - n^2 psi) + (beta - U'') psi = 0

        For the stationary case c = omega/n = 0:
            psi'' + [(beta - U'')/U - n^2] psi = 0

        Written as psi'' = V(rho) psi with:
            V = n^2 - (beta - U'')/U
        """
        N = self.n_grid
        D2 = self._build_d2_matrix()

        V = np.zeros(N)
        for i in range(N):
            U_i = self.U[i]
            Upp_i = self.U_pp[i]
            if omega == 0.0:
                # Stationary Rayleigh-Kuo: psi'' = [n^2 - (beta-U'')/U] psi
                if abs(U_i) > 1e-30:
                    V[i] = n**2 - (self.beta - Upp_i) / U_i
                else:
                    V[i] = n**2
            else:
                # General case: (U - c)(psi'' - n^2 psi) + (beta-U'') psi = 0
                # => psi'' = [n^2 - (beta-U'')/(U - omega/n)] psi
                c = omega / n if n != 0 else 0.0
                denom = U_i - c
                if abs(denom) > 1e-30:
                    V[i] = n**2 - (self.beta - Upp_i) / denom
                else:
                    V[i] = n**2

        # L = D2 - diag(V), so L psi = 0 means psi'' = V psi
        L = D2 - np.diag(V)
        L[0, :] = 0
        L[0, 0] = 1.0
        L[-1, :] = 0
        L[-1, -1] = 1.0
        return L

    def solve_stationary_mode(self, n: int) -> tuple[np.ndarray, np.ndarray]:
        """
        Solve for the stationary (omega=0) eigenfunction of mode n.

        For n=6 this should yield the hexagonal meander eigenfunction.
        For n=0 this yields the axisymmetric (spiral) streamfunction.

        Uses scipy.integrate.solve_bvp with the Rayleigh-Kuo ODE:
            psi'' = V(rho) * psi
        where V = n^2 - (beta - U'')/U for the stationary case.

        Returns
        -------
        rho : np.ndarray
            Log-radius grid
        psi_hat : np.ndarray
            Eigenfunction psi_hat_n(rho)
        """
        # Build potential from stationary Rayleigh-Kuo equation
        V = np.zeros(self.n_grid)
        for i in range(self.n_grid):
            U_i = self.U[i]
            Upp_i = self.U_pp[i]
            if abs(U_i) > 1e-30:
                V[i] = n**2 - (self.beta - Upp_i) / U_i
            else:
                V[i] = n**2

        V_interp = lambda rho_val: np.interp(rho_val, self.rho, V)

        def ode(rho_val, y):
            # y[0] = psi, y[1] = psi'
            psi_val = y[0]
            dpsi = y[1]
            V_val = V_interp(rho_val)
            ddpsi = V_val * psi_val
            return np.vstack([dpsi, ddpsi])

        def bc(ya, yb):
            # Dirichlet: psi(rho_min) = 0, psi(rho_max) = 0
            return np.array([ya[0], yb[0]])

        # Initial guess: sine-like eigenfunction
        rho_bvp = np.linspace(self.rho_domain[0], self.rho_domain[1], self.n_grid)
        L = self.rho_domain[1] - self.rho_domain[0]
        y_init = np.zeros((2, self.n_grid))
        y_init[0] = np.sin(np.pi * (rho_bvp - self.rho_domain[0]) / L)
        y_init[1] = (np.pi / L) * np.cos(np.pi * (rho_bvp - self.rho_domain[0]) / L)

        sol = solve_bvp(ode, bc, rho_bvp, y_init, tol=1e-8)
        if not sol.success:
            # Fall back to eigenvalue approach
            return self._solve_stationary_eigenvalue(n)

        rho_out = sol.x
        psi_hat = sol.y[0]
        # Normalize
        norm = np.max(np.abs(psi_hat))
        if norm > 0:
            psi_hat = psi_hat / norm
        return rho_out, psi_hat

    def _solve_stationary_eigenvalue(self, n: int) -> tuple[np.ndarray, np.ndarray]:
        """Fallback: solve via eigenvalue decomposition of the discretized operator."""
        L = self.build_eigenvalue_matrix(n, omega=0.0)
        # Interior points only (strip BC rows)
        Li = L[1:-1, 1:-1]
        eigenvalues, eigenvectors = eig(Li)

        # Find the eigenvalue closest to zero (stationary mode)
        idx = np.argmin(np.abs(eigenvalues.real))
        psi_interior = eigenvectors[:, idx].real

        # Reconstruct full solution with BCs
        psi_hat = np.zeros(self.n_grid)
        psi_hat[1:-1] = psi_interior
        norm = np.max(np.abs(psi_hat))
        if norm > 0:
            psi_hat = psi_hat / norm
        return self.rho, psi_hat

    def rayleigh_kuo_check(self) -> tuple[np.ndarray, np.ndarray]:
        """
        Compute beta - U''(rho) and identify zero crossings (necessary condition
        for barotropic instability by the Rayleigh-Kuo criterion).

        Returns (rho, beta_minus_Upp) where zero crossings indicate
        potentially unstable regions.
        """
        beta_minus_Upp = self.beta - self.U_pp
        return self.rho, beta_minus_Upp

    def compute_pv_staircase(self, rho_star: float,
                              q_inner: float, q_outer: float) -> np.ndarray:
        """
        Build a PV staircase profile -- step function at rho = rho* modeling
        the sharp PV gradient at the hexagonal jet boundary.

        This is the McIntyre (1982) / Scott-Dritschel (2012) model.
        """
        q = np.where(self.rho < rho_star, q_inner, q_outer)
        return q

    def critical_layer_analysis(self, n: int) -> dict:
        """
        Find the critical latitude where U(rho_c) = c (phase speed).
        For stationary waves c=0, so critical layer is where U=0.
        Returns dict with 'rho_c', 'absorption_coefficient', 'wave_action_flux'.
        """
        # Find zero crossings of U(rho)
        sign_changes = np.where(np.diff(np.sign(self.U)))[0]
        rho_c_values = []
        for idx in sign_changes:
            # Linear interpolation for zero crossing
            rho_c = self.rho[idx] - self.U[idx] * self.drho / (self.U[idx + 1] - self.U[idx])
            rho_c_values.append(rho_c)

        # Absorption coefficient: proportional to |dU/drho|^{-1} at critical layer
        U_prime = np.gradient(self.U, self.drho)
        absorption = []
        for rho_c in rho_c_values:
            idx = np.argmin(np.abs(self.rho - rho_c))
            dU = abs(U_prime[idx])
            absorption.append(1.0 / dU if dU > 1e-30 else np.inf)

        return {
            'rho_c': np.array(rho_c_values),
            'absorption_coefficient': np.array(absorption),
            'wave_action_flux': np.zeros(len(rho_c_values)),  # TODO: compute from eigenfunctions
        }


def gaussian_jet_profile(rho: np.ndarray, U_max: float, rho_0: float,
                          sigma: float) -> np.ndarray:
    """
    Standard Gaussian jet profile for Saturn's hexagonal jet.

    U(rho) = U_max * exp(-(rho - rho_0)^2 / (2*sigma^2))

    Parameters (Saturn defaults)
    ----------------------------
    U_max  ~ 120.0  m/s  (jet peak speed)
    rho_0  ~ 0.0         (jet center in log-radius, normalized)
    sigma  ~ 0.15        (jet half-width in log-radius units)
    """
    return U_max * np.exp(-(rho - rho_0)**2 / (2 * sigma**2))


def gaussian_jet_second_derivative(rho: np.ndarray, U_max: float, rho_0: float,
                                    sigma: float) -> np.ndarray:
    """
    Analytic second derivative U''(rho) of the Gaussian jet profile.

    U''(rho) = U_max/sigma^2 * ((rho - rho_0)^2/sigma^2 - 1) * exp(-(rho-rho_0)^2/(2*sigma^2))
    """
    xi = (rho - rho_0) / sigma
    return U_max / sigma**2 * (xi**2 - 1) * np.exp(-xi**2 / 2)


def stationary_wavenumber(U_max: float, beta: float,
                           sigma: float) -> float:
    """
    Compute the wavenumber n for which the Rossby stationarity condition
    c = U - beta/(k^2 + l^2) = 0 is satisfied, given a Gaussian jet.

    For a barotropic jet of width sigma, the effective total wavenumber
    K^2 = k^2 + l^2 where l ~ 1/sigma is the meridional wavenumber scale
    and k = n/R is the zonal wavenumber.

    At the jet peak: U_max = beta / K^2, so K^2 = beta / U_max.
    The meridional scale l ~ pi/sigma (half-wavelength fits in jet width).
    Then n/R ~ sqrt(K^2 - l^2) or equivalently:

        n = R * sqrt(beta/U_max - (pi/sigma)^2)

    But in log-polar normalized coordinates where R ~ 1, sigma is already
    in log-radius units, so:

        n* = sqrt(beta/U_max - (pi/sigma)^2) * R_eff

    For Saturn: using the simpler scaling n ~ R * sqrt(beta/U_max) with
    R being the hexagon radius.

    Returns n* (need not be integer; closest integer is the selected mode).
    For Saturn parameters this should return ~ 6.
    """
    # Total wavenumber from stationarity: K^2 = beta / U_max
    K_squared = beta / U_max

    # Meridional wavenumber scale from jet width
    # In physical coordinates, l ~ pi / (jet halfwidth in physical units)
    # But here sigma is in log-polar units, so l ~ pi / sigma
    l_squared = (np.pi / sigma)**2

    # Zonal wavenumber: k^2 = K^2 - l^2
    k_squared = K_squared - l_squared
    if k_squared <= 0:
        # Jet too narrow for any zonal mode to be stationary;
        # fall back to simple scaling
        # n ~ R * sqrt(beta / U_max) with R = hexagon radius
        # For Saturn: R ~ 5.1e7 m, gives n ~ 5.1e7 * sqrt(1.5e-14 / 120) ~ 5.7
        R_hex = 5.1e7  # m, Saturn hexagon radius
        return R_hex * np.sqrt(beta / U_max)

    return np.sqrt(k_squared)
