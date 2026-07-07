import pytest

from mini_nucleiq.algorithms import (
    UnknownAlgorithmError,
    count_contiguous_ones,
    count_even_zeroes,
    count_surrounded_ones,
    get_algorithm,
)

SAMPLE_A = [0, 0, 0, 1, 0, 1, 0, 1, 1, 1]
SAMPLE_B = [0, 0, 0, 0, 0, 1, 0, 1, 1, 1]
SAMPLE_C = [0, 0, 1, 0, 0, 1, 0, 1, 1, 1]
SAMPLE_D = [0, 0, 0, 0, 0, 1, 0, 0, 1, 1]
SAMPLE_E = [0, 0, 0, 0, 0, 0, 1, 0, 1, 1]


@pytest.mark.parametrize(
    ("cells", "expected"),
    [(SAMPLE_A, 4), (SAMPLE_B, 4), (SAMPLE_C, 3), (SAMPLE_D, 4), (SAMPLE_E, 3)],
)
def test_even_zeroes_counts(cells: list[int], expected: int) -> None:
    assert count_even_zeroes(cells) == expected


@pytest.mark.parametrize(
    ("cells", "expected"),
    [(SAMPLE_A, 2), (SAMPLE_B, 2), (SAMPLE_C, 2), (SAMPLE_D, 1), (SAMPLE_E, 1)],
)
def test_contiguous_ones_counts(cells: list[int], expected: int) -> None:
    assert count_contiguous_ones(cells) == expected


def test_contiguous_ones_counts_each_one_with_a_following_one() -> None:
    assert count_contiguous_ones([1, 1, 1, 1]) == 3


@pytest.mark.parametrize(
    ("cells", "expected"),
    [(SAMPLE_A, 2), (SAMPLE_B, 1), (SAMPLE_C, 2), (SAMPLE_D, 1), (SAMPLE_E, 1)],
)
def test_surrounded_ones_counts(cells: list[int], expected: int) -> None:
    assert count_surrounded_ones(cells) == expected


def test_surrounded_ones_ignores_boundary_ones() -> None:
    assert count_surrounded_ones([1, 0, 0, 0, 1]) == 0


def test_get_algorithm_returns_registered_algorithm() -> None:
    assert get_algorithm("even-zeroes").threshold == 0.30


def test_get_algorithm_rejects_unknown_name() -> None:
    with pytest.raises(UnknownAlgorithmError):
        get_algorithm("nope")
