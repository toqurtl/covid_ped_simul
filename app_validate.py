import sys
import json
import numpy as np
from pysocialforce.video.result_data import ResultData

idx = sys.argv[1]


gt_path = "data/result/"+idx+"/gt_"+idx+".json"
origin_path = "data/result/"+idx+"/result_"+idx+".json"


result_data = ResultData(origin_path, gt_path)

for person_idx in range(0, result_data.num_person):
    print(result_data.ade_of_person(person_idx))

print(result_data.ade_of_scene())

