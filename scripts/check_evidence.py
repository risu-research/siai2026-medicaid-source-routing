"""Check the public evidence ledger for consistent coverage and source references."""
from __future__ import annotations

import csv
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "evidence" / "louisiana" / "correction_ledger.csv"
EXPECTED = {"6", "13", "17", "28", "30", "37"}
ACTIONS = {"CHECK", "REMOVE", "MOVE", "ADD_FOR_REVIEW"}


def main() -> None:
    with LEDGER.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or [])
        required = {
            "item_id", "review_result", "observed_issue", "review_action",
            "change_or_check", "preserve", "primary_audit_source",
            "additional_authority", "records_to_verify", "source_status",
        }
        if not required <= fields:
            raise ValueError(f"Missing columns: {sorted(required - fields)}")
        rows = list(reader)

    ids = [r["item_id"].strip() for r in rows]
    if len(ids) != 6 or set(ids) != EXPECTED or len(ids) != len(set(ids)):
        raise ValueError(f"Expected one row per audited item: {sorted(EXPECTED)}")
    for row in rows:
        item = row["item_id"]
        for field in required:
            if not (row.get(field) or "").strip():
                raise ValueError(f"Item {item}: missing {field}")
        if row["review_result"] != "Not Met":
            raise ValueError(f"Item {item}: unexpected review result")
        if row["review_action"] not in ACTIONS:
            raise ValueError(f"Item {item}: unexpected research category")
        src = urlparse(row["primary_audit_source"])
        if src.scheme != "https" or src.hostname != "ldh.la.gov":
            raise ValueError(f"Item {item}: expected Louisiana government audit URL")
    if any(r["review_action"] != "REMOVE" for r in rows if r["item_id"] in {"13", "17"}):
        raise ValueError("Items 13 and 17 must retain their shared correction type")
    print("PASS: six Louisiana items, required fields, sources, and action categories")


if __name__ == "__main__":
    main()
