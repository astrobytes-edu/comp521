"""Execute the Pandas/EDA examples and build the student MyST lecture."""
from pathlib import Path
import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import shutil

import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BOOK = HERE / 'pandas-examples.ipynb'
BUILD = HERE / '_build'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', action='store_true', help='Also export the MyST deck and worked handout')
    args = parser.parse_args()
    BUILD.mkdir(exist_ok=True)
    notebook = nbformat.read(BOOK, as_version=4)
    os.environ.setdefault('MPLCONFIGDIR', str(BUILD / 'mpl-cache'))
    os.environ.setdefault('MPLBACKEND', 'Agg')
    with tempfile.TemporaryDirectory(prefix='comp521-pandas-kernel-', dir='/private/tmp') as scratch:
        kernel = Path(scratch) / 'kernels/python3'
        kernel.mkdir(parents=True)
        (kernel / 'kernel.json').write_text(json.dumps({
            'argv': [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}'],
            'display_name': 'COMP 521 Pandas', 'language': 'python'}))
        manager = KernelManager(kernel_name='python3',
                                kernel_spec_manager=KernelSpecManager(kernel_dirs=[str(kernel.parent)]))
        NotebookClient(notebook, km=manager, timeout=180,
                       resources={'metadata': {'path': str(HERE)}}).execute()
        images = sum('image/png' in output.get('data', {}) for cell in notebook.cells
                     if cell.cell_type == 'code' for output in cell.outputs)
        assert images == 7, f'Expected seven executed figures, found {images}'
        nbformat.validate(notebook)
        nbformat.write(notebook, BOOK)

        # Verify the three-download student workflow in a fresh kernel outside
        # the repository, so ancestor lookup cannot conceal a missing file.
        standalone = Path(scratch) / 'student-downloads'
        standalone.mkdir()
        data = ROOT / '08-assessments/projects/data/project4-nasa-exoplanets.csv'
        for file in (data, data.with_suffix('.provenance.json')):
            shutil.copy2(file, standalone / file.name)
        NotebookClient(nbformat.read(BOOK, as_version=4), km=manager, timeout=180,
                       resources={'metadata': {'path': str(standalone)}}).execute()

        # Independently execute the selected cell owners for equality to public P4.
        source_cells = {cell.metadata.get('label'): cell.source for cell in notebook.cells
                        if cell.cell_type == 'code'}
        namespace = {'__name__': '__main__'}
        os.chdir(HERE)
        for label in ('setup', 'read-csv', 'nasa-missing', 'nasa-finite', 'nasa-central',
                      'nasa-signed', 'nasa-endpoints', 'nasa-selection'):
            exec(compile(source_cells[label], label, 'exec'), namespace)
        brief = (ROOT / '08-assessments/projects/project-4.md').read_text()
        public = next(code for code in re.findall(r'^```python\n(.*?)^```', brief, re.M | re.S)
                      if 'raw = pd.read_csv' in code)
        reference = {'raw': namespace['raw'], 'np': namespace['np']}
        for statement in ast.parse(public).body:
            if isinstance(statement, ast.Assign) and isinstance(statement.targets[0], ast.Name):
                if statement.targets[0].id in ('columns', 'finite', 'keep'):
                    exec(compile(ast.Module(body=[statement], type_ignores=[]), 'public-p4', 'exec'), reference)
        namespace['pd'].testing.assert_series_equal(namespace['keep'], reference['keep'])
        practice_counts = {
            f'{lo}-{hi}': int(namespace['planets']['pl_masse'].between(lo, hi).sum())
            for lo, hi in ((1, 5), (2, 8))}

        if args.build:
            env = dict(os.environ, PATH=str(ROOT / '.venv/bin') + os.pathsep + os.environ['PATH'],
                       JUPYTER_PATH=scratch + os.pathsep + os.environ.get('JUPYTER_PATH', ''),
                       PYTHONDONTWRITEBYTECODE='1')
            subprocess.run(['node', str(ROOT / 'tools/myst-reveal/src/build.mjs'),
                            str(HERE), str(BUILD / 'reveal')], cwd=ROOT, env=env, check=True)

    errors = [output for cell in notebook.cells if cell.cell_type == 'code'
              for output in cell.outputs if output.output_type == 'error']
    assert not errors, errors
    images = sum('image/png' in output.get('data', {}) for cell in notebook.cells
                 if cell.cell_type == 'code' for output in cell.outputs)
    assert images == 7, images
    labels = [cell.metadata['label'] for cell in notebook.cells if cell.cell_type == 'code']
    assert len(labels) == len(set(labels))
    result = {'notebook_sha256': hashlib.sha256(BOOK.read_bytes()).hexdigest(),
              'executed_cells': len(labels), 'figures': images,
              'public_p4_mask_matches': True,
              'rows_input': len(namespace['raw']), 'rows_selected': len(namespace['planets']),
              'standalone_downloads_run': True, 'practice_window_counts': practice_counts,
              'hands_on_tasks': sum(label.startswith('task-') for label in labels),
              'built': args.build}
    assert result['hands_on_tasks'] == 5
    if args.build:
        manifest = json.loads((BUILD / 'reveal/decks.json').read_text())
        deck = manifest['decks'][0]
        assert deck['file'] == 'lecture-12-pandas.html'
        result['slides'] = deck['slides']
        result['target_seconds'] = sum(slide['timing'] for slide in deck['slideIndex'])
        assert result['slides'] == 24 and result['target_seconds'] == 1800
        assert (HERE / 'slides.md').read_text().count('{slide-question}') == 2
    (BUILD / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    print('PASS notebook execution, EDA arithmetic, paired-row checks, and public P4 selection')


if __name__ == '__main__':
    main()
