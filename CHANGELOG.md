# Changelog

## 0.5.0

- Added phase 7 final project-level biological synthesis workflow to `AGENTS.md`
- Added phase 7 guidance for:
  - integrating phase 3 through phase 6 into one dataset-level memo
  - distinguishing predictive baseline biology from mechanistic and longitudinal biology
  - integrating DE and DA at the project level
  - using targeted process panels for the final synthesis
- Added reusable phase 7 report templates
- Updated `README.md` to document phase 7 commands, outputs, and templates
- Bumped shared workflow version to `0.5.0`

## 0.1.0

- Initial portable release of `scomnom-anno-bot`
- Added shared `AGENTS.md`
- Added portable deep-dive and phase 1 report templates
- Added `project-local.example.md`
- Added repo `README.md`
- Added `VERSION`
- Added `LICENSE`

## 0.2.0

- Added phase 3 reporting
- Added categorical label-layer UMAP generation commands

## 0.3.0

- Added phase 4 DE overview workflow to `AGENTS.md`
- Added phase 5 DE deep-dive workflow to `AGENTS.md`
- Added reusable DE report templates for phase 4 and phase 5
- Added DE source-weighting guidance:
  - pseudobulk preferred when available
  - cell-level treated as supportive and potentially inflation-prone
- Added explicit `scOmnom` contrast-key semantics to the shared workflow:
  - composite keys via `A:B`
  - within-group contrasts via `A@B`
  - interaction contrasts via `A^B`
- Updated `README.md` to document DE workflows, outputs, and templates
- Bumped shared workflow version to `0.3.0`

## 0.4.0

- Added phase 6 DE synthesis workflow to `AGENTS.md`
- Added cross-layer DE synthesis guidance:
  - integrate broad and fine annotation layers explicitly
  - use phase 4 as the atlas-level backbone and phase 5 as the cluster-level detail layer
  - explain which finer populations drive broad compartment signals
- Added process-panel rules for phase 6:
  - generate targeted custom panels when a coherent biology is inferred
  - prefer process genes that are central and, when possible, also supported by the DE signal
- Added reusable phase 6 report templates
- Updated `README.md` to document phase 6 commands, outputs, and templates
- Bumped shared workflow version to `0.4.0`
