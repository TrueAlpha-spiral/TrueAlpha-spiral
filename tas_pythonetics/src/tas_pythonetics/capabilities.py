"""Capability registry and transactional effector contracts."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from threading import RLock
from typing import Any, Callable, Dict, Mapping, Optional


class PreparationRejected(RuntimeError):
    """Preparation was rejected before any protected effect occurred."""


class CommitRejected(RuntimeError):
    """Commit was rejected and the effector guarantees no protected effect occurred."""


class TwoPhaseEffector(ABC):
    """
    Per-transition capability instance.

    ``prepare`` may stage reversible local state but must not create a protected
    external effect. ``CommitRejected`` is the only commit failure that permits
    the runtime to emit REFUSED. Any other commit exception is treated as an
    uncertain outcome and halts further execution pending reconciliation.
    """

    @abstractmethod
    def prepare(self, parameters: Mapping[str, Any]) -> bool:
        """Stage and validate the effect without changing protected state."""

    @abstractmethod
    def commit(self) -> Mapping[str, Any]:
        """Atomically commit the staged effect and return a canonicalizable result."""

    @abstractmethod
    def rollback(self) -> None:
        """Clear uncommitted staged state."""


@dataclass(frozen=True)
class CapabilityBinding:
    action_id: str
    required_scope: str
    factory: Callable[[], TwoPhaseEffector]


class CapabilityRegistry:
    """Resolves admitted action identifiers to internal capability factories."""

    def __init__(self) -> None:
        self._registry: Dict[str, CapabilityBinding] = {}
        self._lock = RLock()

    def register(
        self,
        action_id: str,
        required_scope: str,
        factory: Callable[[], TwoPhaseEffector],
        *,
        replace_existing: bool = False,
    ) -> None:
        if not action_id or not required_scope:
            raise ValueError("action_id and required_scope must be non-empty")
        if not callable(factory):
            raise TypeError("factory must be callable")

        binding = CapabilityBinding(action_id, required_scope, factory)
        with self._lock:
            if action_id in self._registry and not replace_existing:
                raise ValueError(f"capability already registered: {action_id}")
            self._registry[action_id] = binding

    def resolve(self, action_id: str) -> Optional[CapabilityBinding]:
        with self._lock:
            return self._registry.get(action_id)
