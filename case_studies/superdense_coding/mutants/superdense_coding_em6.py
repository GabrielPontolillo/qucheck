from qiskit import QuantumCircuit
from qiskit.quantum_info import Pauli


def superdense_coding(b1, b2):
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)

    if b1 == 1:
        qc.z(0)

    if b2 == 1:
        qc.x(0)
        # semantic preserving changes loc 7, gates 6, index 1
        qc.s(1)
        qc.s(1)
        qc.z(1)

    qc.cx(0, 1)
    qc.h(0)
    return qc
