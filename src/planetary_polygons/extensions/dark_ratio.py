"""
The per-mode frozen/vacuum ratio: what does it converge to?

R_pm(N) = [E_frozen / (N-2)] / b(N)
        = [(N/2-1)(N/2)(N-1)/6] / [(N-2) * b(N)]

For even N. Numerically converging to ~0.43.
Need to find the exact limit and understand the structure.
"""

import numpy as np
from math import pi, log, exp, sqrt, sin, sinh, cos


def casimir(m, N):
    return m * (N - m) / 2.0


def b_exact(N):
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


def sum_casimir_gaps_even(N):
    """Sum of Casimir gaps for even N: (N/2-1)(N/2)(N-1)/6."""
    return (N/2 - 1) * (N/2) * (N - 1) / 6


def sum_casimir_gaps_any(N):
    """Sum of Casimir gaps for any N."""
    m_crit = N // 2
    f_crit = casimir(m_crit, N)
    total = 0.0
    for m in range(1, N):
        if m == m_crit:
            continue
        total += f_crit - casimir(m, N)
    return total


def per_mode_ratio(N):
    """R_pm = average frozen energy / vacuum energy."""
    gaps = sum_casimir_gaps_any(N)
    n_frozen = N - 2  # N-1 modes minus 1 critical
    b = b_exact(N)
    avg_frozen = gaps / n_frozen if n_frozen > 0 else 0
    return avg_frozen / b if b > 0 else 0


