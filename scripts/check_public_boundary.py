#!/usr/bin/env python3
"""Fail if instructor-only material is tracked by the student course repository."""

from __future__ import annotations

import subprocess
import sys
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


FORBIDDEN_PREFIXES = (
    "_instructor/",
    "_planning/",
    "solutions/",
    "roster/",
)

OPTIMIZATION_EXPORTS = (
    "lecture-15-optimization.html",
    "lecture-15-optimization.handout.html",
)


def check_optimization_exports(reveal: Path) -> list[str]:
    errors = []
    for name in OPTIMIZATION_EXPORTS:
        export = reveal / name
        if not export.is_file():
            errors.append(f"Missing optimization lecture export: {export}")
            continue
        text = export.read_text()
        notes = re.search(r"<aside\b[^>]*\bclass=[\"'][^\"']*\bnotes\b", text, re.I)
        private_markers = ("_instructor/", "/Users/anna/", "SpeakerNotesMath",
                           "comp521NotesMathCss", "presenter-notes.js", "speaker-notes.md")
        if notes or any(marker in text for marker in private_markers):
            errors.append(f"Private content in optimization export: {export}")
    return errors


def check_site(site: Path) -> list[str]:
    errors = check_optimization_exports(site / "reveal")
    for prefix in (*FORBIDDEN_PREFIXES, "tools/", "docs/"):
        if (site / prefix).exists():
            errors.append(f"Non-course workspace in publication artifact: {prefix}")
    config_file = site / "config.json"
    if not config_file.is_file():
        return errors + ["Missing built site config.json"]
    config = json.loads(config_file.read_text())
    slugs = {page["slug"] for project in config["projects"]
             for page in project.get("pages", []) if "slug" in page}
    slugs.update(project["index"] for project in config["projects"])
    # The JupyterLite runtime is an intentionally separate static application.
    for index in site.glob("*/index.html"):
        if index.parent.name not in slugs | {"jupyterlite"}:
            errors.append(f"Page outside course navigation: {index.relative_to(site)}")
    expected = {path.name for path in (ROOT / "09-lectures/reveal").glob("*.html")}
    expected.update({"software-engineering.html", "software-engineering.handout.html"})
    expected.update({"sources/project4-nasa-exoplanets.csv",
                     "sources/project4-nasa-exoplanets.provenance.json"})
    reveal = site / "reveal"
    for file in reveal.rglob("*"):
        if file.is_file() and file.relative_to(reveal).as_posix() not in expected:
            errors.append(f"Unselected slide artifact: {file.relative_to(site)}")
    for name in expected:
        if not (reveal / name).is_file():
            errors.append(f"Missing public slide artifact: reveal/{name}")
    for slug in ("software-engineering", "software-engineering-for-scientists", "software-engineering-guide"):
        if slug not in slugs or not (site / slug / "index.html").is_file():
            errors.append(f"Missing SWE student route: {slug}")
    route = site / "software-engineering/index.html"
    if route.is_file():
        html = route.read_text()
        for name in ("software-engineering.html", "software-engineering.handout.html"):
            if f'href="/comp521/reveal/{name}"' not in html:
                errors.append(f"Student page lacks base-path-correct link: {name}")
    pandas = site / "lecture-12-pandas/index.html"
    if "lecture-12-pandas" not in slugs or not pandas.is_file():
        errors.append("Missing Pandas student lecture route")
    else:
        for name in ("lecture-12-pandas.html", "lecture-12-pandas.handout.html",
                     "sources/project4-nasa-exoplanets.csv",
                     "sources/project4-nasa-exoplanets.provenance.json"):
            if f'href="/comp521/reveal/{name}"' not in pandas.read_text():
                errors.append(f"Pandas page lacks base-path-correct link: {name}")
    for name in ("lecture-12-pandas.html", "lecture-12-pandas.handout.html"):
        export = reveal / name
        if export.is_file():
            text = export.read_text()
            if '<aside class="notes"' in text or '_instructor/' in text or '/Users/anna/' in text:
                errors.append(f"Private content in Pandas export: {name}")
            if 'sources/pandas-examples' in text:
                errors.append(f"Student notebook link remains in Pandas export: {name}")
    if pandas.is_file() and 'sources/pandas-examples' in pandas.read_text():
        errors.append("Student notebook link remains on the Pandas lecture page")
    guide = site / "jaxstro-sciml-guide/index.html"
    if "jaxstro-sciml-guide" not in slugs or not guide.is_file():
        errors.append("Missing Jaxstro SciML guide lecture route")
    else:
        for name in OPTIMIZATION_EXPORTS:
            if f'href="/comp521/reveal/{name}"' not in guide.read_text():
                errors.append(f"Guide page lacks base-path-correct link: {name}")
    for name in ("sources/pandas-examples.html", "sources/pandas-examples.ipynb"):
        if (reveal / name).exists():
            errors.append(f"Retired student notebook still published: {name}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", action="store_true", help="Also check the final _build/html upload artifact")
    args = parser.parse_args()
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

    export_errors = check_optimization_exports(ROOT / "09-lectures/reveal")
    if export_errors:
        print("\n".join(export_errors))
        return 1

    print("Public repository boundary check passed.")
    if args.site:
        errors = check_site(ROOT / "_build/html")
        if errors:
            print("\n".join(errors))
            return 1
        print("Publication artifact boundary and SWE route checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
