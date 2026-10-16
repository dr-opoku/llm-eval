"""Replay a bounded captured run offline, retaining all sample failures."""
import json
from pathlib import Path
import unittest
from llm_eval.contracts import fixture, fingerprint
from llm_eval.engine import evaluate

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT/'evidence/local-smoke-2026-10-15'

class CaseStudyTests(unittest.TestCase):
    def test_original_policy_and_all_attempts_are_retained(self):
        benchmark=json.loads((EVIDENCE/'benchmark.json').read_text())
        run=json.loads((EVIDENCE/'run.json').read_text())
        self.assertEqual(fingerprint(benchmark),fingerprint(fixture('benchmark.json')))
        self.assertEqual(run['benchmark_sha256'],fingerprint(benchmark))
        self.assertEqual([len(c['records']) for c in run['configurations']],[9,9])
        self.assertEqual(benchmark['policy']['maximum_p95_seconds'],3.0)
        self.assertIsNone(benchmark['policy']['maximum_cost_per_accepted_eur'])
        report=evaluate(benchmark,run)
        self.assertEqual(report,json.loads((EVIDENCE/'report.json').read_text()))
        self.assertEqual([c['accepted_records'] for c in report['configurations']],[2,8])
        self.assertEqual([c['boundary_requirement_failures'] for c in report['configurations']],[3,0])
        self.assertTrue(all(c['checks']['latency']=='fail' for c in report['configurations']))
        self.assertTrue(all(c['checks']['cost']=='not_required' for c in report['configurations']))
        self.assertTrue(all(c['outcome']=='does_not_meet_sample_rules' for c in report['configurations']))
        self.assertEqual(report['selection']['candidate_ids'],[])
        self.assertIsNone(report['selection']['automatic_winner'])
