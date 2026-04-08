# Purpose

Version: `0.3.0`

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
- any additional renamed annotation layers present in the merged object, such as archetype, compartment, or supercompartment layers
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

Additional phase 3 layer rule:

- Check whether the final merged object contains additional renamed annotation layers beyond the main final label layer, for example archetype, compartment, supercompartment, or other user-defined categorical layers in `adata.obs`.
- If such extra layers exist and are clearly intended as annotation layers, include them in the phase 3 overview.
- For each extra layer, summarize the layer name, the number of unique labels, the labels themselves when the count is manageable, and cell counts and percentages per label when useful.
- Before generating new UMAPs for an extra layer, first inspect the figure tree for existing outputs, especially `rename_roundN/` folders or similar rename-layer plotting outputs.
- Only generate fresh categorical UMAPs for extra layers when suitable figures are missing or when the user explicitly asks for regeneration.

Recommended workflow for phase 3:

1. Identify the correct merged `adata` and merged label key.

- Do not assume the default main `adata` file is the correct one.
- Check whether a separate merged object exists for the final annotation round.
- Confirm that the object contains the expected merged label key and final names.

2. Identify the final merged visualization set.

- Prefer the figures produced from the merged annotation round, not the earlier phase 1 clustering figures.
- Use the final pretty UMAP and the sample-overlay UMAP as the main atlas illustrations when available.
- Also inspect whether there are existing `rename_roundN/` or comparable rename-layer figure outputs that already visualize additional label layers.
- Reuse those existing rename-layer figures when they match the current extra layers instead of regenerating them manually.

3. Extract atlas-level summary information.

- Count cells per final population.
- If helpful, calculate percentages of the total object.
- Summarize higher-level compartments such as hepatocytes, endothelial, biliary, immune, stromal, mural, or other project-relevant branches.
- Use the merged QC figures to assess whether the final atlas looks stable and globally interpretable.
- If extra annotation layers exist, also count cells per extra-layer label and summarize those higher-abstraction layers alongside the granular final populations.

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
- `Additional Annotation Layers`
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

- `Additional Annotation Layers`:
  If extra renamed categorical layers exist, summarize them here.
  State the layer names, the number of labels in each layer, and what level of abstraction they represent.
  If existing rename-layer UMAPs are available, include them here.
  If no extra layers are present, this section can be omitted.

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
- If extra-layer UMAPs already exist in the figure tree, embed those too in the `Additional Annotation Layers` section.
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

Define these chat commands for atlas-level DE reporting:

- `perform phase 4 de overview`
- `generate phase 4 de overview`
- `phase 4 de overview`

Interpret these commands as a contrast-centric differential-expression overview workflow. The purpose is to summarize one DE run across the atlas, identify where signal is strongest, describe where signal is weak or skipped, and decide which clusters deserve phase 5 deep dives.

When running a phase 4 DE overview:

- Identify the correct DE-enabled object and the correct DE result tree for the active context.
- Confirm the active annotation layer or round that the DE run is based on, for example `r4_subset_annotation` or `r5_archetypes`.
- Confirm the exact contrast key and contrast pair under review.
- Use `scOmnom` contrast-key semantics when interpreting the run:
  - `A:B` means a composite condition key built from multiple `adata.obs` factors and is typically resolved internally to `A.B`.
  - `A@B` means compare `A` within levels of `B`.
  - `A^B` means a true interaction contrast.
  - Dotted keys such as `sex.masld_status` often represent resolved composite keys created from colon input such as `sex:masld_status`.
- Explain contrast names by their biological meaning, not just their folder names.
- Treat this as a reporting and prioritization task, not as a rerun of DE testing.

Store phase 4 DE overview outputs in the active context `annotation/phase4/` folder.

For phase 4 DE overviews, create:

- one structured `.html` overview report
- one matching plain-text `.txt` overview report
- one sibling asset bundle such as `de_phase4_<run_id>_assets/`

Use filenames in this style:

- `annotation/phase4/de_phase4_<run_id>.html`
- `annotation/phase4/de_phase4_<run_id>.txt`
- `annotation/phase4/de_phase4_<run_id>_assets/`

