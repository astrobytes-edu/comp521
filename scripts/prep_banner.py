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

READING_BANNER = f"""{START}
:::{{warning}} This reading is being revised for COMP 521
This chapter was adapted from COMP 536 and is still under review. You may find
references to the wrong course number, setup instructions that do not match
ours, or examples that assume material we have not covered yet.

The Python and the science are sound — it is the packaging that is catching up.
Where this page disagrees with the syllabus, the syllabus is right. If something
here does not work, tell me: that is genuinely useful and I would rather hear it
from you than not.
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
    # Authored pages promise a finalisation date; migrated readings cannot,
    # since they are revised progressively as the semester needs them.
    banner = BANNER if str(path) in DEFAULT_PAGES else READING_BANNER
    path.write_text(f"{fm}\n{banner}\n\n{body.lstrip(chr(10))}")
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
    if sys.argv[2:]:
        targets = [Path(p) for p in sys.argv[2:]]
    else:
        targets = [Path(p) for p in DEFAULT_PAGES]
    if targets and str(targets[0]) == "readings":
        targets = sorted(
            p for d in ("02-getting-started", "03-python", "04-scientific-computing",
                        "05-numerical-methods", "06-linear-algebra-stats")
            for p in Path(d).rglob("*.md") if "figures" not in p.parts
        )

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
