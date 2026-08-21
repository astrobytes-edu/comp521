"""Require unambiguous nesting for MyST colon-fenced directives.

An outer directive must use a longer colon fence than its inner directives.
Otherwise a parser can close the parent at the inner directive's terminator,
causing later admonitions to render as literal source text.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEXTBOOK_DIRS = ("03-python", "04-scientific-computing")
OPEN = re.compile(r"^(?P<fence>:{3,})\{[^\n]+\}")
CLOSE = re.compile(r"^(?P<fence>:{3,})\s*$")


def check(path: Path) -> list[str]:
    """Return fence-nesting errors for one Markdown source file."""
    errors: list[str] = []
    stack: list[tuple[int, int]] = []
    in_code_fence = False

    for line_number, line in enumerate(path.read_text().splitlines(), start=1):
        if line.startswith("```"):
            in_code_fence = not in_code_fence
            continue
        if in_code_fence:
            continue

        opener = OPEN.match(line)
        if opener:
            width = len(opener.group("fence"))
            if stack and width >= stack[-1][0]:
                outer_width, outer_line = stack[-1]
                errors.append(
                    f"{path.relative_to(ROOT)}:{line_number}: nested directive uses "
                    f"{width} colons inside {outer_width}-colon directive opened at "
                    f"line {outer_line}; use fewer colons for the inner fence"
                )
            stack.append((width, line_number))
            continue

        closer = CLOSE.match(line)
        if closer:
            width = len(closer.group("fence"))
            if not stack:
                errors.append(f"{path.relative_to(ROOT)}:{line_number}: closing directive has no opener")
                continue
            expected, opened_at = stack.pop()
            if width != expected:
                errors.append(
                    f"{path.relative_to(ROOT)}:{line_number}: closing directive has "
                    f"{width} colons; expected {expected} for directive opened at line {opened_at}"
                )

    for width, line_number in stack:
        errors.append(
            f"{path.relative_to(ROOT)}:{line_number}: {width}-colon directive is not closed"
        )
    return errors


def main() -> int:
    errors = [
        error
        for directory in TEXTBOOK_DIRS
        for path in sorted((ROOT / directory).glob("*.md"))
        for error in check(path)
    ]
    if errors:
        print("\n".join(errors))
        return 1
    print("MyST directive-fence check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
