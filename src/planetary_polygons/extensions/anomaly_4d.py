"""
The Weyl anomaly in the 4D picture: orbifold correction from Z_N fixed points.

The anomaly delta_m is the mode-resolved difference between:
- The CONTINUUM prediction: f(m,N) = m(N-m)/2 (from the smooth S^1 fiber)
- The DISCRETE computation: the actual Havelock eigenvalue sum

This difference comes from the Z_N LATTICE STRUCTURE of the polygon.
In the KK picture, it's the ORBIFOLD CORRECTION from the N fixed
points of Z_N acting on S^1.

The correction involves CHARACTER SUMS:
- Cotangent sum: Sigma cot(pi p/N) cos(2pi pm/N) = N - 2m
- Cosecant squared sum: Sigma csc^2(pi p/N) cos(2pi pm/N) = ?
- Log-sine Fourier coefficients: the Havelock kernel on Z/NZ

The anomaly should decompose into these sums with Bernoulli
number coefficients.
"""

import numpy as np
from math import pi, sin, cos, log, sqrt, sinh


def casimir(m, N):
    return m * (N - m) / 2.0


def b_exact(N):
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


# =====================================================================
# PART 1: Compute delta_m exactly
# =====================================================================

def compute_delta(N):
    """Compute the Weyl anomaly delta_m for all modes."""
    S = []  # the flat Havelock eigenvalue
    for m in range(1, N):
        S_m = sum(-log(2 * abs(sin(pi * p / N))) * cos(2 * pi * p * m / N)
                  for p in range(1, N))
        S.append(S_m)

    S = np.array(S)
    f = np.array([casimir(m, N) for m in range(1, N)])

    # D(m) = S_m + f_m (the aliasing: deviation from Havelock identity)
    D = S + f

    # delta_m = D(m) - <D> (mean-subtracted aliasing)
    D_mean = np.mean(D)
    delta = D - D_mean

    return S, f, D, D_mean, delta


# =====================================================================
# PART 2: The trigonometric character sums
# =====================================================================

def cotangent_sum(m, N):
    """C(m,N) = Sigma_{p=1}^{N-1} cot(pi p/N) * cos(2pi pm/N).

    Known result: C(m,N) = N - 2m for 1 <= m <= N-1.
    """
    numerical = sum(cos(pi * p / N) / sin(pi * p / N) * cos(2 * pi * p * m / N)
                    for p in range(1, N))
    analytical = N - 2 * m
    return numerical, analytical


def cosecant_sq_sum(m, N):
    """S2(m,N) = Sigma_{p=1}^{N-1} csc^2(pi p/N) * cos(2pi pm/N).

    This is related to the second derivative of the log-sine kernel.
    """
    return sum(1 / sin(pi * p / N)**2 * cos(2 * pi * p * m / N)
               for p in range(1, N))


def cosecant_sum(m, N):
    """S1(m,N) = Sigma_{p=1}^{N-1} csc(pi p/N) * cos(2pi pm/N)."""
    return sum(1 / sin(pi * p / N) * cos(2 * pi * p * m / N)
               for p in range(1, N))


def log_sin_sum(m, N):
    """L(m,N) = Sigma_{p=1}^{N-1} [-log(sin(pi p/N))] * cos(2pi pm/N).

    Note: this is S_m + log(2) * Sigma cos = S_m - log(2)
    where S_m is the flat Havelock eigenvalue.
    """
    return sum(-log(sin(pi * p / N)) * cos(2 * pi * p * m / N)
               for p in range(1, N))


def cot_sq_sum(m, N):
    """Sigma cot^2(pi p/N) * cos(2pi pm/N)."""
    return sum((cos(pi * p / N) / sin(pi * p / N))**2 * cos(2 * pi * p * m / N)
               for p in range(1, N))


# =====================================================================
# PART 3: Decompose delta_m into character sums
# =====================================================================

