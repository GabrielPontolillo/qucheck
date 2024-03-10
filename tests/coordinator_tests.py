# begin testing the coordinator
from coordinator import Coordinator

from unittest import TestCase


class TestCoordinator(TestCase):
    def test_coordinator(self):
        coordinator = Coordinator(5)
        coordinator.test("C:\\Users\\gabri\\PycharmProjects\\QiskitPBT\\case_studies\\quantum_teleportation")
        coordinator.print_outcomes()
