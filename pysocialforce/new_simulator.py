# coding=utf-8

"""Synthetic pedestrian behavior with social groups simulation according to the Extended Social Force model.

See Helbing and Molnár 1998 and Moussaïd et al. 2010
"""
from pysocialforce.utils import DefaultConfig
# from pysocialforce.scene import PedState, EnvState
from pysocialforce.scene import EnvState
from pysocialforce.pedstate import PedState
from pysocialforce import forces
from pysocialforce.data.peds import Pedestrians
import time
import numpy as np
from pysocialforce.data.parameters import DataIndex as Index

# 시뮬레이션 전체과정을 처리
# step 하나를 처리하는 모듈 => Scene의 PedState 클래스
# step이 끝나면 결과를 저장하는 모듈 => record
# step 이전 바뀌는 외부상황을 반영하는 모듈 => inspector
## 새로운 ped 추가나 사라지는 ped 판단
## 추가: self.basic_state를 관찰
## 사라짐: 

class NewSimulator(object):

    def __init__(self, peds_info: Pedestrians, groups=None, obstacles=None, config_file=None):
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

        self._initialize_force()
        return


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
    
    def compute_forces(self):
        return sum(map(lambda x: x.get_force(), self.forces))
    
    """Properties"""    
    def get_states(self):
        # 이름 변경필요 -> 전체 결과를 뽑는거라서 peds를 쓰지 않을 것임
        return self.peds.get_states()

    def get_obstacles(self):
        return self.env.obstacles

    def set_step_width(self, step_width):
        self.peds.step_width = step_width

    def update_visible(self):
        pass


    """시뮬레이션 함수"""

    def step_once(self):
        # update_visible
        whole_state, visible_state = self.before_step()
        next_state, next_group_state = self.do_step(visible_state, None)
        
        id_index = visible_state[:, Index.id.index].astype(np.int64)
        whole_state[id_index] = visible_state
        is_updated = self.after_step(whole_state, next_group_state)        
        # new_state 구하는 과정에서 에러가 없는지 확인하고 업데이트 수행
    
    def before_step(self):
        # visible state를 pool에서 뽑음        
        visible_state = self.peds_info.visible_state_at(self.time_step)        
        return visible_state

    # calculate social force and make result
    # visible state + force -> new_state
    def do_step(self, visible_state, visible_group=None):                
        self.peds.set_state(visible_state, visible_group)
        force = self.compute_forces()        
        next_state, next_group_state = self.peds.new_step(force, visible_state)        
        return next_state, next_group_state

    # result to data
    def after_step(self, next_state, next_group_state):
        is_updated = self.peds_info.update(next_state, self.time_step)
        if is_updated:            
            self.peds.time_step += 1
            self.time_step += 1
        else:
            print("Problem at simulation time:", self.time_step)
        return is_updated

    def check_finish(self):
        return np.sum(self.peds_info.visible_dis_condition(self.peds_info.current_state)) == 0

        
    

