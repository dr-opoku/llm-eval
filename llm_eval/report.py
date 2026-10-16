"""Text and HTML reports with no scripts, network assets or output execution."""

import html
import json


def _number(value, suffix="", digits=3):
    return "unknown" if value is None else f"{value:.{digits}f}{suffix}"


def _columns(item):
    return [item["configuration_id"], item["outcome"],
            f"{item['accepted_records']}/{item['observed_records']} observed",
            f"{item['observed_records']}/{item['expected_records']}",
            str(item["boundary_requirement_failures"]),
            _number(item["latency"]["p95_seconds"], " s"),
            _number(item["cost"]["cost_per_accepted_eur"], " EUR", 6)]


def text_report(report):
    lines = ["llm-eval — task-specific configuration assessment",
             f"Evidence: {report['evidence_scope']} ({report['provenance']['kind']})",
             "Production suitability: not established", ""]
    if report["provenance"]["kind"] == "synthetic":
        lines += ["SYNTHETIC EXAMPLE: answers, timings and costs are authored fixtures.",
                  "These are not measurements of real models.", ""]
    for item in report["configurations"]:
        lines += [f"{item['configuration_id']}: {item['outcome']}",
                  f"  Accepted: {item['accepted_records']}/{item['observed_records']} observed; "
                  f"matrix coverage {item['observed_records']}/{item['expected_records']}",
                  f"  Boundary requirement failures: {item['boundary_requirement_failures']}; execution errors: {item['execution_errors']}",
                  f"  p95 full-request latency: {_number(item['latency']['p95_seconds'], ' s')} "
                  f"({item['latency']['observations']} observations; complete={item['latency']['complete']})",
                  f"  Cost per accepted result: {_number(item['cost']['cost_per_accepted_eur'], ' EUR', 6)}",
                  "  Checks: " + ", ".join(f"{key}={value}" for key, value in item["checks"].items()), ""]
    lines += ["Configurations meeting the declared sample rules: " + (", ".join(report["selection"]["candidate_ids"]) or "none"),
              "Automatic winner: none", "", "Limits:"]
    lines += ["- " + note for note in report["limitations"]]
    lines += ["", "Benchmark SHA-256: " + report["benchmark_sha256"], "Run SHA-256: " + report["run_sha256"]]
    return "\n".join(lines) + "\n"


def html_report(report):
    esc = lambda value: html.escape(str(value), quote=True)
    headers = ["Configuration", "Sample verdict", "Accepted results", "Matrix coverage",
               "Boundary failures", "p95 request time", "Cost / accepted"]
    rows = "".join("<tr>" + "".join(f"<td>{esc(cell)}</td>" for cell in _columns(item)) + "</tr>"
                   for item in report["configurations"])
    details = ""
    for item in report["configurations"]:
        body = "".join(f"<tr><td>{esc(row['case_id'])}</td><td>{row['attempt']}</td>"
                       f"<td>{esc(row['family'])}</td><td>{esc('accepted' if row['accepted'] else 'failed')}</td>"
                       f"<td>{esc(', '.join(row['reason_codes']) or 'all declared checks passed')}</td></tr>"
                       for row in item["cases"])
        details += f"<details><summary>{esc(item['configuration_id'])}: attempt evidence</summary><div class='scroll'><table>"
        details += "<thead><tr><th>Case</th><th>Attempt</th><th>Family</th><th>Result</th><th>Reasons</th></tr></thead>"
        details += f"<tbody>{body}</tbody></table></div></details>"
    synthetic = report["provenance"]["kind"] == "synthetic"
    notice = ("Synthetic example. All responses, timings and costs are constructed. No real model was measured."
              if synthetic else "Measured or imported task sample. Production suitability and cross-configuration comparability remain unestablished.")
    candidates = ", ".join(report["selection"]["candidate_ids"]) or "none"
    notes = "".join(f"<li>{esc(note)}</li>" for note in report["limitations"])
    policy = esc(json.dumps(report["policy"], indent=2))
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">
<title>llm-eval — configuration assessment</title>
<style>body{{font:16px/1.55 system-ui,sans-serif;color:#172b3b;background:#f7f9fc;margin:0}}main{{max-width:1120px;margin:auto;padding:32px 20px}}h1,h2{{line-height:1.2}}.notice{{background:#fff3c6;border-left:5px solid #9a6500;padding:16px}}.scroll{{overflow-x:auto}}table{{border-collapse:collapse;width:100%;background:white;margin:16px 0}}th,td{{text-align:left;padding:12px;border-bottom:1px solid #d6dde5;vertical-align:top}}th{{background:#e9eef5}}summary{{cursor:pointer;padding:12px;font-weight:600}}details{{background:white;margin:12px 0}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;background:#e9eef5;padding:16px}}.hash{{overflow-wrap:anywhere;font-family:monospace}}footer{{margin-top:32px;color:#44566a}}</style>
</head><body><main><h1>Which configuration meets this task's requirements?</h1>
<p class="notice">{esc(notice)}</p>
<p>Acceptance means passing all declared case checks. A fluent answer or a successful request alone does not suffice.</p>
<div class="scroll"><table><thead><tr>{''.join('<th>' + esc(h) + '</th>' for h in headers)}</tr></thead><tbody>{rows}</tbody></table></div>
<p><strong>Sample-rule candidates:</strong> {esc(candidates)}. No automatic winner or deployment recommendation.</p>
<p>Boundary failures include any unmet case requirement, including malformed output. The cases assess proposed decisions; they never execute tools.</p>
<p>Latency uses full request durations, including recorded failures. Partial timing samples are displayed but cannot satisfy a required latency check. Cost per accepted result includes every supplied attempt's cost and is unknown unless accounting covers the full matrix.</p>
<h2>Declared requirements</h2><pre>{policy}</pre>
<h2>Inspect individual attempts</h2>{details}
<h2>What this evidence does not establish</h2><ul>{notes}</ul>
<footer>Benchmark fingerprint: <span class="hash">{esc(report['benchmark_sha256'])}</span><br>Run fingerprint: <span class="hash">{esc(report['run_sha256'])}</span><br>Standalone local report. No scripts or external assets.</footer>
</main></body></html>"""


def render(report, format="text"):
    if format == "json":
        return json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    if format == "html":
        return html_report(report)
    return text_report(report)
