from __future__ import annotations

"""Template for compact DE tally plots from scOmnom DE summary tables.

Run this inside the project-local `scomnom_env` / `scOmnom_env` Python stack.
The script is intentionally generic so it can be adapted for phase 4, 5, 6,
and later synthesis stages without rewriting the plotting logic.

Expected inputs:
- a DE-enabled scOmnom AnnData object or a path to one
- pseudobulk and/or cell-level DE summary tables
- cluster labels in `adata.obs`

Outputs:
- a CSV tally table with counts of significant genes per cluster
- a full atlas bar plot
- a nonzero-only companion bar plot
"""

from dataclasses import dataclass
from pathlib import Path
import csv

import matplotlib.pyplot as plt
import pandas as pd
import scomnom as om
from pandas.errors import EmptyDataError


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_ALPHA = 0.05
SALMON = "#FA8072"
TEAL = "#267C7B"
GRAY = "#B9BDC6"


@dataclass(frozen=True)
class TallyConfig:
    dataset_id: str
    adata_path: Path
    pseudobulk_dir: Path | None
    celllevel_dir: Path | None
    cluster_label_key: str
    contrast_id: str
    pseudobulk_suffix: str | None = None
    celllevel_dirname: str | None = None
    parenchymal_clusters: set[str] | None = None
    immune_clusters: set[str] | None = None


def load_cluster_labels(adata_path: Path, cluster_label_key: str) -> dict[str, str]:
    adata = om.load_dataset(str(adata_path))
    series = adata.obs[cluster_label_key].astype(str)
    labels: dict[str, str] = {}
    for label in series.unique():
        cluster_id = label.split(":")[0].strip()
        labels[cluster_id] = label
    return labels


def count_pseudobulk_significant_genes(
    pseudobulk_dir: Path,
    contrast_suffix: str,
    alpha: float = DEFAULT_ALPHA,
) -> pd.DataFrame:
    rows = []
    pattern = f"condition_within_cluster__*__{contrast_suffix}.csv"
    for path in sorted(pseudobulk_dir.glob(pattern)):
        cluster_id = path.name.split("__")[1]
        n_sig = 0
        min_padj = 1.0
        with open(path, newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                try:
                    padj = float(row["padj"])
                except Exception:
                    continue
                if padj < alpha:
                    n_sig += 1
                min_padj = min(min_padj, padj)
        rows.append({"cluster_id": cluster_id, "n_sig_genes": n_sig, "min_padj": min_padj})
    return pd.DataFrame(rows).sort_values(["n_sig_genes", "min_padj"], ascending=[False, True]).reset_index(drop=True)


def count_celllevel_significant_genes(
    celllevel_dir: Path,
    contrast_dirname: str,
    alpha: float = DEFAULT_ALPHA,
) -> pd.DataFrame:
    base = celllevel_dir / contrast_dirname
    rows = []
    for subdir in sorted(base.glob("cluster__C*")):
        cluster_id = subdir.name.split("__")[1]
        csv_path = subdir / f"{subdir.name}__wilcoxon.csv"
        try:
            df = pd.read_csv(csv_path)
        except EmptyDataError:
            df = pd.DataFrame()
        except FileNotFoundError:
            df = pd.DataFrame()
        if df.empty:
            rows.append({"cluster_id": cluster_id, "n_sig_genes": 0, "min_padj": 1.0})
            continue
        n_sig = int((df["cell_wilcoxon_padj"] < alpha).sum())
        min_padj = float(df["cell_wilcoxon_padj"].min())
        rows.append({"cluster_id": cluster_id, "n_sig_genes": n_sig, "min_padj": min_padj})
    return pd.DataFrame(rows).sort_values(["n_sig_genes", "min_padj"], ascending=[False, True]).reset_index(drop=True)


def color_for_cluster(cluster_id: str, parenchymal_clusters: set[str] | None, immune_clusters: set[str] | None) -> str:
    if parenchymal_clusters and cluster_id in parenchymal_clusters:
        return SALMON
    if immune_clusters and cluster_id in immune_clusters:
        return TEAL
    return GRAY


def plot_barplot(
    df: pd.DataFrame,
    label_map: dict[str, str],
    outdir: Path,
    out_stem: str,
    title_text: str,
    xlabel: str,
    parenchymal_clusters: set[str] | None = None,
    immune_clusters: set[str] | None = None,
) -> None:
    plot_df = df.copy()
    plot_df["cluster_label"] = plot_df["cluster_id"].map(label_map).fillna(plot_df["cluster_id"])
    plot_df["color"] = plot_df["cluster_id"].map(
        lambda x: color_for_cluster(x, parenchymal_clusters, immune_clusters)
    )

    height = max(4.0, 0.5 * len(plot_df) + 0.8)
    fig, ax = plt.subplots(figsize=(8.2, height))
    ax.barh(plot_df["cluster_label"], plot_df["n_sig_genes"], color=plot_df["color"], edgecolor="none")
    ax.invert_yaxis()
    ax.set_xlabel(xlabel)
    ax.set_ylabel("")
    ax.set_title(title_text)
    ax.grid(axis="x", color="#D9D9D9", linewidth=0.8)
    ax.set_axisbelow(True)
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)

    max_value = int(plot_df["n_sig_genes"].max()) if len(plot_df) else 0
    offset = max(1.0, 0.015 * max(max_value, 10))
    for y, value in enumerate(plot_df["n_sig_genes"]):
        ax.text(value + offset, y, str(int(value)), va="center", ha="left", fontsize=9)

    fig.tight_layout()
    fig.savefig(outdir / f"{out_stem}.png", dpi=300, bbox_inches="tight", pad_inches=0.12)
    fig.savefig(outdir / f"{out_stem}.pdf", bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)


