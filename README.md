# scomnom-anno-bot

Version: `0.4.0`

`scomnom-anno-bot` is a portable annotation workflow for reviewing `scOmnom` analysis outputs with an agentic LLM.

It is designed to help with:

- phase 1 overview annotation of full datasets or subset result trees
- phase 2 deep-dive annotation of individual clusters
- phase 3 final integrated atlas overview after subset labels are merged back into the main object
- phase 4 atlas-level DE overview for one selected contrast
- phase 5 cluster-level DE deep dive for one selected contrast and cluster
- phase 6 cross-layer DE synthesis overview for one selected contrast
- evidence-driven cell type naming based on markers, specificity, pathways, and literature
- structured annotation and DE note generation in HTML and TXT formats
- targeted 9-gene validation panel design and plotting through `scomnom`
- targeted DE follow-up plotting through `scomnom`
- process-focused DE synthesis panels through `scomnom`
- keeping annotation workflow conventions consistent across projects

`scomnom-anno-bot` is intended for use inside a `scOmnom` project results folder, with the actual dataset-specific assumptions stored locally in `project-local.md`.

## What It Does

`scomnom-anno-bot` provides:

- a portable `AGENTS.md` with startup checks, annotation workflow rules, report conventions, and panel-plotting workflow
- portable report templates for phase 1, phase 3, phase 4, phase 5, and phase 6 style outputs
- a starter template for `project-local.md`
- a structured command vocabulary for common annotation tasks

The workflow is built around the idea that cluster annotation should be based on multiple lines of evidence together:

- cell-level markers
- pseudobulk markers
- expression specificity in dotplots and violin plots
- pathway and activity evidence from MSigDB, DoRothEA, and PROGENy
- clustering QC when relevant
- targeted custom validation panels
- literature support

For DE reporting, the workflow is built around:

- DE summary tables
- cluster-level combined DE tables
- cell-level and pseudobulk DE source agreement when both are available
- pathway and regulator outputs from MSigDB, DoRothEA, and PROGENy
- targeted additional plotting or `adata` queries only when the exported figures and tables are insufficient
- cross-layer synthesis across broad and fine annotation layers
- targeted process panels when the integrated signal supports a coherent biology

When both cell-level and pseudobulk DE are available, `scomnom-anno-bot` should weigh pseudobulk more heavily for inferential confidence because cell-level ranksum-style testing can be inflation-prone in large single-cell datasets.

## Requirements

`scomnom-anno-bot` has been tested with:

- OpenAI GPT-5.4
- a Codex environment

Other agentic LLMs may or may not work out of the box.

For custom panel plotting, the active project should also have:

- a working `scOmnom` analysis result tree
- a usable `scOmnom_env` Conda environment, or an equivalent environment with `scomnom` installed

If `scomnom` plotting is unavailable, `scomnom-anno-bot` should still be able to perform evidence review from existing figures and tables, but it will skip custom panel generation.

## Installation

Clone `scomnom-anno-bot` into the results folder of your `scOmnom` project:

```bash
git clone https://github.com/prangelab/scomnom-anno-bot.git scomnom-anno-bot
```

Then create an `AGENTS.md` file in that same results folder with this exact one-line instruction:

```text
Open, read, and execute the instructions in `scomnom-anno-bot/AGENTS.md`.
```

Then create a local override file in that same results folder:

```text
project-local.md
```

For a new project, start by copying the simple default file:

```bash
cp scomnom-anno-bot/templates/report_templates/project-local.example.md project-local.md
```

That file is intentionally project-agnostic and acts as a sensible default baseline until you add project-specific notes.

If you want an explained version that describes what each section is for, also see:

```text
scomnom-anno-bot/templates/report_templates/project-local.annotated-example.md
```

The resulting results-folder layout will typically look like:

```text
your-results-folder/
├── AGENTS.md
├── project-local.md
├── scomnom-anno-bot/
│   ├── AGENTS.md
│   ├── README.md
│   └── templates/
│       └── report_templates/
└── ... your scOmnom outputs ...
```

## How To Use It

At session start, `scomnom-anno-bot` should:

- read the root `AGENTS.md`
- follow it into `scomnom-anno-bot/AGENTS.md`
- read `project-local.md` if present
- check whether the current folder contains a usable `scOmnom` results tree
- determine the active context
- check whether `scOmnom_env` and `scomnom` plotting are available

After that, you can work conversationally and steer the annotation process with simple commands.

## Typical Workflow

