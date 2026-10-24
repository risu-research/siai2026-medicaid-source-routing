# Medicaid appeals audit: source-routing experiments

This repository provides the reproducibility artifact for Moon Hwan Lee's *Corrective Action in Medicaid Appeals: Legal Authority and Source Retrieval* (SIAI 2026, paper #110).

The study uses publicly reported Medicaid compliance reviews from Nevada. It tests whether lexical retrieval can locate a designated audit requirement and how the results change when that requirement is unavailable. The input cards and target labels were transcribed by the author from the cited reports.

## Reproduce the results

Use Python 3.13 in a fresh environment. The versions in `requirements.txt` are the versions used for the archived replay. After installing dependencies, the experiments run without network access.

```bash
python -m venv .venv
# Linux and macOS
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/run_all.py
.venv/bin/python analysis/corpus_removal_sensitivity.py
```

On Windows PowerShell:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts\run_all.py
.\.venv\Scripts\python.exe analysis\corpus_removal_sensitivity.py
```

The first command checks the six frozen input and protocol hashes, runs the three experiments, and compares regenerated outputs with the saved reference files. A successful run ends with:

```text
SUCCESS: all archived outputs reproduced; report in results/reproduced/VERIFICATION.json
```

It verifies **276 row-level results**, **92 score-change records**, and the six-row threshold-transfer table. Small floating-point differences are accepted within the bounds specified in the comparison script; categorical results must match exactly. The separate sensitivity script compares removing the designated card only from eligible retrieval candidates with rebuilding the TF-IDF index after removal. Its outputs appear in `results/sensitivity/`.

## Experiments and files

| Evaluation | Input | Targets | Cards | Query form |
| --- | --- | ---: | ---: | --- |
| SilverSummit S1 | `nevada_heldout_dataset_v1.json` | 8 | 16 | Required audit action |
| SilverSummit S2 | `nevada_finding_to_warrant_dataset_v2.json` | 8 | 16 | Reported audit finding |
| Molina | `molina_finding_to_warrant_dataset_v3.json` | 7 | 21 | Reported audit finding |

- `data/frozen/` has the preserved JSON inputs, evaluation protocols, and SHA-256 records.
- `scripts/` has portable experiment replay and verification code.
- `results/reference/` has the archived row-level results and threshold comparison.
- `analysis/` has the post hoc sensitivity calculation.
- `work/`, `results/reproduced/`, and `results/sensitivity/` are generated locally and excluded from version control.

### Scoring and interpretation

TF-IDF and BM25 rank source cards. The primary index is fit on the complete card pool; a designated source is then excluded from the eligible candidates in each removal trial. An unthresholded top-one ranker necessarily returns another candidate when at least one remains. The more informative diagnostic is how a selected abstention threshold behaves across query formulations. The post hoc refitting analysis evaluates a different absence condition and is reported separately.

The measured target is an **author-designated audit item**, not a determination that every other provision lacks legal relevance. A valid item identifier is assumed by the identity-lookup diagnostic and must be authenticated before practical use. These are curated-card retrieval tests, not an assessment of end-to-end document extraction, legal decision making, or professional reviewer performance.

### Source and implementation provenance

The original execution scripts for S1 and Molina were retained and adapted to use relative paths. The original S2 execution script was not preserved. `scripts/replay_s2_reconstructed.py` recreates its scoring procedure from the retained S1 implementation and S2's frozen input, protocol, and expected outputs. Its row-level predictions and scores were checked against the archived results. This validates reproducibility of the archived calculation, not independent annotation or historical source-code identity.

The source cards are author transcriptions. SHA-256 verification checks that the preserved input bytes are unchanged; it does not independently authenticate the cards against agency originals or verify when they were first prepared.

## Public documents

- [SilverSummit Healthplan, 2025 Nevada compliance review](https://www.nevadamedicaid.nv.gov/uploadedFiles/dhcfpnvgov/content/Resources/AdminSupport/Reports/SilverSummit_NVSFY2025_MCO_Compliance_Report_F1.pdf)
- [Molina Healthcare of Nevada, 2025 compliance review](https://www.nevadamedicaid.nv.gov/uploadedFiles/dhcfpnvgov/content/Resources/AdminSupport/Reports/Molina_NVSFY2025_MCO_Compliance_Report_F1.pdf)
- [Nevada Medicaid reports index](https://www.nevadamedicaid.nv.gov/medicaid-members/health-plan-home/reports/)

The government reports are linked rather than redistributed here. This repository contains the transcribed research inputs and the code needed to reproduce the reported retrieval results. No license for reuse of the code or data is granted by this README.
