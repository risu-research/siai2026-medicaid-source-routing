# Archived SIAI 2026 research artifact

This repository accompanies *Corrective Action in Medicaid Appeals: Legal Authority and Source Retrieval* (SIAI 2026, paper 110; presented November 14, 2026).

## Published research archive

| Record | Link |
| --- | --- |
| GitHub release | [v1.0.0](https://github.com/risu-research/siai2026-medicaid-source-routing/releases/tag/v1.0.0) |
| Version DOI | [10.5281/zenodo.24235732](https://doi.org/10.5281/zenodo.24235732) |
| All-versions DOI | [10.5281/zenodo.24235731](https://doi.org/10.5281/zenodo.24235731) |
| Zenodo record | [Record 24235732](https://zenodo.org/records/24235732) |
| Release commit | [`68caa7f6223c3d80a9dd2084abc1bcdc8c6a7082`](https://github.com/risu-research/siai2026-medicaid-source-routing/commit/68caa7f6223c3d80a9dd2084abc1bcdc8c6a7082) |

Zenodo published version v1.0.0 on **November 15, 2026 (UTC)** as open-access software under the MIT license. The repository was archived as `risu-research/siai2026-medicaid-source-routing-v1.0.0.zip` (107,518 bytes).

The GitHub release tag permanently identifies the reviewed commit. DOI links added to the repository after publication leave that archived source version unchanged.

## Contents

The archived version includes:

- Three Nevada retrieval datasets, study protocols, frozen-input hashes and reference results.
- Code for rebuilding retrieval outputs and the separate index-refitting sensitivity test.
- Source-linked Louisiana and Colorado compliance findings.
- Follow-up research on MCNA contract amendments and public member handbooks, added after the SIAI presentation.

The original agency PDFs remain available from their publishers. The conference paper's proceedings citation can be added when published.

## Reproduce the calculations

Use Python 3.13 with the pinned research dependencies.

```bash
python -m pip install -r requirements.txt
python scripts/run_all.py
python analysis/corpus_removal_sensitivity.py
```

The [GitHub Actions reproduction workflow](.github/workflows/reproduce.yml) runs the same calculations. The replay checks six frozen input hashes and compares regenerated results with the archived predictions, score changes and threshold-transfer table.

The original S1, S2 and Molina research inputs and outputs were copied into the public repository in November 2026. The S2 runner was reconstructed from the archived scoring method and original inputs, then checked against the preserved results. The Louisiana source investigations were completed later.

## Citation

Use the [version DOI](https://doi.org/10.5281/zenodo.24235732) when citing this precise artifact and the [all-versions DOI](https://doi.org/10.5281/zenodo.24235731) for the evolving research archive. The [CITATION.cff](CITATION.cff) metadata supplies the preferred citation. Cite the relevant state or federal documents when discussing their legal text or audit findings.
