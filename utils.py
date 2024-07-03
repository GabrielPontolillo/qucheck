from uuid import uuid4
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

"""
hack to use quantum circuits as dictionary keys, 
this is hash by "reference" not by value - as in, two equal objects will not be hashed to the same value
but it is guaranteed that the same object will always return same hash value
"""
class HashableQuantumCircuit(QuantumCircuit):
    def __hash__(self):
         if hasattr(self, "_hash_val"):
             return self._hash_val
         else:
             self._hash_val = hash(uuid4())
             return self._hash_val

    def reset_hash(self) -> None:
        self._hash_val = hash(uuid4())
