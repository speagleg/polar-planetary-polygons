r"""Stability of regular tessellations: {3,6}, {4,4}, {6,3}.

Extends the single-ring constrained Hessian analysis to tessellations.
Vertices sit at polygon corners. Boundary vertices are fixed (Dirichlet BC).
Interior vertices are free, constrained by angular impulse L = Σ|z_k|².

The headline result: N=3 (triangular tessellation) is the unique regular
tiling that is dynamically stable for ALL interaction ranges Δ ≥ 0.
"""

import math
import numpy as np
from numpy.linalg import eigvalsh, svd, norm


# ============================================================
# Analytical Hessian for V = r^{-2Δ}
# ============================================================

def pairwise_hessian_block(dx, dy, Delta):
    """Analytical second derivatives of V(r) w.r.t. vertex i's position.

    V(r) = r^{-2Δ} for Δ > 0
    V(r) = -log(r) for Δ = 0

    Returns (h_xx, h_yy, h_xy) for d²V/dx_i², d²V/dy_i², d²V/(dx_i dy_i).
    Cross terms: d²V/dx_i dx_j = -h_xx, etc.
    """
    r2 = dx * dx + dy * dy
    if r2 < 1e-30:
        return 0.0, 0.0, 0.0

    if abs(Delta) < 1e-10:
        # Log case: V = -log(r) = -(1/2)log(r²)
        # d²V/dx_i² = (2dx² - r²)/r⁴ = (dx² - dy²)/r⁴
        # d²V/dy_i² = (2dy² - r²)/r⁴ = (dy² - dx²)/r⁴
        # d²V/(dx_i dy_i) = 2 dx dy / r⁴
        r4 = r2 * r2
        h_xx = (dx * dx - dy * dy) / r4
        h_yy = (dy * dy - dx * dx) / r4
        h_xy = 2 * dx * dy / r4
    else:
        # Power law: V = r^{-2Δ} = (r²)^{-Δ}
        s = Delta
        r2_neg_s_m2 = r2 ** (-s - 2)  # r^{-(2Δ+4)}
        coeff = 2 * s
        h_xx = coeff * r2_neg_s_m2 * ((2 * s + 2) * dx * dx - r2)
        h_yy = coeff * r2_neg_s_m2 * ((2 * s + 2) * dy * dy - r2)
        h_xy = coeff * (2 * s + 2) * dx * dy * r2_neg_s_m2

    return h_xx, h_yy, h_xy


def build_hessian(vertices, Delta, cutoff=None):
    """Full analytical Hessian for E = Σ_{i<j} V(|r_i - r_j|).

    vertices: (M, 2) array of positions.
    cutoff: if set, ignore pairs with distance > cutoff.

    Returns: (2M, 2M) symmetric Hessian. Layout: [x₀,...,x_{M-1},y₀,...,y_{M-1}].
    """
    M = len(vertices)
    H = np.zeros((2 * M, 2 * M))

    for i in range(M):
        for j in range(i + 1, M):
            dx = vertices[i, 0] - vertices[j, 0]
            dy = vertices[i, 1] - vertices[j, 1]
            if cutoff is not None and dx * dx + dy * dy > cutoff * cutoff:
                continue

            hxx, hyy, hxy = pairwise_hessian_block(dx, dy, Delta)

            # d²V/dx_i² contribution to diagonal
            H[i, i] += hxx
            H[j, j] += hxx
            H[i + M, i + M] += hyy
            H[j + M, j + M] += hyy
            H[i, i + M] += hxy
            H[i + M, i] += hxy
            H[j, j + M] += hxy
            H[j + M, j] += hxy

            # Cross terms: d²V/dx_i dx_j = -hxx, etc.
            H[i, j] -= hxx
            H[j, i] -= hxx
            H[i + M, j + M] -= hyy
            H[j + M, i + M] -= hyy
            H[i, j + M] -= hxy
            H[j + M, i] -= hxy
            H[i + M, j] -= hxy
            H[j, i + M] -= hxy

    return H


# ============================================================
# Geometry: tessellation patches
# ============================================================

def _unique_vertices(coords, tol=1e-8):
    """Deduplicate vertices, return (unique_verts, index_map).

    index_map[i] gives the unique index of the i-th input coordinate.
    """
    unique = []
    index_map = []
    for c in coords:
        found = False
        for k, u in enumerate(unique):
            if abs(c[0] - u[0]) < tol and abs(c[1] - u[1]) < tol:
                index_map.append(k)
                found = True
                break
        if not found:
            index_map.append(len(unique))
            unique.append(c)
    return np.array(unique), index_map


