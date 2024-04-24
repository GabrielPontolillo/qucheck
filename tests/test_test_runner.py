# a test script for the test runner
from QiskitPBT.test_runner import TestRunner
from QiskitPBT.case_studies.quantum_teleportation.inq0_equal_outq2 import Inq0EqualOutq2
from QiskitPBT.case_studies.quantum_fourier_transform.identity_property import IdentityProperty
from QiskitPBT.tests.mock_properties.failing_precondition_property import FailingPrecondition


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

    def test_two_different_properties(self):
        # create an instance of the test runner
        test_runner = TestRunner([Inq0EqualOutq2, IdentityProperty], 3, 1917)
        # run the tests
        test_runner.run_tests()
        # list the failing properties
        assert test_runner.list_failing_properties() == []
        assert test_runner.list_passing_properties() == [Inq0EqualOutq2, IdentityProperty]

