# Medicaid appeals: audit sources and retrieval experiments

This repository accompanies Moon Hwan Lee's paper, *Corrective Action in Medicaid Appeals: Legal Authority and Source Retrieval* (SIAI 2026, paper 110; presented November 14, 2026).

A Louisiana Medicaid dental-plan audit reported six unmet elements in its grievance-and-appeal review. The findings called for different corrections. Two policies started the state-hearing filing period at the initial benefit notice, even though the period begins after the plan resolves an appeal. Member handbooks also retained a signed follow-up step that a 2021 contract amendment had removed. In Colorado, a separate audit recorded approved dental care that never reached the member's chart or provider.

For the retrieval experiments, I used requirement cards prepared from two Nevada Medicaid compliance reports. The tests ask whether a word-based search method selects the assigned audit item, and what happens to its ranking when that item is removed from the eligible results.

## What is here

- **[Louisiana evidence ledger](evidence/louisiana/correction_ledger.csv)** — six audit elements, their proposed corrections, sources, and records needed for review. The accompanying [authority notes](evidence/louisiana/authority_trace.md) follow the dated contract provisions.
- **[Colorado case notes](evidence/colorado/delivery_evidence.md)** — the report's findings on care coordination, the approved cleanings, and the records that would help trace service delivery.
- **[Follow-up enforcement record](evidence/louisiana/enforcement_followup_2026.md)** — the 2026 state notice and its implications for the contract history.
- **[MCNA contract amendment trail](evidence/louisiana/contract_amendment_trail.md)** — dated source inventory and a [complete official link registry](evidence/louisiana/mcna_official_source_registry.csv), including amendments previously missing from the paper.
- **[2024 legal-source crosswalk](evidence/louisiana/2024_AUTHORITY_CROSSWALK.md)** — compare federal rules, contract provisions, and the audit's correction requests, with a [CSV dataset](evidence/louisiana/2024_authority_crosswalk.csv).
- **[2024 clause history](evidence/louisiana/CLAUSE_HISTORY_2024.md)** — dated changes, including the earlier contract language, with a [change CSV](evidence/louisiana/mcna_clause_changes.csv).
- **[Contract source reconstruction](evidence/louisiana/SOURCE_RECONSTRUCTION.md)** — original PDFs and page-level evidence extraction.
- **`data/frozen/`** — three preserved Nevada datasets and their protocols, with SHA-256 checksums.
- **`scripts/`** — the search experiments and output comparisons.
- **`results/reference/`** — archived predictions, scores, and threshold-transfer results.
- **`analysis/`** — the separate index-refitting sensitivity test.

The [Louisiana enforcement follow-up](evidence/louisiana/enforcement_followup_2026.md) records a $30,000 penalty assessed in March 2026 across six noncompliant standards. The [contract amendment trail](evidence/louisiana/contract_amendment_trail.md) brings together source dates and amendments relevant to the 2024 review. The identified changes now include Amendment 9's grievance extension rules and Amendment 11's appeal-reversal threshold. The original contract's fourth continued-benefits ending event is recorded separately from the three events listed in the 2024 federal regulation. The full 2024 governing text remains under review.

## Results at a glance

All three tasks use designated audit-item IDs as their targets. S1 and S2 share the same SilverSummit cards, with different query wording. Molina uses a second health plan's report.

| Test | Questions | Cards | TF–IDF top-1 | BM25 top-1 |
| --- | ---: | ---: | ---: | ---: |
| SilverSummit S1: required actions | 8 | 16 | 8/8 | 7/8 |
| SilverSummit S2: audit findings | 8 | 16 | 7/8 | 5/8 |
| Molina: audit findings | 7 | 21 | 3/7 | 3/7 |

These are matches to author-assigned item IDs after procedural-stage filtering.

A score-gap rule selected on S1 accepted seven correct matches and held all eight source-removal cases. Applied unchanged to S2 and Molina, it held every answer, including cases with the assigned source present. In a separate full-pool SilverSummit example, removing item 18 increased the gap between the top two TF–IDF scores from 0.006382 to 0.128800. Both conditions and the original scores are recorded in the archived outputs.

## Run the experiments

Python 3.13 and the versions in [`requirements.txt`](requirements.txt) reproduce the archived calculation. After installing those packages, the scripts run locally without fetching reports or datasets.

```bash
python -m pip install -r requirements.txt
python scripts/run_all.py
python analysis/corpus_removal_sensitivity.py
```

On Windows PowerShell, use `py -3.13` for the Python commands if that is how Python is installed.

`run_all.py` checks six archived dataset and protocol hashes, regenerates three experiments, and compares the results against the reference files. The comparison covers 276 prediction rows, 92 score-change records, and six threshold-transfer rows. Generated files appear under `results/reproduced/` and `results/sensitivity/`.

The [GitHub Actions workflow](.github/workflows/reproduce.yml) reruns the Nevada experiments on new commits. The Louisiana and Colorado records are source-linked research notes, maintained separately from the computational replay.

## Sources and research record

- [Louisiana: 2025 MCNA compliance review](https://ldh.la.gov/assets/medicaid/EQRO/2025/Compliance/MCNA_LA_2025_CR_Report_F1.pdf), Standard XIII, reviewing calendar-year 2024 materials
- [Louisiana: March 2026 monetary-penalty notice](https://ldh.la.gov/assets/docs/BayouHealth/Accountability/2.0/MCNA/MCNA1-16_Notice_of_Monetary_Penalty-_2025_External_Quality_Compliance_Review_3.12.26.pdf), state assessment and the contract reference
- [Louisiana: MCNA contract amendment 2](https://www.ldh.la.gov/assets/medicaid/ContractsDental/2000506243Amd2MCNA.pdf), signed-return and hearing-filing provisions
- [Colorado: DentaQuest FY2024–2025 review](https://spl.cde.state.co.us/artemis/hcpserials/hcp62125internet/hcp62125202425internet.pdf), Section 2
- [Nevada: SilverSummit 2025 review](https://www.nevadamedicaid.nv.gov/uploadedFiles/dhcfpnvgov/content/Resources/AdminSupport/Reports/SilverSummit_NVSFY2025_MCO_Compliance_Report_F1.pdf), Standard X
- [Nevada: Molina 2025 review](https://www.nevadamedicaid.nv.gov/uploadedFiles/dhcfpnvgov/content/Resources/AdminSupport/Reports/Molina_NVSFY2025_MCO_Compliance_Report_F1.pdf), Standard X

The Louisiana contract trail is a working source inventory. It identifies the dates and amendment documents located so far without assigning an automated legal-validity score. The Nevada cards were transcribed and grouped by the author. The S2 execution script was reconstructed from the preserved S1 method and S2 inputs; its outputs match the archived reference results. Source-card accuracy and the legal sufficiency of a selected passage require separate review of the agency documents. For Louisiana, the complete set of contract changes governing 2024 remains an open research item.

The code and research data currently have no reuse license. The public agency reports are linked from their original publishers.
