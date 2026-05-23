import argparse
import sys
import os

# Ensure local imports work for tas_tools (in root) and tas_pythonetics (in tas_pythonetics/src)
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'tas_pythonetics/src'))

from tas_tools.tas_shadow_scan import scan_repository, print_report
from tas_tools.tas_sequencer import sequence_artifact, TAS_HUMAN_SIG

# Try to import tas_pythonetics modules, handle if not present (though we just added path)
try:
    from tas_pythonetics.sentient_lock import verify_kinematic_identity, PhoenixError
except ImportError:
    verify_kinematic_identity = None
    PhoenixError = None

class TASHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass

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

    # shadow-scan
    scan_parser = subparsers.add_parser(
        "shadow-scan",
        help="Scan a directory for sequenced and unsequenced artifacts",
        description="Scan a directory and classify artifacts as verified living braid entries or unsequenced noise.",
        formatter_class=TASHelpFormatter,
    )
    scan_parser.add_argument("path", nargs="?", default=".", help="Directory path to scan")

    # sequence
    seq_parser = subparsers.add_parser(
        "sequence",
        help="Create TAS metadata for an artifact",
        description="Run the sequencing ceremony for a file and emit the matching .tasmeta.json sidecar.",
        formatter_class=TASHelpFormatter,
    )
    seq_parser.add_argument("file", help="File to sequence")
    seq_parser.add_argument("--seed", default=TAS_HUMAN_SIG, help="Human Seed ID used in the metadata")
    seq_parser.add_argument("--genome", default="TAS_GENOME_V1", help="Genome ID recorded in the metadata")

    # verify-identity
    verify_parser = subparsers.add_parser(
        "verify-identity",
        help="Verify a file against the Kinematic Identity invariant",
        description="Verify a file's contents against the Prime Invariant using the provided anchor signature.",
        formatter_class=TASHelpFormatter,
    )
    verify_parser.add_argument("file", help="Path to the file to verify")
    verify_parser.add_argument("--signature", default=TAS_HUMAN_SIG, help="Human signature anchor to verify against")

    args = parser.parse_args()

    if args.command == "shadow-scan":
        print(f"Scanning: {args.path} ...")
        report = scan_repository(args.path)
        print_report(report)
        if report["noise"]:
            sys.exit(1)

    elif args.command == "sequence":
        print(f"Sequencing: {args.file} ...")
        success = sequence_artifact(args.file, args.seed, args.genome)
        if not success:
            sys.exit(1)

    elif args.command == "verify-identity":
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

            verify_kinematic_identity(content, args.signature)
            print("\n[SUCCESS] Kinematic Identity Verified.")
            print("The structural integrity holds under the Prime Invariant.")
        except PhoenixError as e:
            print(f"\n[FAILURE] PhoenixError Triggered:\n{e}")
            sys.exit(1)
        except Exception as e:
            print(f"\n[ERROR] An unexpected error occurred: {e}")
            sys.exit(1)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
# Nonce: 49877
