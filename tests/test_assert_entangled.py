# a test script for the test runner
from QiskitPBT.test_runner import TestRunner
from QiskitPBT.tests.mock_properties.entangled_property import EntangledPrecondition, EntangledCheckOnUnentangledState, EntangledCheckOnGHZState


from unittest import TestCase


class TestAssertEntangled(TestCase):
    def tearDown(self):
        TestRunner.property_objects = []
        TestRunner.seeds_list_dict = []

    def test_entangled_precondition(self):
        # create an instance of the test runner
        test_runner = TestRunner([EntangledPrecondition], 2,  548, 1000)
        # run the tests
        test_runner.run_tests()
        # list the failing properties
        assert test_runner.list_passing_properties() == [EntangledPrecondition]
        assert test_runner.list_failing_properties() == []

    def test_entangled_check_on_unentangled_state(self):
        # create an instance of the test runner
        test_runner = TestRunner([EntangledCheckOnUnentangledState], 2,  548, 1000)
        # run the tests
        test_runner.run_tests()
        # list the failing properties
        assert test_runner.list_passing_properties() == []
        assert test_runner.list_failing_properties() == [EntangledCheckOnUnentangledState]

    def test_entangled_check_on_GHZ_state(self):
        # create an instance of the test runner
        test_runner = TestRunner([EntangledCheckOnGHZState], 1,  548, 1000)
        # run the tests
        test_runner.run_tests()
        # list the failing properties
        assert test_runner.list_passing_properties() == [EntangledCheckOnGHZState]
        assert test_runner.list_failing_properties() == []
