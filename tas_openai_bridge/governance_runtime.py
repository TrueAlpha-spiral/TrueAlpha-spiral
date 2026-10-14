"""Hash-linked governance runtime events with explicit attestation projection."""

from __future__ import annotations

import copy
import hashlib
from typing import Any

from .kms import RuntimeKeyResolver
from .registry_checkpoint import canonicalize, canonical_hash

DOMAIN = b"TAS-RUNTIME-V2"
VALID_STATES = {"PAUSED", "COMMIT_AUTHORIZED", "EXECUTING", "CANCELLED"}
VALID_EVENT_TYPES = {"RESUME_DECISION", "EXECUTION_STARTED", "COMMIT_CANCELLED"}
VALID_TRANSITIONS = {
    ("PAUSED", "RESUME_DECISION", "COMMIT_AUTHORIZED"),
    ("COMMIT_AUTHORIZED", "EXECUTION_STARTED", "EXECUTING"),
    ("COMMIT_AUTHORIZED", "COMMIT_CANCELLED", "CANCELLED"),
}


def runtime_attestation_body(event: dict[str, Any]) -> dict[str, Any]:
    body = copy.deepcopy(event)
    body.pop("event_hash", None)
    body["runtime_attestation"]["runtime_signature"] = None
    return body


def runtime_signing_message(event: dict[str, Any], previous_hash: str) -> bytes:
    attestation = event["runtime_attestation"]
    digest = hashlib.sha256(canonicalize(runtime_attestation_body(event))).hexdigest()
    fields = [
        DOMAIN.decode(),
        previous_hash,
        "sha256:" + digest,
        event["decision"].get("state", ""),
        attestation["lease_id"],
        str(attestation["lease_usage_count"]),
        attestation["registry_checkpoint_hash"],
    ]
    return "|".join(fields).encode()


def final_event_hash(event: dict[str, Any]) -> str:
    body = copy.deepcopy(event)
    body.pop("event_hash", None)
    return canonical_hash(body)


class GovernanceRuntimeLedger:
    def __init__(self, runtime_resolver: RuntimeKeyResolver, runtime_key_id: str):
        if not runtime_resolver.is_trusted_runtime_key(runtime_key_id):
            raise ValueError("Runtime key is not trusted")
        self.runtime_resolver = runtime_resolver
        self.runtime_key_id = runtime_key_id
        self.current_state = "PAUSED"
        self.previous_hash = "sha256:genesis"
        self.events: list[dict[str, Any]] = []

    def commit_transition(
        self,
        *,
        event_type: str,
        next_state: str,
        decision: dict[str, Any],
        lease_id: str,
        lease_usage_count: int,
        registry_checkpoint_hash: str,
    ) -> dict[str, Any]:
        if next_state not in VALID_STATES:
            raise ValueError("Invalid resulting state")
        if event_type not in VALID_EVENT_TYPES:
            raise ValueError("Invalid event type")
        if (self.current_state, event_type, next_state) not in VALID_TRANSITIONS:
            raise ValueError("Invalid governance transition")
        event = {
            "event_type": event_type,
            "previous_state": self.current_state,
            "decision": {**decision, "state": next_state},
            "runtime_attestation": {
                "runtime_key_id": self.runtime_key_id,
                "lease_id": lease_id,
                "lease_usage_count": lease_usage_count,
                "registry_checkpoint_hash": registry_checkpoint_hash,
                "runtime_signature": None,
            },
            "previous_hash": self.previous_hash,
        }
        message = runtime_signing_message(event, self.previous_hash)
        event["runtime_attestation"]["runtime_signature"] = self.runtime_resolver.sign_runtime(
            self.runtime_key_id, message
        )
        event["event_hash"] = final_event_hash(event)
        self.events.append(event)
        self.previous_hash = event["event_hash"]
        self.current_state = next_state
        return event


def audit_event(event: dict[str, Any], resolver: RuntimeKeyResolver) -> None:
    if event["decision"]["state"] not in VALID_STATES:
        raise ValueError("Invalid audited state")
    transition = (event["previous_state"], event["event_type"], event["decision"]["state"])
    if transition not in VALID_TRANSITIONS:
        raise ValueError("Invalid audited transition")
    attestation = event["runtime_attestation"]
    if not resolver.is_trusted_runtime_key(attestation["runtime_key_id"]):
        raise ValueError("Untrusted runtime key")
    message = runtime_signing_message(event, event["previous_hash"])
    if not resolver.verify_runtime(attestation["runtime_key_id"], message, attestation["runtime_signature"]):
        raise ValueError("Invalid runtime signature")
    if event["event_hash"] != final_event_hash(event):
        raise ValueError("Invalid final event hash")
