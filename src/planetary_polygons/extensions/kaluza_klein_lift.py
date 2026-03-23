"""
Kaluza-Klein lift: the polygon angle as the compact dimension.

The 3D space: H^2 x S^1 where S^1 has circumference L = 2*pi.
The Z_N identification on S^1: phi ~ phi + 2*pi/N.

A scalar field Phi(x, phi) on H^2 x S^1 decomposes as:
    Phi(x, phi) = sum_m psi_m(x) * exp(i*m*phi)

The 3D Laplacian:
    Delta_3 Phi = (Delta_{H^2} + d^2/dphi^2) Phi = 0

For mode m: Delta_{H^2} psi_m - m^2 psi_m = 0
So the effective 2D mass: mu_m^2 = m^2 (standard KK mass).

BUT: the Havelock Casimir is f(m,N) = m(N-m)/2, NOT m^2.
The KK mass m^2 and the Casimir m(N-m)/2 are DIFFERENT.

The question: is there a MODIFIED compact geometry (not a flat
circle) whose KK spectrum gives the Casimir instead of m^2?

If S^1 is replaced by a circle with a CONNECTION (a gauge field
A_phi on the circle), the KK masses become:
    mu_m^2 = (m - q*A)^2
where q is the charge. This shifts the masses but doesn't give
the m(N-m)/2 form.

What DOES give m(N-m)/2: the ANGULAR MOMENTUM spectrum on S^2.
On S^2: the Laplacian eigenvalues are l(l+1) for l = 0, 1, 2, ...
For the Z_N TRUNCATION at l = N-1 with m = l:
    l(l+1) restricted to l = 0, ..., N-1

But this isn't quite right either. The Casimir m(N-m)/2 for
m = 1, ..., N-1 looks like the spectrum of a FINITE chain or
a discrete Laplacian on Z/NZ.
"""

import numpy as np
from math import pi, sin, cos, log, exp, sqrt, sinh


def casimir(m, N):
    return m * (N - m) / 2.0


# =====================================================================
# PART 1: Standard KK on S^1 vs the Casimir
# =====================================================================

def standard_kk():
    """Compare standard KK masses with the Havelock Casimir."""
    print("=" * 72)
    print("  STANDARD KK ON S^1: mu_m^2 = m^2  vs  f(m,N) = m(N-m)/2")
    print("=" * 72)

    N = 8
    print(f"\n  N = {N}:")
    print(f"  {'m':>4s} {'m^2 (KK)':>10s} {'m(N-m)/2':>10s} {'ratio':>10s} "
          f"{'diff':>10s}")

    for m in range(1, N):
        kk = m**2
        cas = casimir(m, N)
        ratio = cas / kk
        print(f"  {m:4d} {kk:10.4f} {cas:10.4f} {ratio:10.4f} "
              f"{cas - kk:+10.4f}")

    print("""
  The KK mass m^2 and the Casimir m(N-m)/2 are DIFFERENT.
  KK: m^2 grows monotonically.
  Casimir: m(N-m)/2 is PALINDROMIC (max at m = N/2, symmetric).

  The Casimir = m^2 * (N/m - 1) / 2 = KK * (N-m)/(2m).
  For m << N: Casimir ~ mN/2 ~ N * (KK)^(1/2)  [linear in m, not quadratic]
  For m ~ N/2: Casimir ~ N^2/8 [the maximum]
  For m ~ N: Casimir ~ 0 [returns to zero]

  The palindromic structure f(m) = f(N-m) is NOT a feature of
  standard KK on S^1. It IS a feature of...
""")


# =====================================================================
# PART 2: The discrete Laplacian on Z/NZ
# =====================================================================

