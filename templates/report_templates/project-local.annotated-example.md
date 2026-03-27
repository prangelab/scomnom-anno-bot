# project-local.md annotated example

Use this file as a guide for what belongs in `project-local.md`.

If you just want a clean starter file to copy into a new project and then customize only if needed, use:

- `templates/report_templates/project-local.example.md`

# Dataset

Describe the dataset briefly and concretely.

Examples:

- Human adipose snRNA-seq
- Mouse liver scRNA-seq
- Human PBMC scRNA-seq

# Directory guidance

List only project-specific rules here.

Examples:

- prefer PNG over PDF
- ignore superseded clustering rounds
- ignore DE folders if the current task is marker-stage annotation

# Annotation backbone

Use this section to say which clustering round and embedding should drive annotation.

Examples:

- use the compacted clustering round as the identity backbone
- use the post-annotation UMAP only for display
- use Harmony for identity calls and scANVI for presentation

# Current annotation workflow caveats

Record anything that could systematically mislead annotation.

Examples:

- CellTypist used an immune-only model
- one subset contains known stromal contamination
- only subset marker discovery is available

# Plotting workflow

Record the project’s preferred plotting entrypoint and any important local environment details.

Examples:

- default reusable plotting script template
- preferred local plotting script if the project has one
- Conda environment name
- machine-specific Conda activation helper path if needed

# Active context notes

Use this section to help the agent choose the right result tree.

Examples:

- root-level work should use the main result tree
- lymphoid work should use `results_subset_lymphoid/`
- if duplicate result trees exist, prefer the newest one
