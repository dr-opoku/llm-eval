"""Small command line entry point; live collection is an explicit subcommand."""

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

from .contracts import fixture, read_json
from .demo import demonstration
from .engine import evaluate
from .report import render


def _write(path, text):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def _protect_output(path, inputs):
    if path and any(Path(path).resolve() == Path(item).resolve() for item in inputs if item):
        raise ValueError("Output must not overwrite an input file")


def _checkpoint(path, run):
    """Replace the run atomically so interruption preserves a readable checkpoint."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    pending = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=target.parent, delete=False) as stream:
            pending = Path(stream.name)
            stream.write(json.dumps(run, indent=2, ensure_ascii=False, allow_nan=False) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(pending, target)
    finally:
        if pending and pending.exists():
            pending.unlink()


def main(argv=None):
    parser = argparse.ArgumentParser(prog="llm-eval", description="Assess configurations against a bounded task; no universal model ranking.")
    commands = parser.add_subparsers(dest="command", required=True)
    demo = commands.add_parser("demo", help="Replay invented responses; no model, account or network required")
    demo.add_argument("--scenario", choices=("comparison", "incomplete"), default="comparison")
    demo.add_argument("--save-run", help="Also write the complete illustrative response records")
    check = commands.add_parser("evaluate", help="Evaluate a supplied run against its frozen benchmark")
    check.add_argument("run_file")
    check.add_argument("--benchmark", help="Custom benchmark JSON; defaults to the bundled synthetic task")
    for command in (demo, check):
        command.add_argument("--format", choices=("text", "json", "html"), default="text")
        command.add_argument("--output", help="Write the report to a file instead of stdout")
        command.add_argument("--require-candidate", action="store_true", help="Exit 1 if no configuration meets the declared sample rules")
    live = commands.add_parser("run", help="Explicitly collect new responses from already installed local Ollama models")
    live.add_argument("--model", action="append", required=True, help="Installed model name; repeat for several configurations")
    live.add_argument("--output", required=True, help="Run JSON destination, preferably under ignored runs/")
    live.add_argument("--benchmark")
    live.add_argument("--endpoint", default="http://127.0.0.1:11434")
    live.add_argument("--attempts", type=int, default=3)
    live.add_argument("--timeout", type=float, default=120)
    live.add_argument("--context", type=int, default=4096)
    live.add_argument("--output-limit", type=int, default=512)
    live.add_argument("--mode", choices=("auto", "standard", "fast", "thinking"), default="auto")
    args = parser.parse_args(argv)
    try:
        inputs = [getattr(args, "benchmark", None), getattr(args, "run_file", None)]
        _protect_output(args.output, inputs)
        benchmark = read_json(args.benchmark) if getattr(args, "benchmark", None) else fixture("benchmark.json")
        if args.command == "run":
            from .runner import collect
            run = collect(benchmark, args.model, endpoint=args.endpoint, attempts=args.attempts,
                          timeout=args.timeout, context=args.context, output_limit=args.output_limit,
                          mode=args.mode, progress=lambda message: print(message, file=sys.stderr),
                          checkpoint=lambda captured: _checkpoint(args.output, captured))
            print(f"Captured run: {args.output}. Evaluate separately; successful capture does not mean acceptable answers.", file=sys.stderr)
            return 0
        if args.command == "demo":
            run = demonstration(benchmark, args.scenario)
            if args.save_run:
                _protect_output(args.save_run, [args.output])
                _write(args.save_run, json.dumps(run, indent=2, ensure_ascii=False, allow_nan=False) + "\n")
        else:
            run = read_json(args.run_file)
        report = evaluate(benchmark, run)
        output = render(report, args.format)
        if args.output:
            _write(args.output, output)
        else:
            print(output, end="")
        return 1 if args.require_candidate and not report["selection"]["candidate_ids"] else 0
    except (ValueError, OSError, UnicodeError, RecursionError) as exc:
        error = {"schema_version": "1.0", "status": "error", "error_type": type(exc).__name__, "message": str(exc)}
        if getattr(args, "format", None) == "json":
            print(json.dumps(error), file=sys.stdout)
        else:
            print(f"Error: {exc}", file=sys.stderr)
        return 2
