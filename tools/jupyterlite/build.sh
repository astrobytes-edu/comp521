#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "$0")" && pwd)"
output_dir="$root_dir/../../assets/jupyterlite"
stage_dir="$root_dir/.generated-content"
builder_python="${JUPYTERLITE_PYTHON:-$root_dir/../../.jupyterlite-build/bin/python}"

if [[ ! -x "$builder_python" ]]; then
  echo "JupyterLite builder Python not found: $builder_python" >&2
  exit 1
fi
export PATH="$(dirname "$builder_python"):$PATH"
# Keep Jupyter's notebook-signing database inside the ignored build workspace.
# This avoids writing to a developer-specific home-directory cache during builds.
export JUPYTER_DATA_DIR="$root_dir/.jupyter-data"
mkdir -p "$JUPYTER_DATA_DIR"

rm -rf "$stage_dir"
mkdir -p "$stage_dir"
cp -R "$root_dir/content/." "$stage_dir/"

# Activities are authored as reviewable MyST Markdown. JupyterLite's xeus
# kernel launches notebooks, so generate the notebook only in this ignored
# build staging directory; do not track hand-authored .ipynb JSON.
for activity in "$root_dir"/activities/*.md; do
  activity_name="$(basename "${activity%.md}")"
  "$builder_python" -m jupytext --to ipynb \
    --output "$stage_dir/$activity_name.ipynb" \
    "$activity"
done

cd "$root_dir"
"$builder_python" -m jupyter lite build \
  --config "$root_dir/jupyter_lite_config.json" \
  --contents "$stage_dir" \
  --output-dir "$output_dir"

# MyST's development proxy can discard a query string while handing the browser
# to this static app. A small same-origin launcher restores the notebook path
# only after JupyterLite has loaded, so local and published links behave alike.
cp "$root_dir"/launchers/*.html "$output_dir/"
