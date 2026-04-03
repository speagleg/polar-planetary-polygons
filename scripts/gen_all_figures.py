#!/usr/bin/env python3
"""Generate all publication-quality figures for the paper series.

Run from project root:
    PYTHONPATH=src python3 scripts/gen_all_figures.py
"""
import sys
import os

# Ensure we can import project modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'figures'), exist_ok=True)
os.chdir(os.path.join(os.path.dirname(__file__), '..'))

import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['mathtext.fontset'] = 'cm'
import matplotlib.pyplot as plt
import numpy as np


def fig1_eigenvalue_threshold():
    """Figure 1: Eigenvalue threshold at N=7."""
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
    print("  [1/6] figures/fig_eigenvalue_threshold.pdf")


def fig2_oblateness_signflip():
    """Figure 2: Saturn oblateness sign flip."""
    from planetary_polygons.extensions.oblate_spheroid import havelock_eigenvalue_spheroid

    a, b = 60268e3, 54364e3  # Saturn semi-axes in meters
    R_ring = 15000e3
    N, m = 6, 3

    phis = np.linspace(60, 90, 200)
    lams = np.array([
        havelock_eigenvalue_spheroid(N, m, np.radians(phi), R_ring, a, b)
        for phi in phis
    ])

    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.plot(phis, lams, 'k-', linewidth=2)
    ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
    ax.fill_between(phis, lams, 0, where=(lams > 0), alpha=0.15, color='green')
    ax.fill_between(phis, lams, 0, where=(lams < 0), alpha=0.15, color='red')

    phi_crit = phis[np.argmin(np.abs(lams))]
    ax.axvline(x=phi_crit, color='gray', linestyle=':', linewidth=1)
    ax.annotate(rf'$\varphi_{{\mathrm{{crit}}}} \approx {phi_crit:.0f}^\circ$',
                xy=(phi_crit, -0.02), xytext=(phi_crit-5, -0.08),
                fontsize=9, arrowprops=dict(arrowstyle='->', color='gray'))

    ax.axvline(x=78, color='#2166ac', linestyle='--', linewidth=1.5)
    ax.annotate('Hexagon\n$(78^\\circ\\mathrm{N})$', xy=(78, 0.005), xytext=(82, 0.04),
                fontsize=9, color='#2166ac',
                arrowprops=dict(arrowstyle='->', color='#2166ac'))

    ax.set_xlabel(r'Latitude $\varphi$ ($^\circ$N)', fontsize=11)
    ax.set_ylabel(r'$\lambda_3(N{=}6)$', fontsize=11)
    ax.set_xlim(60, 90)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig('figures/fig_oblateness_signflip.pdf', bbox_inches='tight')
    plt.close()
    print("  [2/6] figures/fig_oblateness_signflip.pdf")


def fig3_constraint_intersection():
    """Figure 3: Constraint intersection diagram."""
    fig, ax = plt.subplots(figsize=(6, 4))

    planets = ['Saturn', 'Jupiter N', 'Jupiter S', 'Neptune']
    N_obs = [6, 8, 5, None]
    x = np.arange(len(planets))
    width = 0.22

    bars_t = ax.bar(x - width, [7, 8, 7, 7], width, label='Thomson', color='#4393c3', alpha=0.8)
    bars_r = ax.bar(x, [6, 12, 12, 12], width, label='Rossby', color='#92c5de', alpha=0.8)
    bars_p = ax.bar(x + width, [12, 12, 5, 4], width, label='Packing', color='#f4a582', alpha=0.8)

    for i, n in enumerate(N_obs):
        if n is not None:
            ax.plot(i, n, 'k*', markersize=15, zorder=5)

    for i in [1, 2, 3]:
        bars_r[i].set_alpha(0.15)
    for i in [0, 1]:
        bars_p[i].set_alpha(0.15)

    ax.set_ylabel(r'$N_{\mathrm{max}}$', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(planets, fontsize=10)
    ax.set_ylim(0, 13)
    ax.legend(fontsize=9, loc='upper right')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.annotate(u'\u2605 = observed $N$', xy=(0.02, 0.95), xycoords='axes fraction',
                fontsize=9, va='top')
    plt.tight_layout()
    plt.savefig('figures/fig_constraint_intersection.pdf', bbox_inches='tight')
    plt.close()
    print("  [3/6] figures/fig_constraint_intersection.pdf")


def fig4_wdw_potential():
    """Figure 4: WDW potential for N=7 and N=11."""
    from planetary_polygons.extensions.hierarchy import V_BO, find_threshold_BO

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.5))

    for ax, N, title in [(ax1, 7, r'$N = 7$'), (ax2, 11, r'$N = 11$')]:
        rho_star = find_threshold_BO(N)
        rhos = np.linspace(0.01, rho_star * 1.5, 500)
        V = np.array([V_BO(r, N) for r in rhos])

        ax.plot(rhos, V, 'k-', linewidth=2)
        ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
        ax.axvline(x=rho_star, color='#d6604d', linestyle=':', linewidth=1)

        mask = V < 0
        if np.any(mask):
            ax.fill_between(rhos[mask], V[mask], 0, alpha=0.15, color='#2166ac')

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
    print("  [4/6] figures/fig_wdw_potential.pdf")


