import hashlib, pathlib, json, datetime, requests, os

def sha_tree(root="tas_pythonetics"):
    h = hashlib.sha256()
    for p in sorted(pathlib.Path(root).rglob("*")):
        if p.is_file():
            h.update(p.read_bytes())
    return h.hexdigest()

payload = {
    "hash": sha_tree(),
    "author": "Russell Nordland",
    "timestamp": datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None).isoformat() + "Z",
    "version": "0.1.0",
}
token = os.environ.get("TAS_ITL_API_TOKEN")
if not token:
    raise ValueError("TAS_ITL_API_TOKEN environment variable is required but not set.")
headers = {"Authorization": f"Bearer {token}"}
# Replace with real TAS_ITL_API endpoint/token
response = requests.post("https://tas.itl/anchor", json=payload, headers=headers, timeout=10)
response.raise_for_status()
print("ITL anchor submitted:", payload["hash"])
# Nonce: 10875