The phase 4 DE overview should summarize:

- the DE scope, including annotation layer, contrast key, and contrast pair
- run settings that materially affect interpretation
- which DE evidence sources are available:
  - `cell_based/`
  - `pseudobulk_DE/`
- which clusters were testable, skipped, or weakly powered
- where the strongest DE signal sits across the atlas
- whether the signal is concentrated in a few compartments or distributed broadly
- whether gene-level and pathway/regulator signals agree
- which clusters should be prioritized for phase 5 deep dives
- any global caveats such as interaction-only contrasts, sparse replicate support, or inflation-prone cell-level-only evidence

Phase 4 reports should not:

- restate every per-cluster result in equal detail
- rerun DE by default
- treat cell-level p-values as gold-standard evidence when pseudobulk is available
- describe pathway outputs as long unranked term dumps

Instead, phase 4 should read like an atlas-level DE triage memo:

- concise
- contrast-centered
- explicit about evidence source availability
- clear about where the real biology appears to be
- clear about what deserves deeper review

DE evidence-source rules:

- Always check whether both `cell_based/` and `pseudobulk_DE/` result trees are present for the requested run.
- If only `cell_based/` exists, use it and say clearly that replicate-aware pseudobulk evidence is unavailable.
- If both `cell_based/` and `pseudobulk_DE/` exist, use both throughout the report.
- Treat pseudobulk DE as the preferred inferential framework when replicate-aware results are available.
- Treat cell-level ranksum or logistic-regression DE as supportive and potentially inflation-prone because large cell counts can drive very small p-values.
- When both sources are present:
  - weight pseudobulk more heavily for significance and robustness
  - use cell-level results mainly for expression prevalence, within-cluster distribution, and direction consistency
  - describe concordance as a confidence booster
  - describe discordance explicitly rather than smoothing it over
- Do not silently privilege cell-level significance over weaker or absent pseudobulk evidence.
- For interaction contrasts, expect pseudobulk to be especially important because cell-level interaction contrasts may be skipped.

Recommended data inputs for phase 4:

- DE settings file for the requested contrast key
- `__summary.csv` from `cell_based/` when available
- `__summary.csv` from `pseudobulk_DE/` when available
- selected per-cluster `combined.csv` tables for spot checks
- existing DE figures:
  - condition or contrast UMAPs
  - volcano plots
  - dotplots
  - sample heatmaps
  - decoupler outputs for DoRothEA, MSigDB, and PROGENy

Additional phase 4 plotting and query rule:

- Reuse existing pipeline figures first.
- If the figure tree is insufficient to answer the interpretive question, generate targeted additional plots through the `scomnom` plotting API.
- Suitable extra plots include contrast-split expression UMAPs, contrast-split violins, and targeted dotplots for selected genes.
- Extra plots should be hypothesis-driven and used selectively.
- If tables are insufficient, query the DE-enabled `adata` object directly in Python for targeted supporting summaries such as:
  - per-group cell counts
  - fraction expressing
  - per-sample spread
  - prevalence asymmetry
- Prefer lightweight targeted summaries rather than building a second analysis pipeline.

Recommended section order for phase 4 DE overview reports:

- `Phase 4 DE Overview`
- `Scope`
- `Run Settings`
- `Atlas-Level DE Summary`
- `Coverage And Skip Summary`
- `Differential Abundance Overview`
- `Strongest Responding Clusters`
- `Weak Or Ambiguous Clusters`
- `Pathway And Regulator Overview`
- `Priority Shortlist For Phase 5`
- `Practical Takeaway`

Content expectations for each phase 4 section:

- `Scope`:
  State the active context, annotation layer, DE round, contrast key, and selected contrast.
  Explain the biological meaning of the contrast using the correct `scOmnom` condition-key semantics.

- `Run Settings`:
  Summarize only the DE settings that materially affect interpretation, such as engine, methods, minimum cell thresholds, explicit contrasts, and whether pseudobulk was run.

- `Atlas-Level DE Summary`:
  Describe the overall amplitude and distribution of DE signal across the atlas.
  State whether the contrast appears strong, focal, diffuse, or weak.

