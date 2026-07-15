import os
import hashlib
import json
import logging
from datetime import datetime, timezone
import uuid
import sys

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

TAS_META_EXT = ".tasmeta.json"
TAS_HUMAN_SIG = "Russell Nordland" # Default seed if none provided

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

def sequence_artifact(filepath, h_seed=TAS_HUMAN_SIG, genome_id="TAS_GENOME_V1"):
    """
    Perform the Sequencing Ceremony on a file.

    The ceremony records provenance attribution only. It does not create or
    imply cryptographic human authorization.
    """
    if not os.path.exists(filepath):
        logger.error(f"File not found: {filepath}")
        return False

    form_id = calculate_sha256(filepath)
    if not form_id:
        return False

    # Check for previous lineage
    meta_path = filepath + TAS_META_EXT
    previous_lineage = None
    if os.path.exists(meta_path):
        try:
            with open(meta_path, 'r') as f:
                old_meta = json.load(f)
                previous_lineage = old_meta.get("lineage_id")
                logger.info(f"Found previous lineage: {previous_lineage}")
        except (OSError, json.JSONDecodeError) as exc:
            logger.warning(f"Ignoring unreadable prior metadata {meta_path}: {exc}")

    timestamp = datetime.now(timezone.utc).isoformat()
    lineage_content = f"{form_id}{previous_lineage or ''}{h_seed}{timestamp}{genome_id}"
    lineage_id = hashlib.sha256(lineage_content.encode()).hexdigest()
    cert_id = str(uuid.uuid4())

    meta = {
        "id": lineage_id,
        "type": "TasArtifact",
        "form_id": form_id,
        "genome_id": genome_id,
        "lineage_id": lineage_id,
        "parent_lineage_id": previous_lineage,
        "h_seed": h_seed,
        "cert_id": cert_id,
        "timestamp": timestamp,
        "paradata_trail": [],
        "authorization": {
            "status": "not_provided",
            "cryptographically_verified": False,
            "reason": "sequencing_ceremony_is_provenance_only"
        },
        "attestations": [
            {
                "attestor": h_seed,
                "type": "TAS_CEREMONIAL_ATTRIBUTION_V1",
                "value": "attributed_by_sequencing_ceremony",
                "cryptographic": False
            }
        ],
        "signatures": []
    }

    try:
        with open(meta_path, 'w') as f:
            json.dump(meta, f, indent=2)
            f.write("\n")
        print(f"Sequencing complete for {filepath}")
        print(f"  Form ID: {form_id}")
        print(f"  Lineage ID: {lineage_id}")
        print(f"  Cert ID: {cert_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to write metadata: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tas_sequencer.py <filepath> [h_seed] [genome_id]")
        sys.exit(1)

    filepath = sys.argv[1]
    h_seed = sys.argv[2] if len(sys.argv) > 2 else TAS_HUMAN_SIG
    genome_id = sys.argv[3] if len(sys.argv) > 3 else "TAS_GENOME_V1"

    sequence_artifact(filepath, h_seed, genome_id)
# Nonce: 171859
