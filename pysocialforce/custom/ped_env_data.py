def inspect_state():
    # state가 특정 조건을 만족하는지 검사
    pass

def px(np_state, agent_idx=None):
    if agent_idx == None:
        return np_state[:, 0]
    else:
        return np_state[np_state[:, 8] == agent_idx][0][0]

def py(np_state, agent_idx=None):
    if agent_idx == None:
        return np_state[:, 1]
    else:
        return np_state[np_state[:, 8] == agent_idx][0][1]

def vx(np_state, agent_idx=None):
    if agent_idx == None:
        return np_state[:, 2]
    else:
        return np_state[np_state[:, 8] == agent_idx][0][2]

def vy(np_state, agent_idx=None):
    if agent_idx == None:
        return np_state[:, 3]
    else:
        return np_state[np_state[:, 8] == agent_idx][0][3]

def gx(np_state, agent_idx=None):
    if agent_idx == None:
        return np_state[:, 4]
    else:
        return np_state[np_state[:, 8] == agent_idx][0][4]

def gy(np_state, agent_idx=None):
    if agent_idx == None:
        return np_state[:, 5]
    else:
        return np_state[np_state[:, 8] == agent_idx][0][5]

def distancing(np_state, agent_idx=None):
    if agent_idx == None:
        return np_state[:, 6]
    else:
        return np_state[np_state[:, 8] == agent_idx][0][6]

def visible(np_state, agent_idx=None):
    if agent_idx == None:
        return np_state[:, 7]
    else:
        return np_state[np_state[:, 8] == agent_idx][0][7]

