import hashlib
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass, field

from .sentient_lock import DilithiumSigner, TAS_HUMAN_SIG

# Bitfield scope definitions
SCOPE_READ = 0x01
SCOPE_WRITE = 0x02
SCOPE_ADMIN = 0x04

class InvalidDelegationError(Exception):
    pass

@dataclass
class DelegationToken:
    delegate_pubkey: str
    scope: int
    parent_signature: str
    start_time: int = field(default_factory=lambda: int(time.time()))
    end_time: int = field(default_factory=lambda: int(time.time()) + 86400) # 24h default
    revocation_hash: Optional[str] = None
    nonce: str = field(default_factory=lambda: str(time.time()))
    token_id: str = field(init=False)

    def __post_init__(self):
        self.token_id = self._generate_token_id()

    def _generate_token_id(self) -> str:
        payload = f"{self.parent_signature}:{self.delegate_pubkey}:{self.nonce}"
        return hashlib.sha256(payload.encode()).hexdigest()

    def is_valid(self, current_time: Optional[int] = None) -> bool:
        if current_time is None:
            current_time = int(time.time())
        if current_time < self.start_time or current_time > self.end_time:
            return False
        if self.revocation_hash is not None:
            return False
        return True

    def has_scope(self, required_scope: int) -> bool:
        return (self.scope & required_scope) == required_scope

    def verify_parent_signature(self, root_key: str) -> bool:
        # Recreate the payload that the parent would have signed
        # In a real system, the payload would be the delegate pubkey and other immutable fields
        payload = f"{self.delegate_pubkey}:{self.scope}:{self.start_time}:{self.end_time}"
        expected_sig = DilithiumSigner.sign(root_key.encode('utf-8'), payload.encode('utf-8'))
        return self.parent_signature == expected_sig

    @classmethod
    def issue(cls, root_key: str, delegate_pubkey: str, scope: int, validity_seconds: int = 86400) -> 'DelegationToken':
        start_time = int(time.time())
        end_time = start_time + validity_seconds
        payload = f"{delegate_pubkey}:{scope}:{start_time}:{end_time}"
        parent_signature = DilithiumSigner.sign(root_key.encode('utf-8'), payload.encode('utf-8'))

        return cls(
            delegate_pubkey=delegate_pubkey,
            scope=scope,
            parent_signature=parent_signature,
            start_time=start_time,
            end_time=end_time
        )
# Nonce: 961
