# Purpose

Version: `0.1.0`

This `AGENTS.md` is a portable workflow guide for annotating `scOmnom` analysis outputs across projects. Use it as the shared workflow layer, and keep dataset-specific assumptions in a separate local override file when needed.

# Project-local overrides

If a `project-local.md` file exists in the active project or active subset root, read it during startup and treat it as the dataset-specific override layer.

When creating a new project-local override file, use this starter template if available:

- `templates/report_templates/project-local.example.md`

If the user wants more explanation of the intended contents, also consult:

- `templates/report_templates/project-local.annotated-example.md`

Use `project-local.md` for items such as:

- dataset description
- excluded or superseded directories
- preferred clustering round or embedding for annotation
- known CellTypist caveats for the current dataset
- project-specific plotting entrypoint details when they differ from the default reusable plotting script
- environment or path details that are not portable across machines or projects

Keep the shared workflow logic in `AGENTS.md` and move project-specific biology or layout assumptions into `project-local.md`.

# Startup check

At the start of a new session, before doing annotation work, perform a short startup check.

This startup check should be portable and should not assume anything specific about the project beyond what is written in the local `AGENTS.md` and optional `project-local.md`.

Run through the following in order:

- Read the full local `AGENTS.md` before starting annotation work.
- If `project-local.md` exists, read that too before starting annotation work.
- Identify the working root that contains the active `AGENTS.md`.
- Determine whether the current work should start at the main project root or in a subset result tree.
- If the user has not yet set an active subset context, default to the main project root.
- Identify the expected input and output locations for the current context:
  - `adata`
  - `figures`
  - `tables`
  - `annotation`
  - `panels`
- Check whether portable templates exist under `templates/report_templates/` and use them when present.
- Check whether there are obvious duplicated, nested, outdated, or superseded result folders, and prefer the newest or explicitly active one.
- Read the local directory guidance and exclusion rules before inspecting figures or tables.
- Apply any project-local overrides from `project-local.md` before deciding which result tree, round, embedding, or notebook to use.

Environment check:

- Check whether `scOmnom_env` can be activated.
- Before importing `scomnom` or other plotting-related libraries, set writable cache directories:
  - `NUMBA_CACHE_DIR=/tmp/numba_cache`
  - `MPLCONFIGDIR=/tmp/matplotlib_cache`
- Check whether `scomnom` can be imported inside that environment after setting those cache variables.
- If both succeed, panel plotting and other `scomnom`-dependent steps can be used normally.
- If either check fails, do not hard-fail later. Instead, continue with the annotation steps that can still be done from existing figures, tables, and reports, and explicitly note that custom panel plotting or other `scomnom`-dependent steps are currently unavailable.
- When `scOmnom_env` or `scomnom` is unavailable, gracefully opt out of panel generation until the environment issue is resolved.

Startup behavior rules:

- Log the startup checks to chat in short plain-language updates so the user can see what is being validated.
- When locating the working tree, use wording such as `Checking whether this folder contains a usable scOmnom results tree.` or similarly clear portable phrasing.
- When determining context, use wording such as `Checking which result tree is active for this task.`
- When checking the environment, explicitly report the `scOmnom_env` and `scomnom` status in chat.
- If plotting is available, say so clearly, for example: `scOmnom plotting is available, so custom panel generation can be used if needed.`
- If plotting is unavailable, say so clearly, for example: `scOmnom plotting is not available right now, so I will continue with existing figures and tables and skip custom panel generation unless the environment is fixed.`
- Do not start a persistent panel session automatically unless the user asks for panel plotting, says `start panel session`, or a deep-dive workflow explicitly requires it.
- Before writing any report, confirm the correct output tree for the active context.
- For phase 1 work, inspect the relevant global QC outputs early so later interpretations are grounded in dataset quality.
- For deep dives, confirm that the cluster-specific report should be written into the active context, not a previously used one.

# Directory guidance

Apply any dataset-specific directory exclusions from `project-local.md` first.

In general:

