"""Tests use mocked HTTP clients, not real network connections."""

import json
import sqlite3
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError, URLError

from uptime_monitor.__main__ import load_targets, main
from uptime_monitor.monitor import CheckResult, check_url, validate_url
from uptime_monitor.storage import save_result


class UrlTests(unittest.TestCase):
    def test_accepts_http_and_https(self):
        self.assertEqual(validate_url("https://example.com/path"), "https://example.com/path")
        self.assertEqual(validate_url("http://127.0.0.1:8080/"), "http://127.0.0.1:8080/")

    def test_rejects_invalid_urls_and_embedded_credentials(self):
        for url in ("", "ftp://example.com", "https://", "http://user:pass@example.com", "https://example.com bad", "http://example.com:wrong"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                validate_url(url)

    def test_rejects_invalid_timeout(self):
        with self.assertRaises(ValueError):
            check_url("https://example.com", timeout=0)


class HttpTests(unittest.TestCase):
    @patch("uptime_monitor.monitor.urlopen")
    def test_successful_check(self, opener):
        opener.return_value.__enter__.return_value.getcode.return_value = 200
        result = check_url("https://example.com")
        self.assertTrue(result.is_up)
        self.assertEqual(result.status_code, 200)
        self.assertGreaterEqual(result.latency_ms, 0)
        opener.assert_called_once()

    @patch("uptime_monitor.monitor.urlopen")
    def test_server_error(self, opener):
        opener.side_effect = HTTPError("https://example.com", 503, "Unavailable", {}, None)
        result = check_url("https://example.com")
        self.assertFalse(result.is_up)
        self.assertEqual(result.status_code, 503)
        self.assertEqual(result.error, "HTTP 503")

    @patch("uptime_monitor.monitor.urlopen")
    def test_network_failure(self, opener):
        opener.side_effect = URLError("DNS failure")
        result = check_url("https://example.com")
        self.assertFalse(result.is_up)
        self.assertIsNone(result.status_code)
        self.assertIn("DNS failure", result.error)


class StorageAndCliTests(unittest.TestCase):
    def test_sqlite_history(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "history.sqlite3"
            result = CheckResult("2026-11-14T10:00:00+00:00", "https://example.com", 200, 10.5, True, None)
            save_result(database, result)
            save_result(database, result)
            with sqlite3.connect(database) as connection:
                rows = connection.execute("SELECT url, status_code, is_up FROM uptime_checks").fetchall()
            self.assertEqual(rows, [("https://example.com", 200, 1)] * 2)

    def test_load_targets_deduplicates_and_ignores_comments(self):
        with tempfile.TemporaryDirectory() as directory:
            file = Path(directory) / "sites.txt"
            file.write_text("# demo\nhttps://example.com\n\nhttps://www.python.org\n")
            self.assertEqual(
                load_targets(["https://example.com"], file),
                ["https://example.com", "https://www.python.org"],
            )

    @patch("uptime_monitor.__main__.check_url")
    def test_cli_json_and_database(self, checker):
        checker.return_value = CheckResult(
            "2026-11-14T10:00:00+00:00", "https://example.com", 200, 10.0, True, None
        )
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "checks.sqlite3"
            stdout = StringIO()
            with redirect_stdout(stdout):
                code = main(["--url", "https://example.com", "--db", str(database), "--json"])
            with sqlite3.connect(database) as connection:
                count = connection.execute("SELECT COUNT(*) FROM uptime_checks").fetchone()[0]
        self.assertEqual(code, 0)
        self.assertEqual(count, 1)
        self.assertTrue(json.loads(stdout.getvalue())["is_up"])


if __name__ == "__main__":
    unittest.main()
