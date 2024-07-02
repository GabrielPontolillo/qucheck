from typing import Sequence
from scipy import stats as sci

from QiskitPBT.utils import HashableQuantumCircuit
from QiskitPBT.stats.assertion import Assertion
from QiskitPBT.stats.measurement_configuration import MeasurementConfiguration
from QiskitPBT.stats.measurements import Measurements
from QiskitPBT.stats.utils.common_measurements import measure_x, measure_y, measure_z


class AssertEntangled(Assertion):
    def __init__(self, qubits: Sequence[tuple[int, int]], circuit: HashableQuantumCircuit, basis = ["x", "y", "z"]) -> None:
        super().__init__()
        self.qubits_pairs = qubits
        self.circuit = circuit
        self.basis = basis

    def calculate_p_values(self, measurements: Measurements) -> list[float]:
        p_vals = []
        for qubit1, qubit2 in self.qubits_pairs:
            for basis in self.basis:
                counts = measurements.get_counts(self.circuit, basis)
                contingency_table = [[0, 0], [0, 0]]
                for count in counts:
                    for bitstring, frequency in count.items():
                        if bitstring[len(bitstring) - qubit1 - 1] == "0":
                            contingency_table[0][0] += frequency
                        else:
                            contingency_table[0][1] += frequency
                    for bitstring, frequency in count.items():
                        if bitstring[len(bitstring) - qubit2 - 1] == "0":
                            contingency_table[1][0] += frequency
                        else:
                            contingency_table[1][1] += frequency
                _, p_value = sci.fisher_exact(contingency_table)
                # TODO: this is kind of weird in the sense that we dont seperate p values of different qubits and just dump everything together
                p_vals.append(p_value)
        return p_vals

    def calculate_outcome(self, p_values: Sequence[float], expected_p_values: Sequence[float]) -> bool:
        for p_value, expected_p_value in zip(p_values, expected_p_values):
            if p_value < expected_p_value:
                return False
        return True

    def get_measurement_configuration(self) -> MeasurementConfiguration:
        measurement_config = MeasurementConfiguration()
        for qubit_pair in self.qubits_pairs:
            if "x" in self.basis:
                measurement_config.add_measurement(qubit_pair, self.circuit, "x", [measure_x() for _ in qubit_pair])
            if "y" in self.basis:
                measurement_config.add_measurement(qubit_pair, self.circuit, "y", [measure_y() for _ in qubit_pair])
            if "z" in self.basis:
                measurement_config.add_measurement(qubit_pair, self.circuit, "z", [measure_z() for _ in qubit_pair])
        return measurement_config
