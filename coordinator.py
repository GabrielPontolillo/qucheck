import os
import importlib
import inspect
import sys

from property import Property
from test_runner import TestRunner


class Coordinator:
    def __init__(self, num_inputs):
        self.num_inputs = num_inputs
        self.property_classes = set()
        self.test_runner = None

    def get_classes(self, folder_path):
        sys.path.insert(0, folder_path)
        for file in os.listdir(folder_path):
            if file.endswith('.py'):
                module = importlib.import_module(file[:-3])
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and issubclass(obj, Property) and obj is not Property:
                        self.property_classes.add(obj)
        sys.path.pop(0)

    def test(self, path):
        self.get_classes(path)
        self.test_runner = TestRunner(self.property_classes, self.num_inputs)
        self.test_runner.run_tests()

    def print_outcomes(self):
        if self.test_runner is None:
            raise Exception("No tests have been run yet")

        print("failing properties:")
        failing_properties = self.test_runner.list_failing_properties()

        for prop_obj in self.test_runner.property_objects:
            if type(prop_obj) in failing_properties:
                print("property: ", prop_obj)
                print(self.test_runner.list_failing_inputs(prop_obj))

        print("passing properties:")
        print(self.test_runner.list_passing_properties())


