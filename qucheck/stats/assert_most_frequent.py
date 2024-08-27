from typing import Sequence
from uuid import uuid4

from qucheck.utils import HashableQuantumCircuit
from qucheck.stats.assertion import StandardAssertion
from qucheck.stats.measurement_configuration import MeasurementConfiguration
from qucheck.stats.measurements import Measurements
from qucheck.stats.utils.common_measurements import measure_x, measure_y, measure_z


class AssertMostFrequent(StandardAssertion):
    def __init__(self, qubits: Sequence[int], circuit: HashableQuantumCircuit, states: Sequence[str], basis=["z"]) -> None:
        super().__init__()
        self.qubits = qubits
        self.circuit = circuit
        self.states = states
        self.basis = basis
        self.measurement_ids = {basis: uuid4() for basis in basis}

    def calculate_outcome(self, measurements: Measurements) -> bool:
        for basis in self.basis:
            counts = measurements.get_counts(self.circuit, self.measurement_ids[basis])
            # get the key with the largest counts, or frequency in the dictionary
            max_key = max(zip(counts.values(), counts.keys()))[1]

            # get only the qubits from the max string that we are checking
            relevant_bits_in_max_string = ""
            for qubit in self.qubits:
                relevant_bits_in_max_string += max_key[len(max_key) - qubit - 1]

            # check that most frequent state is in the states we are checking for current basis
            if relevant_bits_in_max_string not in self.states:
                return False

        return True

    def get_measurement_configuration(self) -> MeasurementConfiguration:
        measurement_config = MeasurementConfiguration()
        if "x" in self.basis:
            measurement_config.add_measurement(self.measurement_ids["x"], self.circuit, {i: measure_x() for i in self.qubits})
        if "y" in self.basis:
            measurement_config.add_measurement(self.measurement_ids["y"],self.circuit, {i: measure_y() for i in self.qubits})
        if "z" in self.basis:
            measurement_config.add_measurement(self.measurement_ids["z"],self.circuit, {i: measure_z() for i in self.qubits})

        return measurement_config
