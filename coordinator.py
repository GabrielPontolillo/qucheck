import os
import importlib
import inspect
import random
import sys
import statsmodels.stats.power as smp

from qiskit.providers.basic_provider import BasicSimulator

from QiskitPBT.property import Property
from QiskitPBT.stats.statistical_analysis_coordinator import TestExecutionStatistics
from QiskitPBT.test_runner import TestRunner


class Coordinator:
    def __init__(self, num_inputs, random_seed=None, alpha=0.01, backend=BasicSimulator()):
        self.num_inputs = num_inputs
        self.property_classes = set()
        self.test_runner = None
        self.backend = backend
        self.alpha = alpha

        # this random seed is used to generate other random seeds for the test runner, such that we can replay
        # an entire test run
        if random_seed is None:
            self.random_seed = random.randint(0, 2147483647)
        else:
            self.random_seed = random_seed

    def get_classes(self, folder_path):
        # TODO: I kind of hate this but also maybe not?
        sys.path.insert(0, folder_path)
        for file in os.listdir(folder_path):
            if file.endswith('.py'):
                module = importlib.import_module(file[:-3])
                for name, obj in inspect.getmembers(module):
                    # TODO: I'm not convinced this works (if someone creates a base property class from which more concrete property classes inherit, it will pull in the abstract class and possibly blow up)
                    if inspect.isclass(obj) and issubclass(obj, Property) and obj is not Property:
                        self.property_classes.add(obj)
        sys.path.pop(0)

    def test(self, path, measurements: int = 2000, run_optimization=True) -> TestExecutionStatistics:
        self.get_classes(path)
        print(self.property_classes)
        self.test_runner = TestRunner(self.property_classes, self.num_inputs, self.random_seed, measurements)
        return self.test_runner.run_tests(self.backend, self.alpha, run_optimization)

    def print_outcomes(self):
        if self.test_runner is None:
            raise Exception("No tests have been run yet")

        print("failing properties:")
        failing_properties = self.test_runner.list_failing_properties()

        for prop_obj in self.test_runner.property_objects:
            if type(prop_obj) in failing_properties:
                print("property: ", prop_obj)
                print(self.test_runner.list_inputs(prop_obj))

        print("passing properties:")
        print(self.test_runner.list_passing_properties())


