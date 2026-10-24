import json, math, re, csv, hashlib
from pathlib import Path
from collections import Counter
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE=Path(__file__).resolve().parents[1] / 'work'
dataset=json.loads((BASE/'nevada_finding_to_warrant_dataset_v2.json').read_text())
protocol=json.loads((BASE/'nevada_finding_to_warrant_protocol_v2.json').read_text())

cards=dataset['cards']
target_ids=dataset['targets']
card_by_id={c['item_id']:c for c in cards}

def norm(s):
    s=s.lower().replace('state fair hearing','sfh').replace('adverse benefit determination','abd')
    s=re.sub(r"[^a-z0-9' -]+",' ',s)
    s=re.sub(r'\s+',' ',s).strip()
    return s

# fixed TF-IDF corpus fit on candidate cards only; queries transform against same fixed vocabulary
corpus=[norm(c['requirement']) for c in cards]
vec=TfidfVectorizer(lowercase=False, ngram_range=(1,2), sublinear_tf=True, norm='l2', token_pattern=r"(?u)\b[\w'-]+\b")
X=vec.fit_transform(corpus)
idx_by_id={c['item_id']:i for i,c in enumerate(cards)}

# BM25 fixed corpus stats
bm_docs=[norm(c['requirement']).split() for c in cards]
N=len(bm_docs); avgdl=sum(map(len,bm_docs))/N
DF=Counter()
for d in bm_docs:
    for t in set(d): DF[t]+=1
k1=1.5; b=0.75

def bm25_scores(query, candidate_indices):
    q=norm(query).split(); scores=[]
    for i in candidate_indices:
        d=bm_docs[i]; tf=Counter(d); dl=len(d); score=0.0
        for t in q:
            if t not in DF: continue
            idf=math.log(1+(N-DF[t]+0.5)/(DF[t]+0.5))
            f=tf[t]
            score += idf * (f*(k1+1))/(f+k1*(1-b+b*dl/avgdl)) if f else 0.0
        scores.append(score)
    return np.array(scores,float)

def tfidf_scores(query, candidate_indices):
    qv=vec.transform([norm(query)])
    return cosine_similarity(qv, X[candidate_indices]).ravel()

def candidates_for(target, removed=None, stage=False):
    out=[]
    for i,c in enumerate(cards):
        if removed is not None and c['item_id']==removed: continue
        if stage and c['stage']!=target['stage']: continue
        if c['role']!='warrant': continue
        out.append(i)
    return out

def rank(method,target,removed=None,stage=False):
    cand=candidates_for(target,removed,stage)
    if not cand: return None
    scores=tfidf_scores(target['finding_query'],cand) if method=='tfidf' else bm25_scores(target['finding_query'],cand)
    order=np.argsort(-scores, kind='mergesort')
    top=cand[int(order[0])]; top_score=float(scores[order[0]])
    second_score=float(scores[order[1]]) if len(order)>1 else 0.0
    return {
        'selected_id':cards[top]['item_id'], 'selected_stage':cards[top]['stage'],
        'top_score':top_score,'second_score':second_score,'margin':top_score-second_score,
        'num_candidates':len(cand)
    }

def verified_id(target,removed=None,stage=False,item_id_override=None):
    qid=target['item_id'] if item_id_override is None else item_id_override
    for i in candidates_for(target,removed,stage):
        if cards[i]['item_id']==qid:
            return {'selected_id':qid,'selected_stage':cards[i]['stage'],'top_score':None,'second_score':None,'margin':None,'num_candidates':len(candidates_for(target,removed,stage))}
    return {'selected_id':None,'selected_stage':None,'top_score':None,'second_score':None,'margin':None,'num_candidates':len(candidates_for(target,removed,stage))}

