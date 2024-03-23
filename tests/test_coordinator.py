# begin testing the coordinator
import unittest
import os

from stats.single_qubit_distributions.single_qubit_statistical_analysis import SingleQubitStatisticalAnalysis

from coordinator import Coordinator
from test_runner import TestRunner

from unittest import TestCase


class TestCoordinator(unittest.TestCase):
    def tearDown(self):
        SingleQubitStatisticalAnalysis.assertions = []
        SingleQubitStatisticalAnalysis.unique_circuits = []
        SingleQubitStatisticalAnalysis.union_of_qubits = []
        SingleQubitStatisticalAnalysis.outcomes = []
        TestRunner.property_objects = []
        TestRunner.generated_seeds = []

    def test_coordinator(self):

        coordinator = Coordinator(5)
        coordinator.test(os.path.join(os.getcwd(), "case_studies/quantum_teleportation"))
        coordinator.print_outcomes()

    # test coordinator to check if it will generate the same local seeds with the same random seed
    def test_coordinator_same_seeds(self):
        coordinator = Coordinator(2, 1)
        coordinator.test(os.path.join(os.getcwd(), "case_studies/quantum_teleportation"))
        save_seeds = coordinator.test_runner.generated_seeds
        passing = coordinator.test_runner.list_passing_properties()
        failing = coordinator.test_runner.list_failing_properties()
        TestRunner.generated_seeds = []
        TestRunner.property_objects = []
        coordinator2 = Coordinator(2, 1)
        coordinator2.test(os.path.join(os.getcwd(), "case_studies/quantum_teleportation"))
        save_seeds2 = coordinator2.test_runner.generated_seeds
        passing2 = coordinator2.test_runner.list_passing_properties()
        failing2 = coordinator2.test_runner.list_failing_properties()
        self.assertEqual(save_seeds, save_seeds2)
        self.assertEqual(passing, passing2)
        self.assertEqual(failing, failing2)

    def test_coordinator_different_seeds(self):
        coordinator = Coordinator(2, 902)
        coordinator.test(os.path.join(os.getcwd(), "case_studies/quantum_teleportation"))
        save_seeds = coordinator.test_runner.generated_seeds
        passing = coordinator.test_runner.list_passing_properties()
        failing = coordinator.test_runner.list_failing_properties()
        coordinator.print_outcomes()
        TestRunner.generated_seeds = []
        TestRunner.property_objects = []
        coordinator2 = Coordinator(2, 1000068)
        coordinator2.test(os.path.join(os.getcwd(), "case_studies/quantum_teleportation"))
        save_seeds2 = coordinator2.test_runner.generated_seeds
        passing2 = coordinator2.test_runner.list_passing_properties()
        failing2 = coordinator2.test_runner.list_failing_properties()
        self.assertNotEqual(save_seeds, save_seeds2)
        # same properties need to pass or fail, no matter the input
        self.assertEqual(passing, passing2)
        self.assertEqual(failing, failing2)

    def test_coordinator_failing_precondition(self):
        coordinator = Coordinator(2, 902)
        coordinator.test(os.path.join(os.getcwd(), "tests/mock_properties"))
        passing = coordinator.test_runner.list_passing_properties()
        print("passing properties:")
        print(passing)
        failing = coordinator.test_runner.list_failing_properties()
        print("failing properties:")
        print(failing)


