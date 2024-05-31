from typing import Sequence
from scipy import stats as sci

from stats.single_qubit_distributions.assert_equal import AssertEqual
from stats.measurement_configuration import MeasurementConfiguration
from stats.measurements import Measurements
from stats.utils.common_measurements import measure_x, measure_y, measure_z


class AssertDifferent(AssertEqual):
    def calculate_outcome(self, p_values: Sequence[float], expected_p_values: Sequence[float]) -> bool:
        for p_value, expected_p_value in zip(p_values, expected_p_values):
            if p_value < expected_p_value:
                return True
        return False
