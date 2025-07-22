# Immutability and Obfuscation

The ledger provides a simple guard against hidden changes. Each self-test writes
its console output to `audit.log`, then stores the SHA-256 hash in `ledger/`.
Because each entry links to the previous one, any attempt to alter a prior
record becomes obvious. This immutable chain makes obfuscation impossible
without leaving visible evidence.