### 1. Start at the results-folder root

Example:

```text
Please make a phase 1 overview of the root clusters.
```

Expected behavior:

- inspect the main result tree
- review UMAP, marker heatmaps, marker tables, and relevant QC
- produce a phase 1 overview report
- suggest which clusters are final versus which compartments should be subsetted

### 2. Switch to a subset context

Example:

```text
Let's work on the myeloid subset now.
```

Expected behavior:

- switch all inputs and outputs to the myeloid subset result tree
- keep that subset as the active context until told otherwise

### 3. Run a phase 1 overview for the subset

Example:

```text
Please do phase 1 here.
```

Expected behavior:

- inspect the subset UMAP, marker outputs, and QC
- identify resolved clusters, likely contaminants, and any clusters still needing caution
- write the overview report into the subset annotation directory

### 4. Deep-dive a cluster

Example:

```text
Annotate C00
```

Expected behavior:

- inspect cell-level and pseudobulk markers
- inspect dotplots and violins
- inspect MSigDB, DoRothEA, and PROGENy
- inspect QC if relevant
- propose a final two-marker plus description label
- find 2 to 3 literature references
- design a 9-gene validation panel
- plot the panel if `scomnom` plotting is available
- iterate if needed
- write structured HTML, TXT, and MD notes plus copied assets

### 5. Work through multiple clusters

Example:

```text
Annotate clusters C00, C01, C02
```

Expected behavior:

- annotate them serially using the active context
- write one report per cluster

### 6. Generate the final integrated atlas summary

Example:

```text
Generate phase 3 overview
```

Expected behavior:

- locate the merged main-object `adata` containing the final merged label key
- use the final merged UMAP and merged QC figures rather than the earlier phase 1 backbone
- summarize the final population names and compartment structure
- report cell counts and atlas-level organization when available
- comment briefly on any remaining mixed borders at atlas level
- write a final integrated overview report into the main `annotation/` directory

### 7. Generate an atlas-level DE overview

Example:

```text
Generate phase 4 DE overview for r4_subset_annotation masld_status better_vs_worse
```

Expected behavior:

- locate the correct DE result tree for the active context and layer
- identify whether `cell_based/` only or both `cell_based/` and `pseudobulk_DE/` are available
- summarize which clusters were testable, skipped, or weakly powered
- describe where the strongest DE signal sits across the atlas
- shortlist the best phase 5 targets
- write a structured DE overview report into `annotation/phase4/`

### 8. Deep-dive one cluster for one contrast

Example:

```text
Generate phase 5 DE report for C03 in masld_status better_vs_worse
```

Expected behavior:

- use the per-cluster combined DE table as the main backbone
- weigh pseudobulk more heavily than cell-level significance when both are available
- summarize genes higher in A versus genes higher in B
- inspect pathway and regulator figures
- add targeted extra plots through `scomnom` only when needed
- write a structured DE report into `annotation/phase5/`

### 9. Synthesize one contrast across layers

Example:

```text
Generate phase 6 DE synthesis for masld_status better_vs_worse
```

Expected behavior:

- identify the relevant phase 4 and phase 5 reports for that contrast across the available annotation layers
- generate missing phase 4 or phase 5 prerequisites first if needed
- integrate broad and fine layers into one final contrast-level DE memo
- explain which fine-grained populations are driving the broad compartment signals
- generate targeted custom process panels when the integrated signal supports a coherent biology
- write a structured synthesis report into `annotation/phase6/`

## Commands

These are the main command-style phrases `scomnom-anno-bot` is designed to understand.

### Context control

- `Let's work on the myeloid subset now`
- `Let's work on the lymphoid subset now`
- `Let's switch back to the main dataset`

These commands set the active context. Later `Annotate Cnn` requests should use that active context by default.

### Panel session control

- `start panel session`
- `stop panel session`

These commands manage the persistent Python plotting session used for custom 9-gene validation panels.

### Cluster deep dive

- `Annotate Cnn`
- `Annotate cluster Cnn`
- `Annotate clusters Cnn, ..., Ckk`

These commands trigger the full deep-dive workflow for the requested cluster or clusters.

### Overview work

Examples:

- `Please do phase 1 here`
- `Please make a phase 1 overview of the root clusters`
- `Give me a rough overview of this subset`
- `Generate phase 3 overview`
- `Perform phase 3 overview`
- `Generate phase 4 DE overview`
- `Perform phase 4 DE overview`
- `Generate phase 5 DE report for Cnn`
- `Perform phase 5 DE reports on Cnn, ..., Ckk`
- `Generate phase 6 DE synthesis`
- `Perform phase 6 DE overview`

