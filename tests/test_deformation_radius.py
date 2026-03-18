# tests/test_deformation_radius.py
from planetary_polygons.extensions.deformation_radius import (
    K0_eigenvalue, suppression_transition
)


def test_K0_small_ratio_positive():
    """At small R/Rd, N=6 should be stable (positive eigenvalue)."""
    e = K0_eigenvalue(N=6, m=1, R_over_Rd=0.01)
    assert e > 0, f"Small R/Rd should be stable for N=6, got {e}"


def test_suppression_transition_n6_reasonable():
    R_Rd = suppression_transition(N=6)
    assert 0.3 < R_Rd < 5.0, f"Expected transition in (0.3, 5.0), got {R_Rd}"
