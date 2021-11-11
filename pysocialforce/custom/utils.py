from pysocialforce.potentials import PedPedPotential
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

def field_of_view(peds):
    
    # angle
    potential_func = PedPedPotential(peds.step_width, v0=2.1, sigma=0.3)
    f_ab = -1.0 * potential_func.grad_r_ab(peds.state)
    forces_direction = -f_ab
    desired_direction = peds.desired_directions()
    cosphi = np.cos(30 / 180.0 * np.pi)
    in_angle = (
        np.einsum("aj,abj->ab", desired_direction, forces_direction)
        > np.linalg.norm(forces_direction, axis=-1) * cosphi
    )
    # distance
    diff_list = stateutils.vec_diff(peds.state[:,:2])
    person_list = []
    for person_diff in diff_list:
        detail_list = []
        for a in person_diff:
            detail_list.append(np.linalg.norm(a))
        person_list.append(detail_list)
    in_distance = np.array(person_list) < 5    
    np.fill_diagonal(in_distance, False)

    print(in_angle)
    print(in_distance)    
    print(np.logical_and(in_angle, in_distance))
    # obstacle
    print()
