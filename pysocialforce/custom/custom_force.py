from pysocialforce.forces import Force
from pysocialforce.custom.utils import CustomUtils
import numpy as np

class DistancingForceOne(Force):
    def _get_force(self):
        # fov = CustomUtils.field_of_view(self.peds, self.scene.env)
        # desired_direction = self.peds.desired_directions()
        distance_mat = CustomUtils.get_distance_matrix(self.peds)        
        desired_social_distance = self.peds.state[:, -1:]
        
        in_desired_distance = distance_mat < desired_social_distance
        np.fill_diagonal(in_desired_distance, False)
        in_desired_distance = in_desired_distance.astype(int)

        angle_matrix = CustomUtils.get_angle_matrix(self.peds)

        term_1 = 0.5 * (distance_mat - desired_social_distance)
        term_2 = 0 + (1-0)*(1 + angle_matrix)/2
        term = term_1 * term_2 * in_desired_distance
        term = np.repeat(np.expand_dims(term, axis=2), 2, axis=2)
        e_ij = CustomUtils.ped_directions(self.peds)   
        return np.sum(e_ij * term, axis=1)
