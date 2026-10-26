"""Authority objects for separating human stewardship from conduit execution."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True)
class HumanAPIKey:
    """Represents the steward authority anchor, not the OpenAI API key."""

    key_id: str
    active: bool = True

    def validate(self) -> bool:
        return bool(self.key_id.strip()) and self.active


@dataclass(frozen=True)
class AuthorityConfig:
    """Configuration grouping optional parameters for ScopedAuthority."""

    conduit: str = "openai"
    scope: list[str] | tuple[str, ...] = ("openai.responses.create",)
    forbidden: list[str] | tuple[str, ...] = (
        "final_authority_without_receipt",
        "silent_tool_execution",
    )
    expires_at: datetime | None = None
    active: bool = True


@dataclass(frozen=True)
class ScopedAuthority:
    """Bounded conduit authority for a specific execution surface."""

    authority: str
    conduit: str = "openai"
    scope: tuple[str, ...] = ("openai.responses.create",)
    forbidden: tuple[str, ...] = (
        "final_authority_without_receipt",
        "silent_tool_execution",
    )
    expires_at: datetime | None = None
    active: bool = True

    @classmethod
    def from_iterables(
        cls,
        authority: str,
        config: AuthorityConfig | None = None,
    ) -> "ScopedAuthority":
        config = config or AuthorityConfig()
        return cls(
            authority=authority,
            conduit=config.conduit,
            scope=tuple(config.scope),
            forbidden=tuple(config.forbidden),
            expires_at=config.expires_at,
            active=config.active,
        )

    def allows(self, action: str) -> bool:
        if not self.active or self.conduit != "openai":
            return False
        if self.expires_at is not None and self.expires_at <= datetime.now(
            timezone.utc
        ):
            return False
        return action in self.scope and action not in self.forbidden
# Nonce: 148834
