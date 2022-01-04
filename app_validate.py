import sys
import json
import numpy as np
import os
from pysocialforce.video.result_data import ResultData

idx = sys.argv[1]

if len(sys.argv) > 2:
    force_idx = sys.argv[2]
else:
    force_idx = str(0)

with open("setting.json", 'r') as f:
    setting_data = json.load(f)

result_folder_path = setting_data["path"]["result_folder_path"]

result_path = os.path.join(result_folder_path, idx+"_"+force_idx)

gt_path = result_path+"/gt_"+idx+".json"
origin_path = result_path+"/result_"+idx+".json"
valid_path = result_path+"/valid_"+idx+"_"+force_idx+".json"

result_data = ResultData(origin_path, gt_path)
result_data.to_json(valid_path, idx, force_idx)