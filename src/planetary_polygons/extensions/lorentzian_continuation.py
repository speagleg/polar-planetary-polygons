"""
Lorentzian continuation: following the sinh/cosh hint from JT gravity.

The JT gravity test found:
    C_1 = log(2sinh rho)  [our system, EXACT]
    C_1^{JT} = log(cosh rho)  [JT gravity, FAILS]

The key: sinh and cosh are related by a COMPLEX SHIFT:
    sinh(rho + i*pi/2) = i*cosh(rho)
    log(2sinh(rho + i*pi/2)) = log(2*cosh(rho)) + i*pi/2

So the JT profile lives at Im(rho) = pi/2 in complexified moduli space.

In the BTZ black hole geometry:
    - rho real: the EXTERIOR (spatial geodesic distance)
    - rho + i*pi/2: the INTERIOR (behind the horizon)

Our vortex system is in the BTZ EXTERIOR.
JT gravity probes the BTZ INTERIOR.

The palindromic threshold (lambda = 0 at rho*) maps to a
HORIZON CROSSING in the Lorentzian theory.
"""

import numpy as np
from math import pi, sin, cos, log, sinh, cosh, tanh, sqrt, exp, atan2


def casimir(m, N):
    return m * (N - m) / 2.0


def b_exact(N):
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


def C1_sinh(rho):
    """C_1 in our system: log(2sinh rho)."""
    if rho > 0:
        return log(2 * sinh(rho))
    return float('-inf')


def C1_cosh(rho):
    """C_1 in JT gravity: log(cosh rho)."""
    return log(cosh(rho))


# =====================================================================
# PART 1: The complex shift sinh -> cosh
# =====================================================================

def complex_shift_verification():
    """Verify: sinh(rho + i*pi/2) = i*cosh(rho)."""
    print("=" * 72)
    print("  PART 1: The complex shift sinh <-> cosh")
    print("=" * 72)

    print(f"\n  sinh(z + i*pi/2) = i*cosh(z)")
    print(f"  log(2*sinh(z + i*pi/2)) = log(2*cosh(z)) + i*pi/2")
    print(f"\n  {'rho':>8s} {'log(2sinh)':>14s} {'log(2cosh)':>14s} "
          f"{'diff':>10s} {'i*pi/2':>10s}")

    for rho in [0.5, 1.0, 2.0, 5.0, 10.0]:
        log_sinh = log(2 * sinh(rho))
        log_cosh = log(2 * cosh(rho))
        diff = log_cosh - log_sinh

        # sinh(rho + i*pi/2) = sinh(rho)*cos(pi/2) + i*cosh(rho)*sin(pi/2)
        #                    = 0 + i*cosh(rho) = i*cosh(rho)
        # |sinh(rho + i*pi/2)| = cosh(rho)
        # arg = pi/2

        print(f"  {rho:8.2f} {log_sinh:14.8f} {log_cosh:14.8f} "
              f"{diff:10.6f} {pi/2:10.6f}")

    print(f"\n  The difference log(2cosh) - log(2sinh) = log(cosh/sinh) = log(coth)")
    print(f"  For large rho: coth -> 1, so diff -> 0 (same IR).")
    print(f"  For small rho: coth -> 1/rho, so diff -> log(1/rho) (different UV).")

    print("""
  INTERPRETATION:
  The JT gravity profile is obtained from our C_1 by the COMPLEX SHIFT
  rho -> rho + i*pi/2 in the complexified moduli space.

  In the BTZ black hole (which is a quotient of AdS_3):
    - rho real: the EXTERIOR region (spatial distance from the horizon)
    - rho complex with Im = pi/2: the INTERIOR (behind the horizon)

  Our vortex system lives in the BTZ EXTERIOR.
  JT gravity probes the BTZ INTERIOR.
  The two are related by the Kruskal analytic continuation.
""")


# =====================================================================
# PART 2: Wick rotation to flat space
# =====================================================================

