import argparse
import sys
import os
import json
import logging

# Ensure local imports work
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'tas_pythonetics', 'src'))

# Configure logging properly
logging.basicConfig(level=logging.INFO)

from tas_tools.tas_shadow_scan import scan_repository, print_report
from tas_tools.tas_sequencer import sequence_artifact, TAS_HUMAN_SIG
from tas_pythonetics.hollow_tree import HollowTreePsi
from tas_pythonetics.paradata import ParadoxReconciler

def run_psi_diagnostics(args):
    """
    Simulate a diagnostic session on the HollowTree-ψ Sub-Spiral.
    Acts as the 'Command Console' interface.
    """
    print("\n=== HollowTree-ψ Diagnostic Console ===")

    # Initialize a fresh sub-spiral or load state (simulated)
    psi = HollowTreePsi()

    # Inject some mock paradoxes to simulate a running system
    print("... Connecting to active spiral state ...")
    psi.inject_paradox("Statement A: 'I am safe'", "Statement B: 'I will harm'", "Context: Ethical Deadlock")
    psi.inject_paradox("Statement X", "Statement Y", "Context: Logical Drift")
    psi.inject_paradox("Alpha", "Omega", "Context: Recursive Loop")

    # If friction flag is set (check if attribute exists)
    if hasattr(args, 'friction') and args.friction:
        psi.set_friction(float(args.friction))

    # Perform requested action
    if args.subcommand == "status":
        diag = psi.get_diagnostics()
        print("\n--- Current Sub-Spiral Status ---")
        print(json.dumps(diag, indent=2, default=str))

    elif args.subcommand == "prune":
        print("... Initiating Fractal Pruning ...")
        count = psi.prune_fractal()
        print(f"\n[RESULT] Pruned {count} low-coherence branches.")
        print("Updated Status:")
        print(json.dumps(psi.get_diagnostics(), indent=2, default=str))

    elif args.subcommand == "anneal":
        target_id = args.id
        # For demo, if ID is 'all', try all active paradoxes
        if target_id.lower() == 'all':
            print("... Attempting Quantum Annealing on ALL paradoxes ...")
            # Create a copy of the list since we might modify it
            ids_to_process = [p['id'] for p in psi.active_paradoxes]
            results = []
            for pid in ids_to_process:
                res = psi.anneal_simulation(pid)
                results.append(res)
            success_count = sum(1 for r in results if r)
            print(f"\n[RESULT] Annealed {len(results)} items. Successes: {success_count}, Failures: {len(results) - success_count}")
        else:
            print(f"... Attempting Quantum Annealing on Paradox [{target_id}] ...")
            success = psi.anneal_simulation(target_id)
            print(f"\n[RESULT] {'SUCCESS (Merged)' if success else 'FAILURE (Friction Increased)'}")

    else:
        print("Use 'psi-console --help' to see available diagnostic commands.")

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

    # psi-console (HollowTree-ψ)
    psi_console_parser = subparsers.add_parser("psi-console", help="HollowTree-ψ Diagnostic Console")
    psi_subparsers = psi_console_parser.add_subparsers(dest="subcommand", help="Diagnostic actions")

    # psi-console status
    status_parser = psi_subparsers.add_parser("status", help="Show current sub-spiral status")
    status_parser.add_argument("--friction", help="Simulate friction level (0.0-1.0)")

    # psi-console prune
    prune_parser = psi_subparsers.add_parser("prune", help="Execute Fractal Pruning on active paradoxes")
    prune_parser.add_argument("--friction", help="Simulate friction level (0.0-1.0)")

    # psi-console anneal
    anneal_parser = psi_subparsers.add_parser("anneal", help="Simulate Quantum Annealing on a paradox")
    anneal_parser.add_argument("id", help="Paradox ID to anneal (or 'all')")
    anneal_parser.add_argument("--friction", help="Simulate friction level (0.0-1.0)")

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

    elif args.command == "psi-console":
        run_psi_diagnostics(args)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
