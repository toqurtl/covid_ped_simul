# coding=utf-8

"""Synthetic pedestrian behavior with social groups simulation according to the Extended Social Force model.

See Helbing and Molnár 1998 and Moussaïd et al. 2010
"""
from pysocialforce.utils import DefaultConfig
# from pysocialforce.scene import PedState, EnvState
from pysocialforce.scene import EnvState
from pysocialforce.pedstate import PedState
from pysocialforce import forces
import time

# 시뮬레이션 전체과정을 처리
# step 하나를 처리하는 모듈 => Scene의 PedState 클래스
# step이 끝나면 결과를 저장하는 모듈 => record
# step 이전 바뀌는 외부상황을 반영하는 모듈 => inspector
## 새로운 ped 추가나 사라지는 ped 판단
## 추가: self.basic_state를 관찰
## 사라짐: 

class NewSimulator(object):

    def __init__(self, state, groups=None, obstacles=None, config_file=None):
        # Config 읽어보는 부분 -> 제일 마지막에 대대적으로 수정 ㄱ
        self.config = DefaultConfig()
        if config_file:
            self.config.load_config(config_file)        
        self.scene_config = self.config.sub_config("scene")

        # 시뮬레이션 전체를 관장하는 것
        self.basic_state = state        
        self.time_step = 0

        self._initialize_obstacle(obstacles)
        self._initialize_agent(groups)
        self._initialize_force()
        return

    """초기화"""
    def _initialize_obstacle(self, obstacle_info):        
        self.env = EnvState(obstacle_info, self.config("resolution", 10.0))
        return

    def _initialize_agent(self, groups):
        """
        peds의 역할은, input을 주면 그에 맞는 output을 반환
        input: step_width, new agent 등
        output: 변화된 state
        """  
        self.peds = PedState(self.basic_state, groups, self.config)
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

    """시뮬레이션 함수"""
    def step_once(self):
        """
        1) 현재 스텝에 변화시킬 내용 탐지(new_agent, step_width, )
        2) PedEnv에 넣기
        3) 반환값 받아서 사라져야 할 놈들 처리
        4) time_step 추가
        """
        
        self.peds.step(self.compute_forces())    
        self.peds.time_step += 1
        self.time_step += 1    
    

    def set_step_width(self, step_width):
        self.peds.step_width = step_width