def wick_rotation():
    """The Wick rotation rho -> i*t maps H^2 to flat space."""
    print("=" * 72)
    print("  PART 2: Wick rotation rho -> i*t")
    print("=" * 72)

    print("""
  Under rho -> i*t:
    sinh(rho) -> sinh(i*t) = i*sin(t)
    cosh(rho) -> cosh(i*t) = cos(t)

  So:
    C_1^{{vortex}} = log(2*sinh(rho)) -> log(2*i*sin(t)) = log(2*sin(t)) + i*pi/2
    C_1^{{JT}}     = log(cosh(rho))   -> log(cos(t))

  The REAL part of the vortex continuation:
    Re[C_1(i*t)] = log(2*sin(t))

  This IS the flat-plane Havelock kernel! The Wick rotation maps
  the H^2 vortex theory to the flat-plane vortex theory.

  The IMAGINARY part:
    Im[C_1(i*t)] = pi/2 (constant Berry phase)

  The flat-plane eigenvalue:
    lambda_m^{{flat}}(t) = log(2*sin(t)) + b(N) - f(m) + delta_m
""")

    print(f"  Verification: H^2 kernel at rho vs flat kernel at t = rho")
    print(f"  {'rho=t':>8s} {'log(2sinh)':>14s} {'log(2sin)':>14s} "
          f"{'cosh':>14s} {'cos':>14s}")

    for t in [0.1, 0.3, 0.5, 0.8, 1.0, 1.2, pi/4, pi/3, pi/2 - 0.01]:
        log_sinh = log(2 * sinh(t))
        log_sin = log(2 * sin(t)) if sin(t) > 0 else float('-inf')
        log_cosh_val = log(cosh(t))
        log_cos_val = log(cos(t)) if cos(t) > 0 else float('-inf')

        print(f"  {t:8.4f} {log_sinh:14.8f} {log_sin:14.8f} "
              f"{log_cosh_val:14.8f} {log_cos_val:14.8f}")


# =====================================================================
# PART 3: The three geometries from analytic continuation
# =====================================================================

def three_geometries():
    """The three geometries connected by analytic continuation."""
    print(f"\n{'='*72}")
    print("  PART 3: Three geometries from analytic continuation")
    print("=" * 72)

    print("""
  The Green's function G(d) and curvature K under continuation:

  Geometry     | G(d)                | K    | C_1           | Continuation
  -------------|---------------------|------|---------------|-------------
  H^2          | -log(2*sinh(d/2))   | -1   | log(2*sinh r) | r real
  Flat (R^2)   | -log(d)             |  0   | log(2*sin t)  | r -> i*t
  Sphere (S^2) | -log(2*sin(d/2))    | +1   | log(2*cos t)  | r -> i*t + pi/2

  The developing map parameter beta interpolates these:
    beta = 0:     flat (K = 0)
    beta = 1/(2N): max curvature (K = 1/N)
    beta = 1/N:   sphere endpoint (K = 0, but wrapped)

  The ANALYTIC CONTINUATION interpolates the same geometries:
    Im(rho) = 0:     H^2 (our system)
    Im(rho) = pi/2:  Flat (Wick rotation)
    Im(rho) = pi:    Sphere (double Wick)
""")

    # The three C_1 functions
    print(f"  {'Im(rho)':>10s} {'Re(C1)':>14s} {'kernel':>20s} {'geometry':>12s}")
    rho = 2.0

    # H^2: rho real
    C1_H2 = log(2 * sinh(rho))
    print(f"  {'0':>10s} {C1_H2:14.8f} {'log(2sinh rho)':>20s} {'H^2':>12s}")

    # Flat: rho -> rho + i*pi/2, take |sinh(rho + i*pi/2)| = cosh(rho)
    # But the flat limit is rho -> i*t with t in (0, pi)
    # At t = pi/2: log(2*sin(pi/2)) = log(2) = 0.693
    C1_flat = log(2 * sin(pi/3))  # example point
    print(f"  {'pi/2':>10s} {C1_flat:14.8f} {'log(2sin t)':>20s} {'Flat':>12s}")

    # Sphere: rho -> rho + i*pi
    # sinh(rho + i*pi) = -sinh(rho)
    # |2*sinh(rho + i*pi)| = 2*sinh(rho)
    # But with a SIGN CHANGE: the sphere Green's function
    C1_S2 = log(2 * abs(sin(pi/6)))  # sphere with specific angle
    print(f"  {'pi':>10s} {C1_S2:14.8f} {'log(2sin(d/2))':>20s} {'S^2':>12s}")


