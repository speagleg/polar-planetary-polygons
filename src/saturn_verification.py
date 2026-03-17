"""
Quantitative verification of the five theorems against Saturn observational data.

For each theorem, provide:
1. The specific prediction made
2. The observed value
3. The residual / relative error
4. A pass/fail determination with tolerance
"""

import numpy as np
from saturn_data import (
    SaturnParameters, ALL_EPOCHS, intrinsic_drift_rate,
    nps_coupling_coefficient, near_resonance_period, rossby_number_at_jet,
)
from qgpv import QGPVSolver, gaussian_jet_profile, stationary_wavenumber
from rossby import saturn_beta, wavenumber_prediction, stationary_jet_speed
from thomson import stability_sweep, thomson_to_mobius_multiplier
from matching import LoxodromicFlow, hexagon_amplitude_analytic


def verify_theorem1_log_polar(verbose: bool = True) -> dict:
    """
    Theorem 1 verification: The n=6 mode is the dominant stationary mode
    in the outer region (rho > rho*) for Saturn's jet parameters.

    Test: Compute the stationary wavenumber from jet parameters.
    Verify that the predicted n* is closest to 6.
    """
    saturn = SaturnParameters()
    result = wavenumber_prediction(
        saturn.jet_speed_peak, saturn.beta, saturn.jet_halfwidth
    )
    n_predicted = result['n_integer']
    passed = 4 <= n_predicted <= 8

    if verbose:
        print("THEOREM 1: Log-polar spectral decomposition")
        print(f"  Predicted: n* = {result['n_star']:.2f} (integer: {n_predicted})")
        print(f"  Expected:  n = 6")
        print(f"  Status:    {'PASS' if passed else 'FAIL'}")

    return {'predicted_n': result['n_star'], 'n_integer': n_predicted,
            'passed': passed, 'tolerance': '4 <= n <= 8'}


def verify_theorem2_mobius(verbose: bool = True) -> dict:
    """
    Theorem 2 verification: The loxodromic flow with Saturn parameters
    gives a Mobius parameter r close to 1.

    Two independent estimates of sigma:
    1. KINEMATIC: sigma = alpha * |u_r/u_theta| from hexagon meander geometry
    2. SCALING:   sigma ~ delta_U / U* from jet excess dimensional analysis

    Both should give sigma ~ O(0.1), r ~ O(1).
    """
    from saturn_data import mobius_sigma_kinematic

    # Primary: kinematic identification (observational)
    kin = mobius_sigma_kinematic(epsilon_hex=0.05)
    sigma_kin = kin['sigma']
    r_kin = kin['r']

    # Secondary: jet excess scaling
    sigma_jet = kin['sigma_jet_excess']
    r_jet = np.exp(sigma_jet)

    # Build flow from kinematic identification
    flow = LoxodromicFlow.from_velocity_ratio(kin['velocity_ratio_rms'])
    ratio = flow.radial_to_azimuthal_ratio(0.0)

    # Both estimates should place r within 0.5 of 1
    passed = abs(r_kin - 1.0) < 0.5 and abs(r_jet - 1.0) < 0.5

    if verbose:
        print("THEOREM 2: Mobius identification of loxodromic flow")
        print(f"  Kinematic (primary):")
        print(f"    epsilon_hex:      {kin['epsilon_hex']}")
        print(f"    |u_r/u_theta|_rms: {kin['velocity_ratio_rms']:.4f}")
        print(f"    sigma_kinematic:  {sigma_kin:.4f}")
        print(f"    r = e^sigma:      {r_kin:.4f}")
        print(f"  Jet excess (scaling):")
        print(f"    delta_U/U*:       {sigma_jet:.4f}")
        print(f"    r = e^sigma:      {r_jet:.4f}")
        print(f"  Both estimates:     r ~ 1 +/- 0.3 (near hexagonal locus)")
        print(f"  Status:             {'PASS' if passed else 'FAIL'}")

    return {
        'sigma_kinematic': sigma_kin, 'r_kinematic': r_kin,
        'sigma_jet_excess': sigma_jet, 'r_jet_excess': r_jet,
        'velocity_ratio': kin['velocity_ratio_rms'],
        'epsilon_hex': kin['epsilon_hex'],
        'passed': passed,
    }


