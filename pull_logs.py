"""Download the audit log from the live Render service into the repo.

Usage (PowerShell):
    $env:ADMIN_TOKEN = "<the same value set on Render>"
    python pull_logs.py                      # writes sample_posts/live_log.jsonl
    python pull_logs.py --out other.jsonl --url https://my-service.onrender.com

Render's free-tier disk is wiped on spin-down or redeploy, so run this soon after
using the app. Entries are merged with the existing file (deduplicated by
request_id + event), so repeated pulls keep what's already saved.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_URL = "https://ai201-project3-takemeter-starter-v2026.onrender.com"
DEFAULT_OUT = Path(__file__).parent / "sample_posts" / "live_log.jsonl"


def fetch(url: str, token: str) -> list[dict]:
    req = urllib.request.Request(f"{url.rstrip('/')}/logs", headers={"X-Admin-Token": token})
    with urllib.request.urlopen(req, timeout=120) as r:  # long timeout: free tier may be waking up
        text = r.read().decode("utf-8")
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()

    token = os.getenv("ADMIN_TOKEN")
    if not token:
        print("Set the ADMIN_TOKEN environment variable first.", file=sys.stderr)
        return 1
    try:
        fetched = fetch(args.url, token)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.reason}. (404 = ADMIN_TOKEN not set on Render; 401 = wrong token)", file=sys.stderr)
        return 1

    existing = []
    if args.out.exists():
        existing = [json.loads(l) for l in args.out.read_text(encoding="utf-8").splitlines() if l.strip()]

    seen, merged = set(), []
    for e in existing + fetched:
        key = (e.get("request_id"), e.get("event"), e.get("timestamp"))
        if key not in seen:
            seen.add(key)
            merged.append(e)
    merged.sort(key=lambda e: e.get("timestamp", ""))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in merged), encoding="utf-8")
    print(f"Fetched {len(fetched)} entries; {len(merged)} total in {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