rows=[]
methods=[('tfidf_all','tfidf',False),('tfidf_stage','tfidf',True),('bm25_all','bm25',False),('bm25_stage','bm25',True)]
for tid in target_ids:
    t=card_by_id[tid]
    for label,alg,stage in methods:
        for condition,removed in [('intact',None),('removed',tid)]:
            r=rank(alg,t,removed=removed,stage=stage)
            rows.append({'target_id':tid,'target_stage':t['stage'],'method':label,'condition':condition, **r,
                         'correct': (r['selected_id']==tid if condition=='intact' else r['selected_id'] is None),
                         'false_substitution': (condition=='removed' and r['selected_id'] is not None)})
    for label,stage in [('verified_id',False),('stage_plus_verified_id',True)]:
        for condition,removed in [('intact',None),('removed',tid)]:
            r=verified_id(t,removed=removed,stage=stage)
            rows.append({'target_id':tid,'target_stage':t['stage'],'method':label,'condition':condition, **r,
                         'correct': (r['selected_id']==tid if condition=='intact' else r['selected_id'] is None),
                         'false_substitution': (condition=='removed' and r['selected_id'] is not None)})

# corrupted-ID secondary diagnostic: nearest extant item numerically, prefer lower on ties
allids=sorted(card_by_id)
corrupt=[]
for tid in target_ids:
    t=card_by_id[tid]
    others=[x for x in allids if x!=tid]
    bad=min(others,key=lambda x:(abs(x-tid),x))
    for stage in [False,True]:
        r=verified_id(t,removed=None,stage=stage,item_id_override=bad)
        corrupt.append({'target_id':tid,'corrupted_id':bad,'stage_filter':stage,'selected_id':r['selected_id'],
                        'misrouted':r['selected_id'] is not None and r['selected_id']!=tid,
                        'abstained':r['selected_id'] is None})

# threshold frontier on tfidf all and tfidf stage. Applied symmetrically to intact and removed scores.
frontier=[]
for label,stage in [('tfidf_all',False),('tfidf_stage',True)]:
    ints={r['target_id']:r for r in rows if r['method']==label and r['condition']=='intact'}
    rems={r['target_id']:r for r in rows if r['method']==label and r['condition']=='removed'}
    for st_i in range(101):
        st=st_i/100
        for mg_i in range(51):
            mg=mg_i/100
            intact_correct_answered=0; intact_abstain=0; removed_abstain=0; removed_sub=0
            for tid in target_ids:
                a=ints[tid]
                abst=(a['top_score']<st or a['margin']<mg)
                if abst: intact_abstain+=1
                elif a['selected_id']==tid: intact_correct_answered+=1
                brr=rems[tid]
                abst2=(brr['top_score']<st or brr['margin']<mg)
                if abst2: removed_abstain+=1
                else: removed_sub+=1
            if intact_correct_answered>=7:
                frontier.append({'method':label,'score_threshold':st,'margin_threshold':mg,
                                 'intact_correct_answered':intact_correct_answered,'intact_abstain':intact_abstain,
                                 'removed_abstain':removed_abstain,'removed_false_substitution':removed_sub})
# choose max removed abstention, then max intact, then lowest thresholds (most conservative reporting tie-break)
best={}
for label in ['tfidf_all','tfidf_stage']:
    fs=[x for x in frontier if x['method']==label]
    fs.sort(key=lambda x:(-x['removed_abstain'],-x['intact_correct_answered'],x['score_threshold']+x['margin_threshold'],x['score_threshold'],x['margin_threshold']))
    best[label]=fs[0] if fs else None

# per-target score drops
score_drops=[]
for label in ['tfidf_all','tfidf_stage','bm25_all','bm25_stage']:
    for tid in target_ids:
        a=next(r for r in rows if r['method']==label and r['condition']=='intact' and r['target_id']==tid)
        brr=next(r for r in rows if r['method']==label and r['condition']=='removed' and r['target_id']==tid)
        score_drops.append({'method':label,'target_id':tid,'intact_selected':a['selected_id'],'removed_selected':brr['selected_id'],
                            'intact_score':a['top_score'],'removed_score':brr['top_score'],
                            'score_drop':a['top_score']-brr['top_score'],'intact_margin':a['margin'],'removed_margin':brr['margin'],
                            'substitution_distance':None if brr['selected_id'] is None else abs(tid-brr['selected_id'])})

