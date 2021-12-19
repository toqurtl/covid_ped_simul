import numpy as np
from pysocialforce.utils import stateutils


def get_state_of_agent(agent_id, states: np.ndarray):
    return states[states[:, 8]==agent_id]


def visible_peds(states :np.ndarray) -> np.ndarray:
    return states[states[:, 7]==0]


def is_visible(states :np.ndarray):    
    return states[:, 7] == 0


def added_agent(states: np.ndarray, time_step):
    new_agents = states[states[:, 7] == time_step]
    return len(new_agents) > 0, new_agents   


def check_start_time(states: np.ndarray, start_schedule: np.ndarray):
    a = start_schedule.reshape(-1, 1)    


def add_agent(existing_state, new_state: np.ndarray):
    next_state = np.append(existing_state, new_state, axis=0)
    return next_state, stateutils.speeds(next_state)