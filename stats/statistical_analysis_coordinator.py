from typing import Sequence
from qiskit import QuantumCircuit, transpile
from qiskit.providers.basic_provider import BasicSimulator
from qiskit.providers import Backend
from qiskit.circuit import Operation
from QiskitPBT.property import Property
from QiskitPBT.stats.assert_entangled import AssertEntangled
from QiskitPBT.stats.measurement_configuration import MeasurementConfiguration
from QiskitPBT.utils import HashableQuantumCircuit
from QiskitPBT.stats.assertion import Assertion
from QiskitPBT.stats.measurements import Measurements
from QiskitPBT.stats.single_qubit_distributions.assert_equal import AssertEqual
from QiskitPBT.stats.single_qubit_distributions.assert_different import AssertDifferent
from QiskitPBT.stats.utils.corrections import holm_bonferroni_correction


class StatisticalAnalysisCoordinator:
    # TODO: this should be a single instance fed to all properties?
    # esentially the problem is that we are only considering the circuits from this single property when
    # adding up the unique circuits in _perfrom_measurements
    # there may be multiple properties that run the same circuit
    # (now we are passing the same input to all properties that use the same generators)
    # to check if its working we should see the execution time be roughly the same for the tests:
    # test_run_tests and test_run_costs in test_testRunner
    # aside from that, as a general sanity check, you can use all the case study tests to see if they pass, and all tests in test_coordinator

    def __init__(self, number_of_measurements=2000, family_wise_p_value=0.05) -> None:
        self.assertions_for_property: dict[Property, list[Assertion]] = {}
        self.results: dict[Property, bool] = {}
        self.number_of_measurements = number_of_measurements
        self.family_wise_p_value = family_wise_p_value
        self.circuits_executed = 0 # for statistics
        self.unique_circuits: list[HashableQuantumCircuit] = []
        self.measured_circuit_to_original_circuit_info: dict[HashableQuantumCircuit, tuple[Assertion, str, HashableQuantumCircuit]] = {}

    #Assertions
    def assert_equal(self, property: Property, qubits1: int | Sequence[int], circuit1: QuantumCircuit, qubits2: int | Sequence[int], circuit2: QuantumCircuit, basis = ["x", "y", "z"]):
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
        if property in self.assertions_for_property:
            self.assertions_for_property[property].append(AssertEqual(qubits1, circ1, qubits2, circ2, basis))
        else:
            self.assertions_for_property[property] = [AssertEqual(qubits1, circ1, qubits2, circ2, basis)]

    def assert_different(self, property: Property, qubits1: int | Sequence[int], circuit1: QuantumCircuit, qubits2: int | Sequence[int], circuit2: QuantumCircuit, basis = ["x", "y", "z"]):
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

        if property in self.assertions_for_property:
            self.assertions_for_property[property].append(AssertDifferent(qubits1, circ1, qubits2, circ2, basis))
        else:
            self.assertions_for_property[property] = [AssertDifferent(qubits1, circ1, qubits2, circ2, basis)]

    def assert_entangled(self, property: Property, qubits_pairs: tuple[int, int] | Sequence[tuple[int, int]], circuit: QuantumCircuit, basis = ["x", "y", "z"]):
        # parse qubits so that assert equals always gets sequences of qubits
        if not isinstance(qubits_pairs[0], Sequence):
            qubits_pairs = (qubits_pairs, )
        # hack to make circuits in assert equals be usable as dictionary keys (by ref)
        circ = circuit.copy()
        circ.__class__ = HashableQuantumCircuit

        if property in self.assertions_for_property:
            self.assertions_for_property[property].append(AssertEntangled(qubits_pairs, circ,basis))
        else:
            self.assertions_for_property[property] = [AssertEntangled(qubits_pairs, circ,basis)]
    
    # Entrypoint for analysis
    def perform_analysis(self, properties: list[Property], backend: Backend=BasicSimulator()) -> None:
        # classical assertion failed dont run quantum
        for property in properties:
            if not property.classical_assertion_outcome:
                self.results[property] = False
                continue

            self._generate_circuits(property)

        measurements = self._perform_measurements(backend)

        # the dictionary comprehension was confusing me so I expanded it
        p_values = {}
        for property in properties:
            # p_values[property] = {assertion: assertion.calculate_p_values(measurements[assertion]) for assertion in self.assertions_for_property[property]}

            p_values[property] = {}
            for assertion in self.assertions_for_property[property]:
                p_value = assertion.calculate_p_values(measurements[assertion])
                p_values[property][assertion] = p_value

        # perform family wise error rate correction
        # Ideally, we need to sort all of the p-values from all assertions, then pass back the corrected alpha values to compare them to in a list
        expected_p_values = holm_bonferroni_correction(self.assertions_for_property, p_values, self.family_wise_p_value)

        # calculate the outcome of each assertion
        for property in properties:
            if property not in self.results:
                self.results[property] = True
            for assertion in self.assertions_for_property[property]:
                self.results[property] = (self.results[property] and assertion.calculate_outcome(p_values[property][assertion], expected_p_values[property][assertion]))

    def _perform_measurements(self, backend: Backend) -> dict[Assertion, Measurements]:
        measurements_dict: dict[Assertion, Measurements] = {}
        for circuit in self.unique_circuits:
            # TODO: get counts actually returns (or used to) unparsed bit strings, so if there are 2 quantum registers there is a space in there - this may need some attention
            # this is necessary for measure to work
            circuit.__class__ = QuantumCircuit
            counts = backend.run(transpile(circuit, backend), shots=self.number_of_measurements).result().get_counts()
            self.circuits_executed += 1
            # cast back so we can use it as a key
            circuit.__class__ = HashableQuantumCircuit
            assertion, measurement_names, original_circuit = self.measured_circuit_to_original_circuit_info[circuit]
            if assertion not in measurements_dict:
                measurements_dict[assertion] = Measurements()
            for measurement_name in measurement_names:
                measurements_dict[assertion].add_measurement(original_circuit, measurement_name, counts)
        
        return measurements_dict

    # iterates through the assertions within a property, appends measurements to the circuit
    def _generate_circuits(self, property):
        for assertion in self.assertions_for_property[property]:
            measured_circuits = self._get_measured_circuits(assertion)
            for measured_circ in measured_circuits:
                if measured_circ not in self.unique_circuits:
                    self.unique_circuits.append(measured_circ)
            self.measured_circuit_to_original_circuit_info.update(measured_circuits)

    def _get_measured_circuits(self, assertion: Assertion) -> dict[HashableQuantumCircuit, tuple[Assertion, list[str], HashableQuantumCircuit]]:
        measured_circuits = {}
        measurement_config = assertion.get_measurement_configuration()
        for circ in measurement_config.get_measured_circuits():
            for measurement_ids, qubits, operations in self._get_optimized_measurements_for_circ(circ, measurement_config):
                measured_circ = circ.copy()
                for qubit, operation in zip(qubits, operations):
                    # TODO: uncommnet line before to make it work
                    # measured_circ.compose(operation, (qubit,), (qubit,), inplace=True)
                    measured_circ.append(operation.to_instruction(), (qubit,), (qubit,))
                measured_circuits[measured_circ] = (assertion, measurement_ids, circ)

        return measured_circuits

    # does this check for overlapping qubits in different assertions?
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

    # this code is not used anywhere
    # def _extract_circuits(self, circuit_measurement_spec: dict[tuple[int, int], dict[str, QuantumCircuit]]) -> list[QuantumCircuit]:
    #     circuits = []
    #     for _, circuits_with_id in circuit_measurement_spec.items():
    #         for _, circuit in circuits_with_id.items():
    #             circuits.append(circuit)
    #     return circuits