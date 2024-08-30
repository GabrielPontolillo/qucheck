# class that inherits from property based test
from qiskit import QuantumCircuit
from qucheck.property import Property
from qucheck.input_generators import RandomStatePreparationCircuit
from case_studies.quantum_teleportation.quantum_teleportation import quantum_teleportation


class InOutQTCircuitGen(Property):
    # specify the inputs that are to be generated
    def get_input_generators(self):
        circuit = RandomStatePreparationCircuit(1, 1)
        return [circuit]

    # specify the preconditions for the test
    def preconditions(self, circuit):
        return True

    # specify the operations to be performed on the input
    def operations(self, circuit):
        qc = QuantumCircuit(3, 3)
        qc.compose(circuit, [0], inplace=True)
        qt = quantum_teleportation()
        # stitch qc and quantum_teleportation together
        qc = qc.compose(qt)

        # initialise qubit to compare to:
        qc2 = QuantumCircuit(1, 1)
        qc2.compose(circuit, [0], inplace=True)
        self.statistical_analysis.assert_equal(self, 2, qc, 0, qc2)


class NotTeleportedPlusCircuitGen(Property):
    # specify the inputs that are to be generated
    def get_input_generators(self):
        circuit = RandomStatePreparationCircuit(1, 1)
        return [circuit]

    # specify the preconditions for the test
    def preconditions(self, q0):
        return True

    # specify the operations to be performed on the input
    def operations(self, circuit):
        # breaks if classical register is not explicitly defined?
        qc = QuantumCircuit(3, 3)
        qc.compose(circuit, [0], inplace=True)
        qt = quantum_teleportation()
        # stitch qc and quantum_teleportation together
        qc = qc.compose(qt)

        # initialise another circuit to |++> state
        # breaks if classical register is not explicitly defined?
        qc2 = QuantumCircuit(2, 2)
        qc2.h(0)
        qc2.h(1)

        self.statistical_analysis.assert_equal(self, [0, 1], qc, [0, 1], qc2)

