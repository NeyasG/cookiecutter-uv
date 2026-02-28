from typing import Callable

import pytest
from conftest import BakedProject
from cookiecutter.exceptions import FailedHookException

BakeFixture = Callable[..., BakedProject]


def test_bake_project(bake: BakeFixture) -> None:
    result = bake()
    result.run_check()


@pytest.mark.parametrize(
    "project_name, generated_slug",
    [("my-project", "my_project"), ("MyProject", "myproject"), ("a-b-c-123", "a_b_c_123"), ("a-b", "a_b")],
)
def test_valid_project_names(bake: BakeFixture, project_name) -> None:
    result = bake(project_name=project_name)

    result.run_check()


@pytest.mark.parametrize("project_name", ["my_project", "123-invalid", "@bad"])
def test_invalid_names(bake: BakeFixture, project_name) -> None:
    with pytest.raises(FailedHookException):
        bake(project_name=project_name)
