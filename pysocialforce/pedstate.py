"""This module tracks the state odf scene and scen elements like pedestrians, groups and obstacles"""
from typing import List
import numpy as np
from pysocialforce.utils import stateutils
from pysocialforce.custom.utils import CustomUtils
from cps.bayesian.model import BayesianModel
from pysocialforce.custom.inspector import add_agent

"""계산기로 변경"""

class PedState:
    """Tracks the state of pedstrains and social groups"""

    def __init__(self, config):
        self.default_tau = config("tau", 0.5)
        self.step_width = config("step_width", 0.133)
        self.agent_radius = config("agent_radius", 0.35)
        self.max_speed_multiplier = config("max_speed_multiplier", 1.3)

        self.max_speeds = None
        self.initial_speeds = None

        self.current_state = None

        self.ped_states = []
        self.group_states = []

        self.time_step = 0
        # self.update(state, groups)

    def set_state(self, state, groups):
        self.current_state = state               
        self.initial_speeds = self.speeds()        
        self.max_speeds = self.max_speed_multiplier * self.initial_speeds        
        self.groups = groups
    
    @property
    def state(self):
        return self.current_state

    def get_states(self):
        return np.stack(self.ped_states), self.group_states

    def size(self) -> int:
        return self.state.shape[0]

    def pos(self) -> np.ndarray:
        return self.state[:, 0:2]

    def vel(self) -> np.ndarray:
        return self.state[:, 2:4]

    def goal(self) -> np.ndarray:
        return self.state[:, 4:6]

    def visible(self):
        return self.state[7:8]

    def tau(self):
        return self.state[:, 9:10]

    def speeds(self):
        """Return the speeds corresponding to a given state."""
        return stateutils.speeds(self.state)

    def step(self, force, groups=None):
        """Move peds according to forces"""
        # desired velocity        
        desired_velocity = self.vel() + self.step_width * force
        desired_velocity = self.capped_velocity(desired_velocity, self.max_speeds)
        # stop when arrived
        desired_velocity[stateutils.desired_directions(self.state)[1] < 0.5] = [0, 0]

        # update state
        next_state = self.state
        next_state[:, 0:2] += desired_velocity * self.step_width
        next_state[:, 2:4] = desired_velocity
        next_groups = self.groups
        if groups is not None:
            next_groups = groups
        
        self.update(next_state, next_groups)

    def new_step(self, force, visible_state, group_state=None):
        # desired velocity
        desired_velocity = self.vel() + self.step_width * force
        desired_velocity = self.capped_velocity(desired_velocity, self.max_speeds)
        # stop when arrived
        desired_velocity[stateutils.desired_directions(self.state)[1] < 0.5] = [0, 0]        
        visible_state[:, 0:2] += desired_velocity * self.step_width        
        visible_state[:, 2:4] = desired_velocity
        
        next_group_state = self.groups if group_state is None else group_state

        return visible_state, next_group_state
        

    # def initial_speeds(self):
    #     return stateutils.speeds(self.ped_states[0])

    # 나중에 그룹도 처리해야함
    def add_agent_to_state(self, new_agent_state):
        next_state = self.state        
        next_state, speed = add_agent(next_state, np.array(new_agent_state))
        self.initial_speeds = speed
        
    def desired_directions(self):
        return stateutils.desired_directions(self.state)[0]

    @staticmethod
    def capped_velocity(desired_velocity, max_velocity):
        """Scale down a desired velocity to its capped speed."""
        
        desired_speeds = np.linalg.norm(desired_velocity, axis=-1)
        factor = np.minimum(1.0, max_velocity / desired_speeds)
        factor[desired_speeds == 0] = 0.0
        return desired_velocity * np.expand_dims(factor, -1)

    @property
    def groups(self) -> List[List]:
        return self._groups

    @groups.setter
    def groups(self, groups: List[List]):
        if groups is None:
            self._groups = []
        else:
            self._groups = groups
        self.group_states.append(self._groups.copy())

    def has_group(self):
        return self.groups is not None

    # def get_group_by_idx(self, index: int) -> np.ndarray:
    #     return self.state[self.groups[index], :]

    def which_group(self, index: int) -> int:
        """find group index from ped index"""
        for i, group in enumerate(self.groups):
            if index in group:
                return i
        return -1

    # add_function
    def distance_matrix(self):
        return CustomUtils.get_distance_matrix(self)     

    def angle_matrix(self):
        return CustomUtils.get_angle_matrix(self)

    def desired_social_distance(self):
        return self.peds.state[:, -1:]  

    def in_desired_distance(self):
        distance_mat = self.distance_matrix(self)
        desired_social_distance = self.state[:, -1:]        
        in_desired_distance = distance_mat < desired_social_distance
        np.fill_diagonal(in_desired_distance, False)
        in_desired_distance = in_desired_distance.astype(int)
        return in_desired_distance
