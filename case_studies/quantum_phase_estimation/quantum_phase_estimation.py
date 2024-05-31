from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
import math

from QiskitPBT.case_studies.quantum_fourier_transform.quantum_fourier_transform import qft_general


def qpe_general(estimation_qubits, unitary_gate, eigenstate_of_unitary):
    print(estimation_qubits)

    qpe = QuantumCircuit(estimation_qubits+unitary_gate.num_qubits, estimation_qubits+unitary_gate.num_qubits)

    # initialise the unitary register to the specified eigenvector of U
    qpe.initialize(eigenstate_of_unitary, list(range(estimation_qubits, estimation_qubits+unitary_gate.num_qubits)))

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

    qpe = qpe.compose(qft_general(estimation_qubits).inverse(), range(estimation_qubits))

    return qpe
