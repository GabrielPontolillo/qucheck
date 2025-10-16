from qiskit import QuantumCircuit
from qiskit.quantum_info import Pauli


def deutsch_jozsa(oracle: QuantumCircuit) -> QuantumCircuit:
    circuit = QuantumCircuit(oracle.num_qubits, oracle.num_qubits)
    
    circuit.x(circuit.qubits[-1])
    # semantic preserving changes loc 2, gates 10, index 1
    circuit.y(1)
    circuit.z(1)
    circuit.append(Pauli('iX'), [1])
    for qubit in circuit.qubits:
        circuit.h(qubit)
        
    circuit.append(oracle, circuit.qubits)

    for qubit in circuit.qubits[:-1]:
        circuit.h(qubit)

    return circuit