- `Coverage And Skip Summary`:
  Summarize which clusters were tested successfully, skipped, or limited by low counts or low replicate support.
  Use summary tables directly and be explicit about why clusters were skipped.

- `Differential Abundance Overview`:
  If DA outputs are available for the same layer and condition key, summarize whether any populations show credible abundance shifts.
  Use the DA consensus table as the main backbone and explain whether DA is absent, weak, focal, or broad.
  Highlight whether the contrast appears dominated by transcriptional state change, abundance change, or both.

- `Strongest Responding Clusters`:
  Highlight only the most compelling clusters.
  Prefer clusters that have coherent biology and, when available, pseudobulk support.

- `Weak Or Ambiguous Clusters`:
  Highlight clusters where signal is weak, inflated-looking, discordant between sources, or too underpowered for confidence.

- `Pathway And Regulator Overview`:
  Summarize broad pathway and regulator patterns across the atlas.
  Focus on agreement with the gene-level story and on compartment-level themes.

- `Priority Shortlist For Phase 5`:
  Name the best next deep-dive targets and explain why each one is worth a cluster-level report.

- `Practical Takeaway`:
  End with a short summary paragraph that says whether the contrast yielded a useful atlas-level biological story and where the trustworthy signals sit.

Rules for phase 4 writing style:

- Keep the report contrast-centered and atlas-level.
- Prioritize interpretive clarity over exhaustiveness.
- Be explicit about whether conclusions are based on cell-level only, pseudobulk only, or concordant across both.
- Avoid overstating significance when the evidence is cell-level-only.
- When DA is available, explain clearly whether the contrast is mainly a state-change story, an abundance-change story, or a combination of both.
- If DA is available but non-significant, say that explicitly rather than leaving the reader to infer it.

Rules for phase 4 HTML output:

- Use the same clean single-page design language as the phase 1, phase 3, and deep-dive reports so outputs look consistent across projects.
- Use bordered section blocks, inline galleries, and clickable lightbox-style figures.
- Keep the HTML self-contained at the folder level by referencing only files inside the local asset folder.

Rules for phase 4 TXT output:

- Preserve the same section order and reasoning as the HTML report.
- Do not include links or HTML.
- Keep tables or count summaries readable in plain text.

Define these chat commands for cluster-level DE reporting:

- `perform phase 5 de report`
- `generate phase 5 de report`
- `phase 5 de report`
- `perform phase 5 de reports on Cnn, ..., Ckk`

Interpret these commands as cluster-and-contrast differential-expression deep dives. The purpose is to explain what changes in one specified cluster for one specified contrast, weigh the evidence across available DE sources, and produce a readable cluster-level DE memo.

Store phase 5 DE outputs in the active context `annotation/phase5/` folder.

For phase 5 DE reports, create:

- one structured `.html` report
- one matching plain-text `.txt` report
- one matching `.md` report
- one sibling asset bundle such as `de_phase5_<run_id>_<cluster>_assets/`

Use filenames in this style:

- `annotation/phase5/de_phase5_<run_id>_<cluster>.html`
- `annotation/phase5/de_phase5_<run_id>_<cluster>.txt`
- `annotation/phase5/de_phase5_<run_id>_<cluster>.md`
- `annotation/phase5/de_phase5_<run_id>_<cluster>_assets/`

Phase 5 reports should answer:

- what changes in this cluster for the requested contrast
- how strong and credible the evidence is
- whether pseudobulk and cell-level evidence agree
- whether the cluster also shows any differential abundance signal for the same contrast
- which genes are higher in A and which are higher in B
- whether pathway and regulator shifts support the gene-level story
- whether the result looks biologically interpretable, weak, or potentially technical

Recommended evidence hierarchy for phase 5:

1. Pseudobulk DE, when available, as the preferred inferential backbone.
2. The combined per-cluster DE table as the main cross-method summary.
3. Differential abundance evidence for the same cluster and contrast, when available, as supporting context for whether the signal reflects state change, abundance change, or both.
4. Cell-level DE for prevalence, direction, and shape of expression changes.
5. Pathway and regulator outputs as a biological coherence layer.
6. Extra targeted plotting or direct `adata` summaries only when needed to resolve ambiguity.

