import importlib.util
import csv
import time
import sys
import os
import pandas as pd
from unittest.mock import patch
from qucheck.coordinator import Coordinator
from qucheck.test_runner import TestRunner
import gc
from qiskit_aer import AerSimulator

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


def run_single_test(algorithm_name, num_inputs, measurements, mutant_type, index, number_of_properties, run_optimization=True,
                    csvwriter=None):
    mutant_name = f"{algorithm_name}_{mutant_type}{index}"

    circuit_function = import_function(mutant_name,
                                       f"{PATH}/{algorithm_name}/mutants/{mutant_name}.py",
                                       algorithm_name)
    print(f"Testing {mutant_name}")

    with patch(f"case_studies.{algorithm_name}.{algorithm_name}.{algorithm_name}", circuit_function):
        reload_classes(f"{PATH}/{algorithm_name}")
        backend = AerSimulator(method='statevector')
        backend.set_options(
            max_parallel_threads = 0,
            max_parallel_experiments = 0,
            max_parallel_shots = 1,
            statevector_parallel_threshold = 8
        )

        coordinator = Coordinator(num_inputs, backend=backend)

        start = time.time()
        result = coordinator.test(f"{PATH}/{algorithm_name}", measurements, run_optimization=run_optimization, number_of_properties=number_of_properties)
        end = time.time()

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

        result_row = [mutant_name, number_of_properties, num_inputs, measurements, str(outcome), str(num_circuits_executed), str(num_unique_failed_properties),
                      str(num_failed_properties), str(failed_property_string), str(end - start)]

        if csvwriter:
            csvwriter.writerow(result_row)

        print(f"Finished testing {mutant_name}")
        return result_row


def test_and_store(algorithm_name, optimisation):
    inputs = [64, 32, 16, 8, 4]
    shots = [3200, 1600, 800, 400, 200]
    number_of_properties_list = [3, 2, 1]
    for input_val in inputs:
        for measurements in shots:
            for number_of_properties in number_of_properties_list:
                print(f"number of inputs: {input_val}, number of measurements: {measurements}, number of properties: {number_of_properties}")
                filename = f"mutation_test_results/{algorithm_name}/{algorithm_name}_{input_val}_{measurements}_{number_of_properties}_mt_results.csv"
                dir_path = os.path.dirname(filename)
                if dir_path and not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                with open(filename, 'w', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(["Mutant Name", "Number of Properties", "Number of Inputs", "Number of Measurements", "Result", "Number of Circuits Executed", "Number of Unique Failed Properties", "Number of Failed Properties", "Unique Failed Properties", "Time Taken"])
                    # Run tests for regular mutants
                    for i in range(10):
                        run_single_test(algorithm_name, input_val, measurements, "m", i, number_of_properties, run_optimization=optimisation, csvwriter=csvwriter)

                    # Run tests for equivalent mutants
                    for i in range(5):
                        run_single_test(algorithm_name, input_val, measurements, "em", i, number_of_properties, run_optimization=optimisation, csvwriter=csvwriter)


def reload_classes(folder_path):
    sys.path.insert(0, folder_path)
    for file in os.listdir(folder_path):
        if file.endswith('.py'):
            module = importlib.import_module(file[:-3])
            importlib.reload(module)
    sys.path.pop(0)


def merge_csv_files(algorithm_name):
    # Define the directory where the CSV files are stored
    directory = f"mutation_test_results/{algorithm_name}/"

    # Get all CSV files in the directory
    all_files = [os.path.join(directory, f) for f in os.listdir(directory) if
                 f.endswith('.csv') and f != f"{algorithm_name}_merged_results.csv"]

    # Read and combine all CSV files
    dataframes = []
    for file in all_files:
        df = pd.read_csv(file)
        dataframes.append(df)

    # Merge all dataframes
    if dataframes:
        merged_df = pd.concat(dataframes, ignore_index=True)

        # Save the merged results
        merged_filename = os.path.join(directory, f"{algorithm_name}_merged_results.csv")
        merged_df.to_csv(merged_filename, index=False)
        print(f"Merged results saved to {merged_filename}")

        # Delete individual CSV files
        for file in all_files:
            os.remove(file)
            print(f"Deleted: {file}")
    else:
        print(f"No CSV files found in {directory}")


# Run the test
test_and_store("quantum_fourier_transform", True)
merge_csv_files("quantum_fourier_transform")
