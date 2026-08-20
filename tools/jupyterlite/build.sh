#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "$0")" && pwd)"
output_dir="$root_dir/../../assets/jupyterlite"
builder_python="${JUPYTERLITE_PYTHON:-$root_dir/../../.jupyterlite-build/bin/python}"

if [[ ! -x "$builder_python" ]]; then
  echo "JupyterLite builder Python not found: $builder_python" >&2
  exit 1
fi
export PATH="$(dirname "$builder_python"):$PATH"

cd "$root_dir"
"$builder_python" -m jupyter lite build \
  --config "$root_dir/jupyter_lite_config.json" \
  --contents "$root_dir/content" \
  --output-dir "$output_dir"
