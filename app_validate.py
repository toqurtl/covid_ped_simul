import sys
import json
import numpy as np
from pysocialforce.video.result_data import ResultData

idx = sys.argv[1]

if len(sys.argv) > 2:
    force_idx = sys.argv[2]
else:
    force_idx = 0

result_path = "data\\result\\"+idx+"_"+force_idx

gt_path = result_path+"/gt_"+idx+".json"
origin_path = result_path+"/result_"+idx+".json"

result_data = ResultData(origin_path, gt_path)

print(result_data.risk_index_of_scene(2))