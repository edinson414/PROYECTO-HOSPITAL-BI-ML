"""Compatibility package.

This package makes `import hospital_bi_ml.*` resolve to the modules
stored in the `src/` directory without moving files. It prepends the
`src` path to this package's `__path__` so submodule lookups find files
under `src/` (e.g. `src/config.py` -> `hospital_bi_ml.config`).
"""
import os

package_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(package_dir, os.pardir))
src_path = os.path.join(project_root, "src")

if os.path.isdir(src_path) and src_path not in __path__:
    __path__.insert(0, src_path)

__all__ = []