Recommended section order for phase 5 DE reports:

- `Phase 5 DE Report`
- `Contrast Definition`
- `Verdict`
- `Testability And QC Context`
- `Differential Abundance Context`
- `Gene-Level DE Summary`
- `Method And Source Agreement`
- `Pathway And Activity Evidence`
- `Contrast-Specific Validation Plots`
- `Interpretation`
- `Caveats Or Next-Step Notes`

Content expectations for each phase 5 section:

- `Contrast Definition`:
  State the cluster, annotation layer, contrast key, and A-versus-B pair.
  Explain the biological meaning of the contrast using the correct `scOmnom` syntax interpretation.

- `Verdict`:
  Give a concise but substantive summary of what the contrast appears to be doing in this cluster.
  Explicitly say whether the conclusion is pseudobulk-backed, cell-level-only, or discordant across sources.

- `Testability And QC Context`:
  Summarize per-group cell counts, replicate support when available, and any QC limitations that materially affect the DE interpretation.

- `Differential Abundance Context`:
  If DA outputs are available for the same layer and contrast, summarize whether this population also changes in relative abundance.
  State the DA direction when relevant and whether the DA evidence is significant, weak, or absent.
  Use this section to clarify whether the cluster primarily shows transcriptional state change, abundance change, or both.

- `Gene-Level DE Summary`:
  Summarize the main up-in-A and up-in-B programs using the combined table as the backbone.
  Prefer coherent gene programs over long lists.

- `Method And Source Agreement`:
  Compare `combined.csv`, method-specific tables, and pseudobulk evidence when present.
  If cell-level significance is strong but pseudobulk is weak or absent, call that out explicitly as inflation-prone or provisional.

- `Pathway And Activity Evidence`:
  Explain how DoRothEA, MSigDB, and PROGENy support or complicate the gene-level readout.
  Focus on biological interpretation, not term enumeration.

- `Contrast-Specific Validation Plots`:
  Reuse existing cluster-level volcanoes, dotplots, violins, heatmaps, and decoupler figures first.
  If needed, add targeted extra plots through the `scomnom` plotting API, including contrast-split gene views.

- `Interpretation`:
  Provide a short integrative paragraph that explains what the cluster seems to be doing biologically in this contrast.

- `Caveats Or Next-Step Notes`:
  Use when the signal is weak, technically suspect, or would benefit from targeted follow-up.

Rules for phase 5 writing style:

- Keep the report cluster-centered and contrast-centered.
- Use effect direction explicitly.
- Do not let inflated cell-level p-values become the sole basis for a strong conclusion when pseudobulk is available.
- If the result is weak or provisional, say so plainly.
- When DA is available, integrate it into the interpretation explicitly.
- Prefer clear statements such as:
  - the cluster changes transcriptionally without detectable abundance change
  - the cluster shows both transcriptional remodeling and abundance expansion
  - the main difference is compositional rather than transcriptional

Portable DE report templates are available in:

- `templates/report_templates/de_phase4_overview_template.html`
- `templates/report_templates/de_phase4_overview_template.txt`
- `templates/report_templates/de_phase5_report_template.html`
- `templates/report_templates/de_phase5_report_template.txt`
- `templates/report_templates/de_phase6_synthesis_template.html`
- `templates/report_templates/de_phase6_synthesis_template.txt`
- `templates/report_templates/de_phase7_master_synthesis_template.html`
- `templates/report_templates/de_phase7_master_synthesis_template.txt`

Use these templates as the default baseline for DE report structure so reports remain stylistically consistent across projects.

Define these chat commands for cross-layer DE synthesis reporting:

- `perform phase 6 de synthesis`
- `generate phase 6 de synthesis`
- `phase 6 de synthesis`
- `perform phase 6 de overview`
- `generate phase 6 de overview`
- `phase 6 de overview`

Interpret these commands as a final contrast-level DE synthesis workflow analogous to the phase 3 annotation overview. The purpose is to integrate the main conclusions from the relevant phase 4 and phase 5 reports for one selected contrast, summarize the cross-compartment biological story, and explain how that story resolves across multiple annotation layers when such layers are available.

