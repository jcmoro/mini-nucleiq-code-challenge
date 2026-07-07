from mini_nucleiq import analyze_sample

ALGORITHMS = ["even-zeroes", "contiguous-ones", "surrounded-ones"]
SAMPLES = ["sample-a", "sample-b", "sample-c", "sample-d", "sample-e"]


def main() -> None:
    for name in SAMPLES:
        analysis = analyze_sample(name, ALGORITHMS)
        print(f"{analysis.sample_name}:")
        for result in analysis.results:
            outcome = "POSITIVE" if result.is_positive else "NEGATIVE"
            positivity = f"{result.positivity:.0%}"
            print(f"  {result.name}: {result.positive_cells} cells, {positivity} -> {outcome}")
        print(f"  final: {analysis.final}\n")


if __name__ == "__main__":
    main()
