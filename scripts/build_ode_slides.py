"""Build the reviewed MyST ODE deck and note-free, self-contained student exports."""
from pathlib import Path
from html.parser import HTMLParser
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / '09-lectures/myst-source/lecture-11-odes'
OUTPUT = SOURCE / '_build/reveal'


class LocalAssets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in {'src', 'href'} and value and not value.startswith(
                    ('#', 'data:', 'http:', 'https:', 'mailto:')):
                self.refs.append(value)


def main():
    subprocess.run(['node', str(ROOT / 'tools/myst-reveal/src/build.mjs'),
                    str(SOURCE), str(OUTPUT)], cwd=ROOT, check=True)
    for name in ('lecture-11-odes.html', 'lecture-11-odes.handout.html'):
        html = (OUTPUT / name).read_text()
        if re.search(r'<aside\b[^>]*class="notes"', html):
            raise ValueError('Instructor notes are not allowed in the student source/export')
        html = re.sub(r'<a\b[^>]*class="[^"]*\bsource-link\b[^"]*"[^>]*>.*?</a>',
                      '', html, flags=re.S)
        if '_instructor/' in html or '/Users/anna/' in html or 'href="sources/' in html:
            raise ValueError('Export contains a private path or undeployed notebook link')
        assets = LocalAssets()
        assets.feed(html)
        if assets.refs:
            raise ValueError(f'Export has unresolved local assets: {assets.refs[:5]}')
        target = ROOT / '09-lectures/reveal' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html)
        print(f'Wrote {target.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
