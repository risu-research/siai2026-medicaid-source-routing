# Preparing the research artifact for Zenodo

This repository holds the research materials accompanying *Corrective Action in Medicaid Appeals: Legal Authority and Source Retrieval*, SIAI 2026 paper 110, presented November 14, 2026.

## Release contents

The archive contains:

- The three frozen Nevada datasets, study protocols, SHA-256 input checks and reference results.
- Scripts for rebuilding the Nevada retrieval results and the separate index-refitting sensitivity analysis.
- Source-linked records of Louisiana and Colorado compliance findings.
- Contract-amendment research and a comparison of publicly available 2025 MCNA member handbooks, added after the SIAI presentation.

The conference paper and the original agency PDFs are available through their respective publishers. They are not bundled in the repository.

## Verification

Run the [reproduction workflow](.github/workflows/reproduce.yml), or execute:

```bash
python -m pip install -r requirements.txt
python scripts/run_all.py
python analysis/corpus_removal_sensitivity.py
```

The main test reproduces the archived predictions, score changes and threshold-transfer results. The official-document scripts can be run separately when the public sources are available.

## Zenodo handoff

1. Connect this public repository in your Zenodo GitHub settings and enable archiving for it.
2. Create a **GitHub Release** from the reviewed `main` commit after the Zenodo connection is ready. Use a version tag such as `v1.0.0`, and summarize the SIAI experiments and the later source review in the release description.
3. Check the Zenodo record's title, author, upload type, license and source files. Zenodo reads the root [CITATION.cff](CITATION.cff).
4. Once Zenodo assigns a DOI, add the DOI to the README and citation metadata if needed, preserving the archived release tag.

GitHub's source archive for the tagged release is the unit preserved by Zenodo. The repository can continue to develop afterward without changing that version.

## Provenance

The experimental data and results were retained from the research archive and uploaded to GitHub in November 2026. Input hashes protect the frozen files against later edits; the first public GitHub commit records their upload, not their original creation. The S2 scoring runner was reconstructed from the archived procedure and inputs.

The Louisiana contract and handbook materials are later investigations. The 2025 public handbook versions are directly readable from MCNA's download service. Audit-cited versions from 2024 and the completed corrective-action plan were not recovered from the public sources. The recorded findings therefore concern document text and audit instructions, with member outcomes left for a separate study.

## Citation

The GitHub citation panel uses [CITATION.cff](CITATION.cff). Cite the archived research artifact when using the code or structured data. Cite the original state and federal reports for their legal provisions and audit findings.
