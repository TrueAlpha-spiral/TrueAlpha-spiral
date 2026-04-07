PHI = 1.61803398875

class TruthSpiral:
    def __init__(self, max_depth=7):
        self.trust_score = 1.0
        self.history = []
        self.max_depth = max_depth

    def amplify(self, node: str) -> str:
        """
        Amplify the truthiness of a node.
        If the node has been seen before (cycle), return a cycle detected flag.
        Otherwise, append to history and increase trust score.
        """
        if node in self.history:
             return f"{node} [CYCLE DETECTED]"

        if len(self.history) >= self.max_depth:
            return f"{node} [DEPTH EXCEEDED]"

        self.history.append(node)
        self.trust_score *= PHI
        return node

    def reset(self):
        self.history = []
        self.trust_score = 1.0