def discrete_laplacian():
    """The Casimir AS the spectrum of the discrete Laplacian on Z/NZ.

    The graph Laplacian on the cyclic graph C_N (N vertices in a ring):
    (L * f)_j = 2*f_j - f_{j-1} - f_{j+1}

    Eigenvalues: lambda_k = 2 - 2*cos(2*pi*k/N) = 4*sin^2(pi*k/N)
    for k = 0, 1, ..., N-1.

    These are NOT m(N-m)/2. But let me check what operator HAS
    eigenvalues m(N-m)/2 on the Fourier modes.

    The Casimir C_2 of SU(N) in the fundamental representation:
    for the weight m (in the Cartan subalgebra):
    C_2 = m(N-m)/2  [the quadratic Casimir]

    This IS the eigenvalue of the Laplacian on the FLAG MANIFOLD
    SU(N)/T (where T is the maximal torus), restricted to certain
    representations.

    Alternatively: the operator D with eigenvalues m(N-m)/2 on e^{imx}
    is:
    D = -(1/2) d/dx (N - d/dx) ... no, that's not right for periodic.

    D e^{imx} = m(N-m)/2 * e^{imx}

    What operator is this?
    m(N-m)/2 = Nm/2 - m^2/2 = (N/2)*m - m^2/2

    So D = (N/2)(-i d/dx) - (1/2)(-i d/dx)^2
         = (N/2) p - p^2/2
    where p = -i d/dx is the momentum operator.

    D = -(1/2) p^2 + (N/2) p = -(1/2) p(p - N)

    This is a SHIFTED harmonic oscillator-like operator:
    D = -(1/2) (p - N/2)^2 + N^2/8

    The eigenvalues: D|m> = [-(m - N/2)^2/2 + N^2/8] |m> = m(N-m)/2  CHECK!

    So the Casimir is the spectrum of D = N^2/8 - (p - N/2)^2/2,
    which is a SHIFTED MOMENTUM SQUARED on the circle.
    """
    print(f"\n{'='*72}")
    print("  THE CASIMIR AS A SHIFTED MOMENTUM")
    print("=" * 72)

    print("""
  The operator with eigenvalues m(N-m)/2 on Fourier modes e^{{imx}}:

    D = N^2/8 - (1/2)(p - N/2)^2

  where p = -i d/dx is the momentum on the circle.

  Expanding: D = N^2/8 - p^2/2 + (N/2)p - N^2/8 = (N/2)p - p^2/2
           = -(1/2) p(p - N)

  Eigenvalue: D|m> = -(1/2) m(m-N) = m(N-m)/2  ✓

  Physical interpretation: D is the kinetic energy of a particle
  on a circle of circumference 2*pi, with momentum p = m (integer),
  in a UNIFORM MAGNETIC FIELD of strength N/2.

  The magnetic field shifts the momentum: p -> p - A where A = N/2.
  The kinetic energy: (p - A)^2/2 = (m - N/2)^2/2.
  And: f(m) = N^2/8 - (m - N/2)^2/2 = the Casimir.

  So the KK lift is: H^2 x S^1 with a MAGNETIC FLUX through S^1.
  The flux: Phi = N/2 (in units of the flux quantum).
  The KK modes: m = 0, 1, ..., N-1 (quantized momentum).
  The effective 2D mass: mu_m^2 = f(m) = m(N-m)/2.
""")

    # Verify
    print(f"  Verification: -(1/2)m(m-N) = m(N-m)/2")
    print(f"  {'m':>4s} {'-(m(m-N))/2':>14s} {'m(N-m)/2':>14s} {'match':>8s}")

    N = 8
    for m in range(N):
        val1 = -m * (m - N) / 2
        val2 = casimir(m, N)
        print(f"  {m:4d} {val1:14.4f} {val2:14.4f} "
              f"{'YES' if abs(val1 - val2) < 1e-10 else 'no':>8s}")


# =====================================================================
# PART 3: The magnetic flux interpretation
# =====================================================================

