# class that tests the statistical analysis class
import unittest

from QiskitPBT.stats.statistical_analysis_coordinator import StatisticalAnalysisCoordinator
from qiskit import QuantumCircuit
from case_studies.quantum_teleportation.input_reg0_equal_to_output_reg2 import Inq0EqualOutq2


# used for hashing the input function
# def input_function():
#     return [0]


# class TestStatisticalAnalysisCoordinator(unittest.TestCase):
    # make sure to reset statistical analysis class variables
    # def tearDown(self):

    # def test_assert_equal(self):