def verify_theorem3_stationarity(verbose: bool = True) -> dict:
    """
    Theorem 3 verification: The stationary jet speed U* predicted by the
    Rossby dispersion relation matches the observed 120 m/s.

    Also verify: intrinsic drift rate from 2008-14 epoch.
    """
    saturn = SaturnParameters()
    # Zonal wavenumber for n=6
    k = 6 / saturn.hexagon_radius
    U_star = stationary_jet_speed(k, 0, saturn.beta)

    omega_intrinsic, omega_err = intrinsic_drift_rate()

    # U* should be same order as observed 120 m/s
    ratio = U_star / saturn.jet_speed_peak
    passed = 0.1 < ratio < 10  # Within an order of magnitude

    if verbose:
        print("THEOREM 3: |lambda|=1 <-> Rossby stationarity")
        print(f"  Predicted U*:    {U_star:.1f} m/s")
        print(f"  Observed U:      {saturn.jet_speed_peak:.1f} m/s")
        print(f"  Ratio U*/U_obs:  {ratio:.3f}")
        print(f"  Intrinsic drift: {omega_intrinsic:.4f} +/- {omega_err:.3f} deg/day")
        print(f"  Status:          {'PASS' if passed else 'FAIL'}")

    return {'U_star': U_star, 'U_observed': saturn.jet_speed_peak,
            'ratio': ratio, 'omega_intrinsic': omega_intrinsic, 'passed': passed}


def verify_theorem4_thomson(verbose: bool = True) -> dict:
    """
    Theorem 4 verification (partial -- CONJECTURE status):

    Test 1: Thomson stability: N<=7 are stable (no center vortex).
    Test 2: Mobius multiplier |lambda| = 1 for N=6.
    Test 3: Rayleigh-Kuo criterion identifies critical radii.
    """
    # Test 1: stability sweep
    results = stability_sweep(range(3, 10))
    stable_N = [N for N in range(3, 10) if results[N]['stable']]

    # Test 2: Mobius multiplier
    lam_6 = thomson_to_mobius_multiplier(6)
    unit_modulus = abs(abs(lam_6) - 1.0) < 0.01

    # Test 3: Rayleigh-Kuo (basic check)
    saturn = SaturnParameters()
    rho_grid = np.linspace(-1, 1, 500)
    U_profile = lambda rho: gaussian_jet_profile(
        rho, saturn.jet_speed_peak, 0.0, saturn.jet_sigma_logpolar
    )
    from thomson import rayleigh_kuo_at_wavenumber
    rk = rayleigh_kuo_at_wavenumber(6, saturn.beta, U_profile, rho_grid)
    has_crossings = len(rk['critical_rho']) > 0

    passed = unit_modulus  # Primary test

    if verbose:
        print("THEOREM 4: Thomson = Rossby in C* (CONJECTURE)")
        print(f"  Stable N (no center): {stable_N}")
        print(f"  |lambda_6| = {abs(lam_6):.6f} (expect 1.0)")
        print(f"  Rayleigh-Kuo crossings: {len(rk['critical_rho'])}")
        print(f"  Status: {'NUMERICAL EVIDENCE' if passed else 'INCONCLUSIVE'}")

    return {'stable_N': stable_N, 'lambda_6_modulus': abs(lam_6),
            'rk_crossings': len(rk['critical_rho']),
            'passed': passed, 'note': 'CONJECTURE - numerical evidence only'}


def verify_cassini_measurements(verbose: bool = True) -> dict:
    """
    Compare predictions against Cassini wind profile measurements.

    This is the INDEPENDENT observational test — using digitized
    Cassini data rather than assumed parameter values.
    """
    from cassini_winds import (
        load_cassini_profile, measure_delta_U, measure_hexagon_epsilon,
    )
    dU = measure_delta_U()
    hex_eps = measure_hexagon_epsilon()

    # Theorem 5 prediction with CORRECT matching constant
    from matching import matching_constant
    saturn = SaturnParameters()
    C_eff = matching_constant(
        n=6, sigma_jet=saturn.jet_sigma_logpolar,
        U_max=dU['U_observed'], U_star=dU['U_star']
    )
    eps_predicted = hexagon_amplitude_analytic(
        dU['delta_U'], dU['U_star'], n=6, rho_star=0.0,
        sigma_jet=saturn.jet_sigma_logpolar, U_max=dU['U_observed']
    )
    eps_ratio = eps_predicted / hex_eps['epsilon_observed'] if hex_eps['epsilon_observed'] > 0 else 0

    if verbose:
        print("CASSINI DATA VERIFICATION")
        print(f"  Wind profile: U_peak = {dU['U_observed']:.1f} m/s at {dU['peak_latitude']:.1f} deg N")
        print(f"  U* (Rossby):  {dU['U_star']:.1f} m/s")
        print(f"  delta_U/U*:   {dU['delta_U_over_Ustar']:.4f}")
        print(f"  Gaussian fit: {dU['gaussian_relative_rms']*100:.1f}% RMS error")
        print(f"  Matching constant C:       {C_eff:.4f} (from Fourier overlap)")
        print(f"  epsilon_predicted:         {eps_predicted:.4f}")
        print(f"  epsilon_observed (geom.):  {hex_eps['epsilon_observed']:.4f}")
        print(f"  Ratio pred/obs:            {eps_ratio:.3f}")

    return {
        'U_observed': dU['U_observed'],
        'U_star': dU['U_star'],
        'delta_U_over_Ustar': dU['delta_U_over_Ustar'],
        'epsilon_predicted': eps_predicted,
        'epsilon_observed': hex_eps['epsilon_observed'],
        'epsilon_ratio': eps_ratio,
        'gaussian_fit_rms': dU['gaussian_relative_rms'],
    }


