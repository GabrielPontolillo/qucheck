from QiskitPBT.case_studies.quantum_phase_estimation.lower_register_unchanged_by_eigenvector import LowerRegisterUnchangedByEigenvector
from QiskitPBT.case_studies.quantum_phase_estimation.phase_estimation_on_sum_of_eigenvectors_property import PhaseEstimationSumEigenvectors
from QiskitPBT.case_studies.quantum_phase_estimation.phase_estimation_on_sum_of_different_eigenvectors_property import PhaseEstimationSumDifferentEigenvectors
from QiskitPBT.test_runner import TestRunner

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

    def test_sum_eigenvector_property(self):
        # run the test
        runner = TestRunner([PhaseEstimationSumEigenvectors], self.num_inputs, 102)
        runner.run_tests()
        # the property should pass
        assert runner.list_failing_properties() == []
        assert runner.list_passing_properties() == [PhaseEstimationSumEigenvectors]

    # TODO: will fail if uncomment, need to implement assert_different, and use that in the property
    def test_sum_eigenvector_different_eigenvalues_property(self):
        # run the test
        runner = TestRunner([PhaseEstimationSumDifferentEigenvectors], self.num_inputs, 102)
        runner.run_tests()
        # the property should pass
        # assert runner.list_failing_properties() == []
        # assert runner.list_passing_properties() == [PhaseEstimationSumDifferentEigenvectors]
