"""CLI, defensive consumer and local runner tests; all model requests mocked."""
import copy
import hashlib
import importlib.util
import io
import json
import os
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from llm_eval import runner
from llm_eval.cli import main, _checkpoint, _protect_output
from llm_eval.contracts import fixture, fingerprint
from llm_eval.demo import demonstration
from llm_eval.engine import evaluate

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('consumer', ROOT/'scripts/inspect_report.py')
consumer = importlib.util.module_from_spec(spec);spec.loader.exec_module(consumer)


class InterfaceTests(unittest.TestCase):
    def setUp(self):
        self.benchmark = fixture('benchmark.json')
        self.run = demonstration(self.benchmark)

    def cli(self, args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = main(args)
        return code, out.getvalue(), err.getvalue()

    def test_demo_cli_exit_status(self):
        self.assertEqual(self.cli(['demo', '--format', 'json', '--require-candidate'])[0], 0)
        self.assertEqual(self.cli(['demo', '--scenario', 'incomplete', '--require-candidate'])[0], 1)
        self.assertEqual(self.cli(['demo', '--scenario', 'incomplete'])[0], 0)
        code, out, _ = self.cli(['evaluate', '/nonexistent/run.json', '--format', 'json'])
        self.assertEqual(code, 2);self.assertEqual(json.loads(out)['status'], 'error')

    def test_saved_run_replays_and_report_is_written(self):
        with TemporaryDirectory() as directory:
            run, report = Path(directory)/'run.json', Path(directory)/'report.html'
            self.assertEqual(self.cli(['demo', '--save-run', str(run), '--output', str(report), '--format', 'html'])[0], 0)
            self.assertIn('<!doctype html>', report.read_text())
            self.assertEqual(self.cli(['evaluate', str(run)])[0], 0)

    def test_deeply_nested_answer_still_produces_complete_cli_report(self):
        nested = '{"x":' + '[' * 100_000 + '0' + ']' * 100_000 + '}'
        for raw in (nested, '```json\n' + nested + '\n```'):
            with self.subTest(fenced=raw.startswith('```')), TemporaryDirectory() as directory:
                run = copy.deepcopy(self.run)
                record = run['configurations'][1]['records'][0]
                record['response'] = raw
                record['response_sha256'] = hashlib.sha256(raw.encode()).hexdigest()
                path = Path(directory) / 'run.json'
                path.write_text(json.dumps(run))
                before = path.read_bytes()
                code, out, err = self.cli(['evaluate', str(path), '--format', 'json'])
                self.assertEqual(code, 0)
                self.assertEqual(err, '')
                report = json.loads(out)
                self.assertEqual(len(report['configurations']), 3)
                self.assertEqual(report['configurations'][1]['reason_counts']['invalid_json'], 1)
                self.assertEqual(path.read_bytes(), before)

    def test_all_input_path_aliases_refused_without_mutation(self):
        for alias in ('same', 'symlink', 'hardlink'):
            with self.subTest(alias=alias), TemporaryDirectory() as directory:
                path = Path(directory)/'run.json';path.write_text(json.dumps(self.run))
                target = path if alias == 'same' else Path(directory)/'alias.json'
                if alias == 'symlink': target.symlink_to(path)
                if alias == 'hardlink': os.link(path, target)
                before = path.read_bytes()
                code, out, _ = self.cli(['evaluate', str(path), '--output', str(target), '--format', 'json'])
                self.assertEqual(code, 2);self.assertIn('overwrite', json.loads(out)['message'])
                self.assertEqual(path.read_bytes(), before)

    def test_benchmark_and_demo_save_report_collisions_refused(self):
        benchmark = ROOT/'llm_eval/fixtures/benchmark.json';before = benchmark.read_bytes()
        for args in (['demo', '--save-run', str(benchmark)], ['demo', '--output', str(benchmark)]):
            self.assertEqual(self.cli(args)[0], 2)
            self.assertEqual(benchmark.read_bytes(), before)
        with TemporaryDirectory() as directory:
            path = Path(directory)/'same.json'
            self.assertEqual(self.cli(['demo', '--save-run', str(path), '--output', str(path)])[0], 2)
            self.assertFalse(path.exists())
            with self.assertRaises(ValueError): _protect_output(benchmark, [benchmark])
            with patch.object(runner, 'collect', side_effect=AssertionError('must not collect')):
                self.assertEqual(self.cli(['run', '--model', 'fake', '--output', str(benchmark)])[0], 2)

    def test_atomic_checkpoint_preserves_json_and_leaves_no_pending_files(self):
        with TemporaryDirectory() as directory:
            target = Path(directory)/'run.json';_checkpoint(target, self.run)
            self.assertEqual(json.loads(target.read_text()), self.run)
            self.assertEqual([p.name for p in Path(directory).iterdir()], ['run.json'])

    def test_consumer_synthetic_and_incomplete(self):
        for scenario, expected in [('comparison', 'sample_rules_met'), ('incomplete', 'insufficient_evidence')]:
            report = evaluate(self.benchmark, demonstration(self.benchmark, scenario))
            result = consumer.inspect_report(report)
            self.assertEqual(result['assessment'], expected)
            self.assertFalse(result['action_authorized'])

    def test_consumer_rejects_overclaims_and_hidden_failures(self):
        changes = [lambda r:r.update(schema_version='2.0'),
                   lambda r:r.update(deployment_readiness='ready'),
                   lambda r:r['selection'].update(automatic_winner='sample-careful'),
                   lambda r:r['selection'].update(candidate_ids=['sample-fluent']),
                   lambda r:r['configurations'][2]['checks'].update(boundary_cases='pass'),
                   lambda r:r['configurations'][1]['checks'].pop('latency'),
                   lambda r:r['configurations'][1].update(expected_records=0),
                   lambda r:r['configurations'][1]['latency'].update(complete=False),
                   lambda r:r['configurations'][1]['checks'].update(latency='not_required')]
        for change in changes:
            report = evaluate(self.benchmark, self.run);change(report)
            with self.assertRaises(ValueError): consumer.inspect_report(report)

    def test_consumer_cli_error_and_unknown_exit_codes(self):
        with TemporaryDirectory() as directory:
            path = Path(directory)/'report.json'
            for scenario, code in [('comparison', 0), ('incomplete', 1)]:
                path.write_text(json.dumps(evaluate(self.benchmark, demonstration(self.benchmark, scenario))))
                with redirect_stdout(io.StringIO()): self.assertEqual(consumer.main([str(path)]), code)
            for text in ('NaN', '{"x":1,"x":2}', '[]', '{', '{"schema_version":"1.0","status":"error"}'):
                path.write_text(text)
                with redirect_stdout(io.StringIO()): self.assertEqual(consumer.main([str(path)]), 2)

    def test_endpoint_allows_only_numeric_loopback_origins(self):
        for url in ('http://127.0.0.1:11434', 'http://[::1]:11434/'):
            self.assertTrue(runner._endpoint(url))
        for url in ('http://example.com', 'http://localhost:11434', 'https://127.0.0.1', 'http://127.0.0.1/path', 'http://u:p@127.0.0.1', 'http://127.0.0.1?x=1', 'http://127.0.0.1:99999'):
            with self.subTest(url=url), self.assertRaises(ValueError): runner._endpoint(url)

    def test_redirect_handler_refuses_redirects(self):
        with self.assertRaises(ValueError):
            runner._NoRedirect().redirect_request(None, None, 302, '', {}, 'http://example.com')

    def test_http_call_disables_environment_proxy_and_preserves_transport(self):
        with patch.object(runner, 'build_opener') as builder:
            response = builder.return_value.open.return_value.__enter__.return_value
            response.read.return_value = b'{"done":true,"response":"OK"}'
            result, raw, _, error = runner._call('http://127.0.0.1:11434', '/api/generate', {'x':1}, 1)
            handlers = builder.call_args.args
            self.assertEqual(handlers[0].proxies, {})
            self.assertIsInstance(handlers[1], runner._NoRedirect)
            self.assertTrue(result['done']);self.assertIn('OK', raw);self.assertIsNone(error)

    def test_collect_records_every_failure_no_retry_and_never_sends_answer_key(self):
        calls, checkpoints = [], []
        def fake(endpoint, path, payload, timeout):
            calls.append((path, payload))
            if path == '/api/version': return {'version':'test'}, '{}', .01, None
            if path == '/api/show': return {'details':{}}, '{}', .01, None
            if payload['prompt'] == 'Reply exactly OK.': return {'done':True, 'response':'OK'}, '{"done":true}', .1, None
            return None, None, 1.0, 'TimeoutError'
        with patch.object(runner, '_call', side_effect=fake):
            run = runner.collect(self.benchmark, ['fake'], attempts=1, timeout=1, checkpoint=lambda r:checkpoints.append(copy.deepcopy(r)))
        config = run['configurations'][0]
        self.assertEqual(len(config['records']), 9)
        self.assertTrue(all(r['status'] == 'error' and r['cost_eur'] is None for r in config['records']))
        self.assertEqual(len(calls), 14) # inventory + show + 3 probes + 9 tasks
        self.assertEqual(config['parameters']['selected_mode'], 'fast')
        self.assertTrue(checkpoints[-1]['provenance']['finished_at'])
        for record, case in zip(config['records'], self.benchmark['cases']):
            self.assertEqual(record['request']['prompt'], case['input'])
            self.assertEqual(record['request']['system'], self.benchmark['instructions'])
            self.assertNotIn('expected', record['request'])
            self.assertEqual(record['request_sha256'], fingerprint(record['request']))
            self.assertEqual(record['request']['keep_alive'], 0)
        self.assertEqual(evaluate(self.benchmark, run)['configurations'][0]['execution_errors'], 9)
