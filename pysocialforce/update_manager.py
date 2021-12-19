import numpy as np
from pysocialforce.data.parameters import DataIndex as Index


class UpdateManager(object):
    # check functions
    @classmethod
    def is_started(cls, state: np.ndarray, time_step):
        return state[:, Index.start_time.index] <= time_step

    @classmethod
    def is_arrived(cls, state: np.ndarray):
        vecs = state[:,4:6] - state[:, 0:2]        
        distance_to_target = np.array([np.linalg.norm(line) for line in vecs])
        return distance_to_target < 0.5

    # TODO - 여러 목적지일 때는 변경해야 함
    @classmethod
    def is_finished(cls, state: np.ndarray):        
        return cls.is_arrived(state)

    @classmethod
    def is_visible(cls, state: np.ndarray, time_step):
        time_cond = cls.is_started(state, time_step)
        not_finish_cond = np.logical_not(cls.is_finished(state))                
        return np.logical_and(time_cond, not_finish_cond)

    # get_idx functions
    @classmethod
    def update_finished(cls, state: np.ndarray):
        finish_cond = cls.is_finished(state)
        state[:, Index.finished.index] = finish_cond * 1
        for data in state:
            if data[Index.id.index] in cls.finished_idx(state):
                data[Index.visible.index] = 0        
        return state

    @classmethod
    def update_visible(cls, state: np.ndarray, time_step):
        visible_cond = cls.is_visible(state, time_step)
        state[:, Index.visible.index] = visible_cond * 1
        return state

    @classmethod
    def update_new_peds(cls, state:np.ndarray, time_step):
        start_time_cond = UpdateManager.is_started(state, time_step)
        state[:, Index.visible.index] = start_time_cond * 1
        return state

    @classmethod
    def new_state(cls, whole_state, next_state):
        id_index = next_state[:, Index.id.index].astype(np.int64)        
        whole_state[id_index] = next_state
        return whole_state

    @classmethod
    def finished_idx(cls, state: np.ndarray):
        finished_peds = state[state[:, Index.finished.index] == 1]
        return finished_peds[:, Index.id.index].astype(np.int64)

    # result_functions
    @classmethod
    def get_visible(cls, state: np.ndarray):
        return state[state[:, Index.visible.index] == 1]

    @classmethod
    def get_visible_idx(cls, state: np.ndarray):
        visible_peds = cls.get_visible(state)
        return visible_peds[:, Index.id.index].astype(np.int64)