These requests should trigger the overview workflow rather than a deep-dive cluster memo.

For `phase 3 overview`, the expected meaning is different from phase 1:

- phase 1 is a first-pass annotation overview used to decide rough identities and subsetting priorities
- phase 3 is a final integrated atlas overview used after phase 2 labels have been merged back into the main object
- phase 3 should summarize the final names and compartments rather than re-arguing identities from scratch

For the DE phases:

- phase 4 is an atlas-level DE triage memo for one selected contrast
- phase 5 is a cluster-level DE memo for one selected contrast and cluster
- phase 6 is a final contrast-level DE synthesis memo that integrates phase 4 and phase 5 across available annotation layers
- DE reports should use `scOmnom` contrast-key semantics:
  - `A:B` builds a composite key, usually resolved internally as `A.B`
  - `A@B` means compare `A` within levels of `B`
  - `A^B` means interaction
- when both `cell_based/` and `pseudobulk_DE/` exist, pseudobulk should be weighted more heavily for inferential confidence
- phase 6 should explicitly connect broad layers and fine layers when both are available

## Output Conventions

`scomnom-anno-bot` writes:

- phase 1 overview reports as `.html` and `.txt`
- phase 3 overview reports as `.html`, `.txt`, and `phase3_overview_assets/`
- phase 4 DE overview reports in `annotation/phase4/` as `.html`, `.txt`, and `de_phase4_<run_id>_assets/`
- phase 5 DE reports in `annotation/phase5/` as `.html`, `.txt`, `.md`, and `de_phase5_<run_id>_<cluster>_assets/`
- phase 6 DE synthesis reports in `annotation/phase6/` as `.html`, `.txt`, and `de_phase6_<run_id>_assets/`
- deep-dive cluster reports as `.html`, `.txt`, `.md`, and `CXX_assets/`
- custom panel plots into the active context `panels/` directory

Phase 3 reports are intended to be final-atlas memos. They should:

- use the merged annotation object with the final merged label key
- report the final population names exactly as they should be used going forward
- summarize atlas compartments and relative abundances
- use merged UMAP, sample-overlay, cluster-size, batch-composition, silhouette, and QC-summary figures when available
- stay more concise than deep-dive reports while still being more structured than a short chat summary

The HTML reports are designed for local browsing and should include:

- structured sections
- embedded figures
- local copied assets
- click-to-enlarge image overlays

DE reports should:

- reuse the existing DE tables and figure trees before generating anything extra
- treat pseudobulk as the preferred inferential source when available
- use cell-level DE mainly for expression prevalence, within-cluster distribution, and direction consistency
- generate targeted extra `scomnom` plots or direct `adata` summaries only when the exported outputs are insufficient for interpretation

Phase 6 synthesis reports should:

- use phase 4 as the atlas-level backbone and phase 5 as the cluster-level detail layer
- integrate broad and fine annotation layers explicitly when both are available
- explain which fine-grained populations are driving the broad signals
- generate targeted custom process panels when the integrated signal supports a coherent biology

## Templates

Portable templates are included in:

- `templates/report_templates/deep_dive_template.html`
- `templates/report_templates/deep_dive_template.txt`
- `templates/report_templates/de_phase4_overview_template.html`
- `templates/report_templates/de_phase4_overview_template.txt`
- `templates/report_templates/de_phase5_report_template.html`
- `templates/report_templates/de_phase5_report_template.txt`
- `templates/report_templates/de_phase6_synthesis_template.html`
- `templates/report_templates/de_phase6_synthesis_template.txt`
- `templates/report_templates/phase1_overview_template.html`
- `templates/report_templates/phase1_overview_template.txt`
- `templates/report_templates/project-local.example.md`
- `templates/report_templates/project-local.annotated-example.md`

These provide a stable baseline for report structure and local project configuration.

## Disclaimer

`scomnom-anno-bot` works from the actual `scOmnom` results data in the project, but the final interpretations are still LLM-generated and therefore prone to confabulations or overconfident inference.

This risk is especially important when:

- clusters are small or QC-sensitive
- marker evidence is mixed
- literature support is sparse
- rare cell types or unusual cell states are involved

All results should be checked and validated by a human researcher.

`scomnom-anno-bot` provides a guide, not a definitive answer.
