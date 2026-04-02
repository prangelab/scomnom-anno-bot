from pathlib import Path

import scanpy as sc
import scomnom as om


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


def plot_label_umap(
    adata_path,
    outdir,
    color_key,
    title=None,
    size=None,
    prefix=None,
):
    adata = om.load_dataset(adata_path)
    ensure_umap(adata)

    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    prefix = prefix or color_key
    title = title or color_key

    om.plotting.plot_de_umap_single(
        adata,
        color=color_key,
        legend_loc="right margin",
        size=size,
        title=title,
        show_umap_corner_axes=True,
        display=True,
        file=str(outdir / f"{prefix}_fulllegend.png"),
    )

    om.plotting.plot_de_umap_single(
        adata,
        color=color_key,
        legend_loc="on data",
        size=size,
        title=title,
        show_umap_corner_axes=True,
        display=True,
        file=str(outdir / f"{prefix}_shortlegend.png"),
    )


if __name__ == "__main__":
    raise SystemExit("Import this file or adapt it for a project-specific label-layer UMAP plotting entrypoint.")
