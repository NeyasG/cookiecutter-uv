"""Test cookiecutter template across multiple option combinations."""

import json
import tomllib
from pathlib import Path
from typing import Callable

import pytest
from conftest import BakedProject

# Defaults from cookiecutter.json (first item in each list)
DEFAULTS = {
    "layout": "src",  # First item in layout list
    "publish_to_pypi": "n",
    "deptry": "y",
    "zensical": "y",
    "open_source_license": "MIT license",
    "include_github_actions": "y",
}

COOKIECUTTER_CONFIG = json.loads((Path(__file__).parent.parent / "cookiecutter.json").read_text())
DEFAULT_PROJECT_NAME = COOKIECUTTER_CONFIG["project_name"]
DEFAULT_PROJECT_SLUG = DEFAULT_PROJECT_NAME.lower().replace("-", "_")

# Define meaningful option combinations to test
COMBINATIONS = [
    pytest.param({}, id="all-defaults"),
    pytest.param({"layout": "flat"}, id="flat-layout"),
    pytest.param({"layout": "flat", "zensical": "n"}, id="flat-no-docs"),
    pytest.param({"zensical": "n"}, id="no-docs"),
    pytest.param({"publish_to_pypi": "y"}, id="with-publish"),
    pytest.param({"publish_to_pypi": "n"}, id="no-publish"),
    pytest.param({"open_source_license": "Not open source"}, id="proprietary"),
    pytest.param({"open_source_license": "Apache Software License 2.0"}, id="apache-license"),
    pytest.param(
        {"layout": "flat", "publish_to_pypi": "n", "zensical": "n"},
        id="flat-no-publish-no-docs",
    ),
    pytest.param({"deptry": "n"}, id="no-deptry"),
    pytest.param({"layout": "flat", "deptry": "n"}, id="flat-no-deptry"),
    pytest.param({"include_github_actions": "n"}, id="no-github-actions"),
    pytest.param({"include_github_actions": "y"}, id="with-github-actions"),
]


def resolve_options(options: dict[str, str]) -> dict[str, str]:
    """Return the full set of resolved options (defaults merged with overrides)."""
    return {**DEFAULTS, **options}