When running a phase 6 DE synthesis:

- Identify the requested contrast key and exact A-versus-B contrast.
- Identify every relevant DE-enabled annotation layer available in the active context, for example `r4_subset_annotation`, `r5_archetypes`, `r6_compartment`, or finer subset DE layers.
- Treat phase 6 as a synthesis task built on top of earlier reports, not as a replacement for them.
- Use the corresponding phase 4 report for each relevant layer as the atlas-level backbone.
- Use the corresponding phase 5 reports for the shortlist clusters as the cluster-level detail layer.
- If the needed phase 4 or phase 5 reports do not yet exist, generate them first before writing phase 6.
- Re-open the underlying DE tables and figure trees when needed to verify or refine the synthesis rather than copying report language blindly.
- Use the final annotation hierarchy, including phase 3 outputs and any rename layers, to relate broad and fine compartments correctly.
- Explain contrast names by their biological meaning using the correct `scOmnom` condition-key semantics.

Store phase 6 DE synthesis outputs in the active context `annotation/phase6/` folder.

For phase 6 DE synthesis reports, create:

- one structured `.html` synthesis report
- one matching plain-text `.txt` synthesis report
- one sibling asset bundle such as `de_phase6_<run_id>_assets/`

Use filenames in this style:

- `annotation/phase6/de_phase6_<run_id>.html`
- `annotation/phase6/de_phase6_<run_id>.txt`
- `annotation/phase6/de_phase6_<run_id>_assets/`

The phase 6 DE synthesis should summarize:

- the selected contrast and the layers included in the synthesis
- the main atlas-level DE story for that contrast
- which broad compartments show signal
- which fine-grained populations drive, refine, or contradict the broad signal
- how concordant the story is across annotation layers
- whether the result points to identifiable biological processes such as inflammation, bile-acid handling, scavenging identity, stress, remodeling, or metabolic reprogramming
- which custom process panels were generated and why
- the final integrated biological interpretation for the contrast
- the overall confidence level based on pseudobulk availability, cell-level-only limitations, and cross-layer agreement

Phase 6 reports should not:

- repeat every phase 4 and phase 5 paragraph in full
- devolve into a long list of cluster summaries
- treat coarse and fine annotation layers as independent unrelated analyses
- assert a broad process label such as inflammation or bile-acid transport without checking whether the gene-level evidence supports it

Instead, phase 6 should read like a final DE memo for one contrast:

- synthesis-centered
- biologically interpretable
- explicit about broad-to-fine lineage resolution
- explicit about evidence strengths and limitations
- more concise than the total set of phase 4 and phase 5 reports it summarizes

Recommended data inputs for phase 6:

- the relevant phase 4 DE overview reports for the requested contrast across available layers
- the relevant phase 5 DE reports for priority clusters across available layers
- the matching DE settings files and `__summary.csv` tables
- selected underlying `combined.csv` cluster tables for spot checks
- phase 3 overview outputs and any active label-hierarchy layers
- existing DE figures and decoupler outputs
- direct `adata` queries when needed for supporting counts, prevalence, or cross-layer mapping checks

Cross-layer synthesis rules:

- Always ask whether the same biological signal is visible at more than one annotation resolution.
- If a broad layer shows a signal and a finer layer resolves it into one or a few driving populations, say that explicitly.
- If a broad signal disappears after splitting, say that explicitly and interpret whether that means dilution, heterogeneity, or loss of power.
- If finer layers disagree with the broad layer, explain whether the disagreement is biological, statistical, or technical.
- Prefer statements of the form:
  - broad compartment summary
  - finer driver populations
  - whether the broad story survives refinement
- Good synthesis language includes examples such as:
  - a macrophage signal at the archetype level is mainly driven by recruited macrophages rather than resident Kupffer cells
  - a broad endothelial signal is preserved specifically in sinusoidal endothelial cells and not in vascular endothelial cells

Phase 6 process-panel rule:

