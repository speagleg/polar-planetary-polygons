#!/usr/bin/env python3
"""Generate Figure 6: Hierarchy decomposition."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs('figures', exist_ok=True)

fig, ax = plt.subplots(figsize=(5, 4))

components = ['Instanton\n$2S_{BO}(7)$', 'Mass gap\n$\\Delta\\varepsilon \\ln\\varepsilon_7$', 'Gravity\nprefactor']
values = [36.548, 2.224, -0.313]
colors = ['#4393c3', '#92c5de', '#f4a582']

# Stacked bar
bottom = 0
for i, (comp, val, col) in enumerate(zip(components, values, colors)):
    if val > 0:
        ax.bar(0, val, bottom=bottom, color=col, width=0.5, label=f'{comp}: {val:+.3f}')
        ax.text(0.3, bottom + val/2, f'{val:+.3f}', va='center', fontsize=9)
        bottom += val
    else:
        ax.bar(0, abs(val), bottom=bottom + val, color=col, width=0.5,
               label=f'{comp}: {val:+.3f}', hatch='//')
        ax.text(0.3, bottom + val/2, f'{val:+.3f}', va='center', fontsize=9)
        bottom += val

# Total line
total = sum(values)
ax.axhline(y=total, color='black', linestyle='-', linewidth=2)
ax.text(0.35, total + 0.3, f'Total: {total:.3f}', fontsize=10, fontweight='bold')

# Observed
ax.axhline(y=38.442, color='#d6604d', linestyle='--', linewidth=1.5)
ax.text(0.35, 38.442 - 0.5, f'Observed: 38.442', fontsize=9, color='#d6604d')

ax.set_xlim(-0.5, 1.5)
ax.set_ylim(0, 40)
ax.set_ylabel(r'$\ln(M_P / v)$', fontsize=12)
ax.set_xticks([])
ax.legend(fontsize=8, loc='upper left', bbox_to_anchor=(-0.15, 1.0))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
plt.tight_layout()
plt.savefig('figures/fig_hierarchy_decomposition.pdf', bbox_inches='tight')
plt.close()
print("OK: figures/fig_hierarchy_decomposition.pdf")
