from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass

Cells = Sequence[int]
CountFn = Callable[[Cells], int]


@dataclass(frozen=True)
class AlgorithmResult:
    name: str
    positive_cells: int
    positivity: float
    is_positive: bool


@dataclass(frozen=True)
class Algorithm:
    name: str
    count: CountFn
    threshold: float


class UnknownAlgorithmError(ValueError):
    def __init__(self, name: str) -> None:
        super().__init__(f"unknown algorithm: {name!r}")
        self.name = name


def count_even_zeroes(cells: Cells) -> int:
    return sum(1 for i in range(0, len(cells), 2) if cells[i] == 0)


def count_contiguous_ones(cells: Cells) -> int:
    return sum(1 for i in range(len(cells) - 1) if cells[i] == 1 and cells[i + 1] == 1)


def count_surrounded_ones(cells: Cells) -> int:
    return sum(
        1
        for i in range(1, len(cells) - 1)
        if cells[i] == 1 and cells[i - 1] == 0 and cells[i + 1] == 0
    )


_REGISTRY: dict[str, Algorithm] = {
    "even-zeroes": Algorithm("even-zeroes", count_even_zeroes, 0.30),
    "contiguous-ones": Algorithm("contiguous-ones", count_contiguous_ones, 0.20),
    "surrounded-ones": Algorithm("surrounded-ones", count_surrounded_ones, 0.10),
}


def get_algorithm(name: str) -> Algorithm:
    try:
        return _REGISTRY[name]
    except KeyError:
        raise UnknownAlgorithmError(name) from None
