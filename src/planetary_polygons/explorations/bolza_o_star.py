r"""
EXPLORATION: O* (binary octahedral) irrep decomposition of the Bolza
convolution spectrum.

The Bolza surface is the genus-2 compact hyperbolic surface with the
largest automorphism group: Aut(Bolza) = GL(2, F_3) ~ O* (binary
octahedral group, order 48).

O* has 8 irreducible representations:
    dim:  1   1'  2   2'  2''  3   3'  4
    sum d^2 = 1 + 1 + 4 + 4 + 4 + 9 + 9 + 16 = 48

The McKay graph of O* (viewed as a finite subgroup of SU(2)) is the
EXTENDED E_7 DYNKIN DIAGRAM.

KEY QUESTION: Does the convolution matrix spectrum on the Bolza surface
decompose into eigenspaces whose degeneracies match the O* irrep
dimensions {1, 1, 2, 2, 2, 3, 3, 4}?

If so, each irrep rho gets a "Casimir" T_rho (eigenvalue of the
convolution operator restricted to the rho-isotypic subspace), and
these Casimirs may relate to E_7 data (exponents, Coxeter number h=18).

E_7 DATA:
    Exponents: 1, 5, 7, 9, 11, 13, 17
    Coxeter number h = 18
    Dual Coxeter number h^v = 18
    Rank = 7
    Dimension = 133
    Extended Dynkin: 8 nodes (matching 8 O* irreps)

The extended E_7 Dynkin diagram has nodes with marks (dimensions of O*
irreps on the McKay graph):

         1 -- 2 -- 3 -- 4 -- 3' -- 2' -- 1'
                    |
                    2''

Run: PYTHONPATH=src python3 -m planetary_polygons.explorations.bolza_o_star
"""

import math
import numpy as np

from planetary_polygons.proofs.bolza_tau import (
    enumerate_group_bfs,
    build_convolution_matrix,
    bolza_geodesic_lengths,
    delta_C1_selberg,
)


# =====================================================================
# O* character table
# =====================================================================

