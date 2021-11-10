from pysocialforce.utils import stateutils
import numpy as np

def get_distance_of_state(state):
    return stateutils.desired_directions(state)[1]


def get_diff_of_peds(state):
    diff = stateutils.vec_diff(state[:,:2])
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
    return distance


def get_num_of_peds_with_threshold(state, threshold):
    distance = get_diff_of_peds(state)
    num_list = []
    for ped_distance in distance:        
        distance_mask = ped_distance < threshold
        num_list.append(len(ped_distance[distance_mask])-1)
    return num_list