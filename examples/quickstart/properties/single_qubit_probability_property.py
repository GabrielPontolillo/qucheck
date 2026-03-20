from qiskit import QuantumCircuit

from qucheck.input_generators import RandomState
from qucheck.property import Property


class SingleQubitProbabilityProperty(Property):
    def get_input_generators(self):
        return [RandomState(1)]

    def preconditions(self, state):
        return True

    def operations(self, state):
        circuit = QuantumCircuit(1, 1)
        circuit.initialize(state, [0])

        probability_of_zero = abs(state[0]) ** 2
        self.statistical_analysis.assert_probability(
            self,
            [0],
            circuit,
            [probability_of_zero],
            basis=["z"],
        )
