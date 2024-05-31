from typing import Sequence
from qiskit import QuantumCircuit, transpile
from qiskit.providers.basic_provider import BasicSimulator
from qiskit.providers import Backend
from qiskit.circuit import Operation
from QiskitPBT.utils import HashableQuantumCircuit
from QiskitPBT.stats.assertion import Assertion
from QiskitPBT.stats.measurements import Measurements
from QiskitPBT.stats.single_qubit_distributions.assert_equal import AssertEqual
from QiskitPBT.stats.utils.corrections import holm_bonferroni_correction


class StatisticalAnalysisCoordinator:
    def __init__(self, property, number_of_measurements=2000, family_wise_p_value=0.05) -> None:
        self.assertions: list[Assertion] = []
        self.results: list[bool] = []
        self.property = property
        self.number_of_measurements = number_of_measurements
        self.family_wise_p_value = family_wise_p_value
    
    #Assertions
    def assert_equal(self, qubits1: int | Sequence[int], circuit1: QuantumCircuit, qubits2: int | Sequence[int], circuit2: QuantumCircuit, basis = ["x", "y", "z"]):
        # parse qubits so that assert equals always gets sequences of qubits
        if not isinstance(qubits1, Sequence):
            qubits1 = (qubits1, )
        if not isinstance(qubits2, Sequence):
            qubits2 = (qubits2, )
        # hack to make circuits in assert equals be usable as dictionary keys (by ref)
        circ1 = circuit1.copy()
        circ1.__class__ = HashableQuantumCircuit
        circ2 = circuit2.copy()
        circ2.__class__ = HashableQuantumCircuit

        self.assertions.append(AssertEqual(qubits1, circ1, qubits2, circ2, basis))
    
    #Analysis
    def perform_analysis(self, backend: Backend=BasicSimulator()) -> None:
        # classical assertion failed dont run quantum
        if not self.property.classical_assertion_outcome:
            self.results.append(False)
            return
        
        measurements = self._perform_measurements(backend)
        p_values_per_assertion = [assertion.calculate_p_values(measurements[assertion]) for assertion in self.assertions]

        # perform family wise error rate correction
        # Ideally, we need to sort all of the p-values from all assertions, then pass back the corrected alpha values to compare them to in a list
        expected_p_values_per_assertion = holm_bonferroni_correction(self.assertions, p_values_per_assertion, self.family_wise_p_value)

        # calculate the outcome of each assertion
        for assertion, p_values, expected_p_vals in zip(self.assertions, p_values_per_assertion, expected_p_values_per_assertion):
            self.results.append(assertion.calculate_outcome(p_values, expected_p_vals))
    
    def _perform_measurements(self, backend: Backend) -> dict[Assertion, Measurements]:
        unique_circuits: list[HashableQuantumCircuit] = []
        measured_circuit_to_original_circuit_info: dict[HashableQuantumCircuit, tuple[Assertion, str, HashableQuantumCircuit]] = {}

        for assertion in self.assertions:
            measured_circuits = self._get_measured_circuits(assertion)
            for measured_circ in measured_circuits:
                if measured_circ not in unique_circuits:
                    unique_circuits.append(measured_circ)
            measured_circuit_to_original_circuit_info.update(measured_circuits)
            
        
        measurements_dict: dict[Assertion, Measurements] = {}
        for circuit in unique_circuits:
            #TODO: get counts actually returns (or used to) unparsed bit strings, so if there are 2 quantum registers there is a space in there - this may need some attention
            # this is necessary for measure to work
            circuit.__class__ = QuantumCircuit
            counts = backend.run(transpile(circuit, backend), shots=self.number_of_measurements).result().get_counts()
            # cast back so we can use it as a key
            circuit.__class__ = HashableQuantumCircuit
            assertion, measurement_name, original_circuit = measured_circuit_to_original_circuit_info[circuit]
            if assertion not in measurements_dict:
                measurements_dict[assertion] = Measurements()
            measurements_dict[assertion].add_measurement(original_circuit, measurement_name, counts)
        
        return measurements_dict
    
        
    def _get_measured_circuits(self, assertion: Assertion) -> dict[HashableQuantumCircuit, tuple[Assertion, str, HashableQuantumCircuit]]:
        measured_circuits = {}
        measurement_config = assertion.get_measurement_configuration()
        for circ in measurement_config.get_measured_circuits():
            for measurement_id, qubits, operations in measurement_config.get_measurements_for_circuit(circ):
                # TODO: we should do actual optimialization here
                measured_circ = circ.copy()
                # this is necessary for append to work
                for qubit, operation in zip(qubits, operations):
                    measured_circ.append(operation.to_instruction(), (qubit,), (qubit,))
                measured_circuits[measured_circ] = (assertion, measurement_id, circ)      

        return measured_circuits
        
    def _extract_circuits(self, circuit_measurement_spec: dict[tuple[int, int], dict[str, QuantumCircuit]]) -> list[QuantumCircuit]:
        circuits = []
        for _, circuits_with_id in circuit_measurement_spec.items():
            for _, circuit in circuits_with_id.items():
                circuits.append(circuit)
        return circuits