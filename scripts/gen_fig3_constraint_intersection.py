#!/usr/bin/env python3
"""Generate Figure 3: Constraint intersection diagram."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs('figures', exist_ok=True)

fig, ax = plt.subplots(figsize=(6, 4))

# Data: planet, N_obs, N_Rossby, N_Thomson, N_pack, binding
planets = ['Saturn', 'Jupiter N', 'Jupiter S', 'Neptune']
N_obs = [6, 8, 5, None]
N_rossby = [6, None, None, None]  # None = not applicable
N_thomson = [7, 8, 7, 7]
N_pack = [None, None, 5, 4]  # estimated

x = np.arange(len(planets))
width = 0.22

# Plot constraints as grouped bars
bars_t = ax.bar(x - width, [7, 8, 7, 7], width, label='Thomson', color='#4393c3', alpha=0.8)
bars_r = ax.bar(x, [6, 12, 12, 12], width, label='Rossby', color='#92c5de', alpha=0.8)
# Use 12 as "not binding" placeholder for visualization
bars_p = ax.bar(x + width, [12, 12, 5, 4], width, label='Packing', color='#f4a582', alpha=0.8)

# Mark observed N with large markers
for i, n in enumerate(N_obs):
    if n is not None:
        ax.plot(i, n, 'k*', markersize=15, zorder=5)

# Mark "not applicable" bars as faded
for i in [1, 2, 3]:  # Rossby not applicable for Jupiter/Neptune
    bars_r[i].set_alpha(0.15)
for i in [0, 1]:  # Packing not binding for Saturn/Jupiter N
    bars_p[i].set_alpha(0.15)

ax.set_ylabel(r'$N_{\mathrm{max}}$', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(planets, fontsize=10)
ax.set_ylim(0, 13)
ax.legend(fontsize=9, loc='upper right')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Add annotation for stars
ax.annotate(u'\u2605 = observed $N$', xy=(0.02, 0.95), xycoords='axes fraction',
            fontsize=9, va='top')

plt.tight_layout()
plt.savefig('figures/fig_constraint_intersection.pdf', bbox_inches='tight')
plt.close()
print("OK: figures/fig_constraint_intersection.pdf")
