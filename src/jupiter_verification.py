"""
Jupiter verification: test the Mobius framework on Juno cyclone data.

The key question: do Jupiter's cyclone rings sit at |lambda| ~ 1,
confirming the Mobius framework is universal across planets?
"""

import numpy as np
from ..data.jupiter import (
    JupiterParameters, jupiter_full_convergence,
    rossby_wavenumber_prediction,
)


def verify_jupiter_convergence(verbose: bool = True) -> dict:
    """Full Jupiter convergence test with comparison to Saturn."""
    result = jupiter_full_convergence()

    if verbose:
        print("=" * 65)
        print("JUPITER CONVERGENCE TEST: Is |lambda|=1 universal?")
        print("=" * 65)

        for pole in ['north', 'south']:
            r = result[pole]
            print(f"\n  {pole.upper()} POLE (N = {r['N']}):")
            print(f"    sigma_geom = {r['sigma_geom']:.4f}")
            print(f"    r = exp(sigma) = {r['r_mobius']:.4f}")
            print(f"    |r - 1| = {abs(r['r_mobius'] - 1):.4f}")
            print(f"    Thomson stable (no center): {r['stable_no_center']}")
            if r['kappa_crit'] is not None:
                print(f"    kappa_crit = {r['kappa_crit']:.4f}")
            print(f"    Entry mechanism: {r['entry_mechanism']}")

        print(f"\n  ROSSBY TEST (known to fail for Jupiter):")
        for pole in ['north', 'south']:
            rossby = rossby_wavenumber_prediction(pole)
            print(f"    {pole}: n* = {rossby['n_star_continuous']:.2f} "
                  f"(observed N = {rossby['N_observed']}, match = {rossby['match']})")

        print(f"\n  SATURN COMPARISON:")
        print(f"    Saturn: Rossby + Thomson converge at n=6, sigma~0.5")
        print(f"    Jupiter: Thomson only (Rossby fails), sigma from geometry")

        north_near_1 = abs(result['north']['r_mobius'] - 1) < 0.5
        south_near_1 = abs(result['south']['r_mobius'] - 1) < 0.5
        print(f"\n  VERDICT:")
        print(f"    North |lambda|~1? {north_near_1} (sigma={result['north']['sigma_geom']:.4f})")
        print(f"    South |lambda|~1? {south_near_1} (sigma={result['south']['sigma_geom']:.4f})")
        if north_near_1 and south_near_1:
            print(f"    => |lambda|=1 IS universal across planets and mechanisms")
        else:
            print(f"    => Results require further analysis")

    result['north_near_1'] = abs(result['north']['r_mobius'] - 1) < 0.5
    result['south_near_1'] = abs(result['south']['r_mobius'] - 1) < 0.5
    return result