- Prefer PNG outputs over PDF outputs when both exist and the PNG is sufficient for inspection.
- Prefer the current active or newest valid result tree over obviously superseded or duplicated ones.
- For annotation-stage work, prioritize marker-stage outputs unless the user explicitly asks for differential expression or another stage.

# Subset directory rule

If the user asks to work on a subset, always switch fully into that subset's own result tree.

This applies to any subset such as lymphoid, myeloid, stromal, or later compartment-specific subsets.

When working on a subset:

- Use the subset-specific `adata` files, not the main-project `adata` files.
- Use the subset-specific `figures` tree, not the main-project `figures` tree.
- Use the subset-specific `tables` tree, not the main-project `tables` tree.
- Write annotation outputs into that subset's own result directory, not the main-project root.
- Write custom panel outputs into that subset's own `panels` location inside the relevant subset result directory, not the main-project `panels/`.

In short:

- Main-project requests use the main project root.
- Subset requests use the matching subset result root for inputs and outputs.

If the user says to annotate a subset cluster, interpret that as:

- read from the appropriate subset `adata`, `figures`, and `tables`
- write the annotation note and copied assets into that subset result tree
- write panel plots into that subset result tree

Maintain an active context rule for subset work:

- If the user says something like `let's work on the stromal subset now`, treat that subset result tree as the active context.
- After that, interpret later commands such as `Annotate Cnn` as referring to the active subset context by default.
- Stay in that active subset context until the user explicitly switches back to the main dataset or to another subset.
- Only pause for clarification if there is real ambiguity about which active context should apply.

# Annotation style

If `project-local.md` specifies a preferred clustering round or preferred display embedding, follow that local rule.

Otherwise:

- Use the chosen annotation clustering round as the identity backbone.
- Treat alternative embeddings used mainly for visualization as display layers rather than the primary source of cluster identity, unless the user explicitly says otherwise.

Use the following evidence hierarchy for annotation:

- Base annotations primarily on marker gene expression, using both cell-level and pseudobulk marker outputs.
- Use pathway enrichment and regulatory/activity outputs as supporting evidence, especially Hallmark, Reactome, DoRothEA, and PROGENy.
- Check marker specificity in dotplots and violin plots before committing to a label.
- If the standard outputs are insufficient for a lineage or state call, request or use additional targeted gene panels.

Final population names should follow this style:

- Use two marker genes plus a short descriptive population or state name.
- Prefer names in the format `MARKER1+ MARKER2+ Short descriptive label`.
- Choose marker genes that are recognizable and reasonably specific for the population.
- Use pathway and regulator evidence to refine the descriptive phrase, but do not let pathway names replace marker-based identity.

# Annotation workflow

If `project-local.md` describes known CellTypist limitations or dataset-specific annotation caveats, incorporate them into the interpretation strategy.

Use a two-pass annotation strategy:

- First pass: determine rough cell types across the full dataset and decide which clusters should be grouped into broader compartments for subsetting.
- During the first pass, if a population is already sufficiently granular and does not need further compartmentalization, it can receive its final label immediately.
- After the first pass, the selected compartments will be subsetted, reclustered, and rerun through marker discovery outside this annotation step.
- Second pass: annotate the reclustered compartment subsets and assign final names to those clusters.
- Final subset annotations will later be merged back into the main AnnData object outside this annotation step.

Within each pass, follow this working order:

- Start with an overview across all clusters in the relevant object.
- Then perform cluster-by-cluster deep dives only on user cue.
- In the first pass, use the overview to propose rough identities and compartment groupings.
- In the second pass, use the overview to orient within each subset before final cluster naming.

QC review rules for both passes:

- In both phase 1 and phase 2, inspect clustering QC plots whenever they are relevant or informative.
- Use clustering QC especially for:
  - suspicious small clusters
  - clusters with high mitochondrial fraction or low complexity
  - possible doublets or mixed clusters
  - deciding whether a cluster is biologically credible or more likely technical
  - checking whether subset reclustering produced weak or unstable clusters
- Incorporate clustering QC evidence into annotation reasoning whenever it materially affects the interpretation.

Additional phase 1 QC rule:

