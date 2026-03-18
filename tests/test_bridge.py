# tests/test_bridge.py
from planetary_polygons.extensions.bridge import blob_convergence_rate


def test_blob_convergence_quadratic():
    result = blob_convergence_rate(N=6, eps_values=[0.1, 0.05, 0.025, 0.01])
    alpha = result['convergence_exponent']
    assert 1.5 < alpha < 2.5, f"Expected O(ε²), got exponent={alpha:.2f}"
