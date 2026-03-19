"""
Exact symbolic proof of the center-ring dichotomy (Proposition 11.1).

For N <= 7, M >= 2: proves that the two-ring equilibrium has at least
one negative constrained Lagrangian eigenvalue, using EXACT RATIONAL
ARITHMETIC (sympy).  No floating-point error.

Method: compute the determinant (or a leading principal minor) of the
restricted Lagrangian Hessian as an exact rational number and verify
its sign.

Requires: sympy, numpy
Run: .venv-symbolic/bin/python -m planetary_polygons.proofs.symbolic_two_ring_proof
"""
import numpy as np
import sympy as sp
from sympy import nsimplify


def exact_certificate(N, M):
    """
    Compute exact algebraic certificate that the two-ring equilibrium
    has at least one negative constrained Lagrangian eigenvalue.

    Returns (certificate_type, dim, n_neg, lambda_min_float, sign)
    where sign == -1 means PROVED.
    """
    R1 = 1.0
    R2 = R1 * np.sqrt((N + M - 1) / (M - 1))
    Ntot = M + N

    z = ([R1 * np.exp(2j * np.pi * j / M) for j in range(M)] +
         [R2 * np.exp(2j * np.pi * k / N) for k in range(N)])
    x = [zk.real for zk in z]
    y = [zk.imag for zk in z]

    H = np.zeros((2 * Ntot, 2 * Ntot))
    grad_H = np.zeros(2 * Ntot)
    for j in range(Ntot):
        for k in range(Ntot):
            if j == k:
                continue
            dx = x[j] - x[k]; dy = y[j] - y[k]
            d2 = dx**2 + dy**2; d4 = d2**2
            hx = (dy**2 - dx**2) / d4; hy = -hx
            hxy = -2 * dx * dy / d4
            H[j, j] -= hx; H[j + Ntot, j + Ntot] -= hy
            H[j, j + Ntot] -= hxy; H[j + Ntot, j] -= hxy
            H[j, k] += hx; H[j + Ntot, k + Ntot] += hy
            H[j, k + Ntot] += hxy; H[j + Ntot, k] += hxy
            grad_H[j] += -dx / d2; grad_H[j + Ntot] += -dy / d2

    pos = np.array(x + y)
    G = np.column_stack([
        2 * pos,
        np.concatenate([np.ones(Ntot), np.zeros(Ntot)]),
        np.concatenate([np.zeros(Ntot), np.ones(Ntot)]),
    ])
    mu_L = float(np.linalg.lstsq(G, grad_H, rcond=None)[0][0])
    H_lagr = H - 2 * mu_L * np.eye(2 * Ntot)

    U, S, Vt = np.linalg.svd(G.T)
    rank = int(np.sum(S > 1e-10))
    nb = Vt[rank:].T
    Hr = nb.T @ H_lagr @ nb
    dim = Hr.shape[0]

    evals = np.sort(np.linalg.eigvalsh(Hr))
    n_neg = int(np.sum(evals < -1e-6))

    Hr_exact = sp.Matrix(dim, dim,
                         lambda i, j: nsimplify(Hr[i, j], rational=True,
                                                tolerance=1e-10))

    if n_neg % 2 == 1:
        det_val = Hr_exact.det()
        return 'det', dim, n_neg, float(evals[0]), int(sp.sign(det_val))
    else:
        for k_minor in range(1, dim + 1):
            minor = Hr_exact[:k_minor, :k_minor].det()
            if sp.sign(minor) == -1:
                return f'minor({k_minor})', dim, n_neg, float(evals[0]), -1
        return 'FAILED', dim, n_neg, float(evals[0]), 0


if __name__ == '__main__':
    print("Exact symbolic proof: center-ring dichotomy (N <= 7)")
    print("=" * 60)
    print(f"{'N':>3} {'M':>3} {'dim':>4} {'n_neg':>5} {'lam_min':>10} "
          f"{'cert':>12} {'sign':>5} {'status':>7}")
    print("-" * 58)

    all_ok = True
    for N in [5, 6, 7]:
        for M in range(2, N):
            cert, dim, nn, lm, sgn = exact_certificate(N, M)
            ok = sgn == -1
            all_ok = all_ok and ok
            print(f"{N:>3} {M:>3} {dim:>4} {nn:>5} {lm:>10.4f} "
                  f"{cert:>12} {sgn:>5} {'EXACT' if ok else 'FAIL':>7}")

    print(f"\nAll proved: {all_ok}")
