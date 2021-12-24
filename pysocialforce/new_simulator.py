# coding=utf-8
from pysocialforce.utils import DefaultConfig
# from pysocialforce.scene import PedState, EnvState
from pysocialforce.envstate import EnvState
from pysocialforce.pedstate import PedState
from pysocialforce import forces
from pysocialforce.data.peds import Pedestrians
from pysocialforce.update_manager import UpdateManager
import numpy as np
import json


class NewSimulator(object):

    def __init__(self, peds_info: Pedestrians, groups=None, obstacles=None, time_table=None, config_file=None):
        # Config 읽어보는 부분 -> 제일 마지막에 대대적으로 수정 ㄱ
        self.config = DefaultConfig()
        if config_file:
            self.config.load_config(config_file)        
        self.scene_config = self.config.sub_config("scene")
        
        # 시뮬레이션 전체를 관장하는 것
        self.peds_info = peds_info        
        self.time_step = 0
        
        self.peds = PedState(self.config)
        self.env = EnvState(obstacles, self.config("resolution", 10.0))

        self.time_table = time_table
        self.step_width_list = []

        self._initialize_force()
        self._initialize()
        return

    def _initialize(self):
        speed_vecs = self.peds_info.current_state[:,2:4]        
        self.initial_speeds = np.array([np.linalg.norm(s) for s in speed_vecs])        
        self.max_speeds = self.peds.max_speed_multiplier * self.initial_speeds

    def _initialize_force(self):        
        force_list = [
            forces.DesiredForce(),        
            forces.ObstacleForce(),
            forces.Myforce()           
        ]
        group_forces = []
        if self.scene_config("enable_group"):
            force_list += group_forces

        for force in force_list:
            force.init(self, self.config)
        
        self.forces = force_list
        return
    
    def set_step_width(self):
        new_step_width = 0
        if self.time_table is None:
            new_step_width = 0.133            
        else:
            try: 
                new_step_width = self.time_table[self.time_step]                
            except IndexError:
                new_step_width = 0.133            
        self.peds.step_width = new_step_width
        self.step_width_list.append(new_step_width)
        return
    def compute_forces(self):
        return sum(map(lambda x: x.get_force(), self.forces))
    
    """Properties"""    
    def get_states(self):
        # 이름 변경필요 -> 전체 결과를 뽑는거라서 peds를 쓰지 않을 것임
        return self.peds.get_states()

    def get_obstacles(self):
        return self.env.obstacles

    """시뮬레이션 함수"""
    def simulate(self):
        while True:            
            is_finished = self.step_once()

            if is_finished: 
                break
            
            if self.time_step>300:
                break
        return

    def step_once(self):
        # update_visible        
        whole_state = self.peds_info.current_state.copy()        
        whole_state = UpdateManager.update_finished(whole_state)

        # whole_state = UpdateManager.update_visible(whole_state, self.time_step)        
        visible_state = UpdateManager.get_visible(whole_state)        
                
        visible_idx = UpdateManager.get_visible_idx(whole_state)
        visible_max_speeds = self.max_speeds[visible_idx]        
        if self.check_finish():
            return True

        self.set_step_width()        
        next_group_state = None
        if len(visible_state) > 0:
            # 계산 결과를 반영하고
            next_state, next_group_state = self.do_step(visible_state, visible_max_speeds, None)            
            whole_state = UpdateManager.new_state(whole_state, next_state)
        
        # 계산안하고 등장해야 하는 애들 반영        
        whole_state = UpdateManager.update_new_peds(whole_state, self.time_step)                        
        
        # 결과 저장        
        is_updated = self.after_step(whole_state, next_group_state)
        if is_updated:            
            self.peds.time_step += 1
            self.time_step += 1
            return False
        else:
            print("update failed")
            return True

    # calculate social force and make result
    # visible state + force -> new_state
    def do_step(self, visible_state, visible_max_speeds, visible_group=None):        
        self.peds.set_state(visible_state, visible_group, visible_max_speeds)
        print(self.time_step)
        force = self.compute_forces()              
        next_state, next_group_state = self.peds.step(force, visible_state)                
        return next_state, next_group_state

    # result to data
    def after_step(self, next_state, next_group_state):
        is_updated = self.peds_info.update(next_state, next_group_state, self.time_step)        
        return is_updated

    def check_finish(self):        
        return np.sum(self.peds_info.check_finished())

    def result_to_json(self, file_path):
        result_data = {}        
        time = 0
        result_data[0] = {
            "step_width": time, 
            "states": self.peds_info.states[0].tolist()
        }
        
        for i in range(0, len(self.step_width_list)):
            time += self.step_width_list[i]
            result_data[i+1] ={
                "step_width": time,
                "states": self.peds_info.states[i+1].tolist()
            }
        
        with open(file_path, 'w') as f:
            json.dump(result_data, f, indent=4)
        return
        
        

        
    