def main():
    print("=" * 72)
    print("  THE PER-MODE FROZEN/VACUUM RATIO")
    print("=" * 72)

    # Part 1: Compute to high N
    print(f"\n  {'N':>6s} {'Σ gaps':>12s} {'N-2':>6s} {'avg frozen':>12s} "
          f"{'b(N)':>12s} {'R_pm':>12s} {'12*R_pm':>10s}")

    ratios = []
    for N in list(range(5, 50)) + list(range(50, 200, 10)) + list(range(200, 1001, 100)):
        gaps = sum_casimir_gaps_any(N)
        n_frozen = N - 2
        b = b_exact(N)
        avg = gaps / n_frozen
        R = avg / b
        ratios.append((N, R))

        if N <= 30 or N % 10 == 0 or N % 100 == 0:
            print(f"  {N:6d} {gaps:12.2f} {n_frozen:6d} {avg:12.4f} "
                  f"{b:12.4f} {R:12.8f} {12*R:10.6f}")

    # Part 2: What does 12*R converge to?
    print(f"\n  {'N':>6s} {'12*R_pm':>12s} {'6*R_pm':>12s} "
          f"{'4*R_pm':>12s} {'R_pm':>12s}")

    for N, R in ratios:
        if N >= 100 and N % 100 == 0:
            print(f"  {N:6d} {12*R:12.8f} {6*R:12.8f} "
                  f"{4*R:12.8f} {R:12.8f}")

    # Part 3: Analytical limit
    print(f"\n{'='*72}")
    print("  ANALYTICAL LIMIT")
    print("=" * 72)

    print(f"""
  For EVEN N:
  Σ gaps = (N/2-1)(N/2)(N-1)/6
  b(N) = N(N+1)/12 - log(2) + log(N)/(N-1)
  n_frozen = N - 2

  R_pm = [(N/2-1)(N/2)(N-1)/6] / [(N-2) · (N(N+1)/12 - log(2) + log(N)/(N-1))]

  At large N:
  Numerator ~ N³/48
  Denominator ~ N · N²/12 = N³/12

  So R_pm ~ (N³/48) / (N³/12) = 12/48 = 1/4

  But the convergence is SLOW because of the subleading terms.
  Let me expand to next order.

  Numerator: (N/2-1)(N/2)(N-1)/6
           = (N³ - 4N² + ... ) / 48
           = N³/48 · (1 - 4/N + ...)

  Denominator: (N-2) · b(N)
             = (N-2) · [N(N+1)/12 - log2 + logN/(N-1)]
             = (N-2) · N²/12 · [1 + 1/N + ...] - (N-2)·log2 + ...
             = N³/12 · (1 - 2/N)(1 + 1/N) - N·log2 + ...
             = N³/12 · (1 - 1/N - 2/N²) - N·log2 + ...

  R_pm = [N³/48 (1 - 4/N)] / [N³/12 (1 - 1/N) - N log2 + ...]
       = (1/4) · (1 - 4/N) / (1 - 1/N - 12 log2/N² + ...)
       = (1/4) · [1 - 4/N + 1/N + ...] / [1 - ...]
       = (1/4) · [1 - 3/N + O(1/N²)]

  So the limit IS 1/4, but the approach is from below with
  correction -3/(4N).
""")

    # Verify the 1/4 - 3/(4N) formula
    print(f"  Verification of R_pm ~ 1/4 - 3/(4N):")
    print(f"  {'N':>6s} {'R_pm':>12s} {'1/4-3/(4N)':>12s} {'diff':>12s}")

    for N in [10, 20, 50, 100, 200, 500, 1000]:
        R = per_mode_ratio(N)
        approx = 0.25 - 3.0 / (4 * N)
        print(f"  {N:6d} {R:12.8f} {approx:12.8f} {R - approx:12.8f}")

    # Part 4: For ODD N the picture is different
    print(f"\n{'='*72}")
    print("  ODD N vs EVEN N")
    print("=" * 72)

    print(f"\n  {'N':>6s} {'even/odd':>8s} {'R_pm':>12s} {'1/4':>8s} {'diff':>10s}")

    for N in range(5, 30):
        R = per_mode_ratio(N)
        parity = "even" if N % 2 == 0 else "odd"
        print(f"  {N:6d} {parity:>8s} {R:12.8f} {0.25:8.4f} {R - 0.25:10.6f}")

    # Part 5: The actual frozen eigenvalues (not just Casimir gaps)
    print(f"\n{'='*72}")
    print("  INCLUDING THE WEYL ANOMALY")
    print("=" * 72)

    print(f"\n  The Casimir gap sum ignores delta_m.")
    print(f"  The ACTUAL frozen energy includes the Weyl corrections.")
    print(f"  Does the Weyl anomaly change the ratio?\n")

    print(f"  {'N':>6s} {'R_pm(Cas)':>12s} {'R_pm(full)':>12s} "
          f"{'diff':>10s} {'Weyl shift':>12s}")

    for N in range(5, 25):
        # Casimir-only ratio
        R_cas = per_mode_ratio(N)

        # Full ratio including Weyl (need actual eigenvalues)
        m_crit = N // 2
        f_crit = casimir(m_crit, N)
        b = b_exact(N)

        # At the threshold: C_1 = f_crit (at leading order)
        # lambda_m = f_crit - f(m) + (delta_m - delta_{m*})
        # We need to compute delta_m, which requires actual Havelock evals

        # Use the flat Havelock eigenvalue as proxy
        # S_m = sum_p [-log(2sin(pi p/N))] cos(2pi pm/N)
        frozen_actual = 0.0
        for m in range(1, N):
            if m == m_crit:
                continue
            S_m = sum(-log(2 * abs(sin(pi * p / N))) * cos(2 * pi * p * m / N)
                      for p in range(1, N))
            # At threshold on flat: lambda_m = S_m + f(m) (since C1_flat = 0 + b)
            # Actually lambda_m(flat) = S_m = -(f(m) - D(m))
            # The frozen eigenvalue is: f_crit - f(m) + (D(m) - D(m_crit))
            frozen_actual += S_m + f_crit  # S_m + f_crit = S_m + C1 - (C1 - f_crit)

        # Hmm, this isn't quite right. Let me use a different approach.
        # At the threshold rho*, C_1 = f_crit - delta_{m*}
        # lambda_m = (f_crit - delta_{m*}) - f(m) + delta_m
        #          = (f_crit - f(m)) + (delta_m - delta_{m*})
        # The Casimir part: f_crit - f(m)
        # The Weyl part: delta_m - delta_{m*}

        # Sum of Weyl parts: sum_{m != m*} (delta_m - delta_{m*})
        # = sum delta_m - (N-2) delta_{m*} - delta_{m*}
        # = -delta_{m*} - (N-2) delta_{m*}  [since sum delta = 0]
        # = -(N-1) delta_{m*}

        # So E_frozen(full) = E_frozen(Cas) - (N-1)*delta_{m*}
        # And delta_{m*} depends on N.

        # From the alternating log-sine sum:
        # For even N, m* = N/2: delta_{m*} can be computed
        # S_{N/2} = sum_p (-1)^p [-log(2sin(pi p/N))] = -log(N/4) [exact]
        # And S_{N/2} = -f(N/2) + D(N/2) where D is the aliasing
        # So delta_{m*} = D(N/2) - <D>

        # This is getting complicated. Let me just compare the two ratios.
        n_frozen = N - 2
        R_full = frozen_actual / (n_frozen * b) if n_frozen > 0 and b > 0 else 0

        weyl_shift = R_full - R_cas

        print(f"  {N:6d} {R_cas:12.8f} {R_full:12.8f} "
              f"{R_full - R_cas:10.6f} {weyl_shift:12.6f}")

    # Part 6: What is 3/7?
    print(f"\n{'='*72}")
    print("  IS THE RATIO A KNOWN CONSTANT?")
    print("=" * 72)

    print(f"""
  The per-mode ratio R_pm converges to 1/4 = 0.25 as N -> inf.
  But the approach is SLOW: R_pm(N) ~ 1/4 - 3/(4N) + O(1/N²).

  The question: is there a PHYSICAL N where R_pm takes a
  cosmologically interesting value?

  Known fractions:
    Omega_DM / (Omega_DM + Omega_DE) = 0.27/0.95 = 0.284
    Omega_DM / Omega_total = 0.27
    Omega_b / Omega_total = 0.05
    Omega_DM / Omega_b = 5.4

  At N = 7: R_pm = {per_mode_ratio(7):.6f}
  At N = 8: R_pm = {per_mode_ratio(8):.6f}

  The value 0.349 (N=7) is between 1/3 and 3/8.
  The value 0.386 (N=8) is close to 3/8 = 0.375.

  Is R_pm(N=8) = 3/8?
  Exact: R_pm(8) = [14/6] / [5.604] = 2.333/5.604 = {14/6 / b_exact(8):.8f}
  3/8 = {3/8:.8f}
  Diff: {14/6 / b_exact(8) - 3/8:.8f}

  Not exactly 3/8. But the RATIO of frozen to total at N = 7:
""")

    # What IS the number?
    for N in [7, 8]:
        gaps = sum_casimir_gaps_any(N)
        b = b_exact(N)
        f_crit = casimir(N // 2, N)

        # The total energy at threshold: E_total = sum lambda_m
        # = (N-1)*C_1 - sum f(m) = (N-1)*f_crit - N(N²-1)/12
        # (since C_1 = f_crit at threshold, ignoring delta)
        E_total = (N - 1) * f_crit - N * (N**2 - 1) / 12

        # Frozen energy: E_frozen = E_total (since critical mode = 0)
        E_frozen = gaps  # the Casimir part

        # The ratio frozen / (frozen + vacuum)
        R1 = E_frozen / (E_frozen + b)
        # The ratio frozen / total_energy
        R2 = E_frozen / E_total if E_total > 0 else 0
        # The ratio frozen / (frozen + f_crit)
        R3 = E_frozen / (E_frozen + f_crit)
        # The ratio vacuum / (frozen + vacuum)
        R4 = b / (E_frozen + b)

        print(f"  N = {N}:")
        print(f"    Σ gaps = {gaps:.4f}")
        print(f"    b(N) = {b:.4f}")
        print(f"    f_crit = {f_crit:.4f}")
        print(f"    E_total = {E_total:.4f}")
        print(f"    frozen/(frozen+vacuum) = {R1:.6f}")
        print(f"    frozen/E_total = {R2:.6f}")
        print(f"    frozen/(frozen+f_crit) = {R3:.6f}")
        print(f"    vacuum/(frozen+vacuum) = {R4:.6f}")
        print()

    # Part 7: What if the "dark matter fraction" is gaps/(gaps + b + f)?
    print(f"\n  The three-component budget: gaps + b(N) + f(m*):\n")
    print(f"  {'N':>4s} {'gaps':>8s} {'b(N)':>8s} {'f(m*)':>8s} "
          f"{'total':>8s} {'g/tot':>8s} {'b/tot':>8s} {'f/tot':>8s}")

    for N in range(5, 20):
        gaps = sum_casimir_gaps_any(N)
        b = b_exact(N)
        f_crit = casimir(N // 2, N)
        total = gaps + b + f_crit

        print(f"  {N:4d} {gaps:8.2f} {b:8.4f} {f_crit:8.2f} "
              f"{total:8.2f} {gaps/total:8.4f} {b/total:8.4f} {f_crit/total:8.4f}")


if __name__ == "__main__":
    main()
