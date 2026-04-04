import hashlib, pathlib, json, datetime, requests

def sha_tree(root="tas_pythonetics"):
    h = hashlib.sha256()
    for p in sorted(pathlib.Path(root).rglob("*")):
        if p.is_file():
            h.update(p.read_bytes())
    return h.hexdigest()

payload = {
    "hash": sha_tree(),
    "author": "Russell Nordland",
    "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    "version": "0.1.0",
}
# Replace with real TAS_ITL_API endpoint/token
requests.post("https://tas.itl/anchor", json=payload)
print("ITL anchor submitted:", payload["hash"])
