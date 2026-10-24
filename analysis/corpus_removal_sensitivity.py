"""Sensitivity test only. Does not overwrite any frozen input or archived score.

Main result: frozen *full corpus* statistics with eligible-card masking.
Sensitivity result: refit vectorizer on corpus minus designated card.
Stage filtering stays the same. Singleton margin uses archived convention,
with second score=0, and is separately flagged as undefined top-two margin.
"""
import csv, json, re
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
FROZEN=ROOT/'data/frozen'
OUT=ROOT/'results/sensitivity'

SPECS=[('S1', 'nevada_heldout','v1','required_action',0.,.25),
       ('S2', 'nevada_finding_to_warrant','v2','finding_query',.22,0.),
       ('Molina','molina_finding_to_warrant','v3','finding_query',.22,0.)]

def norm(s):
    s=s.lower().replace('state fair hearing','sfh').replace('adverse benefit determination','abd')
    s=re.sub(r"[^a-z0-9' -]+",' ',s)
    return re.sub(r'\s+',' ',s).strip()

def make_vec():
    return TfidfVectorizer(lowercase=False,ngram_range=(1,2),sublinear_tf=True,
        norm='l2',token_pattern=r"(?u)\b[\w'-]+\b")

OUT.mkdir(parents=True, exist_ok=True)
records=[]
for label,prefix,version,query_key,st,mg in SPECS:
    data=json.loads((FROZEN/f'{prefix}_dataset_{version}.json').read_text())
    legacy=json.loads((ROOT/'results/reference'/f'{prefix}_results_{version}.json').read_text())
    cards=data['cards']; by_id={c['item_id']:c for c in cards}
    for tid in data['targets']:
        tar=by_id[tid]
        full_text=[norm(c['requirement']) for c in cards]
        fullvec=make_vec(); fullX=fullvec.fit_transform(full_text)
        # Refit only on a collection without the removed target, irrespective of stage.
        reduced=[c for c in cards if c['item_id']!=tid]
        refitvec=make_vec(); refitX=refitvec.fit_transform([norm(c['requirement']) for c in reduced])
        query=norm(tar[query_key])
        for variant,corpus,vec,X in [
            ('fixed_full_corpus',cards,fullvec,fullX),
            ('refit_without_designated',reduced,refitvec,refitX)]:
            candidates=[i for i,c in enumerate(corpus)
                        if c['stage']==tar['stage'] and c['role']=='warrant' and c['item_id']!=tid]
            assert candidates
            sims=cosine_similarity(vec.transform([query]),X[candidates]).ravel()
            order=np.argsort(-sims,kind='mergesort')
            top=float(sims[order[0]])
            second=float(sims[order[1]]) if len(order)>1 else 0.
            margin=top-second
            abstain=top<st or margin<mg
            row=dict(task=label,target_id=tid,stage=tar['stage'],variant=variant,
                selection_id=corpus[candidates[int(order[0])]]['item_id'],n_candidates=len(candidates),
                top_score=top,second_score=second,margin=margin,
                singleton_margin_convention=len(candidates)==1,
                threshold_score=st,threshold_margin=mg,
                removal_abstained=abstain)
            records.append(row)
            if variant=='fixed_full_corpus':
                old=next(z for z in legacy['rows'] if z['target_id']==tid and
                    z['method']=='tfidf_stage' and z['condition']=='removed')
                assert row['selection_id']==old['selected_id'],(label,tid,'selected')
                for key in ['top_score','second_score','margin']:
                    assert abs(row[key]-old[key])<1e-10, (label,tid,key,row[key],old[key])

with (OUT/'refit_sensitivity_rows.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)

summary=[]
for task in ['S1','S2','Molina']:
    for variant in ['fixed_full_corpus','refit_without_designated']:
        rows=[r for r in records if r['task']==task and r['variant']==variant]
        summary.append(dict(task=task,variant=variant,removal_abstained=sum(r['removal_abstained'] for r in rows),
            removal_n=len(rows),singleton_targets=[r['target_id'] for r in rows if r['singleton_margin_convention']],
            false_accept_targets=[r['target_id'] for r in rows if not r['removal_abstained']]))

(OUT/'refit_sensitivity_summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
