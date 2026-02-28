# Project Guidelines

## Code Style
- Python-first project using `uv`; target Python is `>=3.10,<4.0`.
- Keep line length at 120 and rely on Ruff auto-fix (`[tool.ruff] fix = true`).
- Use existing pre-commit pipeline as the style gate; do not introduce parallel lint stacks.
- Follow examples in `pyproject.toml`, `.pre-commit-config.yaml`, and `{{cookiecutter.project_name}}/pyproject.toml`.

## Architecture
- This repository is a Cookiecutter template, not a normal app package.
- Inputs are declared in `cookiecutter.json` and validated in `hooks/pre_gen_project.py`.
- Post-generation structure is enforced in `hooks/post_gen_project.py`:
  - optional docs removal (`docs/`, `zensical.toml`)
  - license file selection/cleanup
  - layout switch (`flat` vs `src`) by moving `{{cookiecutter.project_slug}}`.
- Treat both root files and `{{cookiecutter.project_name}}/*` as first-class template surfaces.

## Build and Test
- Install dev environment: `uv sync`
- Install hooks: `uv run pre-commit install`
- Quality checks: `make check`
- Tests: `make test`
- Build docs checks (if docs enabled): `make docs-test`
- Build package artifacts: `make build`
- Template smoke generation: `make bake` (flat) or `make bake-src` (src layout)

## Project Conventions
- Naming rules are strict and enforced before generation:
  - `project_name` must use hyphens (no `_`)
  - `project_slug` must use underscores (no `-`)
- When changing template options, update both hook logic and templated files together.
- Keep generated-project workflows aligned with `{{cookiecutter.project_name}}/Makefile` and `{{cookiecutter.project_name}}/CONTRIBUTING.md`.
- Prefer minimal, template-safe edits over project-specific assumptions.

## Integration Points
- Core integrations: Cookiecutter, uv/uv_build, pre-commit, Ruff, ty, pytest, optional zensical/mkdocstrings.
- Build backend and package layout are coordinated via `{{cookiecutter.project_name}}/pyproject.toml` (`[tool.uv.build-backend] module-root`).
- Docs behavior is controlled by `cookiecutter.zensical` and hook removal logic.

## Security
- Keep lockfile integrity checks (`uv lock --locked`) in validation flows.
- Preserve lint rule families that include security checks (Ruff `S` rules in template pyproject).
- Treat publish paths as sensitive (`make publish`, Twine upload, `PYPI_TOKEN` secret expectations in templated README).
- Do not bypass pre-gen validation hooks when modifying naming- or path-dependent logic.
