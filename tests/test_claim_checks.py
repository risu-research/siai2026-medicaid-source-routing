"""Mutation checks for real document metadata and its declared relationships."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from check_claims import load_json,check_all,check_claim

S={s["id"]:s for s in load_json(ROOT/"evidence/claims/sources.json")["sources"]}
C={c["id"]:c for c in load_json(ROOT/"evidence/claims/claims.json")["claims"]}

class SourceScopeTests(unittest.TestCase):
    def mutation(self,ident,field,value,status):
        c=deepcopy(C[ident]);c[field]=value
        self.assertEqual(check_claim(c,S)["status"],status)
    def test_example(self):
        results=check_all(list(C.values()),list(S.values()))
        self.assertEqual(sum(r["status"]=="PASS" for r in results),7)
        self.assertEqual(sum(r["status"]=="REVIEW" for r in results),1)
    def test_unknown_id(self):self.mutation("2021-change","source_id","unknown","REJECT")
    def test_wrong_jurisdiction(self):self.mutation("colorado","jurisdiction","Louisiana","REJECT")
    def test_wrong_program(self):self.mutation("colorado","program","MCNA Dental","REJECT")
    def test_wrong_stage(self):self.mutation("2021-change","stage","care_coordination","REJECT")
    def test_future_authority(self):self.mutation("2024-operative","as_of","2020-01-01","REJECT")
    def test_unknown_authority_chain(self):self.mutation("2024-operative","as_of","2024-01-01","REVIEW")
    def test_penalty_overattribution(self):self.mutation("penalty","allocation","grievance_only","REJECT")
    def test_payment_not_reported(self):self.mutation("penalty","key","amount_paid","REJECT")
    def test_penalty_amount(self):self.mutation("penalty","value",5000,"REJECT")
    def test_implementation_not_verified(self):self.mutation("colorado","kind","implementation","REJECT")
    def test_wrong_linked_source(self):self.mutation("audit-to-penalty","linked_source_id","co_review","REJECT")
    def test_wrong_review_period(self):
        ss=deepcopy(S);ss["la_notice"]["review_end"]="2025-12-31"
        self.assertEqual(check_claim(C["audit-to-penalty"],ss)["status"],"REJECT")
    def test_false_claim_fails(self):self.mutation("handbook","value",False,"REJECT")

if __name__=="__main__":unittest.main()