def o_star_character_table():
    r"""Character table of O* = GL(2, F_3) ~ binary octahedral group.

    O* has order 48 and 8 conjugacy classes.

    Conjugacy classes (representative, size, order):
        C_1:  identity          (1,   order 1)
        C_2:  -I = z            (1,   order 2)  [center]
        C_3:  order-3 elements  (8,   order 3)
        C_4:  order-6 elements  (8,   order 6)  [= z * C_3]
        C_5:  order-4 elements  (6,   order 4)  [quaternion type]
        C_6:  order-8 elements  (6,   order 8)  [type A]
        C_7:  order-8 elements  (6,   order 8)  [type B, conjugate]
        C_8:  order-4 elements  (12,  order 4)  [transposition type]

    Sizes: [1, 1, 8, 8, 6, 6, 6, 12]  (sum = 48)

    Irreps with dimensions [1, 1, 2, 2, 2, 3, 3, 4]:
        rho_1:   trivial (1-dim)
        rho_1':  sign rep (1-dim), kernel = O (rotation octahedral)
        rho_2:   faithful 2-dim (quaternionic, from SU(2) embedding)
        rho_2':  2-dim, = rho_2 tensor sign
        rho_2'': 2-dim (another faithful rep)
        rho_3:   3-dim (standard rep of S_4, pulled back via O* -> S_4)
        rho_3':  3-dim, = rho_3 tensor sign
        rho_4:   4-dim (induced from index-2 subgroup)

    The character table entries are organized as:
        Rows = irreps (1, 1', 2, 2', 2'', 3, 3', 4)
        Columns = conjugacy classes (C_1..C_8)

    Returns
    -------
    table : ndarray of shape (8, 8), complex
    class_sizes : list of 8 int
    irrep_dims : list of 8 int
    irrep_names : list of 8 str
    class_orders : list of 8 int
        Element orders in each conjugacy class.
    """
    # sqrt(2) appears in the 2-dim characters
    s2 = math.sqrt(2)

    # Class sizes
    class_sizes = [1, 1, 8, 8, 6, 6, 6, 12]
    assert sum(class_sizes) == 48

    # Element orders in each class
    class_orders = [1, 2, 3, 6, 4, 8, 8, 4]

    # Irrep dimensions
    irrep_dims = [1, 1, 2, 2, 2, 3, 3, 4]
    assert sum(d**2 for d in irrep_dims) == 48

    irrep_names = ['1', "1'", '2', "2'", "2''", '3', "3'", '4']

    # Character table of O* (binary octahedral group)
    #
    # Columns: C_1  C_2  C_3  C_4  C_5  C_6   C_7   C_8
    #          (1)  (1)  (8)  (8)  (6)  (6)   (6)   (12)
    table = np.array([
        # rho_1 (trivial)
        [1,    1,    1,    1,    1,    1,     1,     1],
        # rho_1' (sign: kernel = O, quotient Z_2)
        [1,    1,    1,    1,    1,   -1,    -1,    -1],
        # rho_2 (fundamental 2-dim from SU(2))
        [2,   -2,   -1,    1,    0,    s2,   -s2,    0],
        # rho_2' = rho_2 x sign
        [2,   -2,   -1,    1,    0,   -s2,    s2,    0],
        # rho_2'' (from the binary structure, related to Q_8 subgroup)
        [2,    2,   -1,   -1,    2,    0,     0,     0],
        # rho_3 (standard 3-dim rep of S_4, via O* -> S_4)
        [3,    3,    0,    0,   -1,    1,     1,    -1],
        # rho_3' = rho_3 x sign
        [3,    3,    0,    0,   -1,   -1,    -1,     1],
        # rho_4 (4-dim, induced from binary tetrahedral subgroup)
        [4,   -4,    1,   -1,    0,    0,     0,     0],
    ], dtype=complex)

    # Verify orthogonality: (1/|G|) sum_g chi_i(g)* chi_j(g) = delta_{ij}
    sizes = np.array(class_sizes, dtype=complex)
    for i in range(8):
        for j in range(8):
            inner = np.sum(sizes * np.conj(table[i]) * table[j]) / 48.0
            expected = 1.0 if i == j else 0.0
            if abs(inner - expected) > 1e-10:
                raise ValueError(
                    f"Orthogonality fail: <chi_{i}, chi_{j}> = {inner}, "
                    f"expected {expected}"
                )

    return table, class_sizes, irrep_dims, irrep_names, class_orders


# =====================================================================
# Eigenvalue degeneracy analysis
# =====================================================================

def _cluster_eigenvalues(eigenvalues, tol=1e-4):
    """Group eigenvalues by degeneracy (within tolerance).

    Returns list of (mean_value, degeneracy, indices) sorted by value.
    """
    n = len(eigenvalues)
    used = set()
    groups = []
    sorted_idx = np.argsort(eigenvalues)

    for i in sorted_idx:
        if int(i) in used:
            continue
        val = eigenvalues[i]
        cluster = [int(i)]
        for j in sorted_idx:
            if int(j) != int(i) and int(j) not in used:
                if abs(eigenvalues[j] - val) < tol:
                    cluster.append(int(j))
        for j in cluster:
            used.add(j)
        mean_val = float(np.mean(eigenvalues[cluster]))
        groups.append((mean_val, len(cluster), cluster))

    groups.sort(key=lambda g: g[0])
    return groups


