"""SQLite storage for HTTP monitoring results."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from .monitor import CheckResult


def save_result(database_path: Path, result: CheckResult) -> None:
    """Write a check result to a local SQLite file with parameterized SQL."""
    with sqlite3.connect(database_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS uptime_checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                checked_at TEXT NOT NULL,
                url TEXT NOT NULL,
                status_code INTEGER,
                latency_ms REAL NOT NULL,
                is_up INTEGER NOT NULL,
                error TEXT
            )
            """
        )
        connection.execute(
            """
            INSERT INTO uptime_checks
                (checked_at, url, status_code, latency_ms, is_up, error)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                result.checked_at,
                result.url,
                result.status_code,
                result.latency_ms,
                int(result.is_up),
                result.error,
            ),
        )
