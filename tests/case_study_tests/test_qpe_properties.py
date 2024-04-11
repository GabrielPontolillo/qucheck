from case_studies.quantum_phase_estimation.lower_register_unchanged_by_eigenvector import LowerRegisterUnchangedByEigenvector
from case_studies.quantum_fourier_transform.linear_shift_induces_phase_shift_property import LinearShiftToPhaseShift
from case_studies.quantum_fourier_transform.phase_shift_induces_linear_shift_property import PhaseShiftToLinearShift
from test_runner import TestRunner

import unittest


# test the identity property
class TestQPEProperties(unittest.TestCase):
    def setUp(self):
        self.num_inputs = 3

    def test_eigenvector_property(self):
        # run the test
        runner = TestRunner([LowerRegisterUnchangedByEigenvector], self.num_inputs, 101)
        runner.run_tests()
        # the property should pass
        assert runner.list_failing_properties() == []
        assert runner.list_passing_properties() == [LowerRegisterUnchangedByEigenvector]
