# a test script for the test runner
from unittest import TestCase

from qucheck.test_runner import TestRunner
from tests.mock_properties.probability_property import ProbabilityProperty, ProbabilityPropertyMultipleQubits, WrongProbabilityProperty


class TestAssertProbability(TestCase):
    def setUp(self):
        self.num_inputs = 10
        self.num_measurements = 5000

    def tearDown(self):
        TestRunner.property_objects = []
        TestRunner.seeds_list_dict = []

    def test_single_probability(self):
        # create an instance of the test runner
        test_runner = TestRunner([ProbabilityProperty], self.num_inputs, 546, self.num_measurements)
        # run the tests
        test_runner.run_tests()
        # list the failing properties
        assert test_runner.list_passing_properties() == [ProbabilityProperty]
        assert test_runner.list_failing_properties() == []

    def test_wrong_probability(self):
        # create an instance of the test runner
        test_runner = TestRunner([WrongProbabilityProperty], self.num_inputs, 546, self.num_measurements)
        # run the tests
        test_runner.run_tests()
        # list the failing properties
        assert test_runner.list_passing_properties() == []
        assert test_runner.list_failing_properties() == [WrongProbabilityProperty]

    def test_multiple_probability(self):
        # create an instance of the test runner
        test_runner = TestRunner([ProbabilityPropertyMultipleQubits], self.num_inputs, 547, self.num_measurements)
        # run the tests
        test_runner.run_tests()
        # list the failing properties
        assert test_runner.list_passing_properties() == [ProbabilityPropertyMultipleQubits]
        assert test_runner.list_failing_properties() == []
