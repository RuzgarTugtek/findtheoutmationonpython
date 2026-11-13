"""Small HTTP availability monitor with persistent local history."""

from .monitor import CheckResult, check_url, validate_url

__all__ = ["CheckResult", "check_url", "validate_url"]
