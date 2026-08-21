"""Validate the course-built xeus-python JupyterLite bundle."""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_PACKAGES = ("xeus-python", "numpy", "matplotlib", "scipy", "pandas", "ipywidgets")
REQUIRED_RUNTIME_ARTIFACTS = (
    "xeus/kernels.json",
    "xeus/comp521-xeus/bin/xpython.js",
    "xeus/comp521-xeus/bin/xpython.wasm",
    "files/transit-depth.ipynb",
    "files/ch06-temperature-invariant.ipynb",
)


def required_bundle_files(bundle: Path) -> list[str]:
    """Return missing-artifact errors for a JupyterLite deployment directory."""
    errors: list[str] = []
    if not (bundle / "jupyter-lite.json").is_file():
        errors.append(f"{bundle}: missing jupyter-lite.json")
    kernel_files = list(bundle.glob("**/kernel.json"))
    def is_xeus_kernel(path: Path) -> bool:
        text = path.read_text(errors="ignore").lower()
        return "xeus" in str(path).lower() or "xpython" in text

    if not any(is_xeus_kernel(path) for path in kernel_files):
        errors.append(f"{bundle}: missing xeus-python kernel specification")
    for artifact in REQUIRED_RUNTIME_ARTIFACTS:
        if not (bundle / artifact).is_file():
            errors.append(f"{bundle}: missing required runtime artifact '{artifact}'")
    kernels_index = bundle / "xeus" / "kernels.json"
    if kernels_index.is_file() and '"kernel": "xpython"' not in kernels_index.read_text(errors="ignore"):
        errors.append(f"{bundle}: xeus kernel registry does not declare xpython")
    return errors


def declared_packages(environment_file: Path) -> set[str]:
    """Read simple conda dependency names without adding a runtime YAML dependency."""
    packages: set[str] = set()
    for line in environment_file.read_text().splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            packages.add(stripped.removeprefix("- ").split("=", 1)[0].strip())
    return packages


def validate_bundle(bundle: Path, environment_file: Path | None = None) -> list[str]:
    """Return all bundle and optional environment-contract errors."""
    errors = required_bundle_files(bundle)
    if environment_file is not None:
        if not environment_file.is_file():
            errors.append(f"{environment_file}: missing environment.yml")
        else:
            missing = sorted(set(REQUIRED_PACKAGES) - declared_packages(environment_file))
            errors.extend(f"{environment_file}: missing required package '{package}'" for package in missing)
    return errors


def validate_published_site(site: Path) -> list[str]:
    """Return errors when the generated Lite bundle is absent from site output."""
    bundle = site / "jupyterlite"
    if not (bundle / "jupyter-lite.json").is_file():
        return [f"{site}: missing published jupyterlite/jupyter-lite.json"]
    return required_bundle_files(bundle)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--bundle-only",
        action="store_true",
        help="Validate the generated runtime before it is copied into site output.",
    )
    args = parser.parse_args(argv)
    bundle = ROOT / "assets" / "jupyterlite"
    environment_file = ROOT / "tools" / "jupyterlite" / "environment.yml"
    errors = validate_bundle(bundle, environment_file)
    if errors:
        print("\n".join(errors))
        return 1
    if not args.bundle_only:
        published_errors = validate_published_site(ROOT / "_build" / "html")
        if published_errors:
            print("\n".join(published_errors))
            return 1
    print("JupyterLite xeus bundle check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
