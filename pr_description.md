🎯 **What:** Refactored `TAS_recursive_authenticate` in `tas_pythonetics.py` to extract logic into smaller helper functions and grouped configuration arguments into an `AuthorityConfig` dataclass.
💡 **Why:** The function was becoming too long and complex, taking many arguments. This improves readability and maintainability without altering functionality.
✅ **Verification:** Verified by running `python3 -m pytest` with the proper `PYTHONPATH` and checking that all 172 tests passed successfully.
✨ **Result:** Improved maintainability and modularity of the critical authentication path.
