from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
import math

from case_studies.quantum_fourier_transform.quantum_fourier_transform import qft_general


def qpe_general(estimation_qubits, unitary_gate, eigenstate_of_unitary):
    # We could just send numbers specifying the size of each register,
    # but this allows us to specify the name of each register, making the output circuit easier to follow
    estimation_qubit_register = QuantumRegister(estimation_qubits, "Estimation")
    unitary_qubit_register = QuantumRegister(unitary_gate.num_qubits, "Unitary")
    estimation_bit_register = ClassicalRegister(estimation_qubits)

    qpe = QuantumCircuit(estimation_qubit_register, unitary_qubit_register, estimation_bit_register)

    # initialise the unitary register to the specified eigenvector of U
    qpe.initialize(eigenstate_of_unitary, unitary_qubit_register)

    # apply hadamard to all qubits in estimating register
    for i in range(estimation_qubits):
        qpe.h(i)

    unitary_qubits = [i + estimation_qubits for i in range(unitary_gate.num_qubits)]

    # do controlled unitary operations
    for i in range(estimation_qubits):
        for j in range(2 ** i):
            qubits = [estimation_qubits - 1 - i]
            qubits.extend(unitary_qubits)
            qpe = qpe.compose(unitary_gate.control(), qubits)

    qpe = qpe.compose(qft_general(estimation_qubits).inverse(), estimation_qubit_register)

    return qpe