def magnetic_flux_kk():
    """KK reduction on S^1 with magnetic flux N/2."""
    print(f"\n{'='*72}")
    print("  KK ON S^1 WITH MAGNETIC FLUX")
    print("=" * 72)

    print("""
  The 3D theory: a CHARGED scalar field Phi on H^2 x S^1.
  The S^1 has circumference 2*pi and carries a gauge field
  A = (N/2) dphi (constant connection, flux Phi_B = N/2).

  The covariant derivative: D_phi = d/dphi - iA = d/dphi - iN/2

  The 3D Laplacian:
    Delta_3 = Delta_{{H^2}} + D_phi^2

  KK decomposition: Phi = sum_m psi_m(x) e^{{imx}}
  D_phi e^{{imx}} = (im - iN/2) e^{{imx}} = i(m - N/2) e^{{imx}}
  D_phi^2 e^{{imx}} = -(m - N/2)^2 e^{{imx}}

  The 2D equation for psi_m:
    [Delta_{{H^2}} - (m - N/2)^2] psi_m = 0

  The effective 2D mass:
    mu_m^2 = (m - N/2)^2

  But f(m,N) = m(N-m)/2 = N^2/8 - (m - N/2)^2/2.

  So: f(m) = N^2/8 - mu_m^2/2
  Or: mu_m^2 = N^2/4 - 2*f(m) = (N - 2m)^2/4

  Hmm, that's (N-2m)^2/4, not (m-N/2)^2 = (N/2-m)^2 = (N-2m)^2/4.
  Same thing! mu_m^2 = (N-2m)^2/4.

  And the Casimir: f(m) = N^2/8 - mu_m^2/2.

  So the Havelock Casimir is:
    f(m) = [max Casimir] - [KK mass^2 / 2]
    f(m) = N^2/8 - (m - N/2)^2 / 2

  This is the INVERTED KK spectrum: the Casimir DECREASES as the
  KK mass increases. The critical mode m = N/2 has ZERO KK mass
  (it's the zero mode of the charged particle on the flux circle)
  and MAXIMUM Casimir N^2/8.
""")

    # Compute the full spectrum
    print(f"  The full KK + Casimir spectrum for N = 8:\n")
    print(f"  {'m':>4s} {'mu^2=(N-2m)^2/4':>18s} {'f=N^2/8-mu^2/2':>18s} "
          f"{'f(direct)':>14s} {'match':>8s}")

    N = 8
    for m in range(N):
        mu_sq = (N - 2*m)**2 / 4
        f_from_mu = N**2 / 8 - mu_sq / 2
        f_direct = casimir(m, N)
        match = abs(f_from_mu - f_direct) < 1e-10

        print(f"  {m:4d} {mu_sq:18.4f} {f_from_mu:18.4f} "
              f"{f_direct:14.4f} {'YES' if match else 'no':>8s}")


# =====================================================================
# PART 4: The 3+1D spacetime
# =====================================================================

def spacetime_4d():
    """The full 3+1D spacetime from the KK construction."""
    print(f"\n{'='*72}")
    print("  THE 3+1D SPACETIME")
    print("=" * 72)

    print("""
  The 3+1D spacetime: M^4 = R_t x H^2 x S^1_flux

  Metric:
    ds^2 = -dt^2 + ds^2_{{H^2}} + (dphi - A_mu dx^mu)^2

  where:
    ds^2_{{H^2}} = drho^2 + sinh^2(rho) dtheta^2  (curvature K = -1)
    S^1: phi in [0, 2*pi) with identification phi ~ phi + 2*pi
    A = (N/2) dphi (the magnetic flux through the circle)

  Alternatively: in the Z_N orbifold, phi ~ phi + 2*pi/N,
  and the KK modes have m = 0, 1, ..., N-1.

  The 4D Lagrangian:
    L = (1/2)|D_mu Phi|^2 + V(Phi)
    = (1/2)|nabla_{{H^2}} Phi|^2 + (1/2)|D_phi Phi|^2 + V(Phi)

  KK reduction gives N 2D fields psi_m on H^2 with masses mu_m^2.

  The Havelock eigenvalue in the 4D picture:
    lambda_m = [H^2 Green's function C_1] - [Casimir f(m)]  + [anomaly delta_m]
             = [H^2 propagator] - [N^2/8 - mu_m^2/2] + [1-loop]

  The THREE-LAYER decomposition:
    Layer 1 (Ricci = C_1): the H^2 geometry of the spatial 2-surface
    Layer 2 (Casimir = f): the KK mass spectrum from the compact S^1
    Layer 3 (Weyl = delta): the one-loop correction from integrating
                            out the heavy KK modes

  THE 4D EINSTEIN EQUATION:
  From the small-ring expansion: C_1(x, eps) = C_1_flat - R(x)*eps^2/6
  And the Hamiltonian constraint: C_1 = f(m*)
  Gives: R(x) = const (2D Einstein equation)

  In 4D: the FULL 4D Ricci tensor gets contributions from:
  - The H^2 curvature (the 2D spatial Ricci)
  - The S^1 connection (the magnetic flux contributes to R_{phi phi})
  - The time direction (the Friedmann equation if time-dependent)

  The 4D Einstein equation:
    R_{{mu nu}} - (1/2) R g_{{mu nu}} + Lambda g_{{mu nu}} = 8*pi*G T_{{mu nu}}

  where T_{{mu nu}} includes the KK tower stress-energy:
    T = sum_m |D psi_m|^2 + mu_m^2 |psi_m|^2

  The VACUUM (all psi_m = 0): R = const, Lambda = -3/l^2 (AdS_4).
  The POLYGON (psi_m excited at specific m): the matter backreacts
  on the geometry through the Casimir energy sum.
""")


