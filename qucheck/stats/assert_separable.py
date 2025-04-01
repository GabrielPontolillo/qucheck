from typing import Sequence
from uuid import uuid4

from qucheck.utils import HashableQuantumCircuit
from qucheck.stats.assert_entangled import AssertEntangled
from qucheck.stats.measurement_configuration import MeasurementConfiguration
from qucheck.stats.measurements import Measurements
from qucheck.stats.utils.common_measurements import measure_x, measure_y, measure_z


class AssertSeparable(AssertEntangled):
    def calculate_outcome(self, measurements: Measurements) -> bool:
        return not AssertEntangled.calculate_outcome(self, measurements)
