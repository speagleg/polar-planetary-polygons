# tests/test_bec_vortices.py
from planetary_polygons.extensions.bec_vortices import bec_kappa_crit, bec_stability_table


def test_n8_bec_kappa_crit():
    kc = bec_kappa_crit(8)
    assert kc < 1.0


def test_stability_table_n6():
    table = bec_stability_table(range(5, 10))
    assert abs(table[6]['kappa_crit'] + 0.25) < 0.01


def test_stability_table_q0_min_n8():
    table = bec_stability_table(range(5, 10))
    assert table[8]['q0_min'] == 1
