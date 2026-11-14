"""Collect source-page locations from executed MCNA amendments.

This is a source-extraction aid, not a decision about contract validity.
Government PDFs are fetched live and kept outside version control.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "evidence" / "louisiana" / "mcna_official_source_registry.csv"
DEFAULT = ["3","4","5","8","9","10"]
PATTERN = re.compile(r"\b2\s*\.\s*10\s*\.\s*(?:3|7)(?:\s*\.\s*\d+)*\b|\b(?:appeals?|grievances?|fair hearings?|continued benefits|written confirmation)\b", re.I)
CLAUSE = re.compile(r"\b2\s*\.\s*10\s*\.\s*(?:3|7)(?:\s*\.\s*\d+)*\b")

def get_pdf(url, local_path=None):
    if local_path and local_path.is_file():
        return local_path.read_bytes(), "local"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; RISU-research-source-inventory/1.0)", "Accept": "application/pdf,*/*"})
    with urlopen(req, timeout=65) as res:
        data = res.read(55_000_001)
        if len(data) > 55_000_000:raise ValueError("PDF exceeds 55MB source limit")
        return data, "official-url"

def run(only, out, local_dir=None):
    import fitz
    with REGISTRY.open(newline="", encoding="utf-8") as f:
        known = {r["amendment"]:r for r in csv.DictReader(f)}
    out.mkdir(parents=True, exist_ok=True)
    manifest=[]; snippets=[]
    for n in only:
        if n not in known: raise ValueError("Unknown amendment: " + n)
        item=known[n]
        url=item["official_pdf"]
        row={"amendment":n,"url":url,"status":"unavailable","source_mode":None,"sha256":None,"pdf_pages":0,"candidate_hits":0,"error":None}
        try:
            path=(local_dir / (n + ".pdf")) if local_dir else None
            b,mode=get_pdf(url,path)
            if not b.startswith(b"%PDF-"):raise ValueError("Expected a PDF response")
            pdf=fitz.open(stream=b, filetype="pdf")
            row.update(status="read",source_mode=mode,sha256=hashlib.sha256(b).hexdigest(),pdf_pages=len(pdf))
            for i,page in enumerate(pdf):
                txt=page.get_text("text",sort=True)
                normalized=re.sub(r"\s+", " ",txt)
                for match in PATTERN.finditer(normalized):
                    before=normalized[max(0,match.start()-85):match.start()]
                    after=normalized[match.end():match.end()+185]
                    context=before+normalized[match.start():match.end()]+after
                    clause=CLAUSE.search(context)
                    snippets.append({"amendment":n,"pdf_page":i+1,"match":match.group(),"near_clause":clause.group() if clause else "","excerpt":context.strip()})
            row["candidate_hits"]=sum(v["amendment"]==n for v in snippets)
            if row["candidate_hits"]==0:row["status"]="read_no_matches"
        except (ValueError,HTTPError,URLError,TimeoutError,OSError,RuntimeError) as ex:
            row["error"]=str(ex)[:250]
        manifest.append(row)
        print(f"{n}: {row['status']}; pages={row['pdf_pages']}; candidate_hits={row['candidate_hits']}; sha256={row['sha256'] or '-'}; error={row['error'] or '-'}",flush=True)
        for m in [x for x in snippets if x["amendment"]==n and (x["near_clause"] or "appeal" in x["match"].lower())][:6]:
            print("  page",m["pdf_page"],"term",m["match"],"context",m["excerpt"][:180],flush=True)
    (out/"source_manifest.json").write_text(json.dumps({"purpose":"locate possible clause passages for manual comparison","files":manifest},indent=2)+"\n",encoding="utf8")
    with (out/"candidate_passages.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=["amendment","pdf_page","match","near_clause","excerpt"]);w.writeheader();w.writerows(snippets)
    print("Summary:",sum(x["status"].startswith("read") for x in manifest),"read;",len(snippets),"candidate passages. Manual review required.")
    return 0 if all(x["status"].startswith("read") for x in manifest) else 2

if __name__=="__main__":
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--only",nargs="+",default=DEFAULT,help="Amendment numbers to inspect")
    ap.add_argument("--output",type=Path,default=ROOT/"results"/"contracts"/"scan")
    ap.add_argument("--local-dir",type=Path,help="Folder with N.pdf files, for offline inspection")
    ar=ap.parse_args()
    sys.exit(run(ar.only,ar.output,ar.local_dir))
