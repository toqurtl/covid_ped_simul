import numpy as np


class PedAgent(object):
    def __init__(self, base_data):
        self.base_data = base_data
        self.states = []

    def state_to_list(self):
        return [self.px, self.py, self.vx, self.vy, self.gx, 
            self.gy, self.distancing, self.visible(), self.id, self.tau]

    def state_to_numpy(self):
        return np.array(self.state_to_list())
    
    def add_state(self, state):
        self.states.add(state)
        return

    @property
    def id(self):
        return self.base_data.get("id")

    @property
    def px(self):
        return self.base_data.get("px")    

    @property
    def py(self):
        return self.base_data.get("py")

    @property
    def vx(self):
        return self.base_data.get("vx")

    @property
    def vy(self):
        return self.base_data.get("vy")

    @property
    def gx(self):
        return self.base_data.get("gx")

    @property
    def gy(self):
        return self.base_data.get("gy")

    @property
    def distancing(self):
        return self.base_data.get("distancing")

    @property
    def start_time(self):
        return self.base_data.get("start_time")

    @property
    def tau(self):
        return self.base_data.get("tau")

    @property
    def visible(self):
        if self.start_time == 0:
            return 1
        else:
            return 0
