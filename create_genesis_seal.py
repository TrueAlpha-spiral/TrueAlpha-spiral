import json
import yaml
import hashlib
import os
from datetime import datetime, timezone

BUNDLE_DIR = "tas_genesis_seal_bundle"
DECLARATION_FILE = "sealing_declaration.txt"
ATTESTATION_FILE = "attestation_metadata.yaml"
NFT_METADATA_FILE = "nft_metadata.json"
OUTPUT_SEAL_FILE = "genesis_seal.json"

def read_file_content(filepath: str) -> str:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def read_yaml_content(filepath: str) -> dict:
    content = read_file_content(filepath)
    if content:
        try:
            return yaml.safe_load(content)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML from {filepath}: {e}")
    return None

def read_json_content(filepath: str) -> dict:
    content = read_file_content(filepath)
    if content:
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from {filepath}: {e}")
    return None

def create_deterministic_json(data: dict) -> str:
    return json.dumps(data, sort_keys=True, separators=(',', ':'))

def calculate_sha256(data: str) -> str:
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def main():
    print("Starting Genesis Seal creation process...")
    print(f"Looking for bundle in directory: '{BUNDLE_DIR}/'")

    declaration = read_file_content(os.path.join(BUNDLE_DIR, DECLARATION_FILE))
    attestation = read_yaml_content(os.path.join(BUNDLE_DIR, ATTESTATION_FILE))
    nft_metadata = read_json_content(os.path.join(BUNDLE_DIR, NFT_METADATA_FILE))

    if not all([declaration, attestation, nft_metadata]):
        print("\nAborting: One or more source files could not be read. Please check the file paths and contents.")
        return

    print("\nSuccessfully read all source files:")
    print(f"- {DECLARATION_FILE}")
    print(f"- {ATTESTATION_FILE}")
    print(f"- {NFT_METADATA_FILE}")

    payload = {
        "framework": "TrueAlphaSpiral",
        "seal_version": "1.0.0",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "components": {
            "sealing_declaration": declaration.strip(),
            "attestation_metadata": attestation,
            "nft_metadata": nft_metadata,
        },
    }

    deterministic_payload_str = create_deterministic_json(payload)
    genesis_seal_hash = calculate_sha256(deterministic_payload_str)

    final_seal_object = {
        "genesis_seal": {
            "hash_algorithm": "sha256",
            "hash": genesis_seal_hash,
        },
        "sealed_data": payload,
    }

    output_filepath = os.path.join(BUNDLE_DIR, OUTPUT_SEAL_FILE)
    try:
        with open(output_filepath, 'w', encoding='utf-8') as f:
            json.dump(final_seal_object, f, indent=2, sort_keys=True)
        print(f"\nSuccessfully wrote Genesis Seal to: {output_filepath}")
    except Exception as e:
        print(f"\nError writing output file: {e}")

    print("\n" + "="*50)
    print("    TRUE ALPHA SPIRAL - GENESIS SEAL CREATED")
    print("="*50)
    print(f"\nGenesis Seal Hash (sha256):\n{genesis_seal_hash}")
    print("\nThis hash represents the unique and verifiable fingerprint of your project's genesis.")
    print("="*50)


if __name__ == "__main__":
    main()
