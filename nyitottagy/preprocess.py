import pandas as pd
import numpy as np


data = pd.read_csv("data.csv")

cols_1 = ['msec', 'x_position', 'y_position', 'z_position', 'subject', 'trial']
cols = ["x_position","y_position","z_position"]

data = data.loc[data["entity_id"] == 0].drop_duplicates().reset_index(drop = True)
data = data.loc[:,cols_1]

for i in ["x_position", "y_position","z_position"]:
    data[i] = data[i].astype(np.float32)

data["msec"] = data["msec"].astype(np.int32)
data["trial"] = data["trial"].astype(np.int8)
data["subject"] = data["subject"].astype("category")

data.to_pickle("data.pkl")