from pathlib import Path
import numpy as np
import pysocialforce as psf
from pysocialforce.forces import Force, PedRepulsiveForce
from pysocialforce.potentials import PedPedPotential
from pysocialforce.utils import Config, stateutils, logger
from pysocialforce.fieldofview import FieldOfView
from pysocialforce.custom import utils


if __name__ == "__main__":
    # def perp(a):
    #     b = np.empty_like(a)
    #     b[0] = -a[1]
    #     b[1] = a[0]
    #     return b

    # line_1 = np.array([[0,0],[0,5]])
    # line_2 = np.array([[2,2],[2,-1]])
    # da = line_1[1] - line_1[0]
    # db = line_2[1] - line_2[0]
    # dp = line_1[0] - line_2[0]
    # dap = perp(da)
    # print(dap)
    # print(db)
    # denom = np.dot(dap, db)
    # if denom == 0:
    #     print('fuck')
    #     print('not inter')
    # else:
    #     num = np.dot(dap, dp)
    #     inter = (num/denom.astype(float))*db + line_2[0]
    #     if (inter[0] - line_1[0][0]) * (inter[0]-line_1[1][0]) > 0:
    #         print('not inter')
    #     if (inter[0] - line_2[0][0]) * (inter[0]-line_2[1][0]) > 0:
    #         print('not inter')
    # exit()
    # initial states, each entry is the position, velocity and goal of a pedestrian in the form of (px, py, vx, vy, gx, gy)
    # add(alpha, beta)
    initial_state = np.array(
        [
            [0.0, 20, -0.5, -0.5, 0.0, 0.0],
            [0.5, 20, -0.5, -0.5, 0.5, 0.0],
            [0, 0.0, 0.0, 0.5, 1.0, 10.0],
            [0.5, 0.0, 0.0, 0.5, 1.0, 10.0],
            # [1.0, 0.0, 0.0, 0.5, 2.0, 10.0],
            # [2.0, 0.0, 0.0, 0.5, 3.0, 10.0],
            # [3.0, 0.0, 0.0, 0.5, 4.0, 10.0],
        ]
    )
    # social groups informoation is represented as lists of indices of the state array
    groups = [[0], [1], [2]]
    # list of linear obstacles given in the form of (x_min, x_max, y_min, y_max)
    obs = [[-1, -1, -1, 11], [3, 3, -1, 11]]
    # obs = [[1, 2, 7, 8]]
    # obs = None
    # initiate the simulator,
    s = psf.Simulator(
        initial_state,
        # groups=groups,
        obstacles=obs,
        config_file=Path(__file__).resolve().parent.joinpath("sample/example.toml"),
    )
    
    utils.field_of_view(s.peds, s.env)
    s.step_once()
    # update 80 steps
    # s.step(150)


    # with psf.plot.SceneVisualizer(s, "images/exmaple") as sv:
    #     sv.animate()
    #     sv.plot()
