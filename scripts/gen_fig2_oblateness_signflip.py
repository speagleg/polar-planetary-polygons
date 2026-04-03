#!/usr/bin/env python3
"""Generate Figure 2: Saturn oblateness sign flip."""
import sys
sys.path.insert(0, 'src')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from planetary_polygons.extensions.oblate_spheroid import (
    havelock_eigenvalue_spheroid, gaussian_curvature as gaussian_curvature_spheroid
)
import os

os.makedirs('figures', exist_ok=True)

a, b = 60268e3, 54364e3  # Saturn semi-axes in meters
R_ring = 15000e3  # ring radius
N, m = 6, 3

phis = np.linspace(60, 90, 200)
lams = []
for phi in phis:
    lam = havelock_eigenvalue_spheroid(N, m, np.radians(phi), R_ring, a, b)
    lams.append(lam)
lams = np.array(lams)

fig, ax = plt.subplots(figsize=(5, 3.5))
ax.plot(phis, lams, 'k-', linewidth=2)
ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)

# Shade regions
ax.fill_between(phis, lams, 0, where=(lams > 0), alpha=0.15, color='green')
ax.fill_between(phis, lams, 0, where=(lams < 0), alpha=0.15, color='red')

# Critical latitude
phi_crit = phis[np.argmin(np.abs(lams))]
ax.axvline(x=phi_crit, color='gray', linestyle=':', linewidth=1)
ax.annotate(rf'$\varphi_{{\mathrm{{crit}}}} \approx {phi_crit:.0f}°$',
            xy=(phi_crit, -0.02), xytext=(phi_crit-5, -0.08),
            fontsize=9, arrowprops=dict(arrowstyle='->', color='gray'))

# Hexagon latitude
ax.axvline(x=78, color='#2166ac', linestyle='--', linewidth=1.5)
ax.annotate('Hexagon\n(78°N)', xy=(78, 0.005), xytext=(82, 0.04),
            fontsize=9, color='#2166ac',
            arrowprops=dict(arrowstyle='->', color='#2166ac'))

ax.set_xlabel(r'Latitude $\varphi$ (°N)', fontsize=11)
ax.set_ylabel(r'$\lambda_3(N{=}6)$', fontsize=11)
ax.set_xlim(60, 90)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('figures/fig_oblateness_signflip.pdf', bbox_inches='tight')
plt.close()
print("OK: figures/fig_oblateness_signflip.pdf")
