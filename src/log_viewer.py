"""
Simple CLI to tail PerceptraderAI logs.
"""

import argparse
from pathlib import Path
import time


def tail(file: Path, lines: int = 10):
    """Print last `lines` from file then follow."""
    with file.open() as f:
        data = f.readlines()[-lines:]
        print("".join(data), end="")
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            print(line, end="")


def main():
    parser = argparse.ArgumentParser(description="Tail logs")
    parser.add_argument("name", help="Logger name (e.g. 'orchestrator')")
    parser.add_argument("-n", type=int, default=10, help="Number of lines")
    args = parser.parse_args()

    log_file = Path("logs") / f"{args.name}.log"
    if not log_file.exists():
        print(f"No such log: {log_file}")
        return
    tail(log_file, args.n)


if __name__ == "__main__":
    main()
