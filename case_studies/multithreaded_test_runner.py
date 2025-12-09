import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["QISKIT_NUM_THREADS"] = "1"

import importlib.util
import csv
import time
import sys
import pandas as pd
from unittest.mock import patch
from qucheck.coordinator import Coordinator
from qucheck.test_runner import TestRunner
import gc
from qiskit_aer import AerSimulator
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, as_completed

PATH = os.path.abspath("")
MAX_WORKERS = os.cpu_count()

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
    gc.collect()

def reload_classes(folder_path):
    sys.path.insert(0, folder_path)
    for file in os.listdir(folder_path):
        if file.endswith('.py'):
            module = importlib.import_module(file[:-3])
            importlib.reload(module)
    sys.path.pop(0)

def run_single_test(args):
    """
    Worker function. Runs in a separate process.
    Returns a result_row list.
    """
    (algorithm_name, num_inputs, measurements, mutant_type, index,
     number_of_properties, run_optimization) = args

    mutant_name = f"{algorithm_name}_{mutant_type}{index}"
    try:
        circuit_function = import_function(
            mutant_name,
            f"{PATH}/{algorithm_name}/mutants/{mutant_name}.py",
            algorithm_name
        )

        with patch(f"case_studies.{algorithm_name}.{algorithm_name}.{algorithm_name}", circuit_function):
            reload_classes(f"{PATH}/{algorithm_name}")

            # Build backend IN the worker
            backend = AerSimulator(method='statevector')
            backend.set_options(
                max_parallel_threads=1,
                max_parallel_experiments=1,
                max_parallel_shots=1,
                statevector_parallel_threshold=999999
            )

            coordinator = Coordinator(num_inputs, backend=backend)

            start = time.time()
            result = coordinator.test(
                f"{PATH}/{algorithm_name}",
                measurements,
                run_optimization=run_optimization,
                number_of_properties=number_of_properties
            )
            end = time.time()

            num_circuits_executed = result.number_circuits_executed
            failed_properties = result.failed_property
            unique_classes = []
            failed_property_string = ""
            for prop in failed_properties:
                cls = prop.property.__class__
                if cls not in unique_classes:
                    failed_property_string += cls.__name__ + " & "
                    unique_classes.append(cls)
            if failed_property_string.endswith(" & "):
                failed_property_string = failed_property_string[:-3]

            num_unique_failed_properties = len(unique_classes)
            num_failed_properties = len(failed_properties)
            outcome = "Fail" if num_failed_properties > 0 else "Pass"

            row = [
                mutant_name,
                number_of_properties,
                num_inputs,
                measurements,
                outcome,
                str(num_circuits_executed),
                str(num_unique_failed_properties),
                str(num_failed_properties),
                failed_property_string,
                f"{end - start:.3f}"
            ]
            cleanup_test_runner()
            return row

    except Exception as e:
        # Return a row that records the error
        row = [
            mutant_name,
            number_of_properties,
            num_inputs,
            measurements,
            f"ERROR: {type(e).__name__}",
            "0", "0", "0", f"{e}", "0.0"
        ]
        cleanup_test_runner()
        return row

def test_and_store_parallel(algorithm_name, optimisation):
    number_of_properties_list = [3, 2, 1]
    inputs = [64, 32, 16, 8, 4, 2, 1]
    shots = [3200, 1600, 800, 400, 200, 100, 50, 25, 12]

    experiments = []

    # experiments.append((3, 100, 4200))
    # experiments.append((3, 100, 2500))
    # experiments.append((2, 100, 4200))
    # experiments.append((2, 100, 2500))

    for n in number_of_properties_list:
        for i in inputs:
            for s in shots:
                ex = (n, i, s)
                experiments.append(ex)

    for number_of_properties, input_val, measurements in experiments:
        print(f"inputs={input_val}, shots={measurements}, properties={number_of_properties}")

        # Prepare argument list for all mutants
        tasks = []
        for i in range(20):  # regular mutants
            tasks.append((algorithm_name, input_val, measurements, "m", i,
                          number_of_properties, optimisation))
        for i in range(10):   # equivalent mutants
            tasks.append((algorithm_name, input_val, measurements, "em", i,
                          number_of_properties, optimisation))

        # Run in parallel; collect rows
        results = []
        with ProcessPoolExecutor(max_workers=MAX_WORKERS, mp_context=mp.get_context("spawn")) as ex:
            futures = [ex.submit(run_single_test, t) for t in tasks]
            for fut in as_completed(futures):
                results.append(fut.result())

        # Stable order (optional): sort by mutant name
        results.sort(key=lambda r: r[0])

        # Write CSV once (parent only)
        filename = f"mutation_test_results/{algorithm_name}/{algorithm_name}_{input_val}_{measurements}_{number_of_properties}_mt_results.csv"
        dir_path = os.path.dirname(filename)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)
        with open(filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([
                "Mutant Name", "Number of Properties", "Number of Inputs",
                "Number of Measurements", "Result", "Number of Circuits Executed",
                "Number of Unique Failed Properties", "Number of Failed Properties",
                "Unique Failed Properties", "Time Taken"
            ])
            csvwriter.writerows(results)
        print(f"Wrote {len(results)} rows → {filename}")

def merge_csv_files(algorithm_name, name_mod=None):
    directory = f"mutation_test_results/{algorithm_name}/"
    all_files = [os.path.join(directory, f) for f in os.listdir(directory)
                 if f.endswith('mt_results.csv') and not f.endswith("_merged_results.csv")]
    dataframes = [pd.read_csv(f) for f in all_files]
    if dataframes:
        merged = pd.concat(dataframes, ignore_index=True)
        merged_filename = os.path.join(
            directory,
            f"{algorithm_name}_{name_mod+'_' if name_mod else ''}merged_results.csv"
        ).replace(" _ ", "_")
        merged.to_csv(merged_filename, index=False)
        print(f"Merged results saved to {merged_filename}")
        for f in all_files:
            os.remove(f)
    else:
        print(f"No CSV files found in {directory}")


if __name__ == "__main__":
    ttake = time.time()
    # for i in ["quantum_teleportation", "quantum_fourier_transform", "grovers_algorithm", "deutsch_jozsa", "quantum_phase_estimation"]:
    # for i in ["quantum_teleportation"]:
    # for i in ["superdense_coding"]:
    for i in ["grovers_algorithm"]:
        t1 = time.time()
        test_and_store_parallel(i, True)
        print("Time taken for " + i + " with optimization: ")
        print(time.time()-t1)
        merge_csv_files(i, name_mod="correct_bits")
    print("Total time taken: " + str(time.time()-ttake))
