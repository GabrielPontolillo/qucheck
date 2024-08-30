import os
import unittest
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate

from case_studies.quantum_phase_estimation.quantum_phase_estimation import quantum_phase_estimation
from case_studies.quantum_teleportation.quantum_teleportation import quantum_teleportation
from qucheck.coordinator import Coordinator

from qucheck.input_generators import RandomState, RandomEigenvectorUnitaryPair, RandomUnitary, Integer
from qucheck.property import Property
from qucheck.stats.utils.sampling import split_into_subsamples, weighted_sample
from qucheck.test_runner import TestRunner


class InOutPropertyQTSubsampling(Property):
    def get_input_generators(self):
        state = RandomState(1)
        return [state]

    # specify the preconditions for the test
    def preconditions(self, q0):
        return True

    # specify the operations to be performed on the input
    def operations(self, q0):
        qc = QuantumCircuit(3, 3)
        qc.initialize(q0, [0])
        qt = quantum_teleportation()
        # stitch qc and quantum_teleportation together
        qc = qc.compose(qt)

        # initialise qubit to compare to:
        qc2 = QuantumCircuit(1, 1)
        qc2.initialize(q0, [0])
        self.statistical_analysis.assert_equal(self, 2, qc, 0, qc2, subsample=True)


class LowerRegisterUnchangedByEigenvector(Property):
    # specify the inputs that are to be generated
    def get_input_generators(self):
        eigenvector_unitary_pair = RandomEigenvectorUnitaryPair(RandomUnitary(1, 2), 1)
        estimation_qubits = Integer(1, 3)
        return [eigenvector_unitary_pair, estimation_qubits]

    # specify the preconditions for the test
    def preconditions(self, eigenvector_unitary_pair, estimation_qubits):
        return True

    # specify the operations to be performed on the input
    def operations(self, eigenvector_unitary_pair, estimation_qubits):
        eigenvectors, unitary = eigenvector_unitary_pair

        n = unitary.num_qubits

        # perform qpe on with an eigenvector in lower register
        qpe = quantum_phase_estimation(estimation_qubits, UnitaryGate(unitary), eigenvectors[0][0])

        # state should be the unchanged eigenvector
        qpe2 = QuantumCircuit(n, n)
        qpe2.initialize(eigenvectors[0][0], list(range(n)))

        self.statistical_analysis.assert_equal(self, list(range(estimation_qubits, estimation_qubits+unitary.num_qubits)), qpe, list(range(n)), qpe2, subsample=True)


class TestSamplingUtils(unittest.TestCase):
    def tearDown(self):
        pass

    def test_split_into_subsamples_even_distribution(self):
        counts = {'11': 100, '10': 100, '00': 100}
        subsamples = split_into_subsamples(counts, 3)
        assert len(subsamples) == 3
        for subsample in subsamples:
            assert sum(subsample.values()) == 100

    def test_split_into_subsamples_uneven_distribution(self):
        counts = {'11': 100, '01': 50, '10': 25}
        subsamples = split_into_subsamples(counts, 5)
        assert len(subsamples) == 5
        for subsample in subsamples:
            assert sum(subsample.values()) == 35

    def test_split_into_subsamples_single_subsample(self):
        counts = {'11': 100, '10': 50, '00': 25}
        subsamples = split_into_subsamples(counts, 1)
        assert len(subsamples) == 1
        assert sum(subsamples[0].values()) == 175

    def test_weighted_sample_correct_distribution(self):
        counts = {'11': 100, '01': 50, '10': 25}
        subsample = weighted_sample(counts, 10)
        assert sum(subsample.values()) == 10

    def test_weighted_sample_empty_counts(self):
        self.assertRaises(IndexError, weighted_sample, {}, 10)

    def test_weighted_sample_more_samples_than_counts(self):
        counts = {'11': 5, '10': 3}
        self.assertRaises(IndexError, weighted_sample, counts, 10)

    def test_qt_in_out_property_subsampling(self):
        runner = TestRunner([InOutPropertyQTSubsampling], 5, 1,2000, 10)
        runner.run_tests()
        assert len(runner.list_failing_properties()) == 0
        assert len(runner.list_passing_properties()) == 1

    def test_lower_register_unchanged_by_eigenvalue_subsampling(self):
        runner = TestRunner([LowerRegisterUnchangedByEigenvector], 5, 1,2000)
        runner.run_tests()
        assert len(runner.list_failing_properties()) == 0
        assert len(runner.list_passing_properties()) == 1

    def test_coordinator_subsampling_still_works(self):
        num_inputs = 5
        measurements = 2000
        coordinator = Coordinator(num_inputs, 1)

        coordinator.test(os.path.dirname(os.path.abspath(__file__)), measurements, run_optimization=True, num_experiments=10)

        passing = coordinator.test_runner.list_passing_properties()
        passing = [elem.__name__ for elem in passing]

        self.assertIn("InOutPropertyQTSubsampling", passing)
        self.assertIn("LowerRegisterUnchangedByEigenvector", passing)