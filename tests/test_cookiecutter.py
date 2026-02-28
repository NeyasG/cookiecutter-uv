from collections.abc import Callable

from conftest import BakedProject


def test_bake_project(bake: Callable[..., BakedProject]) -> None:
    result = bake()
    result.run_check()