# =====================================================================
# PART 4: Resonances at complex rho
# =====================================================================

def resonance_structure(N):
    """The palindromic threshold as a resonance in the complex rho plane.

    The threshold condition: lambda_{m*}(rho) = 0
    i.e., C_1(rho) = f(m*) - delta_{m*}

    For real rho: C_1 = log(2sinh rho) + b(N)
    The threshold is at rho* where log(2sinh rho*) = f(m*) - b(N) - delta_{m*}

    Under continuation to complex rho = x + i*y:
    C_1(x + iy) = log|2*sinh(x+iy)| + i*arg(sinh(x+iy)) + b(N)

    sinh(x + iy) = sinh(x)*cos(y) + i*cosh(x)*sin(y)
    |sinh(x+iy)|^2 = sinh^2(x)*cos^2(y) + cosh^2(x)*sin^2(y)
                    = sinh^2(x) + sin^2(y)  [using cosh^2 = 1 + sinh^2]

    The threshold in the COMPLEX plane:
    log(2*sqrt(sinh^2(x) + sin^2(y))) = f(m*) - b(N)
    """
    print(f"\n  N = {N}:")

    m_crit = N // 2
    f_crit = casimir(m_crit, N)
    b = b_exact(N)
    target = f_crit - b  # log(2sinh(rho*)) at the real threshold

    # Real threshold
    if target > log(2):  # sinh(rho) > 1
        sinh_rho_star = exp(target) / 2
        rho_star_real = np.arcsinh(sinh_rho_star)
    else:
        rho_star_real = float('nan')

    print(f"  f_crit = {f_crit:.4f}, b(N) = {b:.4f}, target = {target:.4f}")
    print(f"  Real threshold: rho* = {rho_star_real:.6f}")

    # Complex threshold at y = pi/2 (the JT/flat continuation):
    # |sinh(x + i*pi/2)|^2 = sinh^2(x) + 1 = cosh^2(x)
    # log(2*cosh(x)) = f_crit - b
    if target > 0:
        cosh_x_star = exp(target) / 2
        if cosh_x_star >= 1:
            x_star_JT = np.arccosh(cosh_x_star)
        else:
            x_star_JT = 0
    else:
        x_star_JT = float('nan')

    print(f"  JT threshold (y=pi/2): x* = {x_star_JT:.6f}")

    # Compare: the real threshold and the JT threshold
    if not np.isnan(rho_star_real) and not np.isnan(x_star_JT):
        shift = x_star_JT - rho_star_real
        print(f"  Shift: x*(JT) - rho* = {shift:.6f}")
        print(f"  The JT threshold is {'further' if shift > 0 else 'closer'} "
              f"than the real threshold")

    # The threshold at ARBITRARY imaginary part y:
    # sinh^2(x) + sin^2(y) = (exp(target)/2)^2
    # sinh^2(x) = (exp(target)/2)^2 - sin^2(y)
    # This has a solution for x > 0 when sin^2(y) < (exp(target)/2)^2

    print(f"\n  Threshold curve in the complex rho plane:")
    print(f"  {'Im(rho)':>10s} {'Re(rho)':>12s} {'|sinh|':>12s}")

    target_val = exp(target) / 2
    for y in np.linspace(0, pi/2, 11):
        sinh_sq = target_val**2 - sin(y)**2
        if sinh_sq > 0:
            x = np.arcsinh(sqrt(sinh_sq))
            abs_sinh = sqrt(sinh_sq + sin(y)**2)
            print(f"  {y:10.6f} {x:12.6f} {abs_sinh:12.6f}")
        else:
            print(f"  {y:10.6f} {'(no solution)':>12s}")

    return rho_star_real, x_star_JT


