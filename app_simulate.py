import numpy as np
from pysocialforce.simulator import Simulator
import json
from pysocialforce.video.peds import Pedestrians
from pysocialforce.video.video_data import VideoData
from pysocialforce.utils.new_plot import SceneVisualizer
import sys
import os

np.set_printoptions(formatter={'float_kind': lambda x: "{0:0.3f}".format(x)})


idx = sys.argv[1]
if len(sys.argv) > 2:
    force_idx = sys.argv[2]
else:
    force_idx = 0

# Load Setting
with open("setting.json", 'r') as f:
    setting_data = json.load(f)

# Vid Path
vid_path = setting_data["path"]["vid_folder_path"]
vid_path = os.path.abspath(vid_path)
hp_path, vp_path = os.path.join(vid_path, idx, "hp.csv"), os.path.join(vid_path, idx, "vp.csv")
v = VideoData(hp_path, vp_path)

# Result Path
result_folder_path = setting_data["path"]["result_folder_path"]
env_path = os.path.join(result_folder_path, str(idx))
result_path = os.path.join(env_path, str(force_idx))
if not os.path.exists(env_path):
    os.mkdir(env_path)

if not os.path.exists(result_path):
    os.mkdir(result_path)

v.to_json(result_path+"/data_"+idx+".json")    

with open(result_path+'/data_'+idx+'.json', 'r') as f:
    json_data = json.load(f)

v.trajectory_to_json(result_path+"/gt_"+idx+".json")

# initialize
peds = Pedestrians(json_data)

obs = setting_data["obstacles"]

s = Simulator(
    peds,
    obstacles=obs,
    time_table=v.time_table
    # time_table = None
)

s.set_ped_force(int(force_idx))

s.simulate()
print(s.time_step)

s.result_to_json(result_path+"/result_"+idx+".json")


with SceneVisualizer(s.peds, s, result_path+"/animate_"+idx) as sv:
    sv.animate()        

with SceneVisualizer(s.peds, s, result_path+"/plot_"+idx) as sv:
    sv.plot()




    

