# Business logic — mini-nucleiq

How a tissue sample is analyzed and how the screening result is decided.

## Concepts

- **Sample** — a named tissue sample. Its data is a list of **cells**.
- **Cell** — one position, either `0` or `1`. Positions are 0-based.
- **Algorithm** — a rule that marks some cells as **positive**.
- **Positivity** — positive cells ÷ total cells.
- An algorithm is **POSITIVE** when its positivity is strictly above its threshold; otherwise NEGATIVE.

A sample is submitted with one or more algorithms. The result reports, per algorithm, the positive-cell count, the positivity, and its POSITIVE/NEGATIVE outcome — plus the final sample result.

## Algorithms

Thresholds are strict: a positivity exactly on the threshold is NEGATIVE. Examples use `sample-c = [0,0,1,0,0,1,0,1,1,1]`.

**even-zeroes** — a `0` at an even index is positive. Threshold: above 30%.
_Positive at indices 0, 4, 6 → 3 cells (30%) → NEGATIVE._

**contiguous-ones** — a `1` whose next cell is also `1` is positive (only the next neighbour counts).
Threshold: above 20%.
_Positive at indices 7, 8 → 2 cells (20%) → NEGATIVE._

**surrounded-ones** — a `1` whose previous and next cells are both `0` is positive. Cells at the ends are never positive. Threshold: above 10%.
_Positive at indices 2, 5 → 2 cells (20%) → POSITIVE._

## Final result

**POSITIVE when more than half of the selected algorithms are positive; otherwise NEGATIVE.**

It is a strict majority: 2 of 3 is POSITIVE, 1 of 3 is NEGATIVE, 1 of 2 is NEGATIVE.

For `sample-c` with all three algorithms: 1 of 3 is positive → **NEGATIVE**.

> The README's example states POSITIVE for this case, which contradicts its own "more than half" rule. We follow the rule and treat the example's final line as an erratum.

## Validation

- The sample must have at least one cell.
- Every cell must be the integer `0` or `1`.
- At least one algorithm must be selected.
- An unknown algorithm name is rejected and nothing is analyzed.
