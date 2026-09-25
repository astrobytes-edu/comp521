"""Render self-contained Quarto Reveal decks for the MyST static site."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from itertools import count
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "09-lectures" / "reveal-source"
OUTPUT_DIR = ROOT / "09-lectures" / "reveal"


class LocalAssetRefs(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.refs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name not in {"href", "src"} or not value:
                continue
            if not value.startswith(("#", "data:", "http:", "https:", "mailto:")):
                self.refs.append(f"{tag} {name}={value}")


def build(source: Path) -> None:
    subprocess.run(
        ["quarto", "render", source.name, "--to", "revealjs"],
        cwd=SOURCE_DIR,
        check=True,
    )
    rendered = source.with_suffix(".html")
    try:
        html = rendered.read_text()
        refs = LocalAssetRefs()
        refs.feed(html)
        if refs.refs:
            raise ValueError(
                f"{source.name} is not self-contained; local assets: {refs.refs[:5]}"
            )
        # Quarto assigns fresh random IDs to executed cells on each render.
        # They have no other references in this export, so stable IDs keep
        # source-identical builds reviewable.
        cell_number = count(1)
        html = re.sub(
            r'<div id="[0-9a-f]{8}" class="cell"',
            lambda match: f'<div id="cell-{next(cell_number)}" class="cell"',
            html,
        )
        OUTPUT_DIR.mkdir(exist_ok=True)
        output = OUTPUT_DIR / rendered.name
        output.write_text("\n".join(line.rstrip(" \t") for line in html.split("\n")))
        print(f"Wrote {output.relative_to(ROOT)}")
    finally:
        rendered.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "decks",
        nargs="*",
        help="Quarto source filenames in 09-lectures/reveal-source (default: all)",
    )
    args = parser.parse_args()
    sources = (
        [SOURCE_DIR / name for name in args.decks]
        if args.decks
        else sorted(SOURCE_DIR.glob("*.qmd"))
    )
    if not sources:
        parser.error("no Reveal sources found")
    for source in sources:
        if source.parent != SOURCE_DIR or source.suffix != ".qmd" or not source.is_file():
            parser.error(f"expected an existing .qmd directly in {SOURCE_DIR}: {source}")
        build(source)


if __name__ == "__main__":
    main()
