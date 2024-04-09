# begin testing the coordinator
import os

from coordinator import Coordinator
from test_runner import TestRunner

from unittest import TestCase
class TestCoordinator(TestCase):
    def tearDown(self):
        TestRunner.property_objects = []

    def test_coordinator(self):
        coordinator = Coordinator(5)
        coordinator.test(os.path.join(os.getcwd(), "case_studies/quantum_teleportation"))
        coordinator.print_outcomes()

    def test_coordinator_different_seeds(self):
        coordinator = Coordinator(2, 902)
        coordinator.test(os.path.join(os.getcwd(), "case_studies/quantum_teleportation"))
        passing = coordinator.test_runner.list_passing_properties()
        failing = coordinator.test_runner.list_failing_properties()
        coordinator.print_outcomes()
        TestRunner.property_objects = []
        coordinator2 = Coordinator(2, 1000068)
        coordinator2.test(os.path.join(os.getcwd(), "case_studies/quantum_teleportation"))
        passing2 = coordinator2.test_runner.list_passing_properties()
        failing2 = coordinator2.test_runner.list_failing_properties()
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

