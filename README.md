# Medicaid appeals: source evidence and retrieval experiments

This repository accompanies Moon Hwan Lee's paper, *Corrective Action in Medicaid Appeals: Legal Authority and Source Retrieval* (SIAI 2026, paper 110; presented November 14, 2026).

The paper studies how an audit finding leads to a specific correction. Louisiana's Medicaid dental-plan review found outdated appeal instructions and errors in the state-hearing filing deadline. A Colorado audit described approved dental care that had not reached the member's chart or provider. Separate retrieval experiments use Nevada audit records to test whether a search method finds the assigned requirement and how its ranking changes when that requirement is removed.

The frozen Nevada experiments were part of the SIAI study. The Louisiana contract history and the later handbook comparison were developed after the presentation. Both remain available here, with their source dates and document links.

## Results

The search experiments use requirement cards prepared from two Nevada compliance reports. Each target has an author-assigned audit item ID. Top-1 accuracy measures agreement with that ID.

| Task | Targets | Cards | TF–IDF top-1 | BM25 top-1 |
| --- | ---: | ---: | ---: | ---: |
| SilverSummit S1: required actions | 8 | 16 | 8/8 | 7/8 |
| SilverSummit S2: audit findings | 8 | 16 | 7/8 | 5/8 |
| Molina: audit findings | 7 | 21 | 3/7 | 3/7 |

All figures above use procedural-stage filtering. The S1 score-gap rule accepted seven correct answers and held all eight source-removal cases. Applied unchanged to S2 and Molina, that rule held every answer. The archived outputs record each score, prediction and threshold-transfer result.

The cards and target IDs were prepared by the author from the cited agency reports. Reproducing the calculations checks the recorded experiment; checking the underlying legal meaning requires reading those reports.

## Contents

| Location | Material |
| --- | --- |
| [Louisiana correction ledger](evidence/louisiana/correction_ledger.csv) and [authority notes](evidence/louisiana/authority_trace.md) | Six unmet audit elements, relevant clauses and requested follow-up records |
| [2024 legal-source comparison](evidence/louisiana/2024_AUTHORITY_CROSSWALK.md) | Federal requirements, MCNA contract terms and the audit findings |
| [MCNA contract history](evidence/louisiana/CLAUSE_HISTORY_2024.md) and [amendment inventory](evidence/louisiana/contract_amendment_trail.csv) | Source pages and the original agreement plus Amendments 1–13 |
| [2025 member-handbook review](evidence/louisiana/POST_AUDIT_HANDBOOK_REVIEW.md) | Later public Adult Denture and EPSDT editions, PDF hashes and specific wording |
| [2026 LDH enforcement notice](evidence/louisiana/enforcement_followup_2026.md) | State penalty and its scope across compliance standards |
| [Colorado care-delivery record](evidence/colorado/delivery_evidence.md) | Authorized services, provider communication and the missing delivery evidence |
| [Frozen datasets and protocols](data/frozen/) | Three Nevada study datasets and six SHA-256 input checks |
| [Reference outputs](results/reference/) | Predictions, score changes and threshold-transfer results |
| [Replication scripts](scripts/) and [sensitivity analysis](analysis/corpus_removal_sensitivity.py) | Offline calculation and comparison with the archived outputs |

## Reproduce the Nevada experiments

Use Python 3.13 and the versions in [requirements.txt](requirements.txt).

```bash
python -m pip install -r requirements.txt
python scripts/run_all.py
python analysis/corpus_removal_sensitivity.py
```

The replay verifies six frozen input hashes, regenerates three experiments and compares the results with the archived files. The comparison covers 276 prediction rows, 92 score-change records and six threshold-transfer rows. Outputs are written to `results/reproduced/` and `results/sensitivity/`. On Windows PowerShell, `py -3.13` may be used in place of `python`.

The [reproduction workflow](.github/workflows/reproduce.yml) runs these commands on GitHub Actions.

The source-review scripts use official public PDFs and require internet access. Their instructions are in [contract source reconstruction](evidence/louisiana/SOURCE_RECONSTRUCTION.md) and the [handbook review](evidence/louisiana/POST_AUDIT_HANDBOOK_REVIEW.md).

## Research record

The S1, S2 and Molina datasets and protocols are preserved from the research archive. Their input hashes and reference outputs are included. The S2 runner was reconstructed from the surviving method and study inputs; it reproduces the archived results. The GitHub repository was created later, so the earlier freeze dates come from the research archive.

After the SIAI presentation, the Louisiana follow-up traced amendments to the 2021 contract and read two public member-handbook editions released in August 2025. The record identifies changes in the written-appeal instructions, hearing deadline and grievance provisions. The 2024 handbook editions cited by the auditor, the approved corrective-action plan and member-level implementation records remain unavailable in the reviewed public sources.

The underlying agency reports and contracts are linked from their publishers. The repository contains the author's code, structured cards, findings and research notes. No member-level case records or original government PDF files are packaged here.

## Citation and archive

The [citation file](CITATION.cff) identifies this research artifact. The [release guide](ARCHIVE_AND_RELEASE.md) describes the contents to preserve in Zenodo. The permanent archive DOI can be added after Zenodo records the GitHub release.

The [MIT license](LICENSE) applies to original contributions in this repository. Source reports, contracts and other third-party publications retain their own terms; [source and rights notes](SOURCES_AND_RIGHTS.md) identify the boundary. Please cite the underlying agency documents when using their content.
