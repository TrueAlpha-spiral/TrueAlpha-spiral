import timeit
import sys
import os

# Ensure tas_pythonetics/src is in the python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../tas_pythonetics/src'))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from tas_pythonetics.ethics import compute_empathy_score

def run_benchmark():
    text = "This is a completely safe and innocuous statement that does not trigger any of the filters." * 10

    # Run the benchmark
    num_executions = 100000

    # define a wrapper
    def test_func():
        compute_empathy_score(text)

    time_taken = timeit.timeit(test_func, number=num_executions)
    print(f"Time taken for {num_executions} executions: {time_taken:.4f} seconds")

if __name__ == "__main__":
    run_benchmark()
