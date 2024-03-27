from case_studies.quantum_fourier_transform.identity_property import IdentityProperty
from test_runner import TestRunner

import unittest


# test the identity property
class TestIdentityPropertyQFT(unittest.TestCase):
    def test_identity_property_qft(self):
        num_inputs = 100
        # run the test
        runner = TestRunner([IdentityProperty], num_inputs, 1)
        runner.run_tests()
        # the property should pass
        assert runner.list_failing_properties() == []
        assert runner.list_passing_properties() == [IdentityProperty]
