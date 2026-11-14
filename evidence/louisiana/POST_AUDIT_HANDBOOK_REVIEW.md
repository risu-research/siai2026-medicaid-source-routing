# Member handbook text after the 2024 Louisiana audit

The [2025 MCNA compliance review](https://ldh.la.gov/assets/medicaid/EQRO/2025/Compliance/MCNA_LA_2025_CR_Report_F1.pdf) evaluated calendar-year 2024 operations. Under Standard XIII, HSAG found that the Adult Denture and EPSDT member handbooks instructed members to follow an oral appeal with a written submission. The audit identified the supplied files as **Adult Denture v2.5** (pp. 21–22) and **EPSDT v2.3** (pp. 31–32). The required action was to remove the written-follow-up requirement from the handbooks.

MCNA subsequently published version 3.0 of both English handbooks. This record compares the audit's documented finding with what is printed in those later PDFs. The original 2024 handbooks have not been recovered as independent PDF files, so a word-by-word historical redline is not available.

## Later public files

| Handbook | Public release | Official PDF | Pages | SHA-256 |
| --- | --- | --- | ---: | --- |
| [Adult Denture v3.0](https://handbooks.mcna.net/mh-la-adult-en) | August 12, 2025 | [Download](https://handbooks.mcna.net/api/files/download/689b778236f3559579d5933a) | 40 | `c5e3ac8843f0b77a6aa4c227c3dfce181acf4dcf48f7cfa6b41ef727a7f03b9f` |
| [EPSDT v3.0](https://handbooks.mcna.net/mh-la-epsdt-en) | August 12, 2025 | [Download](https://handbooks.mcna.net/api/files/download/689b770836f3559579d5679e) | 48 | `5cc2ce95128c72d9fdc8eb937a8cf9db01d1e8b27b462f36dada10bb55d785c5` |

These SHA-256 fingerprints identify the two PDFs obtained from MCNA's public document-download endpoint on November 14, 2026. Source locations below give **both** PDF page numbers and printed handbook page numbers.

## What the new text says

| Question | Adult Denture v3.0 | EPSDT v3.0 | Observation |
| --- | --- | --- | --- |
| Can a member request an ordinary appeal by phone? | § 16.1, PDF p. 25 (printed p. 23) | § 18.1, PDF p. 33 (printed p. 31) | Both direct the member to call the hotline to request an appeal |
| Does the standard-appeal timing paragraph refer to receiving an appeal in writing? | § 16.3, PDF p. 25 (printed p. 23) | § 18.3, PDF p. 33 (printed p. 31) | Both open their acknowledgment explanation with **“After we receive your appeal in writing”** |
| Is a signature required to appoint someone else? | § 16.8, PDF p. 26 (printed p. 24) | § 18.8, PDF p. 34 (printed p. 32) | Both request signed permission for an authorized representative |
| When does the state-hearing filing window run? | § 18.1, PDF p. 28 (printed p. 26) | § 20.1, PDF p. 36 (printed p. 34) | Both specify 120 days from the date on the Notice of Appeal Resolution |
| Are service or time limits listed among continued-benefit ending events? | § 16.6, PDF pp. 25–26 (printed pp. 23–24) | § 18.6, PDF pp. 33–34 (printed pp. 31–32) | Both include the authorized service period or limit being reached |

**Oral appeal versus written follow-up.** In the appeal sections of the available v3.0 PDFs, we found the telephone filing instruction and no explicit direction that a member who calls **must send a subsequent written appeal**. The acknowledgment paragraph, however, continues to refer to receiving the appeal *in writing*. A reader could reasonably ask when a telephone appeal is treated as received and acknowledged. This is a document-clarity question for further research. The two statements alone do not establish that MCNA is rejecting oral appeals in practice.

**Representative authorization is a separate step.** The signed form in §§ 16.8 and 18.8 concerns permission for a dentist, legal counsel, or another representative to act for a member. The 2024 audit's elements 13 and 17 concerned written follow-up by the member after **the member's own oral appeal**. The signature printed on the separate state-hearing request form is also a different procedural step.

**Hearing clock.** In each v3.0 handbook, an earlier paragraph describes 120 days after completion of the appeals process. The dedicated State Fair Hearing section then names the **Notice of Appeal Resolution date**, consistent with the event at issue in audit element 28. That audit criticized two **internal policies**, which cannot be pronounced revised merely from the public handbooks.

**Continued benefits.** Both public handbooks list the authorized service/time limit among events ending continued benefits. The audit's item 30 concerned **Policy 13.209**. The handbook text is useful supporting material, with a different document role.

## What this comparison can establish

The v3.0 handbooks were publicly released on **August 12, 2025**, after the CY2024 period reviewed by HSAG but before the final report dated **December 2025**. The dates alone cannot show whether these were revisions prompted by an earlier review exchange, an independent editing cycle, or a formally approved corrective action.

The public site returned v3.0 when its pages were queried with `?v=2.5`/`?version=2.5` for Adult Denture and `?v=2.3`/`?version=2.3` for EPSDT. Those parameters did not retrieve the audited editions. No evidence of the exact historical redline, approval by LDH, mailing to members, or actual intake practice has been recovered in this round.

The comparison therefore supports a specific finding: the explicit *post-call written-submission instruction* described by HSAG is not reproduced in the inspected v3.0 appeal sections, but both newer documents retain an acknowledgment sentence framed around an appeal received in writing. The remaining questions concern clarity and real implementation.

## Availability of the audited PDFs and the CAP

The [December 2025 HSAG report](https://ldh.la.gov/assets/medicaid/EQRO/2025/Compliance/MCNA_LA_2025_CR_Report_F1.pdf), Standard XIII items 13 and 17, names the actual materials supplied for its review: `MCNA_mh-la-adult-en-v2.5` (reported pp. 21–22) and `MCNA_mh-la-epsdt-en-v2.3` (reported pp. 31–32). These are **audit citations to submitted records**, not public copies of those records.

This follow-up searched for the exact filenames, versions, publicly indexed MCNA handbook PDFs, LDH-hosted material, and historical versions offered through MCNA's current handbook pages. The original v2.5 and v2.3 PDF bytes were **not recovered**. As documented by the reproducible source script, the public `?v=` and `?version=` page queries returned the currently published v3.0, rather than the requested audited editions. The PDF hashes recorded above apply only to the **later v3.0** releases.

The HSAG report, **Section 3** (printed p. 3-1), requires MCNA to submit a corrective action plan to HSAG SAFE within 60 calendar days after receiving the final report. Its **Appendix C** (printed p. C-1) is an **unfilled CAP template**, with blanks for interventions, evaluation, responsible individuals, completion dates, approval status, and submission. It is not MCNA's completed or approved CAP.

The [LDH monetary-penalty notice of March 12, 2026](https://ldh.la.gov/assets/docs/BayouHealth/Accountability/2.0/MCNA/MCNA1-16_Notice_of_Monetary_Penalty-_2025_External_Quality_Compliance_Review_3.12.26.pdf), p. 3, instructs MCNA to complete interventions **after CAP approval** and provide completion documents through HSAG SAFE. The notice does not disclose the CAP, identify an approval date, or certify completion. A public copy of the **approved** CAP and implementation evidence was not located during this search.

These are bounded retrieval results. No absence of source publication is treated as proof that the materials were never created, submitted, or approved. In particular, the v3.0 text comparison cannot establish the exact old-to-new redline, formal CAP approval, handbook distribution, or changed member outcomes.

## Reproduce the document review

From the [repository root](../../README.md), run:

```bash
python -m pip install 'pymupdf==1.26.4'
python tools/review_mcna_handbooks.py
```

The script reads public metadata from MCNA's handbook pages, fetches both original PDFs, records their SHA-256 values, and locates the specified passages by PDF page. Its JSON output appears in `results/handbook-investigation/official-pdf-review/`. This is a source-reading aid. Interpretations in this report come from inspection of the pages themselves. The [GitHub Actions workflow](../../.github/workflows/handbook-review.yml) supports a fresh run.

For historical-document reconciliation, the highest-value remaining sources are the actual **v2.5** and **v2.3** files cited by HSAG, the approved corrective-action materials, revised policy 13.209, and distribution records.
