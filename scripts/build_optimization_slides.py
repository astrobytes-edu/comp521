"""Build the public Lectures 3–4 slides and worked handout, without notes.

Run from the course root with .venv/bin/python -B and this file's path.
This local build does not commit, push, publish, or run GitHub CI.
"""

from __future__ import annotations

import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "09-lectures/myst-source/lecture-15-optimization"
NAME = "lecture-15-optimization"
EXPORTS = (f"{NAME}.html", f"{NAME}.handout.html")
FORBIDDEN = (
    "_instructor/", "/Users/anna/", "speaker-notes.md", "presenter-notes.js",
    "comp521NotesMathCss", "SpeakerNotesMath", "comp521-notes-math-css",
)


class ExportCheck(HTMLParser):
    def __init__(self):
        super().__init__()
        self.notes = 0
        self.math = 0
        self.math_errors = 0
        self.images = 0
        self.refs = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "").split()
        if tag == "aside" and "notes" in classes:
            self.notes += 1
        if "katex" in classes:
            self.math += 1
        if "katex-error" in classes:
            self.math_errors += 1
        if tag == "img":
            assert attrs.get("alt", "").strip(), "A lecture image lacks alt text"
            assert attrs.get("src", "").startswith("data:"), "Image is not self-contained"
            self.images += 1
        for key in ("src", "href"):
            if attrs.get(key):
                self.refs.append(attrs[key])


def digest(file):
    return hashlib.sha256(file.read_bytes()).hexdigest()


def execute_figures():
    """Execute once in the invoking course interpreter, not a global kernel."""
    book = SOURCE / "calculations.ipynb"
    notebook = nbformat.read(book, as_version=4)
    count = sum(cell.cell_type == "code" for cell in notebook.cells)
    assert count == 22, f"Expected 22 calculation cells, found {count}"
    os.environ.setdefault("MPLBACKEND", "Agg")
    os.environ.setdefault("MPLCONFIGDIR", str(SOURCE / "_build/mpl-cache"))
    with tempfile.TemporaryDirectory(prefix="comp521-optimization-kernel-") as scratch:
        kernel = Path(scratch) / "kernels/python3"
        kernel.mkdir(parents=True)
        (kernel / "kernel.json").write_text(json.dumps({
            "argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
            "display_name": "COMP 521", "language": "python",
        }))
        manager = KernelManager(kernel_name="python3", kernel_spec_manager=KernelSpecManager(
            kernel_dirs=[str(kernel.parent)]))
        try:
            NotebookClient(notebook, km=manager, timeout=180,
                           resources={"metadata": {"path": str(SOURCE)}}).execute()
        finally:
            if manager.has_kernel:
                manager.shutdown_kernel(now=True)
    errors = [output for cell in notebook.cells if cell.cell_type == "code"
              for output in cell.outputs if output.output_type == "error"]
    assert not errors, errors
    nbformat.validate(notebook)
    nbformat.write(notebook, book)
    return count


def build(output):
    env = dict(os.environ, PATH=str(ROOT / ".venv/bin") + os.pathsep + os.environ["PATH"],
               PYTHONDONTWRITEBYTECODE="1")
    package = ROOT / "tools/myst-reveal"
    # The notebook above owns execution. Process markup without executing again,
    # then use the existing plug-in exporter without changing its behavior.
    subprocess.run(["node", str(package / "node_modules/mystmd/dist/myst.cjs"),
                    "build", "--site", "--strict"], cwd=SOURCE, env=env, check=True)
    exporter = (package / "src/build.mjs").as_uri()
    script = (f"import {{ exportProject }} from {json.dumps(exporter)}; "
              "console.log(JSON.stringify(exportProject(process.argv[1], process.argv[2])));")
    subprocess.run(["node", "--input-type=module", "-e", script, str(SOURCE), str(output)],
                   cwd=ROOT, env=env, check=True)


def main():
    (SOURCE / "_build").mkdir(exist_ok=True)
    slides = (SOURCE / "slides.md").read_text()
    ids = re.findall(r"(?m)^\((opt-[a-z0-9-]+)\)=\n## ", slides)
    assert len(ids) == len(set(ids)) == 52, "Expected 52 unique slide identifiers"
    assert "{speaker-note}" not in slides, "The public source must not contain notes"
    assert not any(marker in slides for marker in FORBIDDEN), "Private material in public source"
    figures = re.findall(r"(?m)^```\{slide-figure\} ([^\n]+)", slides)
    assert figures, "The lecture needs its calculated figures"
    executed_cells = execute_figures()
    for reference in figures:
        file = (SOURCE / reference.strip()).resolve()
        assert file.is_relative_to(SOURCE) and file.is_file(), reference
    json.loads((SOURCE / "numerical-checks.json").read_text())
    output = SOURCE / "_build/reveal"
    build(output)
    manifest = json.loads((output / "decks.json").read_text())
    assert len(manifest["decks"]) == 1 and manifest["decks"][0]["slides"] == 52
    exports = {}
    for name in EXPORTS:
        html = (output / name).read_text()
        parsed = ExportCheck()
        parsed.feed(html)
        assert parsed.notes == 0, f"Presenter notes in {name}"
        assert parsed.math > 0 and parsed.math_errors == 0, (name, parsed.math)
        assert parsed.images >= len(figures), (name, parsed.images)
        assert not any(marker in html for marker in FORBIDDEN), f"Private material in {name}"
        assert not any(ref.startswith(("sources/", "../", "/Users/")) for ref in parsed.refs), name
        exports[name] = {"sha256": digest(output / name), "notes": parsed.notes,
                         "math": parsed.math, "math_errors": parsed.math_errors,
                         "images": parsed.images}

    # Stage only the two checked student exports after both have passed.
    destination = ROOT / "09-lectures/reveal"
    destination.mkdir(exist_ok=True)
    for name in EXPORTS:
        shutil.copy2(output / name, destination / name)
        assert digest(destination / name) == exports[name]["sha256"]
    result = {
        "kind": "optimization-student-lecture-build", "slides": 52,
        "executed_code_cells": executed_cells, "presenter_notes": 0,
        "math_errors": 0, "student_exports": exports,
        "source_hashes": {name: digest(SOURCE / name) for name in
                          ("slides.md", "slides.json", "myst.yml", "lecture.css",
                           "figures.py", "calculations.ipynb", "numerical-checks.json")},
        "publication": "local exports only; no commit, push, or GitHub CI",
    }
    (SOURCE / "_build/verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
