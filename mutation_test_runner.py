import importlib.util
import csv
import time
import inspect
import sys
import os
from unittest.mock import patch
from QiskitPBT.coordinator import Coordinator
from QiskitPBT.test_runner import TestRunner
import gc

PATH = os.path.abspath("")


def import_function(module_str, path, function_name):
    spec = importlib.util.spec_from_file_location(module_str, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_str] = module
    spec.loader.exec_module(module)
    return getattr(module, function_name)


def cleanup_test_runner():
    TestRunner.property_classes = []
    TestRunner.property_objects = []
    TestRunner.seeds_list_dict = {}
    TestRunner.num_inputs = 0
    TestRunner.do_shrinking = None
    TestRunner.max_attempts = 0
    TestRunner.num_measurements = 0
    TestRunner.test_execution_stats = None
    gc.collect()  # Force garbage collection


def run_single_test(algorithm_name, num_inputs, measurements, mutant_type, index, run_optimization=False,
                    csvwriter=None):
    mutant_name = f"{algorithm_name}_{mutant_type}{index}"

    circuit_function = import_function(mutant_name,
                                       f"{PATH}\\case_studies\\{algorithm_name}\\mutants\\{mutant_name}.py",
                                       algorithm_name)
    print(f"Testing {mutant_name}")

    # importlib.reload(sys.modules[f'QiskitPBT.case_studies.{algorithm_name}.{algorithm_name}'])
    with patch(f"QiskitPBT.case_studies.{algorithm_name}.{algorithm_name}.{algorithm_name}", circuit_function):
        # importlib.reload(sys.modules['QiskitPBT.coordinator'])
        reload_classes(f"{PATH}\\case_studies\\{algorithm_name}")
        coordinator = Coordinator(num_inputs, 1)

        start = time.time()
        result = coordinator.test(f"{PATH}\\case_studies\\{algorithm_name}", measurements, run_optimization=run_optimization)
        end = time.time()

        # reload_classes(f"{PATH}\\case_studies\\{algorithm_name}")
        num_circuits_executed = result.number_circuits_executed
        failed_properties = result.failed_property
        unique_properties = []
        failed_property_string = ""
        for property in failed_properties:
            if property.property.__class__ not in unique_properties:
                failed_property_string += property.property.__class__.__name__ + " & "
                unique_properties.append(property.property.__class__)
        failed_property_string = failed_property_string[:-3]
        num_unique_failed_properties = len(unique_properties)
        num_failed_properties = len(failed_properties)
        outcome = "Fail" if num_failed_properties > 0 else "Pass"

        result_row = [mutant_name, str(outcome), str(num_circuits_executed), str(num_unique_failed_properties),
                      str(num_failed_properties), str(failed_property_string), str(end - start)]

        if csvwriter:
            csvwriter.writerow(result_row)

        print(f"Finished testing {mutant_name}")
        return result_row


def test_and_store(algorithm_name, optimisation):
    inputs = [100, 50, 25]
    shots = [2000, 1000, 500]
    for input_val in inputs:
        for measurements in shots:
            print(f"number of inputs: {input_val}, number of measurements: {measurements}")
            filename = f"mutation_test_results/{algorithm_name}/{algorithm_name}_{input_val}_{measurements}_mt_results.csv"
            dir_path = os.path.dirname(filename)
            if dir_path and not os.path.exists(dir_path):
                os.makedirs(dir_path)
            with open(filename, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(["Mutant Name", "Result", "Number of Circuits Executed", "Number of Unique Failed Properties", "Number of Failed Properties", "Unique Failed Properties", "Time Taken"])

                # Run tests for regular mutants
                for i in range(10):
                    run_single_test(algorithm_name, input_val, measurements, "m", i, run_optimization=optimisation, csvwriter=csvwriter)

                # Run tests for equivalent mutants
                for i in range(5):
                    run_single_test(algorithm_name, input_val, measurements, "em", i, run_optimization=optimisation, csvwriter=csvwriter)


def reload_classes(folder_path):
    # TODO: I kind of hate this but also maybe not?
    sys.path.insert(0, folder_path)
    for file in os.listdir(folder_path):
        if file.endswith('.py'):
            module = importlib.import_module(file[:-3])
            importlib.reload(module)
    sys.path.pop(0)


# Run the test
# test_and_store("quantum_teleportation")

test_and_store("quantum_fourier_transform", False)