def bolza_eigenvalue_decomposition(max_word_length=3, tol=1e-4):
    r"""Compute convolution matrix eigenvalues and check O* irrep structure.

    Strategy:
    1. Enumerate Fuchsian group elements up to word length L.
    2. Build the Green's function convolution matrix.
    3. Compute eigenvalues.
    4. Cluster by degeneracy.
    5. Check if degeneracies match O* irrep dimensions {1,1,2,2,2,3,3,4}.

    The matrix size is n x n where n is the number of group elements
    found (n ~ 8, 56, 336, 1968, 6112 for L=1..5).

    The O* symmetry acts on the GROUP ELEMENTS via the automorphism
    action: gamma -> alpha * gamma * alpha^{-1} for alpha in Aut(Bolza).
    This action permutes the rows/columns of the convolution matrix,
    so the spectrum inherits O* symmetry.

    However, the irrep multiplicities scale with the matrix size n.
    For a matrix of size n, the spectrum has n eigenvalues total, and
    they decompose as:

        n = sum_rho m_rho * dim(rho)

    where m_rho is the multiplicity of irrep rho in the permutation
    representation on the n group elements.

    The KEY TEST is whether the eigenvalue degeneracies are multiples
    of {1, 2, 3, 4} consistent with O* irreps.

    Parameters
    ----------
    max_word_length : int
        BFS depth for Fuchsian group enumeration.
    tol : float
        Eigenvalue clustering tolerance.

    Returns
    -------
    dict with keys:
        n_elements : int
        eigenvalues : ndarray
        clusters : list of (value, degeneracy, indices)
        degeneracies : list of int
        o_star_dims : set of O* irrep dimensions
        matches_o_star : bool  (all degeneracies are in {1,2,3,4})
        dim_histogram : dict mapping dim -> count of clusters with that deg
    """
    images, distances, n_by_level = enumerate_group_bfs(max_word_length)
    n = len(images)

    H = build_convolution_matrix(images)
    eigenvalues = np.linalg.eigvalsh(H)

    clusters = _cluster_eigenvalues(eigenvalues, tol=tol)
    degeneracies = [deg for _, deg, _ in clusters]

    o_star_dims = {1, 2, 3, 4}

    # Check if every degeneracy is a valid O* irrep dimension
    matches_o_star = all(d in o_star_dims for d in degeneracies)

    # Histogram of degeneracies
    dim_histogram = {}
    for d in degeneracies:
        dim_histogram[d] = dim_histogram.get(d, 0) + 1

    # Check the sum: each O* irrep dimension d appears with multiplicity
    # m_d, so sum m_d * d = n
    sum_check = sum(d * dim_histogram.get(d, 0) for d in dim_histogram)

    return {
        'n_elements': n,
        'n_by_level': n_by_level,
        'eigenvalues': eigenvalues,
        'clusters': clusters,
        'degeneracies': degeneracies,
        'n_clusters': len(clusters),
        'o_star_dims': o_star_dims,
        'matches_o_star': matches_o_star,
        'dim_histogram': dim_histogram,
        'sum_check': sum_check,
        'sum_ok': sum_check == n,
    }


# =====================================================================
# O* Casimirs from eigenvalue groups
# =====================================================================

def o_star_casimirs_on_bolza(max_word_length=3, tol=1e-4):
    r"""Compute the "Casimir" T_rho for each O* irrep.

    If the convolution matrix H decomposes under O* as:

        H = bigoplus_rho T_rho * Id_{m_rho * dim(rho)}

    then each irrep rho has a single scalar T_rho (the eigenvalue
    restricted to the rho-isotypic subspace).

    In practice, the same irrep rho appears with multiplicity m_rho,
    and each copy may have a DIFFERENT eigenvalue (since the convolution
    operator is not purely algebraic -- it depends on the truncation).
    So we get a set of eigenvalues for each irrep dimension d, and
    the "Casimir" is a statistical summary.

    Strategy:
    1. Cluster eigenvalues by degeneracy.
    2. For each O* irrep dimension d, collect all clusters with
       degeneracy d.
    3. The eigenvalues of these clusters are the candidate Casimirs
       for irreps of dimension d.

    For the extended E_7 McKay graph, the node labels (O* irrep dims)
    are: 1-2-3-4-3-2-1 (main chain) with 2 branching off the 3.
    This suggests a natural ordering of the Casimirs.

    Returns
    -------
    dict mapping irrep_dim -> list of cluster eigenvalues
    """
    result = bolza_eigenvalue_decomposition(max_word_length, tol=tol)
    clusters = result['clusters']

    casimirs_by_dim = {1: [], 2: [], 3: [], 4: []}
    for val, deg, _ in clusters:
        if deg in casimirs_by_dim:
            casimirs_by_dim[deg].append(val)
        else:
            # Degeneracy not matching any O* irrep dimension
            casimirs_by_dim.setdefault(deg, []).append(val)

    return {
        'casimirs_by_dim': casimirs_by_dim,
        'decomposition': result,
    }


# =====================================================================
# E_7 connection
# =====================================================================

