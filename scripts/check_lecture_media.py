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
for page in SOURCE.rglob('*.md'):
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
if errors:
    raise SystemExit('\n'.join(errors))
print(f'Lecture media: {len(films)} films, matching static copies, and all animation pages verified.')
