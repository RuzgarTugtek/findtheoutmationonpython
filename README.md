# Python Automation Projects

A collection of Python automation experiments.

## Projects

### [Website Uptime Monitor](projects/website-uptime-monitor)

Simple HTTP(S) availability checker with response-time measurements, SQLite history, configurable monitoring intervals, JSON Lines output, and mocked automated tests. Python 3.10+; standard library only.

~~~bash
cd projects/website-uptime-monitor
python -m uptime_monitor --url https://example.com
python -m unittest discover -s tests -v
~~~

### Video automation scripts

Earlier scripts for automated video production are at the repository root (main.py, config.py and modules/). The uptime monitor is independent of these scripts.
