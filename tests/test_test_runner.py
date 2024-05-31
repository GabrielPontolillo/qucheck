# a test script for the test runner
import unittest
import copy
from test_runner import TestRunner
from case_studies.quantum_teleportation.input_reg0_equal_to_output_reg2_property import Inq0EqualOutq2
from case_studies.quantum_fourier_transform.identity_property import IdentityProperty
from tests.mock_properties.failing_precondition_property import FailingPrecondition
from case_studies.stats.single_qubit_distributions.single_qubit_statistical_analysis import SingleQubitStatisticalAnalysis


class TestTestRunner(unittest.TestCase):
    def tearDown(self):
        SingleQubitStatisticalAnalysis.assertions = []
        SingleQubitStatisticalAnalysis.unique_circuits = []
        SingleQubitStatisticalAnalysis.union_of_qubits = []
        SingleQubitStatisticalAnalysis.outcomes = []
        TestRunner.property_objects = []
        TestRunner.generated_seeds = []

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

    def test_run_tests2(self):
        # create an instance of the test runner
        test_runner = TestRunner([Inq0EqualOutq2, Inq0EqualOutq2], 3, 1910)
        # run the tests
        test_runner.run_tests()
        # list the failing properties
        print("failing properties:")
        print(test_runner.list_failing_properties())
        print("passing properties:")
        # we actually get a list of passing properties objects
        print(test_runner.list_passing_properties())
        print(test_runner.property_objects[0].statistical_analysis.assertions)

    def test_same_seeds(self):
        # create an instance of the test runner
        test_runner = TestRunner([Inq0EqualOutq2, Inq0EqualOutq2], 3, 1)
        # run the tests
        test_runner.run_tests()
        save_seeds = copy.deepcopy(test_runner.generated_seeds)
        # create an instance of the test runner
        TestRunner.property_objects = []
        TestRunner.generated_seeds = []
        test_runner2 = TestRunner([Inq0EqualOutq2, Inq0EqualOutq2], 3, 1)
        # run the tests
        test_runner2.run_tests()
        save_seeds2 = test_runner2.generated_seeds
        self.assertEqual(save_seeds, save_seeds2)

    def test_different_seeds(self):
        # create an instance of the test runner
        test_runner = TestRunner([Inq0EqualOutq2, Inq0EqualOutq2], 3, 1)
        # run the tests
        test_runner.run_tests()
        save_seeds = copy.deepcopy(test_runner.generated_seeds)
        # create an instance of the test runner
        TestRunner.property_objects = []
        TestRunner.generated_seeds = []
        test_runner2 = TestRunner([Inq0EqualOutq2, Inq0EqualOutq2], 3, 2)
        # run the tests
        test_runner2.run_tests()
        save_seeds2 = test_runner2.generated_seeds
        self.assertNotEqual(save_seeds, save_seeds2)

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

