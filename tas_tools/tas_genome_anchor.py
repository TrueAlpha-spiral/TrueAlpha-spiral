import json
import hashlib
import os
import sys

# Define the core artifacts
CORE_ARTIFACTS = [
    "tas_pythonetics/src/tas_pythonetics/tas_pythonetics.py",
    "tas_pythonetics/src/tas_pythonetics/paradata.py",
    "tas_pythonetics/src/tas_pythonetics/recursion.py",
    "tas_pythonetics/src/tas_pythonetics/ethics.py",
    "tas_pythonetics/src/tas_pythonetics/drift_detection.py",
    "tas_pythonetics/src/tas_pythonetics/git_safety.py"
]

TAS_HUMAN_SIG = "Russell Nordland"
OUTPUT_FILE = "TAS_GENOME_ANCHOR.json"

def calculate_genome_anchor():
    lineage_ids = []

    # Read metadata for each artifact
    for artifact in CORE_ARTIFACTS:
        meta_path = artifact + ".tasmeta.json"
        if not os.path.exists(meta_path):
            print(f"Error: Missing metadata for {artifact}")
            sys.exit(1)

        try:
            with open(meta_path, "r") as f:
                meta = json.load(f)
                lid = meta.get("lineage_id")
                if not lid:
                    print(f"Error: Missing lineage_id in metadata for {artifact}")
                    sys.exit(1)
                lineage_ids.append(lid)
        except Exception as e:
            print(f"Error reading metadata for {artifact}: {e}")
            sys.exit(1)

    # Sort for determinism
    sorted_lids = sorted(lineage_ids)

    # Create the concatenated string
    concatenated = "".join(sorted_lids) + TAS_HUMAN_SIG

    # Compute the SHA-256 hash
    anchor_hash = hashlib.sha256(concatenated.encode()).hexdigest()

    print(f"Computed TAS_GENOME_ANCHOR: {anchor_hash}")

    output_data = {
        "tas_genome_anchor": anchor_hash,
        "human_sig": TAS_HUMAN_SIG,
        "constituent_lineage_ids": sorted_lids,
        "artifacts": CORE_ARTIFACTS
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output_data, f, indent=4)

    print(f"Anchor written to {OUTPUT_FILE}")

if __name__ == "__main__":
    calculate_genome_anchor()
