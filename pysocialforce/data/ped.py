import numpy as np
from .parameters import DataIndex as Index
from pysocialforce.data import parameters

index_list = sorted([index for index in Index], key=lambda data: data.index)


# -1: id, -2: visible, -3: tau
class PedAgent(object):
    def __init__(self, base_data):
        self.base_data = base_data
        self.id = base_data.get(Index.id.str_name)
        self.start_time = base_data.get(Index.start_time.str_name)
        self.states = []        
        self._initialize()

    @property
    def current_state(self):
        return self.states[-1]

    def _initialize(self):
        state = [self.base_data.get(index.str_name) for index in index_list]        
        self.states.append(np.array(state))
        return

    def basic_state(self):
        return np.array([[self.base_data.get(index.str_name) for index in index_list]])

    """ state 검색"""
    def state_at(self, time_step):
        return self.states[time_step]
    
    """ state 추가"""
    def update(self, new_whole_state, time_step):           
        new_state = new_whole_state[self.id]
        return True, np.squeeze(new_state)

    """property들"""
    @property
    def distancing(self):
        return self.current_state.get(Index.distancing.str_name)

    @property
    def tau(self):
        return self.current_state.get(Index.tau.str_name)

    @property
    def px(self):
        return self.current_state[Index.px.index]
    @property
    def py(self):
        return self.current_state[Index.py.index]

    @property
    def vx(self):
        return self.current_state[Index.vx.index]

    @property
    def vy(self):
        return self.current_state[Index.vy.index]

    # TODO - 나중에 step을 받아서 판단하도록 해야함
    @property
    def gx(self):
        return self.current_state[Index.gx.index]

    # TODO - 나중에 step을 받아서 판단하도록 해야함
    @property
    def gy(self):
        return self.current_state[Index.gy.index]

    @property
    def finished(self):
        return self.current_state[Index.finished.index]

    def is_start(self, time_step):
        return self.start_time <= time_step + 1

    def is_finished(self, time_step):
        return self.state_at(time_step)[Index.finished.index]


    def is_visible(self, time_step):
        return self.is_start(time_step) and not self.is_finished(time_step)
