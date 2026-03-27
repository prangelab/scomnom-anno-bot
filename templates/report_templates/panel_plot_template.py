from pathlib import Path

import scanpy as sc
import scomnom as om


def infer_groupby_key(adata):
    candidates = [col for col in adata.obs.columns if col.startswith("cluster_label")]
    if candidates:
        return sorted(candidates)[-1]
    if "leiden" in adata.obs.columns:
        return "leiden"
    raise ValueError("Could not infer a cluster grouping key from adata.obs")


def ensure_umap(adata):
    if "X_umap" in adata.obsm:
        return
    use_rep = None
    for candidate in ["Harmony", "scANVI__annotated", "scANVI", "X_integrated", "X_pca"]:
        if candidate in adata.obsm:
            use_rep = candidate
            break
    sc.pp.neighbors(adata, use_rep=use_rep)
    sc.tl.umap(adata)


def plot_panel(adata_path, outdir, genes, groupby=None, prefix="panel"):
    adata = om.load_dataset(adata_path)
    groupby = groupby or infer_groupby_key(adata)
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    om.plotting.plot_de_dotplot_top_genes(
        adata,
        genes=genes,
        groupby=groupby,
        display=True,
        file=str(outdir / f"{prefix}_dotplot.png"),
    )

    om.plotting.plot_de_violin_grid_genes(
        adata,
        genes=genes,
        groupby=groupby,
        stripplot=True,
        dot_size=0,
        display=True,
        file=str(outdir / f"{prefix}_violin.png"),
    )

    ensure_umap(adata)
    om.plotting.plot_de_umap_features_grid(
        adata,
        genes=genes,
        ncols=3,
        show_umap_corner_axes=True,
        display=True,
        file=str(outdir / f"{prefix}_umap.png"),
    )


if __name__ == "__main__":
    raise SystemExit("Import this file or adapt it for a project-specific plotting entrypoint.")