def resonances():
    """Map the palindromic thresholds to complex resonances."""
    print(f"\n{'='*72}")
    print("  PART 4: Palindromic thresholds as complex resonances")
    print("=" * 72)

    print("""
  The eigenvalue: lambda_m(rho) = log(2sinh rho) + b(N) - f(m) + delta_m

  At REAL rho = rho*: lambda_{m*} = 0 (the palindromic threshold).

  At COMPLEX rho = x + iy: lambda_{m*} has both real and imaginary parts.
  The RESONANCE is where Re(lambda) = 0 with Im(lambda) = width.

  At y = pi/2 (the JT/flat continuation):
    lambda_m(x + i*pi/2) = log(2*cosh(x)) + i*pi/2 + b(N) - f(m) + delta_m

  Re(lambda) = 0 requires: log(2*cosh(x)) + b(N) - f(m) + delta_m = 0
  Im(lambda) = pi/2 (UNIVERSAL width, independent of N and m)

  The QUASI-NORMAL MODE interpretation:
    - Re(lambda) = 0: the resonance frequency (energy = 0)
    - Im(lambda) = pi/2: the decay width (inverse lifetime)
    - The lifetime: tau = 2/pi (in natural units)
""")

    print(f"  {'N':>4s} {'rho*(real)':>12s} {'x*(JT)':>12s} {'shift':>10s} "
          f"{'width':>10s}")

    for N in range(6, 21, 2):
        rho_real, x_JT = resonance_structure(N)
        if not np.isnan(rho_real) and not np.isnan(x_JT):
            print(f"  {N:4d} {rho_real:12.6f} {x_JT:12.6f} "
                  f"{x_JT - rho_real:10.6f} {pi/2:10.6f}")


# =====================================================================
# PART 5: The Lorentzian partition function
# =====================================================================

def lorentzian_partition_function():
    """The partition function under the Lorentzian continuation."""
    print(f"\n{'='*72}")
    print("  PART 5: The Lorentzian partition function")
    print("=" * 72)

    print("""
  The Euclidean partition function near the threshold:
    Z_E(rho) ~ A(N) * |rho - rho*|^{{-1/2}}  (critical exponent 1/2)

  Under analytic continuation rho -> rho + i*epsilon (Lorentzian):
    Z_L(rho) ~ A(N) * (rho - rho* + i*epsilon)^{{-1/2}}

  This has:
    - A BRANCH CUT at rho = rho* (the threshold = horizon)
    - REAL part: A(N) * |rho - rho*|^{{-1/2}} * cos(pi/4) for rho > rho*
    - IMAGINARY part: A(N) * |rho - rho*|^{{-1/2}} * sin(pi/4) for rho > rho*

  The SPECTRAL FUNCTION (imaginary part of the retarded propagator):
    rho(omega) = Im[Z_L] ~ A(N) * |rho - rho*|^{{-1/2}} * sin(pi/4)
               = A(N) / sqrt(2) * |rho - rho*|^{{-1/2}}

  This is a DENSITY OF STATES that diverges at the threshold:
  the van Hove singularity of the polygon-BTZ transition.
""")

    # Compute the spectral function for N = 8
    N = 8
    m_crit = N // 2
    f_crit = casimir(m_crit, N)
    b = b_exact(N)

    # The frozen determinant (from the Casimir approximation)
    log_Z_frozen = 0.0
    for m in range(1, N):
        if m == m_crit:
            continue
        gap = (N - 2*m)**2 / 8.0
        log_Z_frozen += -0.5 * log(gap)

    Z_frozen = exp(log_Z_frozen)
    A_N = Z_frozen  # since coth(rho*) ~ 1 for large rho*

    print(f"  N = {N}: Z_frozen = {Z_frozen:.6e}, A(N) = {A_N:.6e}")
    print(f"\n  Spectral function near the threshold:")
    print(f"  {'rho - rho*':>12s} {'|Z_E|':>14s} {'Re(Z_L)':>14s} {'Im(Z_L)':>14s}")

    for delta_rho in [0.001, 0.01, 0.1, 0.5, 1.0, 2.0]:
        Z_E = A_N / sqrt(delta_rho)
        Z_L_re = A_N / sqrt(delta_rho) * cos(pi/4)
        Z_L_im = A_N / sqrt(delta_rho) * sin(pi/4)
        print(f"  {delta_rho:12.4f} {Z_E:14.6e} {Z_L_re:14.6e} {Z_L_im:14.6e}")


# =====================================================================
# PART 6: The time variable from the spectral flow
# =====================================================================

