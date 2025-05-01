#!/usr/bin/env python3
# package.py

import os
import zipfile
from pathlib import Path
import sys

INCLUDE = [
    ".env",
    "environment.yml",
    "requirements.txt",
    "pyproject.toml",
    "setup.py",
    "README.md",
    "structure.txt",
    "docs",
    "mt5/terminal64.exe",
    "logs",
    "data",
    "models",
    "scripts",
    "src",
    "tests",
]

ZIP_NAME = "PerceptraderAI.zip"


def collect_paths(base: Path):
    paths = []
    for entry in INCLUDE:
        p = base / entry
        if not p.exists():
            print(f"Error: expected path not found: {p}", file=sys.stderr)
            sys.exit(1)
        if p.is_file():
            paths.append(p)
        else:
            for dirpath, _, filenames in os.walk(p):
                for fn in filenames:
                    paths.append(Path(dirpath) / fn)
    return paths


def make_zip(base: Path, zip_name: str):
    zip_path = base / zip_name
    if zip_path.exists():
        zip_path.unlink()
    paths = collect_paths(base)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in paths:
            arcname = file_path.relative_to(base)
            zf.write(file_path, arcname)
            print(f"Added {arcname}")
    print(f"\n✅ Created archive: {zip_path}")


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent
    make_zip(project_root, ZIP_NAME)
