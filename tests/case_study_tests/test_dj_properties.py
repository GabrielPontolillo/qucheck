from QiskitPBT.case_studies.deutsch_jozsa.balanced_property import DeutschJozsaWorksForBalancedFunction
from QiskitPBT.case_studies.deutsch_jozsa.constant_property import DeutschJozsaWorksForConstantFunction
from QiskitPBT.case_studies.deutsch_jozsa.vmerge_two_constant_oracles_property import DeutschJozsaVMergeTwoConstantOracles
from QiskitPBT.case_studies.deutsch_jozsa.vmerge_two_balanced_oracles_property import DeutschJozsaVMergeTwoBalancedOracles
from QiskitPBT.case_studies.deutsch_jozsa.lower_register_minus_property import DeutschJozsaLowerRegisterMinus
from QiskitPBT.test_runner import TestRunner

import unittest


class TestDeutschJozsa(unittest.TestCase):
    def test_balanced_properties(self):
        # run the test
        runner = TestRunner([DeutschJozsaWorksForBalancedFunction], 5, 42)
        runner.run_tests()
        # the property should pass
        assert runner.list_failing_properties() == []
        assert runner.list_passing_properties() == [DeutschJozsaWorksForBalancedFunction]

    def test_constant_properties(self):
        # run the test
        runner = TestRunner([DeutschJozsaWorksForConstantFunction], 5, 4)
        runner.run_tests()
        # the property should pass
        assert runner.list_failing_properties() == []
        assert runner.list_passing_properties() == [DeutschJozsaWorksForConstantFunction]

    def test_vmerge_two_constant_oracles(self):
        # run the test
        runner = TestRunner([DeutschJozsaVMergeTwoConstantOracles], 5, 3)
        runner.run_tests()
        # the property should pass
        assert runner.list_failing_properties() == []
        assert runner.list_passing_properties() == [DeutschJozsaVMergeTwoConstantOracles]

    def test_vmerge_two_balanced_oracles(self):
        # run the test
        runner = TestRunner([DeutschJozsaVMergeTwoBalancedOracles], 5, 2)
        runner.run_tests()
        # the property should pass
        assert runner.list_failing_properties() == []
        assert runner.list_passing_properties() == [DeutschJozsaVMergeTwoBalancedOracles]

    def test_lower_register_minus(self):
        # run the test
        runner = TestRunner([DeutschJozsaLowerRegisterMinus], 5, 11)
        runner.run_tests()
        # the property should pass
        assert runner.list_failing_properties() == []
        assert runner.list_passing_properties() == [DeutschJozsaLowerRegisterMinus]