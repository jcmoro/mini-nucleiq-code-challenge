from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

from mini_nucleiq.algorithms import AlgorithmResult, Cells, get_algorithm

FinalResult = Literal["POSITIVE", "NEGATIVE"]


@dataclass(frozen=True)
class SampleAnalysis:
    results: tuple[AlgorithmResult, ...]
    final: FinalResult
    sample_name: str | None = None


class InvalidSampleError(ValueError):
    pass


def _validate(cells: Cells) -> None:
    if len(cells) == 0:
        raise InvalidSampleError("cells must not be empty")
    if any(type(cell) is not int or cell not in (0, 1) for cell in cells):
        raise InvalidSampleError("cells must contain only the integers 0 and 1")


def analyze(
    cells: Cells,
    algorithm_names: Sequence[str],
    sample_name: str | None = None,
) -> SampleAnalysis:
    if not algorithm_names:
        raise InvalidSampleError("at least one algorithm must be selected")
    _validate(cells)

    results = []
    for name in algorithm_names:
        algorithm = get_algorithm(name)
        positive_cells = algorithm.count(cells)
        positivity = positive_cells / len(cells)
        results.append(
            AlgorithmResult(
                name=algorithm.name,
                positive_cells=positive_cells,
                positivity=positivity,
                is_positive=positivity > algorithm.threshold,
            )
        )

    positive_algorithms = sum(1 for result in results if result.is_positive)
    is_majority = positive_algorithms > len(results) / 2
    final: FinalResult = "POSITIVE" if is_majority else "NEGATIVE"

    return SampleAnalysis(results=tuple(results), final=final, sample_name=sample_name)
