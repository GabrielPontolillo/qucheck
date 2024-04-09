from qiskit import QuantumCircuit, transpile
from qiskit.providers.basic_provider import BasicSimulator
from qiskit.providers import Backend

from stats.assertion import Assertion
from stats.measurement_configuration import MeasurementConfiguration
from stats.measurements import Measurements
from stats.single_qubit_distributions.assert_equal import AssertEqual
from stats.utils.corrections import holm_bonferroni_correction


class StatisticalAnalysisCoordinator:
    def __init__(self, property, number_of_measurements=2000, family_wise_p_value=0.05) -> None:
        self.assertions: list[Assertion] = []
        self.results: list[bool] = []
        self.property = property
        self.number_of_measurements = number_of_measurements
        self.family_wise_p_value = family_wise_p_value
    
    #Assertions
    def assert_equal(self, qubit1: int, circuit1_index: int, qubit2: int, circuit2_index: int, basis = ["x", "y", "z"]):
        assertion = AssertEqual(qubit1, circuit1_index, qubit2, circuit2_index, basis)
        if assertion not in self.assertions:
            self.assertions.append(assertion)
    
    #Analysis
    def perform_analysis(self, seeds: set[int], backend: Backend=BasicSimulator()) -> None:
        # classical assertion failed dont run quantum
        if not self.property.classical_assertion_outcome:
            for _ in self.assertions:
                self.results.append(False)
            return

        measurements = self._perform_measurements(seeds, backend)
        p_values_per_assertion = [assertion.calculate_p_values(measurements) for assertion in self.assertions]

        # perform family wise error rate correction
        # Ideally, we need to sort all of the p-values from all assertions, then pass back the corrected alpha values to compare them to in a list
        expected_p_values_per_assertion = holm_bonferroni_correction(self.assertions, p_values_per_assertion, self.family_wise_p_value)

        # calculate the outcome of each assertion
        for assertion, p_values, expected_p_vals in zip(self.assertions, p_values_per_assertion, expected_p_values_per_assertion):
            self.results.append(assertion.calculate_outcome(p_values, expected_p_vals))
    
    def _perform_measurements(self, seeds: set[int], backend: Backend) -> Measurements:
        unique_circuits: list[QuantumCircuit] = []
        circuits_to_measurement_specifiers: dict[str, dict[tuple[int, int], str]] = {}
        circuit_names_to_circuits: dict[str, QuantumCircuit] = {}
        generators = self.property.get_input_generators()
        for assertion in self.assertions:
            for seed in seeds:
                inputs = [generator.generate(seed) for generator in generators]
                circuits = self.property.operations(*inputs)
                measured_circuit_spec = self._get_measured_circuits(assertion.get_measurement_configuration(), circuits)
                new_circuits = self._extract_circuits(measured_circuit_spec) # only add if they arent already there
                unique_circuits.extend(new_circuits)
                for circuit in new_circuits:
                    circuit_names_to_circuits[circuit.name] = circuit
                circuits_to_measurement_specifiers = self._update_circuits_to_measurement_specifiers(circuits_to_measurement_specifiers, measured_circuit_spec)
        
        measurements = Measurements()
        for circuit in unique_circuits:
            #TODO: get counts actually returns (or used to) unparsed bit strings, so if there are 2 quantum registers there is a space in there - this may need some attention
            measurement_spec = circuits_to_measurement_specifiers[circuit.name]
            counts = backend.run(transpile(circuit, backend), shots=self.number_of_measurements).result().get_counts()
            for qubit_circuit_index, measurement_id in measurement_spec.items():
                qubit, circuit_index = qubit_circuit_index
                measurements.add_measurement(qubit, circuit_index, measurement_id, counts)
        
        return measurements
        
    def _get_measured_circuits(self, measurement_config: MeasurementConfiguration, circuits: tuple[QuantumCircuit]) -> dict[tuple[int, int], dict[str, QuantumCircuit]]:
        measured_circuits = {}
        for qubit, circuit_index in measurement_config.get_measured_qubits():
            key = (qubit, circuit_index)
            measured_circuits[key] = {}
            for measurement_id, operation in measurement_config.get_measurements_for_qubit(qubit, circuit_index).items():
                measured_circ = circuits[circuit_index].copy()
                if qubit > len(measured_circ.qubits):
                    raise ValueError(f"tried measuring qubit {qubit} which does not exist in the circuit")
                if qubit > len(measured_circ.clbits):
                    raise ValueError(f"to measure qubit {qubit}, the circuit must also contain a classical bit {qubit}")
                measured_circ.append(operation.to_instruction(), (qubit,), (qubit,))
                measured_circ.name += measurement_id
                measured_circuits[key][measurement_id] = measured_circ
        return measured_circuits
    
    def _update_circuits_to_measurement_specifiers(
            self, circuits_to_measurement_specifiers: dict[str, dict[tuple[int, int], str]], 
            measured_circuits: dict[tuple[int, int], dict[str, QuantumCircuit]]) -> dict[str, dict[tuple[int, int], str]]:
        # TODO: indexing circuits by name isnt ideal as that does not have to be unique - have to uuid it
        for qubit_and_index, circuits_with_id in measured_circuits.items():
            for id, qc in circuits_with_id.items():
                if qc.name in circuits_to_measurement_specifiers:
                    circuits_to_measurement_specifiers[qc.name][qubit_and_index] = id
                else:
                    circuits_to_measurement_specifiers[qc.name] = {qubit_and_index: id}
        return circuits_to_measurement_specifiers
    
    def _extract_circuits(self, circuit_measurement_spec: dict[tuple[int, int], dict[str, QuantumCircuit]]) -> list[QuantumCircuit]:
        circuits = []
        for _, circuits_with_id in circuit_measurement_spec.items():
            for _, circuit in circuits_with_id.items():
                circuits.append(circuit)
        return circuits