#!/usr/bin/env python3
"""
Logger Program
Reads log messages from standard input and writes them to a log file
with timestamps. Exits when it receives "QUIT".

Usage: python3 logger.py <logfile>
"""

import sys
from datetime import datetime


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 logger.py <logfile>", file=sys.stderr)
        sys.exit(1)

    log_filename = sys.argv[1]

    with open(log_filename, "a") as log_file:
        for line in sys.stdin:
            line = line.strip()

            # Stop on QUIT
            if line == "QUIT":
                break

            # Parse the log message: first word is action, rest is message
            parts = line.split(None, 1)
            if len(parts) == 0:
                continue

            action = parts[0]
            message = parts[1] if len(parts) > 1 else ""

            # Get current timestamp
            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H:%M")

            # Write formatted log entry
            log_entry = f"{timestamp} [{action}] {message}"
            log_file.write(log_entry + "\n")
            log_file.flush()


if __name__ == "__main__":
    main()
