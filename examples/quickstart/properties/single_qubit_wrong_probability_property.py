from qiskit import QuantumCircuit

from qucheck.input_generators import RandomState
from qucheck.property import Property


class SingleQubitWrongProbabilityProperty(Property):
    def get_input_generators(self):
        return [RandomState(1)]

    def preconditions(self, state):
        probability_of_zero = abs(state[0]) ** 2
        return abs(probability_of_zero - 0.5) >= 0.05

    def operations(self, state):
        circuit = QuantumCircuit(1, 1)
        circuit.initialize(state, [0])

        wrong_probability_of_zero = 1 - abs(state[0]) ** 2
        self.statistical_analysis.assert_probability(
            self,
            [0],
            circuit,
            [wrong_probability_of_zero],
            basis=["z"],
        )
