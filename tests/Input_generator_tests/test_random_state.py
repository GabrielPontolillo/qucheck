import itertools
import numpy as np
import unittest

from functools import reduce
from input_generators.random_state import RandomState
from qiskit.quantum_info import Statevector


class TestRandomState(unittest.TestCase):
    def setUp(self):
        self.generator = RandomState(2)

    def test_generate_size(self):
        statevector = self.generator.generate()
        self.assertEqual(len(statevector), 2 ** self.generator.number_of_qubits)

    def test_generate_different(self):
        statevector1 = self.generator.generate()
        statevector2 = self.generator.generate()
        self.assertFalse(np.array_equal(statevector1, statevector2))

    def test_generate_normalized(self):
        statevector = self.generator.generate()
        self.assertTrue(Statevector(statevector).is_valid())