- If phase 4 and phase 5 jointly suggest a coherent process such as inflammation, bile-acid transport, complement handling, endothelial activation, scavenging identity, stress, or remodeling, create at least one targeted custom panel for that process.
- Prefer genes that are both:
  - biologically central to the inferred process
  - present in the significant DE signal when possible
- If the core process genes are not all present among the strongest DE hits, it is acceptable to supplement with canonical process genes.
- Use the `scomnom` plotting API to generate contrast-aware custom plots when possible.
- Prefer targeted plots that clarify the synthesis, for example:
  - contrast-split expression UMAPs
  - contrast-split violins
  - targeted dotplots across the driving clusters or layers
- Keep custom panels hypothesis-driven and limited to the processes actually discussed in the report.

Recommended section order for phase 6 DE synthesis reports:

- `Phase 6 DE Synthesis`
- `Scope`
- `Available Layers And Evidence`
- `Cross-Layer DE Summary`
- `Compartment-Level Themes`
- `Layer-Resolved Drivers`
- `Process Panels`
- `Integrated Interpretation`
- `Confidence And Caveats`
- `Practical Takeaway`

Content expectations for each phase 6 section:

- `Scope`:
  State the active context, the selected contrast, and the layers being synthesized.
  Explain the contrast biologically using the correct `scOmnom` contrast semantics.

- `Available Layers And Evidence`:
  Summarize which phase 4 and phase 5 reports were used, which DE sources exist, and whether pseudobulk support is available anywhere in the synthesis.

- `Cross-Layer DE Summary`:
  Give the short atlas-level story for the contrast and say whether it is broad, focal, or weak.

- `Compartment-Level Themes`:
  Summarize the main biological themes by broad compartment, such as parenchymal, immune, endothelial, biliary, or stromal.

- `Layer-Resolved Drivers`:
  Explain which finer populations are driving the broad signals and which broad effects disappear or sharpen after refinement.

- `Process Panels`:
  Describe the targeted custom panels that were generated, why those genes were chosen, and what they show about the inferred biological process.

- `Integrated Interpretation`:
  Provide a synthesis paragraph that turns the broad-to-fine signal into one coherent biological readout for the contrast.

- `Confidence And Caveats`:
  State whether the synthesis is supported by pseudobulk, by cell-level-only evidence, by cross-layer agreement, or by targeted panels.
  Be explicit about inflation risk, sparse subclusters, or mixed programs when relevant.

- `Practical Takeaway`:
  End with a concise statement of the final biological message for the contrast and which populations matter most.

Rules for phase 6 writing style:

- Write phase 6 as a synthesis memo, not as another raw DE screen.
- Prefer cross-layer biological claims over cluster-by-cluster recitation.
- Use explicit broad-to-fine language.
- Be cautious about process naming unless the gene-level evidence and custom panels support it.
- Treat pseudobulk-supported conclusions as stronger than cell-level-only conclusions.

Rules for phase 6 HTML output:

- Use the same clean single-page design language as the phase 3, phase 4, and phase 5 reports so outputs look consistent across projects.
- Use bordered sections, inline galleries, and local copied assets only.
- Copy every figure used by the HTML into `de_phase6_<run_id>_assets/`.

Rules for phase 6 TXT output:

- Preserve the same section order and synthesis logic as the HTML report.
- Keep the prose readable without links or HTML.
- Refer to custom panels clearly in text so the reasoning remains understandable even without the figures.

Use these templates as the default baseline for dataset-level biological synthesis reports:

- `templates/report_templates/de_phase7_master_synthesis_template.html`
- `templates/report_templates/de_phase7_master_synthesis_template.txt`

Define these chat commands for final project-level biological synthesis reporting:

- `perform phase 7 synthesis`
- `generate phase 7 synthesis`
- `phase 7 synthesis`
- `perform phase 7 biological synthesis`
- `generate phase 7 biological synthesis`
- `phase 7 biological synthesis`
- `perform phase 7 overview`
- `generate phase 7 overview`
- `phase 7 overview`

Interpret these commands as the final project-level biological synthesis workflow. The purpose is to integrate the main conclusions from the annotation phases and the DE phases into one succinct, dataset-wide memo that explains what biological changes are present overall. Unlike phase 6, which is still one-contrast-at-a-time, phase 7 should bring the full project together into one coherent narrative.

