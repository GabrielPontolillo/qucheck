# a test script for the test runner
from QiskitPBT.test_runner import TestRunner
from QiskitPBT.tests.mock_properties.entangled_property import EntangledPrecondition


from unittest import TestCase

class TestAssertEntangled(TestCase):
    def tearDown(self):
        TestRunner.property_objects = []
        TestRunner.seeds = []

    def test_entangled_precondition(self):
        # create an instance of the test runner
        test_runner = TestRunner([EntangledPrecondition], 2,  548)
        # run the tests
        test_runner.run_tests()
        # list the failing properties
        assert test_runner.list_passing_properties() == [EntangledPrecondition]
        assert test_runner.list_failing_properties() == []
