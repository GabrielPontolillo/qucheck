from typing import Sequence
from scipy import stats as sci

from QiskitPBT.utils import HashableQuantumCircuit
from QiskitPBT.stats.assertion import Assertion, StandardAssertion
from QiskitPBT.stats.measurement_configuration import MeasurementConfiguration
from QiskitPBT.stats.measurements import Measurements
from QiskitPBT.stats.utils.common_measurements import measure_x, measure_y, measure_z


class AssertEntangled(StandardAssertion):
    def __init__(self, qubits: Sequence[tuple[int, int]], circuit: HashableQuantumCircuit, basis = ["x", "y", "z"]) -> None:
        super().__init__()
        self.qubits_pairs = qubits
        self.circuit = circuit
        self.basis = basis

    def standard_calculate_outcome(self, measurements: Measurements) -> bool:
        print(measurements)
        for qubit1, qubit2 in self.qubits_pairs:
            for basis in self.basis:
                counts = measurements.get_counts(self.circuit, basis)
                print(counts)
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
