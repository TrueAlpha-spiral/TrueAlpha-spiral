import os
import hashlib
import json
import logging
from datetime import datetime, timezone

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

TAS_META_EXT = ".tasmeta.json"
IGNORED_DIRS = {".git", "__pycache__", ".venv", ".idea", ".vscode", "tas_tools"} # Basic ignores

def calculate_sha256(filepath):
    """
    Compute SHA-256 hash of file content.
    """
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while True:
                data = f.read(65536)
                if not data:
                    break
                sha256.update(data)
        return sha256.hexdigest()
    except Exception as e:
        logger.error(f"Error reading file {filepath}: {e}")
        return None

def scan_repository(root_dir):
    """
    Walk the repository and classify artifacts.
    """
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "living_braid": [],
        "noise": [],
        "errors": []
    }

    for root, dirs, files in os.walk(root_dir):
        # Filter ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        for filename in files:
            if filename.endswith(TAS_META_EXT):
                continue # Skip metadata files themselves

            # Skip hidden files
            if filename.startswith("."):
                continue

            filepath = os.path.join(root, filename)
            meta_path = filepath + TAS_META_EXT

            form_id = calculate_sha256(filepath)
            if not form_id:
                # If we can't read/hash it, skip
                continue

            artifact_info = {
                "path": filepath,
                "form_id": form_id
            }

            if os.path.exists(meta_path):
                try:
                    with open(meta_path, 'r') as f:
                        meta = json.load(f)

                    # Basic validation: check if form_id matches
                    if meta.get("form_id") == form_id:
                        artifact_info["meta"] = meta
                        report["living_braid"].append(artifact_info)
                    else:
                        artifact_info["error"] = "Form ID mismatch (file changed since sequencing)"
                        report["noise"].append(artifact_info)

                except Exception as e:
                    artifact_info["error"] = f"Invalid metadata: {e}"
                    report["noise"].append(artifact_info)
            else:
                artifact_info["error"] = "Missing metadata"
                report["noise"].append(artifact_info)

    return report

def print_report(report):
    print("\n=== TAS Shadow Scan Report ===")
    print(f"Timestamp: {report['timestamp']}")

    print(f"\n[Living Braid] - Verified Artifacts: {len(report['living_braid'])}")
    for item in report['living_braid']:
        print(f"  ✓ {item['path']} (ID: {item['form_id'][:8]}...)")

    print(f"\n[Noise] - Unsequenced / Drifted Artifacts: {len(report['noise'])}")
    for item in report['noise']:
        print(f"  ✗ {item['path']} - Reason: {item.get('error', 'Unknown')}")

    if report["errors"]:
        print(f"\n[Errors] - Could not process: {len(report['errors'])}")
        for err in report["errors"]:
            print(f"  ! {err}")

    print("\n==============================")

if __name__ == "__main__":
    import sys
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    scan_result = scan_repository(target_dir)
    print_report(scan_result)
