import numpy as np
from pysocialforce.data.ped import PedAgent

class Pedestrians(object):
    def __init__(self, json_data):
        self.peds = {}
        self.states = []
        self._initialize(json_data)
    
    def _initialize(self, json_data):
        for key, agent_data in json_data.items():
            self.peds[key] = PedAgent(agent_data)
        return
        
    
    def state_to_list(self):
        return [ped.state_to_list() for ped in self.peds.values()]
        
    def state_to_numpy(self):
        return np.array(self.state_to_list())

    def caluate_states(self):
        pass