- In phase 1, also inspect load-and-filter QC outputs to get a general sense of the dataset quality and any global limitations or biases that may affect later annotation decisions.

# Per-cluster annotation reports

Store per-cluster annotation notes in the active context `annotation/` folder.

In addition to per-cluster reports, phase 1 overview work should also be written to the active context `annotation/`.

For phase 1 overviews, create:

- one structured `.html` overview report
- one matching plain-text `.txt` overview report

These phase 1 overview reports should summarize:

- the full-cluster overview across the active dataset or active subset
- the proposed rough identity of each cluster
- the proposed compartment grouping of each cluster
- which clusters are likely already final
- which clusters should be subsetted or revisited in phase 2
- short but concrete reasoning for each cluster and compartment
- any relevant global QC context from load-and-filter or clustering QC

These overview reports should capture the same kind of high-level decision sheet that may first appear in chat, but should be saved to disk as project records.

Define this chat command for final integrated atlas reporting:

- `perform phase 3 overview`
- `generate phase 3 overview`
- `phase 3 overview`

Interpret this command as a post-merge final-atlas reporting workflow. This is not a fresh annotation pass and not a cluster deep dive. The purpose is to summarize the final integrated annotation state after subset-derived labels have been merged back into the main AnnData object and the final cluster names have already been applied.

When running a phase 3 overview:

- Use the merged main-object `adata` that contains the final merged annotation round, not the earlier pre-merge main-object file unless the user explicitly asks for that older state.
- Prefer the latest merged annotation object that corresponds to the final integrated labels and clustering visuals.
- Confirm which merged label key is active, for example a key such as `cluster_label__r4_subset_annotation`.
- Use the final merged label names exactly as stored in the merged object or as displayed in the final merged UMAP figures.
- Do not redo a full evidence-first annotation workflow unless the user explicitly asks for re-evaluation.
- Treat this as a reporting and atlas-summary task, not as an adjudication task.

Store phase 3 overview outputs in the active context `annotation/` folder.

For phase 3 overviews, create:

- one structured `.html` overview report
- one matching plain-text `.txt` overview report
- one sibling asset bundle such as `phase3_overview_assets/`

Use filenames in this style:

- `annotation/phase3_overview.html`
- `annotation/phase3_overview.txt`
- `annotation/phase3_overview_assets/`

The phase 3 overview should have a similar level of detail to phase 1, but the content goal is different.

Phase 3 overview reports should summarize:

- the final merged atlas structure after subset annotations were merged back into the main object
- the final population names exactly as they should be reported going forward
- the high-level compartment organization of the atlas
- the relative abundance of the final populations when available
- global merged-atlas QC context that helps interpret the integrated result
- concise per-population summaries written from the final names rather than from raw marker discovery
- any broad interpretive caveats about mixed borders or continuous interfaces
- a short final takeaway describing whether the merged atlas is stable and usable as the final annotation state

Phase 3 overview reports should not focus on:

- re-deriving cluster identities from raw markers
- re-litigating fine annotation choices already decided in phase 2
- building new validation panels by default
- long marker-by-marker arguments
- pseudobulk versus cell-level adjudication paragraphs for each cluster

Instead, the phase 3 overview should read like a final integrated atlas memo:

- concise
- structured
- population- and compartment-centered
- grounded in the merged object and merged figures
- explicit about the final names and atlas organization

Recommended data inputs for phase 3:

- the merged annotation `adata` object containing the final merged label key
- final merged UMAP figures
- merged cluster size plot
- merged batch composition plot
- merged silhouette plot
- merged cluster QC summary
- any final sample-overlay UMAP that helps assess mixed pockets or batch-driven artifacts

Recommended workflow for phase 3:

1. Identify the correct merged `adata` and merged label key.

- Do not assume the default main `adata` file is the correct one.
- Check whether a separate merged object exists for the final annotation round.
- Confirm that the object contains the expected merged label key and final names.

2. Identify the final merged visualization set.

- Prefer the figures produced from the merged annotation round, not the earlier phase 1 clustering figures.
- Use the final pretty UMAP and the sample-overlay UMAP as the main atlas illustrations when available.

