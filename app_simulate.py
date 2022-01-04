import numpy as np
from pysocialforce.simulator import Simulator
import json
from pysocialforce.data.peds import Pedestrians
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


vid_path = os.path.abspath("C:\\Users\\yoon9\\OneDrive\\연구\\pandemic\\data\\ped_texas\\origin\\opossite")

hp_path = os.path.join(vid_path, idx+"\\"+idx+"_hp.csv")
vp_path = os.path.join(vid_path, idx+"\\"+idx+"_vp.csv")

v = VideoData(hp_path, vp_path)


result_path = "data\\result\\"+idx+"_"+force_idx
if not os.path.exists(result_path):
    os.mkdir(result_path)

v.to_json(result_path+"/data_"+idx+".json")    


with open(result_path+'/data_'+idx+'.json', 'r') as f:
    json_data = json.load(f)


v.trajectory_to_json(result_path+"/gt_"+idx+".json")

# initialize
peds = Pedestrians(json_data)
# obs = [[4, 4, -5, 14], [-4, -4, -5, 0], [-4, -4, 4, 14]]
obs = [
    [4, 4, -5, 14],
    [-4, -4, -5, 0], 
    [-4, -4, 2, 9], 
    [-4, -4, 11, 14],
    [-3.5, -5, 2, 2],
    [-3.5, -5, 9, 9]
    ]

s = Simulator(
    peds,
    obstacles=obs,
    time_table=v.time_table
    # time_table = None
)

s.simulate()

s.result_to_json(result_path+"/result_"+idx+".json")


with SceneVisualizer(s.peds, s, result_path+"/animate_"+idx) as sv:
    sv.animate()        

with SceneVisualizer(s.peds, s, result_path+"/plot_"+idx) as sv:
    sv.plot()




    

