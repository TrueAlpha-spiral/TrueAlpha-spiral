import argparse
import sys
import os

# Ensure local imports work
sys.path.append(os.getcwd())

from tas_tools.tas_shadow_scan import scan_repository, print_report
from tas_tools.tas_sequencer import sequence_artifact, TAS_HUMAN_SIG

def main():
    parser = argparse.ArgumentParser(description="TAS CLI: TrueAlphaSpiral Toolkit")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # shadow-scan
    scan_parser = subparsers.add_parser("shadow-scan", help="Scan repository for unsequenced artifacts")
    scan_parser.add_argument("path", nargs="?", default=".", help="Path to scan")

    # sequence
    seq_parser = subparsers.add_parser("sequence", help="Perform Sequencing Ceremony on an artifact")
    seq_parser.add_argument("file", help="File to sequence")
    seq_parser.add_argument("--seed", default=TAS_HUMAN_SIG, help="Human Seed ID")
    seq_parser.add_argument("--genome", default="TAS_GENOME_V1", help="Genome ID")

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

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
