# MCNA member handbooks after the CY2024 audit

The [2025 MCNA compliance review](https://ldh.la.gov/assets/medicaid/EQRO/2025/Compliance/MCNA_LA_2025_CR_Report_F1.pdf) assessed the plan's calendar-year 2024 operations. Under Standard XIII, HSAG found that the Adult Denture and EPSDT handbooks asked members to submit a written appeal after filing orally. The reviewed editions were Adult Denture **v2.5**, pp. 21–22, and EPSDT **v2.3**, pp. 31–32. The auditor instructed MCNA to remove the follow-up requirement.

MCNA's public handbook site now carries English v3.0 editions, both dated August 12, 2025. Their wording gives a view of the later public instructions. The audit-cited v2.5 and v2.3 PDFs were unavailable in the public sources reviewed, so the precise wording changes between editions remain untraced.

## Later public editions

| Handbook | Release date | Official PDF | PDF pages | SHA-256 |
| --- | --- | --- | ---: | --- |
| [Adult Denture v3.0](https://handbooks.mcna.net/mh-la-adult-en) | Aug. 12, 2025 | [MCNA PDF](https://handbooks.mcna.net/api/files/download/689b778236f3559579d5933a) | 40 | `c5e3ac8843f0b77a6aa4c227c3dfce181acf4dcf48f7cfa6b41ef727a7f03b9f` |
| [EPSDT v3.0](https://handbooks.mcna.net/mh-la-epsdt-en) | Aug. 12, 2025 | [MCNA PDF](https://handbooks.mcna.net/api/files/download/689b770836f3559579d5679e) | 48 | `5cc2ce95128c72d9fdc8eb937a8cf9db01d1e8b27b462f36dada10bb55d785c5` |

The hashes identify the PDF bytes retrieved from MCNA's public download service on November 14, 2026. Both PDF page numbers and printed handbook pages are recorded below.

## Appeal instructions in v3.0

| Question | Adult Denture | EPSDT | Reading |
| --- | --- | --- | --- |
| Filing an ordinary appeal | § 16.1, PDF p. 25, printed p. 23 | § 18.1, PDF p. 33, printed p. 31 | Members are directed to call the hotline to request an appeal |
| Acknowledging receipt | § 16.3, PDF p. 25, printed p. 23 | § 18.3, PDF p. 33, printed p. 31 | Both descriptions begin “After we receive your appeal in writing” |
| Appointing a representative | § 16.8, PDF p. 26, printed p. 24 | § 18.8, PDF p. 34, printed p. 32 | A signed authorization permits another person to act for a member |
| State fair hearing | § 18.1, PDF p. 28, printed p. 26 | § 20.1, PDF p. 36, printed p. 34 | Both use the date on MCNA's Notice of Appeal Resolution for the 120-day filing period |
| Continued benefits | § 16.6, PDF pp. 25–26, printed pp. 23–24 | § 18.6, PDF pp. 33–34, printed pp. 31–32 | The service authorization's time period or limit appears among the ending events |

### Filing by telephone and receiving an acknowledgment

Both editions permit members to request an ordinary appeal by telephone. Neither inspected appeal section instructs the caller to send a subsequent written appeal. The acknowledgment paragraphs, however, begin by describing receipt of an appeal **in writing**. A person appealing by phone could find the acknowledgment procedure unclear. Member intake and acknowledgment records would show how the instruction was applied.

The signed permission form in §§ 16.8 and 18.8 concerns authorized representatives. That form and the separate State Fair Hearing request form serve different purposes from a member's oral appeal.

### Hearing deadline and continued benefits

The hearing sections give the filing deadline as 120 days from the date on the **Notice of Appeal Resolution**. A shorter summary elsewhere in both handbooks refers to completion of MCNA's appeal process. The dedicated hearing section identifies the actual notice.

The original audit's item 28 concerned **two internal policies** using the initial adverse-benefit notice as the starting event. The later handbook wording offers an additional source for the correct date; revised internal policies would supply the direct evidence of that correction.

Both v3.0 handbooks describe the approved time or service limit among the events ending continued benefits. The audit's item 30 concerned internal **Policy 13.209**, for which a dated revised copy would be the next useful record.

## Document dates and CAP records

The public v3.0 editions were released on **August 12, 2025**, before HSAG's final report in **December 2025**. Earlier review exchanges, internal revisions and the state approval process would be needed to reconstruct how those editions came about.

The HSAG report's **Section 3**, printed p. 3-1, calls for a corrective action plan within 60 calendar days of receipt of the final report. **Appendix C**, printed p. C-1, contains the blank submission template. The completed and approved plan was unavailable among the public materials searched.

The [March 12, 2026 LDH penalty notice](https://ldh.la.gov/assets/docs/BayouHealth/Accountability/2.0/MCNA/MCNA1-16_Notice_of_Monetary_Penalty-_2025_External_Quality_Compliance_Review_3.12.26.pdf), p. 3, requires MCNA to submit completion documentation after the CAP is approved. The approved plan, approval date, handbook distribution records and completed intervention reports remain useful source targets.

MCNA's current public pages returned v3.0 when queried using `?v=2.5` or `?version=2.5` for Adult Denture, and `?v=2.3` or `?version=2.3` for EPSDT. The original audited editions were therefore inaccessible through those public URL parameters. Their absence from this retrieval leaves the historical redline and formal correction sequence open.

## Source reproduction

```bash
python -m pip install 'pymupdf==1.26.4'
python tools/review_mcna_handbooks.py
```

The [source script](../../tools/review_mcna_handbooks.py) reads public version metadata, downloads the two PDFs, computes SHA-256 fingerprints and reports the matching PDF pages. It writes a local JSON record under `results/handbook-investigation/official-pdf-review/`. The [GitHub Actions workflow](../../.github/workflows/handbook-review.yml) runs the same procedure.

The [observation CSV](handbook_observations_2025.csv) carries the page references and document dates for reuse.
