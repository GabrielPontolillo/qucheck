from qiskit import QuantumCircuit
from qiskit.quantum_info import Pauli


# returns the quantum_teleportation circuit
def quantum_teleportation():
    qc = QuantumCircuit(3)
    qc.h(1)
    qc.cx(1, 2)
    qc.cx(0, 1)
    qc.h(0)
    # semantic preserving changes loc 5, gates 6, index 2
    qc.s(2)
    qc.s(2)
    qc.z(2)

    qc.cx(1, 2)
    qc.cz(0, 2)
    return qc