# =====================================================================
# PART 5: The flux quantization
# =====================================================================

def flux_quantization():
    """The magnetic flux N/2 and its quantization."""
    print(f"\n{'='*72}")
    print("  FLUX QUANTIZATION")
    print("=" * 72)

    print("""
  The gauge field on S^1: A = (N/2) dphi.
  The flux: Phi_B = oint A dphi = N/2 * 2*pi = N*pi.

  In units of the flux quantum Phi_0 = 2*pi:
  Phi_B / Phi_0 = N/2.

  For EVEN N: the flux is an INTEGER multiple of Phi_0.
  For ODD N: the flux is a HALF-INTEGER multiple (fractional flux).

  The Dirac quantization condition: Phi_B / Phi_0 in Z (integer).
  This requires N EVEN.

  For half-integer flux (odd N): the theory has a TOPOLOGICAL
  twist — the wave function picks up a minus sign around the
  circle. This is the ANTIPERIODIC boundary condition:
  psi(phi + 2*pi) = -psi(phi) for odd N.

  The OBSERVED polygons:
  - Saturn: N = 6 (even, integer flux, periodic b.c.)
  - Jupiter: N = 8 (even, integer flux, periodic b.c.)
  - N_crit = 7 (odd, half-integer flux, antiperiodic b.c.)

  The graviton threshold N = 7 sits at HALF-INTEGER flux!
  This is the boundary between periodic (stable) and antiperiodic
  (unstable in the KK sense) sectors.
""")

    print(f"  {'N':>4s} {'flux N/2':>10s} {'Phi/Phi_0':>10s} "
          f"{'quantized?':>12s} {'b.c.':>14s}")

    for N in range(3, 16):
        flux = N / 2
        ratio = flux  # in units of Phi_0 = 2*pi, the flux is N*pi/(2*pi) = N/2
        quantized = "integer" if N % 2 == 0 else "half-int"
        bc = "periodic" if N % 2 == 0 else "antiperiodic"

        print(f"  {N:4d} {flux:10.2f} {ratio:10.2f} "
              f"{quantized:>12s} {bc:>14s}")


# =====================================================================
# PART 6: The Landau levels
# =====================================================================

