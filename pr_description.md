💡 **What:**
Extracted `obj.lower()` out of the `any()` generator expression in `compute_empathy_score` within `tas_pythonetics/src/tas_pythonetics/ethics.py`.

🎯 **Why:**
Previously, `obj.lower()` was called redundantly inside the generator for every keyword iterated through from `UNETHICAL_KEYWORDS`. By hoisting the method call before the loop, we prevent $N$ redundant string allocations and conversions, resulting in a cleaner and noticeably faster execution profile.

📊 **Measured Improvement:**
Created a benchmark script `scripts/benchmark_ethics.py`.
- **Baseline (Before Optimization):** ~0.6317 seconds for 100,000 executions.
- **After Optimization:** ~0.4457 seconds for 100,000 executions.
- **Improvement:** ~29.4% reduction in execution time for processing texts with the ethics filter.
