"""Reject Markdown math patterns that MyST renders literally or ambiguously."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
READING_DIRS = (
    "01-course-info",
    "02-getting-started",
    "03-python",
    "04-scientific-computing",
    "05-numerical-methods",
    "06-linear-algebra-stats",
)
FORBIDDEN_DELIMITERS = re.compile(r"\\[\[\]()]")
LATEX_COMMAND = re.compile(
    r"\\(?:neq|pm|times|sqrt|mathrm|to|geq|leq|in|rho|star)\b"
)
# For example, catches `$5.5$\\times$$10^{-17}$`. The lookarounds prevent a
# valid display equation (`$$ ... $$`) from being mistaken for this pattern.
SPLIT_DELIMITERS = re.compile(
    r"(?<!\$)\$(?!\$)[^$\n]+\$(?:\\[A-Za-z]+)?\$\$(?!\$)"
)


def content_lines(path: Path):
    """Yield non-code-fence lines with their one-based line number."""
    in_fence = False
    for number, line in enumerate(path.read_text().splitlines(), start=1):
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            yield number, line


def main() -> int:
    errors: list[str] = []
    for directory in READING_DIRS:
        for path in sorted((ROOT / directory).rglob("*.md")):
            display_delimiters = 0
            for number, line in content_lines(path):
                if FORBIDDEN_DELIMITERS.search(line):
                    errors.append(f"{path.relative_to(ROOT)}:{number}: use $...$ or $$...$$, not \\(...\\) or \\[...\\]")
                inline_code = re.finditer(r"`([^`\n]*)`", line)
                if any(LATEX_COMMAND.search(match.group(1)) for match in inline_code):
                    errors.append(f"{path.relative_to(ROOT)}:{number}: LaTeX appears inside inline code")
                if SPLIT_DELIMITERS.search(line):
                    errors.append(f"{path.relative_to(ROOT)}:{number}: adjacent or split dollar delimiters")
                display_delimiters += line.count("$$")
            if display_delimiters % 2:
                errors.append(f"{path.relative_to(ROOT)}: unmatched $$ display delimiter")
    if errors:
        print("\n".join(errors))
        return 1
    print("Math delimiter check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
