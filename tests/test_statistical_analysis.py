# class that tests the statistical analysis class
import unittest

from QiskitPBT.stats.statistical_analysis_coordinator import StatisticalAnalysisCoordinator
from qiskit import QuantumCircuit
from case_studies.quantum_teleportation.input_reg0_equal_to_output_reg2 import Inq0EqualOutq2


# used for hashing the input function
def input_function():
    return [0]


class TestStatisticalAnalysis(unittest.TestCase):
    # make sure to reset statistical analysis class variables
    def tearDown(self):
        SingleQubitStatisticalAnalysis.assertions = []
        SingleQubitStatisticalAnalysis.unique_circuits = []
        SingleQubitStatisticalAnalysis.union_of_qubits = []
        SingleQubitStatisticalAnalysis.outcomes = []

    def test_assert_equal(self):
        qc = QuantumCircuit(1)
        qc2 = QuantumCircuit(1)
        st = SingleQubitStatisticalAnalysis(Inq0EqualOutq2, input_function.__hash__)
        st.assert_equal(qc, [0], qc2, [0])
        print(st.assertions)
        assert len(st.assertions) == 1
        # assert that first element is a subclass of Property
        print(st.perform_measurements())

    def test_assert_equal2(self):
        qc = QuantumCircuit(2)
        qc2 = QuantumCircuit(2)
        qc3 = QuantumCircuit(4)
        st = SingleQubitStatisticalAnalysis(Inq0EqualOutq2, input_function.__hash__)
        st2 = SingleQubitStatisticalAnalysis(Inq0EqualOutq2, input_function.__hash__)
        st.assert_equal(qc, [0], qc2, [0, 1])
        st2.assert_equal(qc, [0], qc3, [0, 2])
        print(st.assertions)
        assert len(st.assertions) == 2
        assert len(st2.assertions) == 2
        st.perform_measurements()
        print(st.outcomes)
        assert (st.outcomes[0].get(0, None) is not None)
        assert (st.outcomes[0].get(1, None) is not None)
        assert (st.outcomes[1].get(0, None) is not None)
        assert (st.outcomes[1].get(2, None) is not None)

    def test_assert_equal3(self):
        qc = QuantumCircuit(2)
        qc2 = QuantumCircuit(2)
        qc3 = QuantumCircuit(4)
        st = SingleQubitStatisticalAnalysis(Inq0EqualOutq2, input_function.__hash__)
        st2 = SingleQubitStatisticalAnalysis(Inq0EqualOutq2, input_function.__hash__)
        st.assert_equal(qc, [0], qc2, [0, 1])
        st2.assert_equal(qc, [0], qc3, [0, 2])
        print(st.assertions)
        assert len(st.assertions) == 2
        assert len(st2.assertions) == 2
        st.perform_measurements()
        assert (st.outcomes[0].get(0, None) is not None)
        assert (st.outcomes[0].get(1, None) is not None)
        assert (st.outcomes[1].get(0, None) is not None)
        assert (st.outcomes[1].get(2, None) is not None)

    def test_assert_equal4(self):
        qc = QuantumCircuit(2)
        qc2 = QuantumCircuit(2)
        st = SingleQubitStatisticalAnalysis(Inq0EqualOutq2, input_function.__hash__)
        st.assert_equal(qc, [0], qc2, [0])
        print(st.assertions)
        st.perform_analysis()
        assert st.assertions[0].p_vals is not None
        # since they are the same circuit, only one set of measurements is performed, so the p-values should be 1
        assert st.assertions[0].p_vals[0] == 1
        assert st.assertions[0].p_vals[1] == 1
        assert st.assertions[0].p_vals[2] == 1

    def test_assert_equal5(self):
        qc = QuantumCircuit(2)
        qc2 = QuantumCircuit(2)
        st = SingleQubitStatisticalAnalysis(Inq0EqualOutq2, input_function.__hash__, 4000)
        st.assert_equal(qc, [0], qc2, [1])
        print(st.assertions)
        st.perform_analysis()
        assert st.assertions[0].p_vals is not None
        # since they are the same circuit, but the qubits being measured are different, we are comparing different qubits distribution on the same circuit
        # unlikely that the p_value will be exactly 1, though the p-value should be greater than 0.05, though measurement of z basis should be 1
        assert st.assertions[0].p_vals[0] != 1
        assert st.assertions[0].p_vals[1] != 1
        assert st.assertions[0].p_vals[2] == 1

    def test_assert_equal6(self):
        qc = QuantumCircuit(2)
        qc2 = QuantumCircuit(2)
        qc2.x(0)
        st = SingleQubitStatisticalAnalysis(Inq0EqualOutq2, input_function.__hash__, 4000)
        st.assert_equal(qc, [0, 1], qc2, [0, 1])
        print(st.assertions)
        st.perform_analysis()
        assert st.assertions[0].p_vals is not None

