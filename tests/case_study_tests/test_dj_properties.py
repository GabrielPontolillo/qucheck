from QiskitPBT.case_studies.deutsch_jozsa.balanced_prop import DeutschJozsaWorksForBalancedFunction
from QiskitPBT.case_studies.deutsch_jozsa.constant_prop import DeutschJozsaWorksForConstantFunction
from QiskitPBT.test_runner import TestRunner

import unittest


class TestDeutschJozsa(unittest.TestCase):
    def test_balanced_properties(self):
        # run the test
        runner = TestRunner([DeutschJozsaWorksForBalancedFunction], 5, 1)
        runner.run_tests()
        # the property should pass
        assert runner.list_failing_properties() == []
        assert runner.list_passing_properties() == [DeutschJozsaWorksForBalancedFunction]

    def test_constant_properties(self):
        # run the test
        runner = TestRunner([DeutschJozsaWorksForConstantFunction], 5, 1)
        runner.run_tests()
        # the property should pass
        assert runner.list_failing_properties() == []
        assert runner.list_passing_properties() == [DeutschJozsaWorksForConstantFunction]
