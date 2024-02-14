#
# Copyright (c) 2023 Nicolas Erni.
#
# This file is part of python-tool-competition-2024
# (see https://github.com/ThunderKey/python-tool-competition-2024/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""Reporter to write a CSV file."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Literal, Any

from ..config import Config
from ..results import RatioResults, Results, RatioResult


def report_csv(results: Results, config: Config) -> None:
    """Report the results as a CSV to the file configured in `Config`."""
    config.csv_file.parent.mkdir(exist_ok=True, parents=True)
    with config.csv_file.open("w+", encoding="utf-8") as fp:
        writer = csv.writer(fp)
        writer.writerow(
            (
                "target",
                "successful ratio",
                "files",
                "successful files",
                "line coverage",
                "lines",
                "covered lines",
                "branch coverage",
                "branches",
                "covered branches",
                "mutation score",
                "mutants",
                "killed mutants",
            )
        )
        writer.writerows(
            _result_to_csv_row(result.target.relative_source, result)
            for result in results
        )
        writer.writerow(_result_to_csv_row("total", results))


def maybe(obj: RatioResult | None, field: str) -> Any:
    if obj is None:
        return None
    return getattr(obj, field)


def _result_to_csv_row(
    target: Path | Literal["total"], ratios: RatioResults
) -> tuple[Any, ...]:
    return (
        target,
        maybe(ratios.generation_results, 'ratio'),
        maybe(ratios.generation_results, 'total'),
        maybe(ratios.generation_results, 'successful'),
        maybe(ratios.line_coverage, 'ratio'),
        maybe(ratios.line_coverage, 'total'),
        maybe(ratios.line_coverage, 'successful'),
        maybe(ratios.branch_coverage, 'ratio'),
        maybe(ratios.branch_coverage, 'total'),
        maybe(ratios.branch_coverage, 'successful'),
        maybe(ratios.mutation_analysis, 'ratio'),
        maybe(ratios.mutation_analysis, 'total'),
        maybe(ratios.mutation_analysis, 'successful'),
    )
