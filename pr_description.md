💡 **What:**
Optimized the tight loop in `find_nonce.py` by pre-computing the SHA256 state of the base content (`base_content + "# Nonce: "`). Inside the loop, it now copies this hasher state and only hashes the dynamically changing parts (the string representation of the `nonce` and the `\n{TAS_HUMAN_SIG}` suffix).

🎯 **Why:**
The previous implementation repeatedly concatenated the string and hashed the entire content of the file (including the static base content) on every iteration of the while loop. This was unnecessary and very computationally heavy, especially for larger files.

📊 **Measured Improvement:**
Running a benchmark with the `find_nonce.py` script as input content:
- **Original:** `0.2344s`
- **Optimized:** `0.0549s`
- **Speedup:** `~4.27x`

For much larger files, the speedup gets even better (~18x speedup measured in an extended content benchmark because large portions of strings aren't being continually re-hashed).
