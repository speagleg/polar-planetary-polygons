#!/usr/bin/env python3
"""Generate Figure 5: Cosmic energy budget."""
import sys
sys.path.insert(0, 'src')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from planetary_polygons.extensions.dark_sector import dark_sector_budget
import os

os.makedirs('figures', exist_ok=True)

b = dark_sector_budget(11)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.5))

# Theory prediction
sizes1 = [b['DE_pct'], b['DM_pct'], b['M_pct']]
labels = [f'Dark energy\n{sizes1[0]:.1f}%', f'Dark matter\n{sizes1[1]:.1f}%', f'Baryons\n{sizes1[2]:.1f}%']
colors = ['#4393c3', '#92c5de', '#f4a582']
ax1.pie(sizes1, labels=labels, colors=colors, startangle=90, textprops={'fontsize': 9})
ax1.set_title('Theory ($N = 11$)', fontsize=11)

# Planck 2018
sizes2 = [68.5, 26.6, 4.9]
labels2 = [f'Dark energy\n{sizes2[0]}%', f'Dark matter\n{sizes2[1]}%', f'Baryons\n{sizes2[2]}%']
ax2.pie(sizes2, labels=labels2, colors=colors, startangle=90, textprops={'fontsize': 9})
ax2.set_title('Planck 2018', fontsize=11)

plt.tight_layout()
plt.savefig('figures/fig_energy_budget.pdf', bbox_inches='tight')
plt.close()
print("OK: figures/fig_energy_budget.pdf")
