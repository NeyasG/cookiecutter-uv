# Cookiecutter-uv

This is a modern Cookiecutter template that can be used to initiate a Python project with all the necessary tools for development, testing, and deployment. It supports the following features:

- [uv](https://docs.astral.sh/uv/) for dependency management
- Supports both [src and flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/).
- CI/CD with [GitHub Actions](https://github.com/features/actions) (Currently a WIP)
- Pre-commit hooks with [prek](https://prek.j178.dev/)
- Code quality with [ruff](https://github.com/charliermarsh/ruff), [ty](https://docs.astral.sh/ty/).
- Publishing to [PyPI](https://pypi.org) by creating a new release on GitHub (Currently a WIP)
- Testing and coverage with [pytest](https://docs.pytest.org/en/7.1.x/).
- Documentation with [zensical](https://zensical.org/)
- Release management and commit discipline with [commitizen](https://commitizen-tools.github.io/commitizen/) (Currently a WIP)

This project was forked from [cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv)

## Quickstart

On your local machine, navigate to the directory in which you want to
create a project directory, and run the following command:

```bash
uvx cookiecutter https://github.com/NeyasG/cookiecutter-uv.git
```

or if you don't have `uv` installed yet:

```bash
pip install cookiecutter
cookiecutter https://github.com/NeyasG/cookiecutter-uv.git
```

Follow the prompts to configure your project. Once completed, a new directory containing your project will be created. Then navigate into your newly created project directory and follow the instructions in the `README.md` to complete the setup of your project.

### Acknowledgements

This project is partially based on [Audrey
Feldroy's](https://github.com/audreyfeldroy) great
[cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage).