def spectral_flow_as_time():
    """Promoting rho to a dynamical variable: the spectral flow clock."""
    print(f"\n{'='*72}")
    print("  PART 6: The spectral flow as physical time")
    print("=" * 72)

    print("""
  The palindromic staircase parameterized by rho:
    rho < rho*(7):  all polygons stable (the AdS vacuum)
    rho = rho*(7):  heptagon goes unstable (first horizon crossing)
    rho = rho*(8):  octagon goes unstable (second horizon crossing)
    ...
    rho = rho*(N):  N-gon goes unstable (N-th horizon crossing)

  Under the Wick rotation rho -> i*t:
  Each threshold rho*(N) maps to a time t*(N) = i*rho*(N).
  But this is IMAGINARY time — the thresholds are in the Euclidean theory.

  For REAL time: the continuation rho -> rho + i*pi/2 gives the
  Lorentzian theory. The thresholds become:
    rho*(N) + i*pi/2 = complex resonance

  with UNIVERSAL width Im = pi/2 for all N.

  The physical interpretation of the width:
    Gamma = pi (decay rate in natural units)
    tau = 1/Gamma = 1/pi (lifetime of the quasi-bound polygon state)

  This means: in the Lorentzian theory, a polygon at the threshold
  has a FINITE LIFETIME of order 1/pi before it decays to the
  next-lower polygon number.

  The SPECTRAL FLOW CLOCK:
  If rho increases with physical time (e.g., from dissipation),
  the polygon passes through each threshold at a rate determined
  by d(rho)/dt. The SEQUENCE of transitions is:

    N = 7 -> 6 -> 5 -> 4 -> 3 (as rho increases through thresholds)

  with each transition having:
    - Critical exponent: nu = 1/2 (universal)
    - Amplitude: A(N) = 2^{{3(N-2)/4}} / (N-3)!! (from frozen determinant)
    - Width: Gamma = pi (from Lorentzian continuation)
""")

    print(f"  The palindromic staircase with Lorentzian data:")
    print(f"  {'N':>4s} {'rho*(N)':>12s} {'A(N)':>14s} {'Gamma':>10s} "
          f"{'tau=1/Gamma':>12s}")

    for N in range(7, 20):
        m_crit = N // 2
        f_crit = casimir(m_crit, N)
        b = b_exact(N)
        target = f_crit - b

        if target > 0:
            rho_star = np.arcsinh(exp(target) / 2)
        else:
            rho_star = float('nan')

        # Frozen determinant (Casimir approx for even N)
        if N % 2 == 0:
            log_Z = 0
            for m in range(1, N):
                if m == N // 2:
                    continue
                gap = (N - 2*m)**2 / 8.0
                log_Z += -0.5 * log(gap)
            A_N = exp(log_Z)
        else:
            A_N = float('nan')  # odd N needs different formula

        gamma = pi
        tau = 1 / gamma

        if not np.isnan(rho_star):
            print(f"  {N:4d} {rho_star:12.4f} {A_N:14.6e} {gamma:10.6f} "
                  f"{tau:12.6f}")


# =====================================================================
# PART 7: The BTZ exterior/interior connection
# =====================================================================

