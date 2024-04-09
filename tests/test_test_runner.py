# a test script for the test runner
import copy

from test_runner import TestRunner
from case_studies.quantum_teleportation.inq0_equal_outq2 import Inq0EqualOutq2
from tests.mock_properties.failing_precondition_property import FailingPrecondition


from unittest import TestCase

class TestTestRunner(TestCase):
    def tearDown(self):
        TestRunner.property_objects = []

    # test the run_tests method
    def test_run_tests(self):
        # create an instance of the test runner
        test_runner = TestRunner([Inq0EqualOutq2, Inq0EqualOutq2], 5,  548)
        # run the tests
        test_runner.run_tests()
        # list the failing properties
        print("failing properties:")
        print(test_runner.list_failing_properties())
        print("passing properties:")
        # we actually get a list of passing properties objects
        print(test_runner.list_passing_properties())

    def test_failing_precondition(self):
        # create an instance of the test runner
        test_runner = TestRunner([FailingPrecondition], 2,  548)
        # run the tests
        test_runner.run_tests()
        # list the failing properties
        print("failing properties:")
        print(test_runner.list_failing_properties())
        print("passing properties:")
        # we actually get a list of passing properties objects
        print(test_runner.list_passing_properties())