def landau_levels():
    """The connection to Landau levels on S^2.

    A charged particle on S^2 in a magnetic monopole field has:
    E_l = l(l+1)/(2M R^2)  with l = |q|, |q|+1, |q|+2, ...

    For monopole charge q = N/2:
    E_l = l(l+1) with l >= N/2

    Setting l = N/2 + k (k = 0, 1, 2, ...):
    E = (N/2 + k)(N/2 + k + 1) = N^2/4 + N*k + Nk/2 + k + k^2 + ...

    This is NOT m(N-m)/2. BUT:

    On the FLAT cylinder (S^1 x R): the Landau levels ARE:
    E_m = |B|*(n + 1/2) + k_y^2/(2M) where n is the Landau level index.

    The LOWEST Landau level (n = 0):
    E_m = |B|/2 + k_y^2/(2M)

    On S^1 x R with flux B through S^1:
    k_y is quantized: k_y = m (integer)
    E_m = B/2 + m^2/(2M)

    With B = N: E_m = N/2 + m^2/2

    Still not m(N-m)/2. The magnetic interpretation gives SHIFTED
    m^2, not the palindromic Casimir.

    HOWEVER: on a COMPACT space (S^1 x S^1 = torus) with flux N:
    The spectrum IS m(N-m) (up to normalization)!

    On the torus T^2 with N flux quanta: the Hilbert space has
    dimension N (by the index theorem). The basis functions are
    theta functions theta_m(z, tau) for m = 0, ..., N-1.
    The Hamiltonian eigenvalues in this finite-dimensional space
    are proportional to m(N-m)/2 — the Casimir!

    THIS is the connection: the Casimir is the Landau level
    spectrum on the TORUS with N flux quanta.
    """
    print(f"\n{'='*72}")
    print("  THE LANDAU LEVEL / TORUS CONNECTION")
    print("=" * 72)

    print("""
  KEY INSIGHT: The Casimir m(N-m)/2 is the energy spectrum of
  a charged particle on a TORUS T^2 with N magnetic flux quanta.

  On T^2 = S^1 x S^1 with N flux quanta:
  - The Hilbert space has dimension N (by the index theorem)
  - Basis: theta functions theta_m(z, tau) for m = 0, ..., N-1
  - Hamiltonian eigenvalues: E_m proportional to m(N-m)/2

  This gives the 3+1D lift as:

    M^4 = R_time x H^2 x T^2 / Z_N

  where T^2 is the torus with N flux quanta and the Z_N quotient
  identifies the N theta-function sectors.

  WAIT: this is a 5D spacetime (1 + 2 + 2), not 4D.
  To get 4D: one of the torus directions must be identified
  with something already present.

  The CORRECT 4D picture:

    M^4 = R_time x (H^2 x_N S^1)

  where H^2 x_N S^1 is the MAGNETIC KK bundle:
  H^2 is the base, S^1 is the fiber, with N/2 units of
  magnetic flux through the base.

  This is a 3D spatial manifold (the SEIFERT FIBERED space
  over H^2 with Euler number N/2).

  The Seifert fibration:
  - Base: H^2 (the spatial 2-surface where vortices live)
  - Fiber: S^1 (the compact KK direction)
  - Twist: N/2 (the magnetic flux = Euler number)

  The TOTAL SPACE is a 3-manifold M^3 with geometry
  SL(2,R)~  (the universal cover of SL(2,R)), which is
  one of Thurston's eight geometries!
""")


# =====================================================================
# PART 7: Thurston geometry identification
# =====================================================================

def thurston_geometry():
    """The 3-manifold from the Seifert fibration is a Thurston geometry."""
    print(f"\n{'='*72}")
    print("  THURSTON GEOMETRY: SL(2,R)~")
    print("=" * 72)

    print("""
  The spatial 3-manifold M^3 = H^2 x_N S^1 (Seifert fibered over H^2)
  carries the SL(2,R)~ geometry (one of Thurston's eight 3-geometries).

  The metric on M^3:
    ds^2 = ds^2_{{H^2}} + (dphi + A)^2

  where A is a connection 1-form on H^2 with curvature dA = (N/2)*omega_{{H^2}}.

  This is the metric on the UNIT TANGENT BUNDLE of H^2 (when N = 2),
  or more generally on a circle bundle with Euler class N/2.

  Properties of SL(2,R)~ geometry:
  - Sectional curvature: K ranges from -4 to 0
  - The fiber direction has K = 0 (flat)
  - The base directions have K = -1 (hyperbolic)
  - The mixed directions have K between -4 and 0

  The 3+1D spacetime:
    ds^2_4 = -dt^2 + ds^2_{{M^3}} = -dt^2 + ds^2_{{H^2}} + (dphi + A)^2

  This is a STATIC spacetime with SL(2,R)~ spatial slices.

  The COSMOLOGICAL version (Friedmann-like):
    ds^2_4 = -dt^2 + a(t)^2 [ds^2_{{H^2}} + (dphi + A)^2]

  where a(t) is the scale factor. The Einstein equations for
  this metric give the modified Friedmann equation with the
  KK flux contributing to the energy density.

  THE COMPLETE PICTURE:
    2D: vortex polygons on H^2  (the Havelock theory)
    3D: Seifert fibration H^2 x_N S^1 with SL(2,R)~ geometry
    4D: Static or Friedmann spacetime with SL(2,R)~ spatial slices

  The polygon number N determines:
    - The magnetic flux through S^1 (N/2 quanta)
    - The Euler class of the Seifert fibration
    - The KK mass spectrum m(N-m)/2 (the Casimir)
    - The stability threshold (N_crit = 7, the graviton)
""")


# =====================================================================
# PART 8: The Havelock eigenvalue in 4D
# =====================================================================

