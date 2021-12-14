import numpy as np


def visible_peds(states :np.ndarray) -> np.ndarray:
    return states[states[:, 7]==0]
    
def non_visible(states :np.ndarray):
    pass

def add_agent(existing_state, new_state: np.ndarray):
    return np.append(existing_state, new_state, axis=0)