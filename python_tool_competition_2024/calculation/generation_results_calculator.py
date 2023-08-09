"""Calculator to gather generation results."""

from ..config import Config
from ..generation_results import (
    TestGenerationFailure,
    TestGenerationResult,
    TestGenerationSuccess,
)
from ..generator_plugins import find_generator
from ..generators import FileInfo
from ..target_finder import Target


def calculate_generation_result(target: Target, config: Config) -> TestGenerationResult:
    """Calculate the mutation analysis results."""
    generator = find_generator(config.generator_name)()
    result = generator.build_test(_target_to_file_info(target, config))
    if isinstance(result, TestGenerationFailure) and config.show_failures:
        config.console.print(f"Target {target.source} failed with {result.reason}")
        for line in result.error_lines:
            config.console.print("-", line)
    if isinstance(result, TestGenerationSuccess):
        target.test.parent.mkdir(parents=True, exist_ok=True)
        target.test.write_text(result.body, encoding="utf-8")
    return result


def _target_to_file_info(target: Target, config: Config) -> FileInfo:
    return FileInfo(
        absolute_path=target.source, module_name=target.source_module, config=config
    )
