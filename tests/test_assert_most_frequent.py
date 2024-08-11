# a test script for the test runner
from QiskitPBT.test_runner import TestRunner
from QiskitPBT.tests.mock_properties.frequency_property import FrequencyProperty,  UncertainFrequencyProperty


from unittest import TestCase


class TestAssertMostFrequent(TestCase):
    def tearDown(self):
        TestRunner.property_objects = []
        TestRunner.seeds_list_dict = []

    def test_single_frequency(self):
        # create an instance of the test runner
        test_runner = TestRunner([FrequencyProperty], 10,  546, 1000)
        # run the tests
        test_runner.run_tests()
        # list the failing properties
        assert test_runner.list_passing_properties() == [FrequencyProperty]
        assert test_runner.list_failing_properties() == []

    def test_multiple_frequency(self):
        # create an instance of the test runner
        test_runner = TestRunner([UncertainFrequencyProperty], 10,  548, 1000)
        # run the tests
        test_runner.run_tests()
        # list the failing properties
        assert test_runner.list_passing_properties() == [UncertainFrequencyProperty]
        assert test_runner.list_failing_properties() == []
