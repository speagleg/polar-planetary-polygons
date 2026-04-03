#!/usr/bin/env python3
"""Generate Figure 1: Eigenvalue threshold at N=7."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs('figures', exist_ok=True)

fig, ax = plt.subplots(figsize=(5, 3.5))
colors = {5: '#2166ac', 6: '#4393c3', 7: '#333333', 8: '#d6604d', 9: '#b2182b'}
for N in [5, 6, 7, 8, 9]:
    ms = np.arange(1, N)
    lams = (N-1) - ms*(N-ms)/2
    ax.plot(ms, lams, 'o-', color=colors[N], label=f'N={N}', markersize=4, linewidth=1.5)
    if N == 7:
        ax.plot(3, 0, 'ko', markersize=8, zorder=5)
        ax.annotate(r'$\lambda_3 = 0$', xy=(3, 0), xytext=(3.5, 0.8),
                    fontsize=9, arrowprops=dict(arrowstyle='->', color='black'))

ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
ax.fill_between([0.5, 8.5], [-3, -3], [0, 0], alpha=0.08, color='red')
ax.set_xlabel(r'Mode $m$', fontsize=11)
ax.set_ylabel(r'$\lambda_m = (N{-}1) - m(N{-}m)/2$', fontsize=11)
ax.legend(fontsize=9, loc='upper right')
ax.set_xlim(0.5, 8.5)
ax.set_ylim(-3, 7)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('figures/fig_eigenvalue_threshold.pdf', bbox_inches='tight')
plt.close()
print("OK: figures/fig_eigenvalue_threshold.pdf")