When running a phase 7 synthesis:

- Treat phase 7 as a synthesis task built on top of earlier reports, not as a replacement for them.
- Use the final annotation hierarchy from phase 3 as the atlas backbone.
- Use phase 4, phase 5, and phase 6 reports as the DE and DA evidence backbone.
- If essential phase 3, phase 4, phase 5, or phase 6 reports do not yet exist, generate the missing prerequisites first.
- Re-open the underlying annotation, DE, and DA tables when needed to verify the high-level synthesis rather than copying report language blindly.
- Explain the study design explicitly when it matters for interpretation, for example baseline predictive contrasts versus post-intervention mechanistic contrasts.
- Integrate broad and fine annotation layers explicitly when both are available.
- Summarize both what changes and what does not change.
- Be explicit about whether the project-level story is dominated by transcriptional state change, abundance change, or both.
- Use targeted custom process panels when needed to sharpen a project-level biological conclusion.

Store phase 7 synthesis outputs in the active context `annotation/phase7/` folder.

For phase 7 synthesis reports, create:

- one structured `.html` synthesis report
- one matching plain-text `.txt` synthesis report
- one sibling asset bundle such as `de_phase7_master_synthesis_assets/`

Use filenames in this style:

- `annotation/phase7/de_phase7_master_synthesis.html`
- `annotation/phase7/de_phase7_master_synthesis.txt`
- `annotation/phase7/de_phase7_master_synthesis_assets/`

The phase 7 synthesis should summarize:

- the study design and what each major contrast means biologically
- the final atlas structure and main annotated compartments
- the strongest biological changes seen across the full project
- which findings look most predictive at baseline when relevant
- which findings look most mechanistic after intervention or over time when relevant
- which broad compartment signals resolve into specific finer driver populations
- whether the dominant changes are transcriptional state changes, abundance changes, or both
- which signals remain weak, absent, or unconvincing
- which targeted custom panels were generated and why
- the final project-level biological interpretation
- the overall confidence level based on pseudobulk availability, DA support, cell-level-only limitations, and cross-layer agreement

Phase 7 reports should not:

- repeat every prior report in miniature
- stay organized contrast-by-contrast from start to finish
- devolve into a changelog of all clusters
- treat the project as a collection of unrelated results trees
- overstate weak or cell-level-only findings as definitive biology

Instead, phase 7 should read like the final biological memo for the dataset:

- synthesis-centered
- concise
- organized by biological story rather than by pipeline phase
- explicit about predictive versus mechanistic interpretations when relevant
- explicit about what is robust versus provisional

Recommended data inputs for phase 7:

- phase 3 overview outputs and any active label-hierarchy layers
- the relevant phase 4 DE overview reports across layers and contrasts
- the relevant phase 5 DE reports for the key driver populations
- the relevant phase 6 synthesis reports across contrasts
- matching DE and DA settings files and summary tables
- selected underlying DE and DA tables for spot checks
- the final merged annotation object and associated figures
- direct `adata` queries when needed for supporting counts, prevalence, or layer mapping

Cross-contrast synthesis rules:

- Always ask which findings recur across multiple contrasts and which are contrast-specific.
- Distinguish predictive baseline findings from post-intervention or longitudinal mechanistic findings.
- If the same broad compartment recurs across multiple contrasts, identify whether the same fine populations are responsible each time.
- If a signal appears in one contrast but not another, say that explicitly and interpret why that matters biologically.
- Summarize null or weak findings when they materially narrow the interpretation.

Phase 7 process-panel rule:

- If the integrated project-level story suggests one or more coherent processes such as inflammation, metabolic reprogramming, bile-acid handling, endothelial specialization, scavenging identity, fibrosis, stress, or remodeling, create at least one targeted custom panel for each process that is central to the final narrative.
- Prefer genes that are both biologically central to the inferred process and supported somewhere in the DE signal when possible.
- If the strongest process genes are not all among the top DE hits, it is acceptable to supplement with canonical process genes.
- Use the `scomnom` plotting API to generate project-level panels when possible.
- Prefer targeted plots that clarify the final synthesis, for example:
  - layer-aware dotplots across the main driver populations
  - contrast-split violins for the key synthesis genes
  - UMAPs showing the main project-level process genes

