#!/usr/bin/env python3
"""Send batches of requests from sample_posts/ to the TakeMeter web service.

Usage:
    python send_batch.py                              # every sample_posts/*.json
    python send_batch.py sample_posts/malformed_requests.json
    python send_batch.py --url http://127.0.0.1:8000 --delay 0.5
    python send_batch.py --repeat 5 --out results.json

Accepted file formats (a JSON array of entries):
  * Plain requests:    {"text": "...", "topic": "..."}            -> sent as-is
  * Test-case entries: {"id", "name", "body" | "raw_body", "expected_status"}
        body      - JSON object, serialised and sent
        raw_body  - string sent byte-for-byte (duplicate keys, lone surrogates, ...)
        expected_status - optional; the run reports MISMATCH when it differs

Exit code is 1 if any request hit a 5xx / network error, or missed its
expected_status; otherwise 0.
"""

import argparse
import json
import os
import statistics
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _reconfigure = getattr(_stream, "reconfigure", None)
        if callable(_reconfigure):
            _reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError, ValueError):
        pass

DEFAULT_URL = "https://ai201-project3-takemeter-starter-v2026.onrender.com"
SAMPLE_DIR = Path(__file__).parent / "sample_posts"


def load_entries(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"{path.name}: expected a JSON array")
    entries = []
    for i, item in enumerate(data, 1):
        if not isinstance(item, dict):
            raise ValueError(f"{path.name}[{i}]: expected an object")
        if "body" in item or "raw_body" in item:  # test-case entry
            raw = item["raw_body"] if "raw_body" in item else json.dumps(item["body"])
            entries.append({
                "file": path.name, "id": item.get("id", i), "name": item.get("name", ""),
                "payload": raw, "expected": item.get("expected_status"),
                "delay_s": item.get("delay_s"),
            })
        else:  # plain request
            label = str(item.get("text", ""))[:30].replace("\n", " ")
            entries.append({
                "file": path.name, "id": i, "name": label,
                "payload": json.dumps(item), "expected": None, "delay_s": None,
            })
    return entries


def send(url: str, payload: str, timeout: float, delay_s: float | None = None,
         admin_token: str | None = None) -> dict:
    headers = {"Content-Type": "application/json"}
    if delay_s:  # ask the server to stall, to force its 5s timeout (needs the admin token)
        headers["X-Test-Delay"] = str(delay_s)
        if admin_token:
            headers["X-Admin-Token"] = admin_token
    req = urllib.request.Request(url, data=payload.encode("utf-8"), method="POST", headers=headers)
    start = time.perf_counter()
    status, body, error = None, "", None
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status, body = resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        status, body = e.code, e.read().decode("utf-8", "replace")
    except Exception as e:  # timeout, DNS, connection reset
        error = f"{type(e).__name__}: {e}"
    return {
        "status": status, "body": body, "error": error,
        "seconds": round(time.perf_counter() - start, 3),
    }


def summarize_body(body: str) -> str:
    try:
        d = json.loads(body)
    except ValueError:
        return body[:70]
    if isinstance(d, dict) and "label" in d:
        return f"{d['label']} ({d['confidence']})"
    if isinstance(d, dict) and "detail" in d:
        detail = d["detail"]
        return (detail if isinstance(detail, str) else json.dumps(detail))[:70]
    return body[:70]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*", type=Path, help="JSON files (default: sample_posts/*.json)")
    ap.add_argument("--url", default=DEFAULT_URL, help="service base URL (default: the Render service)")
    ap.add_argument("--endpoint", default="/predict")
    ap.add_argument("--timeout", type=float, default=60, help="seconds per request (default 60; covers a Render cold start)")
    ap.add_argument("--admin-token", default=os.getenv("ADMIN_TOKEN"),
                    help="needed for entries with delay_s (default: $ADMIN_TOKEN)")
    ap.add_argument("--delay", type=float, default=0, help="seconds to wait between requests")
    ap.add_argument("--repeat", type=int, default=1, help="send each entry this many times")
    ap.add_argument("--out", type=Path, help="write full per-request results to this JSON file")
    args = ap.parse_args()

    files = args.files or sorted(SAMPLE_DIR.glob("*.json"))
    if not files:
        print("No JSON files found.", file=sys.stderr)
        return 2
    target = args.url.rstrip("/") + args.endpoint

    results, problems = [], 0
    print(f"Target: {target}\n")
    for path in files:
        try:
            entries = load_entries(path)
        except (OSError, ValueError) as e:
            print(f"SKIP {path}: {e}", file=sys.stderr)
            continue
        print(f"== {path.name} ({len(entries)} entries x{args.repeat})")
        for entry in entries:
            for _ in range(args.repeat):
                r = send(target, entry["payload"], args.timeout, entry["delay_s"], args.admin_token)
                exp, got = entry["expected"], r["status"]
                if r["error"] or (got is not None and got >= 500 and got != exp):
                    verdict = "FAIL"
                elif exp is not None and got != exp:
                    verdict = "MISMATCH"
                else:
                    verdict = "ok"
                problems += verdict != "ok"
                shown = r["error"] or summarize_body(r["body"])
                print(f"  [{verdict:8}] #{entry['id']:<3} {entry['name'][:32]:32} "
                      f"status={got} expected={exp if exp is not None else '-'} "
                      f"{r['seconds']:>6.2f}s  {shown}")
                results.append({**{k: entry[k] for k in ("file", "id", "name", "expected")},
                                **r, "verdict": verdict})
                if args.delay:
                    time.sleep(args.delay)
        print()

    if not results:
        return 2
    times = [r["seconds"] for r in results]
    counts: dict = {}
    for r in results:
        key = r["status"] if r["status"] is not None else "error"
        counts[key] = counts.get(key, 0) + 1
    print(f"Sent {len(results)} requests. Status counts: {dict(sorted(counts.items(), key=str))}")
    print(f"Latency: median {statistics.median(times):.2f}s, max {max(times):.2f}s")
    print(f"Problems (5xx/network/unexpected status): {problems}")

    if args.out:
        args.out.write_text(json.dumps(results, indent=2, ensure_ascii=True), encoding="utf-8")
        print(f"Wrote {args.out}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
