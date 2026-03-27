# Dataset

Update this line with a short dataset description.

# Directory guidance

- Prefer `figures/figures/png/` over `figures/figures/pdf/`.
- Do not use `figures/figures/pdf/` unless the user explicitly asks for a PDF-only asset.
- If multiple result trees exist for the same stage, prefer the newest valid one.
- If there are obvious duplicated, nested, outdated, or superseded result folders, prefer the newest or explicitly active one.
- For annotation-stage work, prioritize marker-stage outputs unless the user explicitly asks for differential expression or another stage.

# Annotation backbone

- If multiple clustering rounds exist, prefer the latest compacted or finalized annotation round that looks current and is not marked as superseded.
- Use the chosen clustering round as the annotation backbone.
- If multiple embeddings exist, treat the cleaner annotated or presentation UMAP as a display layer only, unless the user explicitly says it should define identity.

# Current annotation workflow caveats

- Add project-specific caveats here if needed.

# Plotting workflow

- Conda environment name: `scOmnom_env`
- Use `templates/report_templates/panel_plot_template.py` as the default panel-generation path.
- If the project has a preferred local plotting script, add it here.

# Active context notes

- Root-level work should use the main result tree.
- Subset work should use the matching subset result tree.
- Once a subset is made active, continue using that subset context until the user switches again.
