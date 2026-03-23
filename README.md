# QuCheck

Property-based testing for Qiskit programs.

## Installation

QuCheck requires Python 3.11 or newer.

### Install from PyPI

For most users, this is the simplest option:

```bash
conda create -n qucheck_env python=3.11
conda activate qucheck_env
pip install qucheck
```

### Install from the repository

If you want to run the bundled examples, work on the source, or edit the package locally:

```bash
conda create -n qucheck_env python=3.11
conda activate qucheck_env
cd path/to/qucheck
pip install .
```

## Quickstart

If you want to run the bundled example properties from this repository, start with [docs/quickstart.md](docs/quickstart.md).

The quickstart uses:

- `examples/quickstart/properties/single_qubit_probability_property.py`
- `examples/quickstart/properties/single_qubit_wrong_probability_property.py`
- `examples/quickstart/run.py`

### RQ1:

To run the experiment in RQ1, execute: `case_studies/multithreaded_test_runner.py`

This will use all cores available on your machine to execute all case studies under all combinations of numbers or properties, inputs, and shots (can be modified in the `test_and_store_parallel` function).
You can modify the number of threads used by changing the `MAX_WORKERS` variable in the script.

The results will be stored in the `case_studies/mutation_test_results` directory as CSV files.

(3 property, 100 input, 2500 and 4200 shots experiments will also be performed,
which we use as a basis for comparison in RQ2)

### RQ2:

To run the comparison with the MITRE unit tests, navigate to the `case_studies/MITRE_unit_test_baseline` directory and execute:
- `deutsch_jozsa.py`
- `grover_tests.py`
- `qft_tests.py`
- `teleportation.py`

The results will be stored in the `case_studies/mutation_test_results` directory as CSV files.

### RQ3:

To perform the comparison with QSharpCheck, you will need to utilise the QSharpCheck framework.
You can find the mutants and test files used for the comparison in the `case_studies/superdense_coding/mutants/translated_circuits` and `case_studies/quantum_teleportation/mutants/translated_circuits` directories.

You will also need to individually execute the relevant property in QuCheck for Quantum Teleportation and Superdense Coding.

This can be done by setting the number of properties to 1 in the `test_and_store_parallel` function in `case_studies/multithreaded_test_runner.py`, and commenting out all but `input_reg0_equal_to_output_reg2_property.py`

-----------------------------------

## Credits and Third-Party Code

This repository is licensed under the MIT License (c) 2024 Gabriel Pontolillo and Marek Grzesiuk.

Portions of this project include code developed by The MITRE Corporation
(2019) from the `qsfe/Qiskit` repository, licensed under the Apache License,
Version 2.0. See the header of each adapted file and
<http://www.apache.org/licenses/LICENSE-2.0> for details.
