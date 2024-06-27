# class that inherits from property based test
from qiskit import QuantumCircuit
from QiskitPBT.property import Property


class EntangledPrecondition(Property):
    # specify the inputs that are to be generated
    def get_input_generators(self):
        return []

    # specify the preconditions for the test
    def preconditions(self):
        return True

    # specify the operations to be performed on the input
    def operations(self):
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        # TODO: for some reason this does not work on y basis
        self.statistical_analysis.assert_entangled(self, (0, 1), qc, basis=["z", "x"])
