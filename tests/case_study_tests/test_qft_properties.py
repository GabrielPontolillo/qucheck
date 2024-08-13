from QiskitPBT.case_studies.quantum_fourier_transform.identity_property import IdentityProperty
from QiskitPBT.case_studies.quantum_fourier_transform.linear_shift_induces_phase_shift_property import LinearShiftToPhaseShift
from QiskitPBT.case_studies.quantum_fourier_transform.phase_shift_induces_linear_shift_property import PhaseShiftToLinearShift
from QiskitPBT.test_runner import TestRunner


import unittest


# test the identity property
class TestIdentityPropertyQFT(unittest.TestCase):
    def setUp(self):
        self.num_inputs = 5

    def test_identity_property_qft(self):
        # run the test
        runner = TestRunner([IdentityProperty], self.num_inputs, 1, 1500)
        runner.run_tests()
        # the property should pass
        assert runner.list_failing_properties() == []
        assert runner.list_passing_properties() == [IdentityProperty]

    def test_phase_shift_property_qft(self):
        # run the test
        runner = TestRunner([LinearShiftToPhaseShift], self.num_inputs, 2, 1500)
        runner.run_tests()
        # the property should pass
        assert runner.list_failing_properties() == []
        assert runner.list_passing_properties() == [LinearShiftToPhaseShift]

    def test_linear_shift_property_qft(self):
        # run the test
        runner = TestRunner([PhaseShiftToLinearShift], self.num_inputs, 5, 1500)
        runner.run_tests()
        # the property should pass
        assert runner.list_failing_properties() == []
        assert runner.list_passing_properties() == [PhaseShiftToLinearShift]
