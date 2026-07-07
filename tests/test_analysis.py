import pytest

from mini_nucleiq.algorithms import UnknownAlgorithmError
from mini_nucleiq.analysis import InvalidSampleError, analyze

SAMPLE_A = [0, 0, 0, 1, 0, 1, 0, 1, 1, 1]
SAMPLE_B = [0, 0, 0, 0, 0, 1, 0, 1, 1, 1]
SAMPLE_C = [0, 0, 1, 0, 0, 1, 0, 1, 1, 1]
ALL_ALGOS = ["even-zeroes", "contiguous-ones", "surrounded-ones"]


def _by_name(analysis, name):
    return next(result for result in analysis.results if result.name == name)


def test_report_has_one_entry_per_selected_algorithm() -> None:
    analysis = analyze(SAMPLE_A, ["even-zeroes", "surrounded-ones"])
    assert [result.name for result in analysis.results] == ["even-zeroes", "surrounded-ones"]


def test_even_zeroes_at_exact_threshold_is_negative() -> None:
    result = _by_name(analyze(SAMPLE_C, ["even-zeroes"]), "even-zeroes")
    assert (result.positive_cells, result.positivity, result.is_positive) == (3, 0.3, False)


def test_even_zeroes_above_threshold_is_positive() -> None:
    result = _by_name(analyze(SAMPLE_B, ["even-zeroes"]), "even-zeroes")
    assert (result.positive_cells, result.positivity, result.is_positive) == (4, 0.4, True)


def test_surrounded_ones_above_threshold_is_positive() -> None:
    result = _by_name(analyze(SAMPLE_C, ["surrounded-ones"]), "surrounded-ones")
    assert (result.positive_cells, result.is_positive) == (2, True)


def test_surrounded_ones_at_exact_threshold_is_negative() -> None:
    result = _by_name(analyze(SAMPLE_B, ["surrounded-ones"]), "surrounded-ones")
    assert (result.positive_cells, result.positivity, result.is_positive) == (1, 0.1, False)


def test_majority_positive_yields_positive_final() -> None:
    analysis = analyze(SAMPLE_A, ALL_ALGOS)
    positives = sum(1 for result in analysis.results if result.is_positive)
    assert positives == 2
    assert analysis.final == "POSITIVE"


def test_minority_positive_yields_negative_final() -> None:
    analysis = analyze(SAMPLE_C, ALL_ALGOS)
    positives = sum(1 for result in analysis.results if result.is_positive)
    assert positives == 1
    assert analysis.final == "NEGATIVE"


def test_exactly_half_positive_yields_negative_final() -> None:
    analysis = analyze(SAMPLE_C, ["surrounded-ones", "even-zeroes"])
    assert analysis.final == "NEGATIVE"


def test_readme_example_sample_c_all_algorithms() -> None:
    analysis = analyze(SAMPLE_C, ALL_ALGOS, sample_name="sample-c")
    assert _by_name(analysis, "even-zeroes").positive_cells == 3
    assert _by_name(analysis, "contiguous-ones").positive_cells == 2
    assert _by_name(analysis, "surrounded-ones").positive_cells == 2
    assert analysis.final == "NEGATIVE"


def test_unknown_algorithm_is_rejected() -> None:
    with pytest.raises(UnknownAlgorithmError):
        analyze(SAMPLE_A, ["even-zeroes", "does-not-exist"])


def test_empty_cells_are_rejected() -> None:
    with pytest.raises(InvalidSampleError):
        analyze([], ["even-zeroes"])


def test_non_binary_cells_are_rejected() -> None:
    with pytest.raises(InvalidSampleError):
        analyze([0, 1, 2], ["even-zeroes"])


@pytest.mark.parametrize("cells", [[True, False], [0.0, 1.0], ["0", "1"]])
def test_non_integer_cells_are_rejected(cells: list) -> None:
    with pytest.raises(InvalidSampleError):
        analyze(cells, ["even-zeroes"])


def test_empty_algorithm_selection_is_rejected() -> None:
    with pytest.raises(ValueError):
        analyze(SAMPLE_A, [])
