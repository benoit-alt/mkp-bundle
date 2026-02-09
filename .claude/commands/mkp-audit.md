<!-- Part of MKP Claude integration pack v1.0.2 – update here, then re-export the pack. -->
# /mkp-audit — Validate, Load, Summarize

- Canonical strict flow: `validate` → `load --write-sqlite` → optional `build-labels`.
- Uses local `./mkpctl-*.whl` if needed; no network installs in-editor.

## Offline install (required)
Offline install: `PIP_NO_INDEX=1 python -m pip install --no-index ./mkpctl-*.whl` (fail if wheel missing; do not use PyPI).
