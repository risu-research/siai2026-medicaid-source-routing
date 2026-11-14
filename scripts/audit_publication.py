"""Check file structure and links before archiving a release.

These checks concern repository files and metadata. Research findings are
reviewed against their sources in the accompanying evidence notes.
"""
from __future__ import annotations
import csv
import json
from pathlib import Path
import re
from urllib.parse import unquote

ROOT=Path(__file__).resolve().parents[1]
EXCLUDE={".git",".venv","work","__pycache__",".pytest_cache"}
EXTS={".md",".py",".json",".txt",".csv",".cff",".yml",".yaml"}
BROKEN=[]
COUNT={"markdown_links":0,"json_files":0,"csv_files":0,"files_scanned":0}

def checked_files():
    for p in ROOT.rglob("*"):
        if not p.is_file() or any(part in EXCLUDE for part in p.relative_to(ROOT).parts):
            continue
        if p.suffix.lower() not in EXTS and p.name!="LICENSE":
            continue
        yield p

def main():
    paths=list(checked_files())
    COUNT["files_scanned"]=len(paths)
    names={p.relative_to(ROOT).as_posix() for p in paths}
    needed={"README.md","LICENSE","CITATION.cff","ARCHIVE_AND_RELEASE.md",
            "SOURCES_AND_RIGHTS.md","requirements.txt"}
    for item in needed-names:
        BROKEN.append(f"Missing release file: {item}")
    for p in paths:
        source=p.read_text(encoding="utf-8")
        if p.suffix==".json":
            json.loads(source)
            COUNT["json_files"]+=1
        elif p.suffix==".csv":
            with p.open(newline="",encoding="utf-8") as f:
                rows=list(csv.reader(f))
            if rows:
                width=len(rows[0])
                for i,row in enumerate(rows[1:],start=2):
                    if len(row)!=width:
                        BROKEN.append(f"{p.relative_to(ROOT)}:{i} CSV width {len(row)}, expected {width}")
            COUNT["csv_files"]+=1
        elif p.suffix==".md":
            for m in re.finditer(r"\[[^\]]*\]\(([^)]+)\)",source):
                url=m.group(1).split(' "')[0].split("#")[0]
                if not url or url.startswith(("https://","http://","mailto:")):continue
                COUNT["markdown_links"]+=1
                target=(p.parent/unquote(url)).resolve()
                if not target.is_relative_to(ROOT) or not target.exists():
                    line=source[:m.start()].count("\n")+1
                    BROKEN.append(f"{p.relative_to(ROOT)}:{line} unresolved {url}")
        if re.search(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\bghp_[A-Za-z0-9]{30,}\b|\bsk-(?:proj-)?[A-Za-z0-9_-]{25,}\b",source):
            BROKEN.append(f"{p.relative_to(ROOT)}: possible credential material")
        if "/mnt/data/" in source or "sandbox:/mnt/data/" in source:
            BROKEN.append(f"{p.relative_to(ROOT)}: local workspace path")
    if BROKEN:
        for issue in BROKEN:print("FAIL",issue)
        raise SystemExit(1)
    for name,n in COUNT.items():print(f"PASS {name}: {n}")
    print("PASS release file structure")
if __name__=="__main__":
    main()
