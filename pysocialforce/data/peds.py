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
    
    def state_at(self, time_step):
        return self.states[time_step]

    # 확정된 이전타임 state
    @property
    def current_state(self):
        return self.states[-1]

    # 새 step을 시작할 때, 변화환 환경을 적용
    def before_step_state(self, time_step):     
        before_state = self.state_at(time_step).copy()
        visible_time_cond = self.visible_time_condition(self.time_step)                   
        visible_dis_cond = self.visible_dis_condition(before_state)
        finish_cond = np.logical_not(visible_dis_cond)
        visible_cond = np.logical_and(visible_time_cond, visible_dis_cond)        
        before_state[:, Index.visible.index] = visible_cond * 1
        before_state[:, Index.finished.index] = finish_cond        
        return before_state

        
    def visible_time_condition(self, time_step):
        before_state = self.state_at(time_step)        
        return before_state[:, Index.start_time.index] <= time_step + 1

    def visible_dis_condition(self, before_state):        
        vecs = before_state[:,4:6] - before_state[:, 0:2]        
        distance_to_target = np.array([np.linalg.norm(line) for line in vecs])
        return distance_to_target >= 0.5
        # return np.array([ped.is_visible(time_step) for ped in self.peds.values()])
        
    # 다음 스텝을 위한 input값: visible한 친구들만 반환
    def visible_state_at(self, time_step):
        whole_state = self.before_step_state(time_step)        
        # print(whole_state[self.visible_condition(time_step)])       
        return whole_state, whole_state[whole_state[:,Index.visible.index] == 1]

    def update(self, new_peds_state, time_step):
        is_updated, new_state_list = 0, []
        for ped in self.peds.values():
            check, new_state = ped.update(new_peds_state, time_step)
            new_state_list.append(new_state)
            is_updated += check

        is_updated = is_updated == len(self.peds)
        
        if is_updated:            
            self.states.append(np.array(new_state_list))
        return is_updated

