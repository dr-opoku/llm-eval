"""Reproduce stored reports offline; never recollect model responses."""
import argparse
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from llm_eval.contracts import fixture, read_json
from llm_eval.demo import demonstration
from llm_eval.engine import evaluate
from llm_eval.report import render


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = {}
    benchmark = fixture("benchmark.json")
    run = demonstration(benchmark)
    outputs["examples/illustrative-run.json"] = json.dumps(run, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    for ext, fmt in (("json", "json"), ("txt", "text"), ("html", "html")):
        outputs[f"examples/comparison.{ext}"] = render(evaluate(benchmark, run), fmt)
    outputs["examples/incomplete.txt"] = render(evaluate(benchmark, demonstration(benchmark, "incomplete")))
    folder = ROOT / "evidence/local-smoke-2026-10-15"
    measured = evaluate(read_json(folder / "benchmark.json"), read_json(folder / "run.json"))
    for ext, fmt in (("json", "json"), ("txt", "text"), ("html", "html")):
        outputs[f"evidence/local-smoke-2026-10-15/report.{ext}"] = render(measured, fmt)
    mismatches = []
    for name, expected in outputs.items():
        target = ROOT / name
        if args.check:
            if not target.exists() or target.read_text(encoding="utf-8") != expected:
                mismatches.append(name)
        else:
            target.write_text(expected, encoding="utf-8")
    if mismatches:
        print("Stale reports: " + ", ".join(mismatches), file=sys.stderr)
        return 1
    print("Saved reports match the current evaluator." if args.check else "Saved reports regenerated; no model invoked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
