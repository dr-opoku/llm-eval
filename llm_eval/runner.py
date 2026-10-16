"""Explicit local Ollama requests; no cloud credentials, tools or shell execution."""

import hashlib
import json
import platform
import time
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener

from .contracts import MAX_FILE_BYTES, fingerprint, integer, number, parse_json, validate_benchmark


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("Ollama redirects are refused")


def _endpoint(url):
    parts = urlsplit(url)
    if (parts.scheme != "http" or parts.hostname not in {"127.0.0.1", "::1"}
            or parts.username or parts.password or parts.query or parts.fragment or parts.path not in {"", "/"}):
        raise ValueError("Use a loopback HTTP origin, e.g. http://127.0.0.1:11434")
    # Accessing .port also validates malformed ports.
    if parts.port is not None and not 1 <= parts.port <= 65535:
        raise ValueError("Invalid port")
    return url.rstrip("/")


def _call(endpoint, path, payload, timeout):
    request = Request(endpoint + path, data=json.dumps(payload).encode() if payload is not None else None,
                      headers={"Content-Type": "application/json"})
    start = time.monotonic()
    try:
        with build_opener(ProxyHandler({}), _NoRedirect()).open(request, timeout=timeout) as response:
            data = response.read(MAX_FILE_BYTES + 1)
        if len(data) > MAX_FILE_BYTES:
            raise ValueError("Ollama response exceeds capture limit")
        raw = data.decode("utf-8")
        result = parse_json(raw)
        if not isinstance(result, dict):
            raise ValueError("Ollama response must be an object")
        return result, raw, time.monotonic() - start, None
    except HTTPError as exc:
        body = exc.read(MAX_FILE_BYTES + 1)
        raw = body[:MAX_FILE_BYTES].decode("utf-8", errors="replace")
        return None, raw, time.monotonic() - start, f"HTTP_{exc.code}"
    except (URLError, TimeoutError, OSError, ValueError) as exc:
        return None, None, time.monotonic() - start, type(exc).__name__


def collect(benchmark, models, endpoint="http://127.0.0.1:11434", attempts=3,
            timeout=120, context=4096, output_limit=512, mode="auto", progress=None, checkpoint=None):
    validate_benchmark(benchmark)
    endpoint = _endpoint(endpoint)
    integer(attempts, "attempts", maximum=20)
    integer(context, "context", minimum=512, maximum=131072)
    integer(output_limit, "output_limit", minimum=16, maximum=8192)
    number(timeout, "timeout", minimum=1, maximum=900)
    if mode not in {"auto", "standard", "fast", "thinking"}:
        raise ValueError("Invalid mode")
    if not 1 <= len(models) <= 20 or len(set(models)) != len(models) or any(not model.strip() for model in models):
        raise ValueError("Supply 1 to 20 distinct nonempty model names")
    started = datetime.now(timezone.utc).isoformat()
    version, _, _, version_error = _call(endpoint, "/api/version", None, min(timeout, 10))
    configurations = [{"configuration_id": f"local-{index}", "model": model,
                       "parameters": {"requested_mode": mode}, "environment": {}, "records": []}
                      for index, model in enumerate(models, start=1)]
    run = {"schema_version": "1.0", "benchmark_sha256": fingerprint(benchmark),
           "attempts_per_case": attempts, "configurations": configurations,
           "provenance": {"kind": "measured", "started_at": started, "finished_at": None,
                          "adapter": "ollama_generate_http", "scheduler": "serial",
                          "requested_models": models,
                          "timing_scope": "full client request, including model loading; keep_alive=0",
                          "probe_cost_scope": "mode probes and inventory requests are excluded from task metrics",
                          "description": "New requests on supplied cases. No model is installed or promoted. Costs are unmeasured; they are not inferred from tokens."}}
    if checkpoint:
        checkpoint(run)
    for index, model in enumerate(models, start=1):
        if progress:
            progress(f"Collecting {model}; calls are serial and model output is never executed.")
        show, _, _, show_error = _call(endpoint, "/api/show", {"model": model}, min(timeout, 30))
        probes = {}
        for label, think in (("standard", None), ("fast", False), ("thinking", True)):
            payload = {"model": model, "prompt": "Reply exactly OK.", "stream": False, "keep_alive": 0,
                       "options": {"num_ctx": context, "num_predict": 16, "temperature": 0, "seed": 42}}
            if think is not None:
                payload["think"] = think
            result, raw, elapsed, error = _call(endpoint, "/api/generate", payload, min(timeout, 30))
            supported = result is not None and not result.get("error") and result.get("done") is True
            probes[label] = {"request": payload, "raw_transport": raw, "request_completed": supported,
                             "elapsed_seconds": elapsed, "error": error or ("provider_error" if result and result.get("error") else None)}
        selected = ("fast" if probes["fast"]["request_completed"] else "standard") if mode == "auto" else mode
        think = {"standard": None, "fast": False, "thinking": True}[selected]
        config = configurations[index - 1]
        config.update({"parameters": {"selected_mode": selected, "temperature": 0, "seed": 42,
                                       "num_ctx": context, "num_predict": output_limit, "keep_alive": 0},
                       "environment": {"adapter": "ollama_generate_http", "ollama_version": version,
                                       "version_error": version_error, "platform": platform.system(),
                                       "machine": platform.machine(), "model_show": show, "show_error": show_error},
                       "mode_probes": probes})
        records = config["records"]
        if checkpoint:
            checkpoint(run)
        for case in benchmark["cases"]:
            for attempt in range(1, attempts + 1):
                payload = {"model": model, "system": benchmark["instructions"], "prompt": case["input"],
                           "stream": False, "keep_alive": 0,
                           "options": {"num_ctx": context, "num_predict": output_limit,
                                       "temperature": 0, "seed": 42, "top_p": 1}}
                if think is not None:
                    payload["think"] = think
                before = datetime.now(timezone.utc).isoformat()
                result, raw_transport, elapsed, error = _call(endpoint, "/api/generate", payload, timeout)
                if result is not None and (result.get("error") or result.get("done") is not True):
                    error = "provider_error_or_incomplete_response"
                text = result.get("response", "") if result else ""
                if not isinstance(text, str):
                    text, error = "", "invalid_response_field"
                token_count = result.get("eval_count") if result else None
                if type(token_count) is not int or token_count < 0:
                    token_count = None
                records.append({"case_id": case["case_id"], "attempt": attempt,
                                "status": "error" if error else "success", "error": error,
                                "started_at": before, "request": payload, "request_sha256": fingerprint(payload),
                                "response": text, "response_sha256": hashlib.sha256(text.encode()).hexdigest(),
                                "raw_transport": raw_transport, "elapsed_seconds": elapsed,
                                "output_tokens": token_count, "cost_eur": None,
                                "load_duration_ns": result.get("load_duration") if result else None,
                                "eval_duration_ns": result.get("eval_duration") if result else None})
                if checkpoint:
                    checkpoint(run)
    run["provenance"]["finished_at"] = datetime.now(timezone.utc).isoformat()
    if checkpoint:
        checkpoint(run)
    return run
