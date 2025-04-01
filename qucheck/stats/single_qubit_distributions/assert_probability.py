from typing import Sequence
from uuid import uuid4
from scipy import stats as sci

from qucheck.utils import HashableQuantumCircuit
from qucheck.stats.assertion import StatisticalAssertion
from qucheck.stats.measurement_configuration import MeasurementConfiguration
from qucheck.stats.measurements import Measurements
from qucheck.stats.utils.common_measurements import measure_x, measure_y, measure_z


class AssertProbability(StatisticalAssertion):
    def __init__(self, qubits: Sequence[int], circuit: HashableQuantumCircuit, probabilities: Sequence[float], basis = ["x", "y", "z"]) -> None:
    # TODO: add a clause for lists of qubits instead of single registers
        super().__init__()
        self.qubits = qubits
        self.circuit = circuit
        self.probabilities = probabilities
        self.basis = basis
        self.measurement_ids = {basis: uuid4() for basis in basis}
        assert len(self.qubits) == len(self.probabilities), "The number of qubits and probabilities must be the same"

    def calculate_p_values(self, measurements: Measurements) -> list[float]:
        p_vals = []
        for idx, qubit in enumerate(self.qubits):
            for basis in self.basis:
                qubit1_counts = measurements.get_counts(self.circuit, self.measurement_ids[basis])
                contingency_table = [[0, 0], [0, 0]]
                for bitstring, count in qubit1_counts.items():
                    if bitstring[len(bitstring) - qubit - 1] == "0":
                        contingency_table[0][0] += count
                    else:
                        contingency_table[0][1] += count

                total_number_of_measurements = sum([sum(row) for row in contingency_table])
                expected_number_of_0s = int(round(total_number_of_measurements * self.probabilities[idx]))
                expected_number_of_1s = total_number_of_measurements - expected_number_of_0s

                contingency_table[1][0] = expected_number_of_0s
                contingency_table[1][1] = expected_number_of_1s

                _, p_value = sci.fisher_exact(contingency_table)
                print(contingency_table)
                p_vals.append(p_value)
        return p_vals

    def calculate_outcome(self, p_values: Sequence[float], expected_p_values: Sequence[float]) -> bool:
        for p_value, expected_p_value in zip(p_values, expected_p_values):
            if p_value < expected_p_value:
                return False
        return True

    # receives a quantum circuit, specifies which qubits should be measured and in which basis
    def get_measurement_configuration(self) -> MeasurementConfiguration:
        measurement_config = MeasurementConfiguration()
        if "x" in self.basis:
            measurement_config.add_measurement(self.measurement_ids["x"], self.circuit,
                                               {i: measure_x() for i in self.qubits})
        if "y" in self.basis:
            measurement_config.add_measurement(self.measurement_ids["y"], self.circuit,
                                               {i: measure_y() for i in self.qubits})
        if "z" in self.basis:
            measurement_config.add_measurement(self.measurement_ids["z"], self.circuit,
                                               {i: measure_z() for i in self.qubits})
        return measurement_config
