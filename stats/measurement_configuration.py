from qiskit import QuantumCircuit


class MeasurementConfiguration:
    """ class to store information about which measurements need to be performed for a assertion
    dict of dict = (qubit to measure, circuit index (in property.operations)): {measurement name: operation}
    """
    def __init__(self) -> None:
        self.data: dict[tuple[int, QuantumCircuit], dict[str, QuantumCircuit]] = {}
    
    def add_measurement(self, qubit_to_measure: int, circuit_index: int, measurement_id: str, measurement_operation: QuantumCircuit) -> None:
        """_summary_
        TODO: finish
        Args:
            qubit_to_measure (int): _description_
            measurement_id (str): _description_  this has to be unique, across all assertions in a property, if these collide the 
                measurement operations will be treated as the same
            measurement_operation (QuantumCircuit): _description_
        """
        key = (qubit_to_measure, circuit_index)
        if key in self.data:
            self.data[key][measurement_id] = measurement_operation
        else:
            self.data[key] = {measurement_id: measurement_operation}

    def get_measured_qubits(self) -> tuple[tuple[int, int]]:
        return tuple(self.data.keys())
    
    def get_measurements_for_qubit(self, qubit: int, circuit_index: int) -> dict[str, QuantumCircuit]:
        return self.data[(qubit, circuit_index)]