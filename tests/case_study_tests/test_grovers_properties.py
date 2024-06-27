from QiskitPBT.case_studies.grovers_algorithm.lower_register_minus_property import GroversAlgorithmLowerRegisterMinus
from QiskitPBT.test_runner import TestRunner

import unittest


class TestGrovers(unittest.TestCase):
    def test_lower_register_minus(self):
        # run the test
        runner = TestRunner([GroversAlgorithmLowerRegisterMinus], 5, 42, 1000)
        runner.run_tests()
        # the property should pass
        assert runner.list_failing_properties() == []
        assert runner.list_passing_properties() == [GroversAlgorithmLowerRegisterMinus]