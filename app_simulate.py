import numpy as np
from pysocialforce.new_simulator import NewSimulator
import json
from pysocialforce.data.peds import Pedestrians
from pysocialforce.video.video_data import VideoData
from pysocialforce.utils.new_plot import SceneVisualizer
import sys

np.set_printoptions(formatter={'float_kind': lambda x: "{0:0.3f}".format(x)})


idx = sys.argv[1]



v = VideoData("vids/"+idx+"/"+idx+"_hp.csv", "vids/"+idx+"/"+idx+"_vp.csv")
v.to_json("data/result/"+idx+"/data_"+idx+".json")    


with open('data/result/'+idx+'/data_'+idx+'.json', 'r') as f:
    json_data = json.load(f)


v.trajectory_to_json("data/result/"+idx+"/gt_"+idx+".json")

# initialize
peds = Pedestrians(json_data)
# obs = [[4, 4, -5, 14], [-4, -4, -5, 0], [-4, -4, 4, 14]]
obs = [
    [4, 4, -5, 14],
    [-4, -4, -5, 0], 
    [-4, -4, 2, 9], 
    [-4, -4, 11, 14],
    [-3, -5, 2, 2],
    [-3, -5, 9, 9]
    ]

s = NewSimulator(
    peds,
    obstacles=obs,
    time_table=v.time_table
    # time_table = None
)

s.simulate()

s.result_to_json("data/result/"+idx+"/result_"+idx+".json")

exit()
# print(s.peds_info.states[-1][0])
# exit()


with SceneVisualizer(s.peds, s, "data/result/"+idx+"/animate") as sv:
    sv.animate()        

with SceneVisualizer(s.peds, s, "data/result/"+idx+"/plot") as sv:
    sv.plot()




    

