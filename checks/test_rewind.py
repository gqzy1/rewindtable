"""Local scripted-host checks; these do not establish network consensus."""
import itertools
import json
import pathlib
import types
import unittest
import copy


def load():
    class Return:
        def __init__(self, value):
            self.calldata = value
    class Contract:
        def __new__(cls):
            o = super().__new__(cls)
            o.books, o.totals = {}, {}
            return o
    h = types.SimpleNamespace(public=types.SimpleNamespace(view=lambda f:f,write=lambda f:f),
        Contract=Contract,message=types.SimpleNamespace(sender_address="0xabc"),queue=[])
    def prompt(*args, **kwargs):
        v=h.queue.pop(0)
        if isinstance(v,Exception):
            raise v
        return copy.deepcopy(v)
    def nondet(leader,validator):
        v=leader()
        h.validator=validator
        if not validator(Return(v)):
            raise Exception("DISAGREEMENT")
        return v
    h.vm=types.SimpleNamespace(Return=Return,run_nondet_unsafe=nondet)
    h.nondet=types.SimpleNamespace(exec_prompt=prompt)
    ns={"gl":h,"TreeMap":dict,"u32":int}
    p=pathlib.Path(__file__).resolve().parents[1]/"src/rewindtable.py"
    exec(compile(p.read_text().replace("from genlayer import *",""),str(p),"exec"),ns)
    return ns,h


SPEC={"modes":["idle","held","ready"],"actions":[
    {"name":"hold","forward":"idle becomes held; otherwise disabled.","undo":"held becomes idle; otherwise disabled."},
    {"name":"prepare","forward":"held becomes ready; otherwise disabled.","undo":"ready becomes held; otherwise disabled."}]}
GOOD={"tables":[{"forward":[1,-1,-1],"undo":[-1,0,-1]},{"forward":[-1,2,-1],"undo":[-1,-1,1]}]}


class RewindTests(unittest.TestCase):
    def setUp(self):
        self.n,self.h=load()
        self.c=self.n["RewindTable"]()
    def ready(self):
        self.c.register("x",json.dumps(SPEC))
        self.h.queue=[GOOD,GOOD]
        return json.loads(self.c.verify("x",0))
    def test_reverse_order_restores_original(self):
        b=self.ready()
        self.c.start("x",1,b["certificate"],0)
        self.c.step("x",2,0)
        self.c.step("x",3,1)
        b=json.loads(self.c.rewind("x",4))
        self.assertEqual((b["phase"],b["current"]),("ROLLING_BACK",1))
        with self.assertRaisesRegex(Exception,"NOT_RUNNING"):
            self.c.step("x",5,0)
        b=json.loads(self.c.rewind("x",5))
        self.assertEqual((b["phase"],b["current"],b["stack"]),("RESTORED",0,[]))
        self.assertEqual([x["action"] for x in b["events"]],[0,1,1,0])
    def test_all_three_mode_total_map_pairs(self):
        # Independent oracle exhaustively checks 729 forward/undo map pairs.
        for f in itertools.product(range(3),repeat=3):
            for u in itertools.product(range(3),repeat=3):
                r=self.n["roundtrips"]({"tables":[{"forward":list(f),"undo":list(u)}]})
                self.assertEqual(r["result"]=="REVERSIBLE",all(u[f[x]]==x for x in range(3)))
    def test_lossy_forward_has_counterexample(self):
        r=self.n["roundtrips"]({"tables":[{"forward":[2,2,-1],"undo":[-1,-1,0]}]})
        self.assertEqual(r["result"],"BROKEN")
        self.assertIn({"action":0,"before":1,"after":2,"restored":0},r["counterexamples"])
    def test_unknown_blocks_certification(self):
        a=copy.deepcopy(GOOD)
        a["tables"][0]["undo"][2]=-2
        self.assertEqual(self.n["roundtrips"](a)["result"],"UNCERTAIN")
    def test_inert_is_not_reversible(self):
        self.assertEqual(self.n["roundtrips"]({"tables":[{"forward":[-1,-1],"undo":[-1,-1]}]})["result"],"INERT")
    def test_disagreement_keeps_draft(self):
        self.c.register("x",json.dumps(SPEC))
        a=copy.deepcopy(GOOD);a["tables"][0]["forward"][0]=2
        self.h.queue=[GOOD,a]
        with self.assertRaisesRegex(Exception,"DISAGREEMENT"):
            self.c.verify("x",0)
        self.assertEqual(json.loads(self.c.book("0xabc","x"))["phase"],"DRAFT")
    def test_revision_and_identity_guards(self):
        b=self.ready()
        with self.assertRaisesRegex(Exception,"STALE_REVISION"):
            self.c.start("x",0,b["certificate"],0)
        with self.assertRaisesRegex(Exception,"NOT_CERTIFIED"):
            self.c.start("x",1,"wrong",0)
        self.h.message.sender_address="0xdef"
        with self.assertRaisesRegex(Exception,"BOOK_MISSING"):
            self.c.start("x",1,b["certificate"],0)
    def test_disabled_action_does_not_advance(self):
        b=self.ready();self.c.start("x",1,b["certificate"],0)
        with self.assertRaisesRegex(Exception,"ACTION_DISABLED"):
            self.c.step("x",2,1)
        self.assertEqual(json.loads(self.c.book("0xabc","x"))["revision"],2)
    def test_finished_book_cannot_rewind(self):
        b=self.ready();self.c.start("x",1,b["certificate"],0);self.c.step("x",2,0)
        self.c.finish("x",3)
        with self.assertRaisesRegex(Exception,"NOT_REVERSIBLE_NOW"):
            self.c.rewind("x",4)
    def test_model_error_is_not_uncertain(self):
        self.c.register("x",json.dumps(SPEC));self.h.queue=[RuntimeError("down")]
        with self.assertRaisesRegex(RuntimeError,"down"):
            self.c.verify("x",0)
        self.assertEqual(json.loads(self.c.book("0xabc","x"))["revision"],0)
    def test_boolean_mode_and_duplicate_json_rejected(self):
        with self.assertRaisesRegex(Exception,"DUPLICATE_JSON_KEY"):
            self.n["read_json"]('{"a":1,"a":2}')
        a=copy.deepcopy(GOOD);a["tables"][0]["forward"][0]=True
        with self.assertRaisesRegex(Exception,"INTEGER_LIMIT"):
            self.n["tables"](a,SPEC)


if __name__=="__main__":
    unittest.main(verbosity=2)
