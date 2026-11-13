"""HTTP availability checks using only Python's standard library."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from time import perf_counter
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class CheckResult:
    checked_at: str
    url: str
    status_code: int | None
    latency_ms: float
    is_up: bool
    error: str | None


def validate_url(url: str) -> str:
    """Allow only HTTP(S) targets with valid hosts and no embedded credentials."""
    if not url or any(char.isspace() for char in url):
        raise ValueError("URL must not be empty or contain whitespace")
    try:
        parts = urlsplit(url)
        host = parts.hostname
        _ = parts.port
    except ValueError as exc:
        raise ValueError(f"Invalid URL: {exc}") from exc
    if (
        parts.scheme not in {"http", "https"}
        or not host
        or parts.username is not None
        or parts.password is not None
    ):
        raise ValueError("URL must use HTTP(S), have a host, and contain no credentials")
    return url


def check_url(url: str, *, timeout: float = 5.0) -> CheckResult:
    """Perform one request and retain its result, including failures."""
    validate_url(url)
    if timeout <= 0:
        raise ValueError("timeout must be positive")

    checked_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    started = perf_counter()
    request = Request(url, headers={"User-Agent": "WebsiteUptimeMonitor/1.0"})

    try:
        with urlopen(request, timeout=timeout) as response:
            status = response.getcode()
        return CheckResult(
            checked_at, url, status, round((perf_counter() - started) * 1000, 2),
            200 <= status < 400, None,
        )
    except HTTPError as exc:
        return CheckResult(
            checked_at, url, exc.code, round((perf_counter() - started) * 1000, 2),
            False, f"HTTP {exc.code}",
        )
    except (URLError, OSError) as exc:
        return CheckResult(
            checked_at, url, None, round((perf_counter() - started) * 1000, 2),
            False, str(exc),
        )