def hexagon_tessellation(n_rings=1, edge=1.0):
    """Patch of {6,3} tessellation (hexagonal tiling).

    n_rings=1: central hexagon + 6 neighbors = 7 hexagons.

    Returns (vertices, faces, interior_mask).
    """
    # Hexagon centers in axial coordinates
    centers = [(0, 0)]
    if n_rings >= 1:
        # 6 neighbors
        dirs = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
        for dq, dr in dirs:
            centers.append((dq, dr))

    # Convert axial to Cartesian
    hex_spacing = edge * math.sqrt(3)
    cart_centers = []
    for q, r in centers:
        cx = hex_spacing * (q + r * 0.5)
        cy = hex_spacing * r * math.sqrt(3) / 2
        cart_centers.append((cx, cy))

    # Generate hex vertices for each center
    all_coords = []
    face_raw = []
    for cx, cy in cart_centers:
        face = []
        for k in range(6):
            angle = math.pi / 6 + k * math.pi / 3  # pointy-top hex
            vx = cx + edge * math.cos(angle)
            vy = cy + edge * math.sin(angle)
            all_coords.append((vx, vy))
            face.append(len(all_coords) - 1)
        face_raw.append(face)

    # Deduplicate
    vertices, idx_map = _unique_vertices(all_coords)
    faces = [[idx_map[v] for v in f] for f in face_raw]

    # Interior mask: vertex is interior if ALL faces containing it are in the patch
    # Equivalently: for {6,3}, each vertex touches 3 faces. Interior if all 3 are present.
    vertex_face_count = np.zeros(len(vertices), dtype=int)
    for f in faces:
        for v in f:
            vertex_face_count[v] += 1

    # In {6,3}: each vertex should touch 3 faces if fully interior
    interior_mask = vertex_face_count >= 3

    return vertices, faces, interior_mask


def square_tessellation(n_side=3, edge=1.0):
    """Patch of {4,4} tessellation (square tiling).

    n_side=3: 3×3 grid of squares.

    Returns (vertices, faces, interior_mask).
    """
    # Vertices are a (n_side+1) × (n_side+1) grid
    verts = []
    for iy in range(n_side + 1):
        for ix in range(n_side + 1):
            verts.append((ix * edge, iy * edge))
    vertices = np.array(verts)

    # Faces: each square
    faces = []
    for iy in range(n_side):
        for ix in range(n_side):
            v00 = iy * (n_side + 1) + ix
            v10 = v00 + 1
            v01 = v00 + (n_side + 1)
            v11 = v01 + 1
            faces.append([v00, v10, v11, v01])

    # Interior: vertex touches 4 faces (in {4,4})
    vertex_face_count = np.zeros(len(vertices), dtype=int)
    for f in faces:
        for v in f:
            vertex_face_count[v] += 1
    interior_mask = vertex_face_count >= 4

    return vertices, faces, interior_mask


def triangle_tessellation(n_rings=2, edge=1.0):
    """Patch of {3,6} tessellation (triangular tiling).

    Uses a hexagonal-shaped patch of triangles.

    Returns (vertices, faces, interior_mask).
    """
    # Generate vertices on a triangular grid
    all_coords = []
    coord_to_idx = {}

    def add_vertex(x, y):
        key = (round(x / edge * 1000), round(y / edge * 1000))
        if key not in coord_to_idx:
            coord_to_idx[key] = len(all_coords)
            all_coords.append((x, y))
        return coord_to_idx[key]

    h = edge * math.sqrt(3) / 2  # triangle height

    faces = []
    for row in range(-n_rings, n_rings + 1):
        # Determine column range for hexagonal shape
        if row >= 0:
            col_min = -n_rings
            col_max = n_rings - row
        else:
            col_min = -n_rings - row
            col_max = n_rings

        for col in range(col_min, col_max + 1):
            # Base point of upward triangle
            bx = col * edge + row * edge * 0.5
            by = row * h

            # Upward triangle: (bx, by), (bx+edge, by), (bx+edge/2, by+h)
            v0 = add_vertex(bx, by)
            v1 = add_vertex(bx + edge, by)
            v2 = add_vertex(bx + edge / 2, by + h)
            faces.append([v0, v1, v2])

            # Downward triangle (if within bounds):
            # (bx+edge, by), (bx+edge/2, by+h), (bx+3*edge/2, by+h)
            if col < col_max:
                v3 = add_vertex(bx + 3 * edge / 2, by + h)
                faces.append([v1, v3, v2])

    vertices = np.array(all_coords)

    # Interior: vertex touches 6 faces in {3,6}
    vertex_face_count = np.zeros(len(vertices), dtype=int)
    for f in faces:
        for v in f:
            vertex_face_count[v] += 1
    interior_mask = vertex_face_count >= 6

    return vertices, faces, interior_mask


# ============================================================
# Constrained Hessian with Dirichlet boundary
# ============================================================