3. Extract atlas-level summary information.

- Count cells per final population.
- If helpful, calculate percentages of the total object.
- Summarize higher-level compartments such as hepatocytes, endothelial, biliary, immune, stromal, mural, or other project-relevant branches.
- Use the merged QC figures to assess whether the final atlas looks stable and globally interpretable.

4. Write the report as a final annotation-state overview.

- Summarize the final atlas at the level of named populations and compartments.
- Use short interpretive summaries for each final population.
- Mention remaining mixed boundaries only at the level needed to guide interpretation of the final atlas.

5. Save a self-contained local report bundle.

- Copy every figure used by the HTML into `phase3_overview_assets/`.
- Use only relative asset references inside the HTML.

Recommended section order for phase 3 overview reports:

- `Phase 3 Overview`
- `Scope`
- `Global Atlas Structure`
- `Compartment Summary`
- `Global QC Context`
- `Final Population Overview`
- `Interpretive Notes`
- `Practical Takeaway`

Content expectations for each phase 3 section:

- `Scope`:
  State that this is a post-merge final-atlas report built from the merged object with final renamed populations.
  Explicitly say that the purpose is to summarize the integrated annotation state rather than to annotate from scratch.

- `Global Atlas Structure`:
  Describe the overall architecture of the final atlas.
  Name the dominant major compartments and state the total number of nuclei and final labeled populations when available.
  Mention the broad visual read of the final UMAP, especially whether the atlas looks coherent after merge-back.

- `Compartment Summary`:
  Group final populations into biologically meaningful compartments.
  For each compartment, list the final populations with final names and optionally cell counts and percentages.
  Add one short explanatory summary sentence for the compartment.

- `Global QC Context`:
  Use merged cluster-size, batch-composition, silhouette, sample-overlay, and QC-summary plots to comment on whether the final atlas is globally acceptable.
  Focus on final-atlas stability and interpretability rather than cluster-by-cluster troubleshooting.
  If mixed pockets remain, state whether they look biologically expected or technically concerning.

- `Final Population Overview`:
  Provide a concise population-by-population summary using the final cluster ids and final names.
  Each entry should be short, usually one sentence, and should describe the role of that population in the final atlas.
  Do not turn this section into a deep-dive evidence recap.

- `Interpretive Notes`:
  Record any global biological caveats such as zonation continua, expected lineage interfaces, or especially small populations that should be interpreted with caution.

- `Practical Takeaway`:
  End with a short summary paragraph explaining whether the merged atlas is stable enough to use as the final integrated annotation state.

Rules for phase 3 writing style:

- Keep the tone report-like and final-state oriented.
- Be more concise than a cluster deep-dive but more informative than a one-paragraph summary.
- Use the final names exactly and consistently.
- Prefer compartment language and atlas language over marker-discovery language.
- Avoid repeatedly saying that evidence is strong or weak unless that directly matters for interpreting the merged atlas.
- Keep mixed-boundary discussion proportional. Mention it when useful, but do not let small interface regions dominate the report.

Rules for phase 3 HTML output:

- Use the same clean single-page design language as the other reports.
- Include a strong title and clear section blocks.
- Embed the final merged atlas figures directly in the relevant sections.
- Use clickable inline images with the same lightbox behavior used in the deep-dive and phase 1 reports.
- Keep the HTML self-contained at the folder level by referencing only files inside `phase3_overview_assets/`.

Recommended phase 3 figures:

- final merged pretty UMAP with full legend
- optional short-legend variant of the same UMAP
- sample-overlay plus merged-label UMAP
- cluster sizes
- batch composition
- silhouette by cluster
- QC summary

Rules for phase 3 TXT output:

- Preserve the same section order and reasoning as the HTML report.
- Do not include links or HTML.
- Keep counts and percentages readable in plain text.

Phase 3 should usually be generated only after:

- phase 1 overview is complete
- relevant phase 2 subset deep dives are complete
- final names have been applied
- subset annotations have been merged back into the main object

