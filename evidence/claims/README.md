# Claim and source checks

This small command-line tool checks declared facts against a catalog of public agency documents. It handles document identity, program, jurisdiction, procedural stage, authority coverage dates, and the scope of enforcement records.

From the repository root:

    python tools/check_claims.py
    python tools/check_claims.py --json
    python -m unittest discover -s tests -v

For your own records:

    python tools/check_claims.py --sources path/to/sources.json --claims path/to/claims.json

A result of **PASS** means that the value and scope agree with the declared source metadata. **REVIEW** marks a missing contract authority chain. **REJECT** marks an incompatible source, factual value, program, stage, date, or monetary allocation. The default command exits successfully when the published example contains an open review. Add --require-cleared to require every claim to pass.

The sample has seven PASS results and one REVIEW. The open claim asks whether language removed by the 2021 amendment remained operative for the specified obligation in June 2024.

Fourteen tests change values and document relationships deliberately. They cover an incorrect program, procedural stage, review year, source identity, penalty amount, grievance-only penalty allocation, a claimed receipt of payment, and unverified service delivery. The original studies remain available separately.

**Source facts are currently curated by the researcher.** The checker tests consistency with those entries. Before use for independent legal verification, the catalog entries must be checked against their original government documents, including exact passage and version identity. The next development stage will add machine-verifiable text anchors and document-level evidence.
