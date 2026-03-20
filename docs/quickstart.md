# Quickstart: run QuCheck on an example property

This guide shows the smallest useful way to run QuCheck on example properties.
It uses two included properties:

- `examples/quickstart/properties/single_qubit_probability_property.py`
- `examples/quickstart/properties/single_qubit_wrong_probability_property.py`

and the runner script in `examples/quickstart/run.py`.

## 1. Create a Python 3.11 environment

QuCheck requires Python 3.11 or newer.
Use whichever launcher is available on your machine (`python`, `python3`, or `py -3.11`).

### Windows PowerShell

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install .
```

### macOS / Linux

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install .
```

## 2. Run the included example

From the repository root, run:

```bash
python examples/quickstart/run.py
```

The script will:

1. Load both property classes from `examples/quickstart/properties`
2. Generate 10 random one-qubit input states
3. Execute each circuit with 5000 measurements
4. Report which properties passed or failed

The output includes some internal debug logging from QuCheck.
The important lines at the end should look like this:

```text
Passing properties: ['SingleQubitProbabilityProperty']
Failing properties: ['SingleQubitWrongProbabilityProperty']
```

## 3. What the example property is doing

`SingleQubitProbabilityProperty` defines one randomly generated input state:

```python
def get_input_generators(self):
    return [RandomState(1)]
```

For each generated state, it builds a one-qubit circuit, initializes that state,
and checks that measuring qubit `0` in the Z basis matches the expected probability of getting `0`:

```python
probability_of_zero = abs(state[0]) ** 2
self.statistical_analysis.assert_probability(
    self,
    [0],
    circuit,
    [probability_of_zero],
    basis=["z"],
)
```

`SingleQubitWrongProbabilityProperty` uses the wrong probability:

```python
wrong_probability_of_zero = 1 - abs(state[0]) ** 2
```

## 4. Adapting this for your own property

The usual workflow is:

1. Create a new `.py` file containing a class that inherits from `qucheck.property.Property`
2. Implement `get_input_generators`, `preconditions`, and `operations`
3. Add one or more QuCheck assertions inside `operations`
4. Point `Coordinator.test(...)` at the folder containing that property file

The key line in the runner is:

```python
results = coordinator.test(str(PROPERTIES_DIR), measurements=5000)
```

`Coordinator` scans that directory for Python files, imports any `Property` subclasses it finds, and runs them.

## 5. Useful next examples

If you want a more realistic property after the quickstart, these are good follow-ups:

- `case_studies/quantum_teleportation/input_reg0_equal_to_output_reg2_property.py`
- `tests/mock_properties/probability_property.py`
- `tests/mock_properties/entangled_test_property.py`
