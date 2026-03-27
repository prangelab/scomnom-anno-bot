# Dataset

Briefly describe the dataset, tissue, species, and modality here.

Example:

- Human adipose snRNA-seq
- Mouse liver scRNA-seq
- Human PBMC scRNA-seq

# Directory guidance

List any project-specific directory rules here.

Examples:

- Prefer `figures/figures/png/` over `figures/figures/pdf/`.
- Do not use `figures/figures/pdf/`.
- Do not use superseded result folders such as `cluster_and_annotate_round1/` if a newer round exists.
- Ignore `tables/DE_tables_round1/` if the current task is marker-stage annotation rather than differential expression.

# Annotation backbone

State which clustering round and embedding should be used for annotation in this project.

Examples:

- Use the compacted clustering round as the annotation backbone.
- Use the post-annotation UMAP only as a display embedding.
- Use Harmony clustering for identity decisions and scANVI only for figure layout.

# Current annotation workflow caveats

Record any project-specific caveats that affect interpretation.

Examples:

- CellTypist labels were generated with an immune-only model, so non-immune labels are not reliable.
- One subset contains expected stromal contamination.
- Marker discovery has only been run for subset results, not for the project root.

# Plotting workflow

If the project has a preferred plotting notebook or script, record it here.

Examples:

- Preferred plotting notebook: `03_load_and_plot_all_de_functions.ipynb`
- Preferred plotting script: `scripts/plot_gene_panels.py`

If the local environment setup has important non-portable details, record them here.

Examples:

- Conda environment name: `scOmnom_env`
- Conda activation helper path on this machine
- Any known import or cache quirks

# Active context notes

Record any current-project rules that help select the correct result tree.

Examples:

- Root-level work should use `results_round2/`.
- Lymphoid work should use `results_subset_lymphoid/`.
- If duplicate result trees exist, prefer the newest timestamped version.
