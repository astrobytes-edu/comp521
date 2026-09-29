"""Read-only checks for source preservation and the SE teaching example.

Run from any directory after building the migration project.
"""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strip_options(code):
    return re.sub(r'^#\|.*\n', '', code, flags=re.M).strip()


for record in json.loads((ROOT / 'migration-record.json').read_text()):
    name = record['deck']
    original = ROOT / 'originals' / f'{name}.qmd'
    assert digest(original) == record['sha256'], f'Archived source changed: {name}'
    live = Path(record['source'])
    if live.exists():
        assert digest(live) == record['sha256'], f'COMP 536 source changed: {name}'
    expected = []
    for language, code in re.findall(r'```([^\n]*)\n(.*?)\n```', original.read_text(), re.S):
        if language != '{python}' or re.search(r'^#\| eval: false$', code, re.M):
            continue
        expected.append(strip_options(code))
    if expected:
        notebook = json.loads((ROOT / f'{name}-computations.ipynb').read_text())
        actual = [strip_options(''.join(c['source'])) for c in notebook['cells'] if c['cell_type'] == 'code']
        assert actual == expected, f'Computational source changed: {name}'
        built = json.loads((ROOT / '_build/site/content' / f'{name}-computations.json').read_text())
        blocks = built['mdast']['children']
        assert len(blocks) == len(expected)
        for block in blocks:
            assert any(c['type'] == 'outputs' for c in block['children']), 'Missing execution output record'
    for asset in record['assets']:
        assert digest(ROOT / asset['copy']) == asset['sha256']
    print(f'{name}: original hash verified; {len(expected)} computational cells preserved; {len(record["assets"])} assets verified')

text = (ROOT / 'software-engineering.md').read_text()
section = text.split('## Worked example: implement the contract')[1].split('\n## ')[0]
code = re.search(r'```\{slide-code\} python\n:title: [^\n]*\n(.*?)\n```', section, re.S).group(1)
namespace = {}
exec(compile(code, 'software-engineering.md:finite_mean', 'exec'), namespace)
mean = namespace['finite_mean']
values = [1.0, 3.0]
assert mean(values) == 2.0 and values == [1.0, 3.0]
assert mean([7.0]) == 7.0
assert mean([4.0, 6.0]) == 5.0
for values in ([], [float('nan')], [float('inf')], [-float('inf')]):
    try:
        mean(values)
    except ValueError:
        pass
    else:
        raise AssertionError(f'Invalid input accepted: {values}')
print('SE example: independent values, unchanged input, empty and nonfinite rejection passed')
