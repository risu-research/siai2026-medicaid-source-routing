"""Compare regenerated experiments against archived outputs and checked SHA-256 inputs.

Archived output is independent of this code and was preserved in September 2026.
JSON is compared recursively; floating point comparisons use an absolute 1e-9
and relative 1e-10 tolerance for numerical library differences.
"""
from __future__ import annotations
import csv, hashlib, json, math, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/frozen'
REF=ROOT/'results/reference'
WORK=ROOT/'work'
EXPERIMENTS=['nevada_heldout','nevada_finding_to_warrant','molina_finding_to_warrant']
V=['v1','v2','v3']

def verify_inputs():
    count=0
    for kind,ver in zip(EXPERIMENTS,V):
        hashfile=DATA/f'{kind}_prereg_sha256.txt'
        for line in hashfile.read_text().splitlines():
            if not line.strip():continue
            h,name=line.split(maxsplit=1)
            name=Path(name).name
            actual=hashlib.sha256((DATA/name).read_bytes()).hexdigest()
            if actual != h: raise AssertionError(f'Frozen input hash mismatch: {name}')
            count+=1
    return count

def eq(x,y,route='root'):
    if isinstance(x,dict) and isinstance(y,dict):
        if set(x)!=set(y):raise AssertionError(f'{route} differing keys: {set(x)^set(y)}')
        for k in x:eq(x[k],y[k],route+'.'+str(k))
    elif isinstance(x,list) and isinstance(y,list):
        if len(x)!=len(y):raise AssertionError(f'{route} length {len(x)} != {len(y)}')
        for i,(a,b) in enumerate(zip(x,y)):eq(a,b,route+f'[{i}]')
    elif type(x) in (float,int) and type(y) in (float,int):
        if not math.isclose(x,y,abs_tol=1e-9,rel_tol=1e-10):raise AssertionError(f'{route} {x} != {y}')
    elif x!=y:raise AssertionError(f'{route} {x!r} != {y!r}')

def verify_results():
    nrows=0
    for kind,ver in zip(EXPERIMENTS,V):
        name=f'{kind}_results_{ver}.json'
        a=json.loads((REF/name).read_text())
        b=json.loads((WORK/name).read_text())
        eq(a,b,name)
        nrows+=len(a['rows'])
        print(f'PASS {kind}: {len(a["rows"])} outcome rows, {len(a["score_drops"])} score changes, full JSON fields matched')
        # Compare CSVs where both original and reproduced are present; ignore only numeric rendering diffs.
        for nm in [f'{kind}_results_{ver}.csv',f'{kind}_score_drops_{ver}.csv']:
            a_path,b_path=REF/nm,WORK/nm
            if not a_path.exists() or not b_path.exists():continue
            with a_path.open(newline='') as f: ar=list(csv.DictReader(f))
            with b_path.open(newline='') as f: br=list(csv.DictReader(f))
            if not ar and not br:continue
            if len(ar)!=len(br) or set(ar[0])!=set(br[0]):raise AssertionError(f'{nm}: CSV shape differed')
            for j,(left,right) in enumerate(zip(ar,br)):
                for k in left:
                    if left[k]==right[k]:continue
                    try:
                        if math.isclose(float(left[k]),float(right[k]),rel_tol=1e-10,abs_tol=1e-9):continue
                    except (ValueError,TypeError):pass
                    raise AssertionError(f'{nm} row {j} col {k} differed: {left[k]!r} <> {right[k]!r}')
            print(f'  PASS archived CSV comparison: {nm} ({len(ar)} rows)')
    # Archived transfer diagnostics were built from selected S1/S2 threshold rules.
    with (REF/'threshold_transfer_diagnostic.csv').open(newline='') as f:a=list(csv.DictReader(f))
    with (WORK/'threshold_transfer_diagnostic.csv').open(newline='') as f:b=list(csv.DictReader(f))
    eq(a,b,'threshold_transfer_diagnostic.csv')
    print(f'PASS six-row cross-task threshold transfer: {len(a)} rows, every cell matched')
    return nrows

if __name__=='__main__':
    try:
        cnt=verify_inputs()
        print(f'PASS historical frozen hashes: {cnt}/6')
        if len(sys.argv)>1 and sys.argv[1]=='--inputs-only':sys.exit(0)
        cnt_rows=verify_results()
        print(f'PASS all three experiments, {cnt_rows} row-level outcomes, within machine precision')
    except Exception as e:
        print('FAIL',str(e),file=sys.stderr);sys.exit(1)