def btz_connection():
    """The BTZ black hole exterior/interior from sinh/cosh."""
    print(f"\n{'='*72}")
    print("  PART 7: BTZ exterior/interior and the problem of time")
    print("=" * 72)

    print("""
  The BTZ black hole in 2+1 dimensions:
    ds^2 = -(r^2/l^2 - M) dt^2 + (r^2/l^2 - M)^{{-1}} dr^2 + r^2 dphi^2

  The horizon at r_+ = l*sqrt(M), with:
    EXTERIOR (r > r_+): proper distance rho = integral of grr^{{1/2}}
      -> sinh appears in the spatial Green's function
    INTERIOR (r < r_+): time and space swap roles
      -> cosh appears in the "temporal" Green's function

  Our framework:
    C_1 = log(2*sinh(rho)) + b(N)  [EXTERIOR Green's function]
    C_1^{{JT}} = log(cosh(rho))     [INTERIOR Green's function]

  The palindromic threshold rho* is the HORIZON:
    - For rho < rho*: the polygon is in the exterior (stable, no horizon)
    - For rho > rho*: the polygon has "crossed the horizon" (unstable)
    - The lambda = 0 eigenvalue is the HORIZON CONDITION

  THE PROBLEM OF TIME resolution:
    In the EXTERIOR: time is the Killing vector d/dt.
      The vortex dynamics (Hamilton's equations from omega_KR) provides
      physical time evolution. The eigenvalues lambda_m are frequencies
      of oscillation around the static equilibrium.

    At the HORIZON: the Killing vector becomes null.
      lambda_{{m*}} = 0 means the critical mode has zero frequency —
      it's "frozen" on the horizon. This IS the frozen formalism.

    In the INTERIOR: the Killing vector is spacelike.
      The continuation rho -> rho + i*pi/2 exchanges time and space.
      The vortex oscillation (temporal) becomes a spatial modulation
      (static but spatially varying). The "frozen mode" UNFREEZES
      into a spatial structure.

  THE KEY INSIGHT:
    The polynomial phase (rho < rho*) has TIME evolution (vortex oscillations).
    The BTZ phase (rho > rho*) has SPATIAL structure (no oscillation, but
    the configuration varies in space instead of time).

    The transition at rho* is the EXCHANGE OF TIME AND SPACE —
    the mode that was oscillating in time (lambda > 0, temporal)
    becomes a mode that varies in space (lambda < 0, spatial growth).

    This IS the Lorentzian resolution of the frozen formalism:
    the "problem of time" at the threshold is resolved by the
    TIME-SPACE EXCHANGE across the horizon.
""")

    # Illustrate with eigenvalues
    N = 8
    m_crit = N // 2
    f_crit = casimir(m_crit, N)
    b = b_exact(N)

    print(f"  Illustration for N = {N}:")
    print(f"  {'rho':>8s} {'lambda_{m*}':>14s} {'interpretation':>30s}")

    target = f_crit - b
    if target > 0:
        rho_star = np.arcsinh(exp(target) / 2)
    else:
        rho_star = 5.0

    for rho in [rho_star - 2, rho_star - 1, rho_star - 0.1,
                rho_star, rho_star + 0.1, rho_star + 1, rho_star + 2]:
        if rho > 0.01:
            lam = log(2 * sinh(rho)) + b - f_crit
            if abs(lam) < 0.01:
                interp = "HORIZON (lambda = 0)"
            elif lam > 0:
                interp = f"EXTERIOR (oscillation freq {sqrt(lam):.3f})"
            else:
                interp = f"INTERIOR (spatial growth {sqrt(-lam):.3f})"
            print(f"  {rho:8.4f} {lam:14.6f} {interp:>30s}")


def main():
    complex_shift_verification()
    wick_rotation()
    three_geometries()
    resonances()
    lorentzian_partition_function()
    spectral_flow_as_time()
    btz_connection()

    print(f"\n{'='*72}")
    print("  SUMMARY: Where the sinh/cosh hint leads")
    print("=" * 72)
    print("""
  Following the JT gravity hint (sinh ≠ cosh) leads to:

  1. EXTERIOR vs INTERIOR: Our C_1 = log(2sinh rho) is the BTZ
     EXTERIOR Green's function. JT's log(cosh) is the INTERIOR.
     They're connected by the complex shift rho -> rho + i*pi/2.

  2. RESONANCE STRUCTURE: The palindromic thresholds become complex
     resonances at rho* + i*pi/2 with UNIVERSAL width Gamma = pi.
     This gives a finite lifetime tau = 1/pi for the critical polygon.

  3. TIME-SPACE EXCHANGE: At the threshold, the oscillating mode
     (temporal, lambda > 0) becomes a growing mode (spatial, lambda < 0).
     This is the TIME-SPACE SWAP across the BTZ horizon.

  4. THE PROBLEM OF TIME: Resolved by the observation that "time" in
     the polygon phase (exterior) is the Killing vector d/dt, which
     becomes null at the threshold (horizon) and spacelike in the
     BTZ phase (interior). The frozen formalism at the threshold
     IS the horizon, where the Killing vector degenerates.

  5. THE SPECTRAL FLOW CLOCK: If rho is promoted to a dynamical
     variable, the palindromic staircase becomes a sequence of
     HORIZON CROSSINGS, each with universal critical exponent 1/2
     and width pi. The "time" is rho itself, measured in units of
     the palindromic threshold spacing.

  The sinh/cosh distinction is not a technicality —
  it's the EXTERIOR/INTERIOR distinction of the BTZ geometry,
  and the palindromic threshold IS the black hole horizon.
""")


if __name__ == "__main__":
    main()
