"""In-memory paradata ledger sink for tests and local bridge wiring."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class InMemoryLedger:
    records: list[Any] = field(default_factory=list)

    def append(self, record: Any) -> None:
        self.records.append(record)
