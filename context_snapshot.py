"""Content-addressed semantic context for TAS admission decisions.

The context snapshot pins the dictionary, invariant set, authority projection,
canonicalization rules, namespace, and predecessor context used to interpret a
candidate. Context and definition objects are accepted only as exact
TAS-CJSON-1 bytes; mutable aliases and non-canonical encodings fail closed.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Any, Mapping, Protocol, Sequence

CANONICALIZATION_VERSION = "TAS-CJSON-1"
CONTEXT_SCHEMA_VERSION = "tas.context-snapshot.v1"
DEFINITION_SCHEMA_VERSION = "tas.definition.v1"
CONTEXT_SNAPSHOT_DOMAIN = b"TAS-CONTEXT-SNAPSHOT-V1\x00"
CONTEXT_REGISTRY_DOMAIN = b"TAS-CONTEXT-REGISTRY-V1\x00"
DEFINITION_DOMAIN = b"TAS-DEFINITION-V1\x00"
_HEX_64 = re.compile(r"^[0-9a-f]{64}$")


class CanonicalJSONError(ValueError):
    """Raised when input is outside the constrained TAS-CJSON-1 subset."""


class ContextValidationError(ValueError):
    """Raised when semantic context or definition integrity fails."""


def _reject_duplicates(pairs: Sequence[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CanonicalJSONError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def parse_canonical_json(
    raw: bytes,
    *,
    max_bytes: int = 65536,
    max_depth: int = 32,
    max_nodes: int = 4096,
) -> Any:
    """Decode UTF-8 JSON after rejecting ambiguous and non-portable forms."""
    if not isinstance(raw, bytes) or len(raw) > max_bytes:
        raise CanonicalJSONError("JSON input exceeds byte limit")
    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=_reject_duplicates,
            parse_constant=lambda value: (_ for _ in ()).throw(
                CanonicalJSONError(f"invalid JSON constant: {value}")
            ),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise CanonicalJSONError("invalid UTF-8 JSON") from error

    nodes = 0

    def validate(item: Any, depth: int = 0) -> None:
        nonlocal nodes
        nodes += 1
        if nodes > max_nodes or depth > max_depth:
            raise CanonicalJSONError("JSON structural limit exceeded")
        if isinstance(item, float):
            raise CanonicalJSONError(
                "TAS-CJSON-1 does not permit floating point values"
            )
        if isinstance(item, int) and not -(2**53 - 1) <= item <= 2**53 - 1:
            raise CanonicalJSONError("integer outside TAS-CJSON-1 range")
        if isinstance(item, str):
            if any(0xD800 <= ord(character) <= 0xDFFF for character in item):
                raise CanonicalJSONError("Unicode surrogate not permitted")
        elif isinstance(item, Mapping):
            for key, child in item.items():
                if not isinstance(key, str):
                    raise CanonicalJSONError("JSON object key is not a string")
                validate(key, depth + 1)
                validate(child, depth + 1)
        elif isinstance(item, list):
            for child in item:
                validate(child, depth + 1)

    validate(value)
    return value


def canonical_json(value: Any) -> bytes:
    """Serialize TAS-CJSON-1 data as deterministic UTF-8 bytes."""
    provisional = json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        allow_nan=False,
    ).encode("utf-8")
    parse_canonical_json(provisional)
    return provisional


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def domain_hash(domain: bytes, value: Any) -> str:
    return hashlib.sha256(domain + canonical_json(value)).hexdigest()


def _require_hex64(value: Any, field: str) -> str:
    if not isinstance(value, str) or not _HEX_64.fullmatch(value):
        raise ContextValidationError(
            f"{field} must be a lowercase SHA-256 hex digest"
        )
    return value


def _require_nonempty_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise ContextValidationError(f"{field} must be a non-empty string")
    return value


def _validate_definition_mapping(definition: Mapping[str, Any]) -> None:
    fields = {
        "schema_version",
        "canonicalization_version",
        "namespace_id",
        "term",
        "semantic_version",
        "definition",
        "constraints",
        "supersedes",
    }
    if set(definition) != fields:
        raise ContextValidationError("invalid definition record field set")
    if definition["schema_version"] != DEFINITION_SCHEMA_VERSION:
        raise ContextValidationError("unsupported definition schema version")
    if definition["canonicalization_version"] != CANONICALIZATION_VERSION:
        raise ContextValidationError("unsupported definition canonicalization")
    _require_nonempty_string(definition["namespace_id"], "namespace_id")
    _require_nonempty_string(definition["term"], "term")
    _require_nonempty_string(definition["semantic_version"], "semantic_version")
    _require_nonempty_string(definition["definition"], "definition")
    if not isinstance(definition["constraints"], list):
        raise ContextValidationError("constraints must be an array")
    supersedes = definition["supersedes"]
    if supersedes is not None:
        _require_hex64(supersedes, "supersedes")


def definition_id_for_mapping(definition: Mapping[str, Any]) -> str:
    """Return the domain-separated identifier for a definition record."""
    _validate_definition_mapping(definition)
    return domain_hash(DEFINITION_DOMAIN, definition)


def definition_id_for_raw(raw: bytes) -> str:
    definition = parse_canonical_json(raw)
    if canonical_json(definition) != raw:
        raise ContextValidationError(
            "definition bytes are not canonical TAS-CJSON-1"
        )
    if not isinstance(definition, Mapping):
        raise ContextValidationError("definition record must be an object")
    return definition_id_for_mapping(definition)


def registry_root_for(definition_ids: Sequence[str]) -> str:
    """Commit to the exact declared order of DefinitionIDs."""
    identifiers = list(definition_ids)
    if not identifiers:
        raise ContextValidationError("definition_ids must not be empty")
    if len(set(identifiers)) != len(identifiers):
        raise ContextValidationError("definition_ids must not contain duplicates")
    for identifier in identifiers:
        _require_hex64(identifier, "definition_id")
    return domain_hash(CONTEXT_REGISTRY_DOMAIN, identifiers)


def make_definition_record(
    *,
    namespace_id: str,
    term: str,
    semantic_version: str,
    definition: str,
    constraints: Sequence[Any] = (),
    supersedes: str | None = None,
) -> dict[str, Any]:
    record = {
        "schema_version": DEFINITION_SCHEMA_VERSION,
        "canonicalization_version": CANONICALIZATION_VERSION,
        "namespace_id": namespace_id,
        "term": term,
        "semantic_version": semantic_version,
        "definition": definition,
        "constraints": list(constraints),
        "supersedes": supersedes,
    }
    _validate_definition_mapping(record)
    return record


@dataclass(frozen=True)
class ContextSnapshot:
    schema_version: str
    canonicalization_version: str
    namespace_id: str
    context_sequence: int
    registry_root: str
    definition_ids: tuple[str, ...]
    invariant_set_id: str
    authority_binding_hash: str
    parent_context_hash: str | None
    effective_epoch: int
    context_snapshot_hash: str

    @property
    def unsigned_mapping(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "canonicalization_version": self.canonicalization_version,
            "namespace_id": self.namespace_id,
            "context_sequence": self.context_sequence,
            "registry_root": self.registry_root,
            "definition_ids": list(self.definition_ids),
            "invariant_set_id": self.invariant_set_id,
            "authority_binding_hash": self.authority_binding_hash,
            "parent_context_hash": self.parent_context_hash,
            "effective_epoch": self.effective_epoch,
        }

    @property
    def mapping(self) -> dict[str, Any]:
        return {
            **self.unsigned_mapping,
            "context_snapshot_hash": self.context_snapshot_hash,
        }

    @classmethod
    def build(
        cls,
        *,
        namespace_id: str,
        context_sequence: int,
        definition_ids: Sequence[str],
        invariant_set_id: str,
        authority_binding_hash: str,
        parent_context_hash: str | None,
        effective_epoch: int,
    ) -> "ContextSnapshot":
        unsigned = {
            "schema_version": CONTEXT_SCHEMA_VERSION,
            "canonicalization_version": CANONICALIZATION_VERSION,
            "namespace_id": namespace_id,
            "context_sequence": context_sequence,
            "registry_root": registry_root_for(definition_ids),
            "definition_ids": list(definition_ids),
            "invariant_set_id": invariant_set_id,
            "authority_binding_hash": authority_binding_hash,
            "parent_context_hash": parent_context_hash,
            "effective_epoch": effective_epoch,
        }
        snapshot_hash = domain_hash(CONTEXT_SNAPSHOT_DOMAIN, unsigned)
        return cls.from_mapping({**unsigned, "context_snapshot_hash": snapshot_hash})

    @classmethod
    def from_raw(cls, raw: bytes) -> "ContextSnapshot":
        value = parse_canonical_json(raw)
        if canonical_json(value) != raw:
            raise ContextValidationError(
                "context snapshot bytes are not canonical TAS-CJSON-1"
            )
        if not isinstance(value, Mapping):
            raise ContextValidationError("context snapshot must be an object")
        return cls.from_mapping(value)

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ContextSnapshot":
        fields = {
            "schema_version",
            "canonicalization_version",
            "namespace_id",
            "context_sequence",
            "registry_root",
            "definition_ids",
            "invariant_set_id",
            "authority_binding_hash",
            "parent_context_hash",
            "effective_epoch",
            "context_snapshot_hash",
        }
        if set(value) != fields:
            raise ContextValidationError("invalid context snapshot field set")
        if value["schema_version"] != CONTEXT_SCHEMA_VERSION:
            raise ContextValidationError("unsupported context schema version")
        if value["canonicalization_version"] != CANONICALIZATION_VERSION:
            raise ContextValidationError("unsupported context canonicalization")
        namespace_id = _require_nonempty_string(
            value["namespace_id"], "namespace_id"
        )
        sequence = value["context_sequence"]
        epoch = value["effective_epoch"]
        if (
            not isinstance(sequence, int)
            or isinstance(sequence, bool)
            or sequence < 0
            or not isinstance(epoch, int)
            or isinstance(epoch, bool)
            or epoch < 0
        ):
            raise ContextValidationError(
                "context sequence and epoch must be non-negative integers"
            )
        identifiers = value["definition_ids"]
        if not isinstance(identifiers, list):
            raise ContextValidationError("definition_ids must be an array")
        definition_ids = tuple(identifiers)
        registry_root = _require_hex64(value["registry_root"], "registry_root")
        if registry_root != registry_root_for(definition_ids):
            raise ContextValidationError(
                "registry_root does not commit to definition_ids"
            )
        invariant_set_id = _require_hex64(
            value["invariant_set_id"], "invariant_set_id"
        )
        authority_binding_hash = _require_hex64(
            value["authority_binding_hash"], "authority_binding_hash"
        )
        parent = value["parent_context_hash"]
        if sequence == 0:
            if parent is not None:
                raise ContextValidationError(
                    "genesis context must have a null parent"
                )
        else:
            parent = _require_hex64(parent, "parent_context_hash")
        declared_hash = _require_hex64(
            value["context_snapshot_hash"], "context_snapshot_hash"
        )
        unsigned = {
            key: value[key]
            for key in fields
            if key != "context_snapshot_hash"
        }
        computed_hash = domain_hash(CONTEXT_SNAPSHOT_DOMAIN, unsigned)
        if declared_hash != computed_hash:
            raise ContextValidationError("context_snapshot_hash mismatch")
        return cls(
            schema_version=value["schema_version"],
            canonicalization_version=value["canonicalization_version"],
            namespace_id=namespace_id,
            context_sequence=sequence,
            registry_root=registry_root,
            definition_ids=definition_ids,
            invariant_set_id=invariant_set_id,
            authority_binding_hash=authority_binding_hash,
            parent_context_hash=parent,
            effective_epoch=epoch,
            context_snapshot_hash=declared_hash,
        )


class ContextResolver(Protocol):
    def resolve(self, *, context_snapshot_hash: str) -> bytes | None: ...

    def expected_head(self, *, namespace_id: str) -> str | None: ...


class DefinitionResolver(Protocol):
    def resolve(self, *, definition_id: str) -> bytes | None: ...


class InMemoryContextResolver:
    """Test/development resolver for snapshots and namespace heads."""

    def __init__(
        self,
        snapshots: Mapping[str, bytes],
        namespace_heads: Mapping[str, str],
    ) -> None:
        self._snapshots = dict(snapshots)
        self._namespace_heads = dict(namespace_heads)

    def resolve(self, *, context_snapshot_hash: str) -> bytes | None:
        return self._snapshots.get(context_snapshot_hash)

    def expected_head(self, *, namespace_id: str) -> str | None:
        return self._namespace_heads.get(namespace_id)


class InMemoryDefinitionResolver:
    """Test/development resolver for content-addressed definitions."""

    def __init__(self, definitions: Mapping[str, bytes]) -> None:
        self._definitions = dict(definitions)

    def resolve(self, *, definition_id: str) -> bytes | None:
        return self._definitions.get(definition_id)


def resolve_verified_context(
    *,
    context_snapshot_hash: str,
    context_resolver: ContextResolver,
    definition_resolver: DefinitionResolver,
) -> ContextSnapshot:
    """Resolve and verify an active context and every pinned definition."""
    _require_hex64(context_snapshot_hash, "context_snapshot_hash")
    raw_context = context_resolver.resolve(
        context_snapshot_hash=context_snapshot_hash
    )
    if raw_context is None:
        raise ContextValidationError("context snapshot is unavailable")
    try:
        context = ContextSnapshot.from_raw(raw_context)
    except (CanonicalJSONError, ContextValidationError) as error:
        raise ContextValidationError(
            "context snapshot validation failed"
        ) from error
    if context.context_snapshot_hash != context_snapshot_hash:
        raise ContextValidationError(
            "resolved context does not match requested hash"
        )
    expected_head = context_resolver.expected_head(
        namespace_id=context.namespace_id
    )
    if expected_head != context.context_snapshot_hash:
        raise ContextValidationError(
            "context snapshot is not the active namespace head"
        )

    for identifier in context.definition_ids:
        raw_definition = definition_resolver.resolve(definition_id=identifier)
        if raw_definition is None:
            raise ContextValidationError("pinned definition is unavailable")
        try:
            definition = parse_canonical_json(raw_definition)
            if canonical_json(definition) != raw_definition:
                raise ContextValidationError(
                    "definition bytes are not canonical TAS-CJSON-1"
                )
            if not isinstance(definition, Mapping):
                raise ContextValidationError(
                    "definition record must be an object"
                )
            _validate_definition_mapping(definition)
        except (CanonicalJSONError, ContextValidationError) as error:
            raise ContextValidationError("definition validation failed") from error
        if definition["namespace_id"] != context.namespace_id:
            raise ContextValidationError("definition namespace mismatch")
        if definition_id_for_mapping(definition) != identifier:
            raise ContextValidationError(
                "definition content does not match DefinitionID"
            )
    return context
