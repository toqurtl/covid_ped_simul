"""This module tracks the state odf scene and scen elements like pedestrians, groups and obstacles"""
from typing import List

import numpy as np
from pysocialforce.utils import stateutils
from pysocialforce.custom.utils import CustomUtils
from cps.bayesian.model import BayesianModel
from pysocialforce.custom.inspector import add_agent

class PedState:
    """Tracks the state of pedstrains and social groups"""

    def __init__(self, state, groups, config):
        self.default_tau = config("tau", 0.5)
        self.step_width = config("step_width", 0.133)
        self.agent_radius = config("agent_radius", 0.35)
        self.max_speed_multiplier = config("max_speed_multiplier", 1.3)

        self.max_speeds = None
        self.initial_speeds = None

        self.ped_states = []
        self.group_states = []

        self.time_step = 0

        self.update(state, groups)

    def update(self, state, groups):
        self.state = state
        self.groups = groups

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        tau = self.default_tau * np.ones(state.shape[0])
        if state.shape[1] < 9:
            self._state = np.concatenate((state, np.expand_dims(tau, -1)), axis=-1)
        else:
            self._state = state

        if self.initial_speeds is None:            
            self.initial_speeds = self.speeds()

        
        self.max_speeds = self.max_speed_multiplier * self.initial_speeds
        self.ped_states.append(self._state.copy())

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
        
        # if self.time_step == 20:            
        #     next_state, speed = add_agent(next_state, np.array([[3.0, 0.0, 0.0, 0.5, 4.0, 10.0, 2, 1, 3]]))
        #     self.initial_speeds = speed

        self.update(next_state, next_groups)

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

class EnvState:
    """State of the environment obstacles"""

    def __init__(self, obstacles, resolution=10):
        self.resolution = resolution
        self.obstacles = obstacles
        self.obstacles_line = obstacles
        obstacles_min, obstacles_max = [], []
        
        for obstacle in obstacles:
            obstacles_min.append([obstacle[0], obstacle[2]])
            obstacles_max.append([obstacle[1], obstacle[3]])
        self.obstacles_min = np.array(obstacles_min)
        self.obstacles_max = np.array(obstacles_max)
                        

    @property
    def obstacles(self) -> List[np.ndarray]:
        """obstacles is a list of np.ndarray"""
        return self._obstacles

    @obstacles.setter
    def obstacles(self, obstacles):
        """Input an list of (startx, endx, starty, endy) as start and end of a line"""
        if obstacles is None:
            self._obstacles = []
        else:
            self._obstacles = []
            for startx, endx, starty, endy in obstacles:
                samples = int(np.linalg.norm((startx - endx, starty - endy)) * self.resolution)
                line = np.array(
                    list(
                        zip(np.linspace(startx, endx, samples), np.linspace(starty, endy, samples))
                    )
                )
                self._obstacles.append(line)
