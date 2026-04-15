"""
Exploration: try to match Z_polygon(β) with Z_CS(k) term by term to derive c = 12 b(N).

The paper's Derivation 1 claims Z_vortex = Z_CS at β = 1/b(N), k = 2 b(N).
Let me check this numerically.

Z_polygon(β) = Π 1/(2 sinh(β λ_m / 2))  for non-critical modes

Z_CS(k) on H² ×_N S¹ with N Wilson lines: requires the Witten formula.
For SU(2)_k CS on S³ with N Wilson loops in rep j_m:
  Z = Σ_j S_{0j}^{N} / S_{00}^{N-1}  (Verlinde)
where S_{0j} = √(2/(k+2)) sin(π(2j+1)/(k+2)).

For our Seifert manifold H² ×_N S¹ with N Wilson lines at Z_N-symmetric points,
the structure is more involved — the Seifert fibration introduces a specific
monodromy that affects the partition function.
"""
import sys
sys.path.insert(0, '/mnt/c/Users/gspea/source/repos/planetary-polygons-unified')

from math import cos, cosh, log, pi, sin, sinh, sqrt
import numpy as np

from src.planetary_polygons.extensions.cft_central_charge import (
    Z_polygon_harmonic, log_Z_polygon, havelock_eigenvalues, b_N, mean_casimir
)


def log_Z_CS_SU2_S3_Nunknots_j(N: int, k: int, j_half: float = 0.5) -> float:
    """SU(2)_k CS on S³ with N unknots in rep j (Witten 1989).

    Z = (sum over intermediate reps j') of (S_{jj'} / S_{0j'})^N S_{0j'}²

    For the standard Witten formula with N unknots in fundamental (j=1/2):
        Z = Σ_{j'} S_{jj'}^N / S_{0j'}^{N-2}
    """
    def S(a, b):
        return sqrt(2/(k+2)) * sin(pi * (2*a + 1) * (2*b + 1) / (k + 2))

    total = 0.0
    for j_prime_twice in range(k + 1):
        j_prime = j_prime_twice / 2
        num = S(j_half, j_prime) ** N
        den = S(0, j_prime) ** (N - 2)
        if abs(den) < 1e-15:
            continue
        total += num / den
    return log(abs(total))


def log_Z_CS_simple(N: int, k: int) -> float:
    """Simplest CS partition function: trivial Wilson lines, S³ topology."""
    # Z = Σ_j S_{0j}^N / S_{00}^{N-2}
    def S(a, b):
        return sqrt(2/(k+2)) * sin(pi * (2*a + 1) * (2*b + 1) / (k + 2))

    S00 = S(0, 0)
    total = 0.0
    for j_twice in range(k + 1):
        j = j_twice / 2
        total += S(0, j) ** N / S00 ** (N - 2)
    return log(abs(total))


def log_Z_polygon_with_zero_mode(N: int, beta: float) -> float:
    """Polygon partition function including zero-mode contribution.

    Z_polygon = (zero-mode volume) × Π 1/(2 sinh(β λ_m/2))

    The zero-mode is the rigid rotation of the polygon (center of mass).
    """
    eigs = havelock_eigenvalues(N)
    # Harmonic modes contribution
    log_Z = -sum(log(2 * sinh(beta * lam / 2)) for lam in eigs)
    # Zero-mode contribution: rigid rotation adds 2π factor
    # (We'll ignore this for now — focus on mode structure)
    return log_Z


print("=" * 72)
print("Attempting direct match: Z_polygon vs Z_CS at k = 2 b(N), β = 1/b(N)")
print("=" * 72)

for N in [3, 5, 7, 11]:
    print(f"\n=== N = {N} ===")
    b = b_N(N)
    c_predicted = 12 * b
    k_predicted = 2 * b
    print(f"  b(N) = {b:.4f}")
    print(f"  Predicted c = 12 b(N) = {c_predicted:.4f}")
    print(f"  Predicted k = 2 b(N) = {k_predicted:.4f}  (continuous; round to integer for SU(2))")

    # Onsager temperature β = 1/b(N)
    beta = 1 / b
    print(f"  β = 1/b(N) = {beta:.4f}")

    # Polygon partition function
    logZ_poly = log_Z_polygon(N, beta)
    print(f"  log Z_polygon(β = 1/b(N)) = {logZ_poly:.4f}")

    # CS partition function at nearest integer k
    k_int = round(k_predicted)
    try:
        logZ_cs = log_Z_CS_simple(N, k_int)
        print(f"  log Z_CS (S³, k = {k_int}) = {logZ_cs:.4f}")
        print(f"  Match ratio: log Z_poly / log Z_CS = {logZ_poly/logZ_cs:.4f}")
    except Exception as e:
        print(f"  CS computation failed: {e}")

# Try a different normalization: Z_poly at β = 2π/b(N) (conformal frame)
print("\n" + "=" * 72)
print("Alternative: β = 2π/b(N) (conformal temperature)")
print("=" * 72)

for N in [3, 5, 7, 11]:
    b = b_N(N)
    beta = 2 * pi / b
    logZ_poly = log_Z_polygon(N, beta)
    print(f"N={N}: log Z_poly(β=2π/b) = {logZ_poly:.4f}")

# Test: is there any β where Z_poly EXACTLY equals the CS partition function?
print("\n" + "=" * 72)
print("Structure check: factorization patterns")
print("=" * 72)

for N in [5, 7, 11]:
    eigs = havelock_eigenvalues(N)
    b = b_N(N)
    print(f"\nN={N}: eigs = {eigs}, b(N) = {b:.4f}")
    # At β = 1, look at λ_m/2 sinh factors
    for beta in [1.0, 2.0, pi/2, 2*pi, 1/b]:
        factors = [2 * sinh(beta * lam / 2) for lam in eigs]
        print(f"  β={beta:.4f}: sinh factors = {[round(f, 4) for f in factors]}")