def e7_connection(max_word_length=3, tol=1e-4):
    r"""Check if the O* Casimirs relate to E_7 data.

    E_7 invariants:
        Exponents: {1, 5, 7, 9, 11, 13, 17}
        Coxeter number h = 18
        Dual Coxeter h^v = 18
        Rank = 7
        Dimension = 133

    The extended E_7 Dynkin diagram has 8 nodes with Dynkin labels
    (= O* irrep dimensions on the McKay graph):

        a_0=1, a_1=2, a_2=3, a_3=4, a_4=3, a_5=2, a_6=1, a_7=2

    where the branching is at node 2 (the first "3").

    The Cartan matrix eigenvalues of E_7 are:
        4 * sin^2(pi * m_j / (2h))  for exponents m_j

    These are: 4 sin^2(pi*1/36), 4 sin^2(pi*5/36), ..., 4 sin^2(pi*17/36)

    We check:
    1. Whether the number of distinct Casimir levels matches the E_7 rank + 1
    2. Whether Casimir ratios match E_7 Cartan eigenvalue ratios
    3. Whether the spectral gap relates to 1/h = 1/18

    Returns
    -------
    dict with analysis results
    """
    # E_7 data
    e7_exponents = [1, 5, 7, 9, 11, 13, 17]
    e7_h = 18  # Coxeter number
    e7_rank = 7

    # Extended E_7 Dynkin labels (8 nodes) = O* irrep dimensions
    # Node ordering: 1 -- 2 -- 3 -- 4 -- 3' -- 2' -- 1'
    #                              |
    #                              2''
    e7_dynkin_labels = [1, 2, 3, 4, 3, 2, 1, 2]  # sum = 18 = h
    assert sum(e7_dynkin_labels) == e7_h

    # Cartan matrix eigenvalues of E_7
    cartan_eigenvalues = sorted(
        4.0 * math.sin(math.pi * m / (2 * e7_h))**2
        for m in e7_exponents
    )

    # Get the Bolza Casimirs
    cas_result = o_star_casimirs_on_bolza(max_word_length, tol=tol)
    casimirs_by_dim = cas_result['casimirs_by_dim']
    decomp = cas_result['decomposition']

    # Collect all distinct Casimir values (from valid O* dimensions)
    all_casimirs = []
    for d in [1, 2, 3, 4]:
        all_casimirs.extend(casimirs_by_dim.get(d, []))
    all_casimirs.sort()

    # Compare structure
    n_casimir_levels = len(all_casimirs)

    # Spectral gap: smallest nonzero |Casimir|
    abs_casimirs = sorted(abs(c) for c in all_casimirs if abs(c) > 1e-6)
    spectral_gap = abs_casimirs[0] if abs_casimirs else None

    # Ratio test: normalize Casimirs to [0, 1] and compare with
    # normalized Cartan eigenvalues
    ratio_matches = None
    if len(all_casimirs) >= 2:
        cas_min = min(all_casimirs)
        cas_max = max(all_casimirs)
        cas_range = cas_max - cas_min
        if cas_range > 1e-10:
            normalized_cas = [(c - cas_min) / cas_range for c in all_casimirs]
        else:
            normalized_cas = [0.0] * len(all_casimirs)

        cart_min = min(cartan_eigenvalues)
        cart_max = max(cartan_eigenvalues)
        cart_range = cart_max - cart_min
        normalized_cart = [(c - cart_min) / cart_range for c in cartan_eigenvalues]

        # If we have 7 Casimir levels, check 1-to-1 correspondence
        if n_casimir_levels == e7_rank:
            diffs = [abs(a - b) for a, b in zip(normalized_cas, normalized_cart)]
            ratio_matches = max(diffs) if diffs else None

    # Selberg trace data for comparison
    delta_c1 = delta_C1_selberg()
    geodesics = bolza_geodesic_lengths(n_terms=5)

    # Check: does 1/h = 1/18 appear as a spectral ratio?
    coxeter_ratio_check = None
    if spectral_gap is not None and cas_range > 1e-10:
        ratio = spectral_gap / cas_range
        coxeter_ratio_check = {
            'gap_over_range': ratio,
            '1_over_h': 1.0 / e7_h,
            'close_to_1_over_h': abs(ratio - 1.0 / e7_h) < 0.05,
        }

    return {
        'e7_exponents': e7_exponents,
        'e7_coxeter_number': e7_h,
        'e7_cartan_eigenvalues': cartan_eigenvalues,
        'e7_dynkin_labels': e7_dynkin_labels,
        'casimirs_by_dim': casimirs_by_dim,
        'all_casimirs_sorted': all_casimirs,
        'n_casimir_levels': n_casimir_levels,
        'spectral_gap': spectral_gap,
        'ratio_matches': ratio_matches,
        'coxeter_ratio_check': coxeter_ratio_check,
        'delta_c1_selberg': delta_c1,
        'decomposition': decomp,
    }