summary={}
for m in sorted(set(r['method'] for r in rows)):
    ints=[r for r in rows if r['method']==m and r['condition']=='intact']
    rem=[r for r in rows if r['method']==m and r['condition']=='removed']
    summary[m]={
        'intact_exact':sum(r['selected_id']==r['target_id'] for r in ints),
        'intact_n':len(ints),
        'removed_abstain':sum(r['selected_id'] is None for r in rem),
        'removed_false_substitution':sum(r['selected_id'] is not None for r in rem),
        'removed_n':len(rem)
    }

out={
    'dataset_sha256':hashlib.sha256((BASE/'nevada_finding_to_warrant_dataset_v2.json').read_bytes()).hexdigest(),
    'protocol_sha256':hashlib.sha256((BASE/'nevada_finding_to_warrant_protocol_v2.json').read_bytes()).hexdigest(),
    'summary':summary,
    'best_prespecified_threshold_frontier':best,
    'rows':rows,
    'score_drops':score_drops,
    'corrupted_identifier':corrupt
}
# RECONSTRUCTED S2 RUNNER: preserve the archived S2 output schema.
# This is adapted from frozen S1 source, not claimed as recovered original S2 source.
for _r in rows:
    for _k in ('target_stage', 'selected_stage', 'correct', 'false_substitution'):
        _r.pop(_k, None)
for _r in score_drops:
    _r.pop('substitution_distance', None)
out['best_frontier']={k:[k, v['score_threshold'], v['margin_threshold'], v['intact_correct_answered'], v['removed_abstain']] if v is not None else None for k,v in best.items()}
out.pop('best_prespecified_threshold_frontier', None)
out.pop('corrupted_identifier', None)

(BASE/'nevada_finding_to_warrant_results_v2.json').write_text(json.dumps(out,indent=2))

with open(BASE/'nevada_finding_to_warrant_results_v2.csv','w',newline='') as f:
    fields=list(rows[0].keys()); w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
with open(BASE/'nevada_finding_to_warrant_score_drops_v2.csv','w',newline='') as f:
    fields=list(score_drops[0].keys()); w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(score_drops)

# concise report
lines=[]
lines.append('# Nevada Held-out Exact-Warrant Removal Test — Results\n')
lines.append('Frozen dataset SHA-256: `'+out['dataset_sha256']+'`  ')
lines.append('Frozen protocol SHA-256: `'+out['protocol_sha256']+'`\n')
lines.append('## Aggregate results\n')
lines.append('| Method | Intact exact | Removal abstain | Removal false substitution |')
lines.append('|---|---:|---:|---:|')
for m in ['tfidf_all','tfidf_stage','bm25_all','bm25_stage','verified_id','stage_plus_verified_id']:
    s=summary[m]; lines.append(f"| {m} | {s['intact_exact']}/{s['intact_n']} | {s['removed_abstain']}/{s['removed_n']} | {s['removed_false_substitution']}/{s['removed_n']} |")
lines.append('\n## Prespecified threshold frontier\n')
for m in ['tfidf_all','tfidf_stage']:
    lines.append(f"- **{m}**: {best[m]}")
lines.append('\n## Per-target exact-warrant removal (TF-IDF stage-constrained)\n')
lines.append('| Target | Intact pick | Removed pick | Intact score | Removed score | Score drop | Removed margin |')
lines.append('|---:|---:|---:|---:|---:|---:|---:|')
for d in [x for x in score_drops if x['method']=='tfidf_stage']:
    lines.append(f"| {d['target_id']} | {d['intact_selected']} | {d['removed_selected']} | {d['intact_score']:.3f} | {d['removed_score']:.3f} | {d['score_drop']:.3f} | {d['removed_margin']:.3f} |")
lines.append('\n## Corrupted identifier diagnostic\n')
mis=sum(x['misrouted'] for x in corrupt); abst=sum(x['abstained'] for x in corrupt)
lines.append(f"Across {len(corrupt)} corrupted-ID trials (with and without stage filtering), exact-ID lookup misrouted {mis} and abstained {abst}. This is a secondary adversarial diagnostic, not part of the primary confirmatory result.")
(BASE/'nevada_finding_to_warrant_report_v2.md').write_text('\n'.join(lines))
print('\n'.join(lines))
