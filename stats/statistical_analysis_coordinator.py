from time import time
from typing import Sequence
from qiskit import QuantumCircuit, transpile
from qiskit.providers import Backend
from QiskitPBT.property import Property
from QiskitPBT.stats.assert_entangled import AssertEntangled
from QiskitPBT.utils import HashableQuantumCircuit
from QiskitPBT.stats.assertion import StatisticalAssertion, StandardAssertion, Assertion
from QiskitPBT.stats.measurements import Measurements
from QiskitPBT.stats.single_qubit_distributions.assert_equal import AssertEqual
from QiskitPBT.stats.single_qubit_distributions.assert_different import AssertDifferent
from QiskitPBT.stats.assert_most_frequent import AssertMostFrequent
from QiskitPBT.stats.utils.corrections import holm_bonferroni_correction
from QiskitPBT.stats.circuit_generator import CircuitGenerator


class TestExecutionStatistics:
    class FailedProperty:
        def __init__(self, property: Property, failed_classical_assertion: bool, circuits: None | list[QuantumCircuit]):
            self.property: Property = property
            self.failed_classical_assertion: bool = failed_classical_assertion
            self.circuits: None | list[QuantumCircuit] = circuits

    def __init__(self) -> None:
        self.number_circuits_executed = 0
        self.failed_property = []
        
class StatisticalAnalysisCoordinator:
    def __init__(self, number_of_measurements=2000, family_wise_p_value=0.05) -> None:
        self.assertions_for_property: dict[Property, list[Assertion]] = {}
        self.number_of_measurements = number_of_measurements
        self.family_wise_p_value = family_wise_p_value

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

    def assert_entangled(self, property: Property, qubits: Sequence[int], circuit: QuantumCircuit, basis = ["z"]):
        # parse qubits so that assert equals always gets sequences of qubits
        if not isinstance(qubits, Sequence):
            qubits = (qubits,)
        # hack to make circuits in assert equals be usable as dictionary keys (by ref)
        circ = circuit.copy()
        circ.__class__ = HashableQuantumCircuit

        if property in self.assertions_for_property:
            self.assertions_for_property[property].append(AssertEntangled(qubits, circ, basis))
        else:
            self.assertions_for_property[property] = [AssertEntangled(qubits, circ, basis)]

    def assert_most_frequent(self, property: Property, qubits: int | Sequence[int], circuit: QuantumCircuit, states: str | Sequence[str], basis = ["z"]):
        # parse qubits so that assert equals always gets sequences of qubits / bitstrings
        if not isinstance(qubits, Sequence):
            qubits = (qubits,)
        # hack to make circuits in assert equals be usable as dictionary keys (by ref)
        circ = circuit.copy()
        circ.__class__ = HashableQuantumCircuit

        if property in self.assertions_for_property:
            self.assertions_for_property[property].append(AssertMostFrequent(qubits, circ, states, basis))
        else:
            self.assertions_for_property[property] = [AssertMostFrequent(qubits, circ, states, basis)]
    
    # Entrypoint for analysis
    def perform_analysis(self, properties: list[Property], backend: Backend, run_optimization: bool) -> TestExecutionStatistics:
        print(run_optimization)
        circuit_generator = CircuitGenerator(run_optimization)
        test_execution_stats = TestExecutionStatistics()
        # classical assertion failed dont run quantum
        for property in properties:
            if not property.classical_assertion_outcome:
                test_execution_stats.failed_property.append(TestExecutionStatistics.FailedProperty(property, True, None))
                continue

            for assertion in self.assertions_for_property[property]:
                circuit_generator.add_measurement_configuration(assertion.get_measurement_configuration())

        measurements, num_circuits_executed = self._perform_measurements(circuit_generator, backend)
        test_execution_stats.number_circuits_executed = num_circuits_executed
        start_time = time()
        p_values = {}
        for property in properties:
            if property.classical_assertion_outcome and property.classical_assertion_outcome:
                p_values[property] = {}
                for assertion in self.assertions_for_property[property]:
                    if isinstance(assertion, StatisticalAssertion):
                        p_value = assertion.calculate_p_values(measurements)
                        p_values[property][assertion] = p_value
                    elif not isinstance(assertion, Assertion):
                        raise ValueError("Assertion must be a subclass of Assertion")
        
        print("p val calc time", time()-start_time)

        # Only do Holm Bonferroni Correction if there are p_values to correct (preconditions pass)
        if p_values:
            expected_p_values = holm_bonferroni_correction(self.assertions_for_property, p_values, self.family_wise_p_value)

        # calculate the outcome of each assertion
        for property in properties:
            if not property.classical_assertion_outcome:
                continue
            for assertion in self.assertions_for_property[property]:
                if isinstance(assertion, StandardAssertion):
                    assertion_outcome = assertion.calculate_outcome(measurements)
                elif isinstance(assertion, StatisticalAssertion):
                    assertion_outcome = assertion.calculate_outcome(p_values[property][assertion], expected_p_values[property][assertion])
                else:
                    raise ValueError("The provided assertions must be a subclass of Assertion")
                if not assertion_outcome:
                    # this is bad, it relies on assertions having circs as attributes so this really is best guess, but since we are passing all measurements
                    # its quite hard to figure out what exactly failed...
                    failed_circuits = []
                    for _, val in assertion.__dict__.items():
                        if isinstance(val, QuantumCircuit):
                            failed_circuits.append(val)
                    test_execution_stats.failed_property.append(TestExecutionStatistics.FailedProperty(property, False, failed_circuits))
        return test_execution_stats

    # creates a dictionary of measurements for each assertion,
    def _perform_measurements(self, circuit_generator: CircuitGenerator, backend: Backend) -> tuple[dict[StatisticalAssertion, Measurements], int]:
        start_time = time()
        measurements = Measurements()
        print("before get circuits")
        circuits_to_execute = circuit_generator.get_circuits_to_execute()
        print("optim time", time()-start_time)
        if len(circuits_to_execute) == 0:
            return measurements, 0
        # equivalent mutants would get transpiled to the same circuit, so we should run with no optimisation for mutation testing
        start_time = time()
        print("num circuits to transpile", len(circuits_to_execute))
        transpiled_circuits = transpile(circuits_to_execute, backend, optimization_level=1)
        print("transpilation time", time()-start_time)
        start_time = time()
        results = backend.run(transpiled_circuits, shots=self.number_of_measurements).result().get_counts()
        print("circuit execution time", time()-start_time)
        start_time = time()
        if len(circuits_to_execute) == 1:
            results = (results,)
        for counts, circuit in zip(results, circuits_to_execute):
            for measurement_name, original_circuit in circuit_generator.get_measurement_info(circuit):
                measurements.add_measurement(original_circuit, measurement_name, counts)
        print("measurement allocation time", time()-start_time)
        # return measurements and num of circuits executed
        return measurements, len(transpiled_circuits)
