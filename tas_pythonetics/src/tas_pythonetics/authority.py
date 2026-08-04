"""External authority registry for Pythonetics transitions."""

from __future__ import annotations

from dataclasses import replace
from threading import RLock
from typing import Dict, Optional

from .core import AuthorityRecord


class AuthorityRegistry:
    """Stores externally lodged authority records; it never executes actions."""

    def __init__(self) -> None:
        self._records: Dict[str, AuthorityRecord] = {}
        self._lock = RLock()

    def register(self, record: AuthorityRecord, *, replace_existing: bool = False) -> None:
        if not record.authority_id:
            raise ValueError("authority_id must be non-empty")
        if not record.scopes:
            raise ValueError("authority record must grant at least one scope")
        if record.valid_until < record.valid_from:
            raise ValueError("authority validity window is inverted")
        try:
            key_bytes = bytes.fromhex(record.public_key_hex)
        except ValueError as exc:
            raise ValueError("authority public key must be hexadecimal") from exc
        if len(key_bytes) != 32:
            raise ValueError("Ed25519 public key must be 32 bytes")

        normalized = replace(record, public_key_hex=record.public_key_hex.lower())
        with self._lock:
            if record.authority_id in self._records and not replace_existing:
                raise ValueError(f"authority already registered: {record.authority_id}")
            self._records[record.authority_id] = normalized

    def resolve(self, authority_id: str) -> Optional[AuthorityRecord]:
        with self._lock:
            return self._records.get(authority_id)

    def revoke(self, authority_id: str, revoked_at: int) -> None:
        with self._lock:
            record = self._records.get(authority_id)
            if record is None:
                raise KeyError(authority_id)
            self._records[authority_id] = replace(record, revoked_at=revoked_at)
