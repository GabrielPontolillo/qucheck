from unittest import TestCase

from QiskitPBT.stats.execution_optimizer import ExecutionOptimizer
from QiskitPBT.stats.measurement_configuration import MeasurementConfiguration
from QiskitPBT.stats.utils.common_measurements import measure_x, measure_y
from QiskitPBT.utils import HashableQuantumCircuit


class TestExecutionOptimizer(TestCase):
    def test_squash_measurements_into_one_circuit(self):
        optimizer = ExecutionOptimizer()
        measurement1 = MeasurementConfiguration()
        measurement1.add_measurement("1", HashableQuantumCircuit(2, 2), {0: measure_x()})
        optimizer.add_measurement_configuration(measurement1)
        measurement2 = MeasurementConfiguration()
        measurement2.add_measurement("2", HashableQuantumCircuit(2, 2), {1: measure_y()})
        optimizer.add_measurement_configuration(measurement2)

        assert len(optimizer.get_circuits_to_execute()) == 1

    
    def test_dont_squash_measurements_into_one_circuit(self):
        optimizer = ExecutionOptimizer()
        measurement1 = MeasurementConfiguration()
        measurement1.add_measurement("1", HashableQuantumCircuit(3, 3), {0: measure_x(), 1: measure_x()})
        optimizer.add_measurement_configuration(measurement1)

        measurement2 = MeasurementConfiguration()
        # TODO: we could also have a look if the overlapping qubits have the same measurement (for aexample if i put 1: measure_x it would be squashable into one circ but atm it wont be)
        measurement2.add_measurement("2", HashableQuantumCircuit(3, 3), {1: measure_y(), 2: measure_y()})
        optimizer.add_measurement_configuration(measurement2)

        assert len(optimizer.get_circuits_to_execute()) == 2
