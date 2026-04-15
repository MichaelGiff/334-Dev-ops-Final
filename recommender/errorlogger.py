import csv
import os
import re
import subprocess
import time
from datetime import datetime


LOG_FILE = "build_log.csv"


def ensure_log_file_exists():
    
  #  Create the CSV file with headers if it does not already exist.
 
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                "timestamp",
                "status",
                "tests_run",
                "failures",
                "runtime_seconds",
                "error_message"
            ])


def parse_pytest_output(output_text):
   
  #  Parse pytest output to estimate tests run and failures.

    tests_run = 0
    failures = 0

    summary_match = re.search(r"(\d+)\s+passed", output_text)
    if summary_match:
        tests_run += int(summary_match.group(1))

    failed_match = re.search(r"(\d+)\s+failed", output_text)
    if failed_match:
        failed_count = int(failed_match.group(1))
        failures += failed_count
        tests_run += failed_count

    return tests_run, failures


def log_result(status, tests_run, failures, runtime_seconds, error_message=""):
    """
    Append a test/build result row to the CSV log.
    """
    ensure_log_file_exists()

    with open(LOG_FILE, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            datetime.now().isoformat(),
            status,
            tests_run,
            failures,
            round(runtime_seconds, 3),
            error_message.strip()
        ])


def run_tests_and_log():
 
 #  Run pytest, log results to CSV, and return pytest's exit code.
  
    start_time = time.time()

    result = subprocess.run(
        ["pytest", "-v"],
        capture_output=True,
        text=True
    )

    runtime_seconds = time.time() - start_time
    combined_output = result.stdout + "\n" + result.stderr
    tests_run, failures = parse_pytest_output(combined_output)

    status = "passed" if result.returncode == 0 else "failed"

    error_message = ""
    if result.returncode != 0:
        error_message = result.stderr if result.stderr.strip() else result.stdout

    log_result(
        status=status,
        tests_run=tests_run,
        failures=failures,
        runtime_seconds=runtime_seconds,
        error_message=error_message
    )

    print(result.stdout)
    if result.stderr:
        print(result.stderr)

    return result.returncode


if __name__ == "__main__":
    raise SystemExit(run_tests_and_log())