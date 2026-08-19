#!/usr/bin/env python3
"""Fail if instructor-only material is tracked by the student course repository."""

from __future__ import annotations

import subprocess
import sys


FORBIDDEN_PREFIXES = (
    "_instructor/",
    "_planning/",
    "solutions/",
    "roster/",
)


def main() -> int:
    tracked = subprocess.run(
        ["git", "ls-files"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    exposed = [path for path in tracked if path.startswith(FORBIDDEN_PREFIXES)]

    if exposed:
        print("Instructor-only paths are tracked by the public course repository:")
        print("\n".join(f"  - {path}" for path in exposed))
        return 1

    print("Public repository boundary check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
