# ========================================================================
# Copyright (C) 2019 The MITRE Corporation.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Modified by Gabriel Pontolillo, 2025
# Description: Adapted to work with mutation testing, and to work with my implementations
# ========================================================================

from qiskit_aer import Aer

import unittest
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
from utility import run_flip_marker_as_phase_marker
import oracles
from case_studies.deutsch_jozsa.deutsch_jozsa import deutsch_jozsa



class DeutschJozsa():
    """
    This class contains the implementation and tests for the Deutsch-Jozsa algorithm.
    It checks a given function f(x) that takes in a register and outputs a single bit,
    to see whether or not it's "constant" or "balanced". Constant means it always
    returns 0 (or always 1) for all possible inputs. Balanced means it returns 0 for
    half of the possible inputs and 1 for the other half.
    Normally this would take N/2 + 1 checks (N = the number of possible inputs) in order
    to prove with 100% certainty that the algorithm was one or the other, but the DJ
    algorithm takes advantage of the way the Hadamard gate works to cause quantum
    interference, which can produce the answer in only 1 check.

    This is a "toy" algorithm in the sense that it was invented by mathematicians as
    the first simple example of a problem that offers a speedup with quantum computers
    compared to classical computers, but it's a super contrived problem with no real
    practical applications.
    """
    
    
    # ==============================
	# == Algorithm Implementation ==
	# ==============================


    def check_if_constant_or_balanced(self, circuit, oracle, qubits, oracle_args):
        """
        Runs the Deutsch-Jozsa algorithm on the provided oracle, determining
        whether it's constant or balanced.

        Parameters:
            circuit (QuantumCircuit): The circuit being constructed
            oracle (function): The oracle to check
            qubits (QuantumRegister): The register to run the oracle on
            oracle_args (anything): An oracle-specific argument object to pass to
                the oracle during execution
        """
        # Initialize the register to |+...+>
        circuit.h(qubits)

        # Run the oracle in phase-flip mode. Any of the superposition states that
        # triggered the oracle will have their phase flipped. The only way to get
        # back to the |0...0> state with a mass-Hadamard operation is if all of
        # the phases are the same, which corresponds to a constant function. A
        # balanced function will only flip half of them, which will put the register
        # into some other state that's not |0...0> after a mass-Hadamard.
        run_flip_marker_as_phase_marker(circuit, oracle, qubits, oracle_args)

        # Bring the register back to the computational basis and measure each
		# qubit. If it's |0...0>, we know it's constant. If it's literally anything
		# else, it's balanced.
        circuit.h(qubits)
        measurement = ClassicalRegister(len(qubits))
        circuit.add_register(measurement)
        circuit.measure(qubits, measurement)
        
    
    # ====================
	# == Test Case Code ==
	# ====================


    def run_test(self, oracle_name, oracle, should_be_constant, number_of_qubits, oracle_args):
        """
        Runs the Deutsch-Jozsa algorithm on the provided oracle, ensuring that it
        correctly identifies the oracle as constant or balanced.

        Parameters:
            oracle_name(str): The name of the oracle being tested
            oracle (function): The oracle to run the algorithm on
            should_be_constant (bool): True if the oracle is a constant function, false
                if it's balanced.
            number_of_qubits (int): The number of qubits to use for the oracle's input
                register
            oracle_args (anything): An oracle-specific argument object to pass to the
                oracle during execution
        """
        
        # Construct the circuit
        print(f"Running test: {oracle_name}")
        # register = QuantumRegister(number_of_qubits)
        # circuit = QuantumCircuit(register)

        # Run the Deutsch-Jozsa algorithm on the oracle
        # self.check_if_constant_or_balanced(circuit, oracle, register, oracle_args)

        register = QuantumRegister(number_of_qubits)
        work = QuantumRegister(1)
        oracle_circuit = QuantumCircuit(register, work)
        #
        if oracle_args is None:
            oracle(oracle_circuit, register, work)
        else:
            oracle(oracle_circuit, register, work, oracle_args)
        print(oracle_circuit)

        circuit = deutsch_jozsa(oracle_circuit)
        # circuit.cregs = [ClassicalRegister(10)]
        circuit.measure(range(number_of_qubits), range(number_of_qubits))

        # Run the circuit.
        print(circuit)
        backend = Aer.get_backend('qasm_simulator')
        transpiled_circuit = transpile(circuit, backend, optimization_level=0)
        result = backend.run(transpiled_circuit, shots=1).result()
        counts = result.get_counts(circuit)
        # remove the work qubit from the results
        counts = {k[1:]: v for k, v in counts.items()}
        print(counts)

        # Check to see if the resulting input measurement is all 0s, and if that
        # matches the expected behavior or not
        for(state, count) in counts.items():
            state_int = int(state, 2)
            is_constant = (state_int == 0)
            if(is_constant != should_be_constant):
                return False
        
        return True

    def test_constant_zero(self):
        """
        Runs the test on the constant zero function.
        """

        return self.run_test("constant zero", oracles.always_zero, True, 10, None)


    def test_constant_one(self):
        """
        Runs the test on the constant one function.
        """

        return self.run_test("constant zero", oracles.always_one, True, 10, None)


    def test_odd_number_of_ones(self):
        """
        Runs the test on the odd number of |1> state check.
        """

        return self.run_test("odd number of |1> check", oracles.check_for_odd_number_of_ones, False, 10, None)


    def test_nth_qubit_parity(self):
        """
        Runs the test on the Nth-qubit parity check function.
        """

        for i in range(0, 10):
            if self.run_test(f"q{i} parity check", oracles.check_if_qubit_is_one, False, 10, i) == False:
                return False
        return True


    
if __name__ == '__main__':
    # unittest.main()
    import csv
    import importlib
    import os
    import sys
    from os.path import dirname
    from unittest.mock import patch

    def import_function(module_str, path, function_name):
        spec = importlib.util.spec_from_file_location(module_str, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_str] = module
        spec.loader.exec_module(module)
        return getattr(module, function_name)

    def reload_classes(folder_path):
        sys.path.insert(0, folder_path)
        for file in os.listdir(folder_path):
            if file.endswith('.py'):
                module = importlib.import_module(file[:-3])
                importlib.reload(module)
        sys.path.pop(0)

    def run_tests(circuit_function, path, shots):
        with patch("__main__.deutsch_jozsa", circuit_function):
            reload_classes(path)
            tests = [
                DeutschJozsa().test_constant_one(),
                DeutschJozsa().test_constant_zero(),
                DeutschJozsa().test_nth_qubit_parity(),
                DeutschJozsa().test_odd_number_of_ones()
            ]
            return all(tests)

    PATH = dirname(os.path.abspath(""))
    algorithm_name = "deutsch_jozsa"
    mutants = [(f"m", i) for i in range(20)] + [(f"em", i) for i in range(10)]
    shots_list = [7500, 12600]

    csv_path = f"{PATH}/mutation_test_results/{algorithm_name}/{algorithm_name}_unit_tests.csv"
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    with open(csv_path, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Mutant Name", "Number of Measurements", "Result"])

        for mutant_type, index in mutants:
            mutant_name = f"{algorithm_name}_{mutant_type}{index}"
            mutant_path = f"{PATH}/{algorithm_name}/mutants/{mutant_name}.py"
            print(f"Testing mutant {mutant_name}")

            circuit_function = import_function(mutant_name, mutant_path, algorithm_name)

            for shots in shots_list:
                result = run_tests(circuit_function, f"{PATH}/{algorithm_name}", shots)
                status = "Pass" if result else "Fail"
                print(mutant_name, shots, status)
                writer.writerow([mutant_name, shots, status])