"""Review structured claims against source metadata, scope, and dates.

The source catalog is curated from public agency records. PASS checks the
declared metadata relationship; it does not independently verify PDF text.
"""
from __future__ import annotations
import argparse
from datetime import date
import json
from pathlib import Path
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
KINDS = {"documentary","operative_authority","enforcement","implementation","audit_to_enforcement"}

def load_json(path):
    obj=json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(obj,dict) or obj.get("schema_version")!=1:
        raise ValueError("Unsupported schema: "+str(path))
    return obj

def check_claim(claim,sources):
    issues=[]; review=[]
    ident=claim.get("id","(unnamed)")
    source=sources.get(claim.get("source_id"))
    if source is None:
        return {"id":ident,"status":"REJECT","reasons":["Unknown source ID"]}
    if claim.get("kind") not in KINDS:issues.append("Unknown claim kind")
    for field in ("jurisdiction","program"):
        if claim.get(field)!=source.get(field):
            issues.append(field+" differs from source scope")
    if claim.get("stage") not in source.get("stages",[]):
        issues.append("Procedural stage differs from source scope")
    u=urlparse(source.get("url",""))
    if u.scheme!="https" or not u.hostname:issues.append("Missing HTTPS source URL")
    key=claim.get("key")
    if key not in source.get("facts",{}):
        issues.append("No source fact for "+str(key))
    elif type(claim.get("value")) is not type(source["facts"][key]) or claim.get("value")!=source["facts"][key]:
        issues.append("Value differs from cited source fact")
    kind=claim.get("kind")
    if kind=="operative_authority":
        if source.get("kind") not in {"contract","contract_amendment","regulation"}:
            issues.append("Operative authority needs a legal source")
        try:
            day=date.fromisoformat(claim["as_of"])
            start=date.fromisoformat(source["effective_from"]) if source.get("effective_from") else None
            through=date.fromisoformat(source["verified_through"]) if source.get("verified_through") else None
            if start is None or day<start:issues.append("Decision predates effective date")
            elif through is None or day>through:
                review.append("Complete operative authority chain unverified for this date")
        except (KeyError,ValueError,TypeError):
            issues.append("Missing or invalid operative date")
    if kind=="enforcement":
        if source.get("kind")!="enforcement_notice":
            issues.append("Enforcement claim requires an enforcement notice")
        if claim.get("allocation")!=source.get("assessment_scope"):
            issues.append("Penalty allocation exceeds notice scope")
    if kind=="implementation" and source.get("kind")!="implementation_record":
        issues.append("Implementation requires a service or implementation record")
    if kind=="audit_to_enforcement":
        other=sources.get(claim.get("linked_source_id"))
        if source.get("kind")!="audit_report" or other is None or other.get("kind")!="enforcement_notice":
            issues.append("Chain needs an audit and an enforcement notice")
        else:
            if any(source.get(x)!=other.get(x) for x in ("jurisdiction","program","review_start","review_end")):
                issues.append("Audit and notice cover different periods or programs")
            if not source.get("issued") or not other.get("issued") or other["issued"]<source["issued"]:
                issues.append("Notice must follow the audit")
            if claim.get("stage") not in other.get("stages",[]):
                issues.append("Linked source covers a different procedural stage")
            k=claim.get("linked_key")
            if k not in other.get("facts",{}) or type(claim.get("linked_value")) is not type(other["facts"].get(k)) or claim.get("linked_value")!=other["facts"].get(k):
                issues.append("Linked fact differs from notice")
            if claim.get("allocation")!=other.get("assessment_scope"):
                issues.append("Aggregate penalty scope mismatch")
    reasons=issues or review or ["Claim and source metadata agree"]
    return {"id":ident,"status":"REJECT" if issues else "REVIEW" if review else "PASS","reasons":reasons}

def check_all(claims,sources):
    mapping={}
    for s in sources:
        if not s.get("id") or s["id"] in mapping:raise ValueError("Source IDs must be unique")
        mapping[s["id"]]=s
    seen=set(); results=[]
    for c in claims:
        if not c.get("id") or c["id"] in seen:raise ValueError("Claim IDs must be unique")
        seen.add(c["id"]); results.append(check_claim(c,mapping))
    return results

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--sources",type=Path,default=ROOT/"evidence/claims/sources.json")
    p.add_argument("--claims",type=Path,default=ROOT/"evidence/claims/claims.json")
    p.add_argument("--json",action="store_true")
    p.add_argument("--require-cleared",action="store_true")
    args=p.parse_args(argv)
    try: results=check_all(load_json(args.claims)["claims"],load_json(args.sources)["sources"])
    except (ValueError,KeyError,TypeError,OSError) as exc:
        print("Invalid input: "+str(exc),file=sys.stderr);return 2
    if args.json:print(json.dumps({"decisions":results},indent=2))
    else:
        for r in results:print(r["status"].ljust(7),r["id"],":","; ".join(r["reasons"]))
        print("Summary:",*(f"{s}={sum(r['status']==s for r in results)}" for s in ("PASS","REVIEW","REJECT")))
    return 2 if any(r["status"]=="REJECT" or args.require_cleared and r["status"]=="REVIEW" for r in results) else 0

if __name__=="__main__":sys.exit(main())
