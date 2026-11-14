# Source-text screening of MCNA amendments

**Research follow-up — November 14, 2026.** The [LDH public contracts index](https://ldh.la.gov/resources?cat=&d=0&q=RFP&s=0&y=0) links the executed MCNA agreement and its amendments. This record documents a reproducible first pass through the amendments that were missing from the original SIAI study.

## Downloads and extraction

| Amendment | PDF pages | SHA-256 prefix | Extracted text | Relevant search hits |
| --- | ---: | --- | --- | ---: |
| [3](https://ldh.la.gov/assets/medicaid/ContractsDental/2000506243Amd3MCNA.pdf) | 78 | `d2590ace9055` | Embedded text, no OCR | 0 |
| [4](https://ldh.la.gov/assets/medicaid/ContractsDental/Amd4MCNA.pdf) | 10 | `2a03e1d7627b` | OCR, 14,105 nonblank characters | 0 |
| [5](https://ldh.la.gov/assets/medicaid/ContractsDental/2000506243Amd5MCNA-ApprovedContractPacket.pdf) | 9 | `f32d7fa00ce1` | OCR, 18,899 nonblank characters | 0 |
| [8](https://ldh.la.gov/assets/medicaid/ContractsDental/2000506243Amd8MCNA-ApprovedContractPacket.pdf) | 48 | `fe4d1b894847` | OCR, 107,158 nonblank characters | 0 |
| [9](https://ldh.la.gov/assets/medicaid/ContractsDental/2000506243Amd9MCNA-ApprovedContractPacket.pdf) | 15 | `b71924d07b36` | Embedded text | 3 |
| [10](https://ldh.la.gov/assets/medicaid/ContractsDental/2000506243Amd10MCNA-ApprovedContractPacket.pdf) | 2 | `f85ddfb34f38` | Embedded text | 0 |

The scanner searches for the 2.10.3 and 2.10.7 clause families along with common wording for appeals, grievances, fair hearings, written confirmation, and continued benefits. These are **candidate passage counts**, not numbers of changed legal provisions. The three hits in Amendment 9 need direct reading; they have not been classified as amendments to the studied appeal rules.

Amendments 4, 5, and 8 yielded substantial OCR text but no matching passage under those search terms. This screening gives a useful lead for manual clause comparison. A zero search result is not an authenticated statement that every later contract retained a provision. Amendment 3's zero result is weaker because it was not OCR-processed.

The executed PDFs were downloaded by [GitHub Actions](https://github.com/risu-research/siai2026-medicaid-source-routing/actions/runs/43645177386), and the run saved source hashes, candidate passages, and OCR text in its [temporary artifact](https://github.com/risu-research/siai2026-medicaid-source-routing/actions/runs/43645177386/artifacts/14133319759). SHA-256 values help distinguish the downloaded versions. The [source registry](mcna_official_source_registry.csv) provides stable government URLs.

## What to read next

The most consequential contract questions concern the deletion of the signed written follow-up for oral appeals, the 120-day state-hearing filing period, and the fourth continued-benefit ending event in the 2021 original agreement. Start with Amendment 2, and compare any intervening Attachment B replacements through December 2024, especially the full tables for Amendments 4, 5, 8, and 9. The source scan has already narrowed that work.

The 2026 penalty notice references a contract effective January 1, 2023. Amendment 10 shows the 2021 agreement was extended to December 2025. Read these records together before assigning a final governing clause to any 2024 policy correction.

No state enforcement, implementation, or member-outcome finding is inferred from the text scan.
