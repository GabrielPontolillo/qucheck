class Measurements:
    """class to store results of measurements
    (qubit, circuit_index): {measurement name: list of outputs (dict of bitstr and counts) }
    """
    def __init__(self) -> None:
        self.data: dict[tuple[int, int], dict[str, list[dict[str, int]]]] = {}
    
    def add_measurement(self, qubit: int, circuit_index: int, measurement_id: str, counts: dict[str, int]) -> None:
        """

        Args:
            qubit (int): qubit which measurement is added
            measurement_id (str): identifier of measurement operation
            counts (dict[str, int]): dictionary of counts from qiskit (full bitstrings)
        """
        key = (qubit, circuit_index)
        if key in self.data:
            if measurement_id in self.data[key]:
                self.data[key][measurement_id].append(counts)
            else:
                self.data[key][measurement_id] = [counts]
        else:
            self.data[key] = {measurement_id: [counts]}
    
    def get_counts(self, qubit: int, circuit_index: int, measurement_id: str) -> list[dict[str, int]]:
        """_summary_

        Args:
            qubit (int): qubit which measurement is added
            measurement_id (str): identifier of measurement operation

        Returns:
            list[dict[str, int]]: list of dictionaries of counts from qiskit
        """
        return self.data[(qubit, circuit_index)][measurement_id]
