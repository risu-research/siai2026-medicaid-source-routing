"""Reconstruct the archived six-row cross-task threshold diagnostic from frozen run outputs.

Both selected thresholds are post-hoc selections within the frozen grid, never
newly tuned on transferred tasks. This script only applies the archived rules.
"""
from pathlib import Path
import json,csv
ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'work'

SETS=[('S1_action_to_warrant','nevada_heldout_results_v1.json'),('S2_finding_to_warrant','nevada_finding_to_warrant_results_v2.json'),('S3_molina_finding','molina_finding_to_warrant_results_v3.json')]
RULES=[('S1_rule_margin025','score>=0.00, margin>=0.25',0.0,0.25),('S2_rule_score022','score>=0.22, margin>=0.00',0.22,0.0)]
rows=[]
for rule,label,score_cutoff,margin_cutoff in RULES:
    for test_set,file in SETS:
        data=json.loads((WORK/file).read_text())
        records=[r for r in data['rows'] if r['method']=='tfidf_stage']
        intact=[r for r in records if r['condition']=='intact']
        removed=[r for r in records if r['condition']=='removed']
        def abstain(r):return r['selected_id'] is None or r['top_score']<score_cutoff or r['margin']<margin_cutoff
        rows.append(dict(rule=rule,source_threshold=label,test_set=test_set,
                         intact_correct=sum(not abstain(r) and r['selected_id']==r['target_id'] for r in intact),
                         intact_wrong=sum(not abstain(r) and r['selected_id']!=r['target_id'] for r in intact),
                         intact_abstain=sum(abstain(r) for r in intact), intact_n=len(intact),
                         removal_abstain=sum(abstain(r) for r in removed),
                         removal_false_substitution=sum(not abstain(r) for r in removed),removal_n=len(removed)))
with (WORK/'threshold_transfer_diagnostic.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
print('Reconstructed threshold transfer:',len(rows),'rows')