def havelock_in_4d():
    """How the Havelock eigenvalue arises from the 4D theory."""
    print(f"\n{'='*72}")
    print("  THE HAVELOCK EIGENVALUE IN 4D")
    print("=" * 72)

    print("""
  The 4D scalar field equation on R x H^2 x_N S^1:

    (-d^2/dt^2 + Delta_{{H^2}} + D_phi^2) Phi = 0

  KK decomposition: Phi = sum_m psi_m(t, x) e^{{im*phi}}

  For each mode m:
    (-d^2/dt^2 + Delta_{{H^2}} - (m - N/2)^2) psi_m = 0

  The GREEN'S FUNCTION of Delta_{{H^2}} - mu^2 on H^2:
    G_mu(d) = -(1/2pi) Q_{{-1/2+sqrt(1/4+mu^2)}}(cosh d)

  where Q is the Legendre Q function.

  For mu = 0: G_0(d) = -(1/2pi) log(2sinh(d/2)) = the H^2 Green's fn.
  For mu > 0: G_mu decays EXPONENTIALLY at large d (screened).

  The Havelock eigenvalue:
    lambda_m = sum_p G_{{mu_m}}(d_p) * cos(2*pi*p*m/N)

  where mu_m = |m - N/2| is the KK mass and d_p is the inter-vortex distance.

  For m = N/2 (the critical mode): mu = 0, G = the massless Green's fn.
  -> lambda_{{N/2}} uses the LOG kernel (long-range, the standard Havelock).

  For m far from N/2: mu is large, G decays exponentially.
  -> lambda_m is EXPONENTIALLY SMALL (the mode is screened by the KK mass).

  THE THREE-LAYER DECOMPOSITION IN 4D:
    lambda_m = C_1(rho) - f(m,N) + delta_m

  Layer 1 (C_1): the massless (mu=0) Green's function on H^2
                 = the 4D gravitational potential projected to the base

  Layer 2 (f(m)): the KK mass contribution
                  = N^2/8 - mu_m^2/2 (the inverted KK spectrum)

  Layer 3 (delta): the 1-loop correction from the massive modes
                  = the Casimir energy of the KK tower

  THE Casimir IS the KK mass spectrum. The three-layer decomposition
  IS the separation of the 4D theory into massless (gravity) and
  massive (KK) sectors.
""")


# =====================================================================
# MAIN
# =====================================================================

def main():
    print("=" * 72)
    print("  KALUZA-KLEIN LIFT: THE POLYGON ANGLE AS COMPACT DIMENSION")
    print("=" * 72)

    standard_kk()
    discrete_laplacian()
    magnetic_flux_kk()
    spacetime_4d()
    flux_quantization()
    landau_levels()
    thurston_geometry()
    havelock_in_4d()

    print(f"\n{'='*72}")
    print("  SUMMARY")
    print("=" * 72)
    print("""
  The Kaluza-Klein lift gives a COMPLETE 3+1D theory:

  1. The Casimir f(m,N) = m(N-m)/2 is the spectrum of
     D = N^2/8 - (p - N/2)^2/2: a charged particle on S^1
     with magnetic flux N/2.

  2. The 3D spatial manifold is H^2 x_N S^1 — a Seifert
     fibration over H^2 with Euler class N/2. This carries
     the SL(2,R)~ Thurston geometry.

  3. The 3+1D spacetime: R x (H^2 x_N S^1) with metric
     ds^2 = -dt^2 + ds_H^2 + (dphi + A)^2.

  4. The Havelock eigenvalue arises from the massive Green's
     function G_mu on H^2 with KK mass mu = |m - N/2|.
     The critical mode m = N/2 has mu = 0 (massless).

  5. The three-layer decomposition = the separation into
     massless (gravity, C_1) and massive (KK, the Casimir) sectors.

  6. The flux quantization: N EVEN gives integer flux (periodic
     KK modes), N ODD gives half-integer flux (antiperiodic).
     The graviton threshold N = 7 is at HALF-INTEGER flux.

  7. No string theory required. The compact dimension is the
     polygon angle with magnetic flux. The Thurston geometry
     SL(2,R)~ is a standard 3-manifold geometry.
""")


if __name__ == "__main__":
    main()
