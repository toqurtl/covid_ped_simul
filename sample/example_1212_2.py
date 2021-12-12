from pathlib import Path
import numpy as np
import pandas as pd
import pysocialforce as psf
from pysocialforce.forces import Force, PedRepulsiveForce
from pysocialforce.potentials import PedPedPotential
from pysocialforce.utils import Config, stateutils, logger
from pysocialforce.fieldofview import FieldOfView
from pysocialforce.custom.utils import CustomUtils


if __name__ == "__main__":
    # vp_data = np.loadtxt("vids/32/32_vp.csv", delimiter=",")
    vp_data = pd.read_csv("vids/32/32_vp.csv")
    hp_data = pd.read_csv("vids/32/32_hp.csv")
    vp_data = vp_data.to_numpy()
    vp_data = vp_data[~np.isnan(vp_data).any(axis=1)]
    hp_data = hp_data.to_numpy()
    hp_data = hp_data[~np.isnan(hp_data).any(axis=1)]
    v_diff = vp_data[-1] - vp_data[0]
    vv_1, vv_2 = v_diff[1]/v_diff[0]*1000, v_diff[2]/v_diff[0]*1000
    h_diff = hp_data[-1] - hp_data[0]
    hv_1, hv_2 = h_diff[1]/h_diff[0]*1000, h_diff[2]/h_diff[0]*1000
    num_step = len(hp_data)
    print(num_step)
    # initial states, each entry is the position, velocity and goal of a pedestrian in the form of (px, py, vx, vy, gx, gy)
    # 7th -> d_0
    # []
    initial_state = np.array(
        [
            [hp_data[0,1], vp_data[0,1], hv_1, vv_1, hp_data[-1,1], vp_data[-1,1], 2],
            [hp_data[0,2], vp_data[0,2], hv_2, vv_2, hp_data[-1,2], vp_data[-1,2], 2],
            # [1.56, -0.42, 0.0, 0.957, 2.29, 18.46, 2],
            # [0.5, 10, -0.5, -0.5, 0.5, 0.0, 2],
            # [0, 0.0, 0.0, 0.5, 0.0, 10.0, 4],
            # [0.5, 0.0, 0.0, 0.5, 1.0, 10.0, 4],
            # [1.0, 0.0, 0.0, 0.5, 2.0, 10.0, 2],
            # [2.0, 0.0, 0.0, 0.5, 3.0, 10.0, 2],
            # [3.0, 0.0, 0.0, 0.5, 4.0, 10.0, 2],
        ]
    )
    # social groups informoation is represented as lists of indices of the state array
    # groups = [[0], [1], [2]]
    # list of linear obstacles given in the form of (x_min, x_max, y_min, y_max)
    obs = [[0, 0, 0, 14], [4, 4, 0, 14]]
    # obs = [[1, 2, 7, 8]]
    # obs = None
    # initiate the simulator,
    s = psf.Simulator(
        initial_state,
        # groups=groups,
        obstacles=obs,
        config_file=Path(__file__).resolve().parent.joinpath("sample/example.toml"),
    )
    
    # update 80 steps
    s.step(num_step-1)
    for i in range(0, num_step-1):
        s.step_once()
    visual = psf.plot.SceneVisualizer(s, "images/exmaple")
    ped_states, group_states = visual.scene.get_states()
    trajectory_x = ped_states[:, 0, 0]
    trajectory_y = ped_states[:, 0, 1] 
    print(len(trajectory_y))   
    # print(visual.states[:, ped_1])
    

    with psf.plot.SceneVisualizer(s, "images/exmaple") as sv:
        sv.animate()        
    
    # with psf.plot.SceneVisualizer(s, "images/plot_example") as sv:
    #     sv.plot()
        
