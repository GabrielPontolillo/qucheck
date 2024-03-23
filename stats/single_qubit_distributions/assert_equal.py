from stats.assertion_def import AssertionDef
from qiskit import QuantumCircuit
from scipy import stats as sci


class AssertEqual(AssertionDef):
    def __init__(self, property_class: str,
                 circuits_and_indexes_to_measure: list[(str | QuantumCircuit, list[int])],
                 unmodified_input: list[any], input_index: int):
        super().__init__(property_class,
                         circuits_and_indexes_to_measure,
                         unmodified_input, input_index)

    # calculate the outcome of the test from the p-values, and expected_p_values attributes, and store it in the outcomes attribute
    def calculate_outcome(self):
        self.outcome = True
        for i, p_val in enumerate(self.p_vals):
            # if any p-value is less than the expected p-value, the outcome is false (Fail)
            if p_val < self.expected_p_vals[i]:
                self.outcome = False

    def calculate_p_values(self, measurements: list[dict[int, dict[str, int]]], unique_circuits: list[QuantumCircuit],
                           union_of_qubits: list[list[int]]):
        measurement_dict1 = None
        measurement_dict2 = None

        # find the measurements using the circuit and qubit indexes in the measurements list
        for index, circuit in enumerate(unique_circuits):
            if circuit == self.unmodified_input[0]:
                measurement_dict1 = measurements[index]
            if circuit == self.unmodified_input[2]:
                measurement_dict2 = measurements[index]

        # reduce the full measurement dict to the qubits we are interested in
        # turn it to a list of dicts of each qubit we are interested in (in order)
        measurement_dict1 = [measurement_dict1[key] for key in self.unmodified_input[1]]
        measurement_dict2 = [measurement_dict2[key] for key in self.unmodified_input[3]]

        assert measurement_dict1 is not None
        assert measurement_dict2 is not None

        basis = None
        if basis is None:
            basis = ['x', 'y', 'z']

        assert len(measurement_dict1) == len(measurement_dict2)

        p_vals = []

        for i, dist_1 in enumerate(measurement_dict1):
            if 'x' in basis:
                contingency_table_x = [[dist_1.get(x, 0), measurement_dict2[i].get(x, 0)] for x in ["x0", "x1"]]
                _, p_value_x = sci.fisher_exact(contingency_table_x)
                p_vals.append(p_value_x)

            if 'y' in basis:
                contingency_table_y = [[dist_1.get(x, 0), measurement_dict2[i].get(x, 0)] for x in ["y0", "y1"]]
                _, p_value_y = sci.fisher_exact(contingency_table_y)
                p_vals.append(p_value_y)

            if 'z' in basis:
                contingency_table_z = [[dist_1.get(x, 0), measurement_dict2[i].get(x, 0)] for x in ["z0", "z1"]]
                _, p_value_z = sci.fisher_exact(contingency_table_z)
                p_vals.append(p_value_z)

        print(p_vals)
        self.p_vals = p_vals
