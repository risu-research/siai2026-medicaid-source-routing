# Reconstructing the MCNA contract sources

The Louisiana Department of Health [official contract resource page](https://ldh.la.gov/resources?cat=&d=0&q=RFP&s=0&y=0) lists an executed MCNA contract and Amendments 1–15. The [source registry](mcna_official_source_registry.csv) collects the official PDF links for the original contract and Amendments 1–13, including previously missing Amendments 3–8.

Amendments 4, 5, 8, and 9 include changes to the Statement of Work. Their exact effect on appeal rules has to be checked against the original PDF tables. Amendments 3, 6, and 7 primarily concern capitation rate certifications. Those descriptions locate research priorities; they do not certify that a given appeal clause was unchanged.

## Reusable extraction step

The [PDF source scanner](../../tools/scan_mcna_contracts.py) can download the selected official PDFs, compute a SHA-256 fingerprint, and list page-level passages matching appeal and hearing terms. It writes a source manifest and a candidate passage CSV. For files with unreadable embedded fonts, the optional OCR fallback renders pages and runs Tesseract. It is applied only to selected documents, with the extraction method recorded beside each passage. The scanner only identifies places to read. A passage match cannot determine which amended text was legally operative.

```bash
python -m pip install 'pymupdf==1.26.4'
python tools/scan_mcna_contracts.py --only 4 5 8 9 --ocr-on-empty 4 5 8
```

For offline inspection, put the PDFs in a directory named `N.pdf` by amendment number and use `--local-dir path/to/pdfs`. That allows a reader to reproduce the extraction even when the LDH server limits automated downloads.

GitHub Actions runs a source scan on this work branch. PDF bytes are excluded from the Git repository. When the downloads succeed, the run publishes a temporary artifact containing page references and SHA-256 values.

The central substantive task is still the amendment comparison: determine whether the 2021 oral-appeal change, the hearing clock, and continued-benefit language survived each later revision during calendar year 2024. The [contract chronology](contract_amendment_trail.md) records the verified dates and outstanding links.
