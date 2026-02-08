import os
import sys
import subprocess

from typing import List

# Temporary workaround for cases which currently do not support
# parallel execution.
serial_only_cases = [
    "Electromagnetics/Lubin_2015_Axial_Flux_Eddy_Current_Brake",
]


def run_cases(base_directory):

    failed_cases: List[str] = []

    # Walk through the directory structure
    for root, _, files in os.walk(top=base_directory):
        if "case.py" in files:

            # Save the current working directory
            # Note that we run the test in the local directory, so we
            # can easily load the mesh. After the run the directory is
            # restored so we can continue the os.walk.
            original_dir = os.getcwd()

            case_path = f"{root}/case.py"

            if any(case in case_path for case in serial_only_cases):
                print(f"Skipping serial-only case: {case_path}")
                continue

            print(f"Running case: {case_path}")

            # Execute the command
            try:
                os.chdir(path=root)
                args = "pymufem case.py"
                _ = subprocess.run(args=args, shell=True, check=True, text=True)
                print(f"Success: {case_path}")
            except subprocess.CalledProcessError as e:
                print(f"Error running {case_path}: {e}")
                failed_cases.append(object=case_path)
            finally:
                # Return to the original working directory
                os.chdir(path=original_dir)

    if failed_cases:
        print("\nThe following cases failed:")
        for case in failed_cases:
            print(case)
        sys.exit(status=1)


if __name__ == "__main__":

    if len(sys.argv) > 1:
        base_directory = sys.argv[1]
    else:
        base_directory = "."
    print(f"Running cases in directory: {base_directory}")

    run_cases(base_directory=base_directory)
