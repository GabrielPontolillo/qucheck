# class that inherits from property based test
from qiskit import QuantumCircuit
from qucheck.property import Property
from qucheck.input_generators import Integer, RandomState

import random


class ProbabilityProperty(Property):
    # specify the inputs that are to be generated
    def get_input_generators(self):
        # The assumption of our code is that we need at least one input generator, if we do not include it,
        # the code breaks in the test runner - also its a fine assumption to include, property based testing requires inputs
        return [RandomState(1)]

    # specify the preconditions for the test
    def preconditions(self, state):
        return True

    # specify the operations to be performed on the input
    def operations(self, state):
        qc = QuantumCircuit(1, 1)
        qc.initialize(state, [0])

        prob = abs(state[0])**2

        print(prob)

        self.statistical_analysis.assert_probability(self, [0], qc, [prob], basis=["z"])


class WrongProbabilityProperty(Property):
    # specify the inputs that are to be generated
    def get_input_generators(self):
        # The assumption of our code is that we need at least one input generator, if we do not include it,
        # the code breaks in the test runner - also its a fine assumption to include, property based testing requires inputs
        return [RandomState(1)]

    # specify the preconditions for the test
    def preconditions(self, state):
        return True

    # specify the operations to be performed on the input
    def operations(self, state):
        qc = QuantumCircuit(1, 1)
        qc.initialize(state, [0])

        prob = 1 - abs(state[0])**2

        print(prob)

        self.statistical_analysis.assert_probability(self, [0], qc, [prob], basis=["z"])


class ProbabilityPropertyMultipleQubits(Property):
    # specify the inputs that are to be generated
    def get_input_generators(self):
        # The assumption of our code is that we need at least one input generator, if we do not include it,
        # the code breaks in the test runner - also its a fine assumption to include, property based testing requires inputs
        return [RandomState(1), RandomState(1)]

    # specify the preconditions for the test
    def preconditions(self, state1, state2):
        return True

    # specify the operations to be performed on the input
    def operations(self, state1, state2):
        qc = QuantumCircuit(1, 1)
        qc.initialize(state1, [0])

        qc2 = QuantumCircuit(1, 1)
        qc2.initialize(state2, [0])

        qc3 = QuantumCircuit(2, 2)
        qc3.compose(qc, [0], inplace=True)
        qc3.compose(qc2, [1], inplace=True)

        prob1 = abs(state1[0])**2
        prob2 = abs(state2[0])**2

        print(prob1)
        print(prob2)

        self.statistical_analysis.assert_probability(self, [0, 1], qc3, [prob1, prob2], basis=["z"])