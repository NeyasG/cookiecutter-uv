# {{cookiecutter.project_name}}

[![Release](https://img.shields.io/github/v/release/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}})](https://img.shields.io/github/v/release/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}})
[![Build status](https://img.shields.io/github/actions/workflow/status/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/main.yml?branch=main)](https://github.com/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/branch/main/graph/badge.svg)](https://codecov.io/gh/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}})
[![Commit activity](https://img.shields.io/github/commit-activity/m/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}})](https://img.shields.io/github/commit-activity/m/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}})
[![License](https://img.shields.io/github/license/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}})](https://img.shields.io/github/license/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}})

{{cookiecutter.project_description}}

- **Github repository**: <https://github.com/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/>
- **Documentation** <https://{{cookiecutter.author_github_handle}}.github.io/{{cookiecutter.project_name}}/>

## Getting started with your project

### 1. Create a New Repository

First, create a repository on GitHub with the same name as this project, and then run the following commands:

```bash
git init -b main
git add .
git commit -m "init commit"
git remote add origin git@github.com:{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}.git
git push -u origin main
```

### 2. Set Up Your Development Environment

Then, install the environment and the prek hooks with

```bash
make install
```

This will also generate your `uv.lock` file

### 3. Run the prek hooks

Initially, the CI/CD pipeline might be failing due to formatting issues. To resolve those run:

```bash
uv run prek run -a
```

### 4. Commit the changes

Lastly, commit the changes made by the two steps above to your repository.

```bash
git add .
git commit -m 'Fix formatting issues'
git push origin main
```

You are now ready to start development on your project!

## Releasing a new version

This project uses [Commitizen](https://commitizen-tools.github.io/) for versioning:

```bash
# Commit using conventional format
make commit
# OR use git commit manually: "feat: add new feature"

# When ready to release
make bump              # Bumps version, updates CHANGELOG.md, creates tag
git push --follow-tags # Push changes and tags
```

### Conventional Commit Format

- `feat:` — New features (minor version bump)
- `fix:` — Bug fixes (patch version bump)
- `docs:` — Documentation changes
- `BREAKING CHANGE:` — Breaking changes (major version bump)
- Other types: `build:`, `chore:`, `ci:`, `refactor:`, `style:`, `test:`

{% if cookiecutter.publish_to_pypi == "y" -%}

The project is set up to publish to [PyPI](https://pypi.org/) automatically when a new release is created on GitHub.

**Setup (one-time)**

1. Create an account on [PyPI](https://pypi.org/) and generate an API token under *Account settings → API tokens*.
2. Add the token to your repository secrets as `PYPI_TOKEN`: go to
   `https://github.com/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/settings/secrets/actions/new`
   and create a secret named `PYPI_TOKEN` with your token as the value.

**Publishing a new version**

1. Bump the version in `pyproject.toml` to match the release tag (e.g. `version = "0.2.0"`).
2. Commit the change and push to `main`.
3. Create a [new release](https://github.com/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/releases/new) on GitHub with a tag in the form `*.*.*` (e.g. `0.2.0`).

GitHub Actions will automatically build the package with `uv build` and publish it to PyPI using the `PYPI_TOKEN` secret.
{%- endif %}
