"""Test cookiecutter template across multiple option combinations."""

from __future__ import annotations

import pytest

# Defaults from cookiecutter.json (first item in each list)
DEFAULTS = {
    "layout": "src",  # First item in layout list
    "publish_to_pypi": "y",
    "zensical": "y",
    "open_source_license": "MIT license",
}

# Define meaningful option combinations to test
COMBINATIONS = [
    pytest.param({}, id="all-defaults"),
    pytest.param({"layout": "flat"}, id="flat-layout"),
    pytest.param({"layout": "flat", "zensical": "n"}, id="flat-no-docs"),
    pytest.param({"zensical": "n"}, id="no-docs"),
    pytest.param({"publish_to_pypi": "n"}, id="no-publish"),
    pytest.param({"open_source_license": "Not open source"}, id="proprietary"),
    pytest.param({"open_source_license": "Apache Software License 2.0"}, id="apache-license"),
    pytest.param(
        {"layout": "flat", "publish_to_pypi": "n", "zensical": "n"},
        id="flat-no-publish-no-docs",
    ),
]


def resolve_options(options: dict[str, str]) -> dict[str, str]:
    """Return the full set of resolved options (defaults merged with overrides)."""
    return {**DEFAULTS, **options}


@pytest.mark.parametrize("options", COMBINATIONS)
class TestCombinations:
    """Validate file presence/absence for each option combination."""

    def test_always_present_files(self, bake, options):
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

    def test_license_files(self, bake, options):
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

    def test_documentation_layout(self, bake, options):
        """Verify docs directory is present/absent based on zensical option."""
        project = bake(**options)
        effective = resolve_options(options)

        if effective["zensical"] == "y":
            assert project.has_dir("docs"), "Expected docs/ when zensical='y'"
            assert project.has_file("zensical.toml"), "Expected zensical.toml when zensical='y'"
        else:
            assert not project.has_dir("docs"), "Expected no docs/ when zensical='n'"
            assert not project.has_file("zensical.toml"), "Expected no zensical.toml when zensical='n'"

    def test_source_layout(self, bake, options):
        """Verify correct directory layout based on layout option."""
        project = bake(**options)
        effective = resolve_options(options)

        if effective["layout"] == "src":
            assert project.has_dir("src"), "Expected src/ directory for src layout"
            assert project.has_dir("src/my_project"), "Expected src/my_project for src layout"
            assert not project.has_dir("my_project"), "Expected no top-level my_project for src layout"
        else:
            # flat layout
            assert project.has_dir("my_project"), "Expected my_project/ in root for flat layout"
            assert not project.has_dir("src"), "Expected no src/ for flat layout"

    def test_pyproject_metadata(self, bake, options):
        """Verify pyproject.toml contains correct metadata."""
        project = bake(**options)
        content = project.read_file("pyproject.toml")

        # These should always be present
        assert "name = " in content, "Expected name field in pyproject.toml"
        assert "my-project" in content or "my_project" in content, "Expected project reference"