def generate_tally_plots(
    config: TallyConfig,
    outdir: Path,
    alpha: float = DEFAULT_ALPHA,
) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    label_map = load_cluster_labels(config.adata_path, config.cluster_label_key)

    if config.pseudobulk_dir and config.pseudobulk_suffix:
        df = count_pseudobulk_significant_genes(config.pseudobulk_dir, config.pseudobulk_suffix, alpha=alpha)
        layer_id = "pseudobulk"
        xlabel = f"Pseudobulk DE genes (FDR < {alpha:.2f})"
    elif config.celllevel_dir and config.celllevel_dirname:
        df = count_celllevel_significant_genes(config.celllevel_dir, config.celllevel_dirname, alpha=alpha)
        layer_id = "celllevel"
        xlabel = f"Cell-level DE genes (FDR < {alpha:.2f})"
    else:
        raise ValueError("Need either pseudobulk or cell-level DE inputs")

    df["cluster_label"] = df["cluster_id"].map(label_map).fillna(df["cluster_id"])
    df.to_csv(outdir / f"{config.dataset_id}__{config.contrast_id}__{layer_id}__tally.csv", index=False)

    nonzero = df[df["n_sig_genes"] > 0].reset_index(drop=True)
    top12 = df.head(12).reset_index(drop=True)

    title_base = f"{config.dataset_id.upper()} {config.contrast_id} ({layer_id})"
    plot_barplot(
        top12,
        label_map,
        outdir,
        f"{config.dataset_id}__{config.contrast_id}__{layer_id}__top12",
        f"{title_base}: top DE clusters",
        xlabel,
        config.parenchymal_clusters,
        config.immune_clusters,
    )
    plot_barplot(
        nonzero,
        label_map,
        outdir,
        f"{config.dataset_id}__{config.contrast_id}__{layer_id}__nonzero",
        f"{title_base}: clusters with DE signal",
        xlabel,
        config.parenchymal_clusters,
        config.immune_clusters,
    )


if __name__ == "__main__":
    raise SystemExit(
        "This is a template module. Import generate_tally_plots() and configure a TallyConfig "
        "for the specific dataset and contrast you want to render."
    )
