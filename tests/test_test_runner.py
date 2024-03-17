# a test script for the test runner
import unittest
from test_runner import TestRunner
from case_studies.quantum_teleportation.inq0_equal_outq2 import Inq0EqualOutq2
from case_studies.stats.single_qubit_distributions.single_qubit_statistical_analysis import SingleQubitStatisticalAnalysis


class TestTestRunner(unittest.TestCase):
    def tearDown(self):
        SingleQubitStatisticalAnalysis.assertions = []
        SingleQubitStatisticalAnalysis.unique_circuits = []
        SingleQubitStatisticalAnalysis.union_of_qubits = []
        SingleQubitStatisticalAnalysis.outcomes = []

    # test the run_tests method
    def test_run_tests(self):
        # create an instance of the test runner
        test_runner = TestRunner([Inq0EqualOutq2, Inq0EqualOutq2], 5)
        # run the tests
        test_runner.run_tests()
        # list the failing properties
        print("failing properties:")
        print(test_runner.list_failing_properties())
        print("passing properties:")
        # we actually get a list of passing properties objects
        print(test_runner.list_passing_properties())

    def test_run_tests2(self):
        # create an instance of the test runner
        test_runner = TestRunner([Inq0EqualOutq2, Inq0EqualOutq2], 3)
        # run the tests
        test_runner.run_tests()
        # list the failing properties
        print("failing properties:")
        print(test_runner.list_failing_properties())
        print("passing properties:")
        # we actually get a list of passing properties objects
        print(test_runner.list_passing_properties())
        print(test_runner.property_objects[0].statistical_analysis.assertions)

