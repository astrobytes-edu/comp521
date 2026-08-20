"""Validate source contracts for COMP 521 interactive lecture directives."""

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
LECTURE_DIRECTIVES = {
    "interactive-lecture",
    "lecture-scene",
    "lecture-predict",
    "lecture-figure",
    "lecture-write",
    "lecture-reveal",
    "lecture-code",
    "lecture-sandbox",
    "lecture-panel",
    "lecture-checkpoint",
    "lecture-media",
    "presenter-note",
}
PROMPT_DIRECTIVES = {"lecture-write", "lecture-predict", "lecture-checkpoint"}
DIRECTIVE_START = re.compile(r"^:::\{([^}]+)\}\s*$")
OPTION = re.compile(r"^:([\w-]+):\s*(.*?)\s*$")


def blocks(text: str):
    """Yield (directive, one-based start line, options) for MyST directive blocks."""
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        match = DIRECTIVE_START.match(lines[index])
        if not match:
            index += 1
            continue
        directive = match.group(1)
        start = index + 1
        index += 1
        options: dict[str, str] = {}
        while index < len(lines) and lines[index].strip() != ":::":
            option = OPTION.match(lines[index])
            if option:
                options[option.group(1)] = option.group(2)
            index += 1
        yield directive, start, options
        index += 1


def validate_text(text: str, path: str) -> list[str]:
    """Return source-contract errors using one-based Markdown line numbers."""
    errors: list[str] = []
    ids: dict[str, int] = {}
    reveal_targets: list[tuple[str, int, str]] = []
    known_reveals: set[str] = set()
    for directive, line, options in blocks(text):
        if directive.startswith("lecture-") and directive not in LECTURE_DIRECTIVES:
            errors.append(f"{path}:{line}: unknown lecture directive '{directive}'")
            continue
        if directive not in LECTURE_DIRECTIVES:
            continue
        if directive not in {"interactive-lecture", "presenter-note"}:
            identifier = options.get("id", "")
            if not identifier:
                errors.append(f"{path}:{line}: {directive} requires id")
            elif identifier in ids:
                errors.append(f"{path}:{line}: duplicate lecture prompt id '{identifier}'")
            else:
                ids[identifier] = line
                if directive == "lecture-reveal":
                    known_reveals.add(identifier)
        if directive in PROMPT_DIRECTIVES and not options.get("prompt", ""):
            errors.append(f"{path}:{line}: {directive} requires prompt")
        if directive == "lecture-predict" and not options.get("options", ""):
            errors.append(f"{path}:{line}: lecture-predict requires options")
        if directive == "lecture-figure":
            if not options.get("model", "") or not options.get("fallback", ""):
                errors.append(f"{path}:{line}: lecture-figure requires model and fallback")
        if directive == "lecture-code":
            if not options.get("starter", "") or not options.get("fallback", ""):
                errors.append(f"{path}:{line}: lecture-code requires starter and fallback")
        if directive == "lecture-sandbox":
            if not options.get("source", "") or not options.get("fallback", ""):
                errors.append(f"{path}:{line}: lecture-sandbox requires source and fallback")
        if directive == "presenter-note":
            if not options.get("scene", "") or not options.get("ask", "") or not options.get("wait", ""):
                errors.append(f"{path}:{line}: presenter-note requires scene, ask, and wait")
        if directive == "lecture-write" and options.get("reveal"):
            reveal_targets.append((options["reveal"], line, path))
        if directive == "lecture-panel":
            if (not options.get("src", "") and not options.get("code-file", "")) or not options.get("fallback", ""):
                errors.append(f"{path}:{line}: lecture-panel requires src or code-file and fallback")
        if directive == "lecture-media":
            required = ("mp4", "webm", "poster", "captions", "transcript", "fallback")
            if any(not options.get(field, "") for field in required):
                errors.append(
                    f"{path}:{line}: lecture-media requires webm, poster, captions, transcript, and fallback"
                )
    for target, line, source_path in reveal_targets:
        if target not in known_reveals:
            errors.append(f"{source_path}:{line}: lecture-write reveal '{target}' has no matching lecture-reveal")
    return errors


def main() -> int:
    errors: list[str] = []
    for directory in READING_DIRS:
        for path in sorted((ROOT / directory).rglob("*.md")):
            errors.extend(validate_text(path.read_text(), str(path.relative_to(ROOT))))
    if errors:
        print("\n".join(errors))
        return 1
    print("Interactive lecture contract check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
