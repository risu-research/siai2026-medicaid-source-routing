"""Locate appeal passages in public MCNA Louisiana member handbooks.

The script downloads official current PDFs and records provenance and
page locations. Source-text findings need human interpretation.
"""
from __future__ import annotations
from html import unescape
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "handbook-investigation" / "official-pdf-review"
PAGES = {
    "adult": ("https://handbooks.mcna.net/mh-la-adult-en", "2.5"),
    "epsdt": ("https://handbooks.mcna.net/mh-la-epsdt-en", "2.3"),
}
PASSAGES = {
    "ordinary_appeal_by_phone": r"can call our Member Hotline[^.]{0,100}ask for an appeal",
    "acknowledgment_after_written_appeal": r"After we receive your appeal in writing",
    "state_hearing_notice_date": r"within\s*120 days of the date on MCNA.s Notice of Appeal Resolution",
    "hearing_after_appeal_completion": r"120 days after the completion of MCNA.s appeals process",
    "authorized_service_limit": r"The time period or service limits of a previously authorized service has been met",
    "authorized_representative_consent": r"one-page form that you must sign and return to us stating that you give permission",
}
def fetch(url):
    req = Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; RISU-source-research/1.0)"})
    with urlopen(req,timeout=40) as response:
        b = response.read(12_000_001)
        if len(b)>12_000_000:raise ValueError("Source exceeds 12 MB")
        return b
def metadata(url):
    html=fetch(url).decode("utf-8",errors="replace")
    m=re.search(r'<script id="__NEXT_DATA__" type="application/json">([\s\S]*?)</script>',html)
    if not m:raise ValueError("No public document-version metadata found")
    f=json.loads(unescape(m.group(1)))["props"]["pageProps"]["file"]
    version=f["version"]
    return {"title":f["title"],"version":version["number"],"date":version["date"],"version_id":version["_id"]}
def read_pdf(pdf):
    import fitz
    if not pdf.startswith(b"%PDF"):raise ValueError("The response is not a PDF")
    doc=fitz.open(stream=pdf,filetype="pdf")
    locators={}
    for name,pattern in PASSAGES.items():
        occurrences=[]
        for i,page in enumerate(doc):
            raw=page.get_text("text")
            text=re.sub(r"\s+"," ",raw)
            printed=re.search(r"\bPage\s+(\d+)\b",raw)
            for match in list(re.finditer(pattern,text,re.I))[:3]:
                occurrences.append({
                  "pdf_page":i+1,
                  "printed_page":int(printed.group(1)) if printed else None,
                  "excerpt":text[max(0,match.start()-50):min(len(text),match.end()+80)],
                })
        locators[name]=occurrences
    return len(doc),locators
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    results={}
    for key,(url,audited) in PAGES.items():
        page=metadata(url)
        endpoint="https://handbooks.mcna.net/api/files/download/"+page["version_id"]
        pdf=fetch(endpoint)
        count,passages=read_pdf(pdf)
        queries={}
        for param in ("v","version"):
            try:
                queries[param]=metadata(url+"?"+urlencode({param:audited}))["version"]
            except Exception as ex:
                queries[param]="unavailable: "+type(ex).__name__
        results[key]={
            "source_page":url,
            "official_pdf_url":endpoint,
            "public_metadata":page,
            "audit_identified_prior_version":audited,
            "pdf_sha256":hashlib.sha256(pdf).hexdigest(),
            "pdf_pages":count,
            "page_locators":passages,
            "old_version_query_results":queries,
            "method":"Exact source-text location. Human reading required for interpretation.",
        }
        print(f"{key}: version={page['version']} pages={count} sha256={results[key]['pdf_sha256']}",flush=True)
        for name,hits in passages.items():
            print(" ",name,":",[(x["pdf_page"],x["printed_page"]) for x in hits],flush=True)
        print(" old-version public URL probes:",queries,flush=True)
    target=OUT/"official_pdf_evidence.json"
    target.write_text(json.dumps(results,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("Wrote",target)
    return 0
if __name__=="__main__":sys.exit(main())
