from typing import Sequence
from scipy import stats as sci

from stats.assertion import Assertion
from stats.measurement_configuration import MeasurementConfiguration
from stats.measurements import Measurements
from stats.utils.common_measurements import measure_x, measure_y, measure_z


class AssertEqual(Assertion):
    # TODO: add a clause for lists of qubits instead of single registers
    def __init__(self, qubit1: int | list[int], circuit1_index: int, qubit2: int | list[int], circuit2_index: int,
                 basis=["x", "y", "z"]) -> None:
        super().__init__()
        self.qubit1 = qubit1
        self.circuit1_index = circuit1_index
        self.qubit2 = qubit2
        self.circuit2_index = circuit2_index
        self.basis = basis

    def calculate_p_values(self, measurements: Measurements) -> list[float]:
        # TODO: this breaks if basis has anything other than x,y,z
        p_vals = []
        for basis in self.basis:
            qubit1_counts = measurements.get_counts(self.qubit1, self.circuit1_index, basis)
            qubit2_counts = measurements.get_counts(self.qubit2, self.circuit2_index, basis)
            contingency_table = [[0, 0], [0, 0]]
            for counts1, counts2 in zip(qubit1_counts, qubit2_counts):
                for bitstring, count in counts1.items():
                    if bitstring[len(bitstring) - self.qubit1 - 1] == "0":
                        contingency_table[0][0] += count
                    else:
                        contingency_table[0][1] += count
                for bitstring, count in counts2.items():
                    if bitstring[len(bitstring) - self.qubit2 - 1] == "0":
                        contingency_table[1][0] += count
                    else:
                        contingency_table[1][1] += count
            _, p_value = sci.fisher_exact(contingency_table)
            p_vals.append(p_value)
        return p_vals

    def calculate_outcome(self, p_values: Sequence[float], expected_p_values: Sequence[float]) -> bool:
        for p_value, expected_p_value in zip(p_values, expected_p_values):
            if p_value < expected_p_value:
                return False

        return True

    def get_measurement_configuration(self) -> MeasurementConfiguration:
        measurement_config = MeasurementConfiguration()
        for qubit, circ_index in zip((self.qubit1, self.circuit1_index), (self.qubit2, self.circuit2_index)):
            if "x" in self.basis:
                measurement_config.add_measurement(qubit, circ_index, "x", measure_x())
            if "y" in self.basis:
                measurement_config.add_measurement(qubit, circ_index, "y", measure_y())
            if "z" in self.basis:
                measurement_config.add_measurement(qubit, circ_index, "z", measure_z())
        return measurement_config

    def __eq__(self, other: object) -> bool:
        return isinstance(other, AssertEqual) and self.basis == other.basis and self.qubit1 == other.qubit1 and \
            self.qubit2 == other.qubit2 and self.circuit1_index == other.circuit1_index and self.circuit2_index == other.circuit2_index
