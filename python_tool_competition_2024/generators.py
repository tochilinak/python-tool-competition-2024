"""Base classes and helpers for the generators."""


import abc
import dataclasses
import importlib
import os
import sys
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from types import ModuleType

from .config import Config
from .generation_results import TestGenerationResult, TestGenerationSuccess


@dataclasses.dataclass(frozen=True)
class FileInfo:
    """A wrapper around file information and helper functions for targets."""

    absolute_path: Path
    """The absoulte path of the target file."""

    module_name: str
    """The module name of the target file."""

    config: Config
    """The configuration of the current run of the competition tool."""

    def import_module(self) -> ModuleType:
        """Import the module that represents this file."""
        with _extend_path(self.config.targets_dir):
            return importlib.import_module(self.module_name)


class TestGenerator(abc.ABC):
    """A base test generator to generate tests for specific files."""

    @abc.abstractmethod
    def build_test(
        self, target_file_info: FileInfo  # noqa: V107
    ) -> TestGenerationResult:
        """
        Genereate a test for the specific target file.

        Args:
            target_file: The `FileInfo` of the file to generate a test for.

        Returns:
            Either a `TestGenerationSuccess` if it was successful, or a
            `TestGenerationFailure` otherwise.
        """
        raise NotImplementedError


class DummyTestGenerator(TestGenerator):
    """A test generator that generates dummy tests that do nothing."""

    def build_test(self, target_file_info: FileInfo) -> TestGenerationResult:
        """
        Genereate a dummy test for the specific target file.

        The test file will only contain a comment and a test with `assert True`.

        Args:
            target_file: The `FileInfo` of the file to generate a test for.

        Returns:
            A `TestGenerationSuccess` containing the dummy content.
        """
        return TestGenerationSuccess(
            os.linesep.join(
                (
                    f"# dummy test for {target_file_info.absolute_path}",
                    "",
                    "",
                    "def test_dummy() -> None:",
                    "    assert True",
                )
            )
        )


@contextmanager
def _extend_path(path: Path) -> Iterator[None]:
    old_path = sys.path
    sys.path = [*sys.path, str(path)]
    try:
        yield
    finally:
        sys.path = old_path


__all__ = ["FileInfo", "TestGenerator", "DummyTestGenerator"]
