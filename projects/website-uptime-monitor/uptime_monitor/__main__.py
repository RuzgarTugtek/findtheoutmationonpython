"""CLI for monitoring URLs and storing their history."""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import asdict
from pathlib import Path

from .monitor import check_url, validate_url
from .storage import save_result


def load_targets(urls: list[str], file: Path | None) -> list[str]:
    targets = list(urls)
    if file is not None:
        for line in file.read_text(encoding="utf-8").splitlines():
            value = line.strip()
            if value and not value.startswith("#"):
                targets.append(value)
    return list(dict.fromkeys(targets))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Monitor website availability.")
    parser.add_argument("--url", action="append", default=[], help="HTTP(S) target")
    parser.add_argument("--file", type=Path, help="File containing target URLs")
    parser.add_argument("--db", type=Path, default=Path("uptime-history.sqlite3"))
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--interval", type=float, default=60.0)
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--json", action="store_true", help="Output JSON Lines")
    args = parser.parse_args(argv)

    if args.timeout <= 0 or args.interval < 0 or args.count <= 0:
        parser.error("--timeout and --count must be positive; --interval cannot be negative")

    try:
        targets = load_targets(args.url, args.file)
        if not targets:
            parser.error("provide at least one --url or --file with targets")
        for target in targets:
            validate_url(target)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

    for round_number in range(args.count):
        for target in targets:
            result = check_url(target, timeout=args.timeout)
            save_result(args.db, result)
            if args.json:
                print(json.dumps(asdict(result)))
            else:
                status = f"HTTP {result.status_code}" if result.status_code else "NO RESPONSE"
                state = "UP  " if result.is_up else "DOWN"
                print(f"{state} {target}  {status}  {result.latency_ms:.2f} ms")
        if round_number + 1 < args.count:
            time.sleep(args.interval)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