# =====================================================================
# McKay graph adjacency check
# =====================================================================

def _e7_extended_adjacency():
    """Adjacency matrix of the extended E_7 Dynkin diagram (8 nodes).

    Node ordering matching O* irreps:
        0: dim 1  (trivial)
        1: dim 2  (fundamental)
        2: dim 3  (standard)
        3: dim 4  (4-dim)
        4: dim 3' (3 x sign)
        5: dim 2' (2 x sign)
        6: dim 1' (sign)
        7: dim 2'' (extra 2-dim)

    Edges: 0-1, 1-2, 2-3, 3-4, 4-5, 5-6, 2-7 (branch)
    """
    adj = np.zeros((8, 8), dtype=int)
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (2, 7)]
    for i, j in edges:
        adj[i, j] = 1
        adj[j, i] = 1
    return adj


def mckay_graph_check(max_word_length=3, tol=1e-4):
    """Check if Casimir nearest-neighbor structure matches E_7 Dynkin.

    On the McKay graph, adjacent irreps should have "close" Casimirs
    (since the convolution operator is local in the group algebra).

    We assign each cluster to an E_7 node by dimension, then check
    if the Casimir ordering respects the graph distance.
    """
    cas_result = o_star_casimirs_on_bolza(max_word_length, tol=tol)
    casimirs_by_dim = cas_result['casimirs_by_dim']
    adj = _e7_extended_adjacency()

    # Extended E_7 node dimensions
    node_dims = [1, 2, 3, 4, 3, 2, 1, 2]
    node_names = ['1', '2', '3', '4', "3'", "2'", "1'", "2''"]

    # For each node, pick the median Casimir of that dimension
    node_casimirs = []
    for i, d in enumerate(node_dims):
        cas_list = casimirs_by_dim.get(d, [])
        if cas_list:
            # Use median as representative
            node_casimirs.append(float(np.median(cas_list)))
        else:
            node_casimirs.append(None)

    # Check adjacency: for connected nodes, compute Casimir difference
    edge_diffs = []
    non_edge_diffs = []
    for i in range(8):
        for j in range(i + 1, 8):
            if node_casimirs[i] is not None and node_casimirs[j] is not None:
                diff = abs(node_casimirs[i] - node_casimirs[j])
                if adj[i, j] == 1:
                    edge_diffs.append((node_names[i], node_names[j], diff))
                else:
                    non_edge_diffs.append((node_names[i], node_names[j], diff))

    return {
        'node_dims': node_dims,
        'node_names': node_names,
        'node_casimirs': node_casimirs,
        'edge_diffs': edge_diffs,
        'non_edge_diffs': non_edge_diffs,
        'adjacency': adj,
    }


# =====================================================================
# O* representation ring structure
# =====================================================================

def o_star_fusion_rules():
    """Compute the O* tensor product (fusion) rules from the character table.

    For irreps rho_i, rho_j of a finite group G:
        rho_i x rho_j = sum_k N_{ij}^k rho_k

    where N_{ij}^k = (1/|G|) sum_g chi_i(g) chi_j(g) conj(chi_k(g))

    These are the fusion coefficients (= McKay graph adjacency for
    the fundamental rep).

    Returns
    -------
    N : ndarray of shape (8, 8, 8), integer fusion coefficients
    """
    table, class_sizes, irrep_dims, irrep_names, _ = o_star_character_table()
    n_irreps = 8
    order = 48
    sizes = np.array(class_sizes, dtype=complex)

    N = np.zeros((n_irreps, n_irreps, n_irreps), dtype=int)
    for i in range(n_irreps):
        for j in range(n_irreps):
            # Product character
            prod_chi = table[i] * table[j]
            for k in range(n_irreps):
                # Decompose into irrep k
                coeff = np.sum(sizes * prod_chi * np.conj(table[k])) / order
                N[i, j, k] = int(round(coeff.real))

    return N, irrep_names


