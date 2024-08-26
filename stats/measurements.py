from QiskitPBT.utils import HashableQuantumCircuit


class Measurements:
    """class to store results of measurements
    (circuit): {measurement name: dict of bitstr and counts }
    """
    def __init__(self) -> None:
        self._data: dict[HashableQuantumCircuit, dict[str, dict[str, int]]] = {}
    
    def add_measurement(self, circuit: HashableQuantumCircuit, measurement_id: str, counts: dict[str, int]) -> None:
        if circuit in self._data:
            self._data[circuit][measurement_id] = counts
        else:
            self._data[circuit] = {measurement_id: counts}
    
    def get_counts(self, circuit: HashableQuantumCircuit, measurement_id: str) -> dict[str, int]:
        return self._data[circuit][measurement_id]
