# cookiecutter-uv

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A Python project template that gets you up and running with [uv](https://docs.astral.sh/uv/), modern code quality tools, and optional CI/CD—all batteries included.

Inspired by [cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv) by [fpgmaas](https://github.com/fpgmaas).

## What This Is

`cookiecutter-uv` is a [Cookiecutter](https://cookiecutter.readthedocs.io/) template that generates new Python projects with:

- [uv](https://docs.astral.sh/uv/) for fast dependency management
- [Ruff](https://docs.astral.sh/ruff/) for linting and formatting
- [ty](https://docs.astral.sh/ty/) for type checking
- [pytest](https://docs.pytest.org/) for testing
- [prek](https://prek.j178.dev/) for pre-commit hooks
- Optional [deptry](https://github.com/fpgmaas/deptry), [zensical](https://github.com/zensical/zensical) docs, GitHub Actions CI, and PyPI publishing

Choose your project layout (src or flat), pick a license, and toggle features on or off.

## Getting Started

To use this template, you'll need:

- Python 3.11+ (for running the template)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (package installer)
- [Cookiecutter](https://cookiecutter.readthedocs.io/)
- `make` (for running build tasks)

### Generate a Project

```bash
# Install cookiecutter (one-time setup)
uv tool install cookiecutter

# Generate your project
cookiecutter https://github.com/NeyasG/cookiecutter-uv
```

The template will ask you to configure:

- `project_name`: Name of your project (use hyphens)
- `project_description`: Short description
- `author` and `email`: Your details
- `author_github_handle`: Your GitHub username
- `layout`: `src` (recommended) or `flat`
- `publish_to_pypi`: Enable PyPI publishing setup
- `deptry`: Enable dependency auditing
- `zensical`: Enable documentation with MkDocs
- `open_source_license`: MIT, BSD, ISC, Apache 2.0, GPL v3, or none
- `include_github_actions`: Enable GitHub Actions CI

### Initialize Your Project

```bash
cd my-project

# Install dependencies
uv sync

# Install pre-commit hooks
uv run prek install

# Run checks
make check
```

## Working With Your Generated Project

After creating a project, here are the main tasks you'll do:

### Install Dependencies

```bash
uv sync
uv run prek install
```

### Run Quality Checks

```bash
make check        # Everything: linting, formatting, type checks, tests
make test         # Just tests
```

Or run individual tools:

```bash
uv run ruff check .     # Lint
uv run ruff format .    # Format
uv run ty check .       # Type check
uv run pytest
```

### Generate Documentation

If you enabled Zensical:

```bash
make docs
```

### Publishing to PyPI

If you enabled `publish_to_pypi`, create a [PyPI account](https://pypi.org/account/register/) and API token, then add it as a GitHub secret (`PYPI_TOKEN`). When you tag a release (`git tag v1.0.0`), GitHub Actions will automatically build and publish it.

## Contributing

Want to improve the template or add a feature?

```bash
git clone https://github.com/NeyasG/cookiecutter-uv
cd cookiecutter-uv
uv sync
uv run prek install
```

Test your changes:

```bash
make bake              # Generate a test project
make test              # Run the full test suite
make check             # Run linting and type checks
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Making Releases

This repository uses [Commitizen](https://commitizen-tools.github.io/) for versioning:

```bash
# Commit using conventional format
make commit
# OR use git commit manually: "feat: add new feature"
# OR use the VSCode Conventional Commits extension (search "Conventional Commits" in the Extensions panel)

# When ready to release
make bump              # Bumps version, updates CHANGELOG.md, creates tag
git push --follow-tags # Push changes and tags
```

### Conventional Commit Format

- `feat:` — New features (minor version bump)
- `fix:` — Bug fixes (patch version bump)
- `docs:` — Documentation changes
- `BREAKING CHANGE:` — Breaking changes (major version bump)
- Other types: `build:`, `chore:`, `ci:`, `refactor:`, `revert:`, `style:`, `test:`

### Recommended PR Strategy

For the cleanest commit history and changelog generation, configure your GitHub repository to use **squash merging**:

1. Go to **Settings → General → Pull Requests**
2. Enable **Allow squash merging**
3. Set **Default commit message** to **Pull request title**
4. Optionally disable merge commits and rebase merging to enforce squash-only merges

With this setup, PR titles (which must follow the conventional commit format and are linted by the `pr-title` workflow) become the squash commit messages that Commitizen parses to generate the changelog.

## Testing

The template includes comprehensive tests:

- Input validation tests for project names
- Combination tests covering all feature flags
- Integration tests that bake real projects and run checks

```bash
make test              # Run all tests
uv run pytest -v       # Verbose output
uv run pytest --cov    # With coverage
```

## Dependencies

Generated projects include:

- **uv** — Package management
- **Ruff** — Linting and formatting
- **ty** — Type checking
- **pytest** — Testing
- **prek** — Pre-commit hooks

Optional additions:

- **deptry** — Dependency auditing
- **Zensical** — Documentation with MkDocs

## License

This template is MIT licensed—see [LICENSE](LICENSE).

Generated projects use the license you select during creation.

---

Created by [Neyas Guruswamy](https://github.com/NeyasG)

Inspiration drawn from [fpgmaas/cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv).
