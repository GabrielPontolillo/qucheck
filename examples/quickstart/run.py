from pathlib import Path

from qucheck.coordinator import Coordinator


PROPERTIES_DIR = Path(__file__).resolve().parent / "properties"


def main():
    coordinator = Coordinator(num_inputs=10, random_seed=1234)
    results = coordinator.test(
        str(PROPERTIES_DIR),
        measurements=5000,
        run_optimization=True,
    )

    passing = [prop.__name__ for prop in coordinator.test_runner.list_passing_properties()]
    failing = [prop.__name__ for prop in coordinator.test_runner.list_failing_properties()]

    print(f"Circuits executed: {results.number_circuits_executed}")
    print(f"Passing properties: {passing}")
    print(f"Failing properties: {failing}")


if __name__ == "__main__":
    main()
