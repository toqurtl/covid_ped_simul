from typing import Dict, List
import numpy as np
from .ped import PedAgent
from .parameters import DataIndex as Index

class Pedestrians(object):
    def __init__(self, json_data):
        self.peds: Dict[int, PedAgent] = {}
        self.states: List[np.ndarray] = []                
        self._initialize(json_data)
    
    def _initialize(self, json_data):
        initial_state = []
        for key, agent_data in json_data.items():
            ped = PedAgent(agent_data)
            self.peds[key] = ped
            initial_state.append(ped.current_state)        
        self.states.append(np.array(initial_state))
        return
    
    @property
    def time_step(self):
        return len(self.states) - 1    

    @property
    def current_state(self):
        return self.states[-1]

    def state_at(self, time_step):
        return self.states[time_step]

    def update(self, new_peds_state, time_step):
        is_updated, new_state_list = 0, []
        for ped in self.peds.values():
            check, new_state = ped.update(new_peds_state)            
            new_state_list.append(new_state)
            is_updated += check

        is_updated = is_updated == len(self.peds)
        
        if is_updated:            
            self.states.append(np.array(new_state_list))
        return is_updated

    def check_finished(self):
        finish_state = self.current_state[:, Index.finished.index]    
        return np.sum(finish_state) == len(self.peds)

