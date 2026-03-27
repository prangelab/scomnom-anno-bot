# scomnom-anno-bot

Version: `0.1.0`

`scomnom-anno-bot` is a portable annotation workflow for reviewing `scOmnom` analysis outputs with an agentic LLM.

It is designed to help with:

- phase 1 overview annotation of full datasets or subset result trees
- phase 2 deep-dive annotation of individual clusters
- evidence-driven cell type naming based on markers, specificity, pathways, and literature
- structured annotation-note generation in HTML and TXT formats
- targeted 9-gene validation panel design and plotting through `scomnom`
- keeping annotation workflow conventions consistent across projects

`scomnom-anno-bot` is intended for use inside a `scOmnom` project results folder, with the actual dataset-specific assumptions stored locally in `project-local.md`.

## What It Does

`scomnom-anno-bot` provides:

- a portable `AGENTS.md` with startup checks, annotation workflow rules, report conventions, and panel-plotting workflow
- portable report templates for deep dives and phase 1 overviews
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

These requests should trigger the overview workflow rather than a deep-dive cluster memo.

## Output Conventions

`scomnom-anno-bot` writes:

- phase 1 overview reports as `.html` and `.txt`
- deep-dive cluster reports as `.html`, `.txt`, `.md`, and `CXX_assets/`
- custom panel plots into the active context `panels/` directory

The HTML reports are designed for local browsing and should include:

- structured sections
- embedded figures
- local copied assets
- click-to-enlarge image overlays

## Templates

Portable templates are included in:

- `templates/report_templates/deep_dive_template.html`
- `templates/report_templates/deep_dive_template.txt`
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
