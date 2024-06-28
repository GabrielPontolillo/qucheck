from uuid import uuid4
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

"""
hack to use quantum circuits as dictionary keys, 
this is hash by "reference" not by value - as in, two equal objects will not be hashed to the same value
but it is guaranteed that the same object will always return same hash value
"""
class HashableQuantumCircuit(QuantumCircuit):
    # def __hash__(self):
    #     if hasattr(self, "_hash_val"):
    #         return self._hash_val
    #     else:
    #         self._hash_val = hash(uuid4())
    #         return self._hash_val

    # fixing this should fix the issue mostly - currently to add the measurement circuit it is added with a different name
    def __eq__(self, other):
        return self.data.__str__() == other.data.__str__()

    def __hash__(self):
        if hasattr(self, "_hash_val"):
            return self._hash_val
        else:
            # print(QuantumCircuit(self.data[1:]))
            # op = Operator(QuantumCircuit(self.data[1:]))
            # inp = self[0]
            # self._hash_val = hash(op + inp.__str__())
            # return self._hash_val

            # TODO: Ok this works, but I do not know at what cost?
            self._hash_val = hash(self.data.__str__())
            return self._hash_val