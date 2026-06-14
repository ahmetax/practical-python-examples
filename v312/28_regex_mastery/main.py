# Author: Ahmet Aksoy
# Date: 22.05.2026
# Python3.12 Ubuntu 24.04

"""
Advanced Regular Expressions (Regex Mastery) Example
Demonstrates how to build an analytical log parsing engine using 
named capture groups, lookarounds, and multi-line matching parameters.
"""

import json
import re


def parse_system_logs(raw_log_data: str) -> list[dict]:
    """
    Parses unformatted system logs line by line using an advanced regex schema.
    Extracts structured fields using named groups and filters messages.
    """
    # 1. Define a robust pattern using Named Capture Groups (?P<name>...)
    # Structure: [TIMESTAMP] [LEVEL] [COMPONENT] (IP_ADDRESS) - MESSAGE [STATUS_CODE]
    log_pattern = re.compile(
        r"^\[(?P<timestamp>[\d-]+ [\d:,]+)\]\s+"            # [2026-05-22 08:30:15,123]
        r"\[(?P<level>INFO|WARNING|ERROR|CRITICAL)\]\s+"     # [ERROR]
        r"\[(?P<component>[\w\.-]+)\]\s+"                    # [auth.service]
        r"\((?P<ip_address>\d{1,3}(?:\.\d{1,3}){3})\)\s+-\s+" # (192.168.1.50)
        r"(?P<message>.+?)"                                  # Core error text
        r"(?:\s+\[code:(?P<status_code>\d+)\])?$",           # [code:401] (Optional)
        re.MULTILINE
    )

    parsed_records = []

    # Iterate through matches across the multi-line input payload
    for match in log_pattern.finditer(raw_log_data):
        # Extract named fields directly as a dictionary mapping
        record_data = match.groupdict()
        
        # Clean up optional missing fields (like status codes)
        if record_data.get("status_code"):
            record_data["status_code"] = int(record_data["status_code"])
        else:
            record_data["status_code"] = None

        parsed_records.append(record_data)

    return parsed_records


def extract_critical_failures_with_lookahead(raw_log_data: str) -> list[str]:
    """
    Uses positive lookaheads (?=...) to identify lines belonging exclusively to
    the 'database' component that also contain explicit 'denied' or 'failed' sub-strings.
    """
    # Lookahead verifies 'database' is present, then captures the rest of the message line
    lookahead_pattern = re.compile(
        r"^(?=.*\[database\]).*?(?:denied|failed).*$", 
        re.MULTILINE | re.IGNORECASE
    )
    return lookahead_pattern.findall(raw_log_data)


# --- Example Usage ---
if __name__ == "__main__":
    print("--- Advanced Regex Analytical Engine Started ---\n")

    # Mock real-world system dump combining structural noise and variable patterns
    log_dump = (
        "[2026-05-22 08:30:12,001] [INFO] [web.server] (192.168.1.10) - Connection established successfully\n"
        "[2026-05-22 08:30:15,123] [ERROR] [auth.service] (192.168.1.50) - Invalid credentials provided [code:401]\n"
        "[2026-05-22 08:31:02,456] [WARNING] [database] (10.0.0.5) - Connection pool count exceeding 80%\n"
        "[2026-05-22 08:31:05,890] [CRITICAL] [database] (10.0.0.5) - Access denied for user 'admin_app' [code:1045]\n"
        "[2026-05-22 08:32:00,112] [INFO] [auth.service] (192.168.1.52) - Token refreshed gracefully\n"
        "[2026-05-22 08:32:45,999] [ERROR] [payment.gateway] (192.168.1.99) - Transaction failed due to timeout [code:504]"
    )

    print("=== 1. Parsing Full Log Stack via Named Capture Groups ===")
    parsed_logs = parse_system_logs(log_dump)
    # Output formatted JSON snippet for scannability
    print(json.dumps(parsed_logs[:2], indent=2))
    print(f"Total structured log profiles extracted: {len(parsed_logs)}")
    print("-" * 65)

    print("\n=== 2. Filtering Specific Contexts using Lookaheads ===")
    print("Targeting lines matching 'database' containing failures ('denied' / 'failed'):")
    critical_db_events = extract_critical_failures_with_lookahead(log_dump)
    for idx, event in enumerate(critical_db_events, start=1):
        print(f"  Match #{idx}: {event.strip()}")
    print("-" * 65)