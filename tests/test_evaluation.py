"""Offline adversarial tests of task grading, denominators, costs and evidence."""
import copy
import hashlib
import json
import math
import unittest
from llm_eval.contracts import fixture, fingerprint, number, parse_json, validate_benchmark
from llm_eval.demo import demonstration
from llm_eval.engine import evaluate, grade
from llm_eval.report import render


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.benchmark = fixture("benchmark.json")
        self.run = demonstration(self.benchmark)

    def test_fractional_aggregates_are_reproducible(self):
        report = evaluate(self.benchmark, self.run)
        for config, item in zip(self.run["configurations"], report["configurations"]):
            costs = [record["cost_eur"] for record in config["records"]]
            timings = [record["elapsed_seconds"] for record in config["records"]]
            self.assertEqual(item["cost"]["observed_total_eur"], math.fsum(costs))
            self.assertEqual(item["cost"]["cost_per_accepted_eur"], math.fsum(costs) / item["accepted_records"])
            self.assertEqual(item["latency"]["mean_seconds"], math.fsum(value / len(timings) for value in timings))

    def test_finite_individual_costs_with_overflowing_total_are_rejected(self):
        for record in self.run["configurations"][0]["records"]:
            record["cost_eur"] = 1e308
        with self.assertRaisesRegex(ValueError, "total cost exceeds"):
            evaluate(self.benchmark, self.run)

    def test_comparison_and_repeat_denominator(self):
        report = evaluate(self.benchmark, self.run)
        self.assertEqual(report['selection']['candidate_ids'], ['sample-careful'])
        self.assertIsNone(report['selection']['automatic_winner'])
        for item, accepted in zip(report['configurations'], [21, 27, 24]):
            self.assertEqual(item['accepted_records'], accepted)
            self.assertEqual(item['distinct_cases'], 9)
            self.assertEqual(item['expected_records'], 27)
        self.assertEqual(report['configurations'][2]['checks']['boundary_cases'], 'fail')
        self.assertEqual(report['configurations'][2]['checks']['case_acceptance'], 'pass')

    def test_every_expected_answer_is_accepted(self):
        for case in self.benchmark['cases']:
            self.assertTrue(grade(case, json.dumps(case['expected']))['accepted'])

    def test_fences_diagnosed_not_accepted(self):
        case = self.benchmark['cases'][0]
        result = grade(case, '```json\n' + json.dumps(case['expected']) + '\n```')
        self.assertTrue(result['diagnostic_fenced_json'])
        self.assertTrue(result['schema_valid'])
        self.assertFalse(result['accepted'])

    def test_strict_shape_boolean_and_huge_number(self):
        case = self.benchmark['cases'][0]
        for key, value in [('units', True), ('unit_price_eur', True), ('unit_price_eur', 10**400), ('unit_price_eur', float('inf'))]:
            answer = copy.deepcopy(case['expected']);answer['fields'][key] = value
            with self.subTest(key=key, value=str(value)[:30]):
                self.assertFalse(grade(case, json.dumps(answer))['accepted'])
        with self.assertRaises(ValueError):
            number(10**400, 'huge')

    def test_duplicate_keys_and_nonfinite_constants(self):
        for raw in ('{"x":1,"x":2}', 'NaN', 'Infinity', '-Infinity'):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                parse_json(raw)

    def test_wrong_fields_evidence_and_decision_are_separate(self):
        case = self.benchmark['cases'][0]
        mutations = [('fields_match_failed', lambda a:a['fields'].update(supplier='Invented')),
                     ('decision_match_failed', lambda a:a.update(decision='reject')),
                     ('evidence_match_failed', lambda a:a.update(evidence_ids=['invented']))]
        for reason, mutate in mutations:
            answer = copy.deepcopy(case['expected']);mutate(answer)
            self.assertIn(reason, grade(case, json.dumps(answer))['reason_codes'])

    def test_nonempty_reason_is_not_truth_checked(self):
        case = self.benchmark['cases'][0];answer = copy.deepcopy(case['expected'])
        answer['reason'] = 'An intentionally false explanation, not graded as true.'
        self.assertTrue(grade(case, json.dumps(answer))['accepted'])
        answer['reason'] = ''
        self.assertFalse(grade(case, json.dumps(answer))['accepted'])

    def test_impossible_distinct_minimum_rejected(self):
        self.benchmark['policy']['minimum_distinct_cases'] = 10
        with self.assertRaisesRegex(ValueError, 'cannot exceed'):
            validate_benchmark(self.benchmark)

    def test_invalid_policies_and_duplicate_cases(self):
        for change in (lambda b:b['cases'].append(copy.deepcopy(b['cases'][0])),
                       lambda b:b['policy'].update(minimum_pass_rate=True),
                       lambda b:b['policy'].update(maximum_cost_per_accepted_eur=10**400)):
            benchmark = copy.deepcopy(self.benchmark);change(benchmark)
            with self.assertRaises(ValueError):
                validate_benchmark(benchmark)

    def test_fingerprint_and_record_hash_mismatch(self):
        run = copy.deepcopy(self.run);run['benchmark_sha256'] = '0'*64
        with self.assertRaises(ValueError): evaluate(self.benchmark, run)
        run = copy.deepcopy(self.run);run['configurations'][0]['records'][0]['response_sha256'] = '0'*64
        with self.assertRaises(ValueError): evaluate(self.benchmark, run)

    def test_duplicate_cells_ids_and_unknown_case(self):
        for change in (lambda r:r['configurations'][0]['records'].__setitem__(1, copy.deepcopy(r['configurations'][0]['records'][0])),
                       lambda r:r['configurations'][1].update(configuration_id='sample-fast'),
                       lambda r:r['configurations'][0]['records'][0].update(case_id='unknown')):
            run = copy.deepcopy(self.run);change(run)
            with self.assertRaises(ValueError): evaluate(self.benchmark, run)

    def test_missing_matrix_never_candidate(self):
        self.run['configurations'] = [self.run['configurations'][1]]
        self.run['configurations'][0]['records'].pop()
        item = evaluate(self.benchmark, self.run)['configurations'][0]
        self.assertEqual(item['outcome'], 'insufficient_evidence')
        self.assertEqual(item['missing_records'], 1)
        self.assertEqual(item['accepted_records'], 26)

    def test_empty_run_records_and_incomplete_demo(self):
        self.run['configurations'][1]['records'] = []
        item = evaluate(self.benchmark, self.run)['configurations'][1]
        self.assertEqual(item['outcome'], 'insufficient_evidence')
        self.assertIsNone(item['observed_acceptance_rate'])
        report = evaluate(self.benchmark, demonstration(self.benchmark, 'incomplete'))
        self.assertFalse(report['selection']['candidate_ids'])

    def test_execution_failures_are_counted_without_grading_as_success(self):
        record = self.run['configurations'][1]['records'][0]
        record['status'] = 'error'
        item = evaluate(self.benchmark, self.run)['configurations'][1]
        self.assertEqual(item['accepted_records'], 26)
        self.assertEqual(item['execution_errors'], 1)
        self.assertEqual(item['reason_counts']['execution_error'], 1)
        self.assertEqual(item['latency']['observations'], 27)

    def test_partial_timing_unknown_but_observed_failure_visible(self):
        config = self.run['configurations'][2];config['records'][0]['elapsed_seconds'] = None
        item = evaluate(self.benchmark, self.run)['configurations'][2]
        self.assertEqual(item['checks']['latency'], 'unknown')
        self.assertEqual(item['checks']['boundary_cases'], 'fail')
        self.assertEqual(item['outcome'], 'insufficient_evidence')

    def with_required_cost(self, ceiling=.004):
        self.benchmark['policy']['maximum_cost_per_accepted_eur'] = ceiling
        self.run['benchmark_sha256'] = fingerprint(self.benchmark)

    def test_cost_accounts_for_all_attempts_and_unrounded_boundary(self):
        self.with_required_cost()
        report = evaluate(self.benchmark, self.run)
        fast = report['configurations'][0]
        self.assertAlmostEqual(fast['cost']['cost_per_accepted_eur'], 27*.001/21)
        careful = report['configurations'][1]
        # Floating-point sums are assessed as supplied; choose an exact boundary for this case.
        self.benchmark['policy']['maximum_cost_per_accepted_eur'] = careful['cost']['cost_per_accepted_eur']
        self.run['benchmark_sha256'] = fingerprint(self.benchmark)
        self.assertEqual(evaluate(self.benchmark, self.run)['configurations'][1]['checks']['cost'], 'pass')
        self.benchmark['policy']['maximum_cost_per_accepted_eur'] -= 1e-12
        self.run['benchmark_sha256'] = fingerprint(self.benchmark)
        self.assertEqual(evaluate(self.benchmark, self.run)['configurations'][1]['checks']['cost'], 'fail')

    def test_partial_cost_unknown_not_zero(self):
        self.with_required_cost();self.run['configurations'][1]['records'][0]['cost_eur'] = None
        item = evaluate(self.benchmark, self.run)['configurations'][1]
        self.assertEqual(item['checks']['cost'], 'unknown')
        self.assertIsNone(item['cost']['cost_per_accepted_eur'])

    def test_zero_accepted_complete_cost_fails_but_ratio_null(self):
        self.with_required_cost()
        for record in self.run['configurations'][1]['records']:
            record['status'] = 'error'
        item = evaluate(self.benchmark, self.run)['configurations'][1]
        self.assertEqual(item['checks']['cost'], 'fail')
        self.assertEqual(item['outcome'], 'does_not_meet_sample_rules')
        self.assertIsNone(item['cost']['cost_per_accepted_eur'])

    def test_invalid_record_numbers(self):
        for key, value in [('elapsed_seconds', True), ('cost_eur', 10**400), ('output_tokens', -1)]:
            run = copy.deepcopy(self.run);run['configurations'][0]['records'][0][key] = value
            with self.assertRaises(ValueError): evaluate(self.benchmark, run)

    def test_html_escapes_untrusted_labels_and_has_no_external_assets(self):
        self.run['configurations'][0]['configuration_id'] = '<script>alert(1)</script>'
        page = render(evaluate(self.benchmark, self.run), 'html')
        self.assertIn('&lt;script&gt;', page)
        self.assertNotIn('<script>', page)
        self.assertIn("default-src 'none'", page)

    def test_json_roundtrip(self):
        report = evaluate(self.benchmark, self.run)
        self.assertEqual(json.loads(render(report, 'json')), report)