If these conditions are not met, say that clearly and either:

- stop and explain what is missing, or
- generate a clearly labeled provisional phase 3 overview only if the user explicitly wants that.

For doublet QC in phase 1 overview reports:

- Do not use the per-sample doublet-fraction bar plot as a main illustrative figure when the thresholding procedure was configured to enforce a target doublet fraction.
- In that situation, prefer more informative doublet visuals such as:
  - doublet score histograms
  - doublet score ECDF plots
  - doublet score versus total counts
  - inferred threshold plots
- The goal is to illustrate doublet-score behavior and thresholding, not the enforced equality of final retained doublet fractions.

For each cluster, create these files in the active context:

- `annotation/CXX.md`: working note in Markdown with links to relevant files and figures.
- `annotation/CXX.html`: structured rendered report for browsing locally in Safari or another browser.
- `annotation/CXX.txt`: plain text version without links, suitable for TextEdit or simple reading.
- `annotation/CXX_assets/`: local asset bundle containing every figure and table copy used by the HTML report.

Use the HTML report as the main polished output. It should be self-contained at the folder level, meaning the HTML should only reference files inside its own sibling asset directory such as `C13_assets/...`, not paths elsewhere in the project. This avoids browser sandbox issues with local file rendering.

Each per-cluster report should contain these sections in this order:

- Cluster identifier
- Preferred label
- Verdict
- Marker evidence
- Specificity evidence
- Pathway and activity evidence
- Validation panel
- Naming rationale
- Literature support
- Optional clustering or QC evidence
- Optional uncertainty or next-step notes

Content expectations for each section:

- Cluster identifier:
  Include the cluster id prominently as the page title, for example `C13`.
- Preferred label:
  State the current working name in the preferred naming style, for example `PAX5+ BANK1+ Naive B cells`.
- Verdict:
  Give a concise but complete summary paragraph of the current biological interpretation.
  This section must explicitly synthesize the evidence rather than just restate the label.
  It should say what the cluster is, what the main alternative interpretations were when relevant, and why the current interpretation fits best across all evidence lines together.
- Marker evidence:
  Summarize both cell-level and pseudobulk top markers, using the actual ranked marker tables when available.
  Name the most informative ranked genes, describe the lineage or state they support, and mention disagreements between cell-level and pseudobulk evidence when relevant.
- Specificity evidence:
  Refer to dotplots, violin plots, UMAPs, and any custom panel plots to explain why the identity is specific relative to other clusters.
  Make clear whether the proposed markers are truly concentrated in the target cluster or shared with nearby states.
- Pathway and activity evidence:
  Summarize relevant MSigDB, PROGENy, and DoRothEA evidence. Treat these as supporting context rather than the main naming source.
  Explain what the pathway or TF activity adds biologically to the marker-based interpretation rather than listing terms mechanically.
- Validation panel:
  Include the exact gene list used or proposed for custom validation plots, preferably in a Python list block.
  State whether all genes plotted successfully, whether any had to be replaced, and what the resulting panel contributed to the interpretation.
- Naming rationale:
  Explain why the chosen two marker genes and descriptive phrase are appropriate.
  Connect the final name back to the earlier sections and justify both the marker pair and the descriptive wording.
- Literature support:
  Include 2 to 3 references with citation name, year, and DOI.
  State briefly what each reference supports.
- Optional clustering or QC evidence:
  Use this section when clustering QC materially affects the interpretation, for example for high-mito clusters, tiny clusters, poor silhouette support, single-sample clusters, likely contaminants, or possible doublets.
  Place this section near the top of the report when it is central to the verdict.
- Optional uncertainty or next-step notes:
  Note ambiguity, conflicting evidence, or follow-up plots that would help resolve the identity.

Deep-dive reports should follow a polished cluster-note structure.
They should read like polished scientific annotation notes, with each evidence type in its own clearly labeled section and with enough descriptive text that the reasoning is understandable without needing chat history.
Do not jumble markers, specificity, pathways, validation, and naming rationale into one mixed paragraph.

