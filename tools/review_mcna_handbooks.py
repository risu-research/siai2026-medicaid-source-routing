"""Retrieve official public MCNA handbook PDFs and collect appeal passages.

No PDF bytes are committed. Output includes source identities, hashes, and
short page-level excerpts for research review; it is not a legal verdict.
"""
from __future__ import annotations
from html import unescape
import hashlib
import os
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlencode, urljoin
from urllib.request import Request, urlopen

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"results"/"handbook-investigation"/"official-pdf-review"
PAGES={
  "adult":{"url":"https://handbooks.mcna.net/mh-la-adult-en","audited":"2.5"},
  "epsdt":{"url":"https://handbooks.mcna.net/mh-la-epsdt-en","audited":"2.3"},
}
PATS={
 "oral_appeal":r"\b(?:oral|verbally?|phone|telephone)\b.{0,135}\bappeal|\bappeal.{0,135}\b(?:oral|verbally?|phone|telephone)\b",
 "written_appeal":r"\bappeal.{0,100}\b(?:in writing|written|follow.?up|sign(?:ed|ature)?)\b|\b(?:in writing|written|follow.?up).{0,110}\bappeal\b",
 "fair_hearing":r"\b(?:fair hearing|hearing).{0,145}\b(?:120|days|notice|appeal)\b|\b(?:120 calendar days).{0,145}\b(?:hearing|appeal)\b",
 "benefits":r"\b(?:continued|continuation|authorized).{0,135}\b(?:benefits|services|limits)\b|\b(?:services|benefits).{0,140}\b(?:continu(?:e|ed)|limit)\b",
}
def fetch(url):
    req=Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; RISU public-source-research/1.0)","Accept":"application/pdf,text/html,*/*"})
    with urlopen(req,timeout=35) as res:
        data=res.read(12_000_001)
        if len(data)>12_000_000:raise ValueError("Document over 12 MB limit")
        return data,res.geturl(),res.headers.get("Content-Type","")
def next_info(url):
    raw,actual,ctype=fetch(url)
    text=raw.decode("utf8",errors="replace")
    m=re.search(r'<script id="__NEXT_DATA__" type="application/json">([\s\S]*?)</script>',text)
    if not m:raise RuntimeError("Public page did not expose document metadata")
    j=json.loads(unescape(m.group(1)))
    f=j["props"]["pageProps"]["file"]
    v=f["version"]
    return {"title":f["title"],"slug":f["slug"],"version":v["number"],"id":v["_id"],"date":v["date"],"page_url":actual}
def extract_pdf(pdf):
    import fitz
    if not pdf.startswith(b"%PDF"):raise ValueError("API response was not PDF")
    doc=fitz.open(stream=pdf,filetype="pdf")
    hits=[]
    for idx,page in enumerate(doc):
        text=re.sub(r"\s+"," ",page.get_text("text"))
        for kind,pattern in PATS.items():
            matches=list(re.finditer(pattern,text,re.I))
            for m in matches[:7]:
                excerpt=text[max(0,m.start()-85):min(len(text),m.end()+145)].strip()
                hits.append({"pdf_page":idx+1,"kind":kind,"excerpt":excerpt})
    return len(doc),hits
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    results={}
    for key,cfg in PAGES.items():
        official=next_info(cfg["url"])
        api=urljoin(cfg["url"],"/api/files/download/"+official["id"])
        row={"landing":official,"audited_version":cfg["audited"],"pdf_api":api}
        try:
            binary,final,ctype=fetch(api)
            pages,hits=extract_pdf(binary)
            if os.environ.get("RISU_SAVE_REVIEW_PDFS")=="1":
                (OUT/(key+"_v3.pdf")).write_bytes(binary)
            row.update(pdf_status="read",pdf_pages=pages,sha256=hashlib.sha256(binary).hexdigest(),matches=hits,pdf_content_type=ctype)
            print("OFFICIAL",key,"version",official["version"],"pages",pages,"bytes",len(binary),"sha256",row["sha256"],"matches",len(hits),flush=True)
            for hit in hits:
                if hit["kind"] in ("oral_appeal","written_appeal","fair_hearing"):
                    print("  PAGE",hit["pdf_page"],hit["kind"],hit["excerpt"][:290],flush=True)
        except Exception as exc:
            row.update(pdf_status="unavailable",pdf_error=f"{type(exc).__name__}: {exc}"[:450])
            print("OFFICIAL_ERROR",key,row["pdf_error"],flush=True)
        old=[]
        for option in ("v","version"):
            try:
                historic=next_info(cfg["url"]+"?"+urlencode({option:cfg["audited"]}))
                old.append({"parameter":option,"version":historic["version"],"id":historic["id"],"date":historic["date"]})
                print("HISTORY",key,option,"requested",cfg["audited"],"returned",historic["version"],"id",historic["id"],flush=True)
            except Exception as exc:
                old.append({"parameter":option,"error":f"{type(exc).__name__}: {exc}"[:170]})
        row["public_history_queries"]=old
        results[key]=row
    path=OUT/"official_pdf_evidence.json"
    path.write_text(json.dumps(results,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("Written",path,flush=True)
    return 0 if all(v.get("pdf_status")=="read" for v in results.values()) else 2
if __name__=="__main__":sys.exit(main())
