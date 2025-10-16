from qiskit import QuantumCircuit
from qiskit.quantum_info import Pauli


def deutsch_jozsa(oracle: QuantumCircuit) -> QuantumCircuit:
    circuit = QuantumCircuit(oracle.num_qubits, oracle.num_qubits)
    
    circuit.x(circuit.qubits[-1])
    for qubit in circuit.qubits:
        circuit.h(qubit)

    circuit.append(oracle, circuit.qubits)
    # semantic preserving changes loc 6, gates 7, index 1
    circuit.x(1)
    circuit.y(1)
    circuit.append(Pauli('iZ'), [1])

    for qubit in circuit.qubits[:-1]:
        circuit.h(qubit)

    return circuit

