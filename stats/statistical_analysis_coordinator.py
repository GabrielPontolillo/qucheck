from typing import Sequence
from qiskit import QuantumCircuit, transpile
from qiskit.providers.basic_provider import BasicSimulator
from qiskit.providers import Backend
from qiskit.circuit import Operation
from QiskitPBT.stats.measurement_configuration import MeasurementConfiguration
from QiskitPBT.utils import HashableQuantumCircuit
from QiskitPBT.stats.assertion import Assertion
from QiskitPBT.stats.measurements import Measurements
from QiskitPBT.stats.single_qubit_distributions.assert_equal import AssertEqual
from QiskitPBT.stats.single_qubit_distributions.assert_different import AssertDifferent
from QiskitPBT.stats.utils.corrections import holm_bonferroni_correction


class StatisticalAnalysisCoordinator:
#TODO: this should be a single instance fed to all properties?
# esentially the problem is that we are only considering the circuits from this single property when
# adding up the unique circuits in _perfrom_measurements
# there may be multiple properties that run the same circuit
# (now we are passing the same input to all properties that use the same generators)
# to check if its working we should see the execution time be roughly the same for the tests:
# test_run_tests and test_run_costs in test_testRunner
# aside from that, as a general sanity check, you can use all the case study tests to see if they pass, and all tests in test_coordinator

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

    def assert_different(self, qubits1: int | Sequence[int], circuit1: QuantumCircuit, qubits2: int | Sequence[int], circuit2: QuantumCircuit, basis = ["x", "y", "z"]):
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

        self.assertions.append(AssertDifferent(qubits1, circ1, qubits2, circ2, basis))
    
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

        # so we are checking for each unique circuits in the assertions from this statistical analysis coordinator
        # my question is, if we have multiple coordinators (and we will if we have multiple properties),
        # how do we make sure that we are not measuring the same circuit multiple times?
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
            assertion, measurement_names, original_circuit = measured_circuit_to_original_circuit_info[circuit]
            if assertion not in measurements_dict:
                measurements_dict[assertion] = Measurements()
            for measurement_name in measurement_names:
                measurements_dict[assertion].add_measurement(original_circuit, measurement_name, counts)
        
        return measurements_dict
    
        
    def _get_measured_circuits(self, assertion: Assertion) -> dict[HashableQuantumCircuit, tuple[Assertion, list[str], HashableQuantumCircuit]]:
        measured_circuits = {}
        measurement_config = assertion.get_measurement_configuration()
        for circ in measurement_config.get_measured_circuits():
            for measurement_ids, qubits, operations in self._get_optimized_measurements_for_circ(circ, measurement_config):
                measured_circ = circ.copy()
                # this is necessary for append to work
                for qubit, operation in zip(qubits, operations):
                    measured_circ.append(operation.to_instruction(), (qubit,), (qubit,))
                measured_circuits[measured_circ] = (assertion, measurement_ids, circ)      

        return measured_circuits
    
    def _get_optimized_measurements_for_circ(self, circuit: QuantumCircuit, measurement_config: MeasurementConfiguration) -> list[tuple[Sequence[str], Sequence[int], Sequence[QuantumCircuit]]]:
        measurements = measurement_config.get_measurements_for_circuit(circuit)
        optimized_measurements = []
        for i in range(len(measurements)):
            optimized_measurement_ids = [measurements[i][0]]
            optimized_qubits = list(measurements[i][1])
            optimized_operations = list(measurements[i][2])
            for j in range(i, len(measurements)):
                qubits = measurements[j][1]
                
                overlapping = False
                for qubit in optimized_qubits:
                    if qubit in qubits:
                        overlapping = True
                        break

                if overlapping:
                    continue

                optimized_measurement_ids.append(measurements[j][0])
                optimized_qubits.extend(measurements[j][1])
                optimized_operations.extend(measurements[j][2])
            optimized_measurements.append((optimized_measurement_ids, optimized_qubits, optimized_operations))

        return optimized_measurements

    def _extract_circuits(self, circuit_measurement_spec: dict[tuple[int, int], dict[str, QuantumCircuit]]) -> list[QuantumCircuit]:
        circuits = []
        for _, circuits_with_id in circuit_measurement_spec.items():
            for _, circuit in circuits_with_id.items():
                circuits.append(circuit)
        return circuits