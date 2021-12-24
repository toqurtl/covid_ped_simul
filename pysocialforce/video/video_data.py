import pandas as pd
import numpy as np
import json


class VideoData(object):
    def __init__(self, x_path, y_path):
        self.x_origin: np.ndarray = pd.read_csv(x_path).to_numpy()
        self.y_origin: np.ndarray = pd.read_csv(y_path).to_numpy()
        self.origin_data = {
            "x": self.x_origin,
            "y": self.y_origin
        }

    @property
    def num_person(self):
        _, num_col = self.x_origin.shape
        return num_col - 1

    @property
    def num_data(self):
        return len(self.x_origin)        

    @property
    def time_table(self):
        return np.diff(self.x_origin[:,0])/1000

    @property
    def pos_x(self):
        return self.x_origin[:, 1:]

    @property
    def pos_y(self):
        return self.y_origin[:, 1:]

    @property
    def position_vec(self):
        return np.stack((self.x_origin[:, 1:],self.y_origin[:, 1:]), axis=-1)

    @property
    def velocity_vec(self):
        time = np.stack((self.time_table, self.time_table), axis=-1)
        time = np.expand_dims(time, axis=1)
        return np.diff(self.position_vec, axis=0) / time

    # 한 장면만 나온 경우 문제 생김(데이터 검사할 때 필요)
    @property
    def initial_direction(self):
        directions = []    
        for person_idx in range(0, self.num_person):
            start_index = self.start_time_array[person_idx]
            start_pos = self.position_vec[start_index][person_idx]
            next_pos = self.position_vec[start_index+1][person_idx]
            directions.append(next_pos - start_pos)

        return directions / np.expand_dims(np.linalg.norm(directions, axis=1), axis=1)

    @property
    def average_velocity(self):                
        return np.nanmean(self.velocity_vec, axis=0)

    @property
    def initial_speed(self):
        average_speed = np.linalg.norm(self.average_velocity, axis=1)        
        return np.expand_dims(average_speed, axis=1) * self.initial_direction

    @property
    def start_time_array(self):
        start_time_list = []
        for person_idx in range(0, self.num_person):
            start_time, _ = self.represent_time(self.pos_x[:, person_idx])
            start_time_list.append(start_time)
        return np.array(start_time_list)
        


    def initial_state(self):
        state = {}
        for idx in range(0, self.num_person):            
            x_data, y_data = self.x_origin[:, idx+1], self.y_origin[:, idx+1]            
            state[idx] = {}
            state[idx]["id"] = idx
            state[idx]["px"] = self.initial_pos(x_data)
            state[idx]["py"] = self.initial_pos(y_data)
            state[idx]["vx"] = self.initial_speed[idx][0]
            state[idx]["vy"] = self.initial_speed[idx][1]
            state[idx]["gx"] = self.goal_pos(x_data)
            state[idx]["gy"] = self.goal_pos(y_data)
            state[idx]["distancing"] = 2
            start, _ = self.represent_time(x_data)
            state[idx]["start_time"] = start
            state[idx]["visible"] = int(start == 0)
            state[idx]["tau"] = 0.5
            state[idx]["finished"] = 0
        
        return state
            
    def ground_truth(self):
        x_data, y_data = self.x_origin[:, 1:], self.y_origin[:, 1:]
        states = []
        for x, y in zip(x_data, y_data):
            state = []
            for idx in range(0, self.num_person):
                state.append([x[idx], y[idx]])
            states.append(state)        
        return np.array(states)

    def represent_time(self, pos_data):
        represent_idx_list = []        
        for idx, data in enumerate(pos_data):
            if ~np.isnan(data):
                represent_idx_list.append(idx)
        return represent_idx_list[0], represent_idx_list[-1]
    
    def initial_pos(self, pos_data):
        start_idx, finish_idx = self.represent_time(pos_data)
        return pos_data[start_idx]
    
    def goal_pos(self, pos_data):
        start_idx, finish_idx = self.represent_time(pos_data)
        return pos_data[finish_idx]

    def speed_at(self, pos_data):
        print(np.average(pos_data[0:10]))


    def to_json(self, file_path):
        state = self.initial_state()
        with open(file_path, 'w') as f:
            json.dump(state, f, indent=4)
        return
        
    def trajectory_to_json(self, file_path):
        result_data = {}
        
        for time_idx, step_width in enumerate(self.time_table):
            result_data[time_idx] = {}
            states = []
            for ped_idx in range(0, self.num_person):
                state = [] 
                x_data = self.x_origin[:, ped_idx+1]
                start, finish = self.represent_time(x_data)              
                px = self.x_origin[time_idx][ped_idx+1]
                py = self.y_origin[time_idx][ped_idx+1]
                if np.isnan(px):
                    visible = 0
                else:
                    visible = 1
                
                if finish > time_idx:
                    finish_value = 1
                else:
                    finish_value = 0
                if visible == 1:
                    state.append(px)
                    state.append(py)
                else:
                    state.append(0)
                    state.append(0)
                for i in range(0, 6):
                    state.append(0)
                state.append(visible)
                state.append(start)
                state.append(ped_idx)
                state.append(finish_value)
                states.append(state)
                
            
            result_data[time_idx] ={
                "step_width": step_width,
                "states": states
            }        
        with open(file_path, 'w') as f:
            json.dump(result_data, f, indent=4)
        return
    