# Website Uptime Monitor

A lightweight Python CLI that checks HTTP(S) availability, reports response time, and records results in a local SQLite database. No third-party packages are required (Python 3.10+).

## Features

- Single or repeated HTTP(S) checks with configurable timeout and interval.
- Multiple URLs supplied by flags or a plain-text file.
- Status code, response latency, UTC timestamp, and network errors.
- SQLite history for later analysis and JSON Lines output for automation.
- Tests that mock HTTP requests; no live sites contacted during testing.

## Quick start

From the project directory:

~~~bash
python -m uptime_monitor --url https://example.com --db uptime-history.sqlite3
python -m uptime_monitor --file sites.example.txt --count 3 --interval 60 --timeout 5 --json
python -m unittest discover -s tests -v
~~~

Example terminal output:

~~~text
UP   https://example.com  HTTP 200  84.21 ms
~~~

The output above is illustrative, not a measured result. HTTPS sites must be accessible from the machine running the program.

## Command options

- --url: add an HTTP(S) target (repeatable).
- --file: path containing one URL per line (# comments allowed).
- --db: SQLite output path; defaults to uptime-history.sqlite3.
- --timeout: request timeout in seconds; default 5.
- --interval: delay between rounds in seconds; default 60.
- --count: number of rounds; default 1.
- --json: print JSON object per check.

URL validation rejects non-HTTP schemes, missing hosts, and embedded credentials. Redirects are handled by Python's urllib; 2xx and 3xx responses are considered up. HTTP 4xx/5xx and connection errors are recorded as down.

## Data and safety

Checks are sequential. Only monitor sites you are authorized to query and use a respectful interval. The database may contain target URLs; avoid placing secrets or access tokens in URL query strings. Database files are excluded by the project's .gitignore.

## Structure

- uptime_monitor/monitor.py: HTTP checks and validation
- uptime_monitor/storage.py: SQLite history
- uptime_monitor/__main__.py: CLI and scheduling
- tests/: mocked HTTP, CLI, and storage tests
