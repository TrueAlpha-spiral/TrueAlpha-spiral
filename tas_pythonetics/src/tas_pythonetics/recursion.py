PHI = 1.61803398875

class TruthSpiral:
    def __init__(self):
        self.trust_score = 1.0

    def amplify(self, node: str) -> str:
        # toy implementation
        self.trust_score *= PHI
        return node