def decompose_anomaly(N):
    """Express delta_m as a linear combination of character sums."""
    S, f, D, D_mean, delta = compute_delta(N)

    modes = list(range(1, N))
    n_modes = N - 1

    # Compute all the character sums
    cot_vals = np.array([cotangent_sum(m, N)[0] for m in modes])
    csc2_vals = np.array([cosecant_sq_sum(m, N) for m in modes])
    csc_vals = np.array([cosecant_sum(m, N) for m in modes])
    logsin_vals = np.array([log_sin_sum(m, N) for m in modes])
    cot2_vals = np.array([cot_sq_sum(m, N) for m in modes])

    # The KK mass
    mu_vals = np.array([abs(m - N/2) for m in modes])
    mu2_vals = mu_vals**2

    # Also: (N-2m)^2 = 4*mu^2
    n2m_sq = np.array([(N - 2*m)**2 for m in modes])

    print(f"\n  N = {N}: Character sums and delta_m")
    print(f"  {'m':>4s} {'delta':>10s} {'cot':>8s} {'csc2':>10s} "
          f"{'csc':>10s} {'logsin':>10s} {'mu^2':>8s}")

    for i, m in enumerate(modes):
        print(f"  {m:4d} {delta[i]:10.6f} {cot_vals[i]:8.2f} "
              f"{csc2_vals[i]:10.4f} {csc_vals[i]:10.4f} "
              f"{logsin_vals[i]:10.4f} {mu2_vals[i]:8.4f}")

    # Try various linear fits
    print(f"\n  Linear regression: delta = a*X + b")

    candidates = {
        'cot': cot_vals,
        'csc^2': csc2_vals,
        'csc': csc_vals,
        'log sin': logsin_vals,
        'cot^2': cot2_vals,
        'mu^2': mu2_vals,
        '(N-2m)': np.array([N - 2*m for m in modes], dtype=float),
    }

    for name, X in candidates.items():
        A = np.column_stack([X, np.ones(n_modes)])
        coeffs, _, _, _ = np.linalg.lstsq(A, delta, rcond=None)
        fitted = A @ coeffs
        residuals = delta - fitted
        R2 = 1 - np.var(residuals) / np.var(delta) if np.var(delta) > 0 else 0
        print(f"  {name:>10s}: a = {coeffs[0]:+10.6f}, b = {coeffs[1]:+10.6f}, R^2 = {R2:.8f}")

    # Two-variable fits
    print(f"\n  Two-variable regression: delta = a*X1 + b*X2 + c")

    pairs = [
        ('cot + csc^2', cot_vals, csc2_vals),
        ('cot + mu^2', cot_vals, mu2_vals),
        ('csc + csc^2', csc_vals, csc2_vals),
        ('cot + cot^2', cot_vals, cot2_vals),
        ('logsin + csc^2', logsin_vals, csc2_vals),
        ('mu^2 + csc^2', mu2_vals, csc2_vals),
    ]

    best_R2 = 0
    best_name = ""
    best_coeffs = None

    for name, X1, X2 in pairs:
        A = np.column_stack([X1, X2, np.ones(n_modes)])
        coeffs, _, _, _ = np.linalg.lstsq(A, delta, rcond=None)
        fitted = A @ coeffs
        residuals = delta - fitted
        R2 = 1 - np.var(residuals) / np.var(delta) if np.var(delta) > 0 else 0
        print(f"  {name:>18s}: a={coeffs[0]:+8.5f}, b={coeffs[1]:+8.5f}, "
              f"c={coeffs[2]:+8.5f}, R^2={R2:.8f}")

        if R2 > best_R2:
            best_R2 = R2
            best_name = name
            best_coeffs = coeffs

    # The D(m) directly (not mean-subtracted)
    print(f"\n  Direct aliasing D(m) = S_m + f_m:")
    print(f"  {'m':>4s} {'D(m)':>10s} {'csc^2':>10s} {'D/csc2':>10s}")

    for i, m in enumerate(modes):
        d = D[i]
        c2 = csc2_vals[i]
        ratio = d / c2 if abs(c2) > 0.01 else float('nan')
        print(f"  {m:4d} {d:10.6f} {c2:10.4f} {ratio:10.6f}")

    return delta, cot_vals, csc2_vals, mu2_vals, best_name, best_R2


# =====================================================================
# PART 4: The universal decomposition
# =====================================================================

