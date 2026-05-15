"""In-memory immutable ledger helper for bridge receipts and refusals."""

from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock
from typing import Any

from .receipts import canonical_hash


@dataclass
class ImmutableTruthLedger:
    """Append-only ledger that stores hash-linked bridge artifacts."""

    entries: list[dict[str, Any]] = field(default_factory=list)
    _lock: Lock = field(default_factory=Lock, init=False, repr=False)

    def append(self, artifact: Any) -> str:
        payload = artifact.to_dict() if hasattr(artifact, "to_dict") else dict(artifact)
        with self._lock:
            previous_hash = self.entries[-1]["entry_hash"] if self.entries else "sha256:genesis"
            entry = {"payload": payload, "previous_hash": previous_hash}
            entry_hash = canonical_hash(entry)
            entry["entry_hash"] = entry_hash
            self.entries.append(entry)
            return entry_hash
