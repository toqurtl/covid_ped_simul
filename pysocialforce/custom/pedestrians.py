class Pedestrians(object):
    def __init__(self):
        self.peds = {}

    def add_agent(self, agent):
        self.peds[agent.id] = agent
        
    def state(self):
        pass

