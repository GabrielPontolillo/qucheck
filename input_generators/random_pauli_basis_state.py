# class for generating random statevectors using Qiskit, the generator method receives the dimensions of the statevector
from input_generators.input_generator import InputGenerator
from qiskit.quantum_info import Statevector
import random


class RandomPauliBasisState(InputGenerator):
    def __init__(self, number_of_qubits):
        self.number_of_qubits = number_of_qubits

    def generate(self, seed):
        # generate a random statevector from the tensor product of the |+>,|->,|0>,|1>,|i>,|-i>,
        # loop through the number of qubits, choose one of the 6 statevectors
        state_string = ""
        random.seed(seed)
        for _ in range(self.number_of_qubits):
            state_string += random.choice(["+", "-", "0", "1", "r", "l"])


        # convert the string to a statevector
        return Statevector.from_label(state_string).data