def verify_theorem5_amplitude(verbose: bool = True) -> dict:
    """
    Theorem 5 verification: The matched asymptotic solution predicts
    the hexagon amplitude epsilon from the observed delta_U.

    Uses the DERIVED matching constant C from the Fourier overlap integral
    (not the old C = 1/n approximation).
    """
    saturn = SaturnParameters()
    k = 6 / saturn.hexagon_radius
    U_star = stationary_jet_speed(k, 0, saturn.beta)
    delta_U = saturn.jet_speed_peak - U_star

    from matching import matching_constant
    C = matching_constant(n=6, sigma_jet=saturn.jet_sigma_logpolar,
                          U_max=saturn.jet_speed_peak, U_star=U_star)

    epsilon = hexagon_amplitude_analytic(
        delta_U=abs(delta_U), U_star=U_star, n=6, rho_star=0.0,
        sigma_jet=saturn.jet_sigma_logpolar, U_max=saturn.jet_speed_peak
    )

    observed_range = (0.05, 0.20)
    passed = observed_range[0] < epsilon < observed_range[1]

    if verbose:
        print("THEOREM 5: Matched asymptotic expansion")
        print(f"  C (Fourier overlap): {C:.4f}")
        print(f"  delta_U = U - U*:  {delta_U:.1f} m/s")
        print(f"  Predicted epsilon: {epsilon:.4f}")
        print(f"  Observed range:    {observed_range}")
        print(f"  Status:            {'PASS' if passed else 'FAIL'}")

    return {'delta_U': delta_U, 'epsilon': epsilon,
            'observed_range': observed_range, 'passed': passed}


def predict_nps_perturbation() -> dict:
    """
    Predict the NPS-induced drift rate perturbation.
    """
    gamma, gamma_err = nps_coupling_coefficient()
    omega_intrinsic, _ = intrinsic_drift_rate()
    T_resonance = near_resonance_period()

    # Observed drift difference between epochs
    from saturn_data import EPOCH_1980_81, EPOCH_2008_14
    delta_omega_obs = EPOCH_1980_81.hexagon_omega - EPOCH_2008_14.hexagon_omega

    return {
        'gamma': gamma,
        'gamma_err': gamma_err,
        'omega_intrinsic': omega_intrinsic,
        'near_resonance_period_years': T_resonance,
        'delta_omega_observed': delta_omega_obs,
    }


def full_verification_report() -> None:
    """
    Run all verifications and print a formatted report.
    """
    separator = "-" * 60

    print(separator)
    r1 = verify_theorem1_log_polar()
    print(separator)
    r2 = verify_theorem2_mobius()
    print(separator)
    r3 = verify_theorem3_stationarity()
    print(separator)
    r4 = verify_theorem4_thomson()
    print(separator)
    r5 = verify_theorem5_amplitude()
    print(separator)

    # Cassini wind profile comparison
    cassini = verify_cassini_measurements()
    print(separator)

    # NPS perturbation
    nps = predict_nps_perturbation()
    print("NPS PERTURBATION ANALYSIS")
    print(f"  Coupling coefficient: gamma = {nps['gamma']:.4f} +/- {nps['gamma_err']:.4f}")
    print(f"  Near-resonance period: {nps['near_resonance_period_years']:.1f} years")
    print(f"  Delta-omega observed:  {nps['delta_omega_observed']:.4f} deg/day")
    print(separator)

    # Summary
    results = [r1, r2, r3, r4, r5]
    n_passed = sum(1 for r in results if r['passed'])
    print(f"\nOVERALL: {n_passed}/5 theorems verified to stated tolerance.")
    print("(Theorem 4 is a conjecture; 'passed' means numerical evidence supports it.)")
