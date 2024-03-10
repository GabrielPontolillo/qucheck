# a test script for the input_generators
import unittest
from input_generators.qiskit_uniform_statevector import QiskitUniformStatevector


# test the QiskitUniformStatevector input generator
class TestQiskitUniformStatevector(unittest.TestCase):
    # test the generate method
    def test_generate(self):
        # create an instance of the QiskitUniformStatevector input generator
        qiskit_uniform_statevector = QiskitUniformStatevector(2)
        # generate a statevector
        statevector = qiskit_uniform_statevector.generate()
        # check that the statevector is the correct length
        self.assertEqual(len(statevector), 4)
        # check that the statevector is normalized
        self.assertAlmostEqual(sum([abs(x) ** 2 for x in statevector]), 1.0)

    def test_generate_3(self):
        qiskit_uniform_statevector = QiskitUniformStatevector(3)
        statevector = qiskit_uniform_statevector.generate()
        self.assertEqual(len(statevector), 8)
        self.assertAlmostEqual(sum([abs(x) ** 2 for x in statevector]), 1.0)