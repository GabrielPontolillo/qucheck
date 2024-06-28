# a test script for the test runner
import copy
from QiskitPBT.test_runner import TestRunner
from QiskitPBT.case_studies.quantum_teleportation.input_reg0_equal_to_output_reg2_property import Inq0EqualOutq2
from QiskitPBT.case_studies.quantum_teleportation.not_teleported_registers_equal_to_plus_property import NotTeleportedPlus
from QiskitPBT.case_studies.quantum_fourier_transform.identity_property import IdentityProperty
from QiskitPBT.tests.mock_properties.failing_precondition_property import FailingPrecondition

from unittest import TestCase


class TestTestRunner(TestCase):
    def tearDown(self):
        TestRunner.property_objects = []
        TestRunner.seeds_list_dict = {}

    # test the run_tests method
    def test_run_tests(self):
        # create an instance of the test runner
        test_runner = TestRunner([Inq0EqualOutq2], 10,  548, 1000)
        # run the tests
        test_runner.run_tests()
        print(test_runner.seeds_list_dict.values())
        self.assertEqual(test_runner.list_failing_properties(), [])
        self.assertEqual(test_runner.list_passing_properties(), [Inq0EqualOutq2])

    def test_run_tests_cost(self):
        # create an instance of the test runner
        test_runner = TestRunner([Inq0EqualOutq2, NotTeleportedPlus], 2,  548, 1000)
        # run the tests
        test_runner.run_tests()
        print(test_runner.seeds_list_dict.values())
        self.assertEqual(test_runner.list_failing_properties(), [])
        self.assertEqual(test_runner.list_passing_properties(), [Inq0EqualOutq2, NotTeleportedPlus])

    def test_run_tests_cost2(self):
        # create an instance of the test runner
        test_runner = TestRunner([Inq0EqualOutq2, Inq0EqualOutq2], 10,  548, 1000)
        # run the tests
        test_runner.run_tests()
        print(test_runner.seeds_list_dict.values())
        self.assertEqual(test_runner.list_failing_properties(), [])
        self.assertEqual(test_runner.list_passing_properties(), [Inq0EqualOutq2, Inq0EqualOutq2])

    def test_run_tests2(self):
        # create an instance of the test runner
        test_runner = TestRunner([Inq0EqualOutq2, Inq0EqualOutq2], 3, 1910, 1000)
        # run the tests
        test_runner.run_tests()
        # list the failing properties
        print("failing properties:")
        print(test_runner.list_failing_properties())
        print("passing properties:")
        # we actually get a list of passing properties objects
        print(test_runner.list_passing_properties())

    def test_same_seeds(self):
        # create an instance of the test runner
        test_runner = TestRunner([Inq0EqualOutq2, Inq0EqualOutq2], 3, 1, 1000)
        # run the tests
        test_runner.run_tests()
        save_seeds = copy.deepcopy(test_runner.generated_seeds)
        # create an instance of the test runner
        TestRunner.property_objects = []
        TestRunner.generated_seeds = []
        test_runner2 = TestRunner([Inq0EqualOutq2, Inq0EqualOutq2], 3, 1, 1000)
        # run the tests
        test_runner2.run_tests()
        save_seeds2 = test_runner2.generated_seeds
        self.assertEqual(save_seeds, save_seeds2)

    def test_different_seeds(self):
        # create an instance of the test runner
        test_runner = TestRunner([Inq0EqualOutq2, Inq0EqualOutq2], 3, 1, 1000)
        # run the tests
        test_runner.run_tests()
        save_seeds = copy.deepcopy(test_runner.generated_seeds)
        # create an instance of the test runner
        TestRunner.property_objects = []
        TestRunner.generated_seeds = []
        test_runner2 = TestRunner([Inq0EqualOutq2, Inq0EqualOutq2], 3, 2, 1000)
        # run the tests
        test_runner2.run_tests()
        save_seeds2 = test_runner2.generated_seeds
        self.assertNotEqual(save_seeds, save_seeds2)

    def test_failing_precondition(self):
        # create an instance of the test runner
        test_runner = TestRunner([FailingPrecondition], 2,  548, 1000)
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
        test_runner = TestRunner([Inq0EqualOutq2, IdentityProperty], 3, 1917, 1000)
        # run the tests
        test_runner.run_tests()
        # list the failing properties
        assert test_runner.list_failing_properties() == []
        assert test_runner.list_passing_properties() == [Inq0EqualOutq2, IdentityProperty]

