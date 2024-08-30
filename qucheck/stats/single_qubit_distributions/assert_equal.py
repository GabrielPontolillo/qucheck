from typing import Sequence
from uuid import uuid4

import numpy as np
from scipy import stats as sci
from copy import deepcopy

from qucheck.utils import HashableQuantumCircuit
from qucheck.stats.assertion import StatisticalAssertion
from qucheck.stats.measurement_configuration import MeasurementConfiguration
from qucheck.stats.measurements import Measurements
from qucheck.stats.utils.common_measurements import measure_x, measure_y, measure_z

from qucheck.stats.utils.sampling import split_into_subsamples


class AssertEqual(StatisticalAssertion):
    def __init__(self, qubits1: Sequence[int], circuit1: HashableQuantumCircuit, qubits2: Sequence[int],
                 circuit2: HashableQuantumCircuit, basis = ["x", "y", "z"], subsample=False, num_experiments=50) -> None:
    # TODO: add a clause for lists of qubits instead of single registers
        super().__init__()
        self.qubits1 = qubits1
        self.circuit1 = circuit1
        self.qubits2 = qubits2
        self.circuit2 = circuit2
        self.basis = basis
        self.measurement_ids = {basis: uuid4() for basis in basis}
        self.subsample = subsample
        self.num_experiments = num_experiments

    def calculate_p_values(self, measurements: Measurements) -> list[float]:
        p_vals = []
        for qubit1, qubit2 in zip(self.qubits1, self.qubits2):
            
            for basis in self.basis:
                qubit1_counts = measurements.get_counts(self.circuit1, self.measurement_ids[basis])
                qubit2_counts = measurements.get_counts(self.circuit2, self.measurement_ids[basis])

                print(f"subsample: {self.subsample}")
                if not self.subsample:

                    contingency_table = [[0, 0], [0, 0]]
                    for bitstring, count in qubit1_counts.items():
                        if bitstring[len(bitstring) - qubit1 - 1] == "0":
                            contingency_table[0][0] += count
                        else:
                            contingency_table[0][1] += count
                    for bitstring, count in qubit2_counts.items():
                        if bitstring[len(bitstring) - qubit2 - 1] == "0":
                            contingency_table[1][0] += count
                        else:
                            contingency_table[1][1] += count
                    _, p_value = sci.fisher_exact(contingency_table)
                    p_vals.append(p_value)

                else:
                    qubit1_counts_subsamples = split_into_subsamples(deepcopy(qubit1_counts), number_of_subsamples=self.num_experiments)
                    qubit2_counts_subsamples = split_into_subsamples(deepcopy(qubit2_counts), number_of_subsamples=self.num_experiments)

                    # print("subsample 1")
                    # print(qubit1_counts_subsamples)
                    # print("subsample 2")
                    # print(qubit2_counts_subsamples)

                    c1_zero_counts = []
                    c2_zero_counts = []
                    for qubit1_subsample, qubit2_subsample in zip(qubit1_counts_subsamples, qubit2_counts_subsamples):
                        for bitstring, count in qubit1_subsample.items():
                            if bitstring[len(bitstring) - qubit1 - 1] == "0":
                                c1_zero_counts.append(count)
                        for bitstring, count in qubit2_subsample.items():
                            if bitstring[len(bitstring) - qubit2 - 1] == "0":
                                c2_zero_counts.append(count)

                    print("zero counts 1")
                    print(c1_zero_counts)
                    print("zero counts 2")
                    print(c2_zero_counts)

                    _, p_value = sci.ttest_ind(c1_zero_counts, c2_zero_counts)
                    if np.isnan(p_value):
                        p_value = 1
                    # print(p_value)
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
        for qubits, circ in [(self.qubits1, self.circuit1), (self.qubits2, self.circuit2)]:
            if "x" in self.basis:
                measurement_config.add_measurement(self.measurement_ids["x"], circ, {i: measure_x() for i in qubits})
            if "y" in self.basis:
                measurement_config.add_measurement(self.measurement_ids["y"], circ, {i: measure_y() for i in qubits})
            if "z" in self.basis:
                measurement_config.add_measurement(self.measurement_ids["z"], circ, {i: measure_z() for i in qubits})
        return measurement_config