Deep-dive reports are not the same as phase 1 overview reports.
Use a true cluster-note style, not the more summary-like overview structure used in phase 1 reports.
When in doubt, follow the portable examples in:
- `templates/report_templates/deep_dive_template.html`
- `templates/report_templates/deep_dive_template.txt`

For deep-dive reports, the section headers should closely follow this wording:

- `Preferred Label`
- `Verdict`
- `Marker Evidence`
- `Specificity Evidence`
- `Pathway And Activity Evidence`
- `Validation Panel`
- `Naming Rationale`
- `Literature Support`

If clustering or QC evidence is central to the interpretation, add a clearly labeled `Clustering And QC Evidence` section near the top, before the biological evidence sections.

Expected level of detail for deep-dive reports:

- `Preferred Label`:
  Very short. Just the chosen final label in prominent form.
- `Verdict`:
  One concise but substantive paragraph.
  It should state the favored identity, the main rejected alternatives when relevant, and the overall conclusion from the combined evidence.
- `Marker Evidence`:
  Usually 1 to 2 paragraphs.
  One paragraph should cover cell-level markers and one should cover pseudobulk markers when both are informative.
  Use actual marker names and explain what they imply biologically.
- `Specificity Evidence`:
  At least one short paragraph plus the key dotplot or violin figures.
  Explain whether the marker program is concentrated in the cluster or shared with nearby clusters.
- `Pathway And Activity Evidence`:
  Usually one paragraph.
  Explain how MSigDB, DoRothEA, and PROGENy support, refine, or fail to support the marker-based interpretation.
  Do not just enumerate pathway names.
- `Validation Panel`:
  Include the exact Python list.
  State whether all genes plotted successfully, whether replacements were needed, and what the panel showed biologically.
  This should usually be one short paragraph before the figures and one short paragraph after if interpretation needs emphasis.
- `Naming Rationale`:
  Usually a short paragraph or short bullet list.
  Explain why the exact two markers and descriptive phrase are the best final wording.
- `Literature Support`:
  Include 2 to 3 references with citation name, year, and DOI, plus a short sentence or follow-up paragraph explaining what they support in the current label.

In other words, deep-dive reports should feel like readable mini-annotation memos:
- not just a checklist
- not just a dump of plots
- not a phase 1 overview table
- but a structured argument leading from evidence to label

For phase 1 overview reports, use the portable examples in:
- `templates/report_templates/phase1_overview_template.html`
- `templates/report_templates/phase1_overview_template.txt`
- For working execution, also use:
  - `templates/report_templates/subset_phase1_checklist.txt`

Very important:

- The final conclusion must be synergized across all evidence lines.
- Do not treat markers, specificity plots, pathway scores, custom panels, literature, and clustering QC as separate disconnected votes.
- The verdict and naming rationale should explicitly integrate the evidence into one coherent biological interpretation.
- If the evidence conflicts, say so clearly and explain why one interpretation is favored or why the cluster should remain provisional.

Rules for the HTML report:

- Use a clean, readable single-page layout with light background, dark text, bordered content sections, and restrained styling.
- Use short section headers and a strong title at the top.
- Use inline code formatting for gene symbols.
- Include clickable links to local copied assets in the `CXX_assets/` folder.
- Embed small inline image panels directly in the relevant sections so that the text and evidence are visible together.
- Every embedded image should be clickable and open a larger rendered overlay in the same tab.
- The overlay should have a visible close button with `x`, and should also close when clicking the dark background or pressing `Esc`.
- Keep the page compact enough to browse, but large figures should still be readable when opened in the overlay.

HTML structure should follow this pattern closely:

- `<!DOCTYPE html>` page with a small inline `<style>` block and a small inline `<script>` block.
- One main container centered on the page.
- Multiple bordered `<section>` blocks, one per logical report section.
- A reusable gallery layout implemented with a simple CSS grid.
- Each image inside a `<figure>` with `<img class="thumb">` and a `<figcaption>`.
- One hidden lightbox container near the end of the body:
  - outer overlay div
  - inner wrapper
  - close button
  - one `<img>` element whose `src` and `alt` are updated by JavaScript