Recommended section order for phase 7 synthesis reports:

- `Phase 7 Biological Synthesis`
- `Scope`
- `Study Design`
- `Final Atlas Context`
- `Global Biological Findings`
- `Predictive Signals`
- `Mechanistic And Longitudinal Signals`
- `Differential Expression And Abundance Integration`
- `Cross-Layer Resolution`
- `Process Panels`
- `Integrated Interpretation`
- `Confidence And Limitations`
- `Final Takeaway`

Content expectations for each phase 7 section:

- `Scope`:
  State the active context and that this is the final project-level biological synthesis.

- `Study Design`:
  Explain what the main contrasts mean biologically, especially which ones are predictive and which ones are mechanistic.

- `Final Atlas Context`:
  Summarize the final atlas organization from phase 3 so the biological findings are anchored in the final annotation hierarchy.

- `Global Biological Findings`:
  Summarize the strongest recurring biology in the dataset as a whole.

- `Predictive Signals`:
  Summarize the main baseline findings that may foreshadow later outcomes when the study design supports that interpretation.

- `Mechanistic And Longitudinal Signals`:
  Summarize the main post-intervention or over-time biology and explain how it differs from the predictive baseline story.

- `Differential Expression And Abundance Integration`:
  State whether the project-level story is mainly state change, abundance change, or both.
  Be explicit about DA-null interpretations when relevant.

- `Cross-Layer Resolution`:
  Explain which broad signals refine into specific driver populations and which broad signals weaken after splitting.

- `Process Panels`:
  Describe the targeted custom panels used to support the final integrated story, why those genes were chosen, and what they show.

- `Integrated Interpretation`:
  Provide the main biological narrative for the project in one coherent synthesis paragraph or short set of paragraphs.

- `Confidence And Limitations`:
  State the main strengths and weaknesses of the evidence base, including pseudobulk availability, DA support, and cell-level-only limitations.

- `Final Takeaway`:
  End with a concise statement of what the dataset most likely says biologically overall.

Rules for phase 7 writing style:

- Write phase 7 as the final biological memo for the project, not as a recap of every prior phase.
- Prefer biological synthesis over report inventory.
- Be explicit about predictive versus mechanistic framing when relevant to the study design.
- Be explicit about whether the project-level story is dominated by state change, abundance change, or both.
- Keep the report concise relative to the total volume of underlying phase 3 to phase 6 material.

Rules for phase 7 HTML output:

- Use the same clean single-page design language as the phase 3 through phase 6 reports so outputs look consistent across projects.
- Use bordered sections, inline galleries, and local copied assets only.
- Copy every figure used by the HTML into `de_phase7_master_synthesis_assets/`.

Rules for phase 7 TXT output:

- Preserve the same section order and synthesis logic as the HTML report.
- Keep the prose readable without links or HTML.
- Refer to process panels clearly in text so the reasoning remains understandable even without the figures.

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
- `templates/report_templates/label_umap_template.py`

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

Categorical label-layer UMAP workflow:

- For categorical annotation layers stored in `adata.obs`, use `om.plotting.plot_de_umap_single(...)` as the portable default plotting entry point.
- Treat this as the standard way to generate UMAPs for renamed layers such as archetype, compartment, or supercompartment labels.
- Do not depend on pipeline-internal helpers for this portable workflow.
- Prefer generating at least:
  - one full-legend categorical UMAP
  - one short-legend categorical UMAP when readability benefits from a simplified legend or on-data labels
- Follow `templates/report_templates/label_umap_template.py` as the default reusable skeleton for categorical label-layer UMAP generation.
- Before generating a new label-layer UMAP, first check whether a suitable figure already exists in the active figure tree, especially under `rename_roundN/` or comparable rename-output folders.
- Only generate a new UMAP when an appropriate existing figure is missing or stale, or when the user explicitly asks for regeneration.

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