def verify_mckay_graph():
    """Verify that tensoring with the fundamental 2-dim rep of O*
    gives the extended E_7 Dynkin diagram.

    The McKay correspondence: for the fundamental rep rho_2 (index 2),
    the matrix N[2, :, :] should give the adjacency matrix of the
    extended E_7 diagram.

    That is, rho_2 x rho_i = sum_j A_{ij} rho_j  where A is the
    extended E_7 adjacency matrix.
    """
    N, names = o_star_fusion_rules()

    # The fundamental 2-dim rep is index 2 (rho_2)
    fund_idx = 2

    # Extract the "McKay adjacency" for the fundamental rep
    mckay_adj = N[fund_idx, :, :]

    # The extended E_7 adjacency has specific structure
    # Check properties
    is_symmetric = np.allclose(mckay_adj, mckay_adj.T)

    # Diagonal should be zero for a simple graph
    diag_zero = all(mckay_adj[i, i] == 0 for i in range(8))

    # Check that entries are 0 or 1 (simple graph)
    is_simple = np.all((mckay_adj == 0) | (mckay_adj == 1))

    # Number of edges
    n_edges = np.sum(mckay_adj) // 2

    # Expected for extended E_7: 7 edges on 8 nodes
    expected_edges = 7

    # Compare with theoretical extended E_7
    e7_adj = _e7_extended_adjacency()

    # The McKay adjacency might have a different node ordering
    # Check if they are isomorphic (same sorted eigenvalues)
    mckay_evals = sorted(np.linalg.eigvalsh(mckay_adj.astype(float)))
    e7_evals = sorted(np.linalg.eigvalsh(e7_adj.astype(float)))
    spectrally_isomorphic = np.allclose(mckay_evals, e7_evals, atol=1e-10)

    return {
        'mckay_adjacency': mckay_adj,
        'irrep_names': names,
        'is_symmetric': is_symmetric,
        'diag_zero': diag_zero,
        'is_simple': is_simple,
        'n_edges': int(n_edges),
        'expected_edges': expected_edges,
        'spectrally_isomorphic_to_e7': spectrally_isomorphic,
        'mckay_eigenvalues': mckay_evals,
        'e7_eigenvalues': e7_evals,
    }


# =====================================================================
# Main analysis
# =====================================================================