- JavaScript should:
  - register click handlers on `.thumb`
  - copy the clicked image source into the lightbox image
  - open the overlay
  - close on close-button click
  - close on background click
  - close on `Escape`

Rules for the TXT report:

- No links.
- No HTML.
- Preserve the same section order and core reasoning as the HTML report.
- Keep it readable in monospaced or plain editors.

Rules for the asset bundle:

- Copy every figure and table referenced by the HTML into the matching cluster asset folder.
- Prefer descriptive filenames if renaming avoids collisions, for example `pseudobulk_dotplot_C13_Naive_B_cells.png`.
- Keep the HTML references relative, such as `C13_assets/...`.

# Custom gene panel plotting workflow

Custom validation gene panels should default to the reusable plotting script skeleton unless the local project override specifies a different plotting entrypoint.

If `project-local.md` names a preferred notebook or plotting entrypoint, use that as the project-specific starting point.

A suitable plotting workflow should be able to generate:

- dotplots
- violin grids
- UMAP feature grids

using a custom gene list and saving the outputs into the active context `panels/`.

Portable panel templates are available in:

- `templates/report_templates/panel_plot_template.py`
- `templates/report_templates/panel_gene_list_template.txt`

Because `scOmnom` AnnData objects are often large, do not start a fresh Python process for every cluster panel. Instead, use one persistent Python session per working block when panel plotting is available:

- Start one long-lived shell session in `scOmnom_env`.
- Load the AnnData object once.
- Reuse the same in-memory `adata` for all subsequent panel plotting requests.
- Only change the gene list and output filenames between panels.

Persistent session setup should follow this pattern:

- Shell: source Conda with the appropriate local Conda setup if needed.
- Activate environment: `conda activate scOmnom_env`
- Always set writable cache directories before importing `scanpy`, `scomnom`, or related plotting libraries:
  - `NUMBA_CACHE_DIR=/tmp/numba_cache`
  - `MPLCONFIGDIR=/tmp/matplotlib_cache`

In the persistent Python session:

- Import `scanpy` and `scomnom` only after the cache variables above are set
- Load the active context marker-stage `adata` once with `om.load_dataset(...)`
- Reuse helper functions equivalent to:
  - grouping-key inference
  - `ensure_umap(adata)`

Preferred plotting workflow:

- Make a dedicated output directory under `panels/` for test or cluster-specific outputs when useful.
- Use the same three plotting functions already present in the notebook:
  - `om.plotting.plot_de_dotplot_top_genes(...)`
  - `om.plotting.plot_de_violin_grid_genes(...)`
  - `om.plotting.plot_de_umap_features_grid(...)`
- Follow `templates/report_templates/panel_plot_template.py` as the default code skeleton for reusable panel generation.
- Use `templates/report_templates/panel_gene_list_template.txt` as the default working template for recording proposed genes, replacements, and final accepted panels when helpful.

If a persistent session has already successfully loaded `adata`, prefer reusing it rather than relaunching Python. Only restart the session if the kernel crashes, the environment changes, or memory becomes an issue.

Define these chat commands for panel plotting workflow control:

- `start panel session`
- `stop panel session`

Interpret them as follows:

- If the user says `start panel session`, open or refresh the persistent Python session for panel plotting in `scOmnom_env`, using the persistent-session workflow above.
- If the user says `stop panel session`, cleanly terminate the persistent Python session used for panel plotting.

From this point onward, whenever the user asks to plot custom panel genes, use this persistent panel-session mechanism rather than launching one-off plotting processes, unless that mechanism is unavailable or has failed and needs recovery.

Define this chat command for cluster deep-dive annotation:

- `Annotate cluster Cnn`
- `Annotate clusters Cnn, ..., Ckk`

Interpret this command as a full annotation workflow for the requested cluster or clusters. When this command is given, do the following for each requested cluster:

Use these portable working templates as defaults during execution:

- `templates/report_templates/deep_dive_template.html`
- `templates/report_templates/deep_dive_template.txt`
- `templates/report_templates/deep_dive_checklist.txt`
- `templates/report_templates/panel_plot_template.py`
- `templates/report_templates/panel_gene_list_template.txt`

1. Review the marker evidence:

- Analyze both cell-level and pseudobulk marker tables.
- Inspect marker specificity in dotplots and violin plots.

2. Review pathway and activity evidence:

- Inspect MSigDB enrichments.
- Inspect DoRothEA TF activity.
- Inspect PROGENy pathway activity.

3. Form an annotation verdict:

- Combine marker, specificity, pathway and activity evidence, custom panel evidence, literature support, and QC context when relevant into one naming decision.
- Propose a new name following the required pattern:
  - two marker genes plus a short descriptive label
  - example style: `PAX5+ BANK1+ Naive B cells`
- The verdict must be a synthesized interpretation derived jointly from all relevant evidence lines, not a list of separate mini-conclusions.

4. Write explicit reasoning:

- Give a concise but thorough explanation of the naming choice.
- Point to concrete evidence, not vague impressions.
- Refer to the exact supporting markers, pathway terms, and specificity observations.

5. Look for literature support:

- For each cluster, identify 2 or 3 literature references that support the annotation decision.
- For each reference, record:
  - first author or short citation name
  - year
  - DOI
- It is acceptable and encouraged to reuse the same references across multiple clusters when they are broadly relevant and genuinely supportive.
- Prefer reusable references when appropriate, such as immune cell atlases, adipose tissue atlases, vascular/stromal references, or anatomy papers that support several identities in the dataset.

6. Propose a 9-gene validation panel:

- Suggest a focused 9-gene panel that can defend the naming decision visually.
- The panel should include strong identity markers and, where helpful, discriminating genes that could falsify the current hypothesis.
- In phase 2 deep dives, do not assume a single panel is always enough.
- When a cluster could plausibly be explained by several well-described state programs, it is encouraged to design multiple targeted panels and compare them.
- Typical examples include helper, memory, cytotoxic, regulatory, exhausted, Tem, Trm, Temra, NK, activated, inflammatory, APC-like, scavenging, or lipid-associated programs.
- Use extra panels when they materially clarify the state decision rather than treating them as optional decoration.

7. Plot the panel genes using the persistent panel-session mechanism:

- Use the persistent Python session in `scOmnom_env`.
- Plot the panel genes with `scomnom` into the `panels/` directory.
- Generate at least:
  - dotplot
  - violin grid
  - UMAP feature grid
- If multiple custom panels are appropriate, plot all of them through the same persistent session and keep their outputs organized in the relevant `panels/` location.

8. Validate that all genes plotted successfully:

- Check whether every requested gene was present in the AnnData object.
- If one or more genes failed because they are absent from the dataset, replace the missing genes with suitable alternatives and replot.
- Repeat until all 9 genes plot successfully.

9. Reassess the hypothesis after seeing the custom panel:

- Inspect the generated panel plots directly.
- Decide whether the custom panel supports the current naming decision.
- If the panel weakens the current interpretation, set a revised identity hypothesis.
- If needed, design and plot a new validation panel.
- When multiple panels were generated, compare them jointly and use them together in the final reasoning.
- In these cases, the report should explain which panel contributed which part of the interpretation.
- Iterate until the evidence and the proposed label are consistent and satisfactory.

10. Write the final annotation report:

- Save the final decision transcript in the `annotation/` folder.
- Produce the established output set:
  - `CXX.md`
  - `CXX.html`
  - `CXX.txt`
  - `CXX_assets/`
- The report should capture the final verdict and the supporting evidence clearly.
- The HTML and TXT outputs should follow the existing report conventions defined above.
- The report should closely follow:
  - `templates/report_templates/deep_dive_template.html`
  - `templates/report_templates/deep_dive_template.txt`
- Include the selected literature references in the final report with citation name, year, and DOI.

This command should be treated as an end-to-end annotation task, not just a quick opinion. The workflow should continue through marker review, pathway review, validation plotting, iterative refinement if needed, and report writing until a satisfactory cluster annotation is reached.
