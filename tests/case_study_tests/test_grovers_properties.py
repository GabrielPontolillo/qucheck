from case_studies.grovers_algorithm.grover_lower_register_minus_property import GroversAlgorithmLowerRegisterMinus
from case_studies.grovers_algorithm.most_frequent_should_be_marked import GroversAlgorithmMostFrequentMarked
from case_studies.grovers_algorithm.most_frequent_output_should_not_be_marked_when_too_many_marks import GroversAlgorithmMostFrequentNotMarkedIfTooManyMarked
from qucheck.test_runner import TestRunner

import unittest


class TestGrovers(unittest.TestCase):
    def test_lower_register_minus(self):
        # run the test
        runner = TestRunner([GroversAlgorithmLowerRegisterMinus], 5, 42, 1500)
        runner.run_tests()
        # the property should pass
        assert runner.list_failing_properties() == []
        assert runner.list_passing_properties() == [GroversAlgorithmLowerRegisterMinus]

    def test_most_frequent_marked(self):
        # run the test
        runner = TestRunner([GroversAlgorithmMostFrequentMarked], 5, 41, 1500)
        runner.run_tests()
        # the property should pass
        assert runner.list_failing_properties() == []
        assert runner.list_passing_properties() == [GroversAlgorithmMostFrequentMarked]

    def test_most_frequent_not_marked_when_too_many_marks(self):
        # run the test
        runner = TestRunner([GroversAlgorithmMostFrequentNotMarkedIfTooManyMarked], 6, 40, 1500)
        runner.run_tests()
        # the property should pass
        assert runner.list_failing_properties() == []
        assert runner.list_passing_properties() == [GroversAlgorithmMostFrequentNotMarkedIfTooManyMarked]
