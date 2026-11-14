"""Inspect public MCNA handbook landing pages for original PDF links.

This script reads only public page HTML and does not interact with forms.
The output helps document reproducible sources for a subsequent comparison.
"""
from __future__ import annotations

from html.parser import HTMLParser
import json
from urllib.request import Request, urlopen
from urllib.parse import urljoin
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

            data_match=re.search(r'<script\s+id="__NEXT_DATA__"[^>]*>([\s\S]*?)</script>',html)
            if data_match:
                data=json.loads(data_match.group(1))
                print("NEXT_PROPS_KEYS",list(data.get("props",{}).keys()))
                props=data.get("props",{}).get("pageProps",{})
                print("PAGE_PROPS_KEYS",list(props.keys()))
                for name,obj in props.items():
                    if isinstance(obj,dict) and any(t in name.lower() for t in ["document","version","doc","file"]):
                        print("DOC_OBJECT",name,json.dumps(obj,ensure_ascii=False)[:4000])
                    if isinstance(obj,list) and any(t in name.lower() for t in ["version","doc","file"]):
                        print("DOC_LIST",name,json.dumps(obj[:6],ensure_ascii=False)[:3000])
            chunks=[x["attrs"]["src"] for x in parsed.entries if x["tag"]=="script" and x["attrs"].get("src","").endswith(".js") and "/chunks/" in x["attrs"]["src"]]
            for js in chunks:
                try:
                    source,_=fetch(urljoin(final,js))
                    tags=[m for m in re.finditer(r'pdf|fileUrl|downloadFile|download.*api|signedUrl|/api/|webfiles|preSigned|document',source,re.I)]
                    print("CHUNK",js,"bytes",len(source),"matches",len(tags))
                    for m in tags[:10]:
                        if any(t in m.group().lower() for t in ("download","api/","webfiles","signed","fileurl")):
                            print("CHUNK_HINT",source[max(0,m.start()-120):min(len(source),m.end()+180)][:330])
                except Exception as ex:
                    print("JS_ERROR",js,str(ex)[:100])

        except Exception as exc:
            print("ERROR",key,type(exc).__name__,str(exc)[:300])
if __name__=="__main__":
    main()
