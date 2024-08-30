from case_studies.deutsch_jozsa.balanced_property import DeutschJozsaWorksForBalancedFunction
from case_studies.deutsch_jozsa.constant_property import DeutschJozsaWorksForConstantFunction
from case_studies.deutsch_jozsa.vmerge_two_constant_oracles_property import DeutschJozsaVMergeTwoConstantOracles
from case_studies.deutsch_jozsa.vmerge_two_balanced_oracles_property import DeutschJozsaVMergeTwoBalancedOracles
from case_studies.deutsch_jozsa.dj_lower_register_minus_property import DeutschJozsaLowerRegisterMinus
from qucheck.test_runner import TestRunner

import unittest


class TestDeutschJozsa(unittest.TestCase):
    def test_balanced_properties(self):
        # run the test
        runner = TestRunner([DeutschJozsaWorksForBalancedFunction], 5, 42, 5000)
        runner.run_tests()
        # the property should pass
        assert runner.list_failing_properties() == []
        assert runner.list_passing_properties() == [DeutschJozsaWorksForBalancedFunction]

    def test_constant_properties(self):
        # run the test
        runner = TestRunner([DeutschJozsaWorksForConstantFunction], 5, 4,  5000)
        runner.run_tests()
        # the property should pass
        assert runner.list_failing_properties() == []
        assert runner.list_passing_properties() == [DeutschJozsaWorksForConstantFunction]

    def test_vmerge_two_constant_oracles(self):
        # run the test
        runner = TestRunner([DeutschJozsaVMergeTwoConstantOracles], 5, 3, 5000)
        runner.run_tests()
        # the property should pass
        assert runner.list_failing_properties() == []
        assert runner.list_passing_properties() == [DeutschJozsaVMergeTwoConstantOracles]

    def test_vmerge_two_balanced_oracles(self):
        # run the test
        runner = TestRunner([DeutschJozsaVMergeTwoBalancedOracles], 5, 2, 5000)
        runner.run_tests()
        # the property should pass
        assert runner.list_failing_properties() == []
        assert runner.list_passing_properties() == [DeutschJozsaVMergeTwoBalancedOracles]

    def test_lower_register_minus(self):
        # run the test
        runner = TestRunner([DeutschJozsaLowerRegisterMinus], 5, 11, 5000)
        runner.run_tests()
        # the property should pass
        assert runner.list_failing_properties() == []
        assert runner.list_passing_properties() == [DeutschJozsaLowerRegisterMinus]