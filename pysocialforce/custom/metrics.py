def average_displacement_error(ped_states, ground_truth_data):
    pass

def final_displacement_error(ped_states, ground_truth_data):
    pass

# ped_states = s.peds.ped_states
# trajectory_1_x, trajectory_1_y = ped_states[:, 0, 0], ped_states[:, 0, 1]
# trajectory_2_x, trajectory_2_y = ped_states[:, 1, 0], ped_states[:, 1, 1]
# d_1_x, d_1_y = np.sum(trajectory_1_x - vp_data[:, 1]) / (num_step-1), np.sum(trajectory_1_y - hp_data[:, 1]) / (num_step-1)
# d_2_x, d_2_y = np.sum(trajectory_2_x - vp_data[:, 2]) / (num_step-1), np.sum(trajectory_2_y - hp_data[:, 2]) / (num_step-1)
# adl_1, adl_2 = (d_1_x**2 + d_1_y**2)**0.5, (d_2_x**2 + d_2_y**2)**0.5

# last_gt_1_x, last_gt_1_y = hp_data[-1:, 1], vp_data[-1:, 1]    
# last_gt_2_x, last_gt_2_y = hp_data[-1:, 2], vp_data[-1:, 2]
# last_pr_1_x, last_pr_1_y = ped_states[-1:, 0, 0], ped_states[-1:, 0, 1]
# last_pr_2_x, last_pr_2_y = ped_states[-1:, 1, 0], ped_states[-1:, 1, 1]
# fdl_1 = ((last_pr_1_x-last_gt_1_x)**2 + (last_pr_1_y-last_gt_1_y)**2)**0.5
# fdl_2 = ((last_pr_2_x-last_gt_2_x)**2 + (last_pr_2_y-last_gt_2_y)**2)**0.5

