"""Check that the deploy artifact includes every stable lecture media URL.

Run after myst build --html and copying 09-lectures/media/. to _build/html/media/.
"""
from pathlib import Path
import hashlib
import os
import re

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / '_build/html'
SOURCE = ROOT / '09-lectures'
errors = []
films = set()
science_page = ROOT / '08-assessments/projects/project-3-science-background.md'
# Build-cache copies retain source-relative asset paths but are not source pages.
lecture_pages = [page for page in SOURCE.rglob('*.md')
                 if '_build' not in page.relative_to(SOURCE).parts]
for page in [*lecture_pages, science_page]:
    text = page.read_text()
    for relative in re.findall(r'^:(?:video|poster): (.+)$', text, re.M):
        source = (page.parent / relative).resolve()
        target = HTML / 'media' / source.name
        if not source.is_file() or not target.is_file():
            errors.append(f'Missing source or stable deployed file: {source.name}')
            continue
        if hashlib.sha256(source.read_bytes()).digest() != hashlib.sha256(target.read_bytes()).digest():
            errors.append(f'Deployed file differs from source: {source.name}')
        if source.suffix == '.mp4':
            films.add(source.name)
for source in (SOURCE / 'animations').glob('*.md'):
    # These uniquely named source files use MyST's default filename slug.
    page = HTML / source.stem / 'index.html'
    if not page.is_file():
        errors.append(f'Missing animation page: {page}')
        continue
    for name in re.findall(r'^:video: .*/([^/]+\.mp4)$', source.read_text(), re.M):
        expected = f"{os.environ.get('BASE_URL', '').rstrip('/')}/media/{name}"
        if f'"mediaUrl":"{expected}"' not in page.read_text():
            errors.append(f'Missing stable player URL in {page}')
science_html = HTML / 'project-3-science-background/index.html'
if not science_html.is_file():
    errors.append(f'Missing science background page: {science_html}')
else:
    rendered = science_html.read_text()
    base = os.environ.get('BASE_URL', '').rstrip('/')
    for movie in re.findall(r'^:video: .*/([^/]+\.mp4)$', science_page.read_text(), re.M):
        if f'"mediaUrl":"{base}/media/{movie}"' not in rendered:
            errors.append(f'Missing science film URL: {movie}')
    if f'"figureUrl":"{base}/media/Project3Kepler.html"' not in rendered:
        errors.append('Missing interactive Kepler figure URL in science background')
    if f'href="{base}/media/Project3Kepler.html"' not in rendered:
        errors.append('Missing full-size Kepler figure link in science background')
    if f'"figureUrl":"{base}/media/StellarRadiation.html"' not in rendered:
        errors.append('Missing interactive radiation figure URL in science background')
    if f'href="{base}/media/StellarRadiation.html"' not in rendered:
        errors.append('Missing full-size radiation figure link in science background')
figure_files=['Project3Kepler.html','kepler-geometry.mjs','StellarRadiation.html',
              'radiation-physics.mjs','figure-math.mjs']
figure_files += [str(path.relative_to(SOURCE/'media'))
                 for path in (SOURCE/'media/katex').rglob('*') if path.is_file()]
for name in figure_files:
    source, target = SOURCE / 'media' / name, HTML / 'media' / name
    if not source.is_file() or not target.is_file():
        errors.append(f'Missing source or stable deployed file: {name}')
    elif hashlib.sha256(source.read_bytes()).digest() != hashlib.sha256(target.read_bytes()).digest():
        errors.append(f'Deployed file differs from source: {name}')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'Lecture media: {len(films)} films, matching static copies, animation pages, and both Project 3 figures verified.')
