from typing import Sequence
from qiskit import QuantumCircuit

from QiskitPBT.utils import HashableQuantumCircuit


class MeasurementConfiguration:
    def __init__(self) -> None:
        self._data: dict[HashableQuantumCircuit, list[tuple[str, Sequence[int], Sequence[QuantumCircuit]]]] = {}
    
    def add_measurement(self, qubits: Sequence[int], circuit: QuantumCircuit, measurement_id: str, measurement_operations: Sequence[QuantumCircuit]) -> None:
        if circuit in self._data:
            self._data[circuit].append((measurement_id, qubits, measurement_operations))
        else:
            self._data[circuit] = [(measurement_id, qubits, measurement_operations)]

    def get_measured_circuits(self) -> tuple[HashableQuantumCircuit]:
        return tuple(self._data.keys())
    
    def get_measurements_for_circuit(self, circuit: QuantumCircuit) -> list[tuple[str, Sequence[int], Sequence[QuantumCircuit]]]:
        return self._data[circuit]