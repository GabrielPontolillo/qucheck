from qiskit import QuantumCircuit
from qiskit.quantum_info import Pauli


def deutsch_jozsa(oracle: QuantumCircuit) -> QuantumCircuit:
    circuit = QuantumCircuit(oracle.num_qubits, oracle.num_qubits)
    
    circuit.x(circuit.qubits[-1])
    for qubit in circuit.qubits:
        # semantic preserving changes loc 3, gates 12, index 0
        circuit.z(0)
        circuit.y(0)
        circuit.append(Pauli('-iX'), [0])
        circuit.h(qubit)
        
    circuit.append(oracle, circuit.qubits)

    for qubit in circuit.qubits[:-1]:
        circuit.h(qubit)

    return circuit