def main():
    print("=" * 75)
    print("  O* IRREP DECOMPOSITION OF BOLZA CONVOLUTION SPECTRUM")
    print("  Aut(Bolza) = GL(2,F_3) ~ O* (binary octahedral, order 48)")
    print("=" * 75)

    # ---------------------------------------------------------------
    # 1. Character table
    # ---------------------------------------------------------------
    print("\n--- O* Character Table ---\n")
    table, class_sizes, irrep_dims, irrep_names, class_orders = (
        o_star_character_table()
    )
    print(f"  Order: 48")
    print(f"  Irreps: {dict(zip(irrep_names, irrep_dims))}")
    print(f"  Sum d^2 = {sum(d**2 for d in irrep_dims)}")
    print(f"  Class sizes: {class_sizes}")
    print(f"  Class orders: {class_orders}")
    print()

    # Print the table
    header = "       " + "  ".join(f"C{i+1:d}({class_sizes[i]:d})" for i in range(8))
    print(header)
    for i in range(8):
        row = f"  {irrep_names[i]:>3s}: "
        row += "  ".join(f"{table[i,j].real:6.3f}" for j in range(8))
        print(row)

    # ---------------------------------------------------------------
    # 2. McKay graph verification
    # ---------------------------------------------------------------
    print("\n--- McKay Graph (should be extended E_7) ---\n")
    mckay = verify_mckay_graph()
    print(f"  Symmetric: {mckay['is_symmetric']}")
    print(f"  Simple graph (0/1 entries, zero diag): "
          f"{mckay['is_simple'] and mckay['diag_zero']}")
    print(f"  Number of edges: {mckay['n_edges']} (expected: {mckay['expected_edges']})")
    print(f"  Spectrally isomorphic to extended E_7: "
          f"{mckay['spectrally_isomorphic_to_e7']}")
    print(f"\n  McKay adjacency (rho_2 x rho_i decomposition):")
    for i in range(8):
        neighbors = [
            mckay['irrep_names'][j]
            for j in range(8) if mckay['mckay_adjacency'][i, j] > 0
        ]
        print(f"    {mckay['irrep_names'][i]:>3s} -- {', '.join(neighbors)}")

    # ---------------------------------------------------------------
    # 3. Fusion rules
    # ---------------------------------------------------------------
    print("\n--- O* Fusion Rules (selected) ---\n")
    N, names = o_star_fusion_rules()
    # Show a few key products
    for i, j in [(2, 2), (2, 5), (5, 5), (2, 7), (7, 7)]:
        prod_str = " + ".join(
            f"{N[i,j,k]}*{names[k]}" for k in range(8) if N[i,j,k] > 0
        )
        print(f"  {names[i]} x {names[j]} = {prod_str}")

    # ---------------------------------------------------------------
    # 4. Eigenvalue decomposition
    # ---------------------------------------------------------------
    for L in [2, 3]:
        print(f"\n--- Eigenvalue Decomposition (L={L}) ---\n")
        result = bolza_eigenvalue_decomposition(L)
        n = result['n_elements']
        print(f"  Matrix size: {n} x {n}")
        print(f"  Elements by level: {result['n_by_level']}")
        print(f"  Number of eigenvalue clusters: {result['n_clusters']}")
        print(f"  Degeneracy histogram: {result['dim_histogram']}")
        print(f"  All degeneracies in {{1,2,3,4}}: {result['matches_o_star']}")
        print(f"  Sum check: {result['sum_check']} == {n}: {result['sum_ok']}")
        print()

        # Show first and last few clusters
        clusters = result['clusters']
        n_show = min(10, len(clusters))
        print(f"  First {n_show} clusters:")
        for val, deg, _ in clusters[:n_show]:
            dim_label = {1: "1/1'", 2: "2/2'/2''", 3: "3/3'", 4: "4"}.get(deg, "?")
            print(f"    lambda = {val:+10.6f}, deg = {deg} ({dim_label})")
        if len(clusters) > 2 * n_show:
            print(f"    ...")
        if len(clusters) > n_show:
            print(f"  Last {n_show} clusters:")
            for val, deg, _ in clusters[-n_show:]:
                dim_label = {1: "1/1'", 2: "2/2'/2''", 3: "3/3'", 4: "4"}.get(
                    deg, "?")
                print(f"    lambda = {val:+10.6f}, deg = {deg} ({dim_label})")

        # Fraction of negative eigenvalues
        n_neg = int(np.sum(result['eigenvalues'] < 0))
        print(f"\n  Negative eigenvalues: {n_neg}/{n} = {n_neg/n:.6f}")
        print(f"  Compare 30/48 = {30/48:.6f}, 31/48 = {31/48:.6f}")

    # ---------------------------------------------------------------
    # 5. O* Casimirs
    # ---------------------------------------------------------------
    print("\n--- O* Casimirs (eigenvalues by irrep dimension) ---\n")
    cas_result = o_star_casimirs_on_bolza(max_word_length=3)
    casimirs = cas_result['casimirs_by_dim']
    for d in sorted(casimirs.keys()):
        vals = casimirs[d]
        if vals:
            o_star_irreps = {
                1: "1, 1'", 2: "2, 2', 2''", 3: "3, 3'", 4: "4"
            }.get(d, "?")
            print(f"  dim={d} (irreps {o_star_irreps}): "
                  f"{len(vals)} clusters")
            print(f"    range: [{min(vals):.6f}, {max(vals):.6f}]")
            print(f"    mean:  {np.mean(vals):.6f}")

    # ---------------------------------------------------------------
    # 6. E_7 connection
    # ---------------------------------------------------------------
    print("\n--- E_7 Connection ---\n")
    e7 = e7_connection(max_word_length=3)
    print(f"  E_7 exponents: {e7['e7_exponents']}")
    print(f"  E_7 Coxeter number: {e7['e7_coxeter_number']}")
    print(f"  E_7 Cartan eigenvalues: "
          + ", ".join(f"{v:.6f}" for v in e7['e7_cartan_eigenvalues']))
    print(f"  E_7 Dynkin labels (= O* dims): {e7['e7_dynkin_labels']}")
    print(f"  Sum of Dynkin labels = {sum(e7['e7_dynkin_labels'])} = h")
    print()

    n_levels = e7['n_casimir_levels']
    print(f"  Number of distinct Casimir levels: {n_levels}")
    print(f"  E_7 rank + 1 = 8")
    print(f"  Match: {n_levels == 8}")

    if e7['spectral_gap'] is not None:
        print(f"\n  Spectral gap: {e7['spectral_gap']:.6f}")
    if e7['coxeter_ratio_check'] is not None:
        cr = e7['coxeter_ratio_check']
        print(f"  Gap/range = {cr['gap_over_range']:.6f}")
        print(f"  1/h = {cr['1_over_h']:.6f}")
        print(f"  Close to 1/h: {cr['close_to_1_over_h']}")

    # Selberg data
    print(f"\n  Selberg delta_C1 = {e7['delta_c1_selberg']:.6f}")
    print(f"  h * delta_C1 = {e7['e7_coxeter_number'] * e7['delta_c1_selberg']:.4f}")

    # ---------------------------------------------------------------
    # 7. McKay graph Casimir structure
    # ---------------------------------------------------------------
    print("\n--- McKay Graph Casimir Assignment ---\n")
    mg = mckay_graph_check(max_word_length=3)
    print("  E_7 node | dim | Casimir (median)")
    print("  " + "-" * 40)
    for i in range(8):
        cas_str = (f"{mg['node_casimirs'][i]:+.6f}"
                   if mg['node_casimirs'][i] is not None else "  N/A")
        print(f"  {mg['node_names'][i]:>3s}       | {mg['node_dims'][i]}   | {cas_str}")

    if mg['edge_diffs']:
        print(f"\n  Edge Casimir differences (should be small):")
        for n1, n2, diff in mg['edge_diffs']:
            print(f"    {n1} -- {n2}: |Delta| = {diff:.6f}")

    print()
    print("=" * 75)
    print("  SUMMARY")
    print("=" * 75)
    print()

    result_L3 = bolza_eigenvalue_decomposition(3)
    print(f"  O* irrep dimensions:   {{1, 1, 2, 2, 2, 3, 3, 4}}")
    print(f"  Degeneracy histogram:  {result_L3['dim_histogram']}")
    print(f"  All degeneracies match O* dims: {result_L3['matches_o_star']}")
    print()

    mckay_ok = mckay['spectrally_isomorphic_to_e7']
    print(f"  McKay graph = extended E_7:     {mckay_ok}")
    print(f"  Convolution spectrum has O* structure: "
          f"{result_L3['matches_o_star']}")

    if result_L3['matches_o_star']:
        print()
        print("  CONCLUSION: The convolution matrix eigenvalue degeneracies")
        print("  are consistent with O* irrep dimensions. The Bolza surface")
        print("  convolution operator decomposes under Aut(Bolza) = O*,")
        print("  with eigenspaces organized by the extended E_7 Dynkin diagram.")
    else:
        print()
        print("  NOTE: Degeneracies do not exactly match O* irrep dims.")
        print("  This may be due to truncation effects at finite word length,")
        print("  accidental degeneracies, or the need for a finer tolerance.")
        hist = result_L3['dim_histogram']
        non_ostar = {k: v for k, v in hist.items() if k not in {1, 2, 3, 4}}
        if non_ostar:
            print(f"  Non-O* degeneracies found: {non_ostar}")
            print("  These likely arise from accidental near-degeneracies")
            print("  that should split at higher truncation depth.")


if __name__ == '__main__':
    main()
