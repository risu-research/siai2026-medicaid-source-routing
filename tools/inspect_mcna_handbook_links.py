"""Inspect public MCNA handbook landing pages for original PDF links.

This script reads only public page HTML and does not interact with forms.
The output helps document reproducible sources for a subsequent comparison.
"""
from __future__ import annotations

from html.parser import HTMLParser
import json
from urllib.request import Request, urlopen
import re

PAGES = {
    "adult": "https://handbooks.mcna.net/mh-la-adult-en",
    "epsdt": "https://handbooks.mcna.net/mh-la-epsdt-en",
}
KEYWORDS = ("pdf", "download", "webfiles", "fileurl", "file_url", "file_path",
            "viewfile", "downloadfile", "version", "202508", "api/", "__next_data__")

class Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.entries=[]
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag in {"a","script","iframe","meta","link","button","object","embed","form"}:
            self.entries.append({"tag":tag,"attrs":attrs})

def fetch(url):
    req=Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; RISU public-document research/1.0)"})
    with urlopen(req,timeout=25) as res:
        return res.read(4_000_000).decode("utf8",errors="replace"),res.geturl()

def main():
    for key,url in PAGES.items():
        try:
            html, final=fetch(url)
            parsed=Tags()
            parsed.feed(html)
            print("\n###",key,"bytes",len(html),"resolved",final)
            print("HTML_START",html[:1200].replace("\n"," ") )
            print("TAGS",json.dumps(parsed.entries[:120],ensure_ascii=False)[:16000])
            interesting=[m for m in re.finditer(r"pdf|webfiles|download|document\.|s3|file_url|\\.js|appData|blob",html,re.I)]
            print("MATCH_COUNT",len(interesting))
            for m in interesting[:60]:
                print("TEXT_CONTEXT",html[max(0,m.start()-155):min(len(html),m.end()+280)].replace("\n"," ")[:480])
        except Exception as exc:
            print("ERROR",key,type(exc).__name__,str(exc)[:300])
if __name__=="__main__":
    main()
