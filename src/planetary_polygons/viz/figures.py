"""Figure generation API: one function per paper figure."""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt


def _ensure_outdir(outdir):
    os.makedirs(outdir, exist_ok=True)
    return outdir


def fig1_spiral_to_polygon(r_values=None, outdir="figures/"):
    """Fig 1: Loxodromic orbit family r=5→1 with phi=pi/3."""
    if r_values is None:
        r_values = [5.0, 3.0, 2.0, 1.5, 1.2, 1.05, 1.0]
    _ensure_outdir(outdir)
    fig, ax = plt.subplots(figsize=(8, 8))
    colors = plt.cm.plasma(np.linspace(0.1, 0.9, len(r_values)))
    phi = np.pi / 3
    for r, color in zip(r_values, colors):
        t = np.linspace(0, 6, 3000)
        lam = r * np.exp(1j * phi)
        z = lam**t  # orbit of z0=1 under f(z)=lambda*z
        lw = 2.5 if r == 1.0 else 1.5
        ax.plot(z.real, z.imag, color=color, lw=lw, alpha=0.9, label=f'r={r}')
    ax.set_aspect('equal')
    ax.set_title("Spiral → Hexagon family (r: 5 → 1, φ = π/3)")
    ax.legend(fontsize=8, loc='upper right')
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3)
    fpath = os.path.join(outdir, "01_spiral_to_polygon.png")
    fig.savefig(fpath, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return fpath


def fig2_energy_curvature(N_range=None, outdir="figures/"):
    """Fig 2: Minimum constrained eigenvalue vs N."""
    if N_range is None:
        N_range = range(3, 9)
    _ensure_outdir(outdir)
    from planetary_polygons.core.hessian import constrained_hessian_analysis
    N_vals = list(N_range)
    min_evals = []
    for N in N_vals:
        result = constrained_hessian_analysis(N)
        min_evals.append(min(result.constrained_evals))
    colors = ['#2ecc71' if e >= 0 else '#e74c3c' for e in min_evals]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(N_vals, min_evals, color=colors, edgecolor='black', linewidth=0.5)
    ax.axhline(0, color='black', lw=1.5, ls='--')
    ax.axvline(6.5, color='orange', lw=2, ls=':', label='N_crit = 7 boundary')
    ax.set_xlabel("N (number of vortices)", fontsize=12)
    ax.set_ylabel("Minimum constrained eigenvalue", fontsize=12)
    ax.set_title("Energy curvature on constraint surface: N_crit = 7")
    ax.legend()
    fpath = os.path.join(outdir, "02_energy_curvature.png")
    fig.savefig(fpath, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return fpath


def fig3_cross_planetary(outdir="figures/"):
    """Fig 3: Saturn (N=6) and Jupiter (N=8) polar polygon comparison."""
    _ensure_outdir(outdir)
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    for ax, (planet, N_pred, color) in zip(axes, [
        ('Saturn (N=6)', 6, '#3498db'),
        ('Jupiter (N=8)', 8, '#e67e22'),
    ]):
        theta = np.linspace(0, 2*np.pi, 1000)
        amp = 0.06
        r = 1.0 + amp * np.cos(N_pred * theta)
        ax.fill(r*np.cos(theta), r*np.sin(theta), alpha=0.3, color=color)
        ax.plot(r*np.cos(theta), r*np.sin(theta), color=color, lw=2)
        ax.plot(np.cos(theta), np.sin(theta), 'k--', lw=1, alpha=0.4, label='circle')
        ax.set_aspect('equal')
        ax.set_title(planet, fontsize=13)
        ax.legend(fontsize=9)
    fig.suptitle("Cross-planetary polygon comparison", fontsize=14)
    fpath = os.path.join(outdir, "03_cross_planetary.png")
    fig.savefig(fpath, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return fpath


def fig4_complete_chain(outdir="figures/"):
    """Fig 4: Logical chain from energy to planetary observation."""
    _ensure_outdir(outdir)
    fig, ax = plt.subplots(figsize=(12, 3))
    steps = [
        'Log\ninteraction', 'Constrained\nHessian', 'Havelock\nidentity',
        'N_crit = 7', 'Saturn/Jupiter\nobservation'
    ]
    colors = ['#3498db', '#9b59b6', '#e74c3c', '#e67e22', '#2ecc71']
    for i, (step, color) in enumerate(zip(steps, colors)):
        ax.text(i*2, 0, step, ha='center', va='center', fontsize=11,
                bbox=dict(boxstyle='round,pad=0.4', facecolor=color, alpha=0.7, edgecolor='black'))
        if i < len(steps)-1:
            ax.annotate('', xy=((i+1)*2-0.6, 0), xytext=(i*2+0.6, 0),
                       arrowprops=dict(arrowstyle='->', lw=2, color='black'))
    ax.set_xlim(-1, (len(steps)-1)*2+1)
    ax.set_ylim(-1, 1)
    ax.axis('off')
    ax.set_title("Complete logical chain", fontsize=13)
    fpath = os.path.join(outdir, "04_complete_chain.png")
    fig.savefig(fpath, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return fpath


def fig5_thomson_stability(outdir="figures/"):
    """Fig 5: Thomson stability eigenvalues vs N."""
    _ensure_outdir(outdir)
    from planetary_polygons.core.hessian import constrained_hessian_analysis
    N_vals = list(range(3, 10))
    min_evals = [min(constrained_hessian_analysis(N).constrained_evals) for N in N_vals]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(N_vals, min_evals, 'o-', color='navy', lw=2, ms=8, label='min eigenvalue')
    ax.axhline(0, color='red', lw=1.5, ls='--', label='stability boundary')
    ax.axvline(6.5, color='orange', lw=2, ls=':', label='N=7 threshold')
    ax.fill_between(N_vals, min_evals, 0,
                    where=[e < 0 for e in min_evals], alpha=0.2, color='red')
    ax.set_xlabel("N", fontsize=12)
    ax.set_ylabel("Minimum constrained eigenvalue", fontsize=12)
    ax.set_title("Thomson stability: N ≤ 6 stable, N ≥ 7 unstable")
    ax.legend()
    fpath = os.path.join(outdir, "05_thomson_stability.png")
    fig.savefig(fpath, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return fpath


def fig_extension(section, outdir="figures/"):
    """Extension figure placeholder for §6.x."""
    _ensure_outdir(outdir)
    section_names = {
        '6.1': 'Curved Surfaces', '6.2': 'Deformation Radius',
        '6.3': 'N=7 Bifurcation', '6.4': 'Blob Correction',
        '6.5': 'Multiring / Jupiter', '6.6': 'BEC Vortices',
        '6.7': 'Γ-Convergence Bridge', '6.8': 'Riemannian Havelock',
    }
    name = section_names.get(section, section)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.text(0.5, 0.5, f'§{section}\n{name}', ha='center', va='center',
            transform=ax.transAxes, fontsize=16,
            bbox=dict(boxstyle='round', facecolor='lightsteelblue'))
    ax.axis('off')
    ax.set_title(f"Extension §{section}: {name}")
    safe_section = section.replace('.', '_')
    fpath = os.path.join(outdir, f"ext_{safe_section}_{name.replace(' ', '_').replace('/', '')}.png")
    fig.savefig(fpath, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return fpath
