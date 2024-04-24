# class that inherits from property based test
import numpy as np
from qiskit import QuantumCircuit
from QiskitPBT.property import Property
from QiskitPBT.input_generators.random_fourier_transform_state import RandomFourierTransformState
from QiskitPBT.case_studies.quantum_fourier_transform.quantum_fourier_transform import qft_general
from qiskit.quantum_info import Statevector


class PhaseShiftToLinearShift(Property):
    # specify the inputs that are to be generated
    def get_input_generators(self):
        state = RandomFourierTransformState(1, 5)
        return [state]

    # specify the preconditions for the test
    def preconditions(self, state):
        return True

    # specify the operations to be performed on the input
    def operations(self, state):
        n = state.num_qubits

        qft_1 = QuantumCircuit(n, n)
        qft_1.initialize(state, range(n))
        qft_1 = qft_1.compose(qft_general(n, swap=True).inverse(), reversed(range(n)))
        qft_1 = linear_shift(qft_1)
        #print("--------------------")
        #print(np.around(Statevector(qft_1).data, 2))

        qft_2 = QuantumCircuit(n, n)
        qft_2.initialize(state, range(n))
        qft_2 = phase_shift(qft_2)
        qft_2 = qft_2.compose(qft_general(n, swap=True).inverse(), reversed(range(n)))
        #print(np.around(Statevector(qft_2).data, 2))
        #print("--------------------")

        self.statistical_analysis.assert_equal(list(range(n)), qft_1, list(range(n)), qft_2)

def phase_shift(qc):
    # we instead apply a positive phase shift to the qubits as the linear shift adds 1 (down shift instead of up)
    for i in range(qc.num_qubits):
        qc.p(np.pi / 2 ** (qc.num_qubits - 1 - i), i)
    return qc


# Apply a series of controlled gates to perform the addition of 1
def linear_shift(qc):
    # this
    n = qc.num_qubits
    for i in reversed(range(1, n)):
        qubit_list = [j for j in range(i)]
        qc.mcx(qubit_list, i)
    qc.x(0)

    return qc