def fig5_energy_budget():
    """Figure 5: Cosmic energy budget."""
    from planetary_polygons.extensions.dark_sector import dark_sector_budget

    b = dark_sector_budget(11)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.5))

    sizes1 = [b['DE_pct'], b['DM_pct'], b['M_pct']]
    labels = [f'Dark energy\n{sizes1[0]:.1f}%', f'Dark matter\n{sizes1[1]:.1f}%',
              f'Baryons\n{sizes1[2]:.1f}%']
    colors = ['#4393c3', '#92c5de', '#f4a582']
    ax1.pie(sizes1, labels=labels, colors=colors, startangle=90, textprops={'fontsize': 9})
    ax1.set_title('Theory ($N = 11$)', fontsize=11)

    sizes2 = [68.5, 26.6, 4.9]
    labels2 = [f'Dark energy\n{sizes2[0]}%', f'Dark matter\n{sizes2[1]}%',
               f'Baryons\n{sizes2[2]}%']
    ax2.pie(sizes2, labels=labels2, colors=colors, startangle=90, textprops={'fontsize': 9})
    ax2.set_title('Planck 2018', fontsize=11)

    plt.tight_layout()
    plt.savefig('figures/fig_energy_budget.pdf', bbox_inches='tight')
    plt.close()
    print("  [5/6] figures/fig_energy_budget.pdf")


def fig6_hierarchy_decomposition():
    """Figure 6: Hierarchy decomposition."""
    fig, ax = plt.subplots(figsize=(5, 4))

    components = ['Instanton\n$2S_{BO}(7)$',
                  'Mass gap\n$\\Delta\\varepsilon \\ln\\varepsilon_7$',
                  'Gravity\nprefactor']
    values = [36.548, 2.224, -0.313]
    colors = ['#4393c3', '#92c5de', '#f4a582']

    bottom = 0
    for comp, val, col in zip(components, values, colors):
        if val > 0:
            ax.bar(0, val, bottom=bottom, color=col, width=0.5,
                   label=f'{comp}: {val:+.3f}')
            ax.text(0.3, bottom + val/2, f'{val:+.3f}', va='center', fontsize=9)
            bottom += val
        else:
            ax.bar(0, abs(val), bottom=bottom + val, color=col, width=0.5,
                   label=f'{comp}: {val:+.3f}', hatch='//')
            ax.text(0.3, bottom + val/2, f'{val:+.3f}', va='center', fontsize=9)
            bottom += val

    total = sum(values)
    ax.axhline(y=total, color='black', linestyle='-', linewidth=2)
    ax.text(0.35, total + 0.3, f'Total: {total:.3f}', fontsize=10, fontweight='bold')
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
    print("  [6/6] figures/fig_hierarchy_decomposition.pdf")


if __name__ == '__main__':
    print("Generating publication figures...")
    fig1_eigenvalue_threshold()
    fig2_oblateness_signflip()
    fig3_constraint_intersection()
    fig4_wdw_potential()
    fig5_energy_budget()
    fig6_hierarchy_decomposition()
    print("Done. All 6 PDFs written to figures/")
