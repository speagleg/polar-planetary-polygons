"""Figure generation — stub. Full implementation in Task 13."""
import os


def _ensure_outdir(outdir):
    os.makedirs(outdir, exist_ok=True)
    return outdir


def fig1_spiral_to_polygon(r_values=None, outdir="figures/"):
    raise NotImplementedError("fig1 not yet implemented")


def fig2_energy_curvature(N_range=None, outdir="figures/"):
    raise NotImplementedError("fig2 not yet implemented")


def fig3_cross_planetary(outdir="figures/"):
    raise NotImplementedError("fig3 not yet implemented")


def fig4_complete_chain(outdir="figures/"):
    raise NotImplementedError("fig4 not yet implemented")


def fig5_thomson_stability(outdir="figures/"):
    raise NotImplementedError("fig5 not yet implemented")


def fig_extension(section, outdir="figures/"):
    raise NotImplementedError(f"fig_extension({section}) not yet implemented")
