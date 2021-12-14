import pysocialforce as psf


class Agent(object):
    def __init__(self, initial_state):
        self.state = initial_state
        self.state_record = []

    # numpy로 바꿔주는 
    def np_state(self):
        pass

    # numpy 데이터를 업데이트 함
    def update(self, data):
        pass

    # 이번 타이밍에 나타났는지 여부 -> inital state 정보를 받아오기 위함
    def changed_visible(self, data):
        pass

    def changed_invisible(self, data):
        pass


    @property
    def id(self):
        return self.state.get("id")

    @property
    def px(self):
        return self.state.get("px")    

    @property
    def py(self):
        return self.state.get("py")

    @property
    def vx(self):
        return self.state.get("vx")

    @property
    def vy(self):
        return self.state.get("vy")

    @property
    def gx(self):
        return self.state.get("gx")

    @property
    def gy(self):
        return self.state.get("gy")

    @property
    def distancing(self):
        return self.state.get("distancing")

    @property
    def visible(self):
        return self.state.get("visible")

    @property
    def tau(self):
        return self.state.get("tau")

    @id.setter
    def id(self, data):
        self.state["id"] = data

    @px.setter
    def px(self, data):
        self.state["px"] = data

    @py.setter
    def py(self, data):
        self.state["py"] = data

    @vx.setter
    def vx(self, data):
        self.state["vx"] = data

    @vy.setter
    def vy(self, data):
        self.state["vy"] = data

    @gx.setter
    def gx(self, data):
        self.state["gx"] = data

    @gy.setter
    def gy(self, data):
        self.state["gy"] = data

    @distancing.setter
    def distancing(self, data):
        self.state["distancing"] = data

    @visible.setter
    def visible(self, data):
        self.state["visible"] = data

    @tau.setter
    def tau(self, data):
        self.state["tau"] = data