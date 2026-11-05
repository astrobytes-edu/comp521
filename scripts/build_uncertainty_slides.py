"""Build the local student deck and a private presentation with speaker notes."""

from __future__ import annotations

import hashlib
import base64
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
import yaml

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "09-lectures/myst-source/lecture-14-uncertainty"
PRIVATE = ROOT / "_instructor/lectures/lecture-14-uncertainty"
NAME = "lecture-14-uncertainty"
EXPORTS = (f"{NAME}.html", f"{NAME}.handout.html")


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
            assert attrs.get("alt"), "A slide image lacks alt text"
            assert attrs.get("src", "").startswith("data:"), "Image is not self-contained"
            self.images += 1
        for key in ("src", "href"):
            if attrs.get(key):
                self.refs.append(attrs[key])


def execute_figures():
    """Execute in the course interpreter, regardless of the user's global kernel."""
    book = SOURCE / "calculations.ipynb"
    notebook = nbformat.read(book, as_version=4)
    os.environ.setdefault("MPLBACKEND", "Agg")
    os.environ.setdefault("MPLCONFIGDIR", str(SOURCE / "_build/mpl-cache"))
    with tempfile.TemporaryDirectory(prefix="comp521-uncertainty-kernel-") as scratch:
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
    errors = [o for c in notebook.cells if c.cell_type == "code"
              for o in c.outputs if o.output_type == "error"]
    assert not errors, errors
    nbformat.validate(notebook)
    nbformat.write(notebook, book)
    return sum(c.cell_type == "code" for c in notebook.cells)


def build(project, output):
    env = dict(os.environ, PATH=str(ROOT / ".venv/bin") + os.pathsep + os.environ["PATH"],
               PYTHONDONTWRITEBYTECODE="1")
    subprocess.run(["node", str(ROOT / "tools/myst-reveal/src/build.mjs"),
                    str(project), str(output)], cwd=ROOT, env=env, check=True)


def main():
    (SOURCE / "_build").mkdir(exist_ok=True)
    executed_cells = execute_figures()
    slides = (SOURCE / "slides.md").read_text()
    matches = list(re.finditer(r"(?m)^\((unc-[a-z-]+)\)=\n## ", slides))
    ids = [m[1] for m in matches]
    assert len(ids) == len(set(ids)) == 30, ids
    assert "{speaker-note}" not in slides
    notes_text = (PRIVATE / "speaker-notes.md").read_text()
    note_parts = re.split(r"(?m)^## (unc-[a-z-]+)\n", notes_text)
    notes = {note_parts[i]: note_parts[i + 1].strip()
             for i in range(1, len(note_parts), 2)}
    assert set(notes) == set(ids), "Presenter notes and slide IDs differ"
    assert all(len(note.split()) >= 65 and "**" in note for note in notes.values())

    student_output = SOURCE / "_build/reveal"
    build(SOURCE, student_output)

    # One student source owns the content. Notes are added only in a private
    # generated project, so no second authored deck can drift from that source.
    presenter_project = PRIVATE / "_build/presenter-source"
    presenter_project.mkdir(parents=True, exist_ok=True)
    chunks = [slides[:matches[0].start()]]
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(slides)
        chunks.append(slides[match.start():end].rstrip()
                      + "\n\n:::{speaker-note}\n" + notes[match[1]] + "\n:::\n\n")
    (presenter_project / "slides.md").write_text("".join(chunks))
    config = yaml.safe_load((SOURCE / "myst.yml").read_text())
    config["project"]["plugins"] = [str(ROOT / "tools/myst-reveal/plugin.mjs")]
    (presenter_project / "myst.yml").write_text(yaml.safe_dump(config, sort_keys=False))
    shutil.copy2(SOURCE / "lecture.css", presenter_project / "lecture.css")
    # Reveal's separate native notes window does not inherit the deck's math
    # styles. Bundle the same trusted KaTeX CSS/fonts for that private view.
    katex = ROOT / "tools/myst-reveal/node_modules/katex/dist"
    math_css = (katex / "katex.min.css").read_text()
    def font_data(match):
        file = katex / match[1].strip("\"'")
        mime = {".woff2": "font/woff2", ".woff": "font/woff", ".ttf": "font/ttf"}[file.suffix]
        return "url(data:" + mime + ";base64," + base64.b64encode(file.read_bytes()).decode() + ")"
    math_css = re.sub(r"url\(([^)]+)\)", font_data, math_css)
    presenter_extension = ("window.comp521NotesMathCss=" + json.dumps(math_css) + ";\n"
                           + (PRIVATE / "presenter-notes.js").read_text())
    (presenter_project / "presenter-notes.js").write_text(presenter_extension)
    presenter_settings = json.loads((SOURCE / "slides.json").read_text())
    presenter_settings["plugins"] = [{"global": "SpeakerNotesMath", "script": "presenter-notes.js"}]
    (presenter_project / "slides.json").write_text(json.dumps(presenter_settings, indent=2) + "\n")
    shutil.copytree(SOURCE / "assets", presenter_project / "assets", dirs_exist_ok=True)
    presenter_output = PRIVATE / "_build/reveal"
    build(presenter_project, presenter_output)

    for folder, expected_notes in ((student_output, 0), (presenter_output, 30)):
        manifest = json.loads((folder / "decks.json").read_text())
        assert manifest["decks"][0]["slides"] == 30
        for name in EXPORTS:
            html = (folder / name).read_text()
            checked = ExportCheck()
            checked.feed(html)
            assert checked.notes == (0 if ".handout." in name else expected_notes), (folder, name)
            assert checked.math > 60 and checked.math_errors == 0, (name, checked.math)
            assert checked.images >= 11, (name, checked.images)
            assert not any(ref.startswith(("sources/", "../", "/Users/anna"))
                           for ref in checked.refs), (name, checked.refs)
            if expected_notes == 0:
                assert "_instructor/" not in html and "/Users/anna/" not in html

    # Staging these two files is a local build, not a push or web publication.
    destination = ROOT / "09-lectures/reveal"
    for name in EXPORTS:
        shutil.copy2(student_output / name, destination / name)
    result = {
        "slides": 30, "executed_code_cells": executed_cells,
        "student_presenter_notes": 0, "private_presenter_notes": 30,
        "handouts_omit_presenter_notes": True,
        "math_errors": 0,
        "student_exports": {name: hashlib.sha256((destination / name).read_bytes()).hexdigest()
                            for name in EXPORTS},
        "private_deck": str(presenter_output / EXPORTS[0]),
        "publication": "local only; no commit, push, or GitHub CI",
    }
    (SOURCE / "_build/verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
