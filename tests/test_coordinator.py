# begin testing the coordinator
import os
from unittest import TestCase

from QiskitPBT.coordinator import Coordinator
from QiskitPBT.test_runner import TestRunner

PARENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))


class TestCoordinator(TestCase):
    def tearDown(self):
        TestRunner.property_objects = []
        TestRunner.seeds = []

    # basic test just to see if the coordinator runs without throwing an exception
    def test_coordinator(self):
        coordinator = Coordinator(5)
        coordinator.test(os.path.join(PARENT_DIR, "case_studies/quantum_teleportation"))
        coordinator.print_outcomes()

    # test coordinator to check if it will generate the same local seeds with the same random seed
    def test_coordinator_same_seeds(self):
        num_inputs = 2
        coordinator = Coordinator(num_inputs, 1)
        coordinator.test(os.path.join(PARENT_DIR, "case_studies/quantum_teleportation"))
        save_seeds = coordinator.test_runner.seeds

        # reset the seeds and property objects to ensure next run works
        TestRunner.seeds = []
        TestRunner.property_objects = []

        coordinator2 = Coordinator(num_inputs, 1)
        coordinator2.test(os.path.join(PARENT_DIR, "case_studies/quantum_teleportation"))
        save_seeds2 = coordinator2.test_runner.seeds

        self.assertEqual(len(save_seeds), num_inputs * len(TestRunner.property_objects))
        self.assertEqual(save_seeds, save_seeds2)

    # test coordinator to check if it will generate different local seeds with different random seeds
    def test_coordinator_different_seeds(self):
        num_inputs = 2
        coordinator = Coordinator(num_inputs, 1)
        coordinator.test(os.path.join(PARENT_DIR, "case_studies/quantum_teleportation"))
        save_seeds = coordinator.test_runner.seeds

        # reset the seeds and property objects to ensure next run works
        TestRunner.seeds = []
        TestRunner.property_objects = []

        coordinator2 = Coordinator(num_inputs, 2)
        coordinator2.test(os.path.join(PARENT_DIR, "case_studies/quantum_teleportation"))
        save_seeds2 = coordinator2.test_runner.seeds

        self.assertEqual(len(save_seeds), num_inputs * len(TestRunner.property_objects))
        self.assertNotEqual(save_seeds, save_seeds2)

    # test coordinator, to check that the property will fail if the preconditions are not met
    def test_coordinator_failing_precondition(self):
        coordinator = Coordinator(2, 902)
        coordinator.test(os.path.join(PARENT_DIR, "tests/mock_properties"))
        passing = coordinator.test_runner.list_passing_properties()
        self.assertEqual(passing, [])

        failing = coordinator.test_runner.list_failing_properties()
        self.assertEqual(len(failing), 1)
        self.assertEqual(failing[0].__name__, "FailingPrecondition")