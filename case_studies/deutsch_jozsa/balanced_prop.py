import random
from qiskit import QuantumCircuit
from QiskitPBT.case_studies.deutsch_jozsa.deutsch_jozsa import deutsch_jozsa_circ
from QiskitPBT.input_generators.input_generator import InputGenerator
from QiskitPBT.property import Property

class DeutschJozsaWorksForBalancedFunction(Property):
    # specify the inputs that are to be generated
    def get_input_generators(self):
        return [BalancedOracleInputGenerator(5, 10)]

    # specify the preconditions for the test
    def preconditions(self, oracle):
        return True

    # specify the operations to be performed on the input
    def operations(self, oracle: QuantumCircuit):
        circ = deutsch_jozsa_circ(oracle)

        # if oracle is constant this should be all 0
        baseline = QuantumCircuit(oracle.num_qubits - 1, oracle.num_qubits - 1)

        self.statistical_analysis.assert_different(list(range(oracle.num_qubits - 1)), circ, list(range(oracle.num_qubits - 1)), baseline)

class BalancedOracleInputGenerator(InputGenerator):
    def __init__(self, low, high):
        self.low = low
        self.high = high

    def generate(self, seed):
        random.seed(seed)
        num_qubits = random.randint(self.low, self.high)
        circuit = QuantumCircuit(num_qubits)
        
        i = 0
        for qubit in circuit.qubits[:-1]:
            if i % 2 == 0:
                circuit.x(qubit)
            i += 1
            circuit.cx(qubit, circuit.qubits[-1])

        return circuit