def universal_decomposition():
    """Find the decomposition that works for ALL N."""
    print(f"\n{'='*72}")
    print("  UNIVERSAL DECOMPOSITION ACROSS ALL N")
    print("=" * 72)

    print(f"\n  For each N, find the best fit delta = a*csc^2 + b*cot + c:\n")
    print(f"  {'N':>4s} {'a (csc^2)':>12s} {'b (cot)':>10s} {'c (const)':>10s} "
          f"{'R^2':>10s}")

    a_vals = []
    b_vals = []

    for N in range(5, 20):
        S, f, D, D_mean, delta = compute_delta(N)
        modes = list(range(1, N))

        cot_v = np.array([cotangent_sum(m, N)[0] for m in modes])
        csc2_v = np.array([cosecant_sq_sum(m, N) for m in modes])

        A = np.column_stack([csc2_v, cot_v, np.ones(N-1)])
        coeffs, _, _, _ = np.linalg.lstsq(A, delta, rcond=None)
        fitted = A @ coeffs
        resid = delta - fitted
        R2 = 1 - np.var(resid) / np.var(delta) if np.var(delta) > 0 else 0

        a_vals.append(coeffs[0])
        b_vals.append(coeffs[1])

        print(f"  {N:4d} {coeffs[0]:12.8f} {coeffs[1]:10.6f} "
              f"{coeffs[2]:10.6f} {R2:10.8f}")

    # Check if a(N) and b(N) have a pattern
    print(f"\n  Pattern in the coefficients:")
    print(f"  {'N':>4s} {'a':>12s} {'a*12':>10s} {'a*N':>10s} "
          f"{'a*N^2':>10s} {'b':>10s} {'b*N':>10s}")

    for i, N in enumerate(range(5, 20)):
        a = a_vals[i]
        b = b_vals[i]
        print(f"  {N:4d} {a:12.8f} {a*12:10.6f} {a*N:10.6f} "
              f"{a*N**2:10.4f} {b:10.6f} {b*N:10.6f}")


# =====================================================================
# PART 5: The Dedekind sum connection
# =====================================================================

def dedekind_connection():
    """Test whether delta_m involves Dedekind sums."""
    print(f"\n{'='*72}")
    print("  THE DEDEKIND SUM CONNECTION")
    print("=" * 72)

    print(f"""
  The Dedekind sum s(m, N) = (1/4N) Sigma cot(pi p/N) cot(pi pm/N)
  arises in the transformation formula of the Dedekind eta function
  and in the Atiyah-Patodi-Singer eta invariant.

  For the Z_N orbifold, the orbifold correction to the spectral
  zeta function involves:
    delta_zeta(m) = (1/N) Sigma_{{k=1}}^{{N-1}} chi_m(k) * s(k, N)

  where chi_m(k) = exp(2*pi*i*k*m/N) is the character.
""")

    for N in [6, 7, 8, 10]:
        print(f"\n  N = {N}:")
        S, f, D, D_mean, delta = compute_delta(N)

        # Compute the Dedekind sum s(m, N)
        print(f"  {'m':>4s} {'delta_m':>12s} {'s(m,N)':>12s} "
              f"{'12Ns':>10s} {'delta/s':>10s}")

        for m in range(1, N):
            if m == 0 or m == N:
                continue

            # Dedekind sum
            s_mN = sum(cos(pi*p/N)/sin(pi*p/N) * cos(pi*p*m/N)/sin(pi*p*m/N)
                       for p in range(1, N) if abs(sin(pi*p*m/N)) > 1e-10) / (4*N)

            d = delta[m-1]
            ratio = d / s_mN if abs(s_mN) > 1e-10 else float('nan')

            print(f"  {m:4d} {d:12.6f} {s_mN:12.6f} "
                  f"{12*N*s_mN:10.4f} {ratio:10.4f}")


# =====================================================================
# PART 6: The exact formula
# =====================================================================

