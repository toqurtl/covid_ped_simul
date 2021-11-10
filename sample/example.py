from pathlib import Path
import numpy as np
import pysocialforce as psf
from pysocialforce.utils import stateutils
from cps import utils


if __name__ == "__main__":
    # initial states, each entry is the position, velocity and goal of a pedestrian in the form of (px, py, vx, vy, gx, gy)
    initial_state = np.array(
        [
            [0.0, 10, -0.5, -0.5, 0.0, 0.0],
            [0.5, 10, -0.5, -0.5, 0.5, 0.0],
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
        config_file=Path(__file__).resolve().parent.joinpath("example.toml"),
    )
    # update 80 steps
    # s.step(150)
    a = utils.get_num_of_peds_with_threshold(s.peds.state, 5)
    print(a)
    exit()
    print(s.peds.state[:,:2])
    diff = stateutils.vec_diff(s.peds.state[:,:2])
    distance = None
    direction = None
    for d in diff:        
        a, b = stateutils.normalize(d)
        if distance is None:
            # direction = np.expand_dims(a, axis=0)
            distance = b            
            continue
        
        # direction = np.append(direction, [a], axis=0)
        distance = np.vstack((distance, b))
    
    print(direction)
    # print(distance)
    exit()
    # test obstacle force
    for i, p in enumerate(s.peds.pos()):
        print(p)
        
        diff = p-np.vstack(s.get_obstacles())
        directions, dist = stateutils.normalize(diff)
        dist_mask = dist < 5
        
        a = directions[dist_mask] * np.exp(-dist[dist_mask].reshape(-1,1))
        print(np.sum(a, axis=0))
        exit()
        # print(np.vstack(s.get_obstacles()))

    # with psf.plot.SceneVisualizer(s, "images/exmaple") as sv:
    #     sv.animate()
    #     # sv.plot()