def tessellation_constrained_eigenvalues(vertices, interior_mask, Delta,
                                         cutoff=None):
    """Constrained Hessian eigenvalues for interior vertices.

    1. Build full Hessian.
    2. Extract submatrix for interior DOFs (Dirichlet BC on boundary).
    3. Apply angular impulse constraint L = Σ|z_k|² for interior vertices.
    4. Project onto constraint tangent space.
    5. Return eigenvalues.
    """
    M = len(vertices)
    H_full = build_hessian(vertices, Delta, cutoff)

    # Extract interior DOFs
    int_idx = np.where(interior_mask)[0]
    n_int = len(int_idx)
    if n_int == 0:
        return {'constrained_evals': np.array([]), 'is_stable': True,
                'n_neg': 0, 'min_eval': 0.0, 'n_interior': 0}

    # DOF indices in the full Hessian: x-coords at int_idx, y-coords at int_idx + M
    dof_idx = np.concatenate([int_idx, int_idx + M])
    H_int = H_full[np.ix_(dof_idx, dof_idx)]

    dim = 2 * n_int

    # Gradient of energy at interior vertices (for Lagrange multiplier)
    # Use analytical gradient
    grad = np.zeros(2 * M)
    for i in range(M):
        for j in range(i + 1, M):
            dx = vertices[i, 0] - vertices[j, 0]
            dy = vertices[i, 1] - vertices[j, 1]
            r2 = dx * dx + dy * dy
            if r2 < 1e-30:
                continue
            if cutoff is not None and r2 > cutoff * cutoff:
                continue

            if abs(Delta) < 1e-10:
                # -log(r) → gradient: -dx/r², -dy/r²
                gx = -dx / r2
                gy = -dy / r2
            else:
                # r^{-2Δ} → gradient: -2Δ r^{-2Δ-2} (dx, dy)
                coeff = -2 * Delta * r2 ** (-Delta - 1)
                gx = coeff * dx
                gy = coeff * dy
            grad[i] += gx
            grad[j] -= gx
            grad[i + M] += gy
            grad[j + M] -= gy

    grad_int = grad[dof_idx]

    # Interior positions for constraint
    int_pos = np.concatenate([vertices[int_idx, 0], vertices[int_idx, 1]])

    # Constraint gradients
    grad_L = 2 * int_pos  # ∂L/∂x_k = 2x_k, ∂L/∂y_k = 2y_k
    G = grad_L.reshape(-1, 1)  # Only angular impulse constraint

    # Lagrange multiplier
    mu, _, _, _ = np.linalg.lstsq(G, grad_int, rcond=None)
    mu_L = mu[0]
    residual = norm(grad_int - G @ mu)

    # Lagrangian Hessian: H_int - 2μ_L · I (since ∇²L = 2I)
    H_lagr = H_int - 2 * mu_L * np.eye(dim)

    # Tangent space of constraint surface
    U, S, Vt = svd(G.T)
    rank = np.sum(S > 1e-10)
    null_basis = Vt[rank:].T

    # Restricted Hessian
    H_rest = null_basis.T @ H_lagr @ null_basis
    evals = eigvalsh(H_rest)

    tol = 1e-4
    n_neg = int(np.sum(evals < -tol))
    min_eval = float(evals[0]) if len(evals) > 0 else 0.0

    return {
        'constrained_evals': evals,
        'is_stable': n_neg == 0,
        'n_neg': n_neg,
        'min_eval': min_eval,
        'n_interior': n_int,
        'mu_L': float(mu_L),
        'lagrange_residual': float(residual),
    }


def tessellation_stability_margin(vertices, interior_mask, Delta, cutoff=None):
    """The minimum non-trivial constrained eigenvalue.

    Skips eigenvalues near zero (rotation modes).
    """
    result = tessellation_constrained_eigenvalues(
        vertices, interior_mask, Delta, cutoff)
    evals = result['constrained_evals']
    if len(evals) == 0:
        return 0.0

    negative = evals[evals < -1e-4]
    if len(negative) > 0:
        return float(negative[0])
    positive = evals[evals > 1e-4]
    if len(positive) > 0:
        return float(positive[0])
    return 0.0


# ============================================================
# Main comparison
# ============================================================

def tessellation_stability_table(Delta_values=None):
    """Compare stability across tessellation types and Δ values."""
    if Delta_values is None:
        Delta_values = [0, 0.5, 1.0, 2.0, 5.0]

    results = {}
    configs = [
        ('triangle_{3,6}', lambda: triangle_tessellation(n_rings=2)),
        ('square_{4,4}', lambda: square_tessellation(n_side=3)),
        ('hexagon_{6,3}', lambda: hexagon_tessellation(n_rings=1)),
    ]

    for name, builder in configs:
        vertices, faces, interior_mask = builder()
        n_int = np.sum(interior_mask)
        results[name] = {'n_vertices': len(vertices), 'n_interior': n_int,
                         'n_faces': len(faces), 'margins': {}}

        for Delta in Delta_values:
            margin = tessellation_stability_margin(
                vertices, interior_mask, Delta)
            results[name]['margins'][Delta] = margin

    return results


if __name__ == '__main__':
    print("=" * 60)
    print("Tessellation stability comparison")
    print("=" * 60)

    results = tessellation_stability_table()
    for name, data in results.items():
        print(f"\n{name}: {data['n_vertices']} vertices, "
              f"{data['n_interior']} interior, {data['n_faces']} faces")
        for Delta, margin in data['margins'].items():
            status = "STABLE" if margin >= -1e-4 else "UNSTABLE"
            print(f"  Δ={Delta:5.1f}: margin = {margin:+.6f}  {status}")