def exact_formula():
    """Try to find the exact formula for delta_m."""
    print(f"\n{'='*72}")
    print("  SEARCHING FOR THE EXACT FORMULA")
    print("=" * 72)

    print(f"""
  D(m,N) = S_m + f(m,N) is the full aliasing.

  S_m = Sigma [-log(2sin(pi p/N))] cos(2pi pm/N)
      = (1/N) Sigma_k [aliased 1/k] cos(2pi km/N)

  Using the aliased Fourier series:
  Sigma_p [-log(2sin(pi p/N))] cos(2pi pm/N)
  = (N/2) Sigma_{{j=0}}^inf [1/(jN+m) + 1/(jN+N-m)] - H_{{N-1}}

  where H_n is the harmonic number.

  Subtracting f(m,N): D(m,N) = [aliased sum] + f(m,N) - S_m
  ... this is getting circular.

  Let me try a DIFFERENT decomposition of D(m,N).

  D(m,N) = S_m + f(m,N) = Sigma [-log(2sin)] cos + m(N-m)/2.

  The CLOSED FORM for D(m,N) involves the digamma function:
  D(m,N) = (N/2)[psi(m/N) + psi(1-m/N)] / (-2) + gamma + ...
  Hmm, this is related to the REFLECTION FORMULA of the digamma.

  Actually: Sigma_{{p=1}}^{{N-1}} log(sin(pi p/N)) = log(N/2^{{N-1}}) [product formula]
  And the mode-resolved version involves digamma sums.
""")

    # Compute D(m,N) and test specific formulas
    for N in [8, 10, 12]:
        S, f, D, D_mean, delta = compute_delta(N)

        print(f"\n  N = {N}, <D> = {D_mean:.6f}, N^2/12 = {N**2/12:.6f}")
        print(f"  {'m':>4s} {'D(m)':>10s} {'m(N-m)(2N-1)/6N':>18s} "
              f"{'match':>8s} {'D - formula':>12s}")

        # Test: D(m,N) = m(N-m)(2N-1)/(6N)?
        # No... let me test other possibilities.

        # Test: D(m,N) = (N^2-1)/12 - m(N-m)*(something)?
        # <D> ~ N^2/12 + N/12 - log(2) + log(N)/(N-1) - N(N+1)/12
        # Hmm, <D> = b(N) - <f> ... no.

        # Actually: D(m,N) = S_m + f(m,N)
        # and S_m + f(m,N) = [some function of m and N]
        # We computed earlier that <S_m + f_m> = b(N)
        # And b(N) = N(N+1)/12 - log(2) + log(N)/(N-1)
        # But D(m) is the MODE-RESOLVED version.

        # Let me just look at the ratios D(m)/f(m):
        for i, m in enumerate(range(1, N)):
            fm = casimir(m, N)
            d = D[i]
            ratio_f = d / fm if abs(fm) > 0.01 else float('nan')

            # Test formula: D = f * (something simple)?
            # Or D = f + (something involving N only)?
            d_minus_f = d - fm

            print(f"  {m:4d} {d:10.6f} {d_minus_f:18.6f} "
                  f"{'':>8s} {d - D_mean:12.6f}")


# =====================================================================
# MAIN
# =====================================================================

def main():
    print("=" * 72)
    print("  THE WEYL ANOMALY IN THE 4D PICTURE")
    print("  Orbifold correction from Z_N fixed points")
    print("=" * 72)

    # Part 1: Verify the cotangent sum
    print(f"\n{'='*72}")
    print("  PART 1: Cotangent sum verification")
    print("=" * 72)

    print(f"\n  C(m,N) = Sigma cot(pi p/N) cos(2pi pm/N) = N - 2m ?")
    print(f"  {'N':>4s} {'m':>4s} {'numerical':>12s} {'N-2m':>8s} {'match':>8s}")

    for N in [6, 7, 8]:
        for m in range(1, N):
            num, ana = cotangent_sum(m, N)
            match = abs(num - ana) < 1e-8
            print(f"  {N:4d} {m:4d} {num:12.6f} {ana:8.2f} "
                  f"{'YES' if match else 'no':>8s}")

    # Part 2: Decompose delta for specific N
    for N in [7, 8, 10]:
        print(f"\n{'='*72}")
        print(f"  DECOMPOSITION OF delta_m FOR N = {N}")
        print("=" * 72)
        decompose_anomaly(N)

    # Part 3: Universal decomposition
    universal_decomposition()

    # Part 4: Dedekind sums
    dedekind_connection()

    # Part 5: Exact formula search
    exact_formula()

    # Summary
    print(f"\n{'='*72}")
    print("  SUMMARY")
    print("=" * 72)


if __name__ == "__main__":
    main()
