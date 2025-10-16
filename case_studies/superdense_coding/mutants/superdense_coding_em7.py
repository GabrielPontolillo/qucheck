from qiskit import QuantumCircuit
from qiskit.quantum_info import Pauli


def superdense_coding(b1, b2):
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    # semantic preserving changes loc 3, gates 7, index 1
    qc.x(1)
    qc.y(1)
    qc.append(Pauli('iZ'), [1])

    if b1 == 1:
        qc.z(0)

    if b2 == 1:
        qc.x(0)

    qc.cx(0, 1)
    qc.h(0)
    return qc
