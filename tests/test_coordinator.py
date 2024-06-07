# begin testing the coordinator
import os
from unittest import TestCase

from QiskitPBT.coordinator import Coordinator
from QiskitPBT.test_runner import TestRunner

PARENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))


class TestCoordinator(TestCase):
    def tearDown(self):
        TestRunner.property_objects = []
        TestRunner.seeds_list_dict = {}

    # basic test just to see if the coordinator runs without throwing an exception
    def test_coordinator(self):
        coordinator = Coordinator(5)
        coordinator.test(os.path.join(PARENT_DIR, "case_studies/quantum_teleportation"), 1000)
        coordinator.print_outcomes()

    # test coordinator to check if it will generate the correct number of inputs
    # if the generators are different
    def test_coordinator_num_inputs_generated(self):
        num_inputs = 2
        coordinator = Coordinator(num_inputs)
        coordinator.test(os.path.join(PARENT_DIR, "case_studies/quantum_fourier_transform"), 1000)
        save_seeds = coordinator.test_runner.seeds_list_dict

        print(save_seeds)
        all_seed_list = [seed for seed_list in save_seeds.values() for seed in seed_list]
        # three properties, with three properties with different input gens
        self.assertEqual(len(all_seed_list), num_inputs * 3)

    # test coordinator to check if it will generate the same local seeds with the same random seed
    # also checks if the correct number of inputs are generated if some of the generators are the same
    def test_coordinator_same_seeds(self):
        num_inputs = 2
        coordinator = Coordinator(num_inputs, 1)
        coordinator.test(os.path.join(PARENT_DIR, "case_studies/quantum_teleportation"), 1000)
        save_seeds = coordinator.test_runner.seeds_list_dict

        # reset the seeds and property objects to ensure next run works
        TestRunner.seeds_list_dict = {}
        TestRunner.property_objects = []

        coordinator2 = Coordinator(num_inputs, 1)
        coordinator2.test(os.path.join(PARENT_DIR, "case_studies/quantum_teleportation"), 1000)
        save_seeds2 = coordinator2.test_runner.seeds_list_dict

        print(save_seeds)
        print(save_seeds2)

        # add up the sum of the length of all lists in the seed dictionary
        all_seed_list = [seed for seed_list in save_seeds.values() for seed in seed_list]

        # three properties, but two proerties with different input gens
        self.assertEqual(len(all_seed_list), num_inputs * 2)
        self.assertDictEqual(save_seeds, save_seeds2)

    # test coordinator to check if it will generate different local seeds with different random seeds
    def test_coordinator_different_seeds(self):
        num_inputs = 2
        coordinator = Coordinator(num_inputs, 1)
        coordinator.test(os.path.join(PARENT_DIR, "case_studies/quantum_teleportation"), 1000)
        save_seeds = coordinator.test_runner.seeds_list_dict

        # reset the seeds and property objects to ensure next run works
        TestRunner.seeds_list_dict = {}
        TestRunner.property_objects = []

        coordinator2 = Coordinator(num_inputs, 2)
        coordinator2.test(os.path.join(PARENT_DIR, "case_studies/quantum_teleportation"), 1000)
        save_seeds2 = coordinator2.test_runner.seeds_list_dict

        print(save_seeds.values())
        print(save_seeds2.values())

        all_seed_list = [seed for seed_list in save_seeds.values() for seed in seed_list]
        print(all_seed_list)

        # three properties, but two properties with different input gens
        self.assertEqual(len(all_seed_list), num_inputs * 2)
        self.assertNotEqual(save_seeds, save_seeds2)

    # test coordinator, to check that the property will fail if the preconditions are not met
    def test_coordinator_failing_precondition(self):
        coordinator = Coordinator(2, 902)
        coordinator.test(os.path.join(PARENT_DIR, "tests/mock_properties"), 1000)
        passing = coordinator.test_runner.list_passing_properties()
        self.assertEqual(passing, [])

        failing = coordinator.test_runner.list_failing_properties()
        self.assertEqual(len(failing), 1)
        self.assertEqual(failing[0].__name__, "FailingPrecondition")