# begin testing the coordinator
import unittest

from case_studies.stats.single_qubit_distributions.single_qubit_statistical_analysis import \
    SingleQubitStatisticalAnalysis

from coordinator import Coordinator

from unittest import TestCase


class TestCoordinator(unittest.TestCase):
    def tearDown(self):
        SingleQubitStatisticalAnalysis.assertions = []
        SingleQubitStatisticalAnalysis.unique_circuits = []
        SingleQubitStatisticalAnalysis.union_of_qubits = []
        SingleQubitStatisticalAnalysis.outcomes = []

    def test_coordinator(self):
        coordinator = Coordinator(5)
        coordinator.test("C:\\Users\\gabri\\PycharmProjects\\QiskitPBT\\case_studies\\quantum_teleportation")
        coordinator.print_outcomes()
