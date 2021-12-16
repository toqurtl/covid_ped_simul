# coding=utf-8

"""Synthetic pedestrian behavior with social groups simulation according to the Extended Social Force model.

See Helbing and Molnár 1998 and Moussaïd et al. 2010
"""
from pysocialforce.utils import DefaultConfig
from pysocialforce.scene import PedState, EnvState
from pysocialforce import forces
import time

# 시뮬레이션 전체과정을 처리
# step 하나를 처리하는 모듈 => Scene의 PedState 클래스
# step이 끝나면 결과를 저장하는 모듈 => record
# step 이전 바뀌는 외부상황을 반영하는 모듈 => inspector
## 새로운 ped 추가나 사라지는 ped 판단
## 추가: self.basic_state를 관찰
## 사라짐: 

class Simulator:

    def __init__(self, state, groups=None, obstacles=None, config_file=None):
        # Config 읽어보는 부분 -> 제일 마지막에 대대적으로 수정 ㄱ
        self.config = DefaultConfig()
        if config_file:
            self.config.load_config(config_file)
        # TODO: load obstacles from config
        self.scene_config = self.config.sub_config("scene")

        # 시뮬레이션 전체를 관장하는 것
        self.basic_state = state

        # initiate obstacles
        self.env = EnvState(obstacles, self.config("resolution", 10.0))

        # initiate agents
        self.peds = PedState(state, groups, self.config)

        # construct forces
        self.myforce = forces.Myforce()
        self.myforce.init(self, self.config)
        self.forces = self.make_forces(self.config)        
        self.time_step = 0
        

    def make_forces(self, force_configs):
        """Construct forces"""
        force_list = [
            forces.DesiredForce(),
            # forces.SocialForce(),
            forces.ObstacleForce(),
            # forces.PedRepulsiveForce(),
            # forces.SpaceRepulsiveForce(),
            # forces.GoalAttractiveForce(), 
            forces.Myforce()           
        ]
        group_forces = [
            # forces.GroupCoherenceForceAlt(),
            # forces.GroupRepulsiveForce(),
            # forces.GroupGazeForceAlt(),
        ]
        if self.scene_config("enable_group"):
            force_list += group_forces

        # initiate forces
        for force in force_list:
            force.init(self, force_configs)

        return force_list

    def compute_forces(self):
        """compute forces"""
        basic_force = sum(map(lambda x: x.get_force(), self.forces))      
        return basic_force
        
    def get_states(self):
        """Expose whole state"""
        return self.peds.get_states()

    def get_length(self):
        """Get simulation length"""
        return len(self.get_states()[0])

    def get_obstacles(self):
        return self.env.obstacles

    def step_once(self):
        """step once"""
        self.peds.step(self.compute_forces())
        self.time_step += 1
        self.peds.time_step += 1
        
    def step(self, n=1):
        """Step n time"""
        for _ in range(n):
            self.step_once()
        return self

    def set_step_width(self, step_width):
        self.peds.step_width = step_width

    def set_ped_states(self):
        pass
