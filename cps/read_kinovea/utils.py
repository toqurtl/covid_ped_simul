import pandas as pd
import numpy as np

def to_numpy(file_path):
    data = pd.read_csv("vids/32/32_vp.csv")
    data = data.to_numpy()
    