@pytest.mark.parametrize("options", COMBINATIONS)
class TestCombinations:
    """Validate file presence/absence for each option combination."""

    def test_always_present_files(self, bake: Callable[..., BakedProject], options: dict[str, str]) -> None:
        """Core files should always be present regardless of options."""
        EXPECTED_FILES = [
            "pyproject.toml",
            "README.md",
            "Makefile",
            ".gitignore",
            "tests",
        ]
        project = bake(**options)
        for rel_path in EXPECTED_FILES:
            assert (project.path / rel_path).exists(), f"Expected {rel_path} to exist"

    def test_license_files(self, bake: Callable[..., BakedProject], options: dict[str, str]):
        """Verify correct license file is selected."""
        project = bake(**options)
        effective = resolve_options(options)

        license_mapping = {
            "MIT license": "LICENSE",
            "BSD license": "LICENSE",
            "ISC license": "LICENSE",
            "Apache Software License 2.0": "LICENSE",
            "GNU General Public License v3": "LICENSE",
        }

        # Check that the right license file exists and others don't
        if effective["open_source_license"] in license_mapping:
            assert project.has_file("LICENSE"), f"Expected LICENSE file for {effective['open_source_license']}"
        else:
            # "Not open source" case
            assert not project.has_file("LICENSE"), "Expected no LICENSE file for non-open source"

    def test_documentation_layout(self, bake: Callable[..., BakedProject], options: dict[str, str]):
        """Verify docs directory is present/absent based on zensical option."""
        project = bake(**options)
        effective = resolve_options(options)

        if effective["zensical"] == "y":
            assert project.has_dir("docs"), "Expected docs/ when zensical='y'"
            assert project.has_file("zensical.toml"), "Expected zensical.toml when zensical='y'"
        else:
            assert not project.has_dir("docs"), "Expected no docs/ when zensical='n'"
            assert not project.has_file("zensical.toml"), "Expected no zensical.toml when zensical='n'"

    def test_source_layout(self, bake: Callable[..., BakedProject], options: dict[str, str]):
        """Verify correct directory layout based on layout option."""
        project = bake(**options)
        effective = resolve_options(options)

        if effective["layout"] == "src":
            assert project.has_dir("src"), "Expected src/ directory for src layout"
            assert project.has_dir(f"src/{DEFAULT_PROJECT_SLUG}"), f"Expected src/{DEFAULT_PROJECT_SLUG} for src layout"
            assert not project.has_dir(DEFAULT_PROJECT_SLUG), (
                f"Expected no top-level {DEFAULT_PROJECT_SLUG} for src layout"
            )
        else:
            # flat layout
            assert project.has_dir(DEFAULT_PROJECT_SLUG), f"Expected {DEFAULT_PROJECT_SLUG}/ in root for flat layout"
            assert not project.has_dir("src"), "Expected no src/ for flat layout"

    def test_pyproject_metadata(self, bake: Callable[..., BakedProject], options: dict[str, str]):
        """Verify pyproject.toml contains correct metadata."""
        project = bake(**options)
        content = project.read_file("pyproject.toml")
        pyproject = tomllib.loads(content)

        assert "project" in pyproject, "Missing [project] section"
        assert pyproject["project"]["name"] == "my-project", f"Unexpected name: {pyproject['project']['name']}"
        assert "version" in pyproject["project"], "Missing version field"

    def test_deptry_configuration(self, bake: Callable[..., BakedProject], options: dict[str, str]):
        """Verify deptry is configured when deptry='y' and absent when 'n'."""
        project = bake(**options)
        effective = resolve_options(options)

        pyproject_content = project.read_file("pyproject.toml")
        prek_content = project.read_file("prek.toml")
        makefile_content = project.read_file("Makefile")

        if effective["deptry"] == "y":
            assert "deptry" in pyproject_content, "Expected deptry in pyproject.toml dev deps when deptry='y'"
            assert "deptry" in prek_content, "Expected deptry hook in prek.toml when deptry='y'"
            assert "deptry" in makefile_content, "Expected deptry in Makefile when deptry='y'"
        else:
            assert "deptry" not in pyproject_content, "Expected no deptry in pyproject.toml when deptry='n'"
            assert "deptry" not in prek_content, "Expected no deptry hook in prek.toml when deptry='n'"
            assert "deptry" not in makefile_content, "Expected no deptry in Makefile when deptry='n'"

    def test_github_actions(self, bake: Callable[..., BakedProject], options: dict[str, str]):
        """Verify .github/workflows/ci.yml is present/absent based on include_github_actions option."""
        project = bake(**options)
        effective = resolve_options(options)

        if effective["include_github_actions"] == "y":
            assert project.has_dir(".github"), "Expected .github/ when include_github_actions='y'"
            assert project.has_file(".github/workflows/ci.yml"), (
                "Expected .github/workflows/ci.yml when include_github_actions='y'"
            )
            assert project.is_valid_yaml(".github/workflows/ci.yml"), "Expected valid YAML in .github/workflows/ci.yml"
            if effective["zensical"] == "y":
                assert project.has_file(".github/workflows/docs.yml"), (
                    "Expected .github/workflows/docs.yml when include_github_actions='y' and zensical='y'"
                )
                assert project.is_valid_yaml(".github/workflows/docs.yml"), (
                    "Expected valid YAML in .github/workflows/docs.yml"
                )
            else:
                assert not project.has_file(".github/workflows/docs.yml"), (
                    "Expected no .github/workflows/docs.yml when zensical='n'"
                )
        else:
            assert not project.has_dir(".github"), "Expected no .github/ when include_github_actions='n'"

    def test_publish_workflow(self, bake: Callable[..., BakedProject], options: dict[str, str]):
        """Verify publish.yml is present/absent based on publish_to_pypi and include_github_actions options."""
        project = bake(**options)
        effective = resolve_options(options)

        if effective["include_github_actions"] == "y" and effective["publish_to_pypi"] == "y":
            assert project.has_file(".github/workflows/publish.yml"), (
                "Expected .github/workflows/publish.yml when publish_to_pypi='y' and include_github_actions='y'"
            )
            assert project.is_valid_yaml(".github/workflows/publish.yml"), (
                "Expected valid YAML in .github/workflows/publish.yml"
            )
            assert project.file_contains(".github/workflows/publish.yml", "uv publish"), (
                "Expected 'uv publish' in publish.yml"
            )
            assert project.file_contains(".github/workflows/publish.yml", "PYPI_TOKEN"), (
                "Expected 'PYPI_TOKEN' secret reference in publish.yml"
            )
        else:
            assert not project.has_file(".github/workflows/publish.yml"), (
                "Expected no .github/workflows/publish.yml when publish_to_pypi='n' or include_github_actions='n'"
            )

    def test_readme_pypi_section(self, bake: Callable[..., BakedProject], options: dict[str, str]):
        """Verify README contains PyPI section only when publish_to_pypi='y'."""
        project = bake(**options)
        effective = resolve_options(options)

        if effective["publish_to_pypi"] == "y":
            assert project.file_contains("README.md", "PYPI_TOKEN"), (
                "Expected PYPI_TOKEN in README when publish_to_pypi='y'"
            )
            assert project.file_contains("README.md", "PyPI"), (
                "Expected PyPI section in README when publish_to_pypi='y'"
            )
        else:
            assert not project.file_contains("README.md", "PYPI_TOKEN"), (
                "Expected no PYPI_TOKEN in README when publish_to_pypi='n'"
            )
