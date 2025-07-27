import asyncio
import random

class Agent:
    def __init__(self, name):
        self.name = name
        self.phi = 1.0

    async def tick(self):
        self.phi += random.uniform(-0.05, 0.02)
        self.phi = max(0, min(1, self.phi))
        return self.phi

async def orchestrate(agents, phi_min=0.95):
    while True:
        results = await asyncio.gather(*(a.tick() for a in agents))
        global_phi = sum(results) / len(results)
        if global_phi < phi_min:
            print("Φ drop detected, initiating recovery...")
        await asyncio.sleep(1)

if __name__ == "__main__":
    agents = [Agent(f"A{i}") for i in range(5)]
    asyncio.run(orchestrate(agents))
