#!/usr/bin/env python3
"""Add or remove the "still being prepared" banner on course pages.

The banner is delimited by HTML comment markers so it can be removed exactly,
without touching anything a page has grown around it.

Usage:
    python scripts/prep_banner.py add  [PATH ...]   # default: all course pages
    python scripts/prep_banner.py rm   [PATH ...]
    python scripts/prep_banner.py list             # show which pages carry it
"""

from __future__ import annotations

import sys
from pathlib import Path

START = "<!-- prep-banner:start -->"
END = "<!-- prep-banner:end -->"

BANNER = f"""{START}
:::{{warning}} This page is still being prepared
COMP 521 begins **Tuesday, August 25**. This page is being written and revised
until then — dates, policies, and details may still change. It is published
early so you can see the shape of the course, not because it is finished.

Anything still under discussion is settled by **Monday, August 24**. After that,
what is written here is what the course does.
:::
{END}"""

# Pages authored for this course (as opposed to readings migrated from comp536).
DEFAULT_PAGES = [
    "index.md",
    "01-course-info/syllabus.md",
    "01-course-info/schedule.md",
    "01-course-info/ai-policy.md",
    "01-course-info/grading.md",
    "assignments/se-presentation.md",
]


def split_frontmatter(text: str) -> tuple[str, str]:
    """Return (frontmatter including delimiters, rest). Empty first if none."""
    if not text.startswith("---"):
        return "", text
    end = text.find("\n---", 3)
    if end == -1:
        return "", text
    end = text.find("\n", end + 1)
    return text[: end + 1], text[end + 1 :]


def add(path: Path) -> str:
    text = path.read_text()
    if START in text:
        return "already present"
    fm, body = split_frontmatter(text)
    path.write_text(f"{fm}\n{BANNER}\n\n{body.lstrip(chr(10))}")
    return "added"


def remove(path: Path) -> str:
    text = path.read_text()
    i, j = text.find(START), text.find(END)
    if i == -1 or j == -1:
        return "not present"
    # swallow the trailing newline(s) the banner introduced
    rest = text[j + len(END) :].lstrip("\n")
    path.write_text(text[:i].rstrip("\n") + "\n\n" + rest)
    return "removed"


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] not in {"add", "rm", "list"}:
        print(__doc__)
        return 1
    action = sys.argv[1]
    targets = [Path(p) for p in (sys.argv[2:] or DEFAULT_PAGES)]

    for path in targets:
        if not path.exists():
            print(f"  {path}: MISSING")
            continue
        if action == "list":
            print(f"  {path}: {'banner' if START in path.read_text() else '-'}")
        else:
            print(f"  {path}: {add(path) if action == 'add' else remove(path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
