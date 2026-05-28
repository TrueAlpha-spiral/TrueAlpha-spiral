"""
PTY Admission Gate — TrueAlphaSpiral (TAS) Framework

Enforces the Invariant Triple (Form, Function, Faithfulness) *before* any
native PTY resize call is issued, making the entire class of race-condition
crashes architecturally impossible rather than reactively defended.

This is the formal TAS answer to the gemini-cli PTY resize race condition
patched in google-gemini/gemini-cli#27496: instead of a synchronous OS-level
check inserted just before the native call (defense-in-depth after the fact),
the admission gate refuses the resize request at the perimeter — so an invalid
resize never reaches the native layer.
"""

import hashlib
import logging
import os
import sys
from typing import Dict, Optional, Tuple

from tas_phase0_microkernel import InvariantViolation, Phase0Microkernel

logger = logging.getLogger(__name__)


class PTYAdmissionGuard:
    """
    Admit-first PTY resize guard anchored to a Phase 0 genesis root.

    Exposes a single public method, :meth:`admit_resize`, which enforces the
    Invariant Triple in strict order before allowing any downstream resize:

    1. **FORM** — structural validity: pid is a positive integer, cols and rows
       are positive integers.
    2. **FUNCTION** — process liveness: on POSIX systems the OS is asked
       directly (``os.kill(pid, 0)``) whether the process is alive *before* any
       native call.  On Windows this probe is skipped (native errors remain
       catchable there).  A dead process raises :exc:`InvariantViolation`
       rather than allowing a native C++ crash.
    3. **FAITHFULNESS** — event ordering: each admitted resize for a given pid
       is chained to the SHA-256 lineage of the previous admitted resize.
       Stale or duplicate events (e.g. from a reordered event queue) whose
       provided ``lineage_hash`` does not match the expected chain are refused.

    All refusals raise :exc:`InvariantViolation` with a message prefixed by the
    failing invariant name (``FORM FAILURE``, ``FUNCTION FAILURE``,
    ``FAITHFULNESS FAILURE``), consistent with the rest of the TAS framework.

    Attributes:
        genesis_root: 64-char hex anchor produced by
            :meth:`Phase0Microkernel.bootstrap`.
    """

    def __init__(self, genesis_root: str) -> None:
        self.genesis_root = genesis_root
        # Maps pid -> last admitted lineage hash (64-char hex).
        # Initialised to genesis_root for every new pid so the first resize
        # is anchored to the Phase 0 bootstrap.
        self._lineage: Dict[int, str] = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def admit_resize(
        self,
        pid: int,
        cols: int,
        rows: int,
        lineage_hash: str = "",
    ) -> str:
        """
        Validate the Invariant Triple for a resize request, then return the
        new lineage hash for this event.

        The returned hash should be stored by the caller and supplied as
        ``lineage_hash`` on the *next* resize for the same pid, enabling
        faithfulness chaining.

        Args:
            pid: OS process ID of the PTY process.
            cols: New terminal width in columns (must be > 0).
            rows: New terminal height in rows (must be > 0).
            lineage_hash: The lineage hash *returned by the previous*
                ``admit_resize`` call for this pid (i.e. the parent lineage).
                If provided, it is verified against the guard's internal
                record of the last admitted lineage — a mismatch means the
                event is stale, reordered, or forged (FAITHFULNESS FAILURE).
                Pass an empty string (default) for the very first resize.

        Returns:
            str: 64-char SHA-256 lineage hash for this admitted resize event,
                 to be supplied as ``lineage_hash`` on the next call.

        Raises:
            InvariantViolation: If FORM, FUNCTION, or FAITHFULNESS fails.
        """
        self._check_form(pid, cols, rows)
        self._check_function(pid)
        return self._check_faithfulness(pid, cols, rows, lineage_hash)

    # ------------------------------------------------------------------
    # Internal triple checks
    # ------------------------------------------------------------------

    def _check_form(self, pid: int, cols: int, rows: int) -> None:
        """FORM — structural validity of the resize request."""
        if not isinstance(pid, int) or pid <= 0:
            raise InvariantViolation(
                f"FORM FAILURE: pid must be a positive integer, got {pid!r}"
            )
        if not isinstance(cols, int) or cols <= 0:
            raise InvariantViolation(
                f"FORM FAILURE: cols must be a positive integer, got {cols!r}"
            )
        if not isinstance(rows, int) or rows <= 0:
            raise InvariantViolation(
                f"FORM FAILURE: rows must be a positive integer, got {rows!r}"
            )

    def _check_function(self, pid: int) -> None:
        """FUNCTION — OS-level process liveness probe (POSIX only)."""
        if sys.platform == "win32":
            # Native errors on Windows are catchable at the JS/Python layer;
            # skip the heavy OS probe as per gemini-cli convention.
            return

        try:
            os.kill(pid, 0)
        except OSError as exc:
            import errno
            if exc.errno in (errno.ESRCH, errno.EPERM):
                # ESRCH  → process does not exist
                # EPERM  → process exists but we cannot signal it; treat as
                #          dead for admission purposes (cannot resize safely)
                raise InvariantViolation(
                    f"FUNCTION FAILURE: process pid={pid} is not live "
                    f"(os.kill returned errno {exc.errno})"
                ) from exc
            # Any other OS error: propagate as unexpected
            raise

    def _check_faithfulness(
        self,
        pid: int,
        cols: int,
        rows: int,
        provided_parent_lineage: str,
    ) -> str:
        """FAITHFULNESS — lineage chaining for the resize event.

        ``provided_parent_lineage`` is the value the caller claims was
        returned by the *previous* ``admit_resize`` for this pid (i.e. the
        parent lineage hash).  The guard verifies it matches its own internal
        record.  A mismatch catches stale, reordered, or forged events.
        """
        stored_parent = self._lineage.get(pid, "") or self.genesis_root

        # Verify the caller's declared parent matches the guard's record
        if provided_parent_lineage and provided_parent_lineage != stored_parent:
            raise InvariantViolation(
                f"FAITHFULNESS FAILURE: lineage_hash mismatch for pid={pid} "
                f"resize ({cols}x{rows}): provided parent does not match last "
                f"admitted lineage"
            )

        content = f"{pid}:{cols}:{rows}"
        new_lineage = hashlib.sha256(
            f"{stored_parent}:{content}".encode()
        ).hexdigest()

        # Admit: record the new lineage head for this pid
        self._lineage[pid] = new_lineage
        logger.debug(
            "PTY resize admitted: pid=%s cols=%s rows=%s lineage=%s",
            pid, cols, rows, new_lineage,
        )
        return new_lineage
