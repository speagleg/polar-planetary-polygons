#!/usr/bin/env python3
"""Generate Figure 4: WDW potential for N=7 and N=11."""
import sys
sys.path.insert(0, 'src')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from planetary_polygons.extensions.hierarchy import V_BO, find_threshold_BO
import os

os.makedirs('figures', exist_ok=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.5))

for ax, N, title in [(ax1, 7, r'$N = 7$'), (ax2, 11, r'$N = 11$')]:
    rho_star = find_threshold_BO(N)
    rhos = np.linspace(0.01, rho_star * 1.5, 500)
    V = [V_BO(r, N) for r in rhos]

    ax.plot(rhos, V, 'k-', linewidth=2)
    ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
    ax.axvline(x=rho_star, color='#d6604d', linestyle=':', linewidth=1)

    # Shade tunneling region
    V_arr = np.array(V)
    rhos_arr = np.array(rhos)
    mask = V_arr < 0
    if np.any(mask):
        ax.fill_between(rhos_arr[mask], V_arr[mask], 0, alpha=0.15, color='#2166ac')

    ax.annotate(rf'$\rho^* = {rho_star:.2f}$',
                xy=(rho_star, 0), xytext=(rho_star*1.1, max(V)*0.3),
                fontsize=9, arrowprops=dict(arrowstyle='->', color='#d6604d'))

    ax.set_xlabel(r'$\rho$', fontsize=11)
    ax.set_ylabel(r'$V(\rho)$', fontsize=11)
    ax.set_title(title, fontsize=12)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('figures/fig_wdw_potential.pdf', bbox_inches='tight')
plt.close()
print("OK: figures/fig_wdw_potential.pdf")
