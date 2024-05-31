from qiskit import QuantumCircuit


class Measurements:
    """class to store results of measurements
    (circuit): {measurement name: list of outputs (dict of bitstr and counts) }
    """
    def __init__(self) -> None:
        self._data: dict[QuantumCircuit, dict[str, list[dict[str, int]]]] = {}
    
    def add_measurement(self, circuit: QuantumCircuit, measurement_id: str, counts: dict[str, int]) -> None:
        if circuit in self._data:
            if measurement_id in self._data[circuit]:
                self._data[circuit][measurement_id].append(counts)
            else:
                self._data[circuit][measurement_id] = [counts]
        else:
            self._data[circuit] = {measurement_id: [counts]}
    
    def get_counts(self, circuit: QuantumCircuit, measurement_id: str) -> list[dict[str, int]]:
        return self._data[circuit][measurement_id]
