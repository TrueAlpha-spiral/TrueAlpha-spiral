from hashlib import sha256


def aggregate_anchors(statement: str, context: str, sources: list[str]) -> list[str]:
    anchors = []
    for source in sources:
        # Placeholder: Fetch from real APIs (e.g., Wikidata query)
        source_data = f"{statement}{context}{source}"
        anchors.append(sha256(source_data.encode()).hexdigest())
    return anchors
