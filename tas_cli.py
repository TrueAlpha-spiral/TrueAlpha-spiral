import argparse
import sys
import os
import json

# Ensure local imports work for tas_tools (in root) and tas_pythonetics (in tas_pythonetics/src).
# Anchored to the script's own directory rather than os.getcwd() to prevent CWD-based module
# import hijacking: an attacker who controls the working directory cannot shadow legitimate
# modules by placing a same-named .py file there.
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCRIPT_DIR)
sys.path.insert(1, os.path.join(_SCRIPT_DIR, 'tas_pythonetics/src'))

from tas_tools.tas_shadow_scan import scan_repository, print_report
from tas_tools.tas_sequencer import sequence_artifact, calculate_sha256, TAS_HUMAN_SIG, TAS_META_EXT
from core.authority import AuthoritySnapshot
from core.runtime import SovereignRuntime
from core.semantics import ContextSnapshot
from core.vertical_slice import CanonicalVerticalSlice
from core.wakechain import WakeChain

# Try to import tas_pythonetics modules, handle if not present (though we just added path)
try:
    from tas_pythonetics.sentient_lock import verify_kinematic_identity, PhoenixError
except ImportError:
    verify_kinematic_identity = None
    PhoenixError = None

class TASHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass

def _handle_shadow_scan(args):
    print(f"Scanning: {args.path} ...")
    report = scan_repository(args.path)
    print_report(report)
    if report["noise"]:
        sys.exit(1)

def _setup_shadow_scan_parser(subparsers):
    scan_parser = subparsers.add_parser(
        "shadow-scan",
        help="Scan a directory for sequenced and unsequenced artifacts",
        description="Scan a directory and classify artifacts as verified living braid entries or unsequenced noise.",
        formatter_class=TASHelpFormatter,
    )
    scan_parser.add_argument("path", nargs="?", default=".", help="Directory path to scan")
    scan_parser.set_defaults(func=_handle_shadow_scan)

def _handle_sequence(args):
    print(f"Sequencing: {args.file} ...")
    success = sequence_artifact(args.file, args.seed, args.genome)
    if not success:
        sys.exit(1)

def _setup_sequence_parser(subparsers):
    seq_parser = subparsers.add_parser(
        "sequence",
        help="Create TAS metadata for an artifact",
        description="Run the sequencing ceremony for a file and emit the matching .tasmeta.json sidecar.",
        formatter_class=TASHelpFormatter,
    )
    seq_parser.add_argument("file", help="File to sequence")
    seq_parser.add_argument("--seed", default=TAS_HUMAN_SIG, help="Human Seed ID used in the metadata")
    seq_parser.add_argument("--genome", default="TAS_GENOME_V1", help="Genome ID recorded in the metadata")
    seq_parser.set_defaults(func=_handle_sequence)


def _load_sidecar_metadata(target_file):
    meta_path = target_file + TAS_META_EXT
    if not os.path.exists(meta_path):
        raise PhoenixError(f"Missing TAS sidecar anchor: {meta_path}")

    with open(meta_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)

    required_fields = {"form_id", "lineage_id", "h_seed", "timestamp", "signatures"}
    missing = sorted(required_fields - metadata.keys())
    if missing:
        raise PhoenixError(f"Malformed TAS sidecar anchor: missing {', '.join(missing)}")

    current_form_id = calculate_sha256(target_file)
    if current_form_id != metadata.get("form_id"):
        raise PhoenixError(
            "Sovereign Structural Violation: sidecar form_id does not match "
            f"current artifact hash ({current_form_id})."
        )

    if not metadata.get("lineage_id"):
        raise PhoenixError("Malformed TAS sidecar anchor: empty lineage_id")

    return meta_path, metadata

def _handle_verify_identity(args):
    if verify_kinematic_identity is None:
        print("Error: tas_pythonetics module not found or failed to load.")
        sys.exit(1)

    target_file = args.file
    print(f"Verifying Kinematic Identity for: {target_file}")
    print(f"Anchor Signature: {args.signature}")

    if not os.path.exists(target_file):
        print(f"Error: File not found: {target_file}")
        sys.exit(1)

    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            content = f.read()

        meta_path, metadata = _load_sidecar_metadata(target_file)
        anchor_signature = args.signature or metadata["h_seed"]
        verify_kinematic_identity(content, anchor_signature)
        print("\n[SUCCESS] Kinematic Identity Verified.")
        print("The structural integrity holds under the Prime Invariant.")
        print(f"Sidecar Anchor: {meta_path}")
        print(f"ITL Lineage: {metadata['lineage_id']}")
    except PhoenixError as e:
        print(f"\n[FAILURE] PhoenixError Triggered:\n{e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")
        sys.exit(1)

