"""Execute the reviewed Pandas notebook and publish only student artifacts."""
from html.parser import HTMLParser
from pathlib import Path
import shutil
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / '09-lectures/myst-source/lecture-12-pandas'
OUTPUT = SOURCE / '_build/reveal'
FILES = ('lecture-12-pandas.html', 'lecture-12-pandas.handout.html',
         'sources/pandas-examples.html')


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
        self.ids = set()
        self.notes = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if tag == 'aside' and 'notes' in attrs.get('class', '').split():
            self.notes = True
        for key in ('href', 'src'):
            if attrs.get(key):
                self.refs.append(attrs[key])


def main():
    subprocess.run([sys.executable, '-B', str(SOURCE / 'verify.py'), '--build'],
                   cwd=ROOT, check=True)
    parsed = {}
    for name in FILES:
        html = (OUTPUT / name).read_text()
        refs = References()
        refs.feed(html)
        if refs.notes or '_instructor/' in html or '/Users/anna/' in html:
            raise ValueError(f'Private content in student export: {name}')
        parsed[(OUTPUT / name).resolve()] = refs
    count = 0
    for file, refs in parsed.items():
        for ref in refs.refs:
            url = urlsplit(ref)
            if url.scheme or url.netloc:
                continue
            target = (file.parent / unquote(url.path)).resolve() if url.path else file
            anchor = unquote(url.fragment).lstrip('/')
            if target not in parsed or (anchor and anchor not in parsed[target].ids):
                raise ValueError(f'Unresolved export reference: {file.name}: {ref}')
            count += 1
    destination = ROOT / '09-lectures/reveal'
    for name in FILES:
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(OUTPUT / name, target)
    data = ROOT / '08-assessments/projects/data/project4-nasa-exoplanets.csv'
    for file in (SOURCE / 'pandas-examples.ipynb', data, data.with_suffix('.provenance.json')):
        shutil.copy2(file, destination / 'sources' / file.name)
    print(f'PASS student export privacy and {count} local references; copied six release artifacts')


if __name__ == '__main__':
    main()
