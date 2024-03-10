# assertion class that stores all relevant information for a single asseriton
from qiskit import QuantumCircuit

from abc import ABC


class AssertionDef(ABC):
    def __init__(self, property_class: str,
                 circuits_and_indexes_to_measure: list[(QuantumCircuit, list[int])], unmodified_input: list[any], input_index: int):

        self.property_class = property_class
        self.circuits_and_indexes_to_measure = circuits_and_indexes_to_measure
        self.unmodified_input = unmodified_input
        self.p_vals = None
        self.expected_p_vals = None
        self.outcome = None
        self.input_index = input_index


    # this method will be implemented by each assertion, returning the p-values
    def calculate_p_values(self, measurements: list[dict[int, dict[str, int]]], unique_circuits: list[QuantumCircuit],
                           union_of_qubits: list[list[int]]):
        pass

    def calculate_outcome(self):
        pass
