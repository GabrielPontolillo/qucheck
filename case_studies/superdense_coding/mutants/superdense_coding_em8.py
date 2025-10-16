from qiskit import QuantumCircuit
from qiskit.quantum_info import Pauli


def superdense_coding(b1, b2):
    qc = QuantumCircuit(2)
    # semantic preserving changes loc 1, gates 11, index 0
    qc.z(0)
    qc.x(0)
    qc.append(Pauli('iY'), [0])

    qc.h(0)
    qc.cx(0, 1)

    if b1 == 1:
        qc.z(0)

    if b2 == 1:
        qc.x(0)

    qc.cx(0, 1)
    qc.h(0)
    return qc