def _setup_verify_identity_parser(subparsers):
    verify_parser = subparsers.add_parser(
        "verify-identity",
        help="Verify a file against the Kinematic Identity invariant",
        description="Verify a file's contents against the Prime Invariant and its .tasmeta.json sidecar anchor.",
        formatter_class=TASHelpFormatter,
    )
    verify_parser.add_argument("file", help="Path to the file to verify")
    verify_parser.add_argument("--signature", default=TAS_HUMAN_SIG, help="Human signature anchor to verify against")
    verify_parser.set_defaults(func=_handle_verify_identity)


def _handle_vertical_slice(args):
    timestamp = args.timestamp
    authority = AuthoritySnapshot.create(
        principal=args.principal,
        credential_reference=args.credential_reference,
        permitted_scope=[args.operation],
        effective_epoch=args.effective_epoch,
        expiry_epoch=args.expiry_epoch,
        jurisdiction=args.jurisdiction,
        revocation_condition=args.revocation_condition,
    )
    context = ContextSnapshot.create(
        namespace=args.namespace,
        epoch=args.effective_epoch,
        definition_ids=[],
        invariant_set=args.invariant or ["PRIME_INVARIANT"],
        authority_binding=authority.snapshot_id,
    )
    wakechain = WakeChain.start(author=args.principal)
    runtime = (
        SovereignRuntime(lambda *_a, **_k: None, vocab_size=max(args.runtime_vocab, 1), valid_threshold=args.runtime_valid_threshold)
        if args.enable_runtime else None
    )
    outcome = CanonicalVerticalSlice().execute(
        origin=args.origin,
        operation=args.operation,
        authority=authority,
        context=context,
        wakechain=wakechain,
        runtime=runtime,
        timestamp=timestamp,
        required_invariants=tuple(args.invariant or ["PRIME_INVARIANT"]),
    )
    print(json.dumps(outcome.to_dict(), indent=2, sort_keys=True))
    if not outcome.admitted:
        sys.exit(1)


def _setup_vertical_slice_parser(subparsers):
    parser = subparsers.add_parser(
        "vertical-slice",
        help="Run the canonical TAS vertical slice",
        description="Execute Authority -> Context -> Admission -> TASGene -> WakeChain -> Runtime -> Receipt/Refusal.",
        formatter_class=TASHelpFormatter,
    )
    parser.add_argument("--origin", required=True, help="Origin intent for the transition")
    parser.add_argument("--operation", required=True, help="Operation under evaluation")
    parser.add_argument("--principal", default=TAS_HUMAN_SIG, help="Authority principal")
    parser.add_argument("--credential-reference", default="key:tas-cli", help="Opaque credential reference")
    parser.add_argument("--effective-epoch", default="2026-01-01T00:00:00Z", help="Authority/context effective epoch")
    parser.add_argument("--expiry-epoch", default="2027-01-01T00:00:00Z", help="Authority expiry epoch")
    parser.add_argument("--jurisdiction", default="TAS", help="Authority jurisdiction")
    parser.add_argument("--revocation-condition", default="Written revocation by principal", help="Authority revocation condition")
    parser.add_argument("--namespace", default="TAS-SDF", help="Context namespace")
    parser.add_argument("--invariant", action="append", help="Required invariant (repeatable)")
    parser.add_argument("--timestamp", default=None, help="Evaluation timestamp (ISO 8601)")
    parser.add_argument("--enable-runtime", action="store_true", help="Run runtime boundary projection")
    parser.add_argument("--runtime-vocab", type=int, default=128, help="Runtime vocabulary size")
    parser.add_argument("--runtime-valid-threshold", type=int, default=16, help="Runtime valid token threshold")
    parser.set_defaults(func=_handle_vertical_slice)


def main():
    parser = argparse.ArgumentParser(
        description="TAS CLI: TrueAlphaSpiral Toolkit",
        epilog=(
            "Examples:\n"
            "  python tas_cli.py shadow-scan .\n"
            "  python tas_cli.py sequence README.md\n"
            "  python tas_cli.py verify-identity README.md --signature 'Russell Nordland'"
        ),
        formatter_class=TASHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    _setup_shadow_scan_parser(subparsers)
    _setup_sequence_parser(subparsers)
    _setup_verify_identity_parser(subparsers)
    _setup_vertical_slice_parser(subparsers)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
# Nonce: 107980
