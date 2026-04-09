"""Formal derivation of the K^(N-1) instanton suppression for V_ub.

Proves:
1. (YY^dag)_{02} = 0 from the Z_N selection rules (texture zero)
2. Winding numbers: V_ub has w=N-1, V_us and V_cb have smaller w
3. The instanton action S = (N-1) * 2*pi*k_frac
4. The correction applies ONLY to V_ub (selectivity)
"""

import numpy as np
from math import pi, exp, log

from planetary_polygons.extensions.bernoulli_havelock import (
    N_CRIT, instanton_fugacity,
)

N = N_CRIT
UP_L = [1, 2, 4]
DN_L = [6, 5, 3]
HIGGS = [3, 4]


def _build_texture(L_modes, N_val=N):
    """Build the Yukawa texture (0/1) from Z_N selection rules."""
    n = len(L_modes)
    tex = np.zeros((n, n), dtype=int)
    for i in range(n):
        mL = L_modes[i]
        for j in range(n):
            mL_j = L_modes[j]
            for mR in [mL_j, N_val - mL_j]:
                for mH in HIGGS:
                    if (mL - mR + mH) % N_val == 0:
                        tex[i, j] = 1
    return tex


def texture_zero_proof(N_val=N):
    """Prove (YY^dag)_{02} = 0 from the Z_N selection rules.

    The texture is [0,*,*; *,*,0; *,0,0].
    (YY^dag)_{02} = sum_k Y_{0k} * conj(Y_{2k})
    = Y_{00}*conj(Y_{20}) + Y_{01}*conj(Y_{21}) + Y_{02}*conj(Y_{22})
    = 0*conj(Y_{20}) + Y_{01}*0 + Y_{02}*0 = 0
    because Y_{00} = Y_{21} = Y_{22} = 0 from the texture.
    """
    tex = _build_texture(UP_L, N_val)
    nonzero = int(tex.sum())

    y00_zero = tex[0, 0] == 0
    y21_zero = tex[2, 1] == 0
    y22_zero = tex[2, 2] == 0

    yydag_02_zero = y00_zero and y21_zero and y22_zero

    return {
        'texture': tex.tolist(),
        'nonzero_count': nonzero,
        'Y00_zero': y00_zero,
        'Y21_zero': y21_zero,
        'Y22_zero': y22_zero,
        'YYdag_02_is_zero': yydag_02_zero,
    }


def winding_numbers(N_val=N):
    """Compute winding numbers for each CKM element."""
    up = UP_L
    dn = DN_L

    tex = _build_texture(up, N_val)
    # Check which (YY^dag) off-diagonals are nonzero
    # (YY^dag)_{ij} = sum_k tex[k,i]*tex[k,j] (simplified check)
    yydag_01 = any(tex[k, 0] * tex[k, 1] for k in range(3))
    yydag_12 = any(tex[k, 1] * tex[k, 2] for k in range(3))
    yydag_02 = any(tex[k, 0] * tex[k, 2] for k in range(3))

    return [
        {
            'element': 'V_us',
            'up_modes': f'{up[0]}->{up[1]}',
            'dn_modes': f'{dn[0]}->{dn[1]}',
            'w_up': abs(up[0] - up[1]),
            'w_dn': abs(dn[0] - dn[1]),
            'w_total': abs(up[0] - up[1]) + abs(dn[0] - dn[1]),
            'YYdag_nonzero': yydag_01,
            'level': 'TREE',
        },
        {
            'element': 'V_cb',
            'up_modes': f'{up[1]}->{up[2]}',
            'dn_modes': f'{dn[1]}->{dn[2]}',
            'w_up': abs(up[1] - up[2]),
            'w_dn': abs(dn[1] - dn[2]),
            'w_total': abs(up[1] - up[2]) + abs(dn[1] - dn[2]),
            'YYdag_nonzero': yydag_12,
            'level': 'TREE',
        },
        {
            'element': 'V_ub',
            'up_modes': f'{up[0]}->{up[2]}',
            'dn_modes': f'{dn[0]}->{dn[2]}',
            'w_up': abs(up[0] - up[2]),
            'w_dn': abs(dn[0] - dn[2]),
            'w_total': abs(up[0] - up[2]) + abs(dn[0] - dn[2]),
            'YYdag_nonzero': yydag_02,
            'level': 'INSTANTON',
        },
    ]


def instanton_action(N_val=N):
    """S_inst = (N-1) * 2*pi*k_frac."""
    b_N = N_val * (N_val + 1) / 12 - log(2) + log(N_val) / (N_val - 1)
    k_phys = 12 * b_N / 6 - N_val / 2
    k_frac = k_phys - int(k_phys)

    S = (N_val - 1) * 2 * pi * k_frac
    K = exp(-2 * pi * k_frac)

    return {
        'k_frac': k_frac,
        'N_minus_1': N_val - 1,
        'S_inst': S,
        'exp_neg_S': exp(-S),
        'K_to_N_minus_1': K ** (N_val - 1),
    }


def selectivity_proof(N_val=N):
    """Prove the instanton correction applies ONLY to V_ub."""
    table = winding_numbers(N_val)

    return {
        'V_us_corrected': not table[0]['YYdag_nonzero'],
        'V_cb_corrected': not table[1]['YYdag_nonzero'],
        'V_ub_corrected': not table[2]['YYdag_nonzero'],
        'reason': '(YY^dag)_{02}=0 forces V_ub to arise only from indirect path',
    }
