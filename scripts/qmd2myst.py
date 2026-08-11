#!/usr/bin/env python3
"""Convert Quarto .qmd readings to MyST .md, verbatim except for syntax.

Design notes
------------
Idempotent and re-runnable: reads .qmd from a source tree, writes .md to a
destination tree, never edits in place. Re-running after an upstream fix in
comp536-sp26 is always safe.

Content is preserved word-for-word. Only Quarto-specific *syntax* changes:
callout divs, executable cell fences, cell options, and frontmatter.

Anything the script cannot convert confidently is left as-is and recorded in
the report, so nothing is silently mangled.

Usage:
    python scripts/qmd2myst.py SRC_DIR DEST_DIR [--report report.md]
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Quarto callout class -> MyST admonition directive
CALLOUT_MAP = {
    "note": "note",
    "tip": "tip",
    "warning": "warning",
    "important": "important",
    "caution": "caution",
}

# Quarto div class -> MyST directive (non-callout, high confidence)
DIV_MAP = {
    "aside": "margin",
    "column-margin": "margin",
}

# Div classes we deliberately do not auto-convert; low volume, layout-specific.
FLAG_CLASSES = {"columns", "column", "grid", "panel-tabset", "card", "card-header",
                "card-body", "g-col-12", "g-col-md-4"}

# Pandoc/Quarto heading anchors: `## Some Heading {#some-id}`.
# MyST does not read these; it needs a `(some-id)=` target line *before* the
# heading. Without the rewrite, every in-page link to that anchor silently
# dead-ends.
HEADING_ID_RE = re.compile(r"^(#{1,6}\s+.*?)\s*\{#([A-Za-z0-9_-]+)\}\s*$")

CALLOUT_RE = re.compile(r"^(:{3,})\s*\{\.callout-([a-z]+)([^}]*)\}\s*$")
DIV_RE = re.compile(r"^(:{3,})\s*\{\.([a-zA-Z0-9_-]+)([^}]*)\}\s*$")
TITLE_ATTR_RE = re.compile(r'title\s*=\s*"([^"]*)"')
HEADING_RE = re.compile(r"^#{2,4}\s+(.*?)\s*$")


@dataclass
class Report:
    files: int = 0
    callouts: int = 0
    dropdowns: int = 0
    hoisted_titles: int = 0
    exec_cells: int = 0
    static_cells: int = 0
    hidden_input: int = 0
    margins: int = 0
    anchors: int = 0
    grids: int = 0
    flagged: list[str] = field(default_factory=list)


def parse_frontmatter(lines: list[str]) -> tuple[dict, int]:
    """Return (frontmatter dict, index of first body line). Shallow parse:
    we only need top-level scalar keys; nested blocks are skipped wholesale."""
    if not lines or lines[0].strip() != "---":
        return {}, 0
    fm: dict[str, str] = {}
    i = 1
    while i < len(lines) and lines[i].strip() != "---":
        line = lines[i]
        m = re.match(r"^([a-zA-Z_-]+):\s*(.*)$", line)
        if m:
            fm[m.group(1)] = m.group(2).strip()
        i += 1
    return fm, i + 1


def build_frontmatter(fm: dict, has_exec: bool) -> list[str]:
    """Emit MyST frontmatter. Drops Quarto-only keys (format, execute, draft)."""
    out = ["---"]
    for key in ("title", "subtitle", "author"):
        if key in fm and fm[key]:
            val = fm[key].strip()
            if not (val.startswith('"') or val.startswith("'")):
                val = f'"{val}"'
            out.append(f"{key}: {val}")
    if has_exec:
        out.append("kernelspec:")
        out.append("  name: python3")
        out.append("  display_name: Python 3")
    out.append("---")
    return out


def convert_callout(m: re.Match, rpt: Report) -> tuple[list[str], bool]:
    """Convert a Quarto callout opener. Returns (emitted lines, wants_title_hoist)."""
    fence, kind, attrs = m.group(1), m.group(2), m.group(3) or ""
    directive = CALLOUT_MAP.get(kind, "note")
    rpt.callouts += 1

    title_m = TITLE_ATTR_RE.search(attrs)
    title = title_m.group(1) if title_m else ""

    opener = f"{fence}{{{directive}}}"
    if title:
        opener += f" {title}"

    lines = [opener]
    classes = []
    if 'collapse="true"' in attrs:
        classes.append("dropdown")
        rpt.dropdowns += 1
    if 'appearance="simple"' in attrs:
        classes.append("simple")
    if classes:
        lines.append(f":class: {' '.join(classes)}")

    return lines, (not title)


def convert_cell_options(opts: list[str], rpt: Report) -> tuple[list[str], bool, str]:
    """Map Quarto `#|` cell options to MyST code-cell options.

    Returns (myst option lines, is_static, caption_text).
    `eval: false` means show-but-do-not-run, which in MyST is a plain fence.
    """
    myst_opts: list[str] = []
    tags: list[str] = []
    is_static = False
    caption = ""

    for raw in opts:
        body = raw.lstrip("#|").strip()
        if ":" not in body:
            continue
        key, _, val = body.partition(":")
        key, val = key.strip(), val.strip().strip('"').strip("'")

        if key == "eval" and val == "false":
            is_static = True
        elif key == "echo" and val == "false":
            tags.append("remove-input")
            rpt.hidden_input += 1
        elif key == "label":
            myst_opts.append(f":name: {val}")
        elif key == "fig-cap":
            caption = val
        # code-fold / code-summary intentionally dropped: all code is visible.

    if tags:
        myst_opts.append(f":tags: [{', '.join(tags)}]")
    return myst_opts, is_static, caption


def convert(text: str, rpt: Report, relpath: str) -> str:
    lines = text.split("\n")
    fm, start = parse_frontmatter(lines)
    body = lines[start:]

    has_exec = any(l.strip() == "```{python}" for l in body)
    out: list[str] = build_frontmatter(fm, has_exec)
    out.append("")

    i = 0
    pending_hoist = False  # previous line opened a titleless admonition

    while i < len(body):
        line = body[i]
        stripped = line.strip()

        # --- executable / static code cells -------------------------------
        if stripped in ("```{python}", "```{mermaid}"):
            lang = "python" if "python" in stripped else "mermaid"
            j = i + 1
            opts = []
            while j < len(body) and body[j].startswith("#|"):
                opts.append(body[j])
                j += 1

            myst_opts, is_static, caption = convert_cell_options(opts, rpt)

            if lang == "mermaid":
                out.append("```{mermaid}")
            elif is_static:
                out.append("```python")
                rpt.static_cells += 1
            else:
                out.append("```{code-cell} python")
                out.extend(myst_opts)
                if myst_opts:
                    out.append("")
                rpt.exec_cells += 1

            i = j
            while i < len(body) and body[i].strip() != "```":
                out.append(body[i])
                i += 1
            out.append("```")
            if caption:
                out.append("")
                out.append(f"*{caption}*")
                rpt.flagged.append(f"{relpath}: fig-cap emitted as italic caption -> review")
            i += 1
            pending_hoist = False
            continue

        # --- heading anchors: `## X {#id}` -> `(id)=` + `## X` --------------
        him = HEADING_ID_RE.match(line)
        if him:
            out.append(f"({him.group(2)})=")
            out.append(him.group(1))
            rpt.anchors += 1
            i += 1
            pending_hoist = False
            continue

        # --- plain fenced code: strip vestigial Quarto `#|` options --------
        # Quarto ignores cell options inside a non-executable fence, so these
        # are already inert; carrying them into MyST would render them as
        # visible comment lines.
        if stripped.startswith("```") and not stripped.startswith("```{"):
            out.append(line)
            i += 1
            while i < len(body) and body[i].startswith("#|"):
                i += 1
            while i < len(body) and body[i].strip() != "```":
                out.append(body[i])
                i += 1
            if i < len(body):
                out.append(body[i])
                i += 1
            pending_hoist = False
            continue

        # --- callouts ------------------------------------------------------
        m = CALLOUT_RE.match(line)
        if m:
            emitted, wants_hoist = convert_callout(m, rpt)
            out.extend(emitted)
            pending_hoist = wants_hoist
            i += 1
            continue

        # hoist a leading heading inside a titleless admonition into its title
        if pending_hoist:
            if stripped == "":
                out.append(line)
                i += 1
                continue
            hm = HEADING_RE.match(line)
            if hm:
                # rewrite the opener we just emitted to carry the title
                for k in range(len(out) - 1, -1, -1):
                    if out[k].lstrip().startswith(":::"):
                        out[k] = f"{out[k].rstrip()} {hm.group(1)}"
                        break
                rpt.hoisted_titles += 1
                i += 1
                pending_hoist = False
                continue
            pending_hoist = False

        # --- other divs ----------------------------------------------------
        dm = DIV_RE.match(line)
        if dm:
            fence, cls = dm.group(1), dm.group(2)
            if cls in DIV_MAP:
                out.append(f"{fence}{{{DIV_MAP[cls]}}}")
                rpt.margins += 1
                i += 1
                continue
            # Quarto's columns/column layout -> MyST grid/grid-item. Source
            # fence lengths already nest correctly (:::: outer, ::: inner), so
            # they carry over unchanged. `width="33%"` is dropped: MyST sizes
            # grid items by the parent's column spec, not per-item widths.
            if cls == "columns":
                out.append(f"{fence}{{grid}} 1 1 2 3")
                rpt.grids += 1
                i += 1
                continue
            if cls == "column":
                out.append(f"{fence}{{grid-item}}")
                rpt.grids += 1
                i += 1
                continue

            if cls in FLAG_CLASSES:
                rpt.flagged.append(f"{relpath}:{i+1}: layout div .{cls} left as-is -> manual")
                out.append(line)
                i += 1
                continue

        out.append(line)
        i += 1

    rpt.files += 1
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("src", type=Path)
    ap.add_argument("dest", type=Path)
    ap.add_argument("--report", type=Path, default=None)
    args = ap.parse_args()

    rpt = Report()
    sources = sorted(
        p for p in args.src.rglob("*.qmd")
        if ".jupyter_cache" not in p.parts and "OLD" not in p.parts and "drafts" not in p.parts
    )
    if not sources:
        print(f"no .qmd found under {args.src}", file=sys.stderr)
        return 1

    for src in sources:
        rel = src.relative_to(args.src)
        dest = args.dest / rel.with_suffix(".md")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(convert(src.read_text(errors="replace"), rpt, str(rel)))
        print(f"  {rel} -> {dest.relative_to(args.dest)}")

    summary = [
        "",
        f"files converted   : {rpt.files}",
        f"callouts          : {rpt.callouts}  (dropdown: {rpt.dropdowns}, titles hoisted: {rpt.hoisted_titles})",
        f"executable cells  : {rpt.exec_cells}",
        f"static cells      : {rpt.static_cells}",
        f"hidden-input cells: {rpt.hidden_input}",
        f"margin divs       : {rpt.margins}",
        f"heading anchors   : {rpt.anchors}",
        f"grid conversions  : {rpt.grids}",
        f"flagged for review: {len(rpt.flagged)}",
    ]
    print("\n".join(summary))
    for f in rpt.flagged:
        print(f"  FLAG {f}")

    if args.report:
        args.report.write_text(
            "# Conversion report\n" + "\n".join(summary) + "\n\n## Flagged\n"
            + "\n".join(f"- {f}" for f in rpt.flagged) + "\n